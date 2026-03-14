import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { ROUTES } from "@/lib/constants";
import Link from "next/link";
import { AreaChart, BrainCircuit, ShieldAlert, BarChart4, Users } from "lucide-react";

export default function LandingPage() {
  return (
    <div className="flex min-h-screen flex-col bg-background">
      {/* Navbar Minimal */}
      <header className="fixed top-0 z-50 w-full border-b border-white/5 bg-background/50 backdrop-blur-xl">
        <div className="container flex h-20 items-center justify-between">
          <div className="flex items-center gap-3">
            <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gold shadow-[0_0_20px_rgba(201,168,76,0.2)]">
              <span className="font-display text-xl font-bold text-black">
                SA
              </span>
            </div>
            <span className="font-display text-2xl font-bold tracking-tight text-white">
              ShadowAlpha
            </span>
          </div>
          <div className="flex items-center gap-4">
            <Button
              variant="ghost"
              asChild
              className="hidden sm:inline-flex text-muted-foreground hover:text-white"
            >
              <Link href={ROUTES.LOGIN}>Log In</Link>
            </Button>
            <Button
              asChild
              className="font-semibold shadow-[0_0_15px_rgba(201,168,76,0.3)] hover:shadow-[0_0_25px_rgba(201,168,76,0.5)] transition-shadow"
            >
              <Link href={ROUTES.SIGNUP}>Join the Alpha</Link>
            </Button>
          </div>
        </div>
      </header>

      <main className="flex-1">
        {/* Hero Section */}
        <section className="relative pt-32 pb-20 md:pt-48 md:pb-32 overflow-hidden">
          {/* Background Effects */}
          <div className="absolute inset-0 z-0 bg-background" />
          <div className="absolute left-1/2 top-0 z-0 h-[500px] w-[500px] -translate-x-1/2 bg-gold/10 blur-[120px] rounded-full" />
          <div className="absolute right-0 top-1/4 z-0 h-[400px] w-[400px] bg-accent/20 blur-[100px] rounded-full" />

          <div className="container relative z-10 text-center flex flex-col items-center">
            <div className="inline-flex items-center rounded-full border border-gold/30 bg-gold/10 px-3 py-1 text-sm font-medium text-gold mb-8 animate-fade-in">
              <span className="flex h-2 w-2 rounded-full bg-gold mr-2 animate-pulse-gold"></span>
              Private Beta is now live
            </div>

            <h1 className="font-display text-5xl md:text-7xl lg:text-8xl font-black tracking-tight text-white max-w-5xl mx-auto leading-[1.1] animate-fade-up">
              Quantitative Intelligence for{" "}
              <span className="text-gold">Peer-to-Peer</span> Markets
            </h1>

            <p
              className="mt-8 text-lg md:text-xl text-muted-foreground max-w-2xl mx-auto font-body animate-fade-up"
              style={{ animationDelay: "100ms" }}
            >
              Institutional-grade order books, algorithmic pricing models, and
              digital tontines engineered for maximum capital efficiency.
            </p>

            <div
              className="mt-12 flex flex-col sm:flex-row gap-4 justify-center animate-fade-up"
              style={{ animationDelay: "200ms" }}
            >
              <Button
                size="lg"
                asChild
                className="text-base h-14 px-8 shadow-[0_0_20px_rgba(201,168,76,0.25)]"
              >
                <Link href={ROUTES.SIGNUP}>Claim Your Edge</Link>
              </Button>
              <Button
                size="lg"
                variant="outline"
                asChild
                className="text-base h-14 px-8 border-border hover:bg-surface-2 text-white hover:text-white"
              >
                <Link href={ROUTES.DOCS}>Explore the API</Link>
              </Button>
            </div>
          </div>
        </section>

        {/* Features Grid */}
        <section className="py-24 bg-surface-2/30 border-t border-border">
          <div className="container">
            <div className="text-center mb-16">
              <h2 className="font-display text-3xl md:text-4xl font-bold text-white mb-4">
                Infrastructure for the Elite
              </h2>
              <p className="text-muted-foreground max-w-2xl mx-auto">
                We abstracted the complexity of absolute return strategies into
                powerful components.
              </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[
                {
                  title: "Modified Black-Scholes Pricing",
                  desc: "Algorithmic fair value estimation for asymmetric risk events with dynamically calibrated volatility surfaces.",
                  icon: BarChart4,
                },
                {
                  title: "P2P Position Exchange",
                  desc: "A decentralized order book for trading risk exposures instantly with zero counterparty risk.",
                  icon: AreaChart,
                },
                {
                  title: "Digital Tontine Ledger",
                  desc: "Syndicate capital dynamically using rigorous mathematical schedules optimized for IRR.",
                  icon: Users,
                },
                {
                  title: "Kelly Criterion Advisor",
                  desc: "Mathematically optimal position sizing recommendations based on expected value models.",
                  icon: BrainCircuit,
                },
                {
                  title: "Institutional Security",
                  desc: "End-to-end encryption, multi-tier KYC, and real-time anomaly detection protecting assets.",
                  icon: ShieldAlert,
                },
              ].map((f, i) => (
                <Card
                  key={i}
                  className="bg-surface-2 border-border/50 hover:border-gold/30 transition-colors p-6"
                >
                  <div className="h-12 w-12 rounded-lg bg-surface-3 flex items-center justify-center mb-6 text-gold">
                    <f.icon className="h-6 w-6" />
                  </div>
                  <h3 className="font-display text-xl font-bold text-white mb-3">
                    {f.title}
                  </h3>
                  <p className="text-muted-foreground text-sm leading-relaxed">
                    {f.desc}
                  </p>
                </Card>
              ))}
            </div>
          </div>
        </section>
      </main>

      <footer className="border-t border-border bg-background py-12">
        <div className="container text-center text-sm text-muted-foreground flex flex-col items-center">
          <div className="flex h-8 w-8 items-center justify-center rounded bg-gold mb-6">
            <span className="font-display font-bold text-black text-xs">
              SA
            </span>
          </div>
          <p>© {new Date().getFullYear()} ShadowAlpha. All rights reserved.</p>
        </div>
      </footer>
    </div>
  );
}
