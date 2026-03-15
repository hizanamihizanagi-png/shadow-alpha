import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { PortfolioSummary } from "@/types/portfolio";
import { API_ENDPOINTS } from "@/lib/constants";

const toNumber = (value: unknown) => {
  if (typeof value === "number") return value;
  if (typeof value === "string") return Number(value);
  return 0;
};

export function usePortfolio() {
  return useQuery({
    queryKey: ["portfolio"],
    queryFn: async () => {
      const res = await apiClient.get<Record<string, unknown>>(
        API_ENDPOINTS.PORTFOLIO.SUMMARY,
      );
      const data = res.data || {};
      const totalValue = toNumber(data.total_value ?? data.totalValue);
      const totalInvested = toNumber(data.total_invested ?? data.totalInvested);
      const unrealizedPnl = toNumber(data.unrealized_pnl ?? data.unrealizedPnl);
      const positionCount = toNumber(data.position_count ?? data.positionCount);
      const activeCount = toNumber(data.active_count ?? data.activeCount);
      const wonCount = toNumber(data.won_count ?? data.wonCount);
      const lostCount = toNumber(data.lost_count ?? data.lostCount);
      const winRate = toNumber(data.win_rate ?? data.winRate);

      const availableMargin = totalValue;
      const usedMargin = totalInvested;
      const dailyPnl = unrealizedPnl;
      const dailyPnlPct =
        totalInvested > 0 ? (unrealizedPnl / totalInvested) * 100 : 0;

      const summary: PortfolioSummary = {
        totalValue,
        totalInvested,
        unrealizedPnl,
        positionCount,
        activeCount,
        wonCount,
        lostCount,
        winRate,
        availableMargin,
        usedMargin,
        dailyPnl,
        dailyPnlPct,
      };

      return { data: summary };
    },
    staleTime: 1000 * 60, // 1 minute
  });
}
