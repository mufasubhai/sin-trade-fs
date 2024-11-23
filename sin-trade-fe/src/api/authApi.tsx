import type { AuthResponse } from "../context/authContext";

const logUserIn = async ({
  userName,
  pass,
}: {
  userName: string;
  pass: string;
}): Promise<AuthResponse | null> => {
  // Implement login logic here
  return null; // Placeholder return
};

const registerUser = async ({
  userName,
  pass,
  pass2,
}: {
  userName: string;
  pass: string;
  pass2: string;
}): Promise<AuthResponse | null> => {
  // Implement registration logic here
  return null; // Placeholder return
};

export { logUserIn, registerUser };
