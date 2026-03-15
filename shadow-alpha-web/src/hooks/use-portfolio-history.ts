import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/constants";

interface PortfolioHistoryResponse {
  count?: number;
  positions?: Array<Record<string, unknown>>;
}

export interface PortfolioHistoryItem {
  id: string;
  teams: string;
  stake: number;
  maxPayout: number;
  status: string;
  pnl: number;
  createdAt?: string;
  updatedAt?: string;
}

const toNumber = (value: unknown) => {
  if (typeof value === "number") return value;
  if (typeof value === "string") return Number(value);
  return 0;
};

export function usePortfolioHistory() {
  return useQuery({
    queryKey: ["portfolio", "history"],
    queryFn: async () => {
      const res = await apiClient.get<PortfolioHistoryResponse>(
        API_ENDPOINTS.PORTFOLIO.HISTORY,
      );
      const payload = res.data || {};
      const positions = Array.isArray(payload.positions) ? payload.positions : [];
      const mapped: PortfolioHistoryItem[] = positions.map((item) => ({
        id: String(item.id ?? ""),
        teams: String(item.teams ?? ""),
        stake: toNumber(item.stake),
        maxPayout: toNumber(item.max_payout ?? item.maxPayout),
        status: String(item.status ?? ""),
        pnl: toNumber(item.pnl),
        createdAt: item.created_at ? String(item.created_at) : undefined,
        updatedAt: item.updated_at ? String(item.updated_at) : undefined,
      }));
      return {
        data: {
          count: toNumber(payload.count),
          positions: mapped,
        },
      };
    },
    staleTime: 1000 * 30,
  });
}
