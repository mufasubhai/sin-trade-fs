import { UserResponse } from "../interfaces/UserInterface";
import { dataUrl } from "./AuthConfig";

export const login = async ({
  email,
  password,
  setIsLoading,
  loginUser,
  logoutUser,
  setIsError,
  setIsSuccess
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

    console.log(response);
    if (!response.ok || response.status !== 200) {
      setIsError(true);
      setIsSuccess(false);
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    // here we need to redirect to the dashboard page,
    // we also need to store the token and user data in local storage
    // we also need to store the token and user data in state
    // we also need to redirect to the dashboard page
    const data = (await response.json()) as UserResponse;
    setIsError(false);
    setIsSuccess(true);
    loginUser(data);

    console.log(data);
    
    return "success";
    
    // TODO: redirect to dashboard page
  } catch (error) {
    console.error("Error logging in", error);
    logoutUser();
    setIsLoading(false);
    setIsError(true);
    setIsSuccess(false);
  }
  };
