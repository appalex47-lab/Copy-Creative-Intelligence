import { validateAuditRecord, compareAuditsNewestFirst, type AuditRecord } from './audit';
import {
  validateAdaptationRecord,
  compareAdaptationsNewestFirst,
  type AdaptationRecord,
} from './adaptation';
import {
  validateEntityRecord,
  entityKey,
  compareEntities,
  MAX_ENTITIES_PER_KIND,
  type EntityRecord,
} from './entity';
import { validateRulesDoc, canonicalRules, type RulesDoc } from './rulesConfig';
import { validateCopyRecord, compareCopiesNewestFirst, type CopyRecord } from './copy';
import { validateBriefRecord, compareBriefsNewestFirst, type BriefRecord } from './briefRecord';
import { validateActivityEvent, type ActivityEvent } from './activity';
import { parseLocalProfile, validateDisplayName, type LocalProfile } from './profile';
import { validateSettingsPatch, type AppSettings } from './settings';
import { invalid, valid, type Validation } from './validation';

/**
 * Archivo de respaldo (S1.10). El FORMATO es un supuesto de Claude (reversible): JSON con versión, fecha, los datos
 * locales y una suma SHA-256 de los datos para detectar daños. La importación REEMPLAZA todos los datos locales.
 */
export const BACKUP_FORMAT = 'cci-backup';
export const BACKUP_VERSION = 7; // v2 añade `briefs` (S2.2), v3 `copies` (S2.4), v4 `rules` (S2.5b) v5 variantes dentro de cada copy (S2.7) y v6 `entities`, `adaptations` y `campaignId` en briefs (S2.8); v7 `audits` (S3.1); se aceptan v1–v6
export const BACKUP_MAX_BYTES = 5 * 1024 * 1024;
export const BACKUP_MAX_EVENTS = 10_000;
export const BACKUP_MAX_BRIEFS = 2_000;
export const BACKUP_MAX_COPIES = 5_000;
export const BACKUP_MAX_ADAPTATIONS = 5_000;
export const BACKUP_MAX_AUDITS = 5_000;

export interface BackupData {
  readonly profile: LocalProfile;
  readonly settings: AppSettings;
  readonly activity: readonly ActivityEvent[];
  readonly briefs: readonly BriefRecord[];
  readonly copies: readonly CopyRecord[];
  /** Leyendas y términos de marca; `null` = nunca configurados. */
  readonly rules: RulesDoc | null;
  readonly entities: readonly EntityRecord[];
  readonly adaptations: readonly AdaptationRecord[];
  readonly audits: readonly AuditRecord[];
}

export interface ParsedBackup {
  /** Versión del archivo: define con qué forma canónica se calculó la suma. */
  readonly version: number;
  readonly exportedAt: string;
  readonly data: BackupData;
  /** Suma declarada en el archivo (hex en minúsculas); se compara contra la recalculada. */
  readonly declaredHash: string;
}

const SETTINGS_KEYS = ['theme', 'language', 'lastView', 'seenNotices', 'lastBackupAt'] as const;

function canonicalBrief(b: BriefRecord, version: number): unknown {
  return {
    id: b.id,
    createdAt: b.createdAt,
    updatedAt: b.updatedAt,
    fields: Object.fromEntries(Object.entries(b.fields).sort(([x], [y]) => (x < y ? -1 : 1))),
    ...(version >= 6 && b.campaignId !== undefined ? { campaignId: b.campaignId } : {}),
  };
}

function canonicalCopy(c: CopyRecord, version: number): unknown {
  const sorted = (o: Record<string, unknown>) =>
    Object.fromEntries(Object.entries(o).sort(([x], [y]) => (x < y ? -1 : 1)));
  return {
    id: c.id,
    briefId: c.briefId,
    label: c.label,
    tags: c.tags,
    createdAt: c.createdAt,
    updatedAt: c.updatedAt,
    versions: c.versions.map((v) => ({
      n: v.n,
      createdAt: v.createdAt,
      content: sorted(v.content),
      ...(v.restoredFrom !== undefined ? { restoredFrom: v.restoredFrom } : {}),
    })),
    ...(version >= 5
      ? {
          variants: (c.variants ?? []).map((x) => ({
            id: x.id,
            label: x.label,
            content: sorted(x.content),
            createdAt: x.createdAt,
            updatedAt: x.updatedAt,
          })),
        }
      : {}),
  };
}

function canonicalEntity(e: EntityRecord): unknown {
  return {
    id: e.id,
    kind: e.kind,
    name: e.name,
    ...(e.note !== undefined ? { note: e.note } : {}),
    createdAt: e.createdAt,
    updatedAt: e.updatedAt,
  };
}

