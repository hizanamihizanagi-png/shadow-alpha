"use client";

import { motion } from "framer-motion";
import {
  Vault,
  TrendingUp,
  ArrowUpRight,
  ArrowDownLeft,
  Lock,
  Percent,
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

export default function VaultPage() {
  // Mock data — will be replaced with API calls
  const vaultData = {
    totalDeposited: 750000,
    currentValue: 812500,
    netYield: 62500,
    apy: 9.75,
    netApy: 6.34,
    performanceFee: 35,
    deposits: [
      {
        id: "1",
        amount: 500000,
        date: "2025-12-01",
        status: "active",
        yield: 42000,
      },
      {
        id: "2",
        amount: 250000,
        date: "2026-01-15",
        status: "active",
        yield: 20500,
      },
    ],
  };

  return (
    <div className="flex flex-col gap-8 pb-10">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-display font-bold tracking-tight text-white">
          Shadow Vault
        </h1>
        <p className="text-muted-foreground">
          Déposez vos capitaux et générez du rendement automatiquement.
        </p>
      </div>

      {/* Vault KPIs */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="glass-panel group relative overflow-hidden transition-all hover:bg-surface-2/80">
          <div className="absolute right-0 top-0 h-24 w-24 -translate-y-8 translate-x-8 rounded-full bg-gold/10 blur-2xl transition-all group-hover:bg-gold/20" />
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Total Déposé
            </CardTitle>
            <Vault className="h-4 w-4 text-gold" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl lg:text-3xl font-bold font-mono text-white">
              {vaultData.totalDeposited.toLocaleString()} {APP_CONFIG.currency}
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Rendement Net
            </CardTitle>
            <TrendingUp className="h-4 w-4 text-success" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-success">
              +{vaultData.netYield.toLocaleString()} {APP_CONFIG.currency}
            </div>
            <p className="mt-1 text-xs text-muted-foreground">
              APY net: {vaultData.netApy}%
            </p>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              APY Brut
            </CardTitle>
            <Percent className="h-4 w-4 text-gold" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-gold">
              {vaultData.apy}%
            </div>
            <p className="mt-1 text-xs text-muted-foreground">
              Frais performance: {vaultData.performanceFee}%
            </p>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Valeur Actuelle
            </CardTitle>
            <Lock className="h-4 w-4 text-gold" />
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold font-mono text-white">
              {vaultData.currentValue.toLocaleString()} {APP_CONFIG.currency}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Actions */}
      <div className="grid gap-4 md:grid-cols-2">
        <Card className="glass-panel border-gold/20">
          <CardHeader>
            <CardTitle className="text-xl font-display flex items-center gap-2">
              <ArrowUpRight className="h-5 w-5 text-success" />
              Déposer
            </CardTitle>
            <CardDescription>
              Déposez des fonds dans le Shadow Vault pour générer du rendement
              passif.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-4">
              <div className="relative">
                <input
                  type="number"
                  placeholder="Montant en FCFA"
                  className="w-full rounded-lg border border-border bg-surface-2 px-4 py-3 text-white placeholder-muted-foreground focus:border-gold focus:outline-none font-mono"
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">
                  {APP_CONFIG.currency}
                </span>
              </div>
              <div className="flex gap-2">
                {[25000, 50000, 100000, 500000].map((amt) => (
                  <button
                    key={amt}
                    className="flex-1 rounded-md bg-surface-3 py-2 text-xs font-mono text-muted-foreground hover:bg-surface-2 hover:text-gold transition-colors border border-border"
                  >
                    {(amt / 1000).toFixed(0)}k
                  </button>
                ))}
              </div>
              <Button variant="default" className="w-full">
                <ArrowUpRight className="mr-2 h-4 w-4" />
                Déposer dans le Vault
              </Button>
            </div>
          </CardContent>
        </Card>

        <Card className="glass-panel">
          <CardHeader>
            <CardTitle className="text-xl font-display flex items-center gap-2">
              <ArrowDownLeft className="h-5 w-5 text-danger" />
              Retirer
            </CardTitle>
            <CardDescription>
              Retirez vos fonds à tout moment. Le rendement est calculé
              quotidiennement.
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="flex flex-col gap-4">
              <div className="relative">
                <input
                  type="number"
                  placeholder="Montant à retirer"
                  className="w-full rounded-lg border border-border bg-surface-2 px-4 py-3 text-white placeholder-muted-foreground focus:border-gold focus:outline-none font-mono"
                />
                <span className="absolute right-4 top-1/2 -translate-y-1/2 text-muted-foreground text-sm">
                  {APP_CONFIG.currency}
                </span>
              </div>
              <Button variant="secondary" className="w-full">
                <ArrowDownLeft className="mr-2 h-4 w-4" />
                Retirer du Vault
              </Button>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Deposit History */}
      <div>
        <h2 className="text-xl font-display font-bold text-white mb-4 border-b border-border pb-2">
          Historique des Dépôts
        </h2>
        <div className="grid gap-3">
          {vaultData.deposits.map((dep) => (
            <motion.div
              key={dep.id}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
            >
              <Card className="glass-panel hover:border-gold/30 transition-colors">
                <CardContent className="p-4 flex items-center justify-between">
                  <div className="flex items-center gap-4">
                    <div className="h-10 w-10 rounded-full bg-gold/10 flex items-center justify-center">
                      <Vault className="h-5 w-5 text-gold" />
                    </div>
                    <div>
                      <p className="font-mono text-sm font-bold text-white">
                        {dep.amount.toLocaleString()} {APP_CONFIG.currency}
                      </p>
                      <p className="text-xs text-muted-foreground">
                        Déposé le {dep.date}
                      </p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-mono font-bold text-success">
                      +{dep.yield.toLocaleString()} {APP_CONFIG.currency}
                    </p>
                    <Badge className="bg-success/20 text-success border-success/30">
                      {dep.status}
                    </Badge>
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
