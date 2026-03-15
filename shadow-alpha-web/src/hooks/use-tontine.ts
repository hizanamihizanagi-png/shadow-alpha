import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/constants";

interface TontineGroup {
  id: string;
  name: string;
  creator_id: string;
  cycle_type: string;
  target_amount: string;
  description: string | null;
  status: string;
  current_cycle: number;
  total_contributed: string;
  member_count: number;
  created_at: string;
}

interface Contribution {
  id: string;
  group_id: string;
  user_id: string;
  amount: string;
  cycle_number: number;
  created_at: string;
}

export function useTontineGroups() {
  return useQuery({
    queryKey: ["tontine", "groups"],
    queryFn: async () => {
      const res = await apiClient.get<TontineGroup[]>(
        API_ENDPOINTS.TONTINE.MY_GROUPS,
      );
      const list = Array.isArray(res.data) ? res.data : [];
      return { data: list };
    },
    staleTime: 1000 * 30,
  });
}

export function useCreateTontineGroup() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: {
      name: string;
      cycle_type: string;
      target_amount: string;
      description?: string;
    }) => {
      return apiClient.post("/tontine/create-group", payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tontine"] });
    },
  });
}

export function useJoinTontine() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (groupId: string) => {
      return apiClient.post("/tontine/join", { group_id: groupId });
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tontine"] });
    },
  });
}

export function useTontineContribute() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: { group_id: string; amount: string }) => {
      return apiClient.post("/tontine/contribute", payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["tontine"] });
    },
  });
}

export function useTontineLedger(groupId: string | null) {
  return useQuery({
    queryKey: ["tontine", "ledger", groupId],
    queryFn: async () => {
      if (!groupId) return { data: [] };
      const res = await apiClient.get<Contribution[]>(
        `/tontine/${groupId}/ledger`,
      );
      return { data: Array.isArray(res.data) ? res.data : [] };
    },
    enabled: !!groupId,
    staleTime: 1000 * 30,
  });
}
