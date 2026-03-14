import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/constants";

interface ShieldQuote {
  premium: string;
  coverage_pct: number;
  max_payout: string;
  model: string;
}

export function useShieldQuote(positionId: string, enabled = false) {
  return useQuery({
    queryKey: ["shield", "quote", positionId],
    queryFn: async () => {
      if (process.env.NODE_ENV === "development") {
        return {
          data: {
            premium: "3750.00",
            coverage_pct: 70,
            max_payout: "17500.00",
            model: "black_scholes_put",
          } as ShieldQuote,
        };
      }
      return apiClient.post<ShieldQuote>(API_ENDPOINTS.SHIELD.QUOTE, {
        position_id: positionId,
      });
    },
    enabled,
    staleTime: 1000 * 15,
  });
}

export function useActivateShield() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (data: {
      position_id: string;
      coverage_pct: number;
    }) => {
      return apiClient.post(API_ENDPOINTS.SHIELD.ACTIVATE, data);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["shield"] });
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
    },
  });
}

export function useClaimShield() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (contractId: string) => {
      return apiClient.post(API_ENDPOINTS.SHIELD.CLAIM, {
        contract_id: contractId,
      });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["shield"] });
    },
  });
}
