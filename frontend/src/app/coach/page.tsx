"use client";

import { useState } from "react";
import { useApp } from "@/lib/context";
import { analyzeBehavioral, FullAnalysisResult } from "@/lib/api";
import { TiltMeter } from "@/components/ui/tilt-meter";
import { InterventionAlert } from "@/components/ui/intervention-alert";
import { Brain, Play, Loader2, AlertTriangle, Eye, Lightbulb, Target } from "lucide-react";
import { cn } from "@/lib/utils";
import Link from "next/link";

const USER_ACTIONS = [
  { value: "", label: "No Action", icon: "⬜" },
  { value: "place_order", label: "Place Order", icon: "📈" },
  { value: "cancel_order", label: "Cancel Order", icon: "❌" },
  { value: "modify_order", label: "Modify Order", icon: "✏️" },
  { value: "check_position", label: "Check Position", icon: "👁️" },
];

export default function CoachPage() {
  const { ticker, initialized } = useApp();
  const [userAction, setUserAction] = useState("");
  const [result, setResult] = useState<FullAnalysisResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await analyzeBehavioral(ticker, userAction || undefined);
      setResult(res);
    } catch {
      setError("Failed to run analysis. Make sure the system is initialized.");
    }
    setLoading(false);
  };

  if (!initialized) {
    return (
      <div className="container mx-auto px-6 py-10">
        <div className="mb-10">
          <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm text-primary">
            <Brain className="h-4 w-4" />
            <span>Behavioral Coach</span>
          </div>
          <h1 className="mt-4 text-4xl font-bold tracking-tight text-white md:text-5xl">
            Your AI <span className="text-primary">Coach</span>
          </h1>
        </div>

        <div className="glass-card border-amber-500/30 p-12 text-center max-w-lg mx-auto">
          <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-amber-500/20 mx-auto">
            <AlertTriangle className="h-10 w-10 text-amber-400" />
          </div>
          <h3 className="text-xl font-semibold text-white">System Not Initialized</h3>
          <p className="mt-3 text-white/50">
            Please initialize the behavioral analysis system first.
          </p>
          <Link
            href="/"
            className="mt-6 inline-flex btn-primary"
          >
            Go to Dashboard
          </Link>
        </div>
      </div>
    );
  }

  return (
    <div className="container mx-auto px-6 py-10">
      {/* Hero Section */}
      <div className="mb-10">
        <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm text-primary">
          <Brain className="h-4 w-4" />
          <span>Behavioral Coach</span>
        </div>
        <h1 className="mt-4 text-4xl font-bold tracking-tight text-white md:text-5xl">
          Your AI <span className="text-primary">Coach</span>
        </h1>
        <p className="mt-3 text-lg text-white/50">
          AI-powered trading psychology monitoring and personalized interventions.
        </p>
      </div>

      {error && (
        <div className="mb-8 glass-card border-red-500/30 bg-red-500/10 p-4">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      {/* Controls */}
      <div className="mb-10 glass-card p-6">
        <div className="flex flex-wrap items-center gap-4">
          <div className="flex items-center gap-3 rounded-xl bg-white/[0.03] border border-white/[0.08] px-5 py-3">
            <span className="text-sm text-white/60">Analyzing:</span>
            <span className="font-bold text-primary">{ticker}</span>
          </div>

          <select
            value={userAction}
            onChange={(e) => setUserAction(e.target.value)}
            className="rounded-xl border border-white/[0.08] bg-white/[0.03] px-5 py-3.5 text-white backdrop-blur-sm transition-all focus:border-primary/50 focus:outline-none"
          >
            {USER_ACTIONS.map((action) => (
              <option key={action.value} value={action.value} className="bg-[#1a1225]">
                {action.icon} {action.label}
              </option>
            ))}
          </select>

          <button
            onClick={handleAnalyze}
            disabled={loading}
            className="btn-primary flex items-center gap-2"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Play className="h-4 w-4" />
            )}
            Run Analysis
          </button>
        </div>
      </div>

      {result && (
        <div className="space-y-8">
          {/* Combined Insight */}
          {result.combined_insight && (
            <div className="gradient-border glass-card overflow-hidden">
              <div className="p-8">
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600">
                    <Lightbulb className="h-6 w-6 text-white" />
                  </div>
                  <h2 className="text-2xl font-bold text-white">Personalized Insight</h2>
                </div>
                <p className="text-lg text-white/80 leading-relaxed">
                  {result.combined_insight}
                </p>
              </div>
            </div>
          )}

          {result.behavioral_analysis && (
            <div className="grid gap-8 lg:grid-cols-2">
              {/* Left Column */}
              <div className="space-y-8">
                {/* Perception Layer */}
                <div className="glass-card p-6">
                  <div className="flex items-center gap-3 mb-6">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/20">
                      <Eye className="h-5 w-5 text-blue-400" />
                    </div>
                    <h2 className="text-lg font-semibold text-white">Perception Layer</h2>
                  </div>
                  <div className="grid gap-4 md:grid-cols-2">
                    <div className="rounded-xl bg-white/[0.02] border border-white/[0.05] p-4">
                      <h3 className="mb-3 text-sm font-medium text-white/60">Market State</h3>
                      <pre className="max-h-40 overflow-auto text-xs text-white/70 font-mono">
                        {JSON.stringify(result.behavioral_analysis.perception.market, null, 2)}
                      </pre>
                    </div>
                    <div className="rounded-xl bg-white/[0.02] border border-white/[0.05] p-4">
                      <h3 className="mb-3 text-sm font-medium text-white/60">User Behavior</h3>
                      <pre className="max-h-40 overflow-auto text-xs text-white/70 font-mono">
                        {JSON.stringify(result.behavioral_analysis.perception.user, null, 2)}
                      </pre>
                    </div>
                  </div>
                </div>

                {/* Cognitive Layer */}
                <div>
                  <div className="flex items-center gap-3 mb-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/20">
                      <Brain className="h-5 w-5 text-primary" />
                    </div>
                    <h2 className="text-lg font-semibold text-white">Cognitive Layer</h2>
                  </div>
                  <TiltMeter
                    score={result.behavioral_analysis.reasoning.tilt.tilt_score}
                    analysis={result.behavioral_analysis.reasoning.tilt.llm_analysis}
                  />
                </div>
              </div>

              {/* Right Column - Action Layer */}
              <div>
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-red-500/20">
                    <Target className="h-5 w-5 text-red-400" />
                  </div>
                  <h2 className="text-lg font-semibold text-white">Action Layer</h2>
                </div>
                <InterventionAlert
                  type={result.behavioral_analysis.intervention.type}
                  title={result.behavioral_analysis.intervention.ui?.title || result.behavioral_analysis.intervention.type}
                  message={result.behavioral_analysis.intervention.message}
                />
              </div>
            </div>
          )}
        </div>
      )}

      {!result && (
        <div className="glass-card flex flex-col items-center justify-center p-16 text-center">
          <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-primary/10">
            <Brain className="h-10 w-10 text-primary" />
          </div>
          <h3 className="text-xl font-semibold text-white">Ready to Analyze</h3>
          <p className="mt-2 text-white/50 max-w-sm">
            Select a user action and click 'Run Analysis' to see behavioral insights and interventions
          </p>
        </div>
      )}
    </div>
  );
}
