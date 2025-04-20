import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import { BrowserRouter, Routes, Route } from "react-router";
import { AuthProvider } from "./context/AuthContext";
import Register from "./pages/auth/Register.tsx";
import Login from "./pages/auth/Login.tsx";
import App from "./App.tsx";
import "./index.css";
import { ProtectedRoute } from "./components/ProtectedRoute.tsx";
import { UnprotectedRoute } from "./components/UnprotectedRoute.tsx";
import Dashboard from "./pages/auth/Dashboard.tsx";
import { UIProvider } from "./context/UIContext.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <AuthProvider>
      <BrowserRouter>
        <UIProvider>
          <Routes>
            <Route
              path="/"
              element={
                <UnprotectedRoute>
                  <App />
                </UnprotectedRoute>
              }
            />
            <Route
              path="login"
              element={
                <UnprotectedRoute>
                  <Login />
                </UnprotectedRoute>
              }
            />
            <Route
              path="register"
              element={
                <UnprotectedRoute>
                  <Register />
                </UnprotectedRoute>
              }
            />

            <Route
              path="/dashboard"
              element={
                <ProtectedRoute>
                  <Dashboard />
                </ProtectedRoute>
              }
            />
          </Routes>
        </UIProvider>
      </BrowserRouter>
    </AuthProvider>
  </StrictMode>
);
