"use client";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Users, Plus, Trophy, Calendar, Lock } from "lucide-react";
import { Badge } from "@/components/ui/badge";

export default function TontinePage() {
  return (
    <div className="flex flex-col gap-6 pb-10">
      <div className="flex items-center justify-between">
        <div className="flex flex-col gap-2">
          <h1 className="text-3xl font-display font-bold tracking-tight text-white">
            Digital Tontines
          </h1>
          <p className="text-muted-foreground">
            Transparent capital syndication and rotational savings.
          </p>
        </div>
        <Button>
          <Plus className="mr-2 h-4 w-4" /> New Group
        </Button>
      </div>

      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
        {/* Active Tontine Detailed Card */}
        <Card className="glass-panel border-gold/20 lg:col-span-2 overflow-hidden flex flex-col">
          <div className="h-1 w-full bg-gradient-to-r from-gold/50 to-accent/50"></div>
          <CardHeader className="flex flex-row items-start justify-between pb-2 bg-surface-2/30">
            <div>
              <div className="flex items-center gap-2 mb-1">
                <CardTitle className="text-xl">Alpha Syndicate A</CardTitle>
                <Badge className="bg-success/20 text-success border-success/30 px-2 rounded-sm text-[10px]">
                  Active
                </Badge>
              </div>
              <CardDescription>
                Premium Payout Pool • Created Jan 15, 2026
              </CardDescription>
            </div>
            <div className="text-right">
              <p className="text-xs text-muted-foreground mb-1">
                Total Pool Capital
              </p>
              <p className="font-mono text-xl font-bold text-gold">
                500,000 XAF
              </p>
            </div>
          </CardHeader>
          <CardContent className="flex-1 p-0 flex flex-col transition-all">
            <div className="grid grid-cols-2 sm:grid-cols-4 divide-x divide-y sm:divide-y-0 divide-border border-y border-border bg-surface-2/20">
              <div className="p-4 flex flex-col items-center text-center">
                <Users className="h-4 w-4 text-muted-foreground mb-2" />
                <p className="text-xs text-muted-foreground">Members</p>
                <p className="font-mono font-medium text-white">10</p>
              </div>
              <div className="p-4 flex flex-col items-center text-center">
                <Lock className="h-4 w-4 text-muted-foreground mb-2" />
                <p className="text-xs text-muted-foreground">Contribution</p>
                <p className="font-mono font-medium text-white">50k / cycle</p>
              </div>
              <div className="p-4 flex flex-col items-center text-center">
                <Calendar className="h-4 w-4 text-muted-foreground mb-2" />
                <p className="text-xs text-muted-foreground">Cycle</p>
                <p className="font-mono font-medium text-white">Monthly</p>
              </div>
              <div className="p-4 flex flex-col items-center text-center">
                <Trophy className="h-4 w-4 text-gold mb-2" />
                <p className="text-xs text-muted-foreground">Your Position</p>
                <p className="font-mono font-medium text-white text-xs">
                  #7 (Next Month)
                </p>
              </div>
            </div>

            <div className="p-6">
              <div className="flex justify-between items-center mb-4">
                <h4 className="text-sm font-semibold">Payment Schedule</h4>
                <button className="text-xs text-gold hover:underline">
                  View All
                </button>
              </div>

              <div className="space-y-3">
                {[
                  {
                    num: 6,
                    state: "current",
                    name: "John Doe",
                    amount: "500,000 XAF",
                  },
                  { num: 7, state: "next", name: "You", amount: "500,000 XAF" },
                  {
                    num: 8,
                    state: "upcoming",
                    name: "Marie K.",
                    amount: "500,000 XAF",
                  },
                ].map((item, i) => (
                  <div
                    key={i}
                    className={`flex items-center justify-between p-3 rounded-lg border ${item.state === "current" ? "bg-gold/5 border-gold/30" : item.state === "next" ? "bg-surface-3 border-border" : "bg-surface-2/50 border-transparent border-t border-b"}`}
                  >
                    <div className="flex items-center gap-4">
                      <div
                        className={`h-8 w-8 rounded-full flex items-center justify-center font-mono text-sm ${item.state === "current" ? "bg-gold text-black font-bold" : "bg-surface-3 text-muted-foreground"}`}
                      >
                        {item.num}
                      </div>
                      <div>
                        <p
                          className={`text-sm font-medium ${item.state === "current" ? "text-white" : item.state === "next" ? "text-gold" : "text-muted-foreground"}`}
                        >
                          {item.name}
                        </p>
                        <p className="text-xs text-muted-foreground">
                          {item.state === "current"
                            ? "Disbursing this week"
                            : item.state === "next"
                              ? "Your upcoming payout"
                              : "Scheduled"}
                        </p>
                      </div>
                    </div>
                    <div className="font-mono text-sm font-medium text-white text-right">
                      {item.amount}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Action / Invites Column */}
        <div className="flex flex-col gap-6">
          <Card className="glass-panel">
            <CardHeader className="pb-3">
              <CardTitle className="text-sm text-muted-foreground">
                Next Action Required
              </CardTitle>
            </CardHeader>
            <CardContent>
              <h3 className="text-xl font-bold font-display text-white mb-2">
                Cycle #6 Contribution
              </h3>
              <div className="flex justify-between text-sm mb-4">
                <span className="text-muted-foreground">Amount Due</span>
                <span className="font-mono font-bold text-danger">
                  50,000 XAF
                </span>
              </div>
              <div className="flex justify-between text-sm mb-6 pb-4 border-b border-border">
                <span className="text-muted-foreground">Due Date</span>
                <span className="text-white">In 4 days (Oct 31)</span>
              </div>
              <Button className="w-full">Make Payment</Button>
            </CardContent>
          </Card>

          <Card className="glass-panel">
            <CardHeader className="pb-4">
              <CardTitle className="text-sm">Pending Invitations</CardTitle>
            </CardHeader>
            <CardContent className="flex flex-col gap-3">
              <div className="bg-surface-2 p-4 rounded-lg border border-border">
                <div className="flex justify-between items-start mb-2">
                  <p className="text-sm font-bold text-white">
                    Beta Syndicate (Aggressive)
                  </p>
                  <Badge variant="outline" className="text-[10px]">
                    Weekly
                  </Badge>
                </div>
                <p className="text-xs text-muted-foreground mb-4">
                  100k XAF contribution • 5/10 filled
                </p>
                <div className="flex gap-2">
                  <Button size="sm" className="flex-1 text-xs h-8">
                    Accept
                  </Button>
                  <Button
                    size="sm"
                    variant="secondary"
                    className="flex-1 text-xs h-8"
                  >
                    Decline
                  </Button>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
