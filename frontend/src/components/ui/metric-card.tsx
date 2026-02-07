import { cn } from "@/lib/utils";
import { LucideIcon } from "lucide-react";

interface MetricCardProps {
  title: string;
  value: string | number;
  change?: number;
  icon?: LucideIcon;
  className?: string;
}

export function MetricCard({
  title,
  value,
  change,
  icon: Icon,
  className,
}: MetricCardProps) {
  const isPositive = change !== undefined && change >= 0;

  return (
    <div
      className={cn(
        "glass-card group p-6 transition-all duration-300 hover:-translate-y-1",
        className
      )}
    >
      <div className="flex items-center justify-between">
        <span className="text-sm font-medium text-white/50">{title}</span>
        {Icon && (
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/10 transition-colors group-hover:bg-primary/20">
            <Icon className="h-5 w-5 text-primary" />
          </div>
        )}
      </div>
      <div className="mt-4">
        <span className="text-4xl font-bold tracking-tight text-white">{value}</span>
        {change !== undefined && (
          <span
            className={cn(
              "ml-3 inline-flex items-center rounded-lg px-2 py-1 text-sm font-medium",
              isPositive
                ? "bg-emerald-500/10 text-emerald-400"
                : "bg-red-500/10 text-red-400"
            )}
          >
            {isPositive ? "↑" : "↓"} {Math.abs(change).toFixed(2)}%
          </span>
        )}
      </div>
    </div>
  );
}
