"use client";

import { motion } from "framer-motion";
import {
  Shield,
  ShieldCheck,
  ShieldAlert,
  Zap,
  TrendingDown,
  Calculator,
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

export default function ShieldPage() {
  // Mock data — will be wired to API
  const mockPositions = [
    {
      id: "1",
      teams: "PSG vs Marseille",
      stake: 25000,
      odds: 2.1,
      currentProb: 0.52,
      shielded: false,
      premiumEstimate: 3750,
      coveragePct: 70,
    },
    {
      id: "2",
      teams: "Liverpool vs Arsenal",
      stake: 50000,
      odds: 1.85,
      currentProb: 0.6,
      shielded: true,
      premiumPaid: 5200,
      coveragePct: 80,
      payout: 40000,
    },
    {
      id: "3",
      teams: "Real Madrid vs Barcelona",
      stake: 100000,
      odds: 2.5,
      currentProb: 0.45,
      shielded: false,
      premiumEstimate: 18500,
      coveragePct: 70,
    },
  ];

  const stats = {
    activeShields: 1,
    totalPremiumPaid: 5200,
    totalProtected: 50000,
    claimsPaid: 0,
  };

  return (
    <div className="flex flex-col gap-8 pb-10">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-display font-bold tracking-tight text-white">
          Shadow Shield
        </h1>
        <p className="text-muted-foreground">
          Protégez vos positions avec notre assurance actuarielle. Payez une
          prime, récupérez jusqu&apos;à 80% de votre mise en cas de perte.
        </p>
      </div>

      {/* Shield Stats */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="glass-panel group relative overflow-hidden transition-all hover:bg-surface-2/80">
          <div className="absolute right-0 top-0 h-24 w-24 -translate-y-8 translate-x-8 rounded-full bg-blue-500/10 blur-2xl transition-all group-hover:bg-blue-500/20" />
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Shields Actifs
            </CardTitle>
            <ShieldCheck className="h-4 w-4 text-info" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl lg:text-3xl font-bold font-mono text-white">
              {stats.activeShields}
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Capital Protégé
            </CardTitle>
            <Shield className="h-4 w-4 text-gold" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-gold">
              {stats.totalProtected.toLocaleString()} {APP_CONFIG.currency}
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Primes Payées
            </CardTitle>
            <Calculator className="h-4 w-4 text-muted-foreground" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-white">
              {stats.totalPremiumPaid.toLocaleString()} {APP_CONFIG.currency}
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Indemnités Versées
            </CardTitle>
            <TrendingDown className="h-4 w-4 text-success" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-success">
              {stats.claimsPaid.toLocaleString()} {APP_CONFIG.currency}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* How it Works */}
      <Card className="glass-panel border-info/20">
        <CardHeader>
          <CardTitle className="text-lg font-display flex items-center gap-2">
            <Zap className="h-5 w-5 text-info" />
            Comment fonctionne Shadow Shield ?
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-3">
            <div className="flex flex-col items-center text-center gap-2 p-4 rounded-lg bg-surface-2 border border-border">
              <div className="h-12 w-12 rounded-full bg-info/10 flex items-center justify-center mb-2">
                <Shield className="h-6 w-6 text-info" />
              </div>
              <p className="font-semibold text-sm text-white">
                1. Choisissez une position
              </p>
              <p className="text-xs text-muted-foreground">
                Sélectionnez une position active à protéger
              </p>
            </div>
            <div className="flex flex-col items-center text-center gap-2 p-4 rounded-lg bg-surface-2 border border-border">
              <div className="h-12 w-12 rounded-full bg-gold/10 flex items-center justify-center mb-2">
                <Calculator className="h-6 w-6 text-gold" />
              </div>
              <p className="font-semibold text-sm text-white">
                2. Payez la prime
              </p>
              <p className="text-xs text-muted-foreground">
                Prime calculée actuariellement selon vos risques
              </p>
            </div>
            <div className="flex flex-col items-center text-center gap-2 p-4 rounded-lg bg-surface-2 border border-border">
              <div className="h-12 w-12 rounded-full bg-success/10 flex items-center justify-center mb-2">
                <ShieldCheck className="h-6 w-6 text-success" />
              </div>
              <p className="font-semibold text-sm text-white">
                3. Récupérez votre mise
              </p>
              <p className="text-xs text-muted-foreground">
                En cas de perte, récupérez jusqu&apos;à 80% automatiquement
              </p>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Positions to Shield */}
      <div>
        <h2 className="text-xl font-display font-bold text-white mb-4 border-b border-border pb-2">
          Vos Positions
        </h2>
        <div className="grid gap-4">
          {mockPositions.map((pos, i) => (
            <motion.div
              key={pos.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
            >
              <Card
                className={`glass-panel transition-colors ${pos.shielded ? "border-info/30" : "hover:border-gold/30"}`}
              >
                <CardContent className="p-5 flex flex-col md:flex-row items-start md:items-center justify-between gap-4">
                  <div className="flex items-center gap-4">
                    <div
                      className={`h-12 w-12 rounded-full flex items-center justify-center ${pos.shielded ? "bg-info/10" : "bg-surface-3"}`}
                    >
                      {pos.shielded ? (
                        <ShieldCheck className="h-6 w-6 text-info" />
                      ) : (
                        <ShieldAlert className="h-6 w-6 text-muted-foreground" />
                      )}
                    </div>
                    <div>
                      <p className="font-semibold text-white">{pos.teams}</p>
                      <p className="text-sm text-muted-foreground font-mono">
                        Mise: {pos.stake.toLocaleString()} {APP_CONFIG.currency}{" "}
                        • Cote: {pos.odds}x
                      </p>
                    </div>
                  </div>

                  <div className="flex items-center gap-4">
                    {pos.shielded ? (
                      <div className="text-right">
                        <Badge className="bg-info/20 text-info border-info/30 mb-1">
                          Protégé {pos.coveragePct}%
                        </Badge>
                        <p className="text-xs text-muted-foreground font-mono">
                          Prime payée: {pos.premiumPaid?.toLocaleString()}{" "}
                          {APP_CONFIG.currency}
                        </p>
                      </div>
                    ) : (
                      <div className="flex items-center gap-3">
                        <div className="text-right">
                          <p className="text-xs text-muted-foreground">
                            Prime estimée
                          </p>
                          <p className="font-mono text-sm font-bold text-gold">
                            {pos.premiumEstimate?.toLocaleString()}{" "}
                            {APP_CONFIG.currency}
                          </p>
                        </div>
                        <Button variant="default" size="sm">
                          <Shield className="mr-1 h-4 w-4" />
                          Activer
                        </Button>
                      </div>
                    )}
                  </div>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </div>
    </div>
  );
}
