"use client";

import { motion } from "framer-motion";
import {
  User,
  Mail,
  Phone,
  Shield,
  CreditCard,
  Trophy,
  BarChart3,
  Settings,
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

export default function ProfilePage() {
  // Mock data — will be wired to API
  const user = {
    displayName: "Alpha Trader Pro",
    email: "trader@shadow-alpha.com",
    phone: "+237 6XX XXX XXX",
    tier: "Alpha",
    kycStatus: "Vérifié",
    creditScore: 650,
    creditTier: "B",
    joinedDate: "Janvier 2026",
    stats: {
      totalPositions: 47,
      winRate: 62,
      totalPnl: 185000,
      vaultDeposits: 750000,
      tontineGroups: 3,
      shieldsActive: 1,
    },
  };

  return (
    <div className="flex flex-col gap-8 pb-10">
      {/* Profile Header */}
      <Card className="glass-panel overflow-hidden relative">
        <div className="absolute inset-0 bg-gradient-to-br from-gold/5 via-transparent to-transparent" />
        <CardContent className="p-8 relative z-10">
          <div className="flex flex-col md:flex-row items-start md:items-center gap-6">
            <div className="h-20 w-20 rounded-full bg-gold/20 border-2 border-gold flex items-center justify-center">
              <span className="text-2xl font-display font-bold text-gold">
                {user.displayName.substring(0, 2).toUpperCase()}
              </span>
            </div>
            <div className="flex-1">
              <div className="flex items-center gap-3 mb-1">
                <h1 className="text-2xl font-display font-bold text-white">
                  {user.displayName}
                </h1>
                <Badge className="bg-gold/20 text-gold border-gold/30">
                  {user.tier}
                </Badge>
                <Badge className="bg-success/20 text-success border-success/30">
                  {user.kycStatus}
                </Badge>
              </div>
              <p className="text-muted-foreground text-sm">
                Membre depuis {user.joinedDate}
              </p>
            </div>
            <Button variant="secondary" size="sm">
              <Settings className="mr-2 h-4 w-4" />
              Modifier
            </Button>
          </div>
        </CardContent>
      </Card>

      {/* Contact Info */}
      <div className="grid gap-4 md:grid-cols-3">
        <Card className="glass-panel">
          <CardContent className="p-4 flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-surface-3 flex items-center justify-center">
              <Mail className="h-5 w-5 text-muted-foreground" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Email</p>
              <p className="text-sm text-white">{user.email}</p>
            </div>
          </CardContent>
        </Card>
        <Card className="glass-panel">
          <CardContent className="p-4 flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-surface-3 flex items-center justify-center">
              <Phone className="h-5 w-5 text-muted-foreground" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Téléphone</p>
              <p className="text-sm text-white">{user.phone}</p>
            </div>
          </CardContent>
        </Card>
        <Card className="glass-panel">
          <CardContent className="p-4 flex items-center gap-3">
            <div className="h-10 w-10 rounded-full bg-gold/10 flex items-center justify-center">
              <CreditCard className="h-5 w-5 text-gold" />
            </div>
            <div>
              <p className="text-xs text-muted-foreground">Score Crédit</p>
              <p className="text-sm font-mono font-bold text-white">
                {user.creditScore}/1000{" "}
                <span className="text-gold text-xs">({user.creditTier})</span>
              </p>
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Performance Stats */}
      <div>
        <h2 className="text-xl font-display font-bold text-white mb-4 border-b border-border pb-2">
          Statistiques
        </h2>
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
          >
            <Card className="glass-panel hover:border-gold/30 transition-colors">
              <CardContent className="p-5 flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-gold/10 flex items-center justify-center">
                  <BarChart3 className="h-6 w-6 text-gold" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">
                    Positions Totales
                  </p>
                  <p className="text-xl font-mono font-bold text-white">
                    {user.stats.totalPositions}
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
          >
            <Card className="glass-panel hover:border-success/30 transition-colors">
              <CardContent className="p-5 flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-success/10 flex items-center justify-center">
                  <Trophy className="h-6 w-6 text-success" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">Win Rate</p>
                  <p className="text-xl font-mono font-bold text-success">
                    {user.stats.winRate}%
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
          >
            <Card className="glass-panel hover:border-gold/30 transition-colors">
              <CardContent className="p-5 flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-gold/10 flex items-center justify-center">
                  <span className="text-gold font-display font-bold">
                    PnL
                  </span>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">PnL Total</p>
                  <p className="text-xl font-mono font-bold text-success">
                    +{user.stats.totalPnl.toLocaleString()}{" "}
                    {APP_CONFIG.currency}
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <Card className="glass-panel">
              <CardContent className="p-5 flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-surface-3 flex items-center justify-center">
                  <span className="text-gold font-display font-bold text-sm">
                    $V
                  </span>
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">
                    Dépôts Vault
                  </p>
                  <p className="text-xl font-mono font-bold text-white">
                    {user.stats.vaultDeposits.toLocaleString()}{" "}
                    {APP_CONFIG.currency}
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
          >
            <Card className="glass-panel">
              <CardContent className="p-5 flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-surface-3 flex items-center justify-center">
                  <User className="h-6 w-6 text-muted-foreground" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">
                    Groupes Tontine
                  </p>
                  <p className="text-xl font-mono font-bold text-white">
                    {user.stats.tontineGroups}
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
          >
            <Card className="glass-panel">
              <CardContent className="p-5 flex items-center gap-4">
                <div className="h-12 w-12 rounded-full bg-info/10 flex items-center justify-center">
                  <Shield className="h-6 w-6 text-info" />
                </div>
                <div>
                  <p className="text-xs text-muted-foreground">
                    Shields Actifs
                  </p>
                  <p className="text-xl font-mono font-bold text-info">
                    {user.stats.shieldsActive}
                  </p>
                </div>
              </CardContent>
            </Card>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
