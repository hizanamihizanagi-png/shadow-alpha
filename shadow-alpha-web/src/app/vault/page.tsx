"use client";

import { motion } from "framer-motion";
import { useEffect, useState } from "react";
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
import { formatCurrency, formatDate } from "@/lib/utils";
import {
  useVaultDeposit,
  useVaultPerformance,
  useVaultWithdraw,
} from "@/hooks/use-vault";

const toNumber = (value: unknown) => {
  if (typeof value === "number") return value;
  if (typeof value === "string") return Number(value);
  return 0;
};

export default function VaultPage() {
  const {
    data: performance,
    isLoading: isPerformanceLoading,
    isError: isPerformanceError,
  } = useVaultPerformance();
  const depositMutation = useVaultDeposit();
  const withdrawMutation = useVaultWithdraw();

  const [depositAmount, setDepositAmount] = useState("");
  const [selectedDepositId, setSelectedDepositId] = useState<string | null>(null);

  const deposits = performance?.data?.deposits ?? [];
  const activeDeposits = deposits.filter((deposit) => deposit.status === "active");

  useEffect(() => {
    if (!selectedDepositId && activeDeposits.length > 0) {
      setSelectedDepositId(activeDeposits[0].id);
    }
  }, [activeDeposits, selectedDepositId]);

  const totalDeposited = toNumber(performance?.data?.total_deposited);
  const currentValue = toNumber(performance?.data?.current_value);
  const netYield = toNumber(performance?.data?.net_yield);
  const apy = toNumber(performance?.data?.apy_estimate);
  const netApy = toNumber(performance?.data?.net_apy);
  const grossYield = toNumber(performance?.data?.gross_yield);
  const performanceFeeAmount = toNumber(performance?.data?.performance_fee);
  const performanceFeePct =
    grossYield > 0 ? (performanceFeeAmount / grossYield) * 100 : 0;

  const selectedDeposit = deposits.find(
    (deposit) => deposit.id === selectedDepositId,
  );

  const handleDeposit = () => {
    if (!depositAmount || Number(depositAmount) <= 0) return;
    depositMutation.mutate(depositAmount, {
      onSuccess: () => setDepositAmount(""),
    });
  };

  const handleWithdraw = () => {
    if (!selectedDepositId) return;
    withdrawMutation.mutate(selectedDepositId);
  };

  if (isPerformanceError) {
    return <div className="p-8 text-danger">Error loading vault data</div>;
  }

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
              {isPerformanceLoading ? (
                <div className="h-8 w-32 animate-pulse bg-surface-3 rounded" />
              ) : (
                formatCurrency(totalDeposited, APP_CONFIG.currency as any)
              )}
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
              {isPerformanceLoading ? (
                <div className="h-8 w-28 animate-pulse bg-surface-3 rounded" />
              ) : (
                `+${formatCurrency(netYield, APP_CONFIG.currency as any)}`
              )}
            </div>
            <p className="mt-1 text-xs text-muted-foreground">
              APY net: {netApy.toFixed(2)}%
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
              {isPerformanceLoading ? (
                <div className="h-8 w-16 animate-pulse bg-surface-3 rounded" />
              ) : (
                `${apy.toFixed(2)}%`
              )}
            </div>
            <p className="mt-1 text-xs text-muted-foreground">
              Frais performance: {performanceFeePct.toFixed(2)}%
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
              {isPerformanceLoading ? (
                <div className="h-8 w-32 animate-pulse bg-surface-3 rounded" />
              ) : (
                formatCurrency(currentValue, APP_CONFIG.currency as any)
              )}
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
                  value={depositAmount}
                  onChange={(event) => setDepositAmount(event.target.value)}
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
                    type="button"
                    onClick={() => setDepositAmount(String(amt))}
                    className="flex-1 rounded-md bg-surface-3 py-2 text-xs font-mono text-muted-foreground hover:bg-surface-2 hover:text-gold transition-colors border border-border"
                  >
                    {(amt / 1000).toFixed(0)}k
                  </button>
                ))}
              </div>
              <Button
                variant="default"
                className="w-full"
                onClick={handleDeposit}
                disabled={depositMutation.isPending}
              >
                <ArrowUpRight className="mr-2 h-4 w-4" />
                {depositMutation.isPending
                  ? "Dépôt en cours..."
                  : "Déposer dans le Vault"}
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
              <div className="flex flex-col gap-2">
                <label className="text-xs font-medium text-muted-foreground">
                  Dépôt à retirer
                </label>
                <select
                  value={selectedDepositId ?? ""}
                  onChange={(event) => setSelectedDepositId(event.target.value)}
                  className="w-full rounded-lg border border-border bg-surface-2 px-4 py-3 text-white focus:border-gold focus:outline-none font-mono"
                  disabled={activeDeposits.length === 0}
                >
                  {activeDeposits.length === 0 && (
                    <option value="">Aucun dépôt actif</option>
                  )}
                  {activeDeposits.map((deposit) => (
                    <option key={deposit.id} value={deposit.id}>
                      {formatCurrency(
                        toNumber(deposit.amount),
                        APP_CONFIG.currency as any,
                      )}{" "}
                      · {formatDate(deposit.created_at, "dd MMM yyyy")}
                    </option>
                  ))}
                </select>
              </div>
              {selectedDeposit && (
                <div className="rounded-lg border border-border bg-surface-2 px-4 py-3 text-sm text-muted-foreground">
                  Montant sélectionné:{" "}
                  <span className="font-mono text-white">
                    {formatCurrency(
                      toNumber(selectedDeposit.amount),
                      APP_CONFIG.currency as any,
                    )}
                  </span>
                </div>
              )}
              <Button
                variant="secondary"
                className="w-full"
                onClick={handleWithdraw}
                disabled={!selectedDepositId || withdrawMutation.isPending}
              >
                <ArrowDownLeft className="mr-2 h-4 w-4" />
                {withdrawMutation.isPending
                  ? "Retrait en cours..."
                  : "Retirer du Vault"}
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
          {isPerformanceLoading ? (
            <Card className="glass-panel">
              <CardContent className="p-6 text-sm text-muted-foreground">
                Chargement des dépôts...
              </CardContent>
            </Card>
          ) : deposits.length === 0 ? (
            <Card className="glass-panel">
              <CardContent className="p-6 text-sm text-muted-foreground">
                Aucun dépôt enregistré pour le moment.
              </CardContent>
            </Card>
          ) : (
            deposits.map((dep) => {
              const depositAmount = toNumber(dep.amount);
              const depositYield =
                totalDeposited > 0
                  ? (depositAmount / totalDeposited) * netYield
                  : 0;
              return (
                <motion.div
                  key={dep.id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                >
                  <Card className="glass-panel hover:border-gold/30 transition-colors">
                    <CardContent className="p-4 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
                      <div className="flex items-center gap-4">
                        <div className="h-10 w-10 rounded-full bg-gold/10 flex items-center justify-center">
                          <Vault className="h-5 w-5 text-gold" />
                        </div>
                        <div>
                          <p className="font-mono text-sm font-bold text-white">
                            {formatCurrency(
                              depositAmount,
                              APP_CONFIG.currency as any,
                            )}
                          </p>
                          <p className="text-xs text-muted-foreground">
                            Déposé le{" "}
                            {formatDate(dep.created_at, "dd MMM yyyy")}
                          </p>
                        </div>
                      </div>
                      <div className="text-right">
                        <p className="text-sm font-mono font-bold text-success">
                          +{formatCurrency(depositYield, APP_CONFIG.currency as any)}
                        </p>
                        <Badge
                          className={
                            dep.status === "active"
                              ? "bg-success/20 text-success border-success/30"
                              : "bg-surface-3 text-muted-foreground border-border"
                          }
                        >
                          {dep.status}
                        </Badge>
                      </div>
                    </CardContent>
                  </Card>
                </motion.div>
              );
            })
          )}
        </div>
      </div>
    </div>
  );
}
