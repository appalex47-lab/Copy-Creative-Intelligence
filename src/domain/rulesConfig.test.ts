import { describe, expect, it } from 'vitest';
import { TEMPLATE_DOC, validateBrandTerm, validateLegend, validateRulesDoc } from './rulesConfig';

const legend = {
  text: ' Consulta a tu médico ',
  channels: ['Email', 'Email'],
  required: true,
  active: true,
};

describe('validateLegend', () => {
  it('recorta, deduplica canales y acepta lista vacía (todos)', () => {
    const v = validateLegend(legend);
    expect(v).toEqual({
      ok: true,
      value: { text: 'Consulta a tu médico', channels: ['Email'], required: true, active: true },
    });
    expect(validateLegend({ ...legend, channels: [] }).ok).toBe(true);
  });
  it('rechaza vacío, canal desconocido, clave extra y control', () => {
    expect(validateLegend({ ...legend, text: '  ' }).ok).toBe(false);
    expect(validateLegend({ ...legend, channels: ['Llamadas'] }).ok).toBe(false);
    expect(validateLegend({ ...legend, extra: 1 }).ok).toBe(false);
    expect(validateLegend({ ...legend, text: 'a\nb' }).ok).toBe(false);
    expect(validateLegend({ ...legend, required: 'sí' }).ok).toBe(false);
    expect(validateLegend({ ...legend, text: 'x'.repeat(301) }).ok).toBe(false);
  });
});

describe('validateBrandTerm', () => {
  it('acepta término con sugerencia opcional', () => {
    expect(validateBrandTerm({ text: 'cura', kind: 'prohibido', severity: 'mayor' }).ok).toBe(true);
    const v = validateBrandTerm({
      text: 'cura',
      kind: 'prohibido',
      severity: 'mayor',
      suggestion: 'alivia',
    });
    expect(v.ok && v.value.suggestion).toBe('alivia');
    expect(
      validateBrandTerm({ text: 'x', kind: 'prohibido', severity: 'mayor', suggestion: '' }).ok,
    ).toBe(true);
  });
  it('rechaza tipo o severidad inválidos', () => {
    expect(validateBrandTerm({ text: 'x', kind: 'otro', severity: 'mayor' }).ok).toBe(false);
    expect(validateBrandTerm({ text: 'x', kind: 'prohibido', severity: 'grave' }).ok).toBe(false);
  });
});

describe('validateRulesDoc', () => {
  it('la plantilla es válida', () => {
    expect(validateRulesDoc(TEMPLATE_DOC).ok).toBe(true);
  });
  it('rechaza repetidos sin importar mayúsculas ni acentos', () => {
    const l = { text: 'Consulta a tu médico', channels: [], required: true, active: true };
    expect(
      validateRulesDoc({ legends: [l, { ...l, text: 'CONSULTA A TU MEDICO' }], brandTerms: [] }).ok,
    ).toBe(false);
    const t = { text: 'Cura', kind: 'prohibido', severity: 'mayor' };
    expect(validateRulesDoc({ legends: [], brandTerms: [t, { ...t, text: 'cura' }] }).ok).toBe(
      false,
    );
    expect(validateRulesDoc({ legends: [], brandTerms: [t, { ...t, kind: 'preferido' }] }).ok).toBe(
      true,
    );
  });
  it('rechaza forma incorrecta', () => {
    expect(validateRulesDoc(null).ok).toBe(false);
    expect(validateRulesDoc({ legends: [] }).ok).toBe(false);
    expect(validateRulesDoc({ legends: [], brandTerms: [], x: 1 }).ok).toBe(false);
  });
});
