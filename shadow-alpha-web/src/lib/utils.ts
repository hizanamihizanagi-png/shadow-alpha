import { type ClassValue, clsx } from "clsx";
import { twMerge } from "tailwind-merge";
import { format } from "date-fns";
import { fr, enUS } from "date-fns/locale";

/**
 * Merge Tailwind classes safely
 */
export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

/**
 * Format currency amounts
 */
export function formatCurrency(
  amount: number,
  currency: "XAF" | "EUR" | "USD" = "XAF",
  locale: "fr-FR" | "en-US" = "fr-FR",
) {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency,
    maximumFractionDigits: currency === "XAF" ? 0 : 2,
  }).format(amount);
}

/**
 * Format PnL values with color indicators
 */
export function formatPnl(value: number, pct: number) {
  const isPositive = value >= 0;
  return {
    formatted: `${isPositive ? "+" : ""}${formatCurrency(value)} (${isPositive ? "+" : ""}${pct.toFixed(2)}%)`,
    sign: isPositive ? "+" : "-",
    colorClass: isPositive ? "text-success" : "text-danger",
  };
}

/**
 * Format dates
 */
export function formatDate(
  date: string | Date,
  formatStr: string = "dd MMM yyyy",
  localeStr: "fr" | "en" = "fr",
) {
  return format(typeof date === "string" ? new Date(date) : date, formatStr, {
    locale: localeStr === "fr" ? fr : enUS,
  });
}

/**
 * Safely truncate string
 */
export function truncate(str: string, maxLength: number) {
  if (!str || str.length <= maxLength) return str;
  return `${str.slice(0, maxLength)}...`;
}

/**
 * Get initials from a name
 */
export function getInitials(name: string) {
  if (!name) return "??";
  const parts = name.split(" ");
  if (parts.length >= 2) {
    return `${parts[0][0]}${parts[1][0]}`.toUpperCase();
  }
  return name.substring(0, 2).toUpperCase();
}
