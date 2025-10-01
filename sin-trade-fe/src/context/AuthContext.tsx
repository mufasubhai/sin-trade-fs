import React, { createContext, useState, useEffect } from "react";
import { Asset, UserResponse } from "../interfaces/UserInterface";
import { dataUrl } from "../api/AuthConfig";
import { ListAssetResponseSchema } from "../interfaces/ListAssetResponse";

// what is missing is a function to disable tokens after a certain amount of time.
// we should save the date of creation of the tokens and disable them after a certain amount of time.
interface AuthContextType {
  accessToken: string | null;
  refreshToken: string | null;
  tokenCreationDate: Date | null;
  user: UserResponse | null;
  assets: Record<string, Asset>;
  fetchAssets: () => Promise<void>;
  addAssetToDB: (
    assetTicker: string,
    userId: number,
    isCrypto: boolean,
    refreshToken: string,
    accessToken: string
  ) => Promise<Response | undefined>;
  setAssets: (assets: Record<string, Asset>) => void; // Repla
  //ce 'any' with your user type
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

  useEffect(() => {
    const initializeAssets = () => {
      const storedUser = localStorage.getItem("user");
      if (!storedUser) return;

      try {
        const parsedUser = JSON.parse(storedUser) as UserResponse;
        setUser(parsedUser);
      } catch (error) {
        console.error("Error parsing stored user:", error);
      }

      const accessToken = localStorage.getItem("access_token");
      const tokenCreationDate = localStorage.getItem("token_creation_date")
        ? new Date(localStorage.getItem("token_creation_date")!)
        : null;
      const refreshToken = localStorage.getItem("refresh_token");

      setAccessToken(accessToken);
      setTokenCreationDate(tokenCreationDate);
      setRefreshToken(refreshToken);
    };

    initializeAssets();
  }, []);

  const [assets, setAssets] = useState<Record<string, Asset>>({});
  const [accessToken, setAccessToken] = useState<string | null>(null);
  const [tokenCreationDate, setTokenCreationDate] = useState<Date | null>(null);
  const [refreshToken, setRefreshToken] = useState<string | null>(null);
  const [user, setUser] = useState<UserResponse | null>(null);

  const fetchAssets = async () => {
    if (!user) return;
    try {
      const response = await fetch(`${dataUrl}assets/assets/${user.userId}`, {
        headers: {
          "Content-Type": "application/json",
        },
        method: "GET",
      });
      const data = (await response.json()) as object;

      const listAssetResponse = ListAssetResponseSchema.parse(data);

      // looks like everything is good here, but for some reason the setAssets is not updating the state/UI.
      // confirm shape coming back is good. and that we are handling the update function correctly.
      if (listAssetResponse.status === 200) {
        const newAssets = listAssetResponse.data.reduce((acc, asset) => {
          acc[asset.tickerName] = asset;
          return acc;
        }, {} as Record<string, Asset>);

        console.log("NEW ASSETS", newAssets, "NEW ASSETS");

        setAssets(newAssets);
      }
      console.log("RESPONSE", response, "RESPONSE");
      // here we need ot set the assets.
    } catch (error) {
      console.error("Error fetching assets", error);
    }
  };
  useEffect(() => {
    if (user) {
      void fetchAssets();
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user]);

  const addAssetToDB = async (
    assetTicker: string,
    userId: number,
    isCrypto: boolean,
    refreshToken: string,
    accessToken: string
  ) => {
    try {
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
      return response;
    } catch (error) {
      console.error("Error adding asset to database", error);
    }
  };

  // this likely isn't a good enouhg check, btu it's a start. We need verification with supabase

  const loginUser = (userData: UserResponse) => {
    localStorage.setItem("access_token", userData.accessToken);
    localStorage.setItem("refresh_token", userData.refreshToken);
    localStorage.setItem("user", JSON.stringify(userData));
    localStorage.setItem("token_creation_date", new Date().toISOString());
    setTokenCreationDate(new Date());
    setAccessToken(userData.accessToken);
    setRefreshToken(userData.refreshToken);
    setUser(userData);
    setIsAuthenticated(true);
  };

  const logoutUser = () => {
    localStorage.removeItem("user");
    localStorage.removeItem("access_token");
    localStorage.removeItem("refresh_token");
    localStorage.removeItem("token_creation_date");
    setTokenCreationDate(null);
    setAccessToken(null);
    setAssets({});
    setRefreshToken(null);
    setUser(null);
    setIsAuthenticated(false);
  };

  return (
    <AuthContext.Provider
      value={{
        accessToken,
        addAssetToDB,
        assets,
        setAssets,
        refreshToken,
        user,
        fetchAssets,
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
