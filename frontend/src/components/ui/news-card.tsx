import { NewsItem } from "@/lib/api";

interface NewsCardProps {
  news: NewsItem[];
}

export function NewsCard({ news }: NewsCardProps) {
  if (news.length === 0) {
    return (
      <div className="rounded-xl border border-white/10 bg-white/5 p-6 text-center">
        <p className="text-white/60">No recent news available</p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {news.slice(0, 5).map((item, idx) => (
        <div
          key={idx}
          className="rounded-xl border border-white/10 bg-white/5 p-4 transition-colors hover:bg-white/10"
        >
          <h4 className="font-medium text-white line-clamp-2">{item.title}</h4>
          <div className="mt-2 flex items-center gap-2 text-xs text-white/50">
            <span>{item.publisher}</span>
            <span>•</span>
            <span>{item.published}</span>
          </div>
        </div>
      ))}
    </div>
  );
}
