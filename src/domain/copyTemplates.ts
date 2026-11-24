import type { BriefFields, Channel } from './brief';
import type { CopyContent, CopyField } from './copy';

/**
 * Plantillas de copy sin IA (S2.6, IA-A). Solo REORDENAN datos del brief: nunca inventan hechos de negocio (precios,
 * porcentajes, beneficios). Si falta un dato del brief, ese campo queda vacío. El resultado es un punto de partida
 * editable; las longitudes las revisa el motor de reglas, no la plantilla. SUPUESTOS de Claude (reversibles): qué campos
 * del copy usa cada canal y la redacción de las dos plantillas.
 */
export type TemplateId = 'directo' | 'oferta';
export const TEMPLATES: readonly { readonly id: TemplateId; readonly name: string }[] = [
  { id: 'directo', name: 'Directo: producto, beneficio y mensaje' },
  { id: 'oferta', name: 'Oferta: oferta, condiciones y vigencia' },
];

export const CHANNEL_FIELDS: Readonly<Record<Channel, readonly CopyField[]>> = {
  Ecommerce: ['headline', 'description', 'cta'],
  App: ['headline', 'body', 'cta'],
  WhatsApp: ['body', 'cta'],
  Email: ['headline', 'description', 'body', 'cta'],
  'Redes sociales': ['body', 'cta'],
  Banners: ['headline', 'cta'],
  'Landing pages': ['headline', 'description', 'cta'],
};

const join = (parts: readonly (string | undefined)[], sep: string): string | undefined => {
  const p = parts.filter((x): x is string => x !== undefined && x.trim() !== '');
  return p.length === 0 ? undefined : p.join(sep);
};
const ymdToLocal = (s: string): string => s.split('-').reverse().join('/');

function validityText(f: Partial<BriefFields>): string | undefined {
  const { from, to } = f.validity ?? {};
  if (from && to) return `Vigencia: del ${ymdToLocal(from)} al ${ymdToLocal(to)}.`;
  if (to) return `Vigencia: hasta el ${ymdToLocal(to)}.`;
  if (from) return `Vigencia: desde el ${ymdToLocal(from)}.`;
  return undefined;
}

function build(
  id: TemplateId,
  f: Partial<BriefFields>,
): Partial<Record<CopyField, string | undefined>> {
  if (id === 'directo')
    return {
      headline: join([f.product, f.benefit], ': '),
      body: f.message,
      description: f.offer,
      cta: f.cta,
    };
  return {
    headline: join([f.offer, f.product], ' en '),
    body: join([f.message, f.conditions], ' '),
    description: join([validityText(f), f.conditions], ' '),
    cta: f.cta,
  };
}

const ALL_FIELDS: readonly CopyField[] = ['headline', 'body', 'description', 'cta'];

/** Contenido inicial: solo los campos que usa el canal del brief (todos si el brief aún no tiene canal) y con dato. */
export function applyTemplate(id: TemplateId, fields: Partial<BriefFields>): CopyContent {
  const full = build(id, fields);
  const out: Partial<Record<CopyField, string>> = {};
  for (const k of fields.channel ? CHANNEL_FIELDS[fields.channel] : ALL_FIELDS) {
    const v = full[k];
    if (v !== undefined && v.trim() !== '') out[k] = v.trim();
  }
  return out;
}
