import * as React from "react";
import { cva, type VariantProps } from "class-variance-authority";

import { cn } from "@/lib/utils";

const badgeVariants = cva(
  "inline-flex items-center rounded-sm border px-2.5 py-0.5 text-xs font-semibold transition-colors focus:outline-none focus:ring-2 focus:ring-ring focus:ring-offset-2",
  {
    variants: {
      variant: {
        default:
          "border-transparent bg-gold text-surface-2 hover:bg-gold-muted",
        secondary:
          "border-transparent bg-surface-3 text-foreground hover:bg-surface-3/80",
        destructive:
          "border-transparent bg-danger text-danger-foreground hover:bg-danger/80",
        outline: "text-foreground border-border",
        success:
          "border-transparent bg-success/20 text-success hover:bg-success/30",
        danger_outline: "border-danger/50 text-danger bg-danger/10",
      },
    },
    defaultVariants: {
      variant: "default",
    },
  },
);

export interface BadgeProps
  extends
    React.HTMLAttributes<HTMLDivElement>,
    VariantProps<typeof badgeVariants> {}

function Badge({ className, variant, ...props }: BadgeProps) {
  return (
    <div className={cn(badgeVariants({ variant }), className)} {...props} />
  );
}

export { Badge, badgeVariants };
