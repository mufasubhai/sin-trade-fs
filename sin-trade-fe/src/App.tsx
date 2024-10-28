import { useState } from "react";
import reactLogo from "./assets/react.svg";
import viteLogo from "/vite.svg";
import "./App.css";

interface DataResponse {
  status: string;
  data: string;
}

function App() {
  const [count, setCount] = useState(0);
  const dataUrl: string = import.meta.env.VITE_BACKEND_URL as string;

  const fetchFromDataUrl = async () => {
    try {
      const response = await fetch(dataUrl);

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: DataResponse = await response.json() as DataResponse;

      console.log(data);
    } catch (error) {
      console.error("error fetching data", error);
    }
  };

  return (
    <>
      <div>
        <a href="https://vitejs.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button
          onClick={() => {
            setCount((count) => count + 1);
            fetchFromDataUrl().catch((error) => console.log(error));
          }}
        >
          count is {count}
        </button>
        <p>
          Edit <code>src/App.tsx</code> and save to test HMR
        </p>
      </div>
      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  );
}

export default App;
