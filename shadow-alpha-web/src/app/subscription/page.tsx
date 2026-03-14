"use client";

import { motion } from "framer-motion";
import {
  Sparkles,
  Check,
  Crown,
  Zap,
  Star,
  ArrowRight,
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

const plans = [
  {
    name: "Free",
    price: 0,
    icon: Star,
    color: "text-muted-foreground",
    bgColor: "bg-surface-3",
    borderColor: "border-border",
    features: [
      "3 positions/jour",
      "Analytics de base",
      "Accès communautaire",
    ],
    current: true,
  },
  {
    name: "Alpha",
    price: 2500,
    icon: Zap,
    color: "text-info",
    bgColor: "bg-info/10",
    borderColor: "border-info/30",
    features: [
      "10 positions/jour",
      "Pricing engine live",
      "Score de crédit",
      "Groupes tontine",
    ],
    popular: false,
  },
  {
    name: "Premier",
    price: 7500,
    icon: Sparkles,
    color: "text-gold",
    bgColor: "bg-gold/10",
    borderColor: "border-gold/30",
    features: [
      "Positions illimitées",
      "Shield insurance",
      "Position loans",
      "Copy-trading",
      "API access (100 req/jour)",
    ],
    popular: true,
  },
  {
    name: "Black Card",
    price: 25000,
    icon: Crown,
    color: "text-white",
    bgColor: "bg-white/5",
    borderColor: "border-white/20",
    features: [
      "Tout Premier inclus",
      "Support prioritaire",
      "Vault yield boost +1%",
      "API (10K req/jour)",
      "Dashboard analytics custom",
    ],
    popular: false,
  },
];

export default function SubscriptionPage() {
  return (
    <div className="flex flex-col gap-8 pb-10">
      <div className="flex flex-col gap-2 text-center">
        <h1 className="text-3xl font-display font-bold tracking-tight text-white">
          Choisissez Votre Plan
        </h1>
        <p className="text-muted-foreground max-w-xl mx-auto">
          Débloquez l&apos;intégralité de la puissance quantitative Shadow Alpha. Tous
          les plans incluent l&apos;accès à la communauté.
        </p>
      </div>

      {/* Plans Grid */}
      <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-4">
        {plans.map((plan, i) => (
          <motion.div
            key={plan.name}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: i * 0.1 }}
          >
            <Card
              className={`glass-panel relative overflow-hidden transition-all hover:scale-[1.02] ${plan.borderColor} ${
                plan.popular ? "ring-1 ring-gold/40" : ""
              }`}
            >
              {plan.popular && (
                <div className="absolute top-0 left-0 right-0 h-1 bg-gradient-to-r from-gold/50 via-gold to-gold/50" />
              )}
              <CardHeader className="text-center pb-2">
                {plan.popular && (
                  <Badge className="bg-gold/20 text-gold border-gold/30 mx-auto mb-2 w-fit">
                    Plus Populaire
                  </Badge>
                )}
                <div
                  className={`h-14 w-14 rounded-full ${plan.bgColor} flex items-center justify-center mx-auto mb-3`}
                >
                  <plan.icon className={`h-7 w-7 ${plan.color}`} />
                </div>
                <CardTitle className="text-xl font-display text-white">
                  {plan.name}
                </CardTitle>
                <div className="mt-2">
                  {plan.price === 0 ? (
                    <span className="text-3xl font-bold font-mono text-white">
                      Gratuit
                    </span>
                  ) : (
                    <div className="flex items-baseline justify-center gap-1">
                      <span className="text-3xl font-bold font-mono text-white">
                        {plan.price.toLocaleString()}
                      </span>
                      <span className="text-sm text-muted-foreground">
                        {APP_CONFIG.currency}/mois
                      </span>
                    </div>
                  )}
                </div>
              </CardHeader>
              <CardContent className="flex flex-col gap-4">
                <div className="flex flex-col gap-2.5">
                  {plan.features.map((feature) => (
                    <div
                      key={feature}
                      className="flex items-center gap-2 text-sm"
                    >
                      <Check className={`h-4 w-4 ${plan.color} shrink-0`} />
                      <span className="text-muted-foreground">{feature}</span>
                    </div>
                  ))}
                </div>
                <Button
                  variant={plan.current ? "secondary" : "default"}
                  className={`w-full mt-2 ${
                    plan.popular
                      ? "bg-gold hover:bg-gold/90 text-surface"
                      : ""
                  }`}
                  disabled={plan.current}
                >
                  {plan.current ? (
                    "Plan Actuel"
                  ) : (
                    <>
                      Passer à {plan.name}
                      <ArrowRight className="ml-2 h-4 w-4" />
                    </>
                  )}
                </Button>
              </CardContent>
            </Card>
          </motion.div>
        ))}
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
