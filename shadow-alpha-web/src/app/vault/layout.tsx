import type { Metadata } from "next";

export const metadata: Metadata = {
  title: "Shadow Vault | Shadow Alpha",
  description:
    "Déposez vos capitaux dans le Shadow Vault et générez du rendement automatique grâce au moteur quantitatif Shadow Alpha.",
};

export default function VaultLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return children;
}
