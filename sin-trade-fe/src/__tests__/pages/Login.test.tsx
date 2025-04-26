import { describe, it, expect, afterEach, vi } from "vitest";
import { cleanup, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { waitFor } from "@testing-library/react";
import { UserResponse } from "../../interfaces/UserInterface";
// import { MemoryRouter } from "react-router"
vi.mock("../../api/Auth", () => ({
  login: vi
    .fn()
    .mockImplementation(
      ({
        setIsError,
        setIsSuccess,
        email,
        password,
        loginUser,
      }: {
        setIsError: (isError: boolean) => void;
        setIsSuccess: (isSuccess: boolean) => void;
        email: string;
        password: string;
        loginUser: (userData: UserResponse) => void;
      }) => {
        if (email === "success@gmail.com" && password === "success") {
          setIsError(false);
          setIsSuccess(true);
          loginUser({
            email: "success@example.com",
            accessToken: "fake_access_token",
            refreshToken: "fake_refresh_token",
            activeAssets: {},
            avatarUrl: null,
            createdAt: new Date(),
            emailConfirmedAt: null,
            firstName: "success",
            lastName: "success",
            updatedAt: new Date(),
            userId: 1,
            username: "success",
            website: "success",
          });

          return "success";
        } else if (
          email === "aapodaca@gmail.com" &&
          password === "badpassword"
        ) {
          setIsError(true);
          setIsSuccess(false);
        }
      }
    ),
}));

describe("Login", () => {
  afterEach(() => {
    cleanup();
    vi.resetModules();
    vi.clearAllMocks();
  });

  it("should show error on failed login", async () => {
    // Mock useUI for this test
    vi.doMock("../../context/useUI", () => ({
      useUI: () => ({
        setIsLoading: vi.fn(),
        setIsError: vi.fn(),
        setIsSuccess: vi.fn(),
        navigate: vi.fn(),
        isLoading: false,
        isError: true, // Simulate error state
        isSuccess: false,
      }),
    }));

    // Re-import after mocking
    const { renderWithAuth } = await import("../authProvider");
    const Login = (await import("../../pages/auth/Login")).default;

    renderWithAuth(<Login />);

    const email = screen.getByLabelText("Email");
    const password = screen.getByLabelText("Password");
    const button = screen.queryByText("Login");

    expect(email).not.toBeNull();
    expect(password).not.toBeNull();
    expect(button).not.toBeNull();
  });

  it("should cause error if with bad login", async () => {
    const { renderWithAuth } = await import("../authProvider");
    const Login = (await import("../../pages/auth/Login")).default;
    renderWithAuth(<Login />);

    const email = screen.getByLabelText("Email");
    const password = screen.getByLabelText("Password");
    const button = screen.queryByText("Login");

    expect(email).not.toBeNull();
    expect(password).not.toBeNull();
    expect(button).not.toBeNull();

    await userEvent.type(email, "aapodaca@gmail.com");
    await userEvent.type(password, "badpassword");

    expect((email as HTMLInputElement).value).toBe("aapodaca@gmail.com");
    expect((password as HTMLInputElement).value).toBe("badpassword");

    await userEvent.click(button!);

    await waitFor(() => {
      const error = screen.getByText("Invalid credentials. Please try again.");
      expect(error).not.toBeNull();
    });
  });

  it("should successfull navigate to dashboard if login is successful", async () => {
    const mockNavigate = vi.fn();
    vi.doMock("../../context/useUI", () => ({
      useUI: () => ({
        setIsLoading: vi.fn(),
        setIsError: vi.fn(),
        setIsSuccess: vi.fn(),
        navigate: mockNavigate,
        isLoading: false,
        isError: false,
        isSuccess: true, // Simulate success state
      }),
    }));

    // Re-import after mocking
    const { renderWithAuth } = await import("../authProvider");
    const Login = (await import("../../pages/auth/Login")).default;

    renderWithAuth(<Login />);
    const email = screen.getByLabelText("Email");
    const password = screen.getByLabelText("Password");
    const button = screen.queryByText("Login");

    expect(email).not.toBeNull();
    expect(password).not.toBeNull();
    expect(button).not.toBeNull();

    await userEvent.type(email, "success@gmail.com");
    await userEvent.type(password, "success");

    await userEvent.click(button!);
    await waitFor(
      () => {
        expect(mockNavigate).toHaveBeenCalledWith("/dashboard");
      },
      { timeout: 5000 }
    );
  });
});
