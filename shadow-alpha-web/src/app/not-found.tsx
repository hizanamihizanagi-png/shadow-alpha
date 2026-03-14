"use client";

import Link from "next/link";
import { Ghost } from "lucide-react";
import { Button } from "@/components/ui/button";

export default function NotFound() {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen bg-background p-8 text-center">
      <div className="h-24 w-24 rounded-full bg-gold/10 flex items-center justify-center mb-6">
        <Ghost className="h-12 w-12 text-gold" />
      </div>
      <h1 className="text-5xl font-display font-bold text-white mb-2">404</h1>
      <h2 className="text-xl font-display text-muted-foreground mb-6">
        Page introuvable
      </h2>
      <p className="text-sm text-muted-foreground max-w-md mb-8">
        La page que vous cherchez n&apos;existe pas ou a été déplacée. Vérifiez
        l&apos;URL ou retournez au tableau de bord.
      </p>
      <Link href="/dashboard">
        <Button variant="default">Retour au Dashboard</Button>
      </Link>
    </div>
  );
}
