import { fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { ErrorBoundary } from '@/components/ErrorBoundary';
import { App, ConfigurationError } from './App';
import type { AppEnv } from './env';

describe('inicialización de la aplicación', () => {
  beforeEach(() => vi.spyOn(console, 'error').mockImplementation(() => undefined));
  afterEach(() => vi.restoreAllMocks());

  it('arranca en modo DEMO, muestra el aviso y un estado vacío honesto por contratos', async () => {
    render(<App env={{ appEnv: 'test', dataMode: 'demo' }} />);
    expect(screen.getByRole('region', { name: 'Aviso de modo DEMO' })).toHaveTextContent(
      'MODO DEMO',
    );
    expect(await screen.findByText('Sin actividad reciente')).toBeInTheDocument();
  });

  it('permite navegar al estado de conexión y declara que no hay backend', async () => {
    render(<App env={{ appEnv: 'test', dataMode: 'demo' }} />);
    fireEvent.click(screen.getByRole('button', { name: 'Estado de conexión' }));
    expect(await screen.findByRole('note')).toHaveTextContent('no está conectada a ningún backend');
  });

  it('un fallo de composición de servicios lo captura el ErrorBoundary raíz (como en main.tsx)', () => {
    const bad = { appEnv: 'test', dataMode: 'otro' } as unknown as AppEnv;
    render(
      <ErrorBoundary>
        <App env={bad} />
      </ErrorBoundary>,
    );
    expect(screen.getByRole('alert')).toHaveTextContent('Ocurrió un error inesperado');
    expect(document.body.textContent).not.toContain('Modo de datos no soportado');
  });

  it('ConfigurationError se anuncia como alerta y no muestra datos DEMO', () => {
    render(<ConfigurationError message="entorno rechazado" />);
    expect(screen.getByRole('alert')).toHaveTextContent('entorno rechazado');
    expect(screen.queryByText('Sin actividad reciente')).not.toBeInTheDocument();
  });
});
