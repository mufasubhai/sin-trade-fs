import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { deleteAsset } from "../../api/DeleteAsset";

global.fetch = vi.fn();

describe("DeleteAsset API", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  it("should delete asset successfully", async () => {
    const mockResponse = {
      message: "Asset deleted successfully",
      status: 200,
    };

    const mockDeleteAssetFromDB = vi.fn().mockResolvedValueOnce({
      ok: true,
      status: 200,
      json: () => Promise.resolve(mockResponse),
    });

    const mockFetchAssets = vi.fn().mockResolvedValueOnce(undefined);

    const setDeleteLoading = vi.fn();
    const setDeleteError = vi.fn();
    const setDeleteSuccess = vi.fn();
    const setDeleteModalOpen = vi.fn();

    await deleteAsset({
      assetId: 1,
      userId: 1,
      deleteAssetFromDB: mockDeleteAssetFromDB,
      fetchAssets: mockFetchAssets,
      setDeleteError,
      setDeleteSuccess,
      setDeleteModalOpen,
      setDeleteLoading,
    });

    expect(setDeleteLoading).toHaveBeenCalledWith(true);
    expect(setDeleteError).toHaveBeenCalledWith(false);
    expect(setDeleteSuccess).toHaveBeenCalledWith(true);
    expect(mockFetchAssets).toHaveBeenCalled();
    expect(setDeleteModalOpen).toHaveBeenCalledWith(false);
  });

  it("should handle delete asset error", async () => {
    const mockDeleteAssetFromDB = vi.fn().mockResolvedValueOnce({
      ok: false,
      status: 400,
    });

    const mockFetchAssets = vi.fn().mockResolvedValueOnce(undefined);

    const setDeleteLoading = vi.fn();
    const setDeleteError = vi.fn();
    const setDeleteSuccess = vi.fn();
    const setDeleteModalOpen = vi.fn();

    await deleteAsset({
      assetId: 999,
      userId: 1,
      deleteAssetFromDB: mockDeleteAssetFromDB,
      fetchAssets: mockFetchAssets,
      setDeleteError,
      setDeleteSuccess,
      setDeleteModalOpen,
      setDeleteLoading,
    });

    expect(setDeleteError).toHaveBeenCalledWith(true);
    expect(setDeleteSuccess).toHaveBeenCalledWith(false);
    expect(setDeleteModalOpen).toHaveBeenCalledWith(false);
  });

  it("should handle network error", async () => {
    const mockDeleteAssetFromDB = vi.fn().mockRejectedValueOnce(new Error("Network error"));

    const mockFetchAssets = vi.fn().mockResolvedValueOnce(undefined);

    const setDeleteLoading = vi.fn();
    const setDeleteError = vi.fn();
    const setDeleteSuccess = vi.fn();
    const setDeleteModalOpen = vi.fn();

    await deleteAsset({
      assetId: 1,
      userId: 1,
      deleteAssetFromDB: mockDeleteAssetFromDB,
      fetchAssets: mockFetchAssets,
      setDeleteError,
      setDeleteSuccess,
      setDeleteModalOpen,
      setDeleteLoading,
    });

    expect(setDeleteError).toHaveBeenCalledWith(true);
    expect(setDeleteSuccess).toHaveBeenCalledWith(false);
  });
});
