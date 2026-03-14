import { Shield } from "lucide-react";

export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen bg-background">
      {/* Left side: branding/art */}
      <div className="hidden lg:flex lg:w-1/2 relative bg-surface-2 flex-col justify-between p-12 border-r border-border overflow-hidden">
        <div className="absolute inset-0 z-0">
          {/* Abstract mathematical background */}
          <div
            className="absolute inset-0 opacity-[0.03]"
            style={{
              backgroundImage:
                "radial-gradient(circle at 2px 2px, white 1px, transparent 0)",
              backgroundSize: "40px 40px",
            }}
          ></div>
          <div className="absolute bottom-0 left-0 w-full h-[60%] bg-gradient-to-t from-gold/10 to-transparent"></div>
        </div>

        <div className="relative z-10 flex items-center gap-3">
          <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-gold shadow-[0_0_15px_rgba(201,168,76,0.3)]">
            <span className="font-display text-xl font-bold text-black">
              SA
            </span>
          </div>
          <span className="font-display text-2xl font-bold tracking-tight text-white">
            ShadowAlpha
          </span>
        </div>

        <div className="relative z-10 max-w-lg mb-12">
          <div className="mb-6 inline-flex h-12 w-12 items-center justify-center rounded-xl bg-surface-3 text-gold">
            <Shield className="h-6 w-6" />
          </div>
          <h2 className="font-display text-4xl font-bold text-white leading-tight mb-4">
            Institutional intelligence, now accessible.
          </h2>
          <p className="text-lg text-muted-foreground">
            Join the apex of quantitative peer-to-peer markets. Log in to access
            your portfolio, order book, and models.
          </p>
        </div>
      </div>

      {/* Right side: form */}
      <div className="flex w-full flex-col justify-center px-4 py-12 sm:px-6 lg:w-1/2 lg:px-20 xl:px-24">
        <div className="mx-auto w-full max-w-md">{children}</div>
      </div>
    </div>
  );
}
