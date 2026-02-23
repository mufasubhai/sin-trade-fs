import { describe, it, expect, vi, afterEach } from "vitest";
import { cleanup, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import Register from "../../pages/auth/Register";

vi.mock("../../api/Auth", () => ({
  signup: vi.fn(),
}));

vi.mock("../../context/useAuth", () => ({
  useAuth: () => ({
    loginUser: vi.fn(),
    logoutUser: vi.fn(),
  }),
}));

vi.mock("../../context/useUI", () => ({
  useUI: () => ({
    isLoading: false,
    isError: false,
    isSuccess: false,
    setIsLoading: vi.fn(),
    setIsError: vi.fn(),
    setIsSuccess: vi.fn(),
    navigate: vi.fn().mockReturnValue(() => {}),
  }),
}));

describe("Register Page", () => {
  afterEach(() => {
    cleanup();
  });

  it("renders all fields", () => {
    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    expect(screen.getByLabelText(/email/i)).toBeTruthy();
    expect(screen.getByLabelText(/first name/i)).toBeTruthy();
    expect(screen.getByLabelText(/last name/i)).toBeTruthy();
    expect(screen.getByLabelText(/username/i)).toBeTruthy();
    expect(screen.getByLabelText(/avatar url/i)).toBeTruthy();
    expect(screen.getByLabelText(/^password$/i)).toBeTruthy();
    expect(screen.getByLabelText(/confirm password/i)).toBeTruthy();
  });

  it("button disabled when required fields are empty", () => {
    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    const registerButton = screen.getByRole("button", { name: /register/i });
    expect(registerButton.hasAttribute("disabled")).toBe(true);
  });

  it("button enabled when required fields are filled", async () => {
    const user = userEvent.setup();
    
    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    await user.type(screen.getByLabelText(/email/i), "test@example.com");
    await user.type(screen.getByLabelText(/first name/i), "John");
    await user.type(screen.getByLabelText(/last name/i), "Doe");
    await user.type(screen.getByLabelText(/^password$/i), "password123");
    await user.type(screen.getByLabelText(/confirm password/i), "password123");

    const registerButton = screen.getByRole("button", { name: /register/i });
    expect(registerButton.hasAttribute("disabled")).toBe(false);
  });

  it("shows password mismatch error", async () => {
    const user = userEvent.setup();
    
    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    await user.type(screen.getByLabelText(/email/i), "test@example.com");
    await user.type(screen.getByLabelText(/first name/i), "John");
    await user.type(screen.getByLabelText(/last name/i), "Doe");
    await user.type(screen.getByLabelText(/^password$/i), "password123");
    await user.type(screen.getByLabelText(/confirm password/i), "differentpassword");

    const registerButton = screen.getByRole("button", { name: /register/i });
    await user.click(registerButton);

    expect(screen.getByText(/passwords do not match/i)).toBeTruthy();
  });

  it("shows back to login button", () => {
    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    expect(screen.getByRole("button", { name: /back to login/i })).toBeTruthy();
  });

  it("renders register button", () => {
    render(
      <MemoryRouter>
        <Register />
      </MemoryRouter>
    );

    expect(screen.getByRole("button", { name: /register/i })).toBeTruthy();
  });
});
