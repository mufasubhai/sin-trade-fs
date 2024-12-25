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
    build: {
      sourcemap: true,
      minify: false, // During debugging, this can help
    },
    server: {
      port: Number(process.env.PORT) || 5173,
    },
    css: {
      devSourcemap: true
    },
    optimizeDeps: {
      include: ['react', 'react-dom']
    }
  });
};
