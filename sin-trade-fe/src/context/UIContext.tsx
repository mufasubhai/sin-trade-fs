import React, { createContext, useState } from "react";
import { NavigateFunction, useNavigate } from "react-router";

interface UIContextType {
  isLoading: boolean;
  isError: boolean;
  isSuccess: boolean;
  setIsLoading: (isLoading: boolean) => void;
  setIsError: (isError: boolean) => void;
  setIsSuccess: (isSuccess: boolean) => void;
  // useNavigate: () => void;
  navigate: NavigateFunction;
}

export const UIContext = createContext<UIContextType | undefined>(
  undefined
);

export function UIProvider({ children }: { children: React.ReactNode }) {
  const [isLoading, setIsLoading] = useState(false);
  const [isError, setIsError] = useState(false);
  const [isSuccess, setIsSuccess] = useState(false);
  const navigate = useNavigate();
  
  return (
    <UIContext.Provider
      value={{
        isLoading,
        navigate,
        isError,
        isSuccess,
        setIsLoading,
        setIsError,
        setIsSuccess,
      

      }}
    >
      {children}
    </UIContext.Provider>
  );
}

// Custom hook for using the auth context
