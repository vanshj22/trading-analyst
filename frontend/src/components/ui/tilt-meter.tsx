"use client";

import { cn } from "@/lib/utils";

interface TiltMeterProps {
  score: number; // 0-10
  analysis?: string;
}

export function TiltMeter({ score, analysis }: TiltMeterProps) {
  const percentage = (score / 10) * 100;
  
  const getColor = () => {
    if (score <= 3) return "bg-green-500";
    if (score <= 6) return "bg-yellow-500";
    return "bg-red-500";
  };

  const getLabel = () => {
    if (score <= 3) return "Calm";
    if (score <= 6) return "Elevated";
    return "Critical";
  };

  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-6">
      <div className="flex items-center justify-between">
        <h3 className="text-sm font-medium text-white/60">Tilt Score</h3>
        <span
          className={cn(
            "rounded-full px-2 py-1 text-xs font-medium",
            score <= 3
              ? "bg-green-500/20 text-green-400"
              : score <= 6
              ? "bg-yellow-500/20 text-yellow-400"
              : "bg-red-500/20 text-red-400"
          )}
        >
          {getLabel()}
        </span>
      </div>

      <div className="mt-4 flex items-center gap-4">
        <span className="text-4xl font-bold text-white">{score}</span>
        <span className="text-lg text-white/40">/10</span>
      </div>

      <div className="mt-4 h-3 overflow-hidden rounded-full bg-white/10">
        <div
          className={cn("h-full rounded-full transition-all duration-500", getColor())}
          style={{ width: `${percentage}%` }}
        />
      </div>

      {analysis && (
        <p className="mt-4 text-sm text-white/70">{analysis}</p>
      )}
    </div>
  );
}
