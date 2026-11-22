import { fireEvent, render, screen } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { INTERNAL_DETAIL } from '../../tests/support/fakeServices';
import { ErrorBoundary } from './ErrorBoundary';

let shouldThrow = true;
function Bomb() {
  if (shouldThrow) throw new Error(INTERNAL_DETAIL);
  return <p>contenido sano</p>;
}

beforeEach(() => {
  shouldThrow = true;
  vi.spyOn(console, 'error').mockImplementation(() => undefined);
});
afterEach(() => vi.restoreAllMocks());

describe('ErrorBoundary', () => {
  it('captura el error de renderizado y muestra un mensaje genérico sin detalles internos', () => {
    render(
      <ErrorBoundary>
        <Bomb />
      </ErrorBoundary>,
    );
    const alert = screen.getByRole('alert');
    expect(alert).toHaveTextContent('Ocurrió un error inesperado');
    expect(document.body.textContent).not.toContain(INTERNAL_DETAIL);
  });

  it('permite reintentar y recupera el contenido cuando la causa desaparece', () => {
    render(
      <ErrorBoundary>
        <Bomb />
      </ErrorBoundary>,
    );
    shouldThrow = false;
    fireEvent.click(screen.getByRole('button', { name: 'Reintentar' }));
    expect(screen.getByText('contenido sano')).toBeInTheDocument();
  });

  it('no interfiere cuando no hay errores', () => {
    shouldThrow = false;
    render(
      <ErrorBoundary>
        <Bomb />
      </ErrorBoundary>,
    );
    expect(screen.getByText('contenido sano')).toBeInTheDocument();
  });
});
