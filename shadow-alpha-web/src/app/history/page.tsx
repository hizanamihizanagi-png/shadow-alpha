"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import {
  Download,
  Filter,
  ArrowUpRight,
  ArrowDownRight,
  ArrowRightLeft,
} from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { formatCurrency, formatDate } from "@/lib/utils";
import { APP_CONFIG } from "@/lib/constants";
import { usePortfolioHistory } from "@/hooks/use-portfolio-history";

export default function HistoryPage() {
  const { data: historyData, isLoading, isError } = usePortfolioHistory();
  const positions = historyData?.data?.positions ?? [];

  if (isError) {
    return <div className="p-8 text-danger">Error loading history</div>;
  }

  const getIcon = (type: string) => {
    switch (type) {
      case "payout":
      case "trade_win":
      case "deposit":
        return <ArrowUpRight className="h-5 w-5 text-success" />;
      case "contribution":
      case "trade_loss":
      case "withdrawal":
        return <ArrowDownRight className="h-5 w-5 text-danger" />;
      default:
        return <ArrowRightLeft className="h-5 w-5 text-gold" />;
    }
  };

  const getBg = (type: string) => {
    switch (type) {
      case "payout":
      case "trade_win":
      case "deposit":
        return "bg-success/10";
      case "contribution":
      case "trade_loss":
      case "withdrawal":
        return "bg-danger/10";
      default:
        return "bg-surface-3";
    }
  };

  const items = positions.map((pos) => {
    const status = pos.status;
    const type =
      status === "won"
        ? "trade_win"
        : status === "lost"
          ? "trade_loss"
          : "cashout";
    const title =
      status === "won"
        ? `P2P Win: ${pos.teams}`
        : status === "lost"
          ? `P2P Loss: ${pos.teams}`
          : `Cashout: ${pos.teams}`;
    const date = pos.updatedAt ?? pos.createdAt ?? new Date().toISOString();
    return {
      id: pos.id,
      type,
      title,
      amount: pos.pnl,
      date,
      status: status ?? "completed",
    };
  });

  return (
    <div className="flex flex-col gap-6 pb-10">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-display font-bold tracking-tight text-white">
            History
          </h1>
          <p className="text-muted-foreground">
            Comprehensive ledger of all trades and transactions.
          </p>
        </div>
        <div className="flex gap-2">
          <Button variant="outline" size="sm" className="hidden sm:flex">
            <Filter className="mr-2 h-4 w-4" /> Filter
          </Button>
          <Button variant="secondary" size="sm">
            <Download className="mr-2 h-4 w-4" /> Export CSV
          </Button>
        </div>
      </div>

      <Card className="glass-panel border-transparent">
        <CardHeader className="flex flex-row items-center justify-between pb-4 border-b border-border bg-surface-2/30">
          <div className="flex space-x-6">
            <button className="text-sm font-medium text-gold border-b-2 border-gold pb-4 -mb-4">
              All Activity
            </button>
            <button className="text-sm font-medium text-muted-foreground hover:text-white pb-4 -mb-4 transition-colors">
              Trades
            </button>
            <button className="text-sm font-medium text-muted-foreground hover:text-white pb-4 -mb-4 transition-colors">
              Tontine
            </button>
            <button className="text-sm font-medium text-muted-foreground hover:text-white pb-4 -mb-4 transition-colors hidden sm:block">
              Transfers
            </button>
          </div>
        </CardHeader>
        <CardContent className="p-0">
          {isLoading ? (
            <div className="p-6 text-sm text-muted-foreground">
              Chargement de l&apos;historique...
            </div>
          ) : items.length === 0 ? (
            <div className="p-6 text-sm text-muted-foreground">
              Aucun historique disponible pour le moment.
            </div>
          ) : (
            <div className="divide-y divide-border/50">
              {items.map((tx) => (
                <div
                  key={tx.id}
                  className="flex items-center justify-between p-4 sm:p-6 hover:bg-surface-2/30 transition-colors"
                >
                  <div className="flex items-center gap-4">
                    <div
                      className={`h-10 w-10 sm:h-12 sm:w-12 rounded-full flex items-center justify-center shrink-0 ${getBg(tx.type)}`}
                    >
                      {getIcon(tx.type)}
                    </div>
                    <div>
                      <p className="font-semibold text-white text-sm sm:text-base">
                        {tx.title}
                      </p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {formatDate(tx.date, "MMM dd, yyyy • HH:mm", "en")}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p
                      className={`font-mono font-bold text-sm sm:text-base ${tx.amount > 0 ? "text-success" : "text-foreground"}`}
                    >
                      {tx.amount > 0 ? "+" : ""}
                      {formatCurrency(
                        tx.amount,
                        APP_CONFIG.currency as "USD" | "EUR" | "XAF",
                      )}
                    </p>
                    <Badge
                      variant="outline"
                      className={`mt-1 text-[10px] sm:text-xs px-2 ${
                        tx.amount >= 0
                          ? "border-success/30 text-success"
                          : "border-danger/30 text-danger"
                      }`}
                    >
                      {tx.status}
                    </Badge>
                  </div>
                </div>
              ))}
            </div>
          )}

          <div className="p-4 border-t border-border flex justify-center">
            <Button
              variant="ghost"
              className="text-muted-foreground hover:text-white"
            >
              Load More Transactions
            </Button>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
