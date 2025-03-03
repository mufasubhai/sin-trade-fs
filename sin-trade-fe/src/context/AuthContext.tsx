import React, { createContext, useState } from "react";
import { User, UserResponse } from "../interfaces/UserInterface";

// what is missing is a function to disable tokens after a certain amount of time.
// we should save the date of creation of the tokens and disable them after a certain amount of time.
interface AuthContextType {
  accessToken: string | null;
  refreshToken: string | null;
  tokenCreationDate: Date | null;
  user: User | null; // Replace 'any' with your user type
  loginUser: (userData: UserResponse) => void;
  logoutUser: () => void;
  isAuthenticated: boolean;
}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [isAuthenticated, setIsAuthenticated] = useState(
    localStorage.getItem("access_token") !== null
  );
  const [accessToken, setAccessToken] = useState<string | null>(
    localStorage.getItem("access_token")
  );

  const [tokenCreationDate, setTokenCreationDate] = useState<Date | null>(
    localStorage.getItem("token_creation_date")
      ? new Date(localStorage.getItem("token_creation_date")!)
      : null
  );

  const [refreshToken, setRefreshToken] = useState<string | null>(
    localStorage.getItem("refresh_token")
  );
  const [user, setUser] = useState<User | null>(() => {
    const storedUser = localStorage.getItem("user");
    if (!storedUser) return null;
    try {
      const parsedUser = JSON.parse(storedUser) as User;
      return parsedUser;
    } catch {
      return null;
    }
  });
  // this likely isn't a good enouhg check, btu it's a start. We need verification with supabase

  const loginUser = (userData: UserResponse) => {
    localStorage.setItem("access_token", userData.access_token);
    localStorage.setItem("refresh_token", userData.refresh_token);
    localStorage.setItem("user", JSON.stringify(userData.user));
    localStorage.setItem("token_creation_date", new Date().toISOString());
    setTokenCreationDate(new Date());
    setAccessToken(userData.access_token);
    setRefreshToken(userData.refresh_token);
    setUser(userData.user);
    setIsAuthenticated(true);
  };

  const logoutUser = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("token_creation_date");
    setTokenCreationDate(null);
    setAccessToken(null);
    setRefreshToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{
        accessToken,
        refreshToken,
        user,
        loginUser,
        tokenCreationDate,
        logoutUser,
        isAuthenticated,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for using the auth context
