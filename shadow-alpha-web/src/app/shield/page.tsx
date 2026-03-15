"use client";

import { motion } from "framer-motion";
import { useState } from "react";
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
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { APP_CONFIG } from "@/lib/constants";
import { formatCurrency } from "@/lib/utils";
import { usePositions } from "@/hooks/use-positions";
import {
  useActivateShield,
  useClaimShield,
  useShieldContracts,
  useShieldQuote,
} from "@/hooks/use-shield";

const toNumber = (value: unknown) => {
  if (typeof value === "number") return value;
  if (typeof value === "string") return Number(value);
  return 0;
};

export default function ShieldPage() {
  const { data: positionsData, isLoading, isError } = usePositions();
  const { data: contractsData } = useShieldContracts();
  const activateShield = useActivateShield();
  const claimShield = useClaimShield();

  const [quotePositionId, setQuotePositionId] = useState<string | null>(null);
  const { data: quoteData, isFetching: isQuoteLoading } = useShieldQuote(
    quotePositionId ?? "",
    Boolean(quotePositionId),
  );

  const positions = positionsData?.data ?? [];
  const contracts = (Array.isArray(contractsData?.data)
    ? contractsData.data
    : []) as Record<string, unknown>[];

  const positionsById = new Map(positions.map((pos) => [pos.id, pos]));
  const contractsByPositionId = new Map<string, Record<string, unknown>>();
  contracts.forEach((contract) => {
    const key = String(contract.position_id ?? contract.positionId ?? "");
    if (key) contractsByPositionId.set(key, contract);
  });

  const activeShields = contracts.filter(
    (contract) => String(contract.status ?? "") === "active",
  );
  const totalPremiumPaid = activeShields.reduce(
    (sum, contract) => sum + toNumber(contract.premium_paid ?? contract.premiumPaid),
    0,
  );
  const totalProtected = activeShields.reduce((sum, contract) => {
    const positionId = String(contract.position_id ?? contract.positionId ?? "");
    const position = positionsById.get(positionId);
    const coveragePct = toNumber(
      contract.coverage_pct ?? contract.coveragePct ?? 0,
    );
    if (!position) return sum;
    return sum + (position.stake * coveragePct) / 100;
  }, 0);

  if (isError) {
    return <div className="p-8 text-danger">Error loading shield data</div>;
  }

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
              {activeShields.length}
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
              {formatCurrency(totalProtected, APP_CONFIG.currency as any)}
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
              {formatCurrency(totalPremiumPaid, APP_CONFIG.currency as any)}
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
              {formatCurrency(0, APP_CONFIG.currency as any)}
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
          {isLoading ? (
            <Card className="glass-panel">
              <CardContent className="p-6 text-sm text-muted-foreground">
                Chargement des positions...
              </CardContent>
            </Card>
          ) : positions.length === 0 ? (
            <Card className="glass-panel">
              <CardContent className="p-6 text-sm text-muted-foreground">
                Aucune position active à protéger.
              </CardContent>
            </Card>
          ) : (
            positions.map((pos, i) => {
              const contract = contractsByPositionId.get(pos.id);
              const isShielded = Boolean(contract);
              const isActive = pos.status === "active";
              const isQuoteTarget = quotePositionId === pos.id;
              const quote = isQuoteTarget ? quoteData?.data : null;
              const coveragePct = toNumber(
                contract?.coverage_pct ?? contract?.coveragePct ?? 0,
              );
              const premiumPaid = toNumber(
                contract?.premium_paid ?? contract?.premiumPaid ?? 0,
              );
              return (
                <motion.div
                  key={pos.id}
                  initial={{ opacity: 0, y: 12 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: i * 0.05 }}
                >
                  <Card
                    className={`glass-panel transition-colors ${isShielded ? "border-info/30" : "hover:border-gold/30"}`}
                  >
                    <CardContent className="p-5 flex flex-col lg:flex-row items-start lg:items-center justify-between gap-4">
                      <div className="flex items-center gap-4">
                        <div
                          className={`h-12 w-12 rounded-full flex items-center justify-center ${isShielded ? "bg-info/10" : "bg-surface-3"}`}
                        >
                          {isShielded ? (
                            <ShieldCheck className="h-6 w-6 text-info" />
                          ) : (
                            <ShieldAlert className="h-6 w-6 text-muted-foreground" />
                          )}
                        </div>
                        <div>
                          <p className="font-semibold text-white">{pos.teams}</p>
                          <p className="text-sm text-muted-foreground font-mono">
                            Mise:{" "}
                            {formatCurrency(
                              pos.stake,
                              APP_CONFIG.currency as any,
                            )}{" "}
                            · Cote: {pos.odds}x
                          </p>
                          <Badge
                            variant="outline"
                            className="mt-2 text-[10px] border-border text-muted-foreground"
                          >
                            {pos.status}
                          </Badge>
                        </div>
                      </div>

                      <div className="flex items-center gap-4">
                        {isShielded ? (
                          <div className="text-right flex flex-col items-end gap-2">
                            <Badge className="bg-info/20 text-info border-info/30">
                              Protégé {coveragePct}%
                            </Badge>
                            <p className="text-xs text-muted-foreground font-mono">
                              Prime payée:{" "}
                              {formatCurrency(
                                premiumPaid,
                                APP_CONFIG.currency as any,
                              )}
                            </p>
                            {String(contract?.status ?? "") === "active" && (
                              <Button
                                variant="secondary"
                                size="sm"
                                onClick={() =>
                                  claimShield.mutate(String(contract?.id ?? ""))
                                }
                                disabled={claimShield.isPending}
                              >
                                {claimShield.isPending ? "Traitement..." : "Réclamer"}
                              </Button>
                            )}
                          </div>
                        ) : (
                          <div className="flex flex-col sm:flex-row items-start sm:items-center gap-3">
                            <div className="text-right">
                              <p className="text-xs text-muted-foreground">
                                Prime estimée
                              </p>
                              <p className="font-mono text-sm font-bold text-gold">
                                {quote
                                  ? formatCurrency(
                                      toNumber(quote.premium),
                                      APP_CONFIG.currency as any,
                                    )
                                  : "--"}
                              </p>
                              {quote && (
                                <p className="text-xs text-muted-foreground">
                                  Couverture {quote.coverage_pct}% ·
                                  Payout{" "}
                                  {formatCurrency(
                                    toNumber(quote.estimated_payout),
                                    APP_CONFIG.currency as any,
                                  )}
                                </p>
                              )}
                            </div>
                            <div className="flex flex-col gap-2">
                              <Button
                                variant="secondary"
                                size="sm"
                                onClick={() => setQuotePositionId(pos.id)}
                                disabled={!isActive || (isQuoteTarget && isQuoteLoading)}
                              >
                                {isQuoteTarget && isQuoteLoading
                                  ? "Calcul..."
                                  : "Estimer"}
                              </Button>
                              <Button
                                variant="default"
                                size="sm"
                                onClick={() => {
                                  const coverage = quote?.coverage_pct ?? 70;
                                  activateShield.mutate({
                                    position_id: pos.id,
                                    coverage_pct: coverage,
                                  }, {
                                    onSuccess: () => setQuotePositionId(null),
                                  });
                                }}
                                disabled={!isActive || !quote || activateShield.isPending}
                              >
                                <Shield className="mr-1 h-4 w-4" />
                                {activateShield.isPending ? "Activation..." : "Activer"}
                              </Button>
                            </div>
                          </div>
                        )}
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