function canonicalAdaptation(a: AdaptationRecord): unknown {
  return {
    id: a.id,
    copyId: a.copyId,
    sourceVersion: a.sourceVersion,
    channel: a.channel,
    content: Object.fromEntries(Object.entries(a.content).sort(([x], [y]) => (x < y ? -1 : 1))),
    createdAt: a.createdAt,
    updatedAt: a.updatedAt,
  };
}

function canonicalAudit(a: AuditRecord): unknown {
  return {
    id: a.id,
    copyId: a.copyId,
    sourceVersion: a.sourceVersion,
    targetLabel: a.targetLabel,
    channel: a.channel,
    score: a.score,
    verdict: a.verdict,
    blocked: a.blocked,
    findings: a.findings.map((f) => ({
      ruleId: f.ruleId,
      category: f.category,
      severity: f.severity,
      message: f.message,
      ...(f.evidence !== undefined ? { evidence: f.evidence } : {}),
      ...(f.field !== undefined ? { field: f.field } : {}),
    })),
    rules: {
      isTemplate: a.rules.isTemplate,
      legends: a.rules.legends,
      brandTerms: a.rules.brandTerms,
    },
    createdAt: a.createdAt,
  };
}

/** Forma canónica (orden de claves fijo) sobre la que se calcula la suma: no depende del formato del archivo. */
export function canonicalData(data: BackupData, version: number = BACKUP_VERSION): string {
  const s = data.settings;
  return JSON.stringify({
    profile:
      data.profile.displayName === undefined ? {} : { displayName: data.profile.displayName },
    settings: {
      theme: s.theme,
      language: s.language,
      lastView: s.lastView,
      seenNotices: s.seenNotices,
      lastBackupAt: s.lastBackupAt,
    },
    activity: data.activity.map((e) => ({ id: e.id, at: e.at, kind: e.kind })),
    ...(version >= 2 ? { briefs: data.briefs.map((b) => canonicalBrief(b, version)) } : {}),
    ...(version >= 3 ? { copies: data.copies.map((c) => canonicalCopy(c, version)) } : {}),
    ...(version >= 4 ? { rules: canonicalRules(data.rules) } : {}),
    ...(version >= 6
      ? {
          entities: data.entities.map(canonicalEntity),
          adaptations: data.adaptations.map(canonicalAdaptation),
        }
      : {}),
    ...(version >= 7 ? { audits: data.audits.map(canonicalAudit) } : {}),
  });
}

/** Arma el texto del archivo (JSON legible) a partir de los datos y su suma. */
export function serializeBackup(data: BackupData, exportedAt: string, hash: string): string {
  return JSON.stringify(
    {
      format: BACKUP_FORMAT,
      version: BACKUP_VERSION,
      exportedAt,
      data: JSON.parse(canonicalData(data)) as unknown,
      integrity: { algorithm: 'SHA-256', value: hash },
    },
    null,
    2,
  );
}

export function backupFileName(exportedAt: string): string {
  const stamp = exportedAt
    .replace(/\.\d+Z$/, 'Z')
    .replace(/[-:]/g, '')
    .replace('T', '-')
    .replace('Z', '');
  return `cci-respaldo-${stamp}.json`;
}

const isObject = (v: unknown): v is Record<string, unknown> =>
  typeof v === 'object' && v !== null && !Array.isArray(v);
const onlyKeys = (o: Record<string, unknown>, allowed: readonly string[]) =>
  Object.keys(o).every((k) => allowed.includes(k));
const ISO = /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/;

/**
 * Valida el TEXTO de un archivo de respaldo (dato no confiable). Estricto: rechaza claves desconocidas, tamaños
 * excesivos, eventos repetidos o inválidos y versiones no soportadas. Los motivos son textos propios y nunca
 * reproducen contenido del archivo.
 */
