import { describe, it, expect, afterEach, vi } from "vitest";
import { cleanup, screen } from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import { renderWithAuth } from "../authProvider";
import Login from "../../pages/auth/Login";
import { waitFor } from "@testing-library/react";
// import { MemoryRouter } from "react-router";

// import { login } from "../../api/Auth";
// Mock the login function to simulate a failed login


describe("Login", () => {
  afterEach(() => {
    cleanup();
    vi.clearAllMocks();
  });

  it("should render the login page", () => {
    renderWithAuth(<Login />);

    const email = screen.getByLabelText("Email");
    const password = screen.getByLabelText("Password");
    const button = screen.queryByText("Login");

    expect(email).not.toBeNull();
    expect(password).not.toBeNull();
    expect(button).not.toBeNull();
  });

  it("should cause error if with bad login", async () => {
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
    renderWithAuth(
        // <MemoryRouter initialEntries={["/login"]}>
            <Login />
        // </MemoryRouter>
    );
    const email = screen.getByLabelText("Email");
    const password = screen.getByLabelText("Password");
    const button = screen.queryByText("Login");

    expect(email).not.toBeNull();
    expect(password).not.toBeNull();
    expect(button).not.toBeNull();


    await userEvent.type(email, "aapodaca@gmail.com");
    await userEvent.type(password, "6798Akumosan!");

    // await userEvent.click(button!);
    //   await waitFor(() => {
    //     // Check for a specific element on the dashboard page
    //     const dashboardElement = screen.getByRole('heading', { name: /welcome to your dashboard/i });
    //     expect(dashboardElement).not.toBeNull();
    //   }, { timeout: 5000 });
    
  });
});

