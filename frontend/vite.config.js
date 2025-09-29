import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173, // ya jo bhi port tu use kar raha hai
    open: true, // <-- automatically browser khulega
  },
});
