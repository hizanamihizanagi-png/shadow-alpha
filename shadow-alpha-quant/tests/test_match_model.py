"""
Tests for the Dixon-Coles Bivariate Poisson Match Model.
"""

import numpy as np
import pytest
from quant.match_model import (
    DixonColesModel,
    MatchPrediction,
    _tau,
    bayesian_update_after_goal,
    predict_match,
    score_matrix,
)


class TestTauCorrection:
    """Dixon-Coles τ correction factor tests."""

    def test_tau_0_0(self):
        """τ(0,0) = 1 - λ₁·λ₂·ρ."""
        result = _tau(0, 0, 1.5, 1.2, -0.04)
        expected = 1.0 - 1.5 * 1.2 * (-0.04)
        assert result == pytest.approx(expected)

    def test_tau_1_0(self):
        """τ(1,0) = 1 + λ₂·ρ."""
        result = _tau(1, 0, 1.5, 1.2, -0.04)
        expected = 1.0 + 1.2 * (-0.04)
        assert result == pytest.approx(expected)

    def test_tau_0_1(self):
        """τ(0,1) = 1 + λ₁·ρ."""
        result = _tau(0, 1, 1.5, 1.2, -0.04)
        expected = 1.0 + 1.5 * (-0.04)
        assert result == pytest.approx(expected)

    def test_tau_1_1(self):
        """τ(1,1) = 1 - ρ."""
        result = _tau(1, 1, 1.5, 1.2, -0.04)
        expected = 1.0 - (-0.04)
        assert result == pytest.approx(expected)

    def test_tau_high_scores_unchanged(self):
        """τ(x,y) = 1 for x>1 or y>1."""
        for x, y in [(2, 0), (0, 2), (2, 3), (5, 5)]:
            assert _tau(x, y, 1.5, 1.2, -0.04) == 1.0


class TestScoreMatrix:
    """Score probability matrix tests."""

    def test_probabilities_sum_to_one(self):
        """Full score matrix should sum to approximately 1.0."""
        mat = score_matrix(1.5, 1.2, rho=-0.04)
        total = mat.sum()
        assert total == pytest.approx(1.0, abs=1e-6)

    def test_matrix_shape(self):
        """Matrix shape should be (MAX_GOALS+1, MAX_GOALS+1)."""
        mat = score_matrix(1.5, 1.2)
        assert mat.shape == (11, 11)  # MAX_GOALS = 10

    def test_all_probabilities_non_negative(self):
        """All probabilities should be >= 0."""
        mat = score_matrix(1.5, 1.2, rho=-0.04)
        assert np.all(mat >= 0)

    def test_rho_zero_approximately_independent(self):
        """With ρ=0, result should match independent Poisson."""
        mat = score_matrix(1.5, 1.2, rho=0.0)
        # P(0,0) with independent Poisson
        from scipy.stats import poisson
        expected_00 = poisson.pmf(0, 1.5) * poisson.pmf(0, 1.2)
        # Allow small renormalization tolerance
        assert mat[0, 0] == pytest.approx(expected_00, rel=0.01)


class TestPredictMatch:
    """Convenience predict_match function tests."""

    def test_returns_match_prediction(self):
        pred = predict_match("PSG", "Marseille", 1.0, (0, 0), 1.8, 1.1)
        assert isinstance(pred, MatchPrediction)

    def test_outcome_probs_sum_to_one(self):
        """Home win + Draw + Away win ≈ 1.0."""
        pred = predict_match("Arsenal", "Chelsea", 1.0, (0, 0), 1.6, 1.3)
        total = pred.home_win_prob + pred.draw_prob + pred.away_win_prob
        assert total == pytest.approx(1.0, abs=0.01)

    def test_home_advantage(self):
        """With higher λ_home, P(home win) > P(away win)."""
        pred = predict_match("Home", "Away", 1.0, (0, 0), 2.0, 1.0)
        assert pred.home_win_prob > pred.away_win_prob

    def test_time_remaining_narrows_distribution(self):
        """Less time remaining -> higher probability of current scoreline holding."""
        pred_full = predict_match("H", "A", 1.0, (1, 0), 1.5, 1.2)
        pred_late = predict_match("H", "A", 0.1, (1, 0), 1.5, 1.2)
        # With 10% time left and 1-0, P(1-0 final) should be higher
        p_10_full = pred_full.score_matrix[1, 0] if pred_full.score_matrix.shape[0] > 1 else 0
        p_10_late = pred_late.score_matrix[1, 0] if pred_late.score_matrix.shape[0] > 1 else 0
        assert p_10_late > p_10_full

    def test_current_score_shifts_distribution(self):
        """Starting at (2, 0) should make P(home win) very high."""
        pred = predict_match("H", "A", 0.5, (2, 0), 1.5, 1.2)
        assert pred.home_win_prob > 0.7  # 2-0 up with half time left

    def test_top_scores_returns_sorted(self):
        """top_scores() should return scores ordered by probability."""
        pred = predict_match("H", "A", 1.0, (0, 0), 1.5, 1.2)
        top = pred.top_scores(5)
        probs = [p for (_, p) in top]
        assert probs == sorted(probs, reverse=True)


