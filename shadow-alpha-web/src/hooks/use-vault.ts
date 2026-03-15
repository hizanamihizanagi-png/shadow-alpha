import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/constants";

interface VaultPerformance {
  total_deposited: string;
  current_value: string;
  gross_yield: string;
  performance_fee: string;
  net_yield: string;
  apy_estimate: string;
  net_apy: string;
  deposits: Array<{
    id: string;
    amount: string;
    status: string;
    created_at: string;
    withdrawn_at?: string | null;
  }>;
}

export function useVaultPerformance() {
  return useQuery({
    queryKey: ["vault", "performance"],
    queryFn: async () => {
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
    mutationFn: async (depositId: string) => {
      return apiClient.post(API_ENDPOINTS.VAULT.WITHDRAW, {
        deposit_id: depositId,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["vault"] });
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
    },
  });
}
