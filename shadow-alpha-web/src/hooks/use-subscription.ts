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
      if (process.env.NODE_ENV === "development") {
        return {
          data: [
            { name: "free", price_fcfa: 0, features: ["3 positions/jour", "Analytics de base", "Accès communautaire"] },
            { name: "alpha", price_fcfa: 2500, features: ["10 positions/jour", "Pricing engine live", "Score de crédit", "Groupes tontine"] },
            { name: "premier", price_fcfa: 7500, features: ["Positions illimitées", "Shield insurance", "Position loans", "Copy-trading", "API (100 req/jour)"] },
            { name: "black_card", price_fcfa: 25000, features: ["Tout Premier inclus", "Support prioritaire", "Vault yield boost +1%", "API (10K req/jour)", "Dashboard custom"] },
          ] as Plan[],
        };
      }
      return apiClient.get<Plan[]>(API_ENDPOINTS.SUBSCRIPTION.PLANS);
    },
    staleTime: 1000 * 60 * 5,
  });
}

export function useCurrentSubscription() {
  return useQuery({
    queryKey: ["subscription", "current"],
    queryFn: async () => {
      if (process.env.NODE_ENV === "development") {
        return {
          data: {
            id: "sub_1",
            plan: "free",
            status: "active",
            started_at: "2026-01-01T00:00:00Z",
            expires_at: null,
          } as CurrentSubscription,
        };
      }
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
