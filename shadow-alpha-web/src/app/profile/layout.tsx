import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Mon Profil | Shadow Alpha",
  description:
    "Gérez votre profil Shadow Alpha, consultez vos statistiques de trading et vos performances.",
};

export default function ProfileLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
