import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/constants";

interface Plan {
  name: string;
  price_fcfa: number;
  features: string[];
}

interface CurrentSubscription {
  id: string;
  plan: string;
  status: string;
  started_at: string;
  expires_at: string | null;
}

export function useSubscriptionPlans() {
  return useQuery({
    queryKey: ["subscription", "plans"],
    queryFn: async () => {
      return apiClient.get<Plan[]>(API_ENDPOINTS.SUBSCRIPTION.PLANS);
    },
    staleTime: 1000 * 60 * 5,
  });
}

export function useCurrentSubscription() {
  return useQuery({
    queryKey: ["subscription", "current"],
    queryFn: async () => {
      return apiClient.get<CurrentSubscription>(API_ENDPOINTS.SUBSCRIPTION.CURRENT);
    },
    staleTime: 1000 * 30,
  });
}

export function useUpgradeSubscription() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (plan: string) => {
      return apiClient.post(API_ENDPOINTS.SUBSCRIPTION.UPGRADE, { plan });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["subscription"] });
    },
  });
}

export function useCancelSubscription() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async () => {
      return apiClient.post(API_ENDPOINTS.SUBSCRIPTION.CANCEL, {});
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["subscription"] });
    },
  });
}
