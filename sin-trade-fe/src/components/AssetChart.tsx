import { useState } from "react";
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
} from "recharts";
import { type AssetHistoryEntry } from "../interfaces/AssetHistory";

interface AssetChartProps {
  entry: AssetHistoryEntry | undefined;
  onDaysChange: (ticker: string, days: number) => void;
  tickerCode: string  ;
}
function formatTime(isoString: string): string {
  const date = new Date(isoString);
  return date.toLocaleDateString(undefined, { month: "short", day: "numeric" });
}

function formatPrice(value: number): string {
  return value.toLocaleString(undefined, {
    minimumFractionDigits: 2,
    maximumFractionDigits: 2,
  });
}

export default function AssetChart({ entry, onDaysChange, tickerCode }: AssetChartProps) {
  const [days, setDays] = useState(14);

  const handleDaysChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const newDays = parseInt(e.target.value) || 1;
    setDays(newDays);
    onDaysChange(tickerCode, newDays);
  };

  if (!entry || entry.status === "idle" || entry.status === "loading") {
    return (
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">Days:</span>
          <input
            type="number"
            min="1"
            max="365"
            value={days}
            onChange={handleDaysChange}
            className="w-16 text-xs border border-gray-200 rounded px-1 py-0.5"
          />
        </div>
        <div
          data-testid="chart-loading"
          className="h-20 w-full animate-pulse rounded bg-gray-100"
        />
      </div>
    );
  }

  if (entry.status === "error") {
    return (
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">Days:</span>
          <input
            type="number"
            min="1"
            max="365"
            value={days}
            onChange={handleDaysChange}
            className="w-16 text-xs border border-gray-200 rounded px-1 py-0.5"
          />
        </div>
        <div
          data-testid="chart-error"
          className="flex h-20 w-full items-center justify-center text-xs text-red-400"
        >
          Failed to load chart data
        </div>
      </div>
    );
  }

  if (entry.data.length === 0) {
    return (
      <div className="flex flex-col gap-1">
        <div className="flex items-center gap-2">
          <span className="text-xs text-gray-500">Days:</span>
          <input
            type="number"
            min="1"
            max="365"
            value={days}
            onChange={handleDaysChange}
            className="w-16 text-xs border border-gray-200 rounded px-1 py-0.5"
          />
        </div>
        <div
          data-testid="chart-empty"
          className="flex h-20 w-full items-center justify-center text-xs text-gray-400"
        >
          No data available
        </div>
      </div>
    );
  }

  const step = Math.max(1, Math.floor(entry.data.length / 200));
  const chartData = entry.data.filter((_, i) => i % step === 0);

  return (
    <div className="flex flex-col gap-1">
      <div className="flex items-center gap-2">
        <span className="text-xs text-gray-500">Days:</span>
        <input
          type="number"
          min="1"
          max="365"
          value={days}
          onChange={handleDaysChange}
          className="w-16 text-xs border border-gray-200 rounded px-1 py-0.5"
        />
      </div>
      <div data-testid="chart-loaded" className="h-20 w-full">
        <ResponsiveContainer width="100%" height="100%">
          <AreaChart
            data={chartData}
            margin={{ top: 4, right: 0, bottom: 0, left: 0 }}
          >
            <defs>
              <linearGradient id="priceGradient" x1="0" y1="0" x2="0" y2="1">
                <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
                <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
              </linearGradient>
            </defs>          
            <XAxis
            dataKey="priceTime"
            tickFormatter={formatTime}
            tick={{ fontSize: 10, fill: "#9ca3af" }}
            tickLine={false}
            axisLine={false}
            interval="preserveStartEnd"
          />
            <YAxis
              domain={["auto", "auto"]}
              tick={{ fontSize: 10, fill: "#9ca3af" }}
              tickLine={false}
              axisLine={false}
              tickFormatter={formatPrice}
              width={60}
            />
            <Tooltip
              formatter={(value: string | undefined) => [
                value ? `$${formatPrice(Number(value))} Price` : "",
              ]}
              labelFormatter={(label) => {
                if (typeof label === "string" || typeof label === "number") {
                  return new Date(label).toLocaleString();
                }
                return "";
              }}
              contentStyle={{
                fontSize: 12,
                borderRadius: 6,
                border: "1px solid #e5e7eb",
              }}
            />
            <Area
              type="monotone"
              dataKey="currentPrice"
              stroke="#6366f1"
              strokeWidth={1.5}
              fill="url(#priceGradient)"
              dot={false}
              isAnimationActive={false}
            />
          </AreaChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
