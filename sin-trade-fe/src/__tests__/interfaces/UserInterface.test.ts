import { describe, it, expect } from "vitest";
import { AssetSchema, UserResponseSchema} from "../../interfaces/UserInterface";

describe("UserInterface Schemas", () => {
  describe("AssetSchema", () => {
    it("should parse valid asset data", () => {
      const validAsset = {
        asset_id: 1,
        created_at: "2024-01-01",
        id: 1,
        ticker_name: "BTC",
        user_id: 1,
      };

      const result = AssetSchema.parse(validAsset);
      
      expect(result.assetId).toBe(1);
      expect(result.tickerName).toBe("BTC");
      expect(result.userId).toBe(1);
    });

    it("should handle null created_at", () => {
      const assetWithNull = {
        asset_id: 1,
        created_at: null,
        id: null,
        ticker_name: "BTC",
        user_id: 1,
      };

      const result = AssetSchema.parse(assetWithNull);
      
      expect(result.createdAt).toBeNull();
      expect(result.id).toBeNull();
    });
  });

  describe("UserResponseSchema", () => {
    it("should parse valid user response", () => {
      const validUser = {
        access_token: "access_token_123",
        refresh_token: "refresh_token_123",
        active_assets: {},
        avatar_url: "https://example.com/avatar.png",
        created_at: "2024-01-01T00:00:00Z",
        email: "test@example.com",
        email_confirmed_at: null,
        first_name: "John",
        last_name: "Doe",
        updated_at: "2024-01-01T00:00:00Z",
        user_id: 1,
        username: "johndoe",
        website: "https://example.com",
      };

      const result = UserResponseSchema.parse(validUser);
      
      expect(result.accessToken).toBe("access_token_123");
      expect(result.email).toBe("test@example.com");
      expect(result.firstName).toBe("John");
      expect(result.userId).toBe(1);
    });

    it("should handle null optional fields", () => {
      const userWithNulls = {
        access_token: "access_token_123",
        refresh_token: "refresh_token_123",
        active_assets: {},
        avatar_url: null,
        created_at: "2024-01-01T00:00:00Z",
        email: "test@example.com",
        email_confirmed_at: null,
        first_name: null,
        last_name: null,
        updated_at: "2024-01-01T00:00:00Z",
        user_id: 1,
        username: null,
        website: null,
      };

      const result = UserResponseSchema.parse(userWithNulls);
      
      expect(result.firstName).toBeNull();
      expect(result.lastName).toBeNull();
      expect(result.username).toBeNull();
      expect(result.website).toBeNull();
    });
  });
});
