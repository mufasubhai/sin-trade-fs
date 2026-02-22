import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { addAsset } from "../../api/AddAsset";

global.fetch = vi.fn();

describe("AddAsset API", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it("should add asset successfully", async () => {
    const mockResponse = {
      message: "Asset added successfully",
      status: 200,
    };

    const mockAddAssetToDB = vi.fn().mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(mockResponse),
    });

    const mockFetchAssets = vi.fn().mockResolvedValueOnce(undefined);

    const setIsLoading = vi.fn();
    const setIsError = vi.fn();
    const setIsSuccess = vi.fn();
    const setAddModalOpen = vi.fn();

    await addAsset({
      assetTicker: "BTC",
      isCrypto: true,
      setIsLoading,
      fetchAssets: mockFetchAssets,
      setIsError,
      addAssetToDB: mockAddAssetToDB,
      userId: 1,
      setIsSuccess,
      accessToken: "test_token",
      setAddModalOpen,
    });

    expect(setIsLoading).toHaveBeenCalledWith(true);
    expect(setIsError).toHaveBeenCalledWith(false);
    expect(setIsSuccess).toHaveBeenCalledWith(true);
    expect(mockFetchAssets).toHaveBeenCalled();
    expect(setAddModalOpen).toHaveBeenCalledWith(false);
  });

  it("should handle add asset error", async () => {
    const mockAddAssetToDB = vi.fn().mockResolvedValueOnce({
      ok: false,
      status: 400,
    });

    const mockFetchAssets = vi.fn().mockResolvedValueOnce(undefined);

    const setIsLoading = vi.fn();
    const setIsError = vi.fn();
    const setIsSuccess = vi.fn();
    const setAddModalOpen = vi.fn();

    await addAsset({
      assetTicker: "INVALID",
      isCrypto: false,
      setIsLoading,
      fetchAssets: mockFetchAssets,
      setIsError,
      addAssetToDB: mockAddAssetToDB,
      userId: 1,
      setIsSuccess,
      accessToken: "test_token",
      setAddModalOpen,
    });

    expect(setIsError).toHaveBeenCalledWith(true);
    expect(setIsSuccess).toHaveBeenCalledWith(false);
    expect(setAddModalOpen).toHaveBeenCalledWith(false);
  });

  it("should handle network error", async () => {
    const mockAddAssetToDB = vi.fn().mockRejectedValueOnce(new Error("Network error"));

    const mockFetchAssets = vi.fn().mockResolvedValueOnce(undefined);

    const setIsLoading = vi.fn();
    const setIsError = vi.fn();
    const setIsSuccess = vi.fn();
    const setAddModalOpen = vi.fn();

    await addAsset({
      assetTicker: "BTC",
      isCrypto: true,
      setIsLoading,
      fetchAssets: mockFetchAssets,
      setIsError,
      addAssetToDB: mockAddAssetToDB,
      userId: 1,
      setIsSuccess,
      accessToken: "test_token",
      setAddModalOpen,
    });

    expect(setIsError).toHaveBeenCalledWith(true);
    expect(setIsSuccess).toHaveBeenCalledWith(false);
  });
});
