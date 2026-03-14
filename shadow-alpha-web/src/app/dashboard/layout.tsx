"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import { Header } from "@/components/layout/header";
import { Sidebar } from "@/components/layout/sidebar";
import { useAuth } from "@/hooks/use-auth";
import { ROUTES } from "@/lib/constants";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const { isAuthenticated } = useAuth();
  const router = useRouter();
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  useEffect(() => {
    // Protect routes
    if (mounted && !isAuthenticated) {
      router.push(ROUTES.LOGIN);
    }
  }, [isAuthenticated, mounted, router]);

  if (!mounted || !isAuthenticated) {
    // Return empty while hydrating or checking auth to prevent hydration mismatch/flicker
    return (
      <div className="flex min-h-screen bg-background items-center justify-center">
        <div className="h-12 w-12 animate-pulse rounded-full bg-surface-3"></div>
      </div>
    );
  }

  return (
    <div className="flex min-h-screen bg-background flex-col lg:flex-row">
      <Sidebar />
      <div className="flex flex-1 flex-col overflow-hidden">
        <Header />
        <main className="flex-1 overflow-y-auto w-full p-4 sm:p-6 lg:p-8">
          <div className="mx-auto max-w-7xl">{children}</div>
        </main>
      </div>
    </div>
  );
}
