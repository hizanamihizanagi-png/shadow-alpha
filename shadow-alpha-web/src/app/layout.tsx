import type { Metadata } from "next";
import { Syne, DM_Sans, JetBrains_Mono } from "next/font/google";
import "./globals.css";
import { Providers } from "@/components/layout/providers";

const fontSyne = Syne({
  subsets: ["latin"],
  variable: "--font-syne",
  display: "swap",
});

const fontDmSans = DM_Sans({
  subsets: ["latin"],
  variable: "--font-dm-sans",
  display: "swap",
});

const fontJetbrainsMono = JetBrains_Mono({
  subsets: ["latin"],
  variable: "--font-jetbrains-mono",
  display: "swap",
});

export const metadata: Metadata = {
  title: "Shadow Alpha | AI-Powered Quantitative Trading Intelligence",
  description:
    "Institutional P2P position exchange and digital tontine platform.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark" suppressHydrationWarning>
      <body
        className={`${fontSyne.variable} ${fontDmSans.variable} ${fontJetbrainsMono.variable} font-body bg-background text-foreground antialiased selection:bg-gold/30 selection:text-text`}
      >
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
