/** Resultado de una validación de dominio. El dominio no depende de otras capas (regla de arquitectura S1.1). */
export type Validation<T> =
  { readonly ok: true; readonly value: T } | { readonly ok: false; readonly reason: string };

export const valid = <T>(value: T): Validation<T> => ({ ok: true, value });
export const invalid = <T = never>(reason: string): Validation<T> => ({ ok: false, reason });
