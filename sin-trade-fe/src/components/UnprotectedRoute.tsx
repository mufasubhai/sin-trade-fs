import { ReactNode } from 'react';
import {  Navigate, useLocation } from 'react-router';
import { useAuth } from '../context/useAuth';

export function UnprotectedRoute({ children }: { children: ReactNode }) {
  const { isAuthenticated } = useAuth();
  const location = useLocation();

  if (isAuthenticated) {
    // Redirect to login while saving the attempted location
    return <Navigate to="/dashboard" state={{ from: location }} replace />;
  }

  return <>{children}</>;
} 