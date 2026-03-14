import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/constants";

interface VaultPerformance {
  total_deposited: string;
  current_value: string;
  net_yield: string;
  apy_estimate: string;
  performance_fee: string;
  deposits: Array<{
    id: string;
    amount: string;
    status: string;
    created_at: string;
  }>;
}

export function useVaultPerformance() {
  return useQuery({
    queryKey: ["vault", "performance"],
    queryFn: async () => {
      if (process.env.NODE_ENV === "development") {
        return {
          data: {
            total_deposited: "750000.00",
            current_value: "812500.00",
            net_yield: "62500.00",
            apy_estimate: "9.75",
            performance_fee: "35",
            deposits: [
              { id: "1", amount: "500000.00", status: "active", created_at: "2025-12-01T00:00:00Z" },
              { id: "2", amount: "250000.00", status: "active", created_at: "2026-01-15T00:00:00Z" },
            ],
          } as VaultPerformance,
        };
      }
      return apiClient.get<VaultPerformance>(API_ENDPOINTS.VAULT.PERFORMANCE);
    },
    staleTime: 1000 * 30,
  });
}

export function useVaultDeposit() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (amount: string) => {
      return apiClient.post(API_ENDPOINTS.VAULT.DEPOSIT, { amount });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vault"] });
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
    },
  });
}

export function useVaultWithdraw() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (amount: string) => {
      return apiClient.post(API_ENDPOINTS.VAULT.WITHDRAW, { amount });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vault"] });
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
    },
  });
}
