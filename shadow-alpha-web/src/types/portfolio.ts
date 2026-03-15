export interface Position {
  id: string;
  userId: string;
  sportsbook: string;
  teams: string;
  league?: string | null;
  odds: number;
  stake: number;
  maxPayout: number;
  currentValue: number;
  currentProb?: number | null;
  timeRemaining?: number | null;
  status: "active" | "won" | "lost" | "sold" | "settled" | "cancelled" | "locked";
  description?: string | null;
  createdAt: string;
}

export interface PortfolioSummary {
  totalValue: number;
  totalInvested: number;
  unrealizedPnl: number;
  positionCount: number;
  activeCount: number;
  wonCount: number;
  lostCount: number;
  winRate: number;
  availableMargin: number;
  usedMargin: number;
  dailyPnl: number;
  dailyPnlPct: number;
}
