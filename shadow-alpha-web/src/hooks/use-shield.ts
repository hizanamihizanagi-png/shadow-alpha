import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/constants";

interface ShieldQuote {
  position_id: string;
  premium: string;
  coverage_pct: number;
  estimated_payout: string;
  loss_probability: number;
}

export function useShieldQuote(positionId: string, enabled = false) {
  return useQuery({
    queryKey: ["shield", "quote", positionId],
    queryFn: async () => {
      const endpoint = `${API_ENDPOINTS.SHIELD.QUOTE}?position_id=${positionId}`;
      return apiClient.get<ShieldQuote>(endpoint);
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
      return apiClient.post(`${API_ENDPOINTS.SHIELD.CLAIM}/${contractId}`, {});
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["shield"] });
    },
  });
}

export function useShieldContracts() {
  return useQuery({
    queryKey: ["shield", "contracts"],
    queryFn: async () => {
      return apiClient.get(API_ENDPOINTS.SHIELD.CONTRACTS);
    },
    staleTime: 1000 * 30,
  });
}
