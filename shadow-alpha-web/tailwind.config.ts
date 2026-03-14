import type { Config } from "tailwindcss";

const config = {
    darkMode: ["class"],
    content: [
        './pages/**/*.{ts,tsx}',
        './components/**/*.{ts,tsx}',
        './app/**/*.{ts,tsx}',
        './src/**/*.{ts,tsx}',
    ],
    prefix: "",
    theme: {
        container: {
            center: true,
            padding: "2rem",
            screens: {
                "2xl": "1400px",
            },
        },
        extend: {
            fontFamily: {
                display: ["var(--font-syne)"],
                body: ["var(--font-dm-sans)"],
                mono: ["var(--font-jetbrains-mono)"],
            },
            colors: {
                border: "var(--color-border)",
                input: "var(--color-border)",
                ring: "var(--color-gold)",
                background: "var(--color-surface)",
                foreground: "var(--color-text)",
                gold: {
                    DEFAULT: "var(--color-gold)",
                    muted: "var(--color-gold-muted)",
                },
                surface: {
                    DEFAULT: "var(--color-surface)",
                    2: "var(--color-surface-2)",
                    3: "var(--color-surface-3)",
                },
                success: {
                    DEFAULT: "var(--color-green)",
                    foreground: "var(--color-surface)",
                },
                danger: {
                    DEFAULT: "var(--color-red)",
                    foreground: "var(--color-text)",
                },
                info: {
                    DEFAULT: "var(--color-blue)",
                    foreground: "var(--color-text)",
                },
                muted: {
                    DEFAULT: "var(--color-surface-2)",
                    foreground: "var(--color-text-muted)",
                },
                accent: {
                    DEFAULT: "var(--color-surface-3)",
                    foreground: "var(--color-gold)",
                },
            },
            borderRadius: {
                lg: "var(--radius-lg)",
                md: "var(--radius-md)",
                sm: "var(--radius-sm)",
            },
            keyframes: {
                "fade-up": {
                    "0%": { transform: "translateY(16px)", opacity: "0" },
                    "100%": { transform: "translateY(0)", opacity: "1" },
                },
                "fade-in": {
                    "0%": { opacity: "0" },
                    "100%": { opacity: "1" },
                },
                "shimmer": {
                    "0%": { backgroundPosition: "-1000px 0" },
                    "100%": { backgroundPosition: "1000px 0" },
                },
                "pulse-gold": {
                    "0%, 100%": { opacity: "1", boxShadow: "0 0 0 0 rgba(201, 168, 76, 0.4)" },
                    "50%": { opacity: ".8", boxShadow: "0 0 0 4px rgba(201, 168, 76, 0)" },
                },
            },
            animation: {
                "fade-up": "fade-up 400ms ease-out",
                "fade-in": "fade-in 300ms ease-out",
                "shimmer": "shimmer 1.5s infinite linear",
                "pulse-gold": "pulse-gold 2s infinite ease-in-out",
            },
        },
    },
    plugins: [],
} satisfies Config;

export default config;
