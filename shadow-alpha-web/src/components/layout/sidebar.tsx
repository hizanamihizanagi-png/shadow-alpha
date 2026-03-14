"use client";

import { motion, AnimatePresence } from "framer-motion";
import Link from "next/link";
import { usePathname } from "next/navigation";
import {
  LayoutDashboard,
  ArrowRightLeft,
  Users,
  History,
  Settings,
  FileText,
  LogOut,
  Vault,
  Shield,
  CreditCard,
} from "lucide-react";
import { useUiStore } from "@/stores/ui-store";
import { useAuth } from "@/hooks/use-auth";
import { cn } from "@/lib/utils";
import { ROUTES, COPY } from "@/lib/constants";

const navItems = [
  { icon: LayoutDashboard, label: "dashboard", href: ROUTES.DASHBOARD },
  { icon: ArrowRightLeft, label: "exchange", href: ROUTES.EXCHANGE },
  { icon: Users, label: "tontine", href: ROUTES.TONTINE },
  { icon: Vault, label: "vault", href: ROUTES.VAULT },
  { icon: Shield, label: "shield", href: ROUTES.SHIELD },
  { icon: History, label: "history", href: ROUTES.HISTORY },
];

const bottomItems = [
  { icon: CreditCard, label: "subscription", href: ROUTES.SUBSCRIPTION },
  { icon: Settings, label: "settings", href: ROUTES.SETTINGS },
  { icon: FileText, label: "docs", href: ROUTES.DOCS },
];

export function Sidebar() {
  const pathname = usePathname();
  const { sidebarCollapsed, toggleSidebar } = useUiStore();
  const { user, logout } = useAuth();

  // Always use FR logic
  const lang = "fr";
  const navCopy = COPY[lang].nav;

  // Render navigation links
  const renderLinks = (items: typeof navItems) => {
    return items.map((item) => {
      const isActive =
        pathname === item.href || pathname.startsWith(`${item.href}/`);
      return (
        <Link
          key={item.href}
          href={item.href}
          className={cn(
            "flex items-center gap-3 rounded-md px-3 py-2.5 text-sm font-medium transition-colors",
            isActive
              ? "bg-surface-3 text-gold border-l-2 border-gold"
              : "text-muted-foreground border-l-2 border-transparent hover:bg-surface-2 hover:text-foreground",
          )}
        >
          <item.icon className={cn("h-5 w-5", isActive ? "text-gold" : "")} />
          <AnimatePresence>
            {!sidebarCollapsed && (
              <motion.span
                initial={{ opacity: 0, width: 0 }}
                animate={{ opacity: 1, width: "auto" }}
                exit={{ opacity: 0, width: 0 }}
                className="overflow-hidden whitespace-nowrap"
              >
                {navCopy[item.label as keyof typeof navCopy]}
              </motion.span>
            )}
          </AnimatePresence>
        </Link>
      );
    });
  };

  return (
    <motion.aside
      animate={{ width: sidebarCollapsed ? 80 : 256 }}
      className="hidden flex-col border-r border-border bg-background lg:flex sticky top-0 h-screen"
    >
      <div className="flex h-16 items-center border-b border-border px-4 py-4">
        <Link href={ROUTES.HOME} className="flex items-center gap-2">
          <div className="h-8 w-8 shrink-0 rounded bg-gold p-1 flex items-center justify-center">
            <span className="font-display font-bold text-surface-2">SA</span>
          </div>
          <AnimatePresence>
            {!sidebarCollapsed && (
              <motion.span
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="font-display text-lg font-bold tracking-tight whitespace-nowrap"
              >
                ShadowAlpha
              </motion.span>
            )}
          </AnimatePresence>
        </Link>
      </div>

      <div className="flex-1 overflow-y-auto py-6 flex flex-col gap-6">
        <nav className="flex flex-col gap-1 px-3">{renderLinks(navItems)}</nav>
      </div>

      <div className="border-t border-border p-3 flex flex-col gap-1">
        <nav className="flex flex-col gap-1">{renderLinks(bottomItems)}</nav>

        {user && (
          <div className="mt-4 flex flex-col gap-2 rounded-lg bg-surface-2 p-3">
            <div className="flex items-center gap-3">
              <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-full bg-surface-3">
                <span className="text-xs font-medium text-foreground">
                  {user.displayName.substring(0, 2).toUpperCase()}
                </span>
              </div>
              {!sidebarCollapsed && (
                <div className="flex flex-col overflow-hidden">
                  <span className="truncate text-sm font-medium">
                    {user.displayName}
                  </span>
                  <span className="truncate text-xs text-muted-foreground">
                    {user.tier} Tier
                  </span>
                </div>
              )}
            </div>
            {!sidebarCollapsed && (
              <button
                onClick={logout}
                className="mt-2 flex w-full items-center justify-center gap-2 rounded-md bg-surface-3 py-1.5 text-xs font-medium text-muted-foreground hover:bg-danger/10 hover:text-danger"
              >
                <LogOut className="h-3 w-3" />
                Déconnexion
              </button>
            )}
          </div>
        )}
      </div>
    </motion.aside>
  );
}
