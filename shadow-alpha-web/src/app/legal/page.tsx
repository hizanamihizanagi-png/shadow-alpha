"use client";

import { useEffect, useState } from "react";
import { Scale, ShieldCheck, Vault } from "lucide-react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";

const legalDocs = [
  {
    title: "Conditions Générales d'Utilisation",
    icon: Scale,
    file: "/legal/terms-of-service.md",
  },
  {
    title: "Politique de Confidentialité",
    icon: ShieldCheck,
    file: "/legal/privacy-policy.md",
  },
  {
    title: "Conditions Vault, Shield & Prêts",
    icon: Vault,
    file: "/legal/vault-shield-terms.md",
  },
];

export default function LegalPage() {
  const [activeDoc, setActiveDoc] = useState(0);
  const [content, setContent] = useState("");

  useEffect(() => {
    fetch(legalDocs[activeDoc].file)
      .then((r) => r.text())
      .then((t) => setContent(t));
  }, [activeDoc]);

  return (
    <div className="flex flex-col gap-6 pb-10">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-display font-bold tracking-tight text-white">
          Documents Légaux
        </h1>
        <p className="text-muted-foreground">
          Conditions d&apos;utilisation et politiques de Shadow Alpha.
        </p>
      </div>

      {/* Document Tabs */}
      <div className="flex gap-3 flex-wrap">
        {legalDocs.map((doc, i) => (
          <button
            key={doc.file}
            onClick={() => setActiveDoc(i)}
            className={`flex items-center gap-2 px-4 py-2.5 rounded-lg text-sm font-medium transition-all ${
              i === activeDoc
                ? "bg-gold/20 text-gold border border-gold/30"
                : "bg-surface-2 text-muted-foreground border border-border hover:bg-surface-3 hover:text-white"
            }`}
          >
            <doc.icon className="h-4 w-4" />
            {doc.title}
          </button>
        ))}
      </div>

      {/* Document Content */}
      <Card className="glass-panel">
        <CardContent className="p-8">
          <div className="prose prose-invert prose-sm max-w-none prose-headings:font-display prose-h1:text-2xl prose-h2:text-lg prose-h3:text-base prose-p:text-muted-foreground prose-li:text-muted-foreground prose-strong:text-white prose-hr:border-border">
            {content.split("\n").map((line, i) => {
              if (line.startsWith("# "))
                return (
                  <h1 key={i} className="text-2xl font-display font-bold text-white mb-4">
                    {line.replace("# ", "")}
                  </h1>
                );
              if (line.startsWith("## "))
                return (
                  <h2 key={i} className="text-lg font-display font-semibold text-white mt-6 mb-2">
                    {line.replace("## ", "")}
                  </h2>
                );
              if (line.startsWith("### "))
                return (
                  <h3 key={i} className="text-base font-semibold text-gold mt-4 mb-1">
                    {line.replace("### ", "")}
                  </h3>
                );
              if (line.startsWith("- "))
                return (
                  <li key={i} className="text-sm text-muted-foreground ml-4 list-disc">
                    {line.replace("- ", "")}
                  </li>
                );
              if (line.startsWith("---"))
                return <hr key={i} className="border-border my-6" />;
              if (line.startsWith("**") && line.endsWith("**"))
                return (
                  <p key={i} className="text-sm font-semibold text-white mt-2">
                    {line.replace(/\*\*/g, "")}
                  </p>
                );
              if (line.trim() === "") return <div key={i} className="h-2" />;
              return (
                <p key={i} className="text-sm text-muted-foreground leading-relaxed">
                  {line}
                </p>
              );
            })}
          </div>
        </CardContent>
      </Card>
    </div>
  );
}
