import { dataUrl } from "./AuthConfig";
import {
  AssetHistoryResponseSchema,
  type AssetPricePoint,
} from "../interfaces/AssetHistory";

export const getAssetHistory = async (
  tickerCode: string,
  accessToken: string,
  days = 14
): Promise<AssetPricePoint[]> => {
  const response = await fetch(
    `${dataUrl}assets/history/${tickerCode}?days=${days}`,
    {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${accessToken}`,
      },
    }
  );

  if (!response.ok) {
    throw new Error(`HTTP error! status: ${response.status}`);
  }

  const data = (await response.json()) as object;
  const parsed = AssetHistoryResponseSchema.parse(data);
  return parsed.data;
};
