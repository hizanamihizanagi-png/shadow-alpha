import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Abonnements | Shadow Alpha",
  description:
    "Choisissez votre plan Shadow Alpha : Free, Alpha, Premier ou Black Card. Accédez à la puissance quantitative complète.",
};

export default function SubscriptionLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
