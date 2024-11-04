import { defineConfig, loadEnv, UserConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

// https://vitejs.dev/config/
export default ({ mode }: { mode: string }): UserConfig => {
  // Load environment variables based on the current mode
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-call, @typescript-eslint/no-unsafe-member-access
  const env = loadEnv(mode, process.cwd());

  // Merge the loaded environment variables with process.env
  // eslint-disable-next-line @typescript-eslint/no-unsafe-assignment, @typescript-eslint/no-unsafe-member-access
  process.env = { ...process.env, ...env };

  // eslint-disable-next-line @typescript-eslint/no-unsafe-call
  return defineConfig({
    // eslint-disable-next-line @typescript-eslint/no-unsafe-call
    plugins: [react()],
    server: {
      // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
      port: Number(process.env.PORT) || 5173, // Ensure the port is a number
    },
  });
};``