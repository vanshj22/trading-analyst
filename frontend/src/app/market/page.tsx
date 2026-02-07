"use client";

import { useState } from "react";
import { useApp } from "@/lib/context";
import { analyzeMarket, MarketAnalysis } from "@/lib/api";
import { MetricCard } from "@/components/ui/metric-card";
import { NewsCard } from "@/components/ui/news-card";
import { TrendingUp, Activity, BarChart3, Search, Loader2, Lightbulb } from "lucide-react";

export default function MarketPage() {
  const { ticker } = useApp();
  const [analysis, setAnalysis] = useState<MarketAnalysis | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleAnalyze = async () => {
    setLoading(true);
    setError(null);
    try {
      const result = await analyzeMarket(ticker);
      setAnalysis(result);
    } catch {
      setError("Failed to analyze market. Is the API server running?");
    }
    setLoading(false);
  };

  return (
    <div className="container mx-auto px-6 py-10">
      {/* Hero Section */}
      <div className="mb-10">
        <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm text-primary">
          <Search className="h-4 w-4" />
          <span>Market Intelligence</span>
        </div>
        <h1 className="mt-4 text-4xl font-bold tracking-tight text-white md:text-5xl">
          Analyzing <span className="text-primary">{ticker}</span>
        </h1>
        <p className="mt-3 text-lg text-white/50">
          Real-time market intelligence with AI-powered insights and explanations.
        </p>
      </div>

      {error && (
        <div className="mb-8 glass-card border-red-500/30 bg-red-500/10 p-4">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      <div className="mb-8">
        <button
          onClick={handleAnalyze}
          disabled={loading}
          className="btn-primary flex items-center gap-2"
        >
          {loading ? (
            <Loader2 className="h-4 w-4 animate-spin" />
          ) : (
            <Search className="h-4 w-4" />
          )}
          Analyze Market
        </button>
      </div>

      {analysis && !analysis.error && (
        <div className="grid gap-8 lg:grid-cols-2">
          {/* Left Column - Technicals & Explanation */}
          <div className="space-y-8">
            {/* Technical Overview */}
            {analysis.technicals && !analysis.technicals.error && (
              <>
                <div>
                  <h2 className="mb-6 text-xl font-semibold text-white flex items-center gap-2">
                    <TrendingUp className="h-5 w-5 text-primary" />
                    Technical Overview
                  </h2>
                  <div className="grid gap-4 sm:grid-cols-3">
                    <MetricCard
                      title="Price"
                      value={`$${analysis.technicals.current_price?.toFixed(2) || "N/A"}`}
                      change={analysis.technicals.price_change_1d}
                      icon={TrendingUp}
                    />
                    <MetricCard
                      title="RSI"
                      value={analysis.technicals.rsi || "N/A"}
                      icon={Activity}
                    />
                    <MetricCard
                      title="Trend"
                      value={analysis.technicals.trend || "N/A"}
                      icon={BarChart3}
                    />
                  </div>
                </div>

                <div className="glass-card p-6">
                  <div className="flex items-center gap-4">
                    <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-blue-500/20">
                      <BarChart3 className="h-5 w-5 text-blue-400" />
                    </div>
                    <div>
                      <span className="text-white/60 text-sm">Support</span>
                      <p className="font-mono text-lg font-semibold text-white">
                        ${analysis.technicals.support?.toFixed(2) || "N/A"}
                      </p>
                    </div>
                    <div className="h-12 w-px bg-white/10" />
                    <div>
                      <span className="text-white/60 text-sm">Resistance</span>
                      <p className="font-mono text-lg font-semibold text-white">
                        ${analysis.technicals.resistance?.toFixed(2) || "N/A"}
                      </p>
                    </div>
                  </div>
                </div>
              </>
            )}

            {/* Why It Moved */}
            <div className="gradient-border glass-card overflow-hidden">
              <div className="p-6">
                <div className="flex items-center gap-3 mb-4">
                  <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/20">
                    <Lightbulb className="h-5 w-5 text-primary" />
                  </div>
                  <h2 className="text-xl font-semibold text-white">Why It Moved</h2>
                </div>
                <p className="text-white/80 leading-relaxed">
                  {analysis.explanation || "No explanation available"}
                </p>
              </div>
            </div>
          </div>

          {/* Right Column - News */}
          <div className="space-y-6">
            <h2 className="text-xl font-semibold text-white">📰 Recent News</h2>
            <NewsCard news={analysis.news || []} />
          </div>
        </div>
      )}

      {!analysis && (
        <div className="glass-card flex flex-col items-center justify-center p-16 text-center">
          <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-primary/10">
            <Search className="h-10 w-10 text-primary" />
          </div>
          <h3 className="text-xl font-semibold text-white">Ready to Analyze</h3>
          <p className="mt-2 text-white/50 max-w-sm">
            Click "Analyze Market" to get AI-powered insights, technical analysis, and news for {ticker}
          </p>
        </div>
      )}
    </div>
  );
}
