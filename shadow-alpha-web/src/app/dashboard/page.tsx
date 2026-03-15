"use client";

import { motion } from "framer-motion";
import {
  AreaChart,
  Wallet,
  ArrowUpRight,
  ArrowDownRight,
  Activity,
  Users,
  Clock,
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
import { PortfolioChart } from "@/components/charts/portfolio-chart";
import { TontineProgress } from "@/components/charts/tontine-progress";
import { usePortfolio } from "@/hooks/use-portfolio";
import { usePositions } from "@/hooks/use-positions";
import { formatCurrency, formatPnl } from "@/lib/utils";
import { APP_CONFIG } from "@/lib/constants";

export default function DashboardPage() {
  const { data: portfolio, isLoading, isError } = usePortfolio();
  const { data: positionsData, isLoading: isPositionsLoading } = usePositions();
  const recentPositions = positionsData?.data?.slice(0, 3) ?? [];

  if (isError) {
    return (
      <div className="p-8 flex flex-col items-center justify-center gap-4">
        <Wallet className="h-12 w-12 text-gold" />
        <h2 className="text-xl font-display font-bold text-white">Welcome to Shadow Alpha</h2>
        <p className="text-sm text-muted-foreground text-center max-w-md">
          Your portfolio is empty. Head to the Exchange to create your first position,
          or deposit funds into the Shadow Vault to start growing your capital.
        </p>
        <div className="flex gap-3">
          <Button onClick={() => window.location.href = "/exchange"}>
            <AreaChart className="mr-2 h-4 w-4" /> Go to Exchange
          </Button>
          <Button variant="secondary" onClick={() => window.location.href = "/vault"}>
            <Wallet className="mr-2 h-4 w-4" /> Open Vault
          </Button>
        </div>
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-8 pb-10">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-display font-bold tracking-tight text-white">
          Dashboard
        </h1>
        <p className="text-muted-foreground">
          Overview of your capital and active positions.
        </p>
      </div>

      {/* Top Metrics Row */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        {/* Total Value */}
        <Card className="glass-panel group relative overflow-hidden transition-all hover:bg-surface-2/80">
          <div className="absolute right-0 top-0 h-24 w-24 -translate-y-8 translate-x-8 rounded-full bg-gold/10 blur-2xl transition-all group-hover:bg-gold/20" />
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Equity
            </CardTitle>
            <Wallet className="h-4 w-4 text-gold" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl lg:text-3xl font-bold font-mono text-white">
              {isLoading ? (
                <div className="h-8 w-32 animate-pulse bg-surface-3 rounded" />
              ) : (
                formatCurrency(
                  portfolio?.data?.totalValue || 0,
                  APP_CONFIG.currency as any,
                )
              )}
            </div>
            {!isLoading && (
              <p className="mt-1 flex items-center text-xs text-success">
                <ArrowUpRight className="mr-1 h-3 w-3" />
                +2.5% from last week
              </p>
            )}
          </CardContent>
        </Card>

        {/* Available Margin */}
        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Available Margin
            </CardTitle>
            <Activity className="h-4 w-4 text-accent" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-white">
              {isLoading ? (
                <div className="h-8 w-24 animate-pulse bg-surface-3 rounded" />
              ) : (
                formatCurrency(
                  portfolio?.data?.availableMargin || 0,
                  APP_CONFIG.currency as any,
                )
              )}
            </div>
          </CardContent>
        </Card>

        {/* Active P2P Positions */}
        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              P2P Exposure
            </CardTitle>
            <AreaChart className="h-4 w-4 text-gold" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-white">
              {isLoading ? (
                <div className="h-8 w-24 animate-pulse bg-surface-3 rounded" />
              ) : (
                portfolio?.data?.positionCount || 0
              )}{" "}
              Active
            </div>
            <p className="mt-1 flex items-center text-xs text-muted-foreground">
              <span className="text-success-foreground mr-1">
                {((portfolio?.data?.winRate ?? 0) * 100).toFixed(1)}%
              </span>{" "}
              Win Rate
            </p>
          </CardContent>
        </Card>

        {/* Active Tontines */}
        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Tontine Capital
            </CardTitle>
            <Users className="h-4 w-4 text-gold" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-white">
              3 Active
            </div>
            <p className="mt-1 flex items-center text-xs text-muted-foreground">
              Next payout in{" "}
              <span className="text-gold ml-1 font-medium">4 days</span>
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-6 md:grid-cols-7 lg:grid-cols-8">
        {/* Main Chart Section */}
        <Card className="md:col-span-4 lg:col-span-5 flex flex-col glass-panel">
          <CardHeader className="flex flex-row items-center justify-between pb-6">
            <div>
              <CardTitle className="text-xl font-display">
                Performance Overview
              </CardTitle>
              <CardDescription>
                Your portfolio growth over the last 30 days
              </CardDescription>
            </div>
            <div className="flex items-center gap-2">
              <Badge
                variant="outline"
                className="cursor-pointer bg-surface-2 text-gold"
              >
                1M
              </Badge>
              <Badge
                variant="outline"
                className="cursor-pointer hover:text-white"
              >
                3M
              </Badge>
              <Badge
                variant="outline"
                className="cursor-pointer hidden sm:inline-flex hover:text-white"
              >
                YTD
              </Badge>
            </div>
          </CardHeader>
          <CardContent className="flex-1 pb-2">
            <PortfolioChart isLoading={isLoading} />
          </CardContent>
        </Card>

        {/* Right Sidebar Split */}
        <div className="md:col-span-3 lg:col-span-3 flex flex-col gap-6">
          {/* Active Tontine Summary */}
          <Card className="glass-panel overflow-hidden border-gold/20 flex-1">
            <div className="h-1 w-full bg-gradient-to-r from-gold/50 to-accent/50 absolute top-0 left-0"></div>
            <CardHeader className="pb-2">
              <div className="flex justify-between items-start">
                <div>
                  <CardTitle className="text-lg font-display text-white">
                    Alpha Syndicate A
                  </CardTitle>
                  <CardDescription>Premium Payout Pool</CardDescription>
                </div>
                <Badge className="bg-gold/20 text-gold border-gold/30">
                  Active
                </Badge>
              </div>
            </CardHeader>
            <CardContent className="flex flex-col items-center py-6">
              <TontineProgress currentCycle={4} totalCycles={10} size={140} />
              <div className="mt-6 grid grid-cols-2 gap-4 w-full text-center">
                <div className="bg-surface-2 p-3 rounded-lg border border-border">
                  <p className="text-xs text-muted-foreground mb-1">
                    Your Contribution
                  </p>
                  <p className="font-mono text-sm font-bold text-white">
                    50k {APP_CONFIG.currency}
                  </p>
                </div>
                <div className="bg-surface-2 p-3 rounded-lg border border-border">
                  <p className="text-xs text-muted-foreground mb-1">
                    Expected Payout
                  </p>
                  <p className="font-mono text-sm font-bold text-gold">
                    500k {APP_CONFIG.currency}
                  </p>
                </div>
              </div>
              <Button className="w-full mt-4" variant="secondary">
                View Leaderboard
              </Button>
            </CardContent>
          </Card>
        </div>
      </div>

      {/* Recent Activity / Positions */}
      <h2 className="text-xl font-display font-bold text-white mt-4 border-b border-border pb-2">
        Recent Positions
      </h2>
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
        {isPositionsLoading ? (
          <Card className="glass-panel md:col-span-2 lg:col-span-3">
            <CardContent className="p-6 text-sm text-muted-foreground">
              Chargement des positions...
            </CardContent>
          </Card>
        ) : recentPositions.length === 0 ? (
          <Card className="glass-panel md:col-span-2 lg:col-span-3">
            <CardContent className="p-6 text-sm text-muted-foreground">
              Aucune position récente pour le moment.
            </CardContent>
          </Card>
        ) : (
          recentPositions.map((pos) => {
            const pnlValue =
              pos.status === "won"
                ? pos.maxPayout - pos.stake
                : pos.status === "lost"
                  ? -pos.stake
                  : pos.currentValue - pos.stake;
            const pnlPct = pos.stake > 0 ? (pnlValue / pos.stake) * 100 : 0;
            const pnl = formatPnl(pnlValue, pnlPct);
            const isPositive = pnlValue >= 0;
            return (
              <Card
                key={pos.id}
                className="glass-panel hover:border-gold/30 transition-colors cursor-pointer group"
              >
                <CardContent className="p-5">
                  <div className="flex justify-between items-start mb-4">
                    <div className="flex items-center gap-3">
                      <div
                        className={`h-10 w-10 rounded-full flex items-center justify-center ${isPositive ? "bg-success/10 text-success" : "bg-danger/10 text-danger"}`}
                      >
                        {isPositive ? (
                          <ArrowUpRight className="h-5 w-5" />
                        ) : (
                          <ArrowDownRight className="h-5 w-5" />
                        )}
                      </div>
                      <div>
                        <p className="font-semibold text-sm text-white group-hover:text-gold transition-colors">
                          {pos.teams}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          Sports Market • {pos.status}
                        </p>
                      </div>
                    </div>
                    <Badge
                      variant={pos.status === "active" ? "default" : "secondary"}
                      className="text-[10px] px-2"
                    >
                      {pos.status}
                    </Badge>
                  </div>
                  <div className="flex justify-between items-end">
                    <div>
                      <p className="text-xs text-muted-foreground">Stake</p>
                      <p className="font-mono text-sm">
                        {formatCurrency(
                          pos.stake,
                          APP_CONFIG.currency as any,
                        )}
                      </p>
                    </div>
                    <div className="text-right">
                      <p className="text-xs text-muted-foreground">PnL</p>
                      <p className={`font-mono font-bold ${pnl.colorClass}`}>
                        {pnl.formatted}
                      </p>
                    </div>
                  </div>
                </CardContent>
              </Card>
            );
          })
        )}
      </div>
    </div>
  );
}
