import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  base: "/higher-school-of-chess-alik",
  plugins: [react()],
  server: {
    proxy: {
      '/chess': {
        target: 'http://127.0.0.1:8000', // Адрес вашего FastAPI сервера
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/chess/, '/chess'),
      },
    },
  },
});