import { fireEvent, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { fail, ok, type Services } from '@/services/contracts';
import {
  INTERNAL_DETAIL,
  renderWithServices,
  servicesWith,
} from '../../tests/support/fakeServices';
import { ConnectionPage } from './ConnectionPage';
import { HomePage } from './HomePage';

beforeEach(() => vi.spyOn(console, 'error').mockImplementation(() => undefined));
afterEach(() => vi.restoreAllMocks());

const failing = (code: 'unavailable' | 'not_found'): Partial<Services> => ({
  identity: { getCurrentIdentity: () => Promise.resolve(fail(code, INTERNAL_DETAIL)) },
});

describe('HomePage — estados', () => {
  it('muestra carga y luego éxito', async () => {
    renderWithServices(<HomePage />, servicesWith());
    expect(screen.getByText('Cargando…')).toBeInTheDocument();
    expect(await screen.findByText('Persona DEMO')).toBeInTheDocument();
  });

  it('muestra un Result fallido de forma visible, sin detalle interno', async () => {
    renderWithServices(<HomePage />, servicesWith(failing('not_found')));
    const alert = await screen.findByRole('alert');
    expect(alert).toHaveTextContent('No se encontró la información solicitada.');
    expect(document.body.textContent).not.toContain(INTERNAL_DETAIL);
    expect(screen.queryByRole('button', { name: 'Reintentar' })).not.toBeInTheDocument();
    expect(screen.queryByText('Cargando…')).not.toBeInTheDocument();
  });

  it('una excepción del servicio produce error (no carga permanente) con reintento', async () => {
    let calls = 0;
    const services = servicesWith({
      identity: {
        getCurrentIdentity: () => {
          calls += 1;
          return calls === 1
            ? Promise.reject(new Error(INTERNAL_DETAIL))
            : servicesWith().identity.getCurrentIdentity();
        },
      },
    });
    renderWithServices(<HomePage />, services);
    expect(await screen.findByRole('alert')).toHaveTextContent('Ocurrió un error inesperado');
    expect(document.body.textContent).not.toContain(INTERNAL_DETAIL);
    fireEvent.click(screen.getByRole('button', { name: 'Reintentar' }));
    expect(await screen.findByText('Persona DEMO')).toBeInTheDocument();
    expect(calls).toBe(2);
  });

  it('un fallo transitorio ("unavailable") ofrece reintentar', async () => {
    renderWithServices(<HomePage />, servicesWith(failing('unavailable')));
    expect(await screen.findByRole('alert')).toHaveTextContent('no está disponible');
    expect(screen.getByRole('button', { name: 'Reintentar' })).toBeInTheDocument();
  });

  it('el fallo en proyectos no se disfraza de lista vacía', async () => {
    const services = servicesWith({
      projects: { listForOrganization: () => Promise.resolve(fail('unavailable', 'x')) },
    });
    renderWithServices(<HomePage />, services);
    expect(await screen.findByRole('alert')).toBeInTheDocument();
    expect(screen.queryByText(/Proyectos:/)).not.toBeInTheDocument();
  });

  it('una lista vacía legítima se declara explícitamente', async () => {
    const services = servicesWith({
      organizations: { listForCurrentUser: () => Promise.resolve(ok([])) },
    });
    renderWithServices(<HomePage />, services);
    expect(await screen.findByText(/Organizaciones:/)).toHaveTextContent('ninguna');
    expect(screen.getByText(/Proyectos:/)).toHaveTextContent('ninguno');
  });
});

describe('ConnectionPage — estados', () => {
  it('mantiene el aviso de "sin backend" aun cuando falla la consulta de estado', async () => {
    const services = servicesWith({
      appState: { getState: () => Promise.resolve(fail('unavailable', INTERNAL_DETAIL)) },
    });
    renderWithServices(<ConnectionPage />, services);
    expect(await screen.findByRole('alert')).toBeInTheDocument();
    expect(screen.getByRole('note')).toHaveTextContent('no está conectada a ningún backend');
    expect(document.body.textContent).not.toContain(INTERNAL_DETAIL);
  });

  it('excepción: error genérico con reintento que se recupera', async () => {
    let calls = 0;
    const base = servicesWith();
    const services = servicesWith({
      appState: {
        getState: () => {
          calls += 1;
          return calls === 1
            ? Promise.reject(new Error(INTERNAL_DETAIL))
            : base.appState.getState();
        },
      },
    });
    renderWithServices(<ConnectionPage />, services);
    await screen.findByRole('alert');
    fireEvent.click(screen.getByRole('button', { name: 'Reintentar' }));
    expect(await screen.findByLabelText(/Estado de conexión/)).toBeInTheDocument();
    expect(await screen.findByText(/"isDemo": true/)).toBeInTheDocument();
  });
});
