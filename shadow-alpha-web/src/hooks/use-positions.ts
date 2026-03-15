import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { apiClient } from "@/lib/api-client";
import { API_ENDPOINTS } from "@/lib/constants";
import { Position } from "@/types/portfolio";

interface OrderbookEntry {
  id: string;
  price: string;
}

interface OrderbookResponse {
  bids: OrderbookEntry[];
  asks: OrderbookEntry[];
}

const toNumber = (value: unknown) => {
  if (typeof value === "number") return value;
  if (typeof value === "string") return Number(value);
  return 0;
};

const mapPosition = (raw: Record<string, unknown>): Position => {
  return {
    id: String(raw.id ?? ""),
    userId: String(raw.user_id ?? raw.userId ?? ""),
    sportsbook: String(raw.sportsbook ?? ""),
    teams: String(raw.teams ?? ""),
    league: raw.league ? String(raw.league) : null,
    odds: toNumber(raw.odds),
    stake: toNumber(raw.stake),
    maxPayout: toNumber(raw.max_payout ?? raw.maxPayout),
    currentValue: toNumber(raw.current_value ?? raw.currentValue ?? raw.stake),
    currentProb:
      raw.current_prob !== undefined ? Number(raw.current_prob) : null,
    timeRemaining:
      raw.time_remaining !== undefined ? Number(raw.time_remaining) : null,
    status: String(raw.status ?? "active") as Position["status"],
    description: raw.description ? String(raw.description) : null,
    createdAt: String(raw.created_at ?? raw.createdAt ?? new Date().toISOString()),
  };
};

export function usePositions() {
  return useQuery({
    queryKey: ["positions", "my"],
    queryFn: async () => {
      const res = await apiClient.get<Record<string, unknown>[]>(
        "/positions/my",
      );
      const list = Array.isArray(res.data) ? res.data : [];
      return { data: list.map((item) => mapPosition(item)) };
    },
    staleTime: 1000 * 30,
  });
}

export function useCreatePosition() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: {
      sportsbook: string;
      teams: string;
      league?: string | null;
      odds: number;
      stake: number;
      description?: string | null;
    }) => {
      return apiClient.post("/positions/create", payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
    },
  });
}

export function useRepricePosition() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: {
      positionId: string;
      currentProb?: number;
      timeRemaining?: number;
    }) => {
      const params = new URLSearchParams();
      if (payload.currentProb !== undefined) {
        params.set("current_prob", String(payload.currentProb));
      }
      if (payload.timeRemaining !== undefined) {
        params.set("time_remaining", String(payload.timeRemaining));
      }
      const query = params.toString();
      const endpoint = `/positions/${payload.positionId}/value${query ? `?${query}` : ""}`;
      return apiClient.get(endpoint);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
    },
  });
}

export function useInstantCashoutQuote() {
  return useMutation({
    mutationFn: async (positionId: string) => {
      const endpoint = `${API_ENDPOINTS.EXCHANGE.INSTANT_CASHOUT_QUOTE}?position_id=${positionId}`;
      return apiClient.get(endpoint);
    },
  });
}

export function useInstantCashoutExecute() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (positionId: string) => {
      const endpoint = `${API_ENDPOINTS.EXCHANGE.INSTANT_CASHOUT_EXECUTE}?position_id=${positionId}`;
      return apiClient.post(endpoint, {});
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["positions"] });
      queryClient.invalidateQueries({ queryKey: ["portfolio"] });
    },
  });
}

export function useOrderbook(positionId?: string | null) {
  return useQuery({
    queryKey: ["orderbook", positionId],
    queryFn: async () => {
      if (!positionId) return { data: { bids: [], asks: [] } };
      const endpoint = `${API_ENDPOINTS.EXCHANGE.ORDERBOOK}?position_id=${positionId}`;
      return apiClient.get<OrderbookResponse>(endpoint);
    },
    enabled: !!positionId,
    staleTime: 1000 * 10,
  });
}

export function usePlaceOrder() {
  const queryClient = useQueryClient();
  return useMutation({
    mutationFn: async (payload: {
      position_id: string;
      order_type: "buy" | "sell";
      price: number;
    }) => {
      return apiClient.post("/exchange/place-order", payload);
    },
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ["orderbook"] });
      queryClient.invalidateQueries({ queryKey: ["positions"] });
    },
  });
}
