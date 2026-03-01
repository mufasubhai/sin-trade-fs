import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { getAssetHistory } from "../../api/GetAssetHistory";

global.fetch = vi.fn();

const mockPricePoint = {
  price_time: "2026-02-14T10:00:00",
  current_price: 50000.0,
  interval: "5min",
};

const mockResponse = {
  data: [mockPricePoint],
  message: "History fetched successfully",
  status: 200,
};

describe("getAssetHistory", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it("returns parsed price points on success", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(mockResponse),
    } as Response);

    const result = await getAssetHistory("BTC", "test_token");

    expect(result).toHaveLength(1);
    expect(result[0].priceTime).toBe("2026-02-14T10:00:00");
    expect(result[0].currentPrice).toBe(50000.0);
    expect(result[0].interval).toBe("5min");
  });

  it("calls the correct URL with default days", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ ...mockResponse, data: [] }),
    } as Response);

    await getAssetHistory("ETH", "test_token");

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("history/ETH?days=14"),
      expect.objectContaining({
        method: "GET",
        headers: expect.objectContaining({
          Authorization: "Bearer test_token",
        }),
      })
    );
  });

  it("calls the correct URL with custom days", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve({ ...mockResponse, data: [] }),
    } as Response);

    await getAssetHistory("BTC", "test_token", 7);

    expect(fetch).toHaveBeenCalledWith(
      expect.stringContaining("history/BTC?days=7"),
      expect.anything()
    );
  });

  it("throws on non-OK HTTP response", async () => {
    vi.mocked(fetch).mockResolvedValueOnce({
      ok: false,
      status: 401,
    } as Response);

    await expect(getAssetHistory("BTC", "bad_token")).rejects.toThrow(
      "HTTP error! status: 401"
    );
  });

  it("throws on network failure", async () => {
    vi.mocked(fetch).mockRejectedValueOnce(new Error("Network error"));

    await expect(getAssetHistory("BTC", "test_token")).rejects.toThrow(
      "Network error"
    );
  });
});
