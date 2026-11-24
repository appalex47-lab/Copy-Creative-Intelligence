import { CHANNELS, type Channel } from './brief';
import {
  CATEGORY_WEIGHTS,
  CRITICAL_SCORE_CAP,
  SEVERITY_FACTOR,
  THRESHOLDS,
  evaluateCopy,
  type Category,
  type RulesConfig,
  type Severity,
  type Verdict,
} from './copyRules';
import { RESOURCE_ID, countUncertain, type ResourceRecord } from './resource';
import { invalid, valid, type Validation } from './validation';

/**
 * Pieza creativa (S3.4; funciones 5, 6, 7 y 8 de la Fase 3): una imagen (recurso) con nombre y canal. Se audita con
 * las MISMAS reglas deterministas de los copys, aplicadas al texto de la imagen (el validado por una persona; si no
 * existe, el detectado por OCR, y entonces se avisa). Sin IA de visión (ver FASE3_ALCANCE). Una auditoría no aprueba
 * nada. Cada hallazgo tiene origen (regla / ocr / visual) y un estado que una persona puede cambiar
 * (abierto / resuelto / descartado, con nota); el resto de la auditoría es una foto inmutable.
 * SUPUESTOS de Claude (reversibles): 500 piezas, 50 auditorías por pieza, resolución mínima 600 px de ancho,
 * más de 30 % de palabras dudosas = hallazgo mayor; no aplican a imágenes las reglas de CTA ni de longitud de campo.
 */
export const PIECE_ID = /^pie_[A-Za-z0-9_-]{8,64}$/;
export const PIECE_AUDIT_ID = /^pau_[A-Za-z0-9_-]{8,64}$/;
export const MAX_PIECES = 500;
export const MAX_PIECE_AUDITS = 50;
export const MAX_PIECE_NAME = 120;
export const MAX_NOTE = 300;
export const MIN_WIDTH = 600;
export const UNCERTAIN_RATIO = 0.3;

export const FINDING_ORIGINS = ['regla', 'ocr', 'visual'] as const;
export type FindingOrigin = (typeof FINDING_ORIGINS)[number];
export const FINDING_STATUSES = ['abierto', 'resuelto', 'descartado'] as const;
export type FindingStatus = (typeof FINDING_STATUSES)[number];
export const ORIGIN_LABELS: Readonly<Record<FindingOrigin, string>> = {
  regla: 'regla determinista',
  ocr: 'lectura OCR',
  visual: 'revisión de imagen',
};
export const STATUS_LABELS: Readonly<Record<FindingStatus, string>> = {
  abierto: 'Abierto',
  resuelto: 'Resuelto',
  descartado: 'Descartado',
};

export interface PieceFinding {
  readonly ruleId: string;
  readonly category: Category;
  readonly severity: Severity;
  readonly message: string;
  readonly evidence?: string;
  readonly origin: FindingOrigin;
  readonly status: FindingStatus;
  readonly note?: string;
  readonly resolvedAt?: string;
}

export interface PieceAudit {
  readonly id: string; // pau_…
  /** Qué texto se auditó: validado por persona o solo detectado por OCR. */
  readonly textSource: 'validado' | 'detectado';
  readonly textLength: number;
  readonly score: number;
  readonly verdict: Verdict;
  readonly blocked: boolean;
  readonly findings: readonly PieceFinding[];
  readonly createdAt: string;
}

export interface PieceRecord {
  readonly id: string; // pie_…
  readonly name: string;
  readonly channel: Channel;
  readonly resourceId: string;
  readonly createdAt: string;
  readonly updatedAt: string;
  /** Más reciente primero. */
  readonly audits: readonly PieceAudit[];
}

const CATEGORIES = Object.keys(CATEGORY_WEIGHTS) as Category[];
const SEVERITIES = Object.keys(SEVERITY_FACTOR) as Severity[];
const VERDICTS: readonly Verdict[] = ['apto', 'revisar', 'no_apto'];
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const isIso = (v: unknown): v is string =>
  typeof v === 'string' && ISO.test(v) && !Number.isNaN(Date.parse(v));
const str = (v: unknown, max: number): v is string =>
  typeof v === 'string' && v.length > 0 && [...v].length <= max;

