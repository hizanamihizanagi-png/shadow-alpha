"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { motion } from "framer-motion";
import { CheckCircle2, ShieldAlert, Upload } from "lucide-react";

import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/use-auth";
import { ROUTES } from "@/lib/constants";

export default function KYCPage() {
  const router = useRouter();
  const { updateKycLevel } = useAuth();
  const [step, setStep] = useState<1 | 2 | 3>(1);
  const [isLoading, setIsLoading] = useState(false);

  const handleComplete = async () => {
    setIsLoading(true);

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1500));
      updateKycLevel(2);
      router.push(ROUTES.DASHBOARD);
    } catch (error) {
      console.error(error);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.4 }}
      className="glass-panel-heavy p-8 rounded-2xl border-2 border-gold/20"
    >
      <div className="flex flex-col items-center text-center mb-8">
        <div className="mb-4 inline-flex h-16 w-16 items-center justify-center rounded-full bg-surface-3 text-gold">
          <ShieldAlert className="h-8 w-8" />
        </div>
        <h1 className="text-2xl font-bold tracking-tight font-display text-white mb-2">
          Identity Verification
        </h1>
        <p className="text-sm text-muted-foreground max-w-sm">
          To comply with international regulations and ensure platform security,
          we require identity verification.
        </p>
      </div>

      <div className="mb-8 relative">
        <div className="absolute top-1/2 left-0 w-full h-1 bg-surface-3 -translate-y-1/2 z-0 rounded-full overflow-hidden">
          <motion.div
            className="h-full bg-gold"
            initial={{ width: "0%" }}
            animate={{
              width: step === 1 ? "33%" : step === 2 ? "66%" : "100%",
            }}
            transition={{ duration: 0.5 }}
          />
        </div>
        <div className="relative z-10 flex justify-between">
          {[1, 2, 3].map((i) => (
            <div
              key={i}
              className={`h-8 w-8 rounded-full flex items-center justify-center font-bold text-sm border-2 transition-colors duration-300 ${step >= i
                ? "bg-gold border-gold text-black"
                : "bg-surface-2 border-surface-3 text-muted-foreground"
                }`}
            >
              {step > i ? <CheckCircle2 className="h-4 w-4" /> : i}
            </div>
          ))}
        </div>
      </div>

      <div className="min-h-[200px]">
        {step === 1 && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h3 className="text-lg font-semibold mb-4">Personal Information</h3>
            <p className="text-sm text-muted-foreground mb-6">
              Enter your full legal name and residential address.
            </p>
            <div className="grid gap-4">
              {/* Fake inputs for visual flow */}
              <div className="h-10 bg-surface-3 rounded-md w-full border border-border"></div>
              <div className="h-10 bg-surface-3 rounded-md w-full border border-border"></div>
              <Button onClick={() => setStep(2)} className="mt-4">
                Continue
              </Button>
            </div>
          </motion.div>
        )}

        {step === 2 && (
          <motion.div
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
          >
            <h3 className="text-lg font-semibold mb-4">Document Upload</h3>
            <p className="text-sm text-muted-foreground mb-6">
              Please upload a valid government-issued ID.
            </p>

            <div className="border-2 border-dashed border-border hover:border-gold/50 transition-colors rounded-xl p-8 flex flex-col items-center justify-center mb-6 bg-surface-2 cursor-pointer">
              <Upload className="h-8 w-8 text-muted-foreground mb-3" />
              <p className="text-sm font-medium mb-1">
                Click to upload or drag and drop
              </p>
              <p className="text-xs text-muted-foreground">
                PNG, JPG or PDF (max. 10MB)
              </p>
            </div>

            <div className="flex gap-4">
              <Button
                variant="outline"
                onClick={() => setStep(1)}
                className="flex-1"
              >
                Back
              </Button>
              <Button onClick={() => setStep(3)} className="flex-1">
                Verify Document
              </Button>
            </div>
          </motion.div>
        )}

        {step === 3 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            className="flex flex-col items-center justify-center text-center py-6"
          >
            <CheckCircle2 className="h-16 w-16 text-success mb-4" />
            <h3 className="text-xl font-bold mb-2">Verification Complete</h3>
            <p className="text-sm text-muted-foreground mb-8">
              Your identity has been verified. You now have full access to
              ShadowAlpha trading features.
            </p>
            <Button
              onClick={handleComplete}
              isLoading={isLoading}
              size="lg"
              className="w-full"
            >
              Go to Dashboard
            </Button>
          </motion.div>
        )}
      </div>
    </motion.div>
  );
}
