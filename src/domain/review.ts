import { invalid, valid, type Validation } from './validation';

/**
 * Revisión de calidad (S4.1) según la metodología Copy & Creative Intelligence (documento del propietario,
 * 2026-11-23): matriz de 8 dimensiones sobre 100, checklist de 12 puntos, hallazgos con 4 elementos, y DOS filtros
 * independientes (creativo y comercial) que deben estar aprobados para poder publicar. La califica una PERSONA: la app
 * calcula puntaje, banda y veredicto, pero no inventa calificaciones ni hechos comerciales (SKU, precios, vigencias).
 * Es independiente del puntaje automático por reglas (Q-5), que sigue vigente. La revisión no publica nada.
 * SUPUESTOS de Claude (reversibles): ≥90 APROBADO; 80–89 APROBADO CON AJUSTES; <80 RECHAZADO; solo «APROBADO» con
 * ambos filtros aprobados es publicable; un hallazgo bloqueante fuerza RECHAZADO; una revisión por copy o pieza.
 */
export const DIMENSIONS = [
  {
    id: 'claridad',
    label: 'Claridad del mensaje',
    max: 15,
    hint: '¿Se entiende inmediatamente qué se ofrece?',
  },
  {
    id: 'titular',
    label: 'Fuerza del titular',
    max: 15,
    hint: '¿Captura atención y despierta interés?',
  },
  {
    id: 'beneficio',
    label: 'Beneficio y persuasión',
    max: 15,
    hint: '¿Explica por qué conviene comprar?',
  },
  {
    id: 'propuesta',
    label: 'Propuesta comercial',
    max: 15,
    hint: '¿La oferta es atractiva y está bien comunicada?',
  },
  {
    id: 'cta',
    label: 'CTA y conversión',
    max: 10,
    hint: '¿La acción es clara, concreta y visible?',
  },
  {
    id: 'ux',
    label: 'UX y legibilidad',
    max: 10,
    hint: '¿Se entiende y se lee bien en el formato?',
  },
  {
    id: 'marca',
    label: 'Coherencia de marca',
    max: 10,
    hint: '¿El tono y la comunicación son consistentes?',
  },
  {
    id: 'precision',
    label: 'Precisión y cumplimiento',
    max: 10,
    hint: '¿Descuentos, vigencias y restricciones son correctos?',
  },
] as const;
export type DimensionId = (typeof DIMENSIONS)[number]['id'];

export const CHECKLIST = [
  'El objetivo comercial está definido.',
  'El producto y la oferta son correctos.',
  'El titular comunica el principal atractivo.',
  'El beneficio para el cliente es evidente.',
  'El texto es claro, natural y fácil de entender.',
  'La promoción no utiliza afirmaciones engañosas.',
  'El CTA indica claramente qué hacer.',
  'El diseño tiene jerarquía visual.',
  'El arte es legible en móvil.',
  'Las condiciones y la vigencia son visibles.',
  'El mensaje corresponde al canal.',
  'La URL o destino del CTA funciona.',
] as const;

export const COMMERCIAL_CHECKS = [
  'El SKU o los productos participan en la promoción.',
  'El porcentaje y el precio son correctos.',
  'La vigencia es correcta.',
  'Hay disponibilidad.',
  'Las restricciones están comunicadas.',
  'El mensaje es consistente entre canales.',
] as const;

export const TARGET_TYPES = ['copy', 'pieza'] as const;
export type ReviewTargetType = (typeof TARGET_TYPES)[number];
export const FILTER_STATES = ['pendiente', 'aprobado', 'rechazado'] as const;
export type FilterState = (typeof FILTER_STATES)[number];
export const FILTER_LABELS: Readonly<Record<FilterState, string>> = {
  pendiente: 'Pendiente',
  aprobado: 'Aprobado',
  rechazado: 'Rechazado',
};

export const REVIEW_ID = /^rev_[A-Za-z0-9_-]{8,64}$/;
export const MAX_REVIEWS = 2_000;
export const MAX_REVIEW_FINDINGS = 30;
export const MAX_FINDING_TEXT = 500;
export const MAX_REVIEWER = 60;

