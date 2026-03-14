import { useQuery } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { Portfolio } from "@/types/portfolio";
import { API_ENDPOINTS } from "@/lib/constants";

export function usePortfolio() {
  return useQuery({
    queryKey: ["portfolio"],
    queryFn: async () => {
      // For development, return mock data since API doesn't exist yet
      if (process.env.NODE_ENV === "development") {
        return {
          data: {
            totalValue: 1250000,
            availableMargin: 250000,
            usedMargin: 1000000,
            unrealizedPnl: 150000,
            dailyPnl: 45000,
            dailyPnlPct: 3.75,
            positions: [
              {
                id: "pos_1",
                assetSymbol: "RMA-FCB",
                assetName: "Real Madrid vs Barcelona",
                direction: "LONG",
                entryPrice: 100000,
                currentPrice: 120000,
                quantity: 1,
                leverage: 1,
                unrealizedPnl: 20000,
                unrealizedPnlPct: 20,
                status: "ACTIVE",
                createdAt: new Date().toISOString(),
              },
              {
                id: "pos_2",
                assetSymbol: "CMR-NGA",
                assetName: "Cameroon vs Nigeria",
                direction: "SHORT",
                entryPrice: 50000,
                currentPrice: 40000,
                quantity: 1,
                leverage: 1,
                unrealizedPnl: 10000,
                unrealizedPnlPct: 20,
                status: "ACTIVE",
                createdAt: new Date().toISOString(),
              },
            ],
          } as Portfolio,
        };
      }
      return apiClient.get<Portfolio>(API_ENDPOINTS.PORTFOLIO.SUMMARY);
    },
    staleTime: 1000 * 60, // 1 minute
  });
}
