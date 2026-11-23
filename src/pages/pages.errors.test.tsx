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
  activity: {
    listRecent: () => Promise.resolve(fail(code, INTERNAL_DETAIL)),
    record: () => Promise.resolve(ok(undefined)),
  },
});

describe('HomePage — estados', () => {
  it('muestra carga y luego éxito', async () => {
    renderWithServices(<HomePage />, servicesWith());
    expect(screen.getByText('Cargando…')).toBeInTheDocument();
    expect(await screen.findByText('Sin actividad reciente')).toBeInTheDocument();
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
      activity: {
        record: () => Promise.resolve(ok(undefined)),
        listRecent: () => {
          calls += 1;
          return calls === 1
            ? Promise.reject(new Error(INTERNAL_DETAIL))
            : servicesWith().activity.listRecent();
        },
      },
    });
    renderWithServices(<HomePage />, services);
    expect(await screen.findByRole('alert')).toHaveTextContent('Ocurrió un error inesperado');
    expect(document.body.textContent).not.toContain(INTERNAL_DETAIL);
    fireEvent.click(screen.getByRole('button', { name: 'Reintentar' }));
    expect(await screen.findByText('Sin actividad reciente')).toBeInTheDocument();
    expect(calls).toBe(2);
  });

  it('un fallo transitorio ("unavailable") ofrece reintentar', async () => {
    renderWithServices(<HomePage />, servicesWith(failing('unavailable')));
    expect(await screen.findByRole('alert')).toHaveTextContent('no está disponible');
    expect(screen.getByRole('button', { name: 'Reintentar' })).toBeInTheDocument();
  });

  it('el fallo de la actividad no se disfraza de estado vacío', async () => {
    renderWithServices(<HomePage />, servicesWith(failing('unavailable')));
    expect(await screen.findByRole('alert')).toBeInTheDocument();
    expect(screen.queryByText('Sin actividad reciente')).not.toBeInTheDocument();
  });

  it('una lista vacía legítima se declara explícitamente', async () => {
    renderWithServices(<HomePage />, servicesWith());
    expect(
      await screen.findByRole('region', { name: 'Sin actividad reciente' }),
    ).toBeInTheDocument();
  });

  it('con actividad real la lista muestra una entrada por evento', async () => {
    const services = servicesWith({
      activity: {
        record: () => Promise.resolve(ok(undefined)),
        listRecent: () =>
          Promise.resolve(
            ok([
              { id: 'evt_00000001', at: '2026-11-22T10:00:00.000Z', kind: 'app_opened' as const },
            ]),
          ),
      },
    });
    renderWithServices(<HomePage />, services);
    expect(await screen.findByText(/Se abrió la aplicación/)).toBeInTheDocument();
    expect(screen.queryByText('Sin actividad reciente')).not.toBeInTheDocument();
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
