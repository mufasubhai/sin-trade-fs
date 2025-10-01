import { z } from "zod";
import { Asset, AssetSchema } from "./UserInterface";

export interface ListAssetResponse {
  message: string;
  status: number;
  data: Asset[];
}

export const ListAssetResponseSchema = z.object({
  message: z.string(),
  status: z.number(),
  data: z.array(AssetSchema),
});
