import { UserResponse, UserResponseSchema } from "../interfaces/UserInterface";
import { dataUrl } from "./AuthConfig";

export const login = async ({
  email,
  password,
  setIsLoading,
  loginUser,
  logoutUser,
  setIsError,
  setIsSuccess,
}: {
  email: string;
  password: string;
  setIsLoading: (isLoading: boolean) => void;
  loginUser: (userData: UserResponse) => void;
  logoutUser: () => void;
  setIsError: (isError: boolean) => void;
  setIsSuccess: (isSuccess: boolean) => void;
}) => {
  setIsLoading(true);
  try {
    const response = await fetch(`${dataUrl}auth/login`, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok || response.status !== 200) {
      setIsError(true);
      setIsSuccess(false);
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = (await response.json()) as object;
    const user = UserResponseSchema.parse(data);

    setIsError(false);
    setIsSuccess(true);
    loginUser(user);

    return "success";
  } catch (error) {
    console.error("Error logging in", error);
    logoutUser();
    setIsLoading(false);
    setIsError(true);
    setIsSuccess(false);
  }
};

export const signup = async ({
  email,
  password,
  firstName,
  lastName,
  username,
  avatarUrl,
  setIsLoading,
  
  logoutUser,
  setIsError,
  setIsSuccess,
}: {
  email: string;
  password: string;
  firstName?: string;
  lastName?: string;
  username?: string;
  avatarUrl?: string;
  setIsLoading: (isLoading: boolean) => void;
  loginUser: (userData: UserResponse) => void;
  logoutUser: () => void;
  setIsError: (isError: boolean) => void;
  setIsSuccess: (isSuccess: boolean) => void;
}) => {
  setIsLoading(true);
  try {
    const response = await fetch(`${dataUrl}auth/signup`, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({
        email,
        password,
        first_name: firstName,
        last_name: lastName,
        username,
        avatar_url: avatarUrl,
      }),
    });

    if (!response.ok || response.status !== 200) {
      setIsError(true);
      setIsSuccess(false);
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    setIsError(false);
    setIsSuccess(true);

    return "success";
  } catch (error) {
    console.error("Error signing up", error);
    logoutUser();
    setIsLoading(false);
    setIsError(true);
    setIsSuccess(false);
  }
};
