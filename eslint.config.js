import js from '@eslint/js';
import reactHooks from 'eslint-plugin-react-hooks';
import reactRefresh from 'eslint-plugin-react-refresh';
import globals from 'globals';
import tseslint from 'typescript-eslint';

export default tseslint.config(
  {
    // Fuera de alcance: artefactos de build y documentación/expedientes (no son código de la aplicación).
    ignores: [
      'dist',
      'coverage',
      'node_modules',
      'public/ocr',
      'playwright-report',
      'test-results',
      'docs',
      'evidencia',
      'evidence',
      'AUDITORIA_*',
      'ARTEFACTOS_REVISION_PUBLICACION',
    ],
  },
  {
    // Scripts y configuración en JavaScript: también se revisan (antes quedaban fuera en silencio).
    files: ['**/*.{js,mjs,cjs}'],
    extends: [js.configs.recommended],
    languageOptions: { ecmaVersion: 2023, sourceType: 'module', globals: { ...globals.node } },
    rules: { 'no-restricted-syntax': 'off' },
  },
  {
    files: ['**/*.{ts,tsx,mts}'],
    extends: [js.configs.recommended, ...tseslint.configs.strict],
    languageOptions: { ecmaVersion: 2023, globals: { ...globals.browser } },
    plugins: { 'react-hooks': reactHooks, 'react-refresh': reactRefresh },
    rules: {
      ...reactHooks.configs.recommended.rules,
      'react-refresh/only-export-components': ['error', { allowConstantExport: true }],
      '@typescript-eslint/consistent-type-imports': 'error',
      // Regla de arquitectura: el dominio, la aplicación y la UI no pueden depender de Supabase.
      'no-restricted-imports': [
        'error',
        {
          patterns: [
            {
              group: ['@supabase/*'],
              message:
                'Solo un adaptador en src/services/adapters/supabase puede importar Supabase (fase futura).',
            },
          ],
        },
      ],
      // Los imports dinámicos de Supabase tampoco están permitidos fuera de su adaptador.
      'no-restricted-syntax': [
        'error',
        {
          selector: 'ImportExpression[source.value=/supabase/i]',
          message: 'Solo el adaptador src/services/adapters/supabase puede importar Supabase.',
        },
      ],
    },
  },
  {
    // Único lugar donde una futura implementación autorizada puede importar Supabase.
    files: ['src/services/adapters/supabase/**/*.{ts,tsx}'],
    rules: { 'no-restricted-imports': 'off', 'no-restricted-syntax': 'off' },
  },
  {
    files: ['vite.config.ts', 'playwright.config.ts', 'e2e/**/*.ts', 'tests/**/*.ts'],
    languageOptions: { globals: { ...globals.node } },
  },
);
