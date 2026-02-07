"use client";

import { cn } from "@/lib/utils";

interface InterventionAlertProps {
  type: "HARD_LOCK" | "CRITICAL" | "SOFT_NUDGE" | "NONE";
  title: string;
  message: string;
}

export function InterventionAlert({ type, title, message }: InterventionAlertProps) {
  if (type === "NONE") {
    return (
      <div className="rounded-xl border border-green-500/30 bg-green-500/10 p-6">
        <div className="flex items-center gap-3">
          <span className="text-2xl">✅</span>
          <div>
            <h3 className="font-semibold text-green-400">All Clear</h3>
            <p className="text-sm text-green-400/70">
              No intervention needed - trader state is healthy
            </p>
          </div>
        </div>
      </div>
    );
  }

  const styles = {
    HARD_LOCK: {
      bg: "bg-red-500/20",
      border: "border-red-500/50",
      icon: "🚨",
      titleColor: "text-red-400",
      textColor: "text-red-300",
    },
    CRITICAL: {
      bg: "bg-orange-500/20",
      border: "border-orange-500/50",
      icon: "⚠️",
      titleColor: "text-orange-400",
      textColor: "text-orange-300",
    },
    SOFT_NUDGE: {
      bg: "bg-yellow-500/20",
      border: "border-yellow-500/50",
      icon: "💡",
      titleColor: "text-yellow-400",
      textColor: "text-yellow-300",
    },
  };

  const style = styles[type as keyof typeof styles] || styles.CRITICAL;

  return (
    <div
      className={cn(
        "rounded-xl border p-6",
        style.bg,
        style.border
      )}
    >
      <div className="flex items-start gap-4">
        <span className="text-3xl">{style.icon}</span>
        <div>
          <h3 className={cn("text-lg font-bold", style.titleColor)}>
            {title}
          </h3>
          <p className={cn("mt-2", style.textColor)}>{message}</p>
          {type === "HARD_LOCK" && (
            <p className={cn("mt-2 text-sm font-medium", style.textColor)}>
              Action: Trading locked for 5 minutes
            </p>
          )}
        </div>
      </div>
    </div>
  );
}
