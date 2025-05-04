import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss(),],
  
  // Configuración para desarrollo - proxy para API requests
  server: {
    port: 5173,
    proxy: {
      '/api': {
        target: 'http://localhost:5000',
        changeOrigin: true,
        secure: false,
      }
    }
  },
  
  // Configuración para producción - output a folder estático de Flask
  build: {
    outDir: 'dist',
    emptyOutDir: true,
    sourcemap: true,
    assetsDir: 'assets',
    // Asegura que las rutas sean relativas
    assetsInlineLimit: 0,
    rollupOptions: {
      output: {
        manualChunks: undefined,
      },
    },
    chunkSizeWarningLimit: 1000
  },
  
  resolve: {
    alias: {
      '@': '/src',
    },
  },
})
