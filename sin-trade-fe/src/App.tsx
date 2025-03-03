import { useEffect } from "react";
import { useAuth } from "./context/useAuth";
import { useNavigate } from "react-router";

function App() {
  const { isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    if (isAuthenticated) {
      void navigate("/dashboard");
    } else {
      void navigate("/login");
    }
  }, [isAuthenticated, navigate]);
  // here we just have a self closing placeholder div.
  // we don't actually ever want to render this page for the time being,
  // this may change in the future.
  return <div className="flex flex-row" />;
}

export default App;
