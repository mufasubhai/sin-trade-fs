import { z } from "zod";

export const AssetPricePointSchema = z
  .object({
    price_time: z.string(),
    current_price: z.number(),
    interval: z.enum(["5min", "daily_expanded"]),
  })
  .passthrough()
  .transform((data) => ({
    priceTime: data.price_time,
    currentPrice: data.current_price,
    interval: data.interval,
  }));

export type AssetPricePoint = z.infer<typeof AssetPricePointSchema>;

export const AssetHistoryResponseSchema = z.object({
  data: z.array(AssetPricePointSchema),
  message: z.string(),
  status: z.number(),
});

export type AssetHistoryStatus = "idle" | "loading" | "loaded" | "error";

export interface AssetHistoryEntry {
  data: AssetPricePoint[];
  status: AssetHistoryStatus;
}
