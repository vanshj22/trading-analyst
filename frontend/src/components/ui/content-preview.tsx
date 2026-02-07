"use client";

import { useState } from "react";
import { Copy, Check } from "lucide-react";
import { cn } from "@/lib/utils";

interface ContentPreviewProps {
  content: string | { twitter?: string; linkedin?: string };
  platform?: string;
}

export function ContentPreview({ content, platform }: ContentPreviewProps) {
  const [copied, setCopied] = useState(false);

  const handleCopy = async (text: string) => {
    await navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  if (typeof content === "object") {
    return (
      <div className="space-y-4">
        {content.twitter && (
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-white/60">🐦 Twitter Version</span>
              <button
                onClick={() => handleCopy(content.twitter!)}
                className="flex items-center gap-1 rounded-lg bg-white/10 px-3 py-1 text-xs text-white/70 hover:bg-white/20 transition-colors"
              >
                {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                {copied ? "Copied!" : "Copy"}
              </button>
            </div>
            <pre className="whitespace-pre-wrap font-mono text-sm text-white/90">
              {content.twitter}
            </pre>
          </div>
        )}
        {content.linkedin && (
          <div className="rounded-xl border border-white/10 bg-white/5 p-4">
            <div className="flex items-center justify-between mb-3">
              <span className="text-sm text-white/60">💼 LinkedIn Version</span>
              <button
                onClick={() => handleCopy(content.linkedin!)}
                className="flex items-center gap-1 rounded-lg bg-white/10 px-3 py-1 text-xs text-white/70 hover:bg-white/20 transition-colors"
              >
                {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
                {copied ? "Copied!" : "Copy"}
              </button>
            </div>
            <pre className="whitespace-pre-wrap font-mono text-sm text-white/90">
              {content.linkedin}
            </pre>
          </div>
        )}
      </div>
    );
  }

  return (
    <div className="rounded-xl border border-white/10 bg-white/5 p-4">
      <div className="flex items-center justify-between mb-3">
        <span className="text-sm text-white/60">
          {platform === "linkedin" ? "💼 LinkedIn" : platform === "thread" ? "🧵 Twitter Thread" : "🐦 Twitter"}
        </span>
        <button
          onClick={() => handleCopy(content)}
          className="flex items-center gap-1 rounded-lg bg-white/10 px-3 py-1 text-xs text-white/70 hover:bg-white/20 transition-colors"
        >
          {copied ? <Check className="h-3 w-3" /> : <Copy className="h-3 w-3" />}
          {copied ? "Copied!" : "Copy"}
        </button>
      </div>
      <pre className="whitespace-pre-wrap font-mono text-sm text-white/90">
        {content}
      </pre>
    </div>
  );
}
