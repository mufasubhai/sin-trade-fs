import { StandardResponseSchema } from "../interfaces/StandardResponse";

export const deleteAsset = async ({
  assetId,
  userId,
  deleteAssetFromDB,
  fetchAssets,
  setDeleteError,
  setDeleteSuccess,
  setDeleteModalOpen,
  setDeleteLoading,
}: // refreshToken,
{
  assetId: number;
  fetchAssets: () => Promise<void>;
  setDeleteModalOpen: (deleteModalOpen: boolean) => void;
  userId: number | null;
  deleteAssetFromDB: (
    assetId: number,
    userId: number
  ) => Promise<Response | undefined>;
  setDeleteLoading: (isLoading: boolean) => void;
  setDeleteError: (isError: boolean) => void;
  setDeleteSuccess: (isSuccess: boolean) => void;
  // refreshToken: string;
}) => {
  setDeleteLoading(true);
  try {
    // should set this to a different location. Make this a discrete function outside of the UI.

    const response = await deleteAssetFromDB(assetId, userId ?? 0);
    // this needs to be cleaned up

    if (!response || !response.ok || response.status !== 200) {
      setDeleteError(true);
      setDeleteSuccess(false);
      throw new Error(`HTTP error! status: ${response?.status}`);
      setDeleteLoading(false);
      return "error";
    }

    setDeleteLoading(false);

    const data = (await response.json()) as object;

    const addAssetResponse = StandardResponseSchema.parse(data);

    if (addAssetResponse.status === 200) {
      await fetchAssets();
    }

    setDeleteError(false);
    setDeleteSuccess(true);
    // loginUser(user);
    setDeleteModalOpen(false);

    return "success";

    // TODO: redirect to dashboard page
  } catch (error) {
    console.error("Error deleting asset", error);
    // logoutUser();
    setDeleteLoading(false);
    setDeleteError(true);
    setDeleteModalOpen(false);
    setDeleteSuccess(false);
  }
};
