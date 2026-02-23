import { describe, it, expect, vi, beforeEach, afterEach } from "vitest";
import { login, signup } from "../../api/Auth";

global.fetch = vi.fn();

describe("Auth API", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  afterEach(() => {
    vi.resetAllMocks();
  });

  describe("login", () => {
    it("should login successfully", async () => {
      const mockUser = {
        access_token: "test_token",
        refresh_token: "test_refresh",
        active_assets: {},
        avatar_url: null,
        created_at: "2024-01-01",
        email: "test@example.com",
        email_confirmed_at: null,
        first_name: "Test",
        last_name: "User",
        updated_at: "2024-01-01",
        user_id: 1,
        username: "testuser",
        website: null,
      };

      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve(mockUser),
      });

      const setIsLoading = vi.fn();
      const loginUser = vi.fn();
      const logoutUser = vi.fn();
      const setIsError = vi.fn();
      const setIsSuccess = vi.fn();

      await login({
        email: "test@example.com",
        password: "password",
        setIsLoading,
        loginUser,
        logoutUser,
        setIsError,
        setIsSuccess,
      });

      expect(setIsLoading).toHaveBeenCalledWith(true);
      expect(setIsError).toHaveBeenCalledWith(false);
      expect(setIsSuccess).toHaveBeenCalledWith(true);
      expect(loginUser).toHaveBeenCalled();
    });

    it("should handle login error", async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 401,
      });

      const setIsLoading = vi.fn();
      const loginUser = vi.fn();
      const logoutUser = vi.fn();
      const setIsError = vi.fn();
      const setIsSuccess = vi.fn();

      await login({
        email: "test@example.com",
        password: "wrongpassword",
        setIsLoading,
        loginUser,
        logoutUser,
        setIsError,
        setIsSuccess,
      });

      expect(setIsError).toHaveBeenCalledWith(true);
      expect(setIsSuccess).toHaveBeenCalledWith(false);
      expect(logoutUser).toHaveBeenCalled();
    });

    it("should handle network error", async () => {
      (global.fetch as any).mockRejectedValueOnce(new Error("Network error"));

      const setIsLoading = vi.fn();
      const loginUser = vi.fn();
      const logoutUser = vi.fn();
      const setIsError = vi.fn();
      const setIsSuccess = vi.fn();

      await login({
        email: "test@example.com",
        password: "password",
        setIsLoading,
        loginUser,
        logoutUser,
        setIsError,
        setIsSuccess,
      });

      expect(setIsError).toHaveBeenCalledWith(true);
      expect(setIsSuccess).toHaveBeenCalledWith(false);
    });
  });

  describe("signup", () => {
    it("should signup successfully", async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({}),
      });

      const setIsLoading = vi.fn();
      const loginUser = vi.fn();
      const logoutUser = vi.fn();
      const setIsError = vi.fn();
      const setIsSuccess = vi.fn();

      await signup({
        email: "test@example.com",
        password: "password123",
        firstName: "John",
        lastName: "Doe",
        username: "johndoe",
        setIsLoading,
        loginUser,
        logoutUser,
        setIsError,
        setIsSuccess,
      });

      expect(setIsLoading).toHaveBeenCalledWith(true);
      expect(setIsError).toHaveBeenCalledWith(false);
      expect(setIsSuccess).toHaveBeenCalledWith(true);
    });

    it("should signup with optional fields", async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: () => Promise.resolve({}),
      });

      const setIsLoading = vi.fn();
      const loginUser = vi.fn();
      const logoutUser = vi.fn();
      const setIsError = vi.fn();
      const setIsSuccess = vi.fn();

      await signup({
        email: "test@example.com",
        password: "password123",
        firstName: "John",
        lastName: "Doe",
        username: "johndoe",
        avatarUrl: "https://example.com/avatar.png",
        setIsLoading,
        loginUser,
        logoutUser,
        setIsError,
        setIsSuccess,
      });

      expect(setIsSuccess).toHaveBeenCalledWith(true);
    });

    it("should handle signup error", async () => {
      (global.fetch as any).mockResolvedValueOnce({
        ok: false,
        status: 400,
      });

      const setIsLoading = vi.fn();
      const loginUser = vi.fn();
      const logoutUser = vi.fn();
      const setIsError = vi.fn();
      const setIsSuccess = vi.fn();

      await signup({
        email: "test@example.com",
        password: "password123",
        firstName: "John",
        lastName: "Doe",
        setIsLoading,
        loginUser,
        logoutUser,
        setIsError,
        setIsSuccess,
      });

      expect(setIsError).toHaveBeenCalledWith(true);
      expect(setIsSuccess).toHaveBeenCalledWith(false);
      expect(logoutUser).toHaveBeenCalled();
    });

    it("should handle network error", async () => {
      (global.fetch as any).mockRejectedValueOnce(new Error("Network error"));

      const setIsLoading = vi.fn();
      const loginUser = vi.fn();
      const logoutUser = vi.fn();
      const setIsError = vi.fn();
      const setIsSuccess = vi.fn();

      await signup({
        email: "test@example.com",
        password: "password123",
        firstName: "John",
        lastName: "Doe",
        setIsLoading,
        loginUser,
        logoutUser,
        setIsError,
        setIsSuccess,
      });

      expect(setIsError).toHaveBeenCalledWith(true);
      expect(setIsSuccess).toHaveBeenCalledWith(false);
    });
  });
});
