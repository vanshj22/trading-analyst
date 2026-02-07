"use client";

import { useState, useEffect } from "react";
import { useApp } from "@/lib/context";
import { getPersonas, generateSocialContent, generateBriefing } from "@/lib/api";
import { ContentPreview } from "@/components/ui/content-preview";
import { MessageSquare, Sparkles, Loader2, Newspaper, Twitter, Linkedin, Users } from "lucide-react";
import { cn } from "@/lib/utils";

const TICKERS_FOR_BRIEFING = ["AAPL", "TSLA", "NVDA", "GOOGL", "AMZN", "META", "SPY", "BTC-USD"];

const PLATFORMS = [
  { value: "twitter", label: "Twitter Post", icon: Twitter },
  { value: "thread", label: "Twitter Thread", icon: MessageSquare },
  { value: "linkedin", label: "LinkedIn Post", icon: Linkedin },
] as const;

export default function SocialPage() {
  const { ticker } = useApp();
  const [personas, setPersonas] = useState<string[]>([]);
  const [selectedPersona, setSelectedPersona] = useState("");
  const [platform, setPlatform] = useState<"twitter" | "thread" | "linkedin">("twitter");
  const [content, setContent] = useState<string | { twitter?: string; linkedin?: string } | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Briefing state
  const [selectedBriefingTickers, setSelectedBriefingTickers] = useState(["AAPL", "TSLA", "NVDA"]);
  const [briefing, setBriefing] = useState<string | null>(null);
  const [briefingLoading, setBriefingLoading] = useState(false);

  useEffect(() => {
    loadPersonas();
  }, []);

  const loadPersonas = async () => {
    try {
      const res = await getPersonas();
      setPersonas(res.personas);
      if (res.personas.length > 0) {
        setSelectedPersona(res.personas[0]);
      }
    } catch {
      console.log("Failed to load personas");
    }
  };

  const handleGenerate = async () => {
    setLoading(true);
    setError(null);
    try {
      const res = await generateSocialContent(ticker, selectedPersona, platform);
      setContent(res.content);
    } catch {
      setError("Failed to generate content. Is the API server running?");
    }
    setLoading(false);
  };

  const handleGenerateBriefing = async () => {
    setBriefingLoading(true);
    try {
      const res = await generateBriefing(selectedBriefingTickers);
      setBriefing(res.briefing);
    } catch {
      console.log("Failed to generate briefing");
    }
    setBriefingLoading(false);
  };

  const toggleBriefingTicker = (t: string) => {
    if (selectedBriefingTickers.includes(t)) {
      setSelectedBriefingTickers(selectedBriefingTickers.filter((x) => x !== t));
    } else {
      setSelectedBriefingTickers([...selectedBriefingTickers, t]);
    }
  };

  return (
    <div className="container mx-auto px-6 py-10">
      {/* Hero Section */}
      <div className="mb-10">
        <div className="inline-flex items-center gap-2 rounded-full border border-primary/30 bg-primary/10 px-4 py-1.5 text-sm text-primary">
          <MessageSquare className="h-4 w-4" />
          <span>Social Content Studio</span>
        </div>
        <h1 className="mt-4 text-4xl font-bold tracking-tight text-white md:text-5xl">
          Create <span className="text-primary">Viral</span> Content
        </h1>
        <p className="mt-3 text-lg text-white/50">
          Generate AI-powered social media content with unique personas and market context.
        </p>
      </div>

      {error && (
        <div className="mb-8 glass-card border-red-500/30 bg-red-500/10 p-4">
          <p className="text-red-400">{error}</p>
        </div>
      )}

      <div className="grid gap-8 lg:grid-cols-3">
        {/* Left Column - Controls */}
        <div className="space-y-6">
          {/* Persona Selector */}
          <div className="glass-card p-6">
            <div className="flex items-center gap-3 mb-4">
              <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-primary/20">
                <Users className="h-5 w-5 text-primary" />
              </div>
              <h2 className="text-lg font-semibold text-white">Select Persona</h2>
            </div>
            <select
              value={selectedPersona}
              onChange={(e) => setSelectedPersona(e.target.value)}
              className="w-full rounded-xl border border-white/[0.08] bg-white/[0.03] px-4 py-3.5 text-white backdrop-blur-sm transition-all focus:border-primary/50 focus:outline-none"
            >
              {personas.map((p) => (
                <option key={p} value={p} className="bg-[#1a1225]">
                  {p}
                </option>
              ))}
            </select>
          </div>

          {/* Platform Selector */}
          <div className="glass-card p-6">
            <h2 className="text-lg font-semibold text-white mb-4">Content Type</h2>
            <div className="space-y-2">
              {PLATFORMS.map((opt) => {
                const Icon = opt.icon;
                return (
                  <button
                    key={opt.value}
                    onClick={() => setPlatform(opt.value)}
                    className={cn(
                      "flex w-full items-center gap-3 rounded-xl p-4 transition-all",
                      platform === opt.value
                        ? "bg-gradient-to-r from-primary/20 to-purple-600/20 border border-primary/30"
                        : "border border-white/[0.05] hover:bg-white/[0.03]"
                    )}
                  >
                    <Icon className={cn("h-5 w-5", platform === opt.value ? "text-primary" : "text-white/60")} />
                    <span className={cn("font-medium", platform === opt.value ? "text-white" : "text-white/70")}>
                      {opt.label}
                    </span>
                  </button>
                );
              })}
            </div>
          </div>

          <button
            onClick={handleGenerate}
            disabled={loading || !selectedPersona}
            className="btn-primary w-full flex items-center justify-center gap-2"
          >
            {loading ? (
              <Loader2 className="h-4 w-4 animate-spin" />
            ) : (
              <Sparkles className="h-4 w-4" />
            )}
            Generate Content
          </button>
        </div>

        {/* Right Columns - Preview */}
        <div className="lg:col-span-2 space-y-6">
          <h2 className="text-xl font-semibold text-white">📄 Content Preview</h2>
          
          {content ? (
            <>
              <ContentPreview content={content} platform={platform} />
              <div className="glass-card p-4 flex items-center gap-3">
                <Sparkles className="h-5 w-5 text-primary" />
                <p className="text-sm text-white/60">
                  Copy the content above and paste it directly into your social media platform!
                </p>
              </div>
            </>
          ) : (
            <div className="glass-card flex flex-col items-center justify-center p-16 text-center">
              <div className="mb-6 flex h-20 w-20 items-center justify-center rounded-2xl bg-primary/10">
                <MessageSquare className="h-10 w-10 text-primary" />
              </div>
              <h3 className="text-xl font-semibold text-white">Ready to Create</h3>
              <p className="mt-2 text-white/50 max-w-sm">
                Select a persona and click 'Generate Content' to create social media posts
              </p>
            </div>
          )}
        </div>
      </div>

      {/* Daily Briefing Section */}
      <div className="mt-16 border-t border-white/[0.06] pt-12">
        <div className="flex items-center gap-3 mb-8">
          <div className="flex h-12 w-12 items-center justify-center rounded-xl bg-gradient-to-br from-primary to-purple-600">
            <Newspaper className="h-6 w-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-white">Daily Market Briefing</h2>
            <p className="text-white/50">Generate a comprehensive market summary</p>
          </div>
        </div>
        
        <div className="grid gap-8 lg:grid-cols-3">
          <div className="space-y-4">
            <h3 className="text-sm font-medium text-white/60">Select tickers for briefing</h3>
            <div className="flex flex-wrap gap-2">
              {TICKERS_FOR_BRIEFING.map((t) => (
                <button
                  key={t}
                  onClick={() => toggleBriefingTicker(t)}
                  className={cn(
                    "rounded-xl px-4 py-2.5 text-sm font-medium transition-all",
                    selectedBriefingTickers.includes(t)
                      ? "bg-gradient-to-r from-primary to-purple-600 text-white shadow-lg shadow-primary/20"
                      : "border border-white/[0.08] bg-white/[0.02] text-white/60 hover:bg-white/[0.05]"
                  )}
                >
                  {t}
                </button>
              ))}
            </div>
            <button
              onClick={handleGenerateBriefing}
              disabled={briefingLoading || selectedBriefingTickers.length === 0}
              className="w-full mt-4 rounded-xl border border-white/[0.1] bg-white/[0.03] px-4 py-3 text-white font-medium transition-all hover:bg-white/[0.06] flex items-center justify-center gap-2"
            >
              {briefingLoading ? (
                <Loader2 className="h-4 w-4 animate-spin" />
              ) : (
                <Newspaper className="h-4 w-4" />
              )}
              Generate Daily Briefing
            </button>
          </div>

          <div className="lg:col-span-2">
            {briefing ? (
              <div className="glass-card p-6">
                <h3 className="mb-4 font-semibold text-white flex items-center gap-2">
                  <Newspaper className="h-5 w-5 text-primary" />
                  Today's Market Briefing
                </h3>
                <div className="prose prose-invert max-w-none">
                  <pre className="whitespace-pre-wrap text-sm text-white/80 font-sans">{briefing}</pre>
                </div>
              </div>
            ) : (
              <div className="glass-card flex flex-col items-center justify-center p-12 text-center">
                <Newspaper className="h-12 w-12 text-white/20 mb-4" />
                <p className="text-white/50">Select tickers and generate a briefing</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
