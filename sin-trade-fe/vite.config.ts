// /* eslint-disable @typescript-eslint/no-unsafe-assignment */
// /* eslint-disable @typescript-eslint/no-unsafe-call */
// /* eslint-disable @typescript-eslint/no-unsafe-member-access */

/// <reference types="vitest" />
import { defineConfig, loadEnv, UserConfig } from "vite";
import react from "@vitejs/plugin-react-swc";
import tailwindcss from "@tailwindcss/vite";

// https://vitejs.dev/config/
export default ({ mode }: { mode: string }): UserConfig => {
  const env = loadEnv(mode, process.cwd());

  process.env = { ...process.env, ...env };

  const isDev = process.env.NODE_ENV === "development";
  const defaultPort = isDev ? 5173 : 4173;
  const port = Number(process.env.PORT) || defaultPort;

  return defineConfig({
    // eslint-disable-next-line @typescript-eslint/no-unsafe-call
    plugins: [react(), tailwindcss()],
    build: {
      sourcemap: isDev,
      minify: !isDev,
    },
    server: {
      port: port,
      host: true,
    },
    preview: {
      port: port,
      host: "0.0.0.0",
    },
    css: {
      devSourcemap: isDev,
    },
    optimizeDeps: {
      include: ["react", "react-dom"],
    },
    test: {
      include: ["src/**/*.test.tsx", "src/**/*.spec.tsx"],
      environment: "jsdom",
    },
  });
};
