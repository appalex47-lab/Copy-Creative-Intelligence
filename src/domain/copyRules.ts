import type { Channel } from './brief';
import { COPY_FIELDS, COPY_FIELD_LABELS, type CopyContent, type CopyField } from './copy';

/**
 * Reglas deterministas de copy (S2.5a). Decisiones Q-1, Q-2 y Q-5 del propietario (aprobadas bajo delegación,
 * revocables; ver evidence/CCI_FASE1_S1_13…/01_Q1_Q2_Q5). Sin IA, sin red: misma entrada → mismo resultado.
 * SUPUESTOS de Claude (reversibles) al aplicarlas al modelo de copy de cuatro campos:
 *  - «asunto/título/H1/titular» = Titular; «preheader/descripción» = Descripción; «cuerpo/mensaje/texto» = Texto.
 *  - Una regla de canal con límite para un campo solo lo evalúa si el campo tiene texto.
 *  - Deducción = peso de la categoría × factor de severidad (mayor 1, menor 0.5, aviso 0), con tope por categoría
 *    igual a su peso; una crítica además limita la nota a 59.
 * Las longitudes por canal son orientativas y NO están verificadas contra las plataformas.
 */
export type Severity = 'critica' | 'mayor' | 'menor' | 'aviso';
export type Category = 'cumplimiento' | 'precios' | 'marca' | 'claridad' | 'canal' | 'redaccion';

export const CATEGORY_LABELS: Readonly<Record<Category, string>> = {
  cumplimiento: 'Cumplimiento regulatorio/legal',
  precios: 'Precios y promoción',
  marca: 'Marca',
  claridad: 'Claridad del mensaje y CTA',
  canal: 'Adecuación al canal',
  redaccion: 'Ortografía y redacción',
};
export const CATEGORY_WEIGHTS: Readonly<Record<Category, number>> = {
  cumplimiento: 25,
  precios: 25,
  marca: 15,
  claridad: 15,
  canal: 10,
  redaccion: 10,
};
export const SEVERITY_FACTOR: Readonly<Record<Severity, number>> = {
  critica: 1,
  mayor: 1,
  menor: 0.5,
  aviso: 0,
};
export const SEVERITY_LABELS: Readonly<Record<Severity, string>> = {
  critica: 'Crítica',
  mayor: 'Mayor',
  menor: 'Menor',
  aviso: 'Aviso',
};
export const CRITICAL_SCORE_CAP = 59;
export const THRESHOLDS = { apto: 85, revisar: 60 } as const;
/** Q-1: tolerancia por defecto, en puntos porcentuales. */
export const DEFAULT_TOLERANCE_PP = 0.5;

export interface ChannelRule {
  readonly limits: Readonly<Partial<Record<CopyField, number>>>;
  readonly cta: 'obligatorio' | 'recomendado';
}
export const CHANNEL_RULES: Readonly<Record<Channel, ChannelRule>> = {
  Ecommerce: { limits: { headline: 70, description: 300 }, cta: 'obligatorio' },
  App: { limits: { headline: 40, body: 120 }, cta: 'obligatorio' },
  WhatsApp: { limits: { body: 600 }, cta: 'obligatorio' },
  Email: { limits: { headline: 60, description: 100 }, cta: 'obligatorio' },
  'Redes sociales': { limits: { body: 280 }, cta: 'recomendado' },
  Banners: { limits: { headline: 40 }, cta: 'obligatorio' },
  'Landing pages': { limits: { headline: 70 }, cta: 'obligatorio' },
};

export interface Legend {
  readonly text: string;
  /** Vacío = aplica a todos los canales. */
  readonly channels: readonly Channel[];
  readonly required: boolean;
  readonly active: boolean;
}
export interface BrandTerm {
  readonly text: string;
  readonly kind: 'prohibido' | 'preferido';
  readonly severity: Severity;
  readonly suggestion?: string;
}
export interface RulesConfig {
  readonly legends: readonly Legend[];
  readonly brandTerms: readonly BrandTerm[];
  readonly tolerancePp: number;
}

