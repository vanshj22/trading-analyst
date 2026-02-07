import { Trade } from "@/lib/api";
import { cn } from "@/lib/utils";
import { ArrowUpRight, ArrowDownRight } from "lucide-react";

interface TradeTableProps {
  trades: Trade[];
  className?: string;
}

export function TradeTable({ trades, className }: TradeTableProps) {
  if (trades.length === 0) {
    return (
      <div className="glass-card flex flex-col items-center justify-center p-12 text-center">
        <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-2xl bg-primary/10">
          <ArrowUpRight className="h-8 w-8 text-primary" />
        </div>
        <h3 className="text-lg font-semibold text-white">No Trades Yet</h3>
        <p className="mt-2 text-white/50">Load demo trades to see your trading history</p>
      </div>
    );
  }

  return (
    <div className={cn("premium-table", className)}>
      <table className="w-full">
        <thead>
          <tr>
            <th>Time</th>
            <th>Ticker</th>
            <th>Action</th>
            <th className="text-right">Price</th>
            <th className="text-right">Qty</th>
            <th className="text-right">P&L</th>
          </tr>
        </thead>
        <tbody>
          {trades.slice(-10).reverse().map((trade, idx) => (
            <tr key={idx}>
              <td className="text-white/60">
                {new Date(trade.timestamp).toLocaleDateString()}
              </td>
              <td className="font-semibold text-white">
                {trade.ticker}
              </td>
              <td>
                <span
                  className={cn(
                    "inline-flex items-center gap-1 rounded-lg px-2.5 py-1 text-xs font-semibold",
                    trade.action === "BUY"
                      ? "bg-emerald-500/15 text-emerald-400"
                      : "bg-red-500/15 text-red-400"
                  )}
                >
                  {trade.action === "BUY" ? (
                    <ArrowUpRight className="h-3 w-3" />
                  ) : (
                    <ArrowDownRight className="h-3 w-3" />
                  )}
                  {trade.action}
                </span>
              </td>
              <td className="text-right font-mono text-white/80">
                ${typeof trade.price === 'number' ? trade.price.toFixed(2) : '0.00'}
              </td>
              <td className="text-right font-mono text-white/60">
                {trade.quantity}
              </td>
              <td
                className={cn(
                  "text-right font-mono font-semibold",
                  (trade.PnL || 0) >= 0 ? "text-emerald-400" : "text-red-400"
                )}
              >
                {(trade.PnL || 0) >= 0 ? "+" : ""}${(trade.PnL || 0).toFixed(2)}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
