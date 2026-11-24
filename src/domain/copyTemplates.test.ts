import { describe, expect, it } from 'vitest';
import type { BriefFields } from './brief';
import { CHANNEL_FIELDS, applyTemplate } from './copyTemplates';
import { CHANNELS } from './brief';

const brief: BriefFields = {
  campaign: 'Buen Fin',
  objective: 'Ventas',
  product: 'Vitamina C',
  audience: 'Recurrentes',
  message: 'Cuida tu salud',
  channel: 'Email',
  cta: 'Compra ahora',
  benefit: 'defensas fuertes',
  offer: '20% de descuento',
  conditions: 'Aplican restricciones.',
  validity: { from: '2026-11-13', to: '2026-11-17' },
};

describe('applyTemplate', () => {
  it('directo en Email usa headline, description, body y cta', () => {
    expect(applyTemplate('directo', brief)).toEqual({
      headline: 'Vitamina C: defensas fuertes',
      description: '20% de descuento',
      body: 'Cuida tu salud',
      cta: 'Compra ahora',
    });
  });
  it('oferta arma titular, texto y vigencia solo con datos del brief', () => {
    expect(applyTemplate('oferta', brief)).toEqual({
      headline: '20% de descuento en Vitamina C',
      body: 'Cuida tu salud Aplican restricciones.',
      description: 'Vigencia: del 13/11/2026 al 17/11/2026. Aplican restricciones.',
      cta: 'Compra ahora',
    });
  });
  it('sin datos opcionales no inventa nada: el campo queda fuera', () => {
    const { benefit: _b, offer: _o, conditions: _c, validity: _v, ...min } = brief;
    void [_b, _o, _c, _v];
    expect(applyTemplate('directo', min)).toEqual({
      headline: 'Vitamina C',
      body: 'Cuida tu salud',
      cta: 'Compra ahora',
    });
    expect(applyTemplate('oferta', min)).toEqual({
      headline: 'Vitamina C',
      body: 'Cuida tu salud',
      cta: 'Compra ahora',
    });
  });
  it('solo rellena los campos que el canal usa', () => {
    for (const channel of CHANNELS) {
      const keys = Object.keys(applyTemplate('directo', { ...brief, channel }));
      for (const k of keys) expect(CHANNEL_FIELDS[channel]).toContain(k);
    }
    expect(Object.keys(applyTemplate('directo', { ...brief, channel: 'WhatsApp' })).sort()).toEqual(
      ['body', 'cta'],
    );
  });
  it('vigencia parcial', () => {
    expect(
      applyTemplate('oferta', {
        ...brief,
        channel: 'Landing pages',
        validity: { to: '2026-11-17' },
      }).description,
    ).toBe('Vigencia: hasta el 17/11/2026. Aplican restricciones.');
  });
});
