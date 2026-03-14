"use client";

import { useMemo, useState, useEffect } from "react";
import {
  Area,
  AreaChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
  CartesianGrid,
} from "recharts";
import { formatCurrency, formatDate } from "@/lib/utils";
import { APP_CONFIG } from "@/lib/constants";

interface PortfolioDataPoint {
  date: string;
  value: number;
}

interface PortfolioChartProps {
  data?: PortfolioDataPoint[];
  isLoading?: boolean;
}

export function PortfolioChart({ data, isLoading }: PortfolioChartProps) {
  const [chartData, setChartData] = useState<PortfolioDataPoint[]>([]);

  // Generate mock data if none provided
  useEffect(() => {
    if (data && data.length > 0) {
      setChartData(data);
      return;
    }

    // Generate 30 days of realistic-looking portfolio data
    const mock = [];
    let startValue = 1000000; // Starting baseline
    const now = new Date();

    for (let i = 30; i >= 0; i--) {
      const date = new Date(now);
      date.setDate(date.getDate() - i);

      // Add some pseudo-random walk volatility
      // Using a deterministic approach based on date to avoid Math.random() in render loop
      const seed = date.getDate() * date.getMonth();
      const pseudoRandom = (seed % 100) / 100;
      const change = (pseudoRandom - 0.45) * 50000;
      startValue = Math.max(10000, startValue + change);

      mock.push({
        date: date.toISOString(),
        value: startValue,
      });
    }
    setChartData(mock);
  }, [data]);

  // Determine trend for gradient colors
  const isPositive = useMemo(() => {
    if (chartData.length < 2) return true;
    return chartData[chartData.length - 1].value >= chartData[0].value;
  }, [chartData]);

  if (isLoading) {
    return (
      <div className="flex h-[300px] w-full items-center justify-center bg-surface-2 animate-pulse rounded-lg border border-border">
        <div className="text-muted-foreground">Chargement des données...</div>
      </div>
    );
  }

  return (
    <div className="h-[300px] w-full">
      <ResponsiveContainer width="100%" height="100%">
        <AreaChart
          data={chartData}
          margin={{ top: 10, right: 0, left: 0, bottom: 0 }}
        >
          <defs>
            <linearGradient id="colorValue" x1="0" y1="0" x2="0" y2="1">
              <stop
                offset="5%"
                stopColor={
                  isPositive ? "var(--color-gold)" : "var(--color-red)"
                }
                stopOpacity={0.3}
              />
              <stop
                offset="95%"
                stopColor={
                  isPositive ? "var(--color-gold)" : "var(--color-red)"
                }
                stopOpacity={0}
              />
            </linearGradient>
          </defs>
          <CartesianGrid
            strokeDasharray="3 3"
            vertical={false}
            stroke="var(--color-border)"
            opacity={0.5}
          />
          <XAxis
            dataKey="date"
            tickFormatter={(date) => formatDate(date, "MMM dd")}
            stroke="var(--color-text-muted)"
            fontSize={12}
            tickLine={false}
            axisLine={false}
            dy={10}
            minTickGap={30}
          />
          <YAxis hide={true} domain={["auto", "auto"]} />
          <Tooltip
            content={({ active, payload, label }) => {
              if (active && payload && payload.length) {
                return (
                  <div className="glass-panel rounded-lg p-3 shadow-xl">
                    <p className="mb-1 text-xs text-muted-foreground">
                      {formatDate(label as string)}
                    </p>
                    <p className="font-mono text-base font-bold text-gold">
                      {formatCurrency(
                        payload[0].value as number,
                        APP_CONFIG.currency as "XAF" | "EUR" | "USD",
                      )}
                    </p>
                  </div>
                );
              }
              return null;
            }}
          />
          <Area
            type="monotone"
            dataKey="value"
            stroke={isPositive ? "var(--color-gold)" : "var(--color-red)"}
            strokeWidth={2}
            fillOpacity={1}
            fill="url(#colorValue)"
            animationDuration={1500}
          />
        </AreaChart>
      </ResponsiveContainer>
    </div>
  );
}
