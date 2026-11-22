import { act, renderHook, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { fail, ok, type Result } from '@/services/contracts';
import { useAsyncResource } from './useAsyncResource';

beforeEach(() => vi.spyOn(console, 'error').mockImplementation(() => undefined));
afterEach(() => vi.restoreAllMocks());

describe('useAsyncResource', () => {
  it('pasa de cargando a éxito', async () => {
    const loader = () => Promise.resolve(ok(42));
    const { result } = renderHook(() => useAsyncResource(loader));
    expect(result.current.state.status).toBe('loading');
    await waitFor(() => expect(result.current.state).toEqual({ status: 'success', data: 42 }));
  });

  it('un Result fallido pasa a error visible con mensaje por código, no el interno', async () => {
    const loader = () => Promise.resolve(fail<number>('not_found', 'tabla x fila 9'));
    const { result } = renderHook(() => useAsyncResource(loader));
    await waitFor(() => expect(result.current.state.status).toBe('error'));
    expect(result.current.state).toEqual({
      status: 'error',
      message: 'No se encontró la información solicitada.',
      retryable: false,
    });
  });

  it('una excepción pasa a error genérico reintentable y no a carga permanente', async () => {
    const loader = () => Promise.reject(new Error('detalle sensible'));
    const { result } = renderHook(() => useAsyncResource<number>(loader));
    await waitFor(() => expect(result.current.state.status).toBe('error'));
    const s = result.current.state;
    expect(s.status === 'error' && s.retryable).toBe(true);
    expect(JSON.stringify(s)).not.toContain('sensible');
    expect(console.error).toHaveBeenCalledWith('[cci] operación asíncrona fallida:', 'Error');
  });

  it('reintentar vuelve a cargar y puede terminar en éxito', async () => {
    let n = 0;
    const loader = (): Promise<Result<string>> =>
      Promise.resolve(++n === 1 ? fail('unavailable', 'x') : ok('listo'));
    const { result } = renderHook(() => useAsyncResource(loader));
    await waitFor(() => expect(result.current.state.status).toBe('error'));
    act(() => result.current.retry());
    expect(result.current.state.status).toBe('loading');
    await waitFor(() => expect(result.current.state).toEqual({ status: 'success', data: 'listo' }));
    expect(n).toBe(2);
  });

  it('ignora la respuesta de una solicitud ya descartada (desmontaje)', async () => {
    let resolve!: (r: Result<number>) => void;
    const loader = () => new Promise<Result<number>>((r) => (resolve = r));
    const { result, unmount } = renderHook(() => useAsyncResource(loader));
    unmount();
    resolve(ok(1));
    await Promise.resolve();
    expect(result.current.state.status).toBe('loading');
  });
});
