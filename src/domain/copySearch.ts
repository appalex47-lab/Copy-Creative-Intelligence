import { normalize } from './copyRules';
import { COPY_FIELDS, currentVersion, type CopyRecord } from './copy';

/**
 * Búsqueda local de copys (S2.8): coincide por nombre, etiquetas o texto del contenido actual y de las variantes.
 * Sin distinguir mayúsculas ni acentos; todas las palabras de la consulta deben aparecer (en cualquier campo).
 * Consulta vacía = todos. No busca en versiones anteriores (decisión de Claude, reversible).
 */
export function matchesCopy(copy: CopyRecord, query: string): boolean {
  const words = normalize(query).split(/\s+/).filter(Boolean);
  if (words.length === 0) return true;
  const parts: string[] = [copy.label, ...copy.tags];
  const push = (c: Partial<Record<(typeof COPY_FIELDS)[number], string>>) => {
    for (const f of COPY_FIELDS) {
      const v = c[f];
      if (v !== undefined) parts.push(v);
    }
  };
  push(currentVersion(copy).content);
  for (const v of copy.variants ?? []) {
    parts.push(v.label);
    push(v.content);
  }
  const haystack = normalize(parts.join(' \n '));
  return words.every((w) => haystack.includes(w));
}
