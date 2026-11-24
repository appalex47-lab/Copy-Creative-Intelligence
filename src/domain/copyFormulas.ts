/**
 * Plantillas de copy (S4.2; etapas 2 y 3 de la metodología CCI). NO es IA: arma borradores combinando únicamente los
 * datos que la persona escribió, con las fórmulas del documento (AIDA, PAS, FAB, 4U, Antes-Después-Puente y
 * Oferta + beneficio + CTA). Nunca inventa descuentos, beneficios ni vigencias; la versión de urgencia solo existe si se
 * indicó una vigencia. Son borradores para editar, no copy final.
 */
export interface FormulaInput {
  readonly product: string;
  readonly need: string;
  readonly benefit: string;
  readonly offer: string;
  readonly differentiator: string;
  readonly cta: string;
  readonly validity: string;
  readonly conditions: string;
}

export interface Draft {
  readonly formula: string;
  readonly concept: string;
  readonly headline: string;
  readonly body: string;
  readonly cta: string;
}

const t = (s: string) => s.trim();
const join = (parts: readonly string[], sep: string) =>
  parts
    .map(t)
    .filter((x) => x.length > 0)
    .join(sep);
const sentence = (s: string) => {
  const x = t(s);
  return x === '' ? '' : /[.!?]$/.test(x) ? x : `${x}.`;
};

export const FORMULAS = [
  'AIDA',
  'PAS',
  'FAB',
  '4U',
  'BAB',
  'Oferta + beneficio + CTA',
  'Urgencia',
] as const;
export type Formula = (typeof FORMULAS)[number];

export function draftFor(formula: Formula, i: FormulaInput): Draft | null {
  const cta = t(i.cta);
  const cond = sentence(i.conditions);
  const tail = join([sentence(i.validity === '' ? '' : `Vigencia: ${t(i.validity)}`), cond], ' ');
  switch (formula) {
    case 'AIDA':
      if (!t(i.offer) && !t(i.benefit)) return null;
      return {
        formula,
        concept: 'Atención → interés → deseo → acción',
        headline: join([i.offer, i.product], ' en '),
        body: join([sentence(i.benefit), sentence(i.differentiator), tail], ' '),
        cta,
      };
    case 'PAS':
      if (!t(i.need)) return null;
      return {
        formula,
        concept: 'Problema → agitación → solución',
        headline: sentence(i.need).replace(/\.$/, '?'),
        body: join(
          [
            sentence(`${t(i.product)}${t(i.benefit) ? `: ${t(i.benefit)}` : ''}`),
            sentence(i.offer),
            tail,
          ],
          ' ',
        ),
        cta,
      };
    case 'FAB':
      if (!t(i.product) || !t(i.benefit)) return null;
      return {
        formula,
        concept: 'Característica → ventaja → beneficio',
        headline: t(i.product),
        body: join([sentence(i.differentiator), sentence(i.benefit), sentence(i.offer), tail], ' '),
        cta,
      };
    case '4U':
      if (!t(i.benefit) && !t(i.offer)) return null;
      return {
        formula,
        concept: 'Útil, único, ultraespecífico y urgente (solo si hay vigencia)',
        headline: join([i.benefit, i.offer], ' · '),
        body: join([sentence(i.differentiator), tail], ' '),
        cta,
      };
    case 'BAB':
      if (!t(i.need) || !t(i.benefit)) return null;
      return {
        formula,
        concept: 'Antes → después → puente',
        headline: sentence(i.benefit).replace(/\.$/, ''),
        body: join(
          [
            sentence(`Antes: ${t(i.need)}`),
            sentence(`Después: ${t(i.benefit)}`),
            sentence(`Con ${t(i.product)}${t(i.offer) ? `: ${t(i.offer)}` : ''}`),
            tail,
          ],
          ' ',
        ),
        cta,
      };
    case 'Oferta + beneficio + CTA':
      if (!t(i.offer)) return null;
      return {
        formula,
        concept: 'Directa, para promociones comerciales',
        headline: join([i.offer, i.product], ' en '),
        body: join([sentence(i.benefit), tail], ' '),
        cta,
      };
    case 'Urgencia':
      if (!t(i.validity) || !t(i.offer)) return null;
      return {
        formula,
        concept: 'Solo cuando la vigencia realmente está por terminar',
        headline: `Últimos días: ${t(i.offer)}${t(i.product) ? ` en ${t(i.product)}` : ''}`,
        body: join([sentence(`Vigencia: ${t(i.validity)}`), cond], ' '),
        cta,
      };
  }
}

/** Borradores posibles con los datos dados (los que faltan de datos se omiten). */
export function draftAll(i: FormulaInput): readonly Draft[] {
  return FORMULAS.flatMap((f) => {
    const d = draftFor(f, i);
    return d ? [d] : [];
  });
}

export const MESSAGE_ARCHITECTURE: readonly { readonly step: string; readonly guide: string }[] = [
  { step: 'Captar la atención', guide: 'Comunica el principal atractivo de la promoción.' },
  { step: 'Despertar interés', guide: 'Explica qué gana el cliente y por qué le conviene.' },
  {
    step: 'Justificar la compra',
    guide: 'Descuento, precio especial, regalo, bonificación o ventaja real.',
  },
  {
    step: 'Provocar acción',
    guide: 'Comprar ahora, descubre la promoción, aprovecha el descuento.',
  },
  {
    step: 'Eliminar incertidumbre',
    guide: 'Vigencia, restricciones, productos participantes y condiciones aplicables.',
  },
];

export const CHANNEL_PRIORITIES: readonly {
  readonly format: string;
  readonly goal: string;
  readonly priority: string;
}[] = [
  { format: 'Banner principal', goal: 'Captar atención', priority: 'Titular + beneficio + CTA' },
  { format: 'Banner secundario', goal: 'Generar interés', priority: 'Oferta + diferenciador' },
  { format: 'Arte para redes', goal: 'Detener el scroll', priority: 'Hook + atractivo visual' },
  {
    format: 'WhatsApp',
    goal: 'Generar respuesta',
    priority: 'Personalización + beneficio + acción',
  },
  { format: 'Email', goal: 'Conseguir apertura y clic', priority: 'Asunto + propuesta + CTA' },
  { format: 'Landing page', goal: 'Convertir', priority: 'Argumentos + confianza + productos' },
  {
    format: 'Grid de productos',
    goal: 'Facilitar elección',
    priority: 'Nombre + precio + incentivo',
  },
  { format: 'Publicidad pagada', goal: 'Generar resultados', priority: 'Hook + oferta + CTA' },
];

export const UX_HIERARCHY: readonly string[] = [
  '¿Qué me están ofreciendo?',
  '¿Qué beneficio obtengo?',
  '¿Qué tengo que hacer?',
  '¿Qué condiciones aplican?',
];
