import { useCallback, useEffect, useMemo, useState } from 'react';
import { describeError, isRetryable, UNEXPECTED_MESSAGE } from '@/lib/errorMessages';
import type { Result } from '@/services/contracts';

export type AsyncState<T> =
  | { readonly status: 'loading' }
  | { readonly status: 'success'; readonly data: T }
  | { readonly status: 'error'; readonly message: string; readonly retryable: boolean };

/**
 * Ejecuta una operación asíncrona que devuelve `Result<T>` y expone tres estados diferenciados:
 * cargando, éxito y error. Captura tanto los `Result` fallidos como las excepciones, nunca deja un
 * estado de carga permanente, ignora respuestas tardías y permite reintentar.
 * `loader` debe tener identidad estable (useCallback) para no relanzar la operación en cada render.
 */
export function useAsyncResource<T>(loader: () => Promise<Result<T>>): {
  state: AsyncState<T>;
  retry: () => void;
} {
  const [attempt, setAttempt] = useState(0);
  // Cada combinación (loader, intento) es una "solicitud"; un resultado solo vale para su solicitud.
  const request = useMemo(() => ({ loader, attempt }), [loader, attempt]);
  const [settled, setSettled] = useState<{
    readonly request: object;
    readonly value: Exclude<AsyncState<T>, { status: 'loading' }>;
  } | null>(null);

  useEffect(() => {
    let cancelled = false;
    request.loader().then(
      (result) => {
        if (cancelled) return;
        setSettled({
          request,
          value: result.ok
            ? { status: 'success', data: result.value }
            : {
                status: 'error',
                message: describeError(result.error),
                retryable: isRetryable(result.error.code),
              },
        });
      },
      (cause: unknown) => {
        if (cancelled) return;
        // Se registra solo el tipo de error (sin mensaje ni datos) y se muestra un texto genérico.
        console.error(
          '[cci] operación asíncrona fallida:',
          cause instanceof Error ? cause.name : typeof cause,
        );
        setSettled({
          request,
          value: { status: 'error', message: UNEXPECTED_MESSAGE, retryable: true },
        });
      },
    );
    return () => {
      cancelled = true;
    };
  }, [request]);

  const state: AsyncState<T> =
    settled !== null && settled.request === request ? settled.value : { status: 'loading' };
  const retry = useCallback(() => setAttempt((n) => n + 1), []);
  return { state, retry };
}
