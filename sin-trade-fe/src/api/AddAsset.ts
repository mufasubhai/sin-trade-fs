import { AddAssetResponseSchema } from "../interfaces/AddAssetResponse";

export const addAsset = async ({
  assetTicker,
  isCrypto,
  setIsLoading,
  fetchAssets,
  setIsError,
  addAssetToDB,
  userId,
  setIsSuccess,
  accessToken,
  setAddModalOpen,
  refreshToken,
}: {
  assetTicker: string;
  fetchAssets: () => Promise<void>;
  addAssetToDB: (
    assetTicker: string,
    userId: number,
    isCrypto: boolean,
    refreshToken: string,
    accessToken: string
  ) => Promise<Response | undefined>;
  setAddModalOpen: (addModalOpen: boolean) => void;
  isCrypto: boolean | null;
  userId: number | null;
  setIsLoading: (isLoading: boolean) => void;
  setIsError: (isError: boolean) => void;
  setIsSuccess: (isSuccess: boolean) => void;
  accessToken: string;
  refreshToken: string;
}) => {
  setIsLoading(true);
  try {
    // should set this to a different location. Make this a discrete function outside of the UI.

    const response = await addAssetToDB(
      assetTicker,
      userId ?? 0,
      isCrypto ?? false,
      refreshToken,
      accessToken
    );

    // this needs to be cleaned up

    if (!response || !response.ok || response.status !== 200) {
      setIsError(true);
      setIsSuccess(false);
      throw new Error(`HTTP error! status: ${response?.status}`);
      setIsLoading(false);
      return "error";
    }

    setIsLoading(false);

    const data = (await response.json()) as object;

    const addAssetResponse = AddAssetResponseSchema.parse(data);

    if (addAssetResponse.status === 200) {
      await fetchAssets();
    }

    // we need to refreshe the data base don new data
    // we need to close the modal.
    // we should add proper error handling in case of failure.

    //

    // const user = UserResponseSchema.parse(data);
    // here we need to redirect to the dashboard page,
    // we also need to store the token and user data in local storage
    // we also need to store the token and user data in state
    // we also need to redirect to the dashboard page

    // here we need to validate the data
    // const data = (await response.json());

    // need to use zod here to validate the data

    setIsError(false);
    setIsSuccess(true);
    // loginUser(user);
    setAddModalOpen(false);

    return "success";

    // TODO: redirect to dashboard page
  } catch (error) {
    console.error("Error logging in", error);
    // logoutUser();
    setIsLoading(false);
    setIsError(true);
    setAddModalOpen(false);
    setIsSuccess(false);
  }
};
