"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useApp } from "@/lib/context";
import { cn } from "@/lib/utils";
import { BarChart3, Search, MessageSquare, Brain, ChevronDown } from "lucide-react";

const TICKERS = ["AAPL", "TSLA", "NVDA", "BTC-USD", "SPY", "GOOGL", "AMZN", "META"];

const NAV_ITEMS = [
  { href: "/", label: "Dashboard", icon: BarChart3 },
  { href: "/market", label: "Market", icon: Search },
  { href: "/social", label: "Social", icon: MessageSquare },
  { href: "/coach", label: "Coach", icon: Brain },
];

export function Navbar() {
  const pathname = usePathname();
  const { ticker, setTicker, initialized } = useApp();

  return (
    <nav className="sticky top-0 z-50 border-b border-white/[0.06] bg-background/60 backdrop-blur-2xl">
      <div className="container mx-auto flex h-16 items-center justify-between px-6">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-3 group">
          <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600 shadow-lg shadow-primary/20 transition-transform group-hover:scale-105">
            <Brain className="h-5 w-5 text-white" />
          </div>
          <div className="hidden sm:block">
            <span className="font-bold text-white">Antifragile</span>
            <span className="ml-1 font-light text-white/60">Mirror</span>
          </div>
        </Link>

        {/* Navigation */}
        <div className="flex items-center gap-1 rounded-2xl bg-white/[0.03] p-1">
          {NAV_ITEMS.map((item) => {
            const Icon = item.icon;
            const isActive = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={cn(
                  "flex items-center gap-2 rounded-xl px-4 py-2.5 text-sm font-medium transition-all duration-200",
                  isActive
                    ? "bg-gradient-to-br from-primary/20 to-purple-600/20 text-white shadow-lg shadow-primary/10"
                    : "text-white/50 hover:bg-white/[0.05] hover:text-white"
                )}
              >
                <Icon className={cn("h-4 w-4", isActive && "text-primary")} />
                <span className="hidden md:inline">{item.label}</span>
              </Link>
            );
          })}
        </div>

        {/* Ticker Selector & Status */}
        <div className="flex items-center gap-4">
          <div className="relative">
            <select
              value={ticker}
              onChange={(e) => setTicker(e.target.value)}
              className="appearance-none rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-2.5 pr-10 text-sm font-medium text-white backdrop-blur-sm transition-all focus:border-primary/50 focus:outline-none focus:ring-2 focus:ring-primary/20"
            >
              {TICKERS.map((t) => (
                <option key={t} value={t} className="bg-[#1a1225] text-white">
                  {t}
                </option>
              ))}
            </select>
            <ChevronDown className="pointer-events-none absolute right-3 top-1/2 h-4 w-4 -translate-y-1/2 text-white/40" />
          </div>

          <div
            className={cn(
              "flex items-center gap-2 rounded-xl px-4 py-2 text-xs font-medium transition-all",
              initialized
                ? "border border-emerald-500/20 bg-emerald-500/10 text-emerald-400"
                : "border border-amber-500/20 bg-amber-500/10 text-amber-400"
            )}
          >
            <span
              className={cn(
                "h-2 w-2 rounded-full",
                initialized ? "bg-emerald-400 animate-pulse" : "bg-amber-400"
              )}
            />
            <span className="hidden sm:inline">{initialized ? "Active" : "Setup Required"}</span>
          </div>
        </div>
      </div>
    </nav>
  );
}
