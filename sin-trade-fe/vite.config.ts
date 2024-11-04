/* eslint-disable @typescript-eslint/no-unsafe-assignment */
/* eslint-disable @typescript-eslint/no-unsafe-call */
/* eslint-disable @typescript-eslint/no-unsafe-member-access */
import { defineConfig, loadEnv, UserConfig } from 'vite';
import react from '@vitejs/plugin-react-swc';

// https://vitejs.dev/config/
export default ({ mode }: { mode: string }): UserConfig => {


  const env = loadEnv(mode, process.cwd());



  process.env = { ...process.env, ...env };


  return defineConfig({

    plugins: [react()],
    server: {
      port: Number(process.env.PORT) || 5173, // Ensure the port is a number
    },
    preview: {
      port: Number(process.env.PORT) || 5173, // Ensure the port is a number for preview mode
    },
  });
};