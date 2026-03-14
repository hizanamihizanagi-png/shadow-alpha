"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { AreaChart, TrendingUp, TrendingDown, RefreshCcw } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export default function ExchangePage() {
  return (
    <div className="flex flex-col gap-6 pb-10">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-display font-bold tracking-tight text-white">
            Exchange
          </h1>
          <p className="text-muted-foreground">
            Order book execution and liquidity provisioning.
          </p>
        </div>
        <Button>
          <AreaChart className="mr-2 h-4 w-4" /> Open Orders
        </Button>
      </div>

      <div className="grid gap-6 lg:grid-cols-3">
        {/* Order Book Column */}
        <div className="lg:col-span-2 flex flex-col gap-6">
          <Card className="glass-panel flex-1">
            <CardHeader className="flex flex-row items-center justify-between pb-4">
              <CardTitle className="text-lg">
                Live Order Book: PL/Champions League
              </CardTitle>
              <div className="flex items-center gap-2 text-xs text-muted-foreground bg-surface-2 px-3 py-1.5 rounded-full border border-border">
                <span className="flex h-2 w-2 rounded-full bg-success animate-pulse"></span>
                Market Open
              </div>
            </CardHeader>
            <CardContent className="p-0">
              <div className="grid grid-cols-2 text-sm text-muted-foreground border-b border-border bg-surface-2/50 px-6 py-2">
                <div>Bid (Back)</div>
                <div className="text-right">Ask (Lay)</div>
              </div>

              {/* Mock Asks */}
              <div className="flex flex-col border-b border-border/50">
                {[2.1, 2.05, 2.0].map((price, i) => (
                  <div
                    key={`ask-${i}`}
                    className="grid grid-cols-2 px-6 py-2 hover:bg-surface-2/50 cursor-pointer text-sm font-mono relative overflow-hidden group"
                  >
                    {/* Depth visualization */}
                    <div
                      className="absolute right-1/2 top-0 h-full bg-danger/10 z-0 transition-all group-hover:bg-danger/20"
                      style={{ width: `${(3 - i) * 15}%` }}
                    ></div>
                    <div
                      className="absolute left-1/2 top-0 h-full bg-gold/5 z-0 transition-all group-hover:bg-gold/10"
                      style={{ width: `${(3 - i) * 10}%` }}
                    ></div>

                    <div className="relative z-10 flex justify-between pr-4 items-center">
                      <span className="text-muted-foreground">Vol: 15k</span>
                      <span className="text-white group-hover:text-gold transition-colors">
                        {price.toFixed(2)}
                      </span>
                    </div>
                    <div className="relative z-10 text-right flex justify-between pl-4 items-center">
                      <span className="text-danger font-bold">
                        {price.toFixed(2)}
                      </span>
                      <span className="text-muted-foreground">Vol: 12k</span>
                    </div>
                  </div>
                ))}
              </div>

              {/* Spread Info */}
              <div className="flex items-center justify-center py-2 bg-surface-2 border-b border-border/50 text-xs font-mono text-muted-foreground">
                <RefreshCcw className="h-3 w-3 mr-2" />
                Spread: 0.05
              </div>

              {/* Mock Bids */}
              <div className="flex flex-col">
                {[1.95, 1.9, 1.85].map((price, i) => (
                  <div
                    key={`bid-${i}`}
                    className="grid grid-cols-2 px-6 py-2 hover:bg-surface-2/50 cursor-pointer text-sm font-mono relative overflow-hidden group"
                  >
                    {/* Depth visualization */}
                    <div
                      className="absolute right-1/2 top-0 h-full bg-success/10 z-0 transition-all group-hover:bg-success/20"
                      style={{ width: `${(i + 1) * 20}%` }}
                    ></div>
                    <div
                      className="absolute left-1/2 top-0 h-full bg-gold/5 z-0 transition-all group-hover:bg-gold/10"
                      style={{ width: `${(i + 1) * 8}%` }}
                    ></div>

                    <div className="relative z-10 flex justify-between pr-4 items-center">
                      <span className="text-muted-foreground">Vol: 45k</span>
                      <span className="text-success font-bold">
                        {price.toFixed(2)}
                      </span>
                    </div>
                    <div className="relative z-10 text-right flex justify-between pl-4 items-center">
                      <span className="text-white group-hover:text-gold transition-colors">
                        {price.toFixed(2)}
                      </span>
                      <span className="text-muted-foreground">Vol: 8k</span>
                    </div>
                  </div>
                ))}
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Order Entry Column */}
        <div className="flex flex-col gap-6">
          <Card className="glass-panel">
            <CardHeader className="pb-4">
              <div className="flex space-x-2 border-b border-border pb-4">
                <button className="flex-1 py-1.5 text-center text-sm font-medium bg-gold text-black rounded-md">
                  Buy
                </button>
                <button className="flex-1 py-1.5 text-center text-sm font-medium bg-surface-2 text-muted-foreground hover:bg-surface-3 hover:text-white rounded-md transition-colors">
                  Sell
                </button>
              </div>
            </CardHeader>
            <CardContent className="flex flex-col gap-4">
              <div className="flex justify-between items-center bg-surface-2 p-1 rounded-md mb-2">
                <button className="flex-1 py-1 px-3 text-xs font-medium bg-background text-white rounded shadow-sm border border-border">
                  Limit
                </button>
                <button className="flex-1 py-1 px-3 text-xs font-medium text-muted-foreground hover:text-white transition-colors">
                  Market
                </button>
                <button className="flex-1 py-1 px-3 text-xs font-medium text-muted-foreground hover:text-white transition-colors">
                  Stop
                </button>
              </div>

              <div className="flex flex-col gap-1.5">
                <label className="text-xs font-medium text-muted-foreground">
                  Price (Odds)
                </label>
                <div className="relative flex items-center">
                  <input
                    type="number"
                    defaultValue="2.00"
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
                    defaultValue="10000"
                    step="1000"
                    className="h-10 w-full rounded-md border border-border bg-background px-3 py-2 pl-9 text-sm text-white focus:border-gold focus:outline-none focus:ring-1 focus:ring-gold font-mono"
                  />
                  <div className="absolute left-3 text-muted-foreground font-mono">
                    XAF
                  </div>
                </div>
              </div>

              {/* Slider mock */}
              <div className="pt-2 pb-4">
                <div className="h-1.5 w-full bg-surface-3 rounded-full relative">
                  <div className="absolute top-0 left-0 h-full w-[25%] bg-gold rounded-full"></div>
                  <div className="absolute top-1/2 left-[25%] h-4 w-4 -mt-2 -ml-2 rounded-full bg-white border-2 border-gold shadow-md"></div>
                </div>
                <div className="flex justify-between text-[10px] text-muted-foreground mt-2 px-1">
                  <span>0%</span>
                  <span>25%</span>
                  <span>50%</span>
                  <span>75%</span>
                  <span>100%</span>
                </div>
              </div>

              <div className="flex justify-between items-center text-sm border-t border-border pt-4">
                <span className="text-muted-foreground">Expected Return</span>
                <span className="font-mono font-bold text-white">
                  20,000 XAF
                </span>
              </div>

              <Button className="w-full mt-2" size="lg">
                Place Buy Order
              </Button>
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