/** Plantilla editable (NO validada): ver evidence S2.1/01_DECISIONES_LEYENDAS_Y_TERMINOS. Las leyendas parten vacías. */
export const DEFAULT_BRAND_TERMS: readonly BrandTerm[] = [
  { text: 'cura', kind: 'prohibido', severity: 'mayor' },
  { text: 'milagro', kind: 'prohibido', severity: 'mayor' },
  { text: 'garantizado', kind: 'prohibido', severity: 'mayor' },
  { text: '100% efectivo', kind: 'prohibido', severity: 'mayor' },
  { text: 'sin efectos secundarios', kind: 'prohibido', severity: 'critica' },
  { text: 'adelgaza rápido', kind: 'prohibido', severity: 'mayor' },
  { text: 'el mejor', kind: 'prohibido', severity: 'menor' },
];
export const DEFAULT_CONFIG: RulesConfig = {
  legends: [],
  brandTerms: DEFAULT_BRAND_TERMS,
  tolerancePp: DEFAULT_TOLERANCE_PP,
};

export interface Finding {
  readonly ruleId: string;
  readonly category: Category;
  readonly severity: Severity;
  readonly message: string;
  readonly evidence?: string;
  readonly field?: CopyField;
}
export type Verdict = 'apto' | 'revisar' | 'no_apto';
export interface Evaluation {
  readonly score: number;
  readonly verdict: Verdict;
  /** Hay al menos una crítica: bloquea la aprobación. */
  readonly blocked: boolean;
  readonly findings: readonly Finding[];
  readonly deductions: Readonly<Record<Category, number>>;
}

/** Minúsculas y sin acentos, para comparar sin distinguir mayúsculas ni acentos. */
export const normalize = (s: string): string =>
  s.normalize('NFD').replace(/[̀-ͯ]/g, '').toLowerCase();

const escapeRegExp = (s: string): string => s.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

/** Coincidencia por palabra completa (ni letra ni dígito pegados a los lados). */
export function containsTerm(text: string, term: string): boolean {
  const t = normalize(term).trim();
  if (t === '') return false;
  const re = new RegExp(`(?<![\\p{L}\\p{N}])${escapeRegExp(t)}(?![\\p{L}\\p{N}])`, 'u');
  return re.test(normalize(text));
}

/** Porcentajes mencionados en un texto: «20%», «20 %», «12.5%», «12,5 %». */
export function extractPercents(text: string): readonly number[] {
  const out: number[] = [];
  for (const m of text.matchAll(/(\d{1,3}(?:[.,]\d{1,2})?)\s?%/g)) {
    const n = Number((m[1] ?? '').replace(',', '.'));
    if (Number.isFinite(n)) out.push(n);
  }
  return out;
}

const fieldsWithText = (c: CopyContent): readonly CopyField[] =>
  COPY_FIELDS.filter((f) => (c[f] ?? '').trim() !== '');
const allText = (c: CopyContent): string =>
  fieldsWithText(c)
    .map((f) => c[f] ?? '')
    .join('\n');

