import { cn } from "@/lib/utils";

function Skeleton({
  className,
  ...props
}: React.HTMLAttributes<HTMLDivElement>) {
  return (
    <div
      className={cn(
        "animate-shimmer bg-[length:400%_100%] rounded-md bg-gradient-to-r from-surface-3 via-surface-2 to-surface-3",
        className,
      )}
      {...props}
    />
  );
}

export { Skeleton };