class TestBayesianUpdate:
    """Bayesian live updating tests."""

    def test_home_goal_increases_home_win_prob(self):
        """After a home goal, P(home win) should increase."""
        pred_before = predict_match("H", "A", 0.6, (0, 0), 1.5, 1.2)
        pred_after = bayesian_update_after_goal(
            pred_before, "home",
            lambda_home_full=1.5,
            lambda_away_full=1.2,
            new_time_remaining=0.55,
        )
        assert pred_after.home_win_prob > pred_before.home_win_prob

    def test_away_goal_decreases_home_win_prob(self):
        """After an away goal, P(home win) should decrease."""
        pred_before = predict_match("H", "A", 0.6, (0, 0), 1.5, 1.2)
        pred_after = bayesian_update_after_goal(
            pred_before, "away",
            lambda_home_full=1.5,
            lambda_away_full=1.2,
            new_time_remaining=0.55,
        )
        assert pred_after.home_win_prob < pred_before.home_win_prob

    def test_score_updates_correctly(self):
        """Current score should reflect the new goal."""
        pred = predict_match("H", "A", 0.6, (1, 1), 1.5, 1.2)
        updated = bayesian_update_after_goal(
            pred, "home",
            lambda_home_full=1.5,
            lambda_away_full=1.2,
            new_time_remaining=0.5,
        )
        assert updated.current_score == (2, 1)


class TestDixonColesModel:
    """Full model fitting tests."""

    @pytest.fixture
    def sample_data(self):
        """Small synthetic dataset for model fitting."""
        return [
            # (home, away, home_goals, away_goals, days_ago)
            ("Arsenal", "Chelsea", 2, 1, 30),
            ("Chelsea", "Arsenal", 1, 1, 60),
            ("Arsenal", "Liverpool", 3, 1, 20),
            ("Liverpool", "Arsenal", 0, 2, 45),
            ("Chelsea", "Liverpool", 1, 0, 10),
            ("Liverpool", "Chelsea", 2, 2, 55),
            ("Arsenal", "Chelsea", 1, 0, 5),
            ("Chelsea", "Liverpool", 0, 1, 15),
            ("Liverpool", "Arsenal", 1, 3, 35),
            ("Arsenal", "Liverpool", 2, 0, 8),
        ]

    def test_fit_returns_self(self, sample_data):
        model = DixonColesModel()
        result = model.fit(sample_data)
        assert result is model

    def test_fitted_model_has_ratings(self, sample_data):
        model = DixonColesModel()
        model.fit(sample_data)
        assert "Arsenal" in model.team_ratings
        assert "Chelsea" in model.team_ratings
        assert "Liverpool" in model.team_ratings

    def test_predict_returns_valid_prediction(self, sample_data):
        model = DixonColesModel()
        model.fit(sample_data)
        pred = model.predict("Arsenal", "Chelsea")
        assert isinstance(pred, MatchPrediction)
        total = pred.home_win_prob + pred.draw_prob + pred.away_win_prob
        assert total == pytest.approx(1.0, abs=0.01)

    def test_predict_with_current_score(self, sample_data):
        model = DixonColesModel()
        model.fit(sample_data)
        pred = model.predict("Arsenal", "Chelsea", time_remaining=0.5, current_score=(1, 0))
        assert pred.current_score == (1, 0)
        assert pred.home_win_prob > 0.3  # leading team should have decent odds

