/**
 * Configuración de la aplicación: lista PERMITIDA de cinco categorías documentadas (AC1-09).
 * SUPUESTOS de Claude (S1-D09, reversibles): valores y defaults de abajo; no vienen de un documento aprobado.
 */
export const THEMES = ['system', 'light', 'dark'] as const;
export const LANGUAGES = ['es'] as const;
export const VIEW_IDS = ['inicio', 'conexion'] as const;
export const SEEN_NOTICES_MAX = 50;

export interface AppSettings {
  readonly theme: (typeof THEMES)[number];
  readonly language: (typeof LANGUAGES)[number];
  readonly lastView: (typeof VIEW_IDS)[number];
  readonly seenNotices: readonly string[];
  /** Copia de la fecha del último respaldo (ISO 8601 UTC) o null. */
  readonly lastBackupAt: string | null;
}

export const DEFAULT_SETTINGS: AppSettings = {
  theme: 'system',
  language: 'es',
  lastView: 'inicio',
  seenNotices: [],
  lastBackupAt: null,
};

const oneOf = <T extends string>(list: readonly T[], v: unknown): T | undefined =>
  typeof v === 'string' ? list.find((x) => x === v) : undefined;

const isIsoUtc = (v: unknown): v is string =>
  typeof v === 'string' &&
  /^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d{1,3})?Z$/.test(v) &&
  !Number.isNaN(Date.parse(v));

/**
 * Normaliza lo leído de almacenamiento: descarta claves fuera de la lista permitida y reemplaza por el valor por
 * defecto cualquier valor inválido, sin lanzar excepciones.
 */
export function parseSettings(raw: unknown): AppSettings {
  const r = typeof raw === 'object' && raw !== null ? (raw as Record<string, unknown>) : {};
  const notices = Array.isArray(r['seenNotices'])
    ? r['seenNotices']
        .filter((x): x is string => typeof x === 'string' && /^[a-z0-9_-]{1,40}$/.test(x))
        .slice(0, SEEN_NOTICES_MAX)
    : [];
  return {
    theme: oneOf(THEMES, r['theme']) ?? DEFAULT_SETTINGS.theme,
    language: oneOf(LANGUAGES, r['language']) ?? DEFAULT_SETTINGS.language,
    lastView: oneOf(VIEW_IDS, r['lastView']) ?? DEFAULT_SETTINGS.lastView,
    seenNotices: [...new Set(notices)],
    lastBackupAt: isIsoUtc(r['lastBackupAt']) ? r['lastBackupAt'] : null,
  };
}
