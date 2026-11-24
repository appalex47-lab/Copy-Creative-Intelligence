import { CHANNELS, type Channel } from './brief';
import { COPY_FIELDS, COPY_ID, type CopyField } from './copy';
import type { Category, Evaluation, Finding, Severity, Verdict } from './copyRules';
import { invalid, valid, type Validation } from './validation';

/**
 * Auditoría de Copy guardada (S3.1; funciones 4, 6 y 9 de la Fase 3). Es una FOTO inmutable de la revisión por reglas de
 * un Copy en un momento dado (no se extiende a variantes ni adaptaciones, según el alcance de la Fase 3): versión revisada, canal, puntaje, veredicto y hallazgos. Nunca se
 * edita; se puede eliminar (con confirmación). No es una aprobación ni equivale a una: las aprobaciones son de la
 * Fase 5 (Q-3). SUPUESTOS de Claude (reversibles): se guardan hasta 5 000 auditorías; se audita solo texto (no
 * imágenes); el nombre del copy se guarda como texto para conservarlo aunque cambie.
 */
export interface AuditFinding {
  readonly ruleId: string;
  readonly category: Category;
  readonly severity: Severity;
  readonly message: string;
  readonly evidence?: string;
  readonly field?: CopyField;
}

export interface AuditRecord {
  readonly id: string; // aud_…
  readonly copyId: string;
  /** Versión del copy que se revisó. */
  readonly sourceVersion: number;
  /** Nombre del copy al momento de auditar. */
  readonly targetLabel: string;
  readonly channel: Channel;
  readonly score: number;
  readonly verdict: Verdict;
  readonly blocked: boolean;
  readonly findings: readonly AuditFinding[];
  /** Con qué reglas se evaluó (solo conteos, para saber si cambió la configuración). */
  readonly rules: {
    readonly isTemplate: boolean;
    readonly legends: number;
    readonly brandTerms: number;
  };
  readonly createdAt: string;
}

export const AUDIT_ID = /^aud_[A-Za-z0-9_-]{8,64}$/;
export const MAX_AUDITS = 5_000;
export const MAX_AUDIT_FINDINGS = 100;
const SEVERITIES: readonly Severity[] = ['critica', 'mayor', 'menor', 'aviso'];
const CATEGORIES: readonly Category[] = [
  'cumplimiento',
  'precios',
  'marca',
  'claridad',
  'canal',
  'redaccion',
];
const VERDICTS: readonly Verdict[] = ['apto', 'revisar', 'no_apto'];
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;
const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const only = (o: Record<string, unknown>, keys: readonly string[]) =>
  Object.keys(o).every((k) => keys.includes(k));
const text = (v: unknown, max: number): v is string =>
  typeof v === 'string' && v.length > 0 && [...v].length <= max;
const count = (v: unknown): v is number =>
  typeof v === 'number' && Number.isInteger(v) && v >= 0 && v <= 10_000;

function validateFinding(raw: unknown): Validation<AuditFinding> {
  if (
    !isObject(raw) ||
    !only(raw, ['ruleId', 'category', 'severity', 'message', 'evidence', 'field']) ||
    !text(raw['ruleId'], 80) ||
    !CATEGORIES.includes(raw['category'] as Category) ||
    !SEVERITIES.includes(raw['severity'] as Severity) ||
    !text(raw['message'], 600) ||
    (raw['evidence'] !== undefined && !text(raw['evidence'], 300)) ||
    (raw['field'] !== undefined && !COPY_FIELDS.includes(raw['field'] as CopyField))
  )
    return invalid('Un hallazgo de la auditoría no es válido.');
  return valid({
    ruleId: raw['ruleId'],
    category: raw['category'] as Category,
    severity: raw['severity'] as Severity,
    message: raw['message'],
    ...(raw['evidence'] !== undefined ? { evidence: raw['evidence'] as string } : {}),
    ...(raw['field'] !== undefined ? { field: raw['field'] as CopyField } : {}),
  });
}

