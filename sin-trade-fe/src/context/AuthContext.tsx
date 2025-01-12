import React, { createContext, useState } from "react";
import { User, UserResponse } from "../interfaces/UserInterface";


interface AuthContextType {
  accessToken: string | null;
  refreshToken: string | null;
  user: User | null; // Replace 'any' with your user type
  loginUser: (userData: UserResponse) => void;
  logoutUser: () => void;
  isAuthenticated: boolean;

}

export const AuthContext = createContext<AuthContextType | undefined>(
  undefined
);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [accessToken, setAccessToken] = useState<string | null>(
    localStorage.getItem("access_token")
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

  const [isAuthenticated, setIsAuthenticated] = useState(false);

  const loginUser = (userData: UserResponse) => {
    localStorage.setItem("access_token", userData.access_token);
    localStorage.setItem("refresh_token", userData.refresh_token);
    localStorage.setItem("user", JSON.stringify(userData.user));
    setAccessToken(userData.access_token);
    setRefreshToken(userData.refresh_token);
    setUser(userData.user);
    setIsAuthenticated(true);
  };

  const logoutUser = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
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
        logoutUser,
        isAuthenticated,
      

      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for using the auth context
