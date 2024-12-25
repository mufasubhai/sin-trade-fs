import React, { createContext, useState } from 'react';
import { User, UserResponse } from '../interfaces/UserInterface';

interface AuthContextType {
  token: string | null;
  user: User | null;  // Replace 'any' with your user type
  loginUser: (userData: UserResponse) => void;
  logoutUser: () => void;
}

export const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'));
  const [user, setUser] = useState<User | null>(() => {
    const storedUser = localStorage.getItem('user');
    if (!storedUser) return null;
    try {
      const parsedUser = JSON.parse(storedUser) as User;
      return parsedUser;
    } catch {
      return null;
    }
  });

  const loginUser = (userData: UserResponse) => {
    localStorage.setItem('token', userData.access_token);
    localStorage.setItem('user', JSON.stringify(userData.user));
    setToken(userData.access_token);
    setUser(userData.user);
  };

  const logoutUser = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ token, user, loginUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
}

// Custom hook for using the auth context
