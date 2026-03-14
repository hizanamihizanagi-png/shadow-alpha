import { useAuthStore } from "@/stores/auth-store";

// A simple wrapper around useAuthStore for convenience
export function useAuth() {
  const {
    user,
    token,
    isAuthenticated,
    logout,
    setUser,
    setToken,
    updateKycLevel,
  } = useAuthStore();

  return {
    user,
    token,
    isAuthenticated,
    logout,
    setUser,
    setToken,
    updateKycLevel,
  };
}
