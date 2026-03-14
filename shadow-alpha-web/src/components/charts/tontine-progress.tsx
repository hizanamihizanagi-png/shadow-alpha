"use client";

import { RadialBarChart, RadialBar, ResponsiveContainer } from "recharts";

interface TontineProgressProps {
  currentCycle: number;
  totalCycles: number;
  size?: number;
}

export function TontineProgress({
  currentCycle,
  totalCycles,
  size = 120,
}: TontineProgressProps) {
  const percentage = Math.round((currentCycle / totalCycles) * 100);

  const data = [
    {
      name: "Background",
      value: 100,
      fill: "var(--color-surface-3)",
    },
    {
      name: "Progress",
      value: percentage,
      fill: "var(--color-gold)",
    },
  ];

  return (
    <div
      className="relative flex items-center justify-center"
      style={{ width: size, height: size }}
    >
      <div className="absolute flex flex-col items-center justify-center">
        <span className="font-display text-xl font-bold text-foreground">
          {percentage}%
        </span>
        <span className="text-xs text-muted-foreground">
          {currentCycle}/{totalCycles}
        </span>
      </div>
      <ResponsiveContainer width="100%" height="100%">
        <RadialBarChart
          cx="50%"
          cy="50%"
          innerRadius="75%"
          outerRadius="90%"
          barSize={8}
          data={data}
          startAngle={90}
          endAngle={-270}
        >
          <RadialBar
            background={false}
            dataKey="value"
            cornerRadius={10}
            // Add animation support to recharts radial bar
            animationDuration={1000}
          />
        </RadialBarChart>
      </ResponsiveContainer>
    </div>
  );
}
