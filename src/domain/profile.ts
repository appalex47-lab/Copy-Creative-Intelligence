import { invalid, valid, type Validation } from './validation';

/**
 * Perfil local (P1): solo un nombre visible OPCIONAL, sin identidad autenticada, organización, membresía ni roles.
 * SUPUESTO de Claude (S1-D10, reversible): longitud máxima 60 caracteres tras recortar espacios.
 */
export interface LocalProfile {
  readonly displayName?: string;
}

export const DISPLAY_NAME_MAX = 60;

/** El nombre es texto no confiable: aquí solo se valida; al mostrarlo, React lo escapa (no usar HTML sin escapar). */
export function validateDisplayName(input: unknown): Validation<string | undefined> {
  if (input === undefined || input === null) return valid(undefined);
  if (typeof input !== 'string') return invalid('El nombre visible debe ser texto.');
  const name = input.replace(/\s+/g, ' ').trim();
  if (name === '') return valid(undefined); // vacío = sin nombre (equivale a borrarlo)
  if ([...name].length > DISPLAY_NAME_MAX)
    return invalid(`El nombre visible admite como máximo ${DISPLAY_NAME_MAX} caracteres.`);
  // eslint-disable-next-line no-control-regex
  if (/[\u0000-\u001f\u007f]/.test(name))
    return invalid('El nombre visible contiene caracteres no permitidos.');
  return valid(name);
}

/** Lee un perfil guardado de forma tolerante: ignora claves desconocidas y descarta un nombre inválido. */
export function parseLocalProfile(raw: unknown): LocalProfile {
  if (typeof raw !== 'object' || raw === null) return {};
  const v = validateDisplayName((raw as Record<string, unknown>)['displayName']);
  return v.ok && v.value !== undefined ? { displayName: v.value } : {};
}
