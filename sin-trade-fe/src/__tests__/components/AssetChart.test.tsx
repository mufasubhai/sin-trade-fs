import { describe, it, expect, vi } from "vitest";
import { render, screen } from "@testing-library/react";
import AssetChart from "../../components/AssetChart";
import { type AssetHistoryEntry } from "../../interfaces/AssetHistory";

// ResponsiveContainer needs ResizeObserver
global.ResizeObserver = vi.fn().mockImplementation(() => ({
  observe: vi.fn(),
  unobserve: vi.fn(),
  disconnect: vi.fn(),
}));

const makeEntry = (
  status: AssetHistoryEntry["status"],
  points = 0
): AssetHistoryEntry => ({
  status,
  data: Array.from({ length: points }, (_, i) => ({
    priceTime: `2026-02-14T${String(Math.floor(i / 12)).padStart(2, "0")}:${String((i % 12) * 5).padStart(2, "0")}:00`,
    currentPrice: 50000 + i * 10,
    interval: "5min" as const,
  })),
});

describe("AssetChart", () => {
  it("renders loading skeleton when status is loading", () => {
    render(<AssetChart entry={makeEntry("loading")} />);
    expect(screen.getByTestId("chart-loading")).not.toBeNull();
  });

  it("renders loading skeleton when status is idle", () => {
    render(<AssetChart entry={makeEntry("idle")} />);
    expect(screen.getByTestId("chart-loading")).not.toBeNull();
  });

  it("renders loading skeleton when entry is undefined", () => {
    render(<AssetChart entry={undefined} />);
    expect(screen.getByTestId("chart-loading")).not.toBeNull();
  });

  it("renders error state when status is error", () => {
    render(<AssetChart entry={makeEntry("error")} />);
    expect(screen.getByTestId("chart-error")).not.toBeNull();
    expect(screen.getByText(/failed to load/i)).not.toBeNull();
  });

  it("renders empty state when loaded with no data", () => {
    render(<AssetChart entry={makeEntry("loaded", 0)} />);
    expect(screen.getByTestId("chart-empty")).not.toBeNull();
    expect(screen.getByText(/no data available/i)).not.toBeNull();
  });

  it("renders chart when loaded with data", () => {
    render(<AssetChart entry={makeEntry("loaded", 10)} />);
    expect(screen.getByTestId("chart-loaded")).not.toBeNull();
  });
});