export function validateAuditRecord(raw: unknown): Validation<AuditRecord> {
  if (
    !isObject(raw) ||
    !only(raw, [
      'id',
      'copyId',
      'sourceVersion',
      'targetLabel',
      'channel',
      'score',
      'verdict',
      'blocked',
      'findings',
      'rules',
      'createdAt',
    ])
  )
    return invalid('La auditoría guardada no es válida.');
  const bad = invalid<AuditRecord>('La auditoría guardada no es válida.');
  if (typeof raw['id'] !== 'string' || !AUDIT_ID.test(raw['id'])) return bad;
  if (typeof raw['copyId'] !== 'string' || !COPY_ID.test(raw['copyId'])) return bad;
  const sv = raw['sourceVersion'];
  if (typeof sv !== 'number' || !Number.isInteger(sv) || sv < 1) return bad;
  if (!text(raw['targetLabel'], 200)) return bad;
  if (!CHANNELS.includes(raw['channel'] as Channel)) return bad;
  const score = raw['score'];
  if (typeof score !== 'number' || !Number.isInteger(score) || score < 0 || score > 100) return bad;
  if (!VERDICTS.includes(raw['verdict'] as Verdict) || typeof raw['blocked'] !== 'boolean')
    return bad;
  const fs = raw['findings'];
  if (!Array.isArray(fs) || fs.length > MAX_AUDIT_FINDINGS) return bad;
  const findings: AuditFinding[] = [];
  for (const f of fs) {
    const v = validateFinding(f);
    if (!v.ok) return bad;
    findings.push(v.value);
  }
  const r = raw['rules'];
  if (
    !isObject(r) ||
    !only(r, ['isTemplate', 'legends', 'brandTerms']) ||
    typeof r['isTemplate'] !== 'boolean' ||
    !count(r['legends']) ||
    !count(r['brandTerms'])
  )
    return bad;
  const at = raw['createdAt'];
  if (typeof at !== 'string' || !ISO.test(at) || Number.isNaN(Date.parse(at))) return bad;
  return valid({
    id: raw['id'],
    copyId: raw['copyId'],
    sourceVersion: sv,
    targetLabel: raw['targetLabel'],
    channel: raw['channel'] as Channel,
    score,
    verdict: raw['verdict'] as Verdict,
    blocked: raw['blocked'],
    findings,
    rules: { isTemplate: r['isTemplate'], legends: r['legends'], brandTerms: r['brandTerms'] },
    createdAt: at,
  });
}

/** Arma el registro (sin id ni fecha) a partir de una evaluación. */
export function auditFromEvaluation(
  e: Evaluation,
  meta: {
    readonly id: string;
    readonly copyId: string;
    readonly sourceVersion: number;
    readonly targetLabel: string;
    readonly channel: Channel;
    readonly rules: AuditRecord['rules'];
    readonly createdAt: string;
  },
): unknown {
  return {
    id: meta.id,
    copyId: meta.copyId,
    sourceVersion: meta.sourceVersion,
    targetLabel: meta.targetLabel,
    channel: meta.channel,
    score: Math.round(e.score),
    verdict: e.verdict,
    blocked: e.blocked,
    findings: e.findings.slice(0, MAX_AUDIT_FINDINGS).map((f: Finding) => ({
      ruleId: f.ruleId,
      category: f.category,
      severity: f.severity,
      message: f.message,
      ...(f.evidence !== undefined ? { evidence: f.evidence } : {}),
      ...(f.field !== undefined ? { field: f.field } : {}),
    })),
    rules: meta.rules,
    createdAt: meta.createdAt,
  };
}

/** Más recientes primero (empate: id descendente). */
export function compareAuditsNewestFirst(a: AuditRecord, b: AuditRecord): number {
  if (a.createdAt !== b.createdAt) return a.createdAt < b.createdAt ? 1 : -1;
  return a.id < b.id ? 1 : a.id > b.id ? -1 : 0;
}

/** Mismo objetivo = mismo copy. */
export const sameTarget = (a: AuditRecord, b: AuditRecord): boolean => a.copyId === b.copyId;

const keyOf = (f: AuditFinding): string => `${f.ruleId}|${f.message}`;

export interface AuditDiff {
  readonly scoreDelta: number;
  readonly added: readonly AuditFinding[];
  readonly resolved: readonly AuditFinding[];
}

/** Compara una auditoría con la anterior del mismo objetivo: cambio de puntaje y hallazgos nuevos o resueltos. */
export function diffAudits(previous: AuditRecord, next: AuditRecord): AuditDiff {
  const before = new Set(previous.findings.map(keyOf));
  const after = new Set(next.findings.map(keyOf));
  return {
    scoreDelta: next.score - previous.score,
    added: next.findings.filter((f) => !before.has(keyOf(f))),
    resolved: previous.findings.filter((f) => !after.has(keyOf(f))),
  };
}

/** Para cada auditoría (lista más reciente primero) devuelve la anterior del mismo objetivo, si la hay. */
export function previousOf(
  list: readonly AuditRecord[],
  audit: AuditRecord,
): AuditRecord | undefined {
  return list.find(
    (x) => x.id !== audit.id && sameTarget(x, audit) && compareAuditsNewestFirst(x, audit) > 0,
  );
}