export function validatePieceInput(input: {
  readonly name: unknown;
  readonly channel: unknown;
}): Validation<{ readonly name: string; readonly channel: Channel }> {
  const name = typeof input.name === 'string' ? input.name.trim() : '';
  if (name.length === 0 || [...name].length > MAX_PIECE_NAME)
    return invalid(`El nombre es obligatorio (hasta ${String(MAX_PIECE_NAME)} caracteres).`);
  if (!CHANNELS.includes(input.channel as Channel)) return invalid('Elige un canal válido.');
  return valid({ name, channel: input.channel as Channel });
}

const dropDerived = (ruleId: string) =>
  ruleId === 'claridad.cta' || ruleId.startsWith('canal.longitud.');

/** Evalúa una pieza. No toca el original. Devuelve error si todavía no hay texto que auditar. */
export function evaluatePiece(
  channel: Channel,
  resource: ResourceRecord,
  config: RulesConfig,
): Validation<Omit<PieceAudit, 'id' | 'createdAt'>> {
  const reviewed = resource.reviewedText?.trim() ?? '';
  const detected = resource.ocr?.text.trim() ?? '';
  const textSource: 'validado' | 'detectado' = reviewed.length > 0 ? 'validado' : 'detectado';
  const text = reviewed.length > 0 ? reviewed : detected;
  if (text.length === 0)
    return invalid('Primero lee el texto con OCR o escribe el texto validado de la imagen.');
  const base = evaluateCopy({ channel }, { body: text }, config);
  const findings: PieceFinding[] = base.findings
    .filter((f) => !dropDerived(f.ruleId))
    .map((f) => ({
      ruleId: f.ruleId,
      category: f.category,
      severity: f.severity,
      message: f.message,
      ...(f.evidence !== undefined ? { evidence: f.evidence } : {}),
      origin: 'regla' as const,
      status: 'abierto' as const,
    }));
  if (textSource === 'detectado') {
    findings.push({
      ruleId: 'ocr.sin_validar',
      category: 'claridad',
      severity: 'aviso',
      message: 'Se auditó el texto detectado por OCR; ninguna persona lo ha validado todavía.',
      origin: 'ocr',
      status: 'abierto',
    });
    const words = resource.ocr?.words ?? [];
    const dudosas = countUncertain(words);
    if (dudosas > 0)
      findings.push({
        ruleId: 'ocr.palabras_dudosas',
        category: 'claridad',
        severity: dudosas / words.length > UNCERTAIN_RATIO ? 'mayor' : 'aviso',
        message: `${String(dudosas)} de ${String(words.length)} palabras detectadas son dudosas: revísalas contra la imagen.`,
        origin: 'ocr',
        status: 'abierto',
      });
  }
  if (resource.width < MIN_WIDTH)
    findings.push({
      ruleId: 'visual.resolucion',
      category: 'claridad',
      severity: 'menor',
      message: `La imagen mide ${String(resource.width)} px de ancho; menos de ${String(MIN_WIDTH)} puede verse borrosa.`,
      origin: 'visual',
      status: 'abierto',
    });
  const deductions = CATEGORIES.map((c) =>
    Math.min(
      findings
        .filter((f) => f.category === c)
        .reduce((a, f) => a + CATEGORY_WEIGHTS[c] * SEVERITY_FACTOR[f.severity], 0),
      CATEGORY_WEIGHTS[c],
    ),
  );
  const blocked = findings.some((f) => f.severity === 'critica');
  let score = Math.max(0, 100 - deductions.reduce((a, b) => a + b, 0));
  if (blocked) score = Math.min(score, CRITICAL_SCORE_CAP);
  score = Math.round(score);
  const verdict: Verdict =
    score >= THRESHOLDS.apto ? 'apto' : score >= THRESHOLDS.revisar ? 'revisar' : 'no_apto';
  return valid({
    textSource,
    textLength: text.length,
    score,
    verdict,
    blocked,
    findings: findings.slice(0, 100),
  });
}

/** Cambia el estado de un hallazgo (decisión humana). Los demás datos de la auditoría no se tocan. */
export function withFindingStatus(
  piece: PieceRecord,
  auditId: string,
  index: number,
  status: FindingStatus,
  note: string,
  at: string,
): Validation<PieceRecord> {
  const audit = piece.audits.find((a) => a.id === auditId);
  const finding = audit?.findings[index];
  if (!audit || !finding) return invalid('El hallazgo no existe.');
  const n = note.trim();
  if ([...n].length > MAX_NOTE)
    return invalid(`La nota admite hasta ${String(MAX_NOTE)} caracteres.`);
  const rest: Record<string, unknown> = { ...finding };
  delete rest['note'];
  delete rest['resolvedAt'];
  const next = {
    ...(rest as unknown as PieceFinding),
    status,
    ...(n.length > 0 ? { note: n } : {}),
    ...(status !== 'abierto' ? { resolvedAt: at } : {}),
  } as PieceFinding;
  return valid({
    ...piece,
    updatedAt: at,
    audits: piece.audits.map((a) =>
      a.id === auditId ? { ...a, findings: a.findings.map((f, i) => (i === index ? next : f)) } : a,
    ),
  });
}

