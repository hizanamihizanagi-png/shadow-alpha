"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { motion } from "framer-motion";

import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { useAuth } from "@/hooks/use-auth";
import { ROUTES } from "@/lib/constants";

export default function SignupPage() {
  const router = useRouter();
  const { setUser, setToken } = useAuth();
  const [isLoading, setIsLoading] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [name, setName] = useState("");

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setIsLoading(true);

    try {
      const { apiClient } = await import("@/lib/api-client");
      
      // 1. Register with backend
      await apiClient.post("/auth/register", {
        email,
        password,
        display_name: name || "New User",
        phone: null,
      });

      // 2. Auto-login after registration
      const tokenResponse = await apiClient.post<any>("/auth/login", { 
        email, 
        password 
      });
      
      const accessToken = (tokenResponse as any).access_token || (tokenResponse as any).data?.access_token;
      
      if (!accessToken) throw new Error("Registration succeeded but login failed");
      
      // 3. Set token
      setToken(accessToken);
      await new Promise(resolve => setTimeout(resolve, 50));
      
      // 4. Fetch user profile
      const meResponse = await apiClient.get<any>("/auth/me");
      const user = (meResponse as any).data || meResponse;
      
      setUser({ 
        id: user.id || "1", 
        email: user.email, 
        displayName: user.display_name || user.email.split("@")[0], 
        tier: user.tier || "ALPHA", 
        kycLevel: user.kyc_level || 0 
      });

      // Route to KYC on successful signup
      router.push(ROUTES.KYC);
    } catch (error) {
      console.error("Signup error:", error);
      alert("Registration failed. Email might already be in use.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
    >
      <div className="flex flex-col space-y-2 text-center lg:text-left mb-8">
        <h1 className="text-2xl font-semibold tracking-tight font-display text-white">
          Create an account
        </h1>
        <p className="text-sm text-muted-foreground">
          Enter your details below to create your account
        </p>
      </div>

      <div className="grid gap-6">
        <form onSubmit={handleSubmit}>
          <div className="grid gap-4">
            <div className="grid gap-2">
              <label
                htmlFor="name"
                className="text-sm font-medium leading-none text-foreground"
              >
                Display Name
              </label>
              <Input
                id="name"
                placeholder="Satoshi"
                disabled={isLoading}
                value={name}
                onChange={(e) => setName(e.target.value)}
                required
              />
            </div>
            <div className="grid gap-2">
              <label
                htmlFor="email"
                className="text-sm font-medium leading-none text-foreground"
              >
                Email
              </label>
              <Input
                id="email"
                placeholder="name@example.com"
                type="email"
                autoCapitalize="none"
                autoComplete="email"
                autoCorrect="off"
                disabled={isLoading}
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                required
              />
            </div>
            <div className="grid gap-2">
              <label
                htmlFor="password"
                className="text-sm font-medium leading-none text-foreground"
              >
                Password
              </label>
              <Input
                id="password"
                type="password"
                disabled={isLoading}
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                minLength={8}
              />
            </div>
            <Button disabled={isLoading} className="mt-2 w-full font-semibold">
              {isLoading && (
                <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              )}
              Sign Up
            </Button>
          </div>
        </form>

        <div className="relative">
          <div className="absolute inset-0 flex items-center">
            <span className="w-full border-t border-border" />
          </div>
          <div className="relative flex justify-center text-xs uppercase">
            <span className="bg-background px-2 text-muted-foreground">
              Or continue with
            </span>
          </div>
        </div>

        <div className="grid grid-cols-2 gap-4">
          <Button variant="outline" disabled={isLoading}>
            Google
          </Button>
          <Button variant="outline" disabled={isLoading}>
            Apple
          </Button>
        </div>
      </div>

      <p className="mt-8 text-center text-sm">
        Already have an account?{" "}
        <Link
          href={ROUTES.LOGIN}
          className="font-medium text-gold hover:underline"
        >
          Sign in
        </Link>
      </p>
    </motion.div>
  );
}
