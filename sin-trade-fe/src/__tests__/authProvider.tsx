import { render } from "@testing-library/react";
import { MemoryRouter } from "react-router";
import { AuthProvider } from "../context/AuthContext";
import { UIProvider } from "../context/UIContext";

export function renderWithAuth(ui: React.ReactElement) {
  return render(
    <AuthProvider>
      <MemoryRouter>
        <UIProvider>{ui}</UIProvider>
      </MemoryRouter>
    </AuthProvider>
  );
}
