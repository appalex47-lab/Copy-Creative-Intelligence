import { fileURLToPath, URL } from 'node:url';
import react from '@vitejs/plugin-react';
import { loadEnv, type Plugin } from 'vite';
import { defineConfig } from 'vitest/config';
import { evaluateEnvPolicy } from './src/app/envPolicy.ts';

const ROOT = fileURLToPath(new URL('.', import.meta.url));

/**
 * Valida el entorno ANTES de construir o servir: un build de producción con datos DEMO, o una configuración
 * contradictoria, falla con un mensaje claro. Es una protección contra errores de configuración, no una garantía
 * de seguridad (la seguridad real dependerá de Auth, RLS y backend).
 */
function envGuard(): Plugin {
  return {
    name: 'cci-env-guard',
    config(_config, { mode }) {
      const policy = evaluateEnvPolicy({ ...loadEnv(mode, ROOT, 'VITE_'), MODE: mode });
      if (!policy.ok) {
        throw new Error(`[CCI] Configuración de entorno rechazada (${mode}): ${policy.message}`);
      }
    },
  };
}

// Configuración de Vite + Vitest. Sin secretos; las variables públicas se leen en src/app/env.ts.
export default defineConfig({
  plugins: [envGuard(), react()],
  resolve: { alias: { '@': fileURLToPath(new URL('./src', import.meta.url)) } },
  test: {
    environment: 'jsdom',
    setupFiles: ['./tests/setup.ts'],
    include: ['src/**/*.test.{ts,tsx}', 'tests/**/*.test.{ts,tsx}'],
    exclude: ['e2e/**', 'node_modules/**'],
    css: false,
  },
});
