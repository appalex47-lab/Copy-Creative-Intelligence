import { fireEvent, render, screen, within } from '@testing-library/react';
import { StrictMode } from 'react';
import { describe, expect, it } from 'vitest';
import { App } from './App';

const env = { appEnv: 'test', dataMode: 'demo' } as const;

// Comprobaciones semánticas en jsdom. La validación con axe y teclado REALES se hace en el navegador (e2e).
describe('accesibilidad semántica de la interfaz', () => {
  it('expone landmarks, enlace de salto y jerarquía de encabezados h1 → h2', async () => {
    render(<App env={env} />);
    await screen.findByText('Sin actividad reciente');
    expect(screen.getByRole('banner')).toBeInTheDocument();
    expect(screen.getByRole('navigation', { name: 'Navegación principal' })).toBeInTheDocument();
    expect(screen.getByRole('main')).toHaveAttribute('id', 'contenido');
    expect(screen.getByRole('link', { name: 'Saltar al contenido' })).toHaveAttribute(
      'href',
      '#contenido',
    );
    const levels = screen.getAllByRole('heading').map((h) => h.tagName);
    expect(levels).toEqual(['H1', 'H2', 'H3', 'H3']);
  });

  it('la navegación indica la página activa con aria-current y cambia con la selección', async () => {
    render(<App env={env} />);
    const nav = screen.getByRole('navigation', { name: 'Navegación principal' });
    expect(within(nav).getByRole('button', { name: 'Inicio' })).toHaveAttribute(
      'aria-current',
      'page',
    );
    expect(within(nav).getByRole('button', { name: 'Estado de conexión' })).not.toHaveAttribute(
      'aria-current',
    );
    fireEvent.click(within(nav).getByRole('button', { name: 'Estado de conexión' }));
    expect(within(nav).getByRole('button', { name: 'Estado de conexión' })).toHaveAttribute(
      'aria-current',
      'page',
    );
    expect(within(nav).getByRole('button', { name: 'Inicio' })).not.toHaveAttribute('aria-current');
  });

  it('al navegar, el foco pasa al encabezado de la página y se actualiza el título', async () => {
    render(<App env={env} />);
    await screen.findByText('Sin actividad reciente');
    fireEvent.click(screen.getByRole('button', { name: 'Estado de conexión' }));
    const h2 = await screen.findByRole('heading', { level: 2, name: 'Estado de conexión' });
    expect(h2).toHaveFocus();
    expect(document.title).toContain('Estado de conexión');
  });

  it('en el montaje inicial (incluido StrictMode) no se roba el foco', () => {
    render(
      <StrictMode>
        <App env={env} />
      </StrictMode>,
    );
    expect(document.body).toHaveFocus();
  });

  it('la región de estado es persistente y anuncia carga → contenido cargado', async () => {
    render(<App env={env} />);
    const status = screen.getByRole('status');
    expect(status).toHaveTextContent('Cargando…');
    expect(status).toHaveAttribute('aria-live', 'polite');
    await screen.findByText('Sin actividad reciente');
    expect(screen.getByRole('status')).toBe(status); // mismo nodo: los cambios se anuncian
    expect(status).toHaveTextContent('Contenido cargado.');
  });

  it('no usa aria-label en elementos genéricos y los contenedores con nombre tienen rol adecuado', async () => {
    const { container } = render(<App env={env} />);
    await screen.findByText('Sin actividad reciente');
    fireEvent.click(screen.getByRole('button', { name: 'Estado de conexión' }));
    await screen.findByRole('region', { name: 'Estado de la aplicación (JSON)' });
    for (const el of container.querySelectorAll('pre, p, div:not([role]), span')) {
      expect(el.hasAttribute('aria-label')).toBe(false);
    }
    expect(screen.getByRole('region', { name: 'Estado de la aplicación (JSON)' })).toHaveAttribute(
      'tabindex',
      '0',
    );
  });
});
