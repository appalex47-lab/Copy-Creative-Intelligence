/** Resultado explícito de un caso de uso: evita excepciones como flujo normal. */
export type Result<T> =
  { readonly ok: true; readonly value: T } | { readonly ok: false; readonly error: AppError };

export type AppErrorCode =
  'not_found' | 'not_implemented' | 'unavailable' | 'invalid_configuration' | 'validation_error';

export interface AppError {
  readonly code: AppErrorCode;
  readonly message: string;
}

export const ok = <T>(value: T): Result<T> => ({ ok: true, value });
export const fail = <T = never>(code: AppErrorCode, message: string): Result<T> => ({
  ok: false,
  error: { code, message },
});
