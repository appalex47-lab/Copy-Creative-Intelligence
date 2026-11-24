import { describe, expect, it } from 'vitest';
import { matchesCopy } from './copySearch';
import type { CopyRecord } from './copy';

const t = '2026-11-23T09:00:00.000Z';
const copy: CopyRecord = {
  id: 'cpy_abcdefgh1',
  briefId: 'brf_abcdefgh1',
  label: 'Principal Buen Fin',
  tags: ['Promoción', 'urgente'],
  createdAt: t,
  updatedAt: t,
  versions: [
    { n: 1, createdAt: t, content: { headline: 'Texto viejo único' } },
    { n: 2, createdAt: t, content: { headline: 'Descuento del 20%', cta: 'Compra ahora' } },
  ],
  variants: [
    {
      id: 'var_abcdefgh1',
      label: 'Corta',
      content: { body: 'Ahorra hoy' },
      createdAt: t,
      updatedAt: t,
    },
  ],
};

describe('búsqueda de copys', () => {
  it('consulta vacía o en blanco coincide con todo', () => {
    expect(matchesCopy(copy, '')).toBe(true);
    expect(matchesCopy(copy, '   ')).toBe(true);
  });
  it('busca por nombre, etiqueta, contenido actual y variantes, sin mayúsculas ni acentos', () => {
    expect(matchesCopy(copy, 'buen fin')).toBe(true);
    expect(matchesCopy(copy, 'PROMOCION')).toBe(true);
    expect(matchesCopy(copy, 'compra')).toBe(true);
    expect(matchesCopy(copy, 'ahorra')).toBe(true);
    expect(matchesCopy(copy, 'corta')).toBe(true);
  });
  it('todas las palabras deben aparecer; no busca en versiones anteriores', () => {
    expect(matchesCopy(copy, 'descuento urgente')).toBe(true);
    expect(matchesCopy(copy, 'descuento inexistente')).toBe(false);
    expect(matchesCopy(copy, 'viejo')).toBe(false);
  });
});
