import { createContext, useState, ReactNode } from 'react';
import { logUserIn } from "../api/authApi";


interface AuthContextType {
    authentication: AuthResponse | null;
    login: ({ userName, pass } : { userName: string; pass: string }) => AuthResponse;
    logout: () => void;
    token: string | null;

}

interface AuthResponse {
    token: string | null;
    userId: number | null;
    status: Status; 
}

enum Status {
    error,
    success,
    expired,
}
const AuthContext = createContext<AuthContextType | undefined>(undefined);

const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [authentication, setAuthentication] = useState<AuthResponse | null>(
    null
  );
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [isPendingVerify, setIsPendingVerify] = useState(false);

  const login = async ({ userName, pass }: { userName: string; pass: string }) : Promise<void>=> {

    try {

        const authResponse = await logUserIn({userName, pass});
         
        
        
            setIsAuthenticated(true);
            setAuthentication(authResponse);


    } catch (e) {
        // throw()
        setIsAuthenticated(false);
        setAuthentication(null);
    //   });

  };
} 

  const logout = async () : Promise<void> => {
    setIsAuthenticated(false);
    setAuthentication(null);
  };
  

  const register = async ({
    username,
    pass,
    pass2,
  }: {
    userName: string;
    pass: string;
    pass2: string;
  }) : Promise<void> => {




  };

  
  return (
    <AuthContext.Provider
      value={{
        isAuthenticated,
        isPendingVerify,
        login,
        register,
        logout,
        authentication,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};


export { AuthProvider, AuthContext  };
export type {AuthResponse};