"use client";

import { motion } from "framer-motion";
import { Menu, Bell, Wallet } from "lucide-react";
import { useUiStore } from "@/stores/ui-store";
import { useAuth } from "@/hooks/use-auth";
import { usePortfolio } from "@/hooks/use-portfolio";
import { formatCurrency, getInitials } from "@/lib/utils";
import { APP_CONFIG } from "@/lib/constants";

export function Header() {
  const toggleSidebar = useUiStore((state) => state.toggleSidebar);
  const { user } = useAuth();
  const { data: portfolio } = usePortfolio();

  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      className="sticky top-0 z-40 flex h-16 w-full items-center justify-between border-b border-border bg-background/80 px-4 backdrop-blur-md sm:px-6"
    >
      <div className="flex items-center gap-4">
        <button
          onClick={toggleSidebar}
          className="rounded-md p-2 hover:bg-surface-2 focus:outline-none focus:ring-2 focus:ring-gold lg:hidden"
        >
          <Menu className="h-5 w-5 text-muted-foreground" />
        </button>
        <div className="hidden lg:flex items-center gap-2">
          <div className="h-8 w-8 bg-gold rounded-full flex items-center justify-center font-bold text-black">
            SA
          </div>
          <span className="font-display font-bold text-lg hidden sm:inline-block">
            ShadowAlpha
          </span>
        </div>
      </div>

      <div className="flex items-center gap-4">
        {/* Wallet Balance */}
        <div className="hidden items-center gap-2 rounded-full border border-border bg-surface-2 px-4 py-1.5 sm:flex">
          <Wallet className="h-4 w-4 text-gold" />
          <span className="font-mono text-sm font-medium">
            {portfolio?.data
              ? formatCurrency(
                  portfolio.data.availableMargin,
                  APP_CONFIG.currency as any,
                )
              : "---"}
          </span>
        </div>

        {/* Notifications */}
        <button className="relative rounded-full p-2 hover:bg-surface-2 focus:outline-none focus:ring-2 focus:ring-gold">
          <Bell className="h-5 w-5 text-muted-foreground hover:text-foreground" />
          <span className="absolute right-1.5 top-1.5 flex h-2 w-2">
            <span className="absolute inline-flex h-full w-full animate-ping rounded-full bg-gold opacity-75"></span>
            <span className="relative inline-flex h-2 w-2 rounded-full bg-gold"></span>
          </span>
        </button>

        {/* User Avatar */}
        <div className="flex h-8 w-8 items-center justify-center rounded-full bg-surface-3 border border-border cursor-pointer hover:border-gold transition-colors">
          <span className="text-xs font-medium text-foreground">
            {user ? getInitials(user.displayName) : "G"}
          </span>
        </div>
      </div>
    </motion.header>
  );
}
