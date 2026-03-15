"""
Dixon-Coles Bivariate Poisson Match Model
===========================================
Predicts football match scores using the Dixon & Coles (1997) model.

The model extends independent Poisson scoring with:
    1. Team-specific attack (α) and defense (β) ratings
    2. A home-advantage factor (γ)
    3. A low-score correlation parameter (ρ) via the τ correction
    4. Time-weighted MLE for parameter estimation (recent form matters more)

References:
    Dixon, M. & Coles, S. (1997). "Modelling Association Football Scores
    and Inefficiencies in the Football Betting Market."
    Journal of the Royal Statistical Society, Series C, 46(2), 265-280.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple

import numpy as np
from scipy.optimize import minimize
from scipy.stats import poisson

from .utils import poisson_pmf, poisson_pmf_array

# Maximum number of goals per team to consider in distributions
MAX_GOALS = 10


# ---------------------------------------------------------------------------
# Data classes
# ---------------------------------------------------------------------------

@dataclass
class TeamRatings:
    """Attack and defense strengths for a single team."""
    attack: float = 1.0     # α - higher means more goals scored
    defense: float = 1.0    # β - higher means more goals conceded

    def __repr__(self) -> str:
        return f"TeamRatings(atk={self.attack:.3f}, def={self.defense:.3f})"


@dataclass
class MatchPrediction:
    """Full output of a match prediction."""
    score_matrix: np.ndarray            # P(home=i, away=j) matrix
    home_win_prob: float
    draw_prob: float
    away_win_prob: float
    expected_home_goals: float
    expected_away_goals: float
    most_likely_score: Tuple[int, int]
    # Match context
    time_remaining: float
    current_score: Tuple[int, int]

    def outcome_probs(self) -> Dict[str, float]:
        return {
            "home_win": round(self.home_win_prob, 4),
            "draw": round(self.draw_prob, 4),
            "away_win": round(self.away_win_prob, 4),
        }

    def top_scores(self, n: int = 5) -> List[Tuple[Tuple[int, int], float]]:
        """Return the top-N most likely final scores."""
        flat = []
        rows, cols = self.score_matrix.shape
        for i in range(rows):
            for j in range(cols):
                flat.append(((i, j), float(self.score_matrix[i, j])))
        flat.sort(key=lambda x: x[1], reverse=True)
        return flat[:n]


# ---------------------------------------------------------------------------
# τ (tau) correction - Dixon-Coles low-score adjustment
# ---------------------------------------------------------------------------

def _tau(
    x: int, y: int,
    lambda1: float, lambda2: float,
    rho: float,
) -> float:
    """Dixon-Coles τ correction factor for low-scoring matches.

    Modifies P(X=x, Y=y) for (x,y) ∈ {(0,0),(0,1),(1,0),(1,1)}
    to account for the empirical excess of draws and low-score lines.

    Parameters
    ----------
    x, y : int
        Goals for home, away team.
    lambda1, lambda2 : float
        Expected goals for home, away.
    rho : float
        Correlation parameter (typically small, |ρ| < 0.1).

    Returns
    -------
    float
        Multiplicative correction factor.
    """
    if x == 0 and y == 0:
        return 1.0 - lambda1 * lambda2 * rho
    elif x == 0 and y == 1:
        return 1.0 + lambda1 * rho
    elif x == 1 and y == 0:
        return 1.0 + lambda2 * rho
    elif x == 1 and y == 1:
        return 1.0 - rho
    else:
        return 1.0


# ---------------------------------------------------------------------------
# Score probability matrix
# ---------------------------------------------------------------------------

def score_matrix(
    lambda_home: float,
    lambda_away: float,
    rho: float = 0.0,
    max_goals: int = MAX_GOALS,
) -> np.ndarray:
    """Compute the full score probability matrix P(home=i, away=j).

    Parameters
    ----------
    lambda_home : float
        Expected goals for home team (λ₁ = α_home x β_away x γ).
    lambda_away : float
        Expected goals for away team (λ₂ = α_away x β_home).
    rho : float
        Dixon-Coles correlation parameter.
    max_goals : int
        Maximum goals per team to consider.

    Returns
    -------
    np.ndarray of shape (max_goals+1, max_goals+1)
        Matrix where element [i, j] = P(home=i, away=j).
    """
    n = max_goals + 1
    mat = np.zeros((n, n))

    home_pmf = poisson_pmf_array(max_goals, lambda_home)
    away_pmf = poisson_pmf_array(max_goals, lambda_away)

    for i in range(n):
        for j in range(n):
            tau = _tau(i, j, lambda_home, lambda_away, rho)
            mat[i, j] = tau * home_pmf[i] * away_pmf[j]

    # Renormalize to ensure sum = 1 after τ corrections
    total = mat.sum()
    if total > 0:
        mat /= total

    return mat


# ---------------------------------------------------------------------------
# DixonColesModel - parameter estimation
# ---------------------------------------------------------------------------

class DixonColesModel:
    """Full Dixon-Coles model with MLE parameter estimation.

    Usage
    -----
    >>> model = DixonColesModel()
    >>> model.fit(match_data)   # list of (home, away, home_goals, away_goals, days_ago)
    >>> pred = model.predict("Arsenal", "Chelsea", time_remaining=1.0)
    """

    def __init__(self, home_advantage: float = 1.25, rho: float = -0.04):
        self.home_advantage = home_advantage      # γ
        self.rho = rho
        self.team_ratings: Dict[str, TeamRatings] = {}
        self._teams: List[str] = []
        self._fitted = False

    def _get_lambda(self, home: str, away: str) -> Tuple[float, float]:
        """Compute expected goals (λ) for home and away teams."""
        h = self.team_ratings.get(home, TeamRatings())
        a = self.team_ratings.get(away, TeamRatings())

        lambda_home = h.attack * a.defense * self.home_advantage
        lambda_away = a.attack * h.defense

        # Safety clamp
        lambda_home = max(lambda_home, 0.05)
        lambda_away = max(lambda_away, 0.05)

        return lambda_home, lambda_away

    def fit(
        self,
        matches: List[Tuple[str, str, int, int, float]],
        xi: float = 0.005,
    ) -> "DixonColesModel":
        """Fit model parameters via MLE on historical match data.

        Parameters
        ----------
        matches : list of (home_team, away_team, home_goals, away_goals, days_ago)
            Historical match results with recency in days.
        xi : float
            Time-decay parameter. Larger ξ = stronger recency bias.
            Weight = exp(-ξ x days_ago).

        Returns
        -------
        self (fitted model)
        """
        # Collect unique teams
        teams = set()
        for (h, a, *_) in matches:
            teams.add(h)
            teams.add(a)
        self._teams = sorted(teams)
        n_teams = len(self._teams)
        team_idx = {t: i for i, t in enumerate(self._teams)}

        # Parameter vector: [atk_0, ..., atk_{n-1}, def_0, ..., def_{n-1}, gamma, rho]
        # Initial guess: all attacks = 1, all defenses = 1, gamma = 1.25, rho = -0.04
        x0 = np.ones(2 * n_teams + 2)
        x0[-2] = 1.25  # gamma
        x0[-1] = -0.04  # rho

        def neg_log_likelihood(params):
            atk = params[:n_teams]
            dfn = params[n_teams:2 * n_teams]
            gamma = params[-2]
            rho = params[-1]

            ll = 0.0
            for (home, away, hg, ag, days_ago) in matches:
                hi = team_idx[home]
                ai = team_idx[away]

                lam1 = max(atk[hi] * dfn[ai] * gamma, 0.01)
                lam2 = max(atk[ai] * dfn[hi], 0.01)

                weight = math.exp(-xi * days_ago)

                tau = _tau(hg, ag, lam1, lam2, rho)
                if tau <= 0:
                    tau = 1e-10

                p_home = poisson_pmf(hg, lam1)
                p_away = poisson_pmf(ag, lam2)

                prob = tau * p_home * p_away
                if prob <= 0:
                    prob = 1e-15

                ll += weight * math.log(prob)

            # Penalty: mean attack should be ≈ 1 (identifiability)
            mean_atk = np.mean(atk)
            penalty = 100.0 * (mean_atk - 1.0) ** 2

            return -ll + penalty

        # Bounds
        bounds = (
            [(0.01, 5.0)] * n_teams +   # attacks
            [(0.01, 5.0)] * n_teams +   # defenses
            [(0.5, 3.0)] +              # gamma (home advantage)
            [(-0.3, 0.3)]              # rho
        )

        result = minimize(
            neg_log_likelihood,
            x0,
            method="L-BFGS-B",
            bounds=bounds,
            options={"maxiter": 2000, "ftol": 1e-8},
        )

        # Extract parameters
        params = result.x
        for i, team in enumerate(self._teams):
            self.team_ratings[team] = TeamRatings(
                attack=float(params[i]),
                defense=float(params[n_teams + i]),
            )
        self.home_advantage = float(params[-2])
        self.rho = float(params[-1])
        self._fitted = True

        return self

    def predict(
        self,
        home: str,
        away: str,
        time_remaining: float = 1.0,
        current_score: Tuple[int, int] = (0, 0),
    ) -> MatchPrediction:
        """Predict the final score distribution.

        Parameters
        ----------
        home, away : str
            Team names (must be in fitted model, or defaults used).
        time_remaining : float
            Fraction of match remaining (1.0 = full, 0.5 = halftime).
        current_score : (int, int)
            Current score (home_goals, away_goals).

        Returns
        -------
        MatchPrediction
        """
        lambda_home_full, lambda_away_full = self._get_lambda(home, away)

        # Scale by remaining time (Poisson independence of increments)
        lambda_home = lambda_home_full * time_remaining
        lambda_away = lambda_away_full * time_remaining

        # Score matrix for REMAINING goals
        mat_remaining = score_matrix(lambda_home, lambda_away, self.rho)

        # Shift to final scores (add current score)
        ch, ca = current_score
        n = MAX_GOALS + 1
        final_mat = np.zeros((n + ch, n + ca))
        for i in range(n):
            for j in range(n):
                fi = i + ch
                fj = j + ca
                if fi < final_mat.shape[0] and fj < final_mat.shape[1]:
                    final_mat[fi, fj] = mat_remaining[i, j]

        # Trim to standard size
        final_n = MAX_GOALS + max(ch, ca) + 1
        final_n = min(final_n, final_mat.shape[0])
        final_mat = final_mat[:final_n, :final_n]

        # Normalize
        total = final_mat.sum()
        if total > 0:
            final_mat /= total

        # Outcome probabilities
        home_win = 0.0
        draw = 0.0
        away_win = 0.0
        for i in range(final_mat.shape[0]):
            for j in range(final_mat.shape[1]):
                if i > j:
                    home_win += final_mat[i, j]
                elif i == j:
                    draw += final_mat[i, j]
                else:
                    away_win += final_mat[i, j]

        # Most likely score
        flat_idx = np.argmax(final_mat)
        ml_i, ml_j = divmod(flat_idx, final_mat.shape[1])

        return MatchPrediction(
            score_matrix=final_mat,
            home_win_prob=home_win,
            draw_prob=draw,
            away_win_prob=away_win,
            expected_home_goals=lambda_home + ch,
            expected_away_goals=lambda_away + ca,
            most_likely_score=(int(ml_i), int(ml_j)),
            time_remaining=time_remaining,
            current_score=current_score,
        )


# ---------------------------------------------------------------------------
# Convenience wrapper (standalone, no fitted model needed)
# ---------------------------------------------------------------------------

def predict_match(
    team_home: str,
    team_away: str,
    time_remaining: float = 1.0,
    current_score: Tuple[int, int] = (0, 0),
    lambda_home: float = 1.5,
    lambda_away: float = 1.2,
    rho: float = -0.04,
) -> MatchPrediction:
    """Quick match prediction using known scoring intensities.

    Use this when you already have λ values (e.g. from an external model or
    from pre-calibrated lookup). For full model fitting, use DixonColesModel.

    Parameters
    ----------
    team_home, team_away : str
        Team names (metadata only for the result).
    time_remaining : float
        Fraction of match remaining in (0, 1].
    current_score : (int, int)
        Current (home_goals, away_goals).
    lambda_home, lambda_away : float
        Full-match expected goals for each team.
    rho : float
        Dixon-Coles correlation parameter.

    Returns
    -------
    MatchPrediction

    Example
    -------
    >>> pred = predict_match("PSG", "Marseille", 0.5, (1, 0), 1.8, 1.1)
    >>> pred.home_win_prob > pred.away_win_prob
    True
    """
    # Scale lambdas by remaining time
    lam_h = lambda_home * time_remaining
    lam_a = lambda_away * time_remaining

    # Remaining-goals matrix
    mat_remaining = score_matrix(lam_h, lam_a, rho)

    ch, ca = current_score
    n = MAX_GOALS + 1
    final_size = n + max(ch, ca)
    final_mat = np.zeros((final_size, final_size))

    for i in range(n):
        for j in range(n):
            fi, fj = i + ch, j + ca
            if fi < final_size and fj < final_size:
                final_mat[fi, fj] = mat_remaining[i, j]

    # Normalize
    total = final_mat.sum()
    if total > 0:
        final_mat /= total

    # Outcomes
    home_win = draw = away_win = 0.0
    for i in range(final_mat.shape[0]):
        for j in range(final_mat.shape[1]):
            if i > j:
                home_win += final_mat[i, j]
            elif i == j:
                draw += final_mat[i, j]
            else:
                away_win += final_mat[i, j]

    flat_idx = int(np.argmax(final_mat))
    ml_i, ml_j = divmod(flat_idx, final_mat.shape[1])

    return MatchPrediction(
        score_matrix=final_mat,
        home_win_prob=home_win,
        draw_prob=draw,
        away_win_prob=away_win,
        expected_home_goals=lam_h + ch,
        expected_away_goals=lam_a + ca,
        most_likely_score=(int(ml_i), int(ml_j)),
        time_remaining=time_remaining,
        current_score=current_score,
    )


# ---------------------------------------------------------------------------
# Bayesian live updating helper
# ---------------------------------------------------------------------------

def bayesian_update_after_goal(
    prediction: MatchPrediction,
    goal_for: str,
    lambda_home_full: float,
    lambda_away_full: float,
    new_time_remaining: float,
    rho: float = -0.04,
) -> MatchPrediction:
    """Re-compute prediction after a goal is scored.

    Parameters
    ----------
    prediction : MatchPrediction
        Previous prediction state.
    goal_for : str
        "home" or "away" - who scored.
    lambda_home_full, lambda_away_full : float
        Full-match expected goals (used to compute remaining λ).
    new_time_remaining : float
        Updated time remaining (fraction of match).
    rho : float
        Dixon-Coles ρ.

    Returns
    -------
    MatchPrediction
        Updated prediction with new score and probabilities.
    """
    ch, ca = prediction.current_score
    if goal_for.lower() == "home":
        new_score = (ch + 1, ca)
    else:
        new_score = (ch, ca + 1)

    return predict_match(
        team_home="home",
        team_away="away",
        time_remaining=new_time_remaining,
        current_score=new_score,
        lambda_home=lambda_home_full,
        lambda_away=lambda_away_full,
        rho=rho,
    )

