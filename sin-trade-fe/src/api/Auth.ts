import { dataUrl, DataResponse } from "./AuthConfig";





export const login = async (
  email: string,
  password: string,
  setIsLoading: (isLoading: boolean) => void,
  setIsError: (isError: boolean) => void
) => {
  setIsLoading(true);
  try {
    const response = await fetch(`${dataUrl}auth/login`, {
      headers: {
        "Content-Type": "application/json",
      },
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
      setIsError(true);
      setIsLoading(false);
    }
    const data = (await response.json()) as DataResponse;
    setIsLoading(false);
    setIsError(false);

    

    // TODO: store token in local storage
    // TODO: store user data in local storage
    // TODO: store token in state
    // TODO: store user data in state

    
    // TODO: redirect to dashboard page
    console.log(data);
    return data;
  } catch (error) {
    console.error("Error logging in", error);
    setIsLoading(false);
    setIsError(true);
    throw new Error("Failed to log in");
  }
};
