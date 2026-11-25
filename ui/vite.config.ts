import { defineConfig } from "vitest/config";
import react from "@vitejs/plugin-react";

// Esquema copiado de sldb surface/vite.config.ts: /sldb se redirige al `sldb serve` (sin CORS).
const sldbTarget = process.env.SLDB_TARGET ?? "http://127.0.0.1:8085";

export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      "/sldb": { target: sldbTarget, changeOrigin: true, rewrite: (path) => path.replace(/^\/sldb/, "") },
    },
  },
  test: { environment: "jsdom", globals: true, setupFiles: ["./src/test-setup.ts"] },
});
