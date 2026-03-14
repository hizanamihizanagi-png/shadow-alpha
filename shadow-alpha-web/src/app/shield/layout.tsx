import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Shadow Shield | Shadow Alpha",
  description:
    "Protégez vos positions avec l'assurance actuarielle Shadow Shield. Récupérez jusqu'à 80% de votre mise en cas de perte.",
};

export default function ShieldLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
