import { create } from "zustand";
import { persist } from "zustand/middleware";

interface User {
  id: string;
  email: string;
  displayName: string;
  tier: "FREE" | "ALPHA" | "PREMIER" | "BLACK_CARD";
  kycLevel: 0 | 1 | 2 | 3;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setUser: (user: User | null) => void;
  setToken: (token: string | null) => void;
  updateKycLevel: (level: 0 | 1 | 2 | 3) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      user: null,
      token: null,
      isAuthenticated: false,
      setUser: (user) => set({ user, isAuthenticated: !!user }),
      setToken: (token) => {
        if (typeof window !== "undefined") {
          if (token) localStorage.setItem("sap_token", token);
          else localStorage.removeItem("sap_token");
        }
        set({ token });
      },
      updateKycLevel: (level) =>
        set((state) => ({
          user: state.user ? { ...state.user, kycLevel: level } : null,
        })),
      logout: () => {
        if (typeof window !== "undefined") {
          localStorage.removeItem("sap_token");
        }
        set({ user: null, token: null, isAuthenticated: false });
      },
    }),
    {
      name: "sap-auth-storage",
    },
  ),
);