export function evaluateCopy(
  brief: { readonly channel: Channel; readonly offer?: string | undefined },
  content: CopyContent,
  config: RulesConfig = DEFAULT_CONFIG,
): Evaluation {
  const findings: Finding[] = [];
  const add = (f: Finding) => findings.push(f);
  const text = allText(content);
  const rule = CHANNEL_RULES[brief.channel];

  // Canal (Q-2): longitudes.
  for (const f of fieldsWithText(content)) {
    const limit = rule.limits[f];
    const len = (content[f] ?? '').length;
    if (limit !== undefined && len > limit)
      add({
        ruleId: `canal.longitud.${f}`,
        category: 'canal',
        severity: 'mayor',
        field: f,
        message: `${COPY_FIELD_LABELS[f]} excede el límite orientativo de ${brief.channel} (${len} de ${limit} caracteres).`,
      });
  }

  // CTA (Q-2).
  if ((content.cta ?? '').trim() === '')
    add({
      ruleId: 'claridad.cta',
      category: 'claridad',
      severity: rule.cta === 'obligatorio' ? 'mayor' : 'aviso',
      field: 'cta',
      message:
        rule.cta === 'obligatorio'
          ? `Falta el CTA, obligatorio en ${brief.channel}.`
          : `Falta el CTA, recomendado en ${brief.channel}.`,
    });

  // Marca: términos prohibidos (por palabra completa, sin mayúsculas ni acentos). Solo se sugiere, nunca se reescribe.
  for (const term of config.brandTerms) {
    if (term.kind !== 'prohibido' || !containsTerm(text, term.text)) continue;
    add({
      ruleId: `marca.prohibido.${normalize(term.text)}`,
      category: 'marca',
      severity: term.severity,
      evidence: term.text,
      message: `Contiene el término prohibido «${term.text}».${
        term.suggestion ? ` Sugerencia: ${term.suggestion}.` : ''
      }`,
    });
  }

  // Cumplimiento: leyendas obligatorias activas que aplican al canal y no aparecen.
  for (const legend of config.legends) {
    if (!legend.active || !legend.required) continue;
    if (legend.channels.length > 0 && !legend.channels.includes(brief.channel)) continue;
    if (!normalize(text).includes(normalize(legend.text).trim()))
      add({
        ruleId: 'cumplimiento.leyenda',
        category: 'cumplimiento',
        severity: 'critica',
        evidence: legend.text,
        message: `Falta la leyenda obligatoria: «${legend.text}».`,
      });
  }

  // Precios (Q-1): porcentajes del copy contra los del brief, con tolerancia en puntos porcentuales.
  const copyPercents = extractPercents(text);
  if (copyPercents.length > 0) {
    const briefPercents = extractPercents(brief.offer ?? '');
    for (const p of copyPercents) {
      if (briefPercents.length === 0)
        add({
          ruleId: 'precios.porcentaje_sin_respaldo',
          category: 'precios',
          severity: 'mayor',
          evidence: `${p}%`,
          message: `El copy menciona ${p}% pero la oferta del brief no indica ningún porcentaje.`,
        });
      else if (!briefPercents.some((b) => Math.abs(b - p) <= config.tolerancePp))
        add({
          ruleId: 'precios.porcentaje_distinto',
          category: 'precios',
          severity: 'critica',
          evidence: `${p}%`,
          message: `El copy dice ${p}% y el brief indica ${briefPercents.join(' / ')}% (tolerancia ${config.tolerancePp} pp).`,
        });
    }
  }

  // Redacción (reglas mecánicas; no hay corrector ortográfico).
  for (const f of fieldsWithText(content)) {
    const v = content[f] ?? '';
    if (/ {2,}/.test(v))
      add({
        ruleId: 'redaccion.espacios',
        category: 'redaccion',
        severity: 'menor',
        field: f,
        message: `${COPY_FIELD_LABELS[f]} tiene espacios dobles.`,
      });
    if (/[!?]{2,}/.test(v))
      add({
        ruleId: 'redaccion.signos_repetidos',
        category: 'redaccion',
        severity: 'menor',
        field: f,
        message: `${COPY_FIELD_LABELS[f]} repite signos de admiración o interrogación.`,
      });
    const letters = v.replace(/[^\p{L}]/gu, '');
    if (f === 'headline' && letters.length >= 8 && letters === letters.toUpperCase())
      add({
        ruleId: 'redaccion.mayusculas',
        category: 'redaccion',
        severity: 'menor',
        field: f,
        message: 'El titular está completo en mayúsculas.',
      });
  }

  const deductions = Object.fromEntries(
    (Object.keys(CATEGORY_WEIGHTS) as Category[]).map((c) => {
      const sum = findings
        .filter((x) => x.category === c)
        .reduce((a, x) => a + CATEGORY_WEIGHTS[c] * SEVERITY_FACTOR[x.severity], 0);
      return [c, Math.min(sum, CATEGORY_WEIGHTS[c])];
    }),
  ) as Record<Category, number>;
  const blocked = findings.some((x) => x.severity === 'critica');
  let score = Math.max(0, 100 - Object.values(deductions).reduce((a, b) => a + b, 0));
  if (blocked) score = Math.min(score, CRITICAL_SCORE_CAP);
  score = Math.round(score * 100) / 100;
  const verdict: Verdict =
    score >= THRESHOLDS.apto ? 'apto' : score >= THRESHOLDS.revisar ? 'revisar' : 'no_apto';
  return { score, verdict, blocked, findings, deductions };
}
