"use client";

import { useState, useEffect } from "react";
import { Activity, TrendingUp, DollarSign, Loader2, Rocket, RefreshCw } from "lucide-react";
import { useApp } from "@/lib/context";
import { loadDemoTrades, getTrades, getTradeMetrics, initializeSystem, getTraderProfile, Trade, TradeMetrics } from "@/lib/api";
import { MetricCard } from "@/components/ui/metric-card";
import { TradeTable } from "@/components/ui/trade-table";

export default function DashboardPage() {
  const { initialized, setInitialized, hasTrades, setHasTrades } = useApp();
  const [trades, setTrades] = useState<Trade[]>([]);
  const [metrics, setMetrics] = useState<TradeMetrics>({ total_trades: 0, win_rate: 0, total_pnl: 0 });
  const [profile, setProfile] = useState<Record<string, unknown> | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadInitialData();
  }, []);

  const loadInitialData = async () => {
    try {
      const [tradesRes, metricsRes] = await Promise.all([
        getTrades(),
        getTradeMetrics()
      ]);
      setTrades(tradesRes.trades);
      setMetrics(metricsRes);
      setHasTrades(tradesRes.count > 0);
    } catch {
      console.log("API not ready yet");
    }
  };

  const handleLoadDemoTrades = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await loadDemoTrades();
      setTrades(res.trades);
      setHasTrades(true);
      const metricsRes = await getTradeMetrics();
      setMetrics(metricsRes);
    } catch {
      setError("Failed to load trades. Is the API server running?");
    }
    setLoading(false);
  };

  const handleInitialize = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await initializeSystem();
      setInitialized(true);
      setProfile(res.profile);
    } catch {
      setError("Failed to initialize. Make sure trades are loaded.");
    }
    setLoading(false);
  };

  const loadProfile = async () => {
    try {
      const prof = await getTraderProfile();
      setProfile(prof);
    } catch {
      // ignore
    }
  };

  useEffect(() => {
    if (initialized) loadProfile();
  }, [initialized]);

  return (
    <div className="container mx-auto px-6 py-10">
      {/* Hero Section */}
      <div className="mb-10">
        <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm text-primary">
          <Activity className="h-4 w-4" />
          <span>Trading Dashboard</span>
        </div>
        <h1 className="mt-4 text-4xl font-bold tracking-tight text-white md:text-5xl">
          Welcome back, <span className="text-primary">Trader</span>
        </h1>
        <p className="mt-3 text-lg text-white/50">
          Monitor your performance, analyze patterns, and make data-driven decisions.
        </p>
      </div>

      {error && (
        <div className="mb-8 glass-card border-red-500/30 bg-red-500/10 p-4">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Left Column - Trades */}
        <div className="lg:col-span-2 space-y-8">
          <div className="flex items-center justify-between">
            <h2 className="text-xl font-semibold text-white">Recent Trades</h2>
            <button
              onClick={handleLoadDemoTrades}
              disabled={loading}
              className="btn-primary flex items-center gap-2 text-sm"
            >
              {loading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <RefreshCw className="h-4 w-4" />
              )}
              Load Demo Trades
            </button>
          </div>

          <TradeTable trades={trades} />

          {/* Metrics */}
          <div className="grid gap-6 sm:grid-cols-3">
            <MetricCard
              title="Total Trades"
              value={metrics.total_trades}
              icon={Activity}
            />
            <MetricCard
              title="Win Rate"
              value={`${metrics.win_rate}%`}
              icon={TrendingUp}
            />
            <MetricCard
              title="Total P&L"
              value={`$${metrics.total_pnl.toFixed(2)}`}
              change={metrics.total_pnl}
              icon={DollarSign}
            />
          </div>
        </div>

        {/* Right Column - System Status */}
        <div className="space-y-6">
          <div className="glass-card p-6">
            <div className="flex items-center gap-3">
              <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600">
                <Rocket className="h-6 w-6 text-white" />
              </div>
              <div>
                <h2 className="text-lg font-semibold text-white">System Status</h2>
                <p className="text-sm text-white/50">Behavioral analysis engine</p>
              </div>
            </div>

            {!initialized && hasTrades && (
              <button
                onClick={handleInitialize}
                disabled={loading}
                className="mt-6 w-full btn-primary flex items-center justify-center gap-2"
              >
                {loading ? (
                  <Loader2 className="h-4 w-4 animate-spin" />
                ) : (
                  <Rocket className="h-4 w-4" />
                )}
                Initialize System
              </button>
            )}

            {!hasTrades && (
              <div className="mt-6 rounded-xl border border-dashed border-white/20 p-6 text-center">
                <p className="text-white/50">Load demo trades to begin</p>
              </div>
            )}

            {initialized && (
              <div className="mt-6 flex items-center gap-3 rounded-xl bg-emerald-500/10 p-4">
                <span className="flex h-3 w-3">
                  <span className="absolute inline-flex h-3 w-3 animate-ping rounded-full bg-emerald-400 opacity-75"></span>
                  <span className="relative inline-flex h-3 w-3 rounded-full bg-emerald-500"></span>
                </span>
                <span className="text-emerald-400 font-medium">System Active</span>
              </div>
            )}
          </div>

          {profile && (
            <div className="glass-card p-6">
              <h3 className="text-lg font-semibold text-white">👤 Trader Profile</h3>
              <div className="mt-4 max-h-64 overflow-auto rounded-xl bg-black/30 p-4">
                <pre className="text-xs text-white/60 font-mono">
                  {JSON.stringify(profile, null, 2)}
                </pre>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