export function parseBackupText(text: string): Validation<ParsedBackup> {
  if (new TextEncoder().encode(text).length > BACKUP_MAX_BYTES)
    return invalid('El archivo supera el tamaño máximo permitido (5 MB).');
  let raw: unknown;
  try {
    raw = JSON.parse(text);
  } catch {
    return invalid('El archivo no es un respaldo válido (no es JSON).');
  }
  if (!isObject(raw) || raw['format'] !== BACKUP_FORMAT)
    return invalid('El archivo no es un respaldo de Copy Creative Intelligence.');
  const version = raw['version'];
  if (typeof version !== 'number' || !Number.isInteger(version) || version < 1)
    return invalid('La versión del respaldo no es válida.');
  if (version > BACKUP_VERSION)
    return invalid(
      'El respaldo es de una versión más reciente de la aplicación. Actualiza la aplicación.',
    );
  if (!onlyKeys(raw, ['format', 'version', 'exportedAt', 'data', 'integrity']))
    return invalid('El respaldo contiene campos no permitidos.');
  const exportedAt = raw['exportedAt'];
  if (
    typeof exportedAt !== 'string' ||
    !ISO.test(exportedAt) ||
    Number.isNaN(Date.parse(exportedAt))
  )
    return invalid('La fecha del respaldo no es válida.');
  const integrity = raw['integrity'];
  if (
    !isObject(integrity) ||
    !onlyKeys(integrity, ['algorithm', 'value']) ||
    integrity['algorithm'] !== 'SHA-256' ||
    typeof integrity['value'] !== 'string' ||
    !/^[0-9a-f]{64}$/.test(integrity['value'])
  )
    return invalid('La verificación de integridad del respaldo no es válida.');
  const data = raw['data'];
  const dataKeys =
    version >= 7
      ? [
          'profile',
          'settings',
          'activity',
          'briefs',
          'copies',
          'rules',
          'entities',
          'adaptations',
          'audits',
        ]
      : version >= 6
        ? [
            'profile',
            'settings',
            'activity',
            'briefs',
            'copies',
            'rules',
            'entities',
            'adaptations',
          ]
        : version >= 4
          ? ['profile', 'settings', 'activity', 'briefs', 'copies', 'rules']
          : version >= 3
            ? ['profile', 'settings', 'activity', 'briefs', 'copies']
            : version >= 2
              ? ['profile', 'settings', 'activity', 'briefs']
              : ['profile', 'settings', 'activity'];
  if (
    !isObject(data) ||
    !onlyKeys(data, dataKeys) ||
    (version >= 2 && !('briefs' in data)) ||
    (version >= 3 && !('copies' in data)) ||
    (version >= 4 && !('rules' in data)) ||
    (version >= 6 && (!('entities' in data) || !('adaptations' in data))) ||
    (version >= 7 && !('audits' in data))
  )
    return invalid('Los datos del respaldo no son válidos.');

  const p = data['profile'];
  if (!isObject(p) || !onlyKeys(p, ['displayName']))
    return invalid('El perfil del respaldo no es válido.');
  const name = validateDisplayName(p['displayName']);
  if (!name.ok) return invalid('El nombre visible del respaldo no es válido.');
  const profile = parseLocalProfile(name.value === undefined ? {} : { displayName: name.value });

  const s = data['settings'];
  if (!isObject(s) || !SETTINGS_KEYS.every((k) => k in s))
    return invalid('La configuración del respaldo no es válida.');
  const settings = validateSettingsPatch(s);
  if (!settings.ok) return invalid('La configuración del respaldo no es válida.');

  const a = data['activity'];
  if (!Array.isArray(a)) return invalid('La actividad del respaldo no es válida.');
  if (a.length > BACKUP_MAX_EVENTS)
    return invalid('El respaldo tiene demasiados eventos de actividad.');
  const seen = new Set<string>();
  const activity: ActivityEvent[] = [];
  for (const item of a) {
    const v = validateActivityEvent(item);
    if (!v.ok || seen.has(v.value.id))
      return invalid('La actividad del respaldo contiene eventos no válidos.');
    seen.add(v.value.id);
    activity.push(v.value);
  }
  const entities =
    version >= 6 ? parseEntities(data['entities'], 'respaldo') : valid<EntityRecord[]>([]);
  if (!entities.ok) return entities;
  const briefs =
    version >= 2
      ? parseBriefs(data['briefs'], entities.value, 'respaldo')
      : valid<BriefRecord[]>([]);
  if (!briefs.ok) return briefs;
  const copies =
    version >= 3 ? parseCopies(data['copies'], briefs.value, 'respaldo') : valid<CopyRecord[]>([]);
  if (!copies.ok) return copies;
  const adaptations =
    version >= 6
      ? parseAdaptations(data['adaptations'], copies.value, 'respaldo')
      : valid<AdaptationRecord[]>([]);
  if (!adaptations.ok) return adaptations;
  const audits =
    version >= 7 ? parseAudits(data['audits'], copies.value, 'respaldo') : valid<AuditRecord[]>([]);
  if (!audits.ok) return audits;
  if (version < 6 && briefs.value.some((b) => b.campaignId !== undefined))
    return invalid('Los briefs del respaldo no son válidos para su versión.');
  if (version < 5 && copies.value.some((c) => c.variants !== undefined))
    return invalid('Los copys del respaldo no son válidos para su versión.');
  let rules: RulesDoc | null = null;
  if (version >= 4 && data['rules'] !== null) {
    const r = validateRulesDoc(data['rules']);
    if (!r.ok) return invalid('Las reglas del respaldo no son válidas.');
    rules = r.value;
  }
  return valid({
    version,
    exportedAt,
    declaredHash: integrity['value'],
    data: {
      profile,
      settings: settings.value as AppSettings,
      activity,
      briefs: briefs.value,
      copies: copies.value,
      rules,
      entities: entities.value,
      adaptations: adaptations.value,
      audits: audits.value,
    },
  });
}

