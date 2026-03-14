import { create } from "zustand";
import { persist } from "zustand/middleware";

interface UiState {
  sidebarCollapsed: boolean;
  theme: "dark" | "light";
  toggleSidebar: () => void;
  setTheme: (theme: "dark" | "light") => void;
}

export const useUiStore = create<UiState>()(
  persist(
    (set) => ({
      sidebarCollapsed: false,
      theme: "dark", // Dark mode first
      toggleSidebar: () =>
        set((state) => ({ sidebarCollapsed: !state.sidebarCollapsed })),
      setTheme: (theme) => {
        if (typeof document !== "undefined") {
          if (theme === "dark") {
            document.documentElement.classList.add("dark");
          } else {
            document.documentElement.classList.remove("dark");
          }
        }
        set({ theme });
      },
    }),
    {
      name: "sap-ui-storage",
    },
  ),
);