export interface ReviewFinding {
  /** Qué está mal. */
  readonly hallazgo: string;
  /** Por qué importa. */
  readonly impacto: string;
  /** Qué hacer. */
  readonly recomendacion: string;
  /** Texto propuesto (opcional). */
  readonly correccion?: string;
  /** Impide publicar sin importar el puntaje (error comercial crítico). */
  readonly bloqueante: boolean;
}

export const STAGES = ['creacion', 'validacion', 'aprobacion'] as const;
export type ReviewStage = (typeof STAGES)[number];
export const STAGE_LABELS: Readonly<Record<ReviewStage, string>> = {
  creacion: 'Creación',
  validacion: 'Validación',
  aprobacion: 'Aprobación',
};
export const FINAL_STATES = ['pendiente', 'aprobado', 'rechazado'] as const;
export type FinalApproval = (typeof FINAL_STATES)[number];
export const FINAL_LABELS: Readonly<Record<FinalApproval, string>> = {
  pendiente: 'Pendiente',
  aprobado: 'Liberada para publicar',
  rechazado: 'Rechazada',
};

export interface ReviewRecord {
  readonly id: string; // rev_…
  readonly targetType: ReviewTargetType;
  readonly targetId: string;
  readonly targetLabel: string;
  /** `null` = dimensión aún sin calificar. */
  readonly scores: Readonly<Record<DimensionId, number | null>>;
  readonly checklist: readonly boolean[];
  readonly commercial: readonly boolean[];
  readonly findings: readonly ReviewFinding[];
  readonly creativeFilter: FilterState;
  readonly commercialFilter: FilterState;
  readonly reviewer?: string;
  /** Etapa del flujo Creación → Validación → Aprobación (S4.2). Antes de S4.2 todo era «validacion». */
  readonly stage: ReviewStage;
  /** Aprobación final de una persona (sin cuentas: se registra el nombre). Distinta de «publicable» (calculado). */
  readonly finalApproval: FinalApproval;
  readonly approver?: string;
  readonly createdAt: string;
  readonly updatedAt: string;
}

export type ReviewVerdict = 'pendiente' | 'aprobado' | 'aprobado_con_ajustes' | 'rechazado';
export const VERDICT_LABELS: Readonly<Record<ReviewVerdict, string>> = {
  pendiente: 'PENDIENTE (falta información)',
  aprobado: 'APROBADO',
  aprobado_con_ajustes: 'APROBADO CON AJUSTES',
  rechazado: 'RECHAZADO',
};

export interface ReviewSummary {
  readonly score: number | null;
  readonly band: string;
  readonly verdict: ReviewVerdict;
  readonly blocking: number;
  readonly checklistDone: number;
  readonly publishable: boolean;
  /** Qué falta o bloquea para publicar, en español. */
  readonly reasons: readonly string[];
}

export function bandOf(score: number): string {
  return score >= 90
    ? 'Excelente'
    : score >= 80
      ? 'Bueno: ajustes menores'
      : score >= 70
        ? 'Requiere correcciones'
        : 'Requiere replanteamiento';
}

export function summarizeReview(
  r: Pick<
    ReviewRecord,
    'scores' | 'checklist' | 'findings' | 'creativeFilter' | 'commercialFilter'
  >,
): ReviewSummary {
  const missing = DIMENSIONS.filter((d) => r.scores[d.id] === null);
  const score =
    missing.length === 0 ? DIMENSIONS.reduce((a, d) => a + (r.scores[d.id] ?? 0), 0) : null;
  const blocking = r.findings.filter((f) => f.bloqueante).length;
  const verdict: ReviewVerdict =
    blocking > 0
      ? 'rechazado'
      : score === null
        ? 'pendiente'
        : score >= 90
          ? 'aprobado'
          : score >= 80
            ? 'aprobado_con_ajustes'
            : 'rechazado';
  const reasons: string[] = [];
  if (blocking > 0) reasons.push(`Hay ${String(blocking)} hallazgo(s) bloqueante(s).`);
  if (score === null)
    reasons.push(
      `Faltan calificar ${String(missing.length)} dimensión(es): no hay aprobación definitiva.`,
    );
  else if (verdict === 'aprobado_con_ajustes')
    reasons.push('Aplica los ajustes y vuelve a revisar.');
  else if (verdict === 'rechazado' && blocking === 0) reasons.push('El puntaje es menor a 80.');
  if (r.creativeFilter !== 'aprobado') reasons.push('El filtro creativo no está aprobado.');
  if (r.commercialFilter !== 'aprobado') reasons.push('El filtro comercial no está aprobado.');
  return {
    score,
    band: score === null ? 'Sin calificar' : bandOf(score),
    verdict,
    blocking,
    checklistDone: r.checklist.filter(Boolean).length,
    publishable:
      verdict === 'aprobado' &&
      r.creativeFilter === 'aprobado' &&
      r.commercialFilter === 'aprobado',
    reasons,
  };
}

export interface ReviewInput {
  readonly scores: Readonly<Record<string, unknown>>;
  readonly checklist: readonly unknown[];
  readonly commercial: readonly unknown[];
  readonly findings: readonly unknown[];
  readonly creativeFilter: unknown;
  readonly commercialFilter: unknown;
  readonly reviewer?: unknown;
  readonly stage?: unknown;
  readonly finalApproval?: unknown;
  readonly approver?: unknown;
}

const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const isIso = (v: unknown): v is string =>
  typeof v === 'string' && ISO.test(v) && !Number.isNaN(Date.parse(v));
const text = (v: unknown, min: number): v is string =>
  typeof v === 'string' && v.trim().length >= min && [...v].length <= MAX_FINDING_TEXT;

type Body = Pick<
  ReviewRecord,
  | 'scores'
  | 'checklist'
  | 'commercial'
  | 'findings'
  | 'creativeFilter'
  | 'commercialFilter'
  | 'reviewer'
  | 'stage'
  | 'finalApproval'
  | 'approver'
>;

/** Valida y normaliza el contenido editable. Aplica las reglas de los filtros. */
export function validateReviewBody(input: ReviewInput): Validation<Body> {
  const scores = {} as Record<DimensionId, number | null>;
  for (const d of DIMENSIONS) {
    const v = input.scores[d.id];
    if (v === null || v === undefined || v === '') scores[d.id] = null;
    else if (typeof v === 'number' && Number.isFinite(v) && v >= 0 && v <= d.max)
      scores[d.id] = Math.round(v * 10) / 10;
    else return invalid(`«${d.label}» debe estar entre 0 y ${String(d.max)}.`);
  }
  if (
    input.checklist.length !== CHECKLIST.length ||
    input.checklist.some((x) => typeof x !== 'boolean')
  )
    return invalid('El checklist no es válido.');
  if (
    input.commercial.length !== COMMERCIAL_CHECKS.length ||
    input.commercial.some((x) => typeof x !== 'boolean')
  )
    return invalid('El filtro comercial no es válido.');
  if (input.findings.length > MAX_REVIEW_FINDINGS)
    return invalid(`Se admiten hasta ${String(MAX_REVIEW_FINDINGS)} hallazgos.`);
  const findings: ReviewFinding[] = [];
  for (const f of input.findings) {
    if (
      !isObject(f) ||
      !text(f['hallazgo'], 1) ||
      !text(f['impacto'], 1) ||
      !text(f['recomendacion'], 1) ||
      (f['correccion'] !== undefined && f['correccion'] !== '' && !text(f['correccion'], 1)) ||
      typeof f['bloqueante'] !== 'boolean'
    )
      return invalid(
        'Cada hallazgo necesita hallazgo, impacto y recomendación (hasta 500 caracteres).',
      );
    const correccion = typeof f['correccion'] === 'string' ? f['correccion'].trim() : '';
    findings.push({
      hallazgo: f['hallazgo'].trim(),
      impacto: f['impacto'].trim(),
      recomendacion: f['recomendacion'].trim(),
      ...(correccion.length > 0 ? { correccion } : {}),
      bloqueante: f['bloqueante'],
    });
  }
  if (
    !FILTER_STATES.includes(input.creativeFilter as FilterState) ||
    !FILTER_STATES.includes(input.commercialFilter as FilterState)
  )
    return invalid('El estado de un filtro no es válido.');
  const creativeFilter = input.creativeFilter as FilterState;
  const commercialFilter = input.commercialFilter as FilterState;
  const reviewer = typeof input.reviewer === 'string' ? input.reviewer.trim() : '';
  if ([...reviewer].length > MAX_REVIEWER)
    return invalid(`El nombre de quien revisa admite hasta ${String(MAX_REVIEWER)} caracteres.`);
  const stage = input.stage ?? 'validacion';
  const finalApproval = input.finalApproval ?? 'pendiente';
  if (!STAGES.includes(stage as ReviewStage)) return invalid('La etapa no es válida.');
  if (!FINAL_STATES.includes(finalApproval as FinalApproval))
    return invalid('La aprobación final no es válida.');
  const approver = typeof input.approver === 'string' ? input.approver.trim() : '';
  if ([...approver].length > MAX_REVIEWER)
    return invalid(`El nombre de quien aprueba admite hasta ${String(MAX_REVIEWER)} caracteres.`);
  if (creativeFilter === 'aprobado') {
    if (DIMENSIONS.some((d) => scores[d.id] === null))
      return invalid('Para aprobar el filtro creativo califica las 8 dimensiones.');
    if (findings.some((f) => f.bloqueante))
      return invalid('No se puede aprobar el filtro creativo con hallazgos bloqueantes.');
  }
  if (commercialFilter === 'aprobado' && input.commercial.some((x) => x !== true))
    return invalid('Para aprobar el filtro comercial confirma los 6 puntos comerciales.');
  if (finalApproval === 'aprobado') {
    if (
      !summarizeReview({
        scores,
        checklist: input.checklist as boolean[],
        findings,
        creativeFilter,
        commercialFilter,
      }).publishable
    )
      return invalid(
        'Para liberar la pieza, la revisión debe ser publicable (aprobada, con ambos filtros aprobados).',
      );
    if (approver === '')
      return invalid('Para liberar la pieza escribe el nombre de quien aprueba.');
  }
  return valid({
    scores,
    checklist: input.checklist as boolean[],
    commercial: input.commercial as boolean[],
    findings,
    creativeFilter,
    commercialFilter,
    ...(reviewer.length > 0 ? { reviewer } : {}),
    stage: stage as ReviewStage,
    finalApproval: finalApproval as FinalApproval,
    ...(approver.length > 0 ? { approver } : {}),
  });
}

export function validateReviewRecord(raw: unknown): Validation<ReviewRecord> {
  const bad = invalid<ReviewRecord>('La revisión guardada no es válida.');
  if (!isObject(raw)) return bad;
  if (typeof raw['id'] !== 'string' || !REVIEW_ID.test(raw['id'])) return bad;
  if (!TARGET_TYPES.includes(raw['targetType'] as ReviewTargetType)) return bad;
  if (
    typeof raw['targetId'] !== 'string' ||
    raw['targetId'].length < 4 ||
    raw['targetId'].length > 80
  )
    return bad;
  if (
    typeof raw['targetLabel'] !== 'string' ||
    raw['targetLabel'].length === 0 ||
    raw['targetLabel'].length > 200
  )
    return bad;
  if (!isIso(raw['createdAt']) || !isIso(raw['updatedAt'])) return bad;
  if (
    !isObject(raw['scores']) ||
    !Array.isArray(raw['checklist']) ||
    !Array.isArray(raw['commercial']) ||
    !Array.isArray(raw['findings'])
  )
    return bad;
  const body = validateReviewBody({
    scores: raw['scores'],
    checklist: raw['checklist'],
    commercial: raw['commercial'],
    findings: raw['findings'],
    creativeFilter: raw['creativeFilter'],
    commercialFilter: raw['commercialFilter'],
    reviewer: raw['reviewer'],
    stage: raw['stage'],
    finalApproval: raw['finalApproval'],
    approver: raw['approver'],
  });
  if (!body.ok) return bad;
  return valid({
    id: raw['id'],
    targetType: raw['targetType'] as ReviewTargetType,
    targetId: raw['targetId'],
    targetLabel: raw['targetLabel'],
    ...body.value,
    createdAt: raw['createdAt'],
    updatedAt: raw['updatedAt'],
  });
}

export const compareReviewsNewestFirst = (a: ReviewRecord, b: ReviewRecord): number =>
  a.updatedAt < b.updatedAt ? 1 : a.updatedAt > b.updatedAt ? -1 : a.id < b.id ? 1 : -1;

/** Revisión vacía para empezar a calificar. */
export const emptyReviewBody = (): ReviewInput => ({
  scores: {},
  checklist: CHECKLIST.map(() => false),
  commercial: COMMERCIAL_CHECKS.map(() => false),
  findings: [],
  creativeFilter: 'pendiente',
  commercialFilter: 'pendiente',
});
