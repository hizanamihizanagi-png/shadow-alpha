"use client";

import { useEffect, useState } from "react";
import {
  AreaChart,
  TrendingUp,
  RefreshCcw,
  Plus,
  Wallet,
} from "lucide-react";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { APP_CONFIG } from "@/lib/constants";
import { formatCurrency } from "@/lib/utils";
import {
  useCreatePosition,
  useInstantCashoutExecute,
  useInstantCashoutQuote,
  useOrderbook,
  usePlaceOrder,
  usePositions,
  useRepricePosition,
} from "@/hooks/use-positions";

const toNumber = (value: unknown) => {
  if (typeof value === "number") return value;
  if (typeof value === "string") return Number(value);
  return 0;
};

export default function ExchangePage() {
  const { data: positionsData } = usePositions();
  const createPosition = useCreatePosition();
  const placeOrder = usePlaceOrder();
  const cashoutQuote = useInstantCashoutQuote();
  const cashoutExecute = useInstantCashoutExecute();
  const repricePosition = useRepricePosition();

  const positions = positionsData?.data ?? [];
  const tradablePositions = positions.filter((pos) => pos.status === "active");
  const selectablePositions =
    tradablePositions.length > 0 ? tradablePositions : positions;

  const [selectedPositionId, setSelectedPositionId] = useState("");
  const [orderSide, setOrderSide] = useState<"buy" | "sell">("buy");
  const [orderPrice, setOrderPrice] = useState("2.00");
  const [orderStake, setOrderStake] = useState("10000");
  const [currentProb, setCurrentProb] = useState("0.50");
  const [timeRemaining, setTimeRemaining] = useState("0.75");

  const [newPosition, setNewPosition] = useState({
    sportsbook: "",
    teams: "",
    league: "",
    odds: "",
    stake: "",
  });

  useEffect(() => {
    if (!selectedPositionId && selectablePositions.length > 0) {
      setSelectedPositionId(selectablePositions[0].id);
    }
  }, [selectablePositions, selectedPositionId]);

  useEffect(() => {
    const position = selectablePositions.find(
      (item) => item.id === selectedPositionId,
    );
    if (position) {
      setOrderPrice(position.odds.toFixed(2));
    }
  }, [selectedPositionId, selectablePositions]);

  const selectedPosition = selectablePositions.find(
    (pos) => pos.id === selectedPositionId,
  );

  const { data: orderbookData, isLoading: isOrderbookLoading } = useOrderbook(
    selectedPositionId || null,
  );
  const orderbook = orderbookData?.data ?? { bids: [], asks: [] };
  const asks = Array.isArray(orderbook.asks) ? orderbook.asks : [];
  const bids = Array.isArray(orderbook.bids) ? orderbook.bids : [];
  const bestAsk = asks.length > 0 ? toNumber(asks[0].price) : null;
  const bestBid = bids.length > 0 ? toNumber(bids[0].price) : null;
  const spread =
    bestAsk !== null && bestBid !== null ? bestAsk - bestBid : null;

  const expectedReturn =
    toNumber(orderStake) > 0
      ? toNumber(orderStake) * (toNumber(orderPrice) - 1)
      : 0;

  const pricing = repricePosition.data?.data as Record<string, unknown> | undefined;
  const cashout = cashoutQuote.data?.data as Record<string, unknown> | undefined;

  const handleCreatePosition = () => {
    if (!newPosition.sportsbook || !newPosition.teams) return;
    const odds = Number(newPosition.odds);
    const stake = Number(newPosition.stake);
    if (!odds || !stake) return;
    createPosition.mutate(
      {
        sportsbook: newPosition.sportsbook,
        teams: newPosition.teams,
        league: newPosition.league || undefined,
        odds,
        stake,
      },
      {
        onSuccess: (res) => {
          const resData = res.data as Record<string, unknown> | undefined;
          const createdId = String(resData?.id ?? "");
          setNewPosition({
            sportsbook: "",
            teams: "",
            league: "",
            odds: "",
            stake: "",
          });
          if (createdId) setSelectedPositionId(createdId);
        },
      },
    );
  };

  const handlePlaceOrder = () => {
    if (!selectedPositionId) return;
    const price = Number(orderPrice);
    if (!price || price <= 0) return;
    placeOrder.mutate({
      position_id: selectedPositionId,
      order_type: orderSide,
      price,
    });
  };

  const handleQuoteCashout = () => {
    if (!selectedPositionId) return;
    cashoutQuote.mutate(selectedPositionId);
  };

  const handleExecuteCashout = () => {
    if (!selectedPositionId) return;
    cashoutExecute.mutate(selectedPositionId);
  };

  const handleReprice = () => {
    if (!selectedPositionId) return;
    const probValue = Number(currentProb);
    const timeValue = Number(timeRemaining);
    repricePosition.mutate({
      positionId: selectedPositionId,
      currentProb: Number.isFinite(probValue) ? probValue : undefined,
      timeRemaining: Number.isFinite(timeValue) ? timeValue : undefined,
    });
  };

  return (
    <div className="flex flex-col gap-6 pb-10">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-display font-bold tracking-tight text-white">
            Exchange
          </h1>
          <p className="text-muted-foreground">
            Order book execution, pricing engine, et cashout instantané.
          </p>
        </div>
        <Button>
          <AreaChart className="mr-2 h-4 w-4" /> Open Orders
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Order Book Column */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <Card className="glass-panel">
            <CardHeader className="flex flex-col gap-4 md:flex-row md:items-center md:justify-between pb-4">
              <div>
                <CardTitle className="text-lg">Positions Actives</CardTitle>
                <CardDescription>
                  Sélectionnez une position pour afficher l&apos;order book.
                </CardDescription>
              </div>
              <div className="flex items-center gap-3">
                <select
                  value={selectedPositionId}
                  onChange={(event) => setSelectedPositionId(event.target.value)}
                  className="rounded-md border border-border bg-surface-2 px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
                  disabled={selectablePositions.length === 0}
                >
                  {selectablePositions.length === 0 && (
                    <option value="">Aucune position active</option>
                  )}
                  {selectablePositions.map((pos) => (
                    <option key={pos.id} value={pos.id}>
                      {pos.teams}
                    </option>
                  ))}
                </select>
                {selectedPosition && (
                  <Badge variant="outline" className="bg-surface-2 text-gold">
                    {formatCurrency(
                      selectedPosition.stake,
                      APP_CONFIG.currency as any,
                    )}
                  </Badge>
                )}
              </div>
            </CardHeader>
          </Card>

          <Card className="glass-panel flex-1">
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <CardTitle className="text-lg">
                Live Order Book{" "}
                {selectedPosition ? `: ${selectedPosition.teams}` : ""}
              </CardTitle>
              <div className="flex items-center gap-2 text-xs text-muted-foreground bg-surface-2 px-3 py-1.5 rounded-full border border-border">
                <span className="flex h-2 w-2 rounded-full bg-success animate-pulse"></span>
                {isOrderbookLoading ? "Chargement" : "Market Open"}
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="grid grid-cols-2 text-sm text-muted-foreground border-b border-border bg-surface-2/50 px-6 py-2">
                <div>Bid (Back)</div>
                <div className="text-right">Ask (Lay)</div>
              </div>

              {/* Asks */}
              <div className="flex flex-col border-b border-border/50">
                {(asks.length > 0 ? asks : [null, null, null]).map((ask, i) => {
                  const price = ask ? toNumber(ask.price) : 0;
                  return (
                    <div
                      key={`ask-${ask?.id ?? i}`}
                      className="grid grid-cols-2 px-6 py-2 hover:bg-surface-2/50 cursor-pointer text-sm font-mono relative overflow-hidden group"
                    >
                      <div
                        className="absolute right-1/2 top-0 h-full bg-danger/10 z-0 transition-all group-hover:bg-danger/20"
                        style={{ width: `${(3 - i) * 15}%` }}
                      ></div>
                      <div
                        className="absolute left-1/2 top-0 h-full bg-gold/5 z-0 transition-all group-hover:bg-gold/10"
                        style={{ width: `${(3 - i) * 10}%` }}
                      ></div>

                      <div className="relative z-10 flex justify-between pr-4 items-center">
                        <span className="text-muted-foreground">
                          Vol: {ask ? "--" : "--"}
                        </span>
                        <span className="text-white group-hover:text-gold transition-colors">
                          {ask ? price.toFixed(2) : "--"}
                        </span>
                      </div>
                      <div className="relative z-10 text-right flex justify-between pl-4 items-center">
                        <span className="text-danger font-bold">
                          {ask ? price.toFixed(2) : "--"}
                        </span>
                        <span className="text-muted-foreground">
                          Vol: {ask ? "--" : "--"}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Spread Info */}
              <div className="flex items-center justify-center py-2 bg-surface-2 border-b border-border/50 text-xs font-mono text-muted-foreground">
                <RefreshCcw className="h-3 w-3 mr-2" />
                Spread: {spread !== null ? spread.toFixed(2) : "--"}
              </div>

              {/* Bids */}
              <div className="flex flex-col">
                {(bids.length > 0 ? bids : [null, null, null]).map((bid, i) => {
                  const price = bid ? toNumber(bid.price) : 0;
                  return (
                    <div
                      key={`bid-${bid?.id ?? i}`}
                      className="grid grid-cols-2 px-6 py-2 hover:bg-surface-2/50 cursor-pointer text-sm font-mono relative overflow-hidden group"
                    >
                      <div
                        className="absolute right-1/2 top-0 h-full bg-success/10 z-0 transition-all group-hover:bg-success/20"
                        style={{ width: `${(i + 1) * 20}%` }}
                      ></div>
                      <div
                        className="absolute left-1/2 top-0 h-full bg-gold/5 z-0 transition-all group-hover:bg-gold/10"
                        style={{ width: `${(i + 1) * 8}%` }}
                      ></div>

                      <div className="relative z-10 flex justify-between pr-4 items-center">
                        <span className="text-muted-foreground">
                          Vol: {bid ? "--" : "--"}
                        </span>
                        <span className="text-success font-bold">
                          {bid ? price.toFixed(2) : "--"}
                        </span>
                      </div>
                      <div className="relative z-10 text-right flex justify-between pl-4 items-center">
                        <span className="text-white group-hover:text-gold transition-colors">
                          {bid ? price.toFixed(2) : "--"}
                        </span>
                        <span className="text-muted-foreground">
                          Vol: {bid ? "--" : "--"}
                        </span>
                      </div>
                    </div>
                  );
                })}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Order Entry Column */}
        <div className="flex flex-col gap-6">
          <Card className="glass-panel border-gold/20">
            <CardHeader className="pb-4">
              <CardTitle className="text-lg flex items-center gap-2">
                <Plus className="h-4 w-4 text-gold" />
                Nouvelle Position
              </CardTitle>
              <CardDescription>
                Enregistrez un pari existant pour le trader.
              </CardDescription>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <input
                type="text"
                placeholder="Sportsbook (1xBet, Bet365...)"
                value={newPosition.sportsbook}
                onChange={(event) =>
                  setNewPosition({ ...newPosition, sportsbook: event.target.value })
                }
                className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
              />
              <input
                type="text"
                placeholder="Match / Teams"
                value={newPosition.teams}
                onChange={(event) =>
                  setNewPosition({ ...newPosition, teams: event.target.value })
                }
                className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
              />
              <input
                type="text"
                placeholder="League (optionnel)"
                value={newPosition.league}
                onChange={(event) =>
                  setNewPosition({ ...newPosition, league: event.target.value })
                }
                className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
              />
              <div className="grid grid-cols-2 gap-3">
                <input
                  type="number"
                  placeholder="Odds"
                  value={newPosition.odds}
                  onChange={(event) =>
                    setNewPosition({ ...newPosition, odds: event.target.value })
                  }
                  className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
                />
                <input
                  type="number"
                  placeholder="Stake"
                  value={newPosition.stake}
                  onChange={(event) =>
                    setNewPosition({ ...newPosition, stake: event.target.value })
                  }
                  className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none"
                />
              </div>
              <Button
                className="w-full"
                onClick={handleCreatePosition}
                disabled={createPosition.isPending}
              >
                {createPosition.isPending ? "Création..." : "Créer la position"}
              </Button>
            </CardContent>
          </Card>

          <Card className="glass-panel">
            <CardHeader className="pb-4">
              <div className="flex space-x-2 border-b border-border pb-4">
                <button
                  className={`flex-1 py-1.5 text-center text-sm font-medium rounded-md ${
                    orderSide === "buy"
                      ? "bg-gold text-black"
                      : "bg-surface-2 text-muted-foreground hover:bg-surface-3 hover:text-white"
                  }`}
                  onClick={() => setOrderSide("buy")}
                >
                  Buy
                </button>
                <button
                  className={`flex-1 py-1.5 text-center text-sm font-medium rounded-md ${
                    orderSide === "sell"
                      ? "bg-gold text-black"
                      : "bg-surface-2 text-muted-foreground hover:bg-surface-3 hover:text-white"
                  }`}
                  onClick={() => setOrderSide("sell")}
                >
                  Sell
                </button>
              </div>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-medium text-muted-foreground">
                  Price (Odds)
                </label>
                <div className="relative flex items-center">
                  <input
                    type="number"
                    value={orderPrice}
                    onChange={(event) => setOrderPrice(event.target.value)}
                    step="0.05"
                    className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none focus:ring-1 focus:ring-gold font-mono"
                  />
                  <div className="absolute right-3 text-xs text-muted-foreground">
                    EU
                  </div>
                </div>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-medium text-muted-foreground">
                  Size (Stake)
                </label>
                <div className="relative flex items-center">
                  <input
                    type="number"
                    value={orderStake}
                    onChange={(event) => setOrderStake(event.target.value)}
                    step="1000"
                    className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 pl-9 text-sm text-white focus:border-gold focus:outline-none focus:ring-1 focus:ring-gold font-mono"
                  />
                  <div className="absolute left-3 text-muted-foreground font-mono">
                    {APP_CONFIG.currency}
                  </div>
                </div>
              </div>

              <div className="flex justify-between items-center text-sm border-t border-border pt-4">
                <span className="text-muted-foreground">Expected Return</span>
                <span className="font-mono font-bold text-white">
                  {formatCurrency(expectedReturn, APP_CONFIG.currency as any)}
                </span>
              </div>

              <Button
                className="w-full mt-2"
                size="lg"
                onClick={handlePlaceOrder}
                disabled={!selectedPositionId || placeOrder.isPending}
              >
                {placeOrder.isPending ? "Envoi..." : "Place Order"}
              </Button>
            </CardContent>
          </Card>

          <Card className="glass-panel border-gold/20">
            <CardHeader className="py-4">
              <CardTitle className="text-sm flex items-center gap-2">
                <Wallet className="h-4 w-4 text-gold" />
                Instant Cashout
              </CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>Offre</span>
                <span className="font-mono text-white">
                  {cashout
                    ? formatCurrency(
                        toNumber(cashout.offered_price),
                        APP_CONFIG.currency as any,
                      )
                    : "--"}
                </span>
              </div>
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>Spread</span>
                <span className="font-mono text-white">
                  {cashout ? `${toNumber(cashout.spread_pct).toFixed(2)}%` : "--"}
                </span>
              </div>
              <div className="flex items-center justify-between text-sm text-muted-foreground">
                <span>PnL</span>
                <span
                  className={`font-mono ${toNumber(cashout?.pnl) >= 0 ? "text-success" : "text-danger"}`}
                >
                  {cashout
                    ? formatCurrency(
                        toNumber(cashout.pnl),
                        APP_CONFIG.currency as any,
                      )
                    : "--"}
                </span>
              </div>
              <div className="flex gap-2 pt-2">
                <Button
                  variant="secondary"
                  className="flex-1"
                  onClick={handleQuoteCashout}
                  disabled={!selectedPositionId || cashoutQuote.isPending}
                >
                  {cashoutQuote.isPending ? "Calcul..." : "Obtenir un prix"}
                </Button>
                <Button
                  className="flex-1"
                  onClick={handleExecuteCashout}
                  disabled={!selectedPositionId || cashoutExecute.isPending}
                >
                  {cashoutExecute.isPending ? "Vente..." : "Exécuter"}
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-panel border-info/20">
            <CardHeader className="py-4">
              <CardTitle className="text-sm">Pricing Engine</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <div className="grid grid-cols-2 gap-3">
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-muted-foreground">
                    Current Prob
                  </label>
                  <input
                    type="number"
                    value={currentProb}
                    onChange={(event) => setCurrentProb(event.target.value)}
                    step="0.01"
                    min="0"
                    max="1"
                    className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none font-mono"
                  />
                </div>
                <div className="flex flex-col gap-1.5">
                  <label className="text-xs text-muted-foreground">
                    Time Remaining
                  </label>
                  <input
                    type="number"
                    value={timeRemaining}
                    onChange={(event) => setTimeRemaining(event.target.value)}
                    step="0.01"
                    min="0"
                    max="1"
                    className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 text-sm text-white focus:border-gold focus:outline-none font-mono"
                  />
                </div>
              </div>
              <Button
                variant="secondary"
                onClick={handleReprice}
                disabled={!selectedPositionId || repricePosition.isPending}
              >
                {repricePosition.isPending ? "Calcul..." : "Reprice"}
              </Button>
              <div className="rounded-lg border border-border bg-surface-2 p-3 text-xs text-muted-foreground">
                <div className="flex items-center justify-between">
                  <span>Fair Value</span>
                  <span className="font-mono text-white">
                    {pricing
                      ? formatCurrency(
                          toNumber(pricing.fair_value),
                          APP_CONFIG.currency as any,
                        )
                      : "--"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Implied Prob</span>
                  <span className="font-mono text-white">
                    {pricing
                      ? `${toNumber(pricing.implied_prob).toFixed(3)}`
                      : "--"}
                  </span>
                </div>
                <div className="flex items-center justify-between">
                  <span>Sigma</span>
                  <span className="font-mono text-white">
                    {pricing ? `${toNumber(pricing.sigma).toFixed(3)}` : "--"}
                  </span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card className="glass-panel border-gold/20">
            <CardHeader className="py-4">
              <CardTitle className="text-sm">
                Kelly Criterion Recommendation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <div className="flex items-center gap-4 bg-gold/5 p-3 rounded-lg border border-gold/10">
                <div className="h-10 w-10 flex flex-shrink-0 items-center justify-center rounded-full bg-gold/20 text-gold">
                  <TrendingUp className="h-5 w-5" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground mb-1">
                    Optimal Stake Size
                  </p>
                  <p className="text-sm font-bold text-white font-mono">
                    4.5% of Bankroll
                  </p>
                </div>
              </div>
              <p className="text-xs text-muted-foreground mt-3 leading-relaxed">
                Model indicates edge of 5.2% against current market odds.
                Recommended continuous sizing applied.
              </p>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
