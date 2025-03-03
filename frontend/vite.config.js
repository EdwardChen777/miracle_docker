import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

export default defineConfig({
  server: {
    proxy: {
      "/api": {
        target: "http://localhost:8000",  
        changeOrigin: true,
        secure: false,
        configure: (proxy, options) => {
          proxy.on("error", (err, _req, _res) => {
            console.log("Proxy Error:", err);
          });
          proxy.on("proxyReq", (proxyReq, req, _res) => {
            console.log("Request sent to backend:", req.method, req.url);
            console.log("Final proxied request path:", proxyReq.path); // Logs final proxied URL
          });
          proxy.on("proxyRes", (proxyRes, req, _res) => {
            console.log("Response received from backend:", proxyRes.statusCode, req.url);
          });
        },
      },
    },
  },
  plugins: [react(), tailwindcss()],
});
