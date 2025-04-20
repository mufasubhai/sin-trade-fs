import { z } from "zod";

export interface UserResponse {
  accessToken: string;
  refreshToken: string;
  activeAssets: Record<string, Asset>;
  avatarUrl: string | null;
  createdAt: Date;
  email: string;
  emailConfirmedAt: Date | null;
  firstName: string | null;
  lastName: string | null;
  updatedAt: Date;
  userId: number;
  username: string | null;
  website: string | null;
}

export interface Asset {
  assetId: number;
  createdAt: Date;
  id: number;
  tickerName: string;
  userId: number;
}



  const AssetSchema = z.object({
    asset_id: z.number(),
    created_at: z.string(),
    id: z.number(),
    ticker_name: z.string(),
    user_id: z.number(),
  }).transform((data) => {



    return {
      assetId: data.asset_id,
      // this might be dangerous
      createdAt: new Date(data.created_at),
      id: data.id,
      tickerName: data.ticker_name,
      userId: data.user_id,
    };
  })  ;
  
export const UserResponseSchema = z.object({
  access_token: z.string(),
  refresh_token: z.string(),
  active_assets: z.record(z.string(), AssetSchema),
  avatar_url: z.string().nullable(),
  created_at: z.string(),
  email: z.string(),
  email_confirmed_at: z.date().nullable(),
  first_name: z.string().nullable(),
  last_name: z.string().nullable(),
  updated_at: z.string(),
  user_id: z.number(),
  username: z.string().nullable(),
  website: z.string().nullable(),
}).transform((data) => {
  return {
    accessToken: data.access_token,
    refreshToken: data.refresh_token,
    activeAssets: data.active_assets,
    avatarUrl: data.avatar_url,
    createdAt: new Date(data.created_at),
    email: data.email,
    emailConfirmedAt: data.email_confirmed_at,
    firstName: data.first_name,
    lastName: data.last_name,
    updatedAt: new Date(data.updated_at),
    userId: data.user_id,
    username: data.username,
    website: data.website,
  };
});

