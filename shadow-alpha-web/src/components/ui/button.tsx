import * as React from "react";
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";
import { motion, HTMLMotionProps } from "framer-motion";

import { cn } from "@/lib/utils";

const buttonVariants = cva(
  "inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50",
  {
    variants: {
      variant: {
        default: "bg-gold text-surface-2 hover:bg-gold-muted",
        destructive: "bg-danger text-danger-foreground hover:bg-danger/90",
        outline: "border border-gold text-gold bg-transparent hover:bg-gold/10",
        secondary:
          "bg-surface-3 text-foreground hover:bg-surface-3/80 border border-border",
        ghost: "hover:bg-surface-3 hover:text-foreground",
        link: "text-info underline-offset-4 hover:underline",
        success: "bg-success text-success-foreground hover:bg-success/90",
      },
      size: {
        default: "h-10 px-4 py-2",
        sm: "h-9 rounded-md px-3",
        lg: "h-11 rounded-md px-8 font-semibold",
        icon: "h-10 w-10",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

export interface ButtonProps
  extends
    React.ButtonHTMLAttributes<HTMLButtonElement>,
    VariantProps<typeof buttonVariants> {
  asChild?: boolean;
  isLoading?: boolean;
}

const Button = React.forwardRef<HTMLButtonElement, ButtonProps>(
  (
    {
      className,
      variant,
      size,
      asChild = false,
      isLoading = false,
      children,
      ...props
    },
    ref,
  ) => {
    // Fallback to standard button if asChild is true or we want motion
    if (asChild) {
      return (
        <Slot
          className={cn(buttonVariants({ variant, size, className }))}
          ref={ref}
          {...(props as React.ButtonHTMLAttributes<HTMLButtonElement>)}
        >
          {children}
        </Slot>
      );
    }

    // Motion component
    const MotionButton = motion.button;

    return (
      <MotionButton
        className={cn(buttonVariants({ variant, size, className }))}
        ref={ref as any}
        whileTap={{ scale: 0.98 }}
        disabled={isLoading || props.disabled}
        {...(props as HTMLMotionProps<"button">)}
      >
        {isLoading ? (
          <div className="mr-2 h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
        ) : null}
        {children}
      </MotionButton>
    );
  },
);
Button.displayName = "Button";

export { Button, buttonVariants };
