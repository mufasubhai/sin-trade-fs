// import { UserResponse UserResponseSchema } from "../interfaces/UserInterface";
import { dataUrl } from "./AuthConfig";

export const addAsset = async ({
  assetTicker,
  isCrypto,
  setIsLoading,
  setIsError,
  userId,
  setIsSuccess,
  accessToken,
  refreshToken,
}: {
  assetTicker: string;
  isCrypto: boolean;
  userId: number;
  setIsLoading: (isLoading: boolean) => void;
  setIsError: (isError: boolean) => void;
  setIsSuccess: (isSuccess: boolean) => void;
  accessToken: string;
  refreshToken: string;
}) => {
  setIsLoading(true);
  try {
    console.log("DATA URL", dataUrl, "DATA URL");
    console.log("ENVIRONMENT", import.meta.env, "ENVIRONMENT");

    const response = await fetch(`${dataUrl}assets/asset`, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",

      body: JSON.stringify({
        ticker_code: assetTicker,
        user_id: userId,
        is_crypto: isCrypto,
        refresh_token: refreshToken,
        access_token: accessToken,
      }),
    });

    // this needs to be cleaned up

    if (!response.ok || response.status !== 200) {
      setIsError(true);
      setIsSuccess(false);
      throw new Error(`HTTP error! status: ${response.status}`);
      setIsLoading(false);
      return "error";
    }

    const data = (await response.json()) as object;

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

    return "success";

    // TODO: redirect to dashboard page
  } catch (error) {
    console.error("Error logging in", error);
    // logoutUser();
    setIsLoading(false);
    setIsError(true);
    setIsSuccess(false);
  }
};
