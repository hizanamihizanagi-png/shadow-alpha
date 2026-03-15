"use client";

import { motion } from "framer-motion";
import { Sparkles, Check, Crown, Zap, Star, ArrowRight } from "lucide-react";

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { APP_CONFIG } from "@/lib/constants";
import {
  useCurrentSubscription,
  useSubscriptionPlans,
  useUpgradeSubscription,
} from "@/hooks/use-subscription";
import { formatCurrency } from "@/lib/utils";

const PLAN_META: Record<
  string,
  {
    label: string;
    icon: typeof Star;
    color: string;
    bgColor: string;
    borderColor: string;
    popular?: boolean;
  }
> = {
  free: {
    label: "Free",
    icon: Star,
    color: "text-muted-foreground",
    bgColor: "bg-surface-3",
    borderColor: "border-border",
  },
  alpha: {
    label: "Alpha",
    icon: Zap,
    color: "text-info",
    bgColor: "bg-info/10",
    borderColor: "border-info/30",
  },
  premier: {
    label: "Premier",
    icon: Sparkles,
    color: "text-gold",
    bgColor: "bg-gold/10",
    borderColor: "border-gold/30",
    popular: true,
  },
  black_card: {
    label: "Black Card",
    icon: Crown,
    color: "text-white",
    bgColor: "bg-white/5",
    borderColor: "border-white/20",
  },
};

export default function SubscriptionPage() {
  const { data: plansData, isLoading: isPlansLoading } = useSubscriptionPlans();
  const { data: currentData } = useCurrentSubscription();
  const upgrade = useUpgradeSubscription();

  const currentPlan = String(currentData?.data?.plan ?? "free");
  const plans = plansData?.data ?? [];

  return (
    <div className="flex flex-col gap-8 pb-10">
      <div className="flex flex-col gap-2 text-center">
        <h1 className="text-3xl font-display font-bold tracking-tight text-white">
          Choisissez Votre Plan
        </h1>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Débloquez l&apos;intégralité de la puissance quantitative Shadow Alpha.
          Tous les plans incluent l&apos;accès à la communauté.
        </p>
      </div>

      {/* Plans Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {isPlansLoading ? (
          <Card className="glass-panel md:col-span-2 lg:col-span-4">
            <CardContent className="p-6 text-sm text-muted-foreground">
              Chargement des plans...
            </CardContent>
          </Card>
        ) : (
          plans.map((plan, i) => {
            const meta = PLAN_META[String(plan.name)] ?? PLAN_META.free;
            const isCurrent = String(plan.name) === currentPlan;
            return (
              <motion.div
                key={String(plan.name)}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: i * 0.1 }}
              >
                <Card
                  className={`glass-panel relative overflow-hidden transition-all hover:scale-[1.02] ${meta.borderColor} ${
                    meta.popular ? "ring-1 ring-gold/40" : ""
                  }`}
                >
                  {meta.popular && (
                    <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-gold/50 via-gold to-gold/50" />
                  )}
                  <CardHeader className="text-center pb-2">
                    {meta.popular && (
                      <Badge className="bg-gold/20 text-gold border-gold/30 mx-auto mb-2 w-fit">
                        Plus Populaire
                      </Badge>
                    )}
                    <div
                      className={`h-14 w-14 rounded-full ${meta.bgColor} flex items-center justify-center mx-auto mb-3`}
                    >
                      <meta.icon className={`h-7 w-7 ${meta.color}`} />
                    </div>
                    <CardTitle className="text-xl font-display text-white">
                      {meta.label}
                    </CardTitle>
                    <div className="mt-2">
                      {plan.price_fcfa === 0 ? (
                        <span className="text-3xl font-bold font-mono text-white">
                          Gratuit
                        </span>
                      ) : (
                        <div className="flex items-baseline justify-center gap-1">
                          <span className="text-3xl font-bold font-mono text-white">
                            {formatCurrency(
                              plan.price_fcfa,
                              APP_CONFIG.currency as any,
                            )}
                          </span>
                          <span className="text-sm text-muted-foreground">
                            /mois
                          </span>
                        </div>
                      )}
                    </div>
                  </CardHeader>
                  <CardContent className="flex flex-col gap-4">
                    <div className="flex flex-col gap-2.5">
                      {(plan.features ?? []).map((feature) => (
                        <div
                          key={feature}
                          className="flex items-center gap-2 text-sm"
                        >
                          <Check className={`h-4 w-4 ${meta.color} shrink-0`} />
                          <span className="text-muted-foreground">
                            {feature}
                          </span>
                        </div>
                      ))}
                    </div>
                    <Button
                      variant={isCurrent ? "secondary" : "default"}
                      className={`w-full mt-2 ${
                        meta.popular
                          ? "bg-gold hover:bg-gold/90 text-surface"
                          : ""
                      }`}
                      disabled={isCurrent || upgrade.isPending}
                      onClick={() => upgrade.mutate(String(plan.name))}
                    >
                      {isCurrent ? (
                        "Plan Actuel"
                      ) : (
                        <>
                          Passer à {meta.label}
                          <ArrowRight className="ml-2 h-4 w-4" />
                        </>
                      )}
                    </Button>
                  </CardContent>
                </Card>
              </motion.div>
            );
          })
        )}
      </div>

      {/* FAQ */}
      <Card className="glass-panel">
        <CardHeader>
          <CardTitle className="text-lg font-display">
            Questions Fréquentes
          </CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid gap-4 md:grid-cols-2">
            <div className="p-4 rounded-lg bg-surface-2 border border-border">
              <p className="font-semibold text-sm text-white mb-1">
                Puis-je changer de plan ?
              </p>
              <p className="text-xs text-muted-foreground">
                Oui, vous pouvez upgrader ou downgrader à tout moment.
                L&apos;ajustement est immédiat.
              </p>
            </div>
            <div className="p-4 rounded-lg bg-surface-2 border border-border">
              <p className="font-semibold text-sm text-white mb-1">
                Quels moyens de paiement ?
              </p>
              <p className="text-xs text-muted-foreground">
                Mobile Money (MTN MoMo, Orange Money), Carte bancaire, et
                crypto.
              </p>
            </div>
            <div className="p-4 rounded-lg bg-surface-2 border border-border">
              <p className="font-semibold text-sm text-white mb-1">
                Y a-t-il un engagement ?
              </p>
              <p className="text-xs text-muted-foreground">
                Non, tous les plans sont sans engagement. Annulez quand vous
                voulez.
              </p>
            </div>
            <div className="p-4 rounded-lg bg-surface-2 border border-border">
              <p className="font-semibold text-sm text-white mb-1">
                Que se passe-t-il à l&apos;expiration ?
              </p>
              <p className="text-xs text-muted-foreground">
                Votre plan revient automatiquement au plan Free. Vos données
                sont conservées.
              </p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
