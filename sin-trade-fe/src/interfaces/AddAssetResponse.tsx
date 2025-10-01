import { z } from "zod";

export interface AssetResponse {
  message: string;
  status: number;
}

export const AddAssetResponseSchema = z.object({
  message: z.string(),
  status: z.number(),
});
