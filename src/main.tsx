import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { App, ConfigurationError } from '@/app/App';
import { parseEnv } from '@/app/env';
import '@/styles/global.css';

const root = document.getElementById('root');
if (!root) throw new Error('No existe #root');

const parsed = parseEnv(import.meta.env as unknown as Record<string, string | undefined>);
createRoot(root).render(
  <StrictMode>
    <ErrorBoundary>
      {parsed.ok ? (
        <App env={parsed.value} />
      ) : (
        <ConfigurationError message={parsed.error.message} />
      )}
    </ErrorBoundary>
  </StrictMode>,
);