const key = (f: PieceFinding) => `${f.ruleId}|${f.message}`;
/** Diferencia entre dos auditorías de la misma pieza: hallazgos nuevos y desaparecidos. */
export function diffPieceAudits(prev: PieceAudit, cur: PieceAudit) {
  const before = new Set(prev.findings.map(key));
  const after = new Set(cur.findings.map(key));
  return {
    scoreDelta: cur.score - prev.score,
    added: cur.findings.filter((f) => !before.has(key(f))),
    resolved: prev.findings.filter((f) => !after.has(key(f))),
  };
}

export const comparePiecesNewestFirst = (a: PieceRecord, b: PieceRecord): number =>
  a.updatedAt < b.updatedAt ? 1 : a.updatedAt > b.updatedAt ? -1 : a.id < b.id ? 1 : -1;

function validateFinding(raw: unknown): PieceFinding | null {
  if (
    !isObject(raw) ||
    !str(raw['ruleId'], 80) ||
    !CATEGORIES.includes(raw['category'] as Category) ||
    !SEVERITIES.includes(raw['severity'] as Severity) ||
    !str(raw['message'], 600) ||
    (raw['evidence'] !== undefined && !str(raw['evidence'], 300)) ||
    !FINDING_ORIGINS.includes(raw['origin'] as FindingOrigin) ||
    !FINDING_STATUSES.includes(raw['status'] as FindingStatus) ||
    (raw['note'] !== undefined && !str(raw['note'], MAX_NOTE)) ||
    (raw['resolvedAt'] !== undefined && !isIso(raw['resolvedAt']))
  )
    return null;
  return raw as unknown as PieceFinding;
}

function validateAudit(raw: unknown): PieceAudit | null {
  if (
    !isObject(raw) ||
    typeof raw['id'] !== 'string' ||
    !PIECE_AUDIT_ID.test(raw['id']) ||
    (raw['textSource'] !== 'validado' && raw['textSource'] !== 'detectado') ||
    typeof raw['textLength'] !== 'number' ||
    typeof raw['score'] !== 'number' ||
    !Number.isInteger(raw['score']) ||
    raw['score'] < 0 ||
    raw['score'] > 100 ||
    !VERDICTS.includes(raw['verdict'] as Verdict) ||
    typeof raw['blocked'] !== 'boolean' ||
    !isIso(raw['createdAt']) ||
    !Array.isArray(raw['findings']) ||
    raw['findings'].length > 100
  )
    return null;
  const findings: PieceFinding[] = [];
  for (const f of raw['findings'] as unknown[]) {
    const v = validateFinding(f);
    if (!v) return null;
    findings.push(v);
  }
  return { ...(raw as unknown as PieceAudit), findings };
}

export function validatePieceRecord(raw: unknown): Validation<PieceRecord> {
  const bad = invalid<PieceRecord>('La pieza guardada no es válida.');
  if (!isObject(raw)) return bad;
  if (typeof raw['id'] !== 'string' || !PIECE_ID.test(raw['id'])) return bad;
  if (!str(raw['name'], MAX_PIECE_NAME) || !CHANNELS.includes(raw['channel'] as Channel))
    return bad;
  if (typeof raw['resourceId'] !== 'string' || !RESOURCE_ID.test(raw['resourceId'])) return bad;
  if (!isIso(raw['createdAt']) || !isIso(raw['updatedAt'])) return bad;
  if (!Array.isArray(raw['audits']) || raw['audits'].length > MAX_PIECE_AUDITS) return bad;
  const audits: PieceAudit[] = [];
  for (const a of raw['audits'] as unknown[]) {
    const v = validateAudit(a);
    if (!v) return bad;
    audits.push(v);
  }
  return valid({
    id: raw['id'],
    name: raw['name'],
    channel: raw['channel'] as Channel,
    resourceId: raw['resourceId'],
    createdAt: raw['createdAt'],
    updatedAt: raw['updatedAt'],
    audits,
  });
}
