import { describe, it, expect } from "vitest";
import { ListAssetResponseSchema } from "../../interfaces/ListAssetResponse";

describe("ListAssetResponse Schema", () => {
  it("should parse valid list asset response", () => {
    const validResponse = {
      message: "Success",
      status: 200,
      data: [
        {
          asset_id: 1,
          created_at: "2024-01-01",
          id: 1,
          ticker_name: "BTC",
          user_id: 1,
        },
        {
          asset_id: 2,
          created_at: "2024-01-01",
          id: 2,
          ticker_name: "ETH",
          user_id: 1,
        },
      ],
    };

    const result = ListAssetResponseSchema.parse(validResponse);
    
    expect(result.status).toBe(200);
    expect(result.data).toHaveLength(2);
    expect(result.data[0].tickerName).toBe("BTC");
    expect(result.data[1].tickerName).toBe("ETH");
  });

  it("should handle empty data array", () => {
    const responseWithEmptyData = {
      message: "No assets",
      status: 200,
      data: [],
    };

    const result = ListAssetResponseSchema.parse(responseWithEmptyData);
    
    expect(result.status).toBe(200);
    expect(result.data).toHaveLength(0);
  });

  it("should handle error response", () => {
    const errorResponse = {
      message: "Error",
      status: 400,
      data: [],
    };

    const result = ListAssetResponseSchema.parse(errorResponse);
    
    expect(result.status).toBe(400);
    expect(result.message).toBe("Error");
  });
});