function parseBriefs(
  raw: unknown,
  entities: readonly EntityRecord[],
  where: string,
): Validation<BriefRecord[]> {
  if (!Array.isArray(raw) || raw.length > BACKUP_MAX_BRIEFS)
    return invalid(`Los briefs del ${where} no son válidos.`);
  const campaignIds = new Set(entities.filter((e) => e.kind === 'campaign').map((e) => e.id));
  const seen = new Set<string>();
  const out: BriefRecord[] = [];
  for (const item of raw) {
    const v = validateBriefRecord(item);
    if (!v.ok || seen.has(v.value.id))
      return invalid(`Los briefs del ${where} contienen datos no válidos.`);
    if (v.value.campaignId !== undefined && !campaignIds.has(v.value.campaignId))
      return invalid(`Un brief del ${where} apunta a una campaña que no existe.`);
    seen.add(v.value.id);
    out.push(v.value);
  }
  return valid(out.sort(compareBriefsNewestFirst));
}

/** Cada copy debe apuntar a un brief que exista en el mismo conjunto (integridad referencial). */
function parseCopies(
  raw: unknown,
  briefs: readonly BriefRecord[],
  where: string,
): Validation<CopyRecord[]> {
  if (!Array.isArray(raw) || raw.length > BACKUP_MAX_COPIES)
    return invalid(`Los copys del ${where} no son válidos.`);
  const briefIds = new Set(briefs.map((b) => b.id));
  const seen = new Set<string>();
  const out: CopyRecord[] = [];
  for (const item of raw) {
    const v = validateCopyRecord(item);
    if (!v.ok || seen.has(v.value.id))
      return invalid(`Los copys del ${where} contienen datos no válidos.`);
    if (!briefIds.has(v.value.briefId))
      return invalid(`Un copy del ${where} apunta a un brief que no existe.`);
    seen.add(v.value.id);
    out.push(v.value);
  }
  return valid(out.sort(compareCopiesNewestFirst));
}

function parseEntities(raw: unknown, where: string): Validation<EntityRecord[]> {
  if (!Array.isArray(raw) || raw.length > MAX_ENTITIES_PER_KIND * 3)
    return invalid(`Los registros del catálogo del ${where} no son válidos.`);
  const ids = new Set<string>();
  const keys = new Set<string>();
  const out: EntityRecord[] = [];
  for (const item of raw) {
    const v = validateEntityRecord(item);
    if (!v.ok || ids.has(v.value.id) || keys.has(entityKey(v.value)))
      return invalid(`Los registros del catálogo del ${where} contienen datos no válidos.`);
    ids.add(v.value.id);
    keys.add(entityKey(v.value));
    out.push(v.value);
  }
  return valid(out.sort(compareEntities));
}

/** Cada adaptación debe apuntar a un copy existente y a una versión que exista de él. */
function parseAdaptations(
  raw: unknown,
  copies: readonly CopyRecord[],
  where: string,
): Validation<AdaptationRecord[]> {
  if (!Array.isArray(raw) || raw.length > BACKUP_MAX_ADAPTATIONS)
    return invalid(`Las adaptaciones del ${where} no son válidas.`);
  const byId = new Map(copies.map((c) => [c.id, c]));
  const seen = new Set<string>();
  const out: AdaptationRecord[] = [];
  for (const item of raw) {
    const v = validateAdaptationRecord(item);
    if (!v.ok || seen.has(v.value.id))
      return invalid(`Las adaptaciones del ${where} contienen datos no válidos.`);
    const copy = byId.get(v.value.copyId);
    if (!copy || !copy.versions.some((x) => x.n === v.value.sourceVersion))
      return invalid(`Una adaptación del ${where} apunta a un copy o versión que no existe.`);
    seen.add(v.value.id);
    out.push(v.value);
  }
  return valid(out.sort(compareAdaptationsNewestFirst));
}

/** Cada auditoría debe apuntar a un copy existente y a una versión que exista de él. */
function parseAudits(
  raw: unknown,
  copies: readonly CopyRecord[],
  where: string,
): Validation<AuditRecord[]> {
  if (!Array.isArray(raw) || raw.length > BACKUP_MAX_AUDITS)
    return invalid(`Las auditorías del ${where} no son válidas.`);
  const byId = new Map(copies.map((c) => [c.id, c]));
  const seen = new Set<string>();
  const out: AuditRecord[] = [];
  for (const item of raw) {
    const v = validateAuditRecord(item);
    if (!v.ok || seen.has(v.value.id))
      return invalid(`Las auditorías del ${where} contienen datos no válidos.`);
    const copy = byId.get(v.value.copyId);
    if (!copy || !copy.versions.some((x) => x.n === v.value.sourceVersion))
      return invalid(`Una auditoría del ${where} apunta a un copy o versión que no existe.`);
    seen.add(v.value.id);
    out.push(v.value);
  }
  return valid(out.sort(compareAuditsNewestFirst));
}

export interface Snapshot {
  readonly profile: LocalProfile;
  readonly activity: readonly ActivityEvent[];
  readonly briefs: readonly BriefRecord[];
  readonly copies: readonly CopyRecord[];
  readonly rules: RulesDoc | null;
  readonly entities: readonly EntityRecord[];
  readonly adaptations: readonly AdaptationRecord[];
  readonly audits: readonly AuditRecord[];
}

/** Valida un conjunto (perfil + actividad) antes de reemplazar los datos locales: todo o nada. */
export function validateSnapshot(raw: unknown): Validation<Snapshot> {
  if (
    !isObject(raw) ||
    !onlyKeys(raw, [
      'profile',
      'activity',
      'briefs',
      'copies',
      'rules',
      'entities',
      'adaptations',
      'audits',
    ])
  )
    return invalid('Los datos a restaurar no son válidos.');
  const p = raw['profile'];
  if (!isObject(p) || !onlyKeys(p, ['displayName']))
    return invalid('El perfil a restaurar no es válido.');
  const name = validateDisplayName(p['displayName']);
  if (!name.ok) return invalid('El nombre visible a restaurar no es válido.');
  const a = raw['activity'];
  if (!Array.isArray(a) || a.length > BACKUP_MAX_EVENTS)
    return invalid('La actividad a restaurar no es válida.');
  const seen = new Set<string>();
  const activity: ActivityEvent[] = [];
  for (const item of a) {
    const v = validateActivityEvent(item);
    if (!v.ok || seen.has(v.value.id))
      return invalid('La actividad a restaurar contiene eventos no válidos.');
    seen.add(v.value.id);
    activity.push(v.value);
  }
  const entities =
    raw['entities'] === undefined
      ? valid<EntityRecord[]>([])
      : parseEntities(raw['entities'], 'conjunto a restaurar');
  if (!entities.ok) return entities;
  const briefs =
    raw['briefs'] === undefined
      ? valid<BriefRecord[]>([])
      : parseBriefs(raw['briefs'], entities.value, 'conjunto a restaurar');
  if (!briefs.ok) return briefs;
  const copies =
    raw['copies'] === undefined
      ? valid<CopyRecord[]>([])
      : parseCopies(raw['copies'], briefs.value, 'conjunto a restaurar');
  if (!copies.ok) return copies;
  const adaptations =
    raw['adaptations'] === undefined
      ? valid<AdaptationRecord[]>([])
      : parseAdaptations(raw['adaptations'], copies.value, 'conjunto a restaurar');
  if (!adaptations.ok) return adaptations;
  const audits =
    raw['audits'] === undefined
      ? valid<AuditRecord[]>([])
      : parseAudits(raw['audits'], copies.value, 'conjunto a restaurar');
  if (!audits.ok) return audits;
  let rules: RulesDoc | null = null;
  if (raw['rules'] !== undefined && raw['rules'] !== null) {
    const r = validateRulesDoc(raw['rules']);
    if (!r.ok) return invalid('Las reglas a restaurar no son válidas.');
    rules = r.value;
  }
  return valid({
    profile: name.value === undefined ? {} : { displayName: name.value },
    activity,
    briefs: briefs.value,
    copies: copies.value,
    rules,
    entities: entities.value,
    adaptations: adaptations.value,
    audits: audits.value,
  });
}
