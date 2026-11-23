import { defineConfig } from '@playwright/test';

// Pruebas de navegador REAL (Chrome). Usa el Chrome instalado (channel "chrome") o CCI_CHROME_PATH; no descarga navegadores.
// Dos servidores locales: (1) el build de preview servido con `vite preview` y (2) el servidor de desarrollo
// (con React StrictMode) que además sirve el arnés e2e/harness.html. Ninguno usa backend ni credenciales.
const chromePath = process.env['CCI_CHROME_PATH'];

export default defineConfig({
  testDir: './e2e',
  timeout: 30_000,
  fullyParallel: false,
  workers: 1,
  reporter: [['list'], ['json', { outputFile: 'test-results/e2e-results.json' }]],
  outputDir: 'test-results/artifacts',
  use: {
    ...(chromePath
      ? { launchOptions: { executablePath: chromePath, args: ['--no-sandbox'] } }
      : { channel: 'chrome', launchOptions: { args: ['--no-sandbox'] } }),
    headless: true,
    trace: 'off',
  },
  webServer: [
    {
      command: 'npm run build && npx vite preview --mode preview --port 4173 --strictPort',
      url: 'http://localhost:4173',
      reuseExistingServer: !process.env['CI'],
      timeout: 120_000,
    },
    {
      command: 'npx vite --port 5173 --strictPort',
      url: 'http://localhost:5173',
      reuseExistingServer: !process.env['CI'],
      timeout: 60_000,
    },
    {
      // Servidor de desarrollo en modo de datos LOCAL (IndexedDB + Local Storage reales del navegador).
      command: 'npx vite --port 5174 --strictPort',
      env: { VITE_DATA_MODE: 'local' },
      url: 'http://localhost:5174',
      reuseExistingServer: !process.env['CI'],
      timeout: 60_000,
    },
  ],
});
