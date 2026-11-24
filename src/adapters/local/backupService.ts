import {
  backupFileName,
  canonicalData,
  parseBackupText,
  serializeBackup,
  type BackupData,
} from '@/domain/backup';
import type { ActivityKind } from '@/domain/activity';
import { DEFAULT_SETTINGS, type AppSettings } from '@/domain/settings';
import { sha256Hex } from '@/lib/sha256';
import type { Repositories } from '@/repositories/contracts';
import {
  fail,
  ok,
  type BackupService,
  type BackupSummary,
  type PreferencesService,
  type Result,
} from '@/services/contracts';

export interface BackupDeps {
  readonly repos: () => Promise<Result<Repositories>>;
  readonly preferences: PreferencesService;
  readonly record: (kind: ActivityKind) => Promise<Result<void>>;
  readonly now?: () => Date;
}

const summaryOf = (exportedAt: string, d: BackupData): BackupSummary => ({
  exportedAt,
  activityCount: d.activity.length,
  briefCount: d.briefs.length,
  copyCount: d.copies.length,
  hasRules: d.rules !== null,
  entityCount: d.entities.length,
  adaptationCount: d.adaptations.length,
  auditCount: d.audits.length,
  hasName: d.profile.displayName !== undefined,
});

/** Casos de uso de respaldo sobre repositorios y preferencias. Sin red: el archivo lo maneja la interfaz. */
export function createBackupService(deps: BackupDeps): BackupService {
  const now = deps.now ?? (() => new Date());

  /** Valida el texto y comprueba la suma de integridad. */
  const check = async (text: string) => {
    const parsed = parseBackupText(text);
    if (!parsed.ok) return fail<never>('validation_error', parsed.reason);
    const actual = await sha256Hex(canonicalData(parsed.value.data, parsed.value.version));
    if (actual !== parsed.value.declaredHash)
      return fail<never>(
        'validation_error',
        'El respaldo está dañado o fue modificado (la suma de verificación no coincide).',
      );
    return ok(parsed.value);
  };

  return {
    export: async () => {
      const repos = await deps.repos();
      if (!repos.ok) return fail(repos.error.code, repos.error.message);
      const snap = await repos.value.backup.exportAll();
      if (!snap.ok) return fail(snap.error.code, snap.error.message);
      const prefs = await deps.preferences.get();
      if (!prefs.ok) return fail(prefs.error.code, prefs.error.message);
      const exportedAt = now().toISOString();
      const data: BackupData = {
        profile: snap.value.profile,
        settings: { ...prefs.value, lastBackupAt: exportedAt },
        activity: snap.value.activity,
        briefs: snap.value.briefs,
        copies: snap.value.copies,
        rules: snap.value.rules,
        entities: snap.value.entities,
        adaptations: snap.value.adaptations,
        audits: snap.value.audits,
      };
      const text = serializeBackup(data, exportedAt, await sha256Hex(canonicalData(data)));
      await deps.preferences.update({ lastBackupAt: exportedAt }); // secundario: si falla, el archivo igual es válido
      await deps.record('backup_exported');
      return ok({
        fileName: backupFileName(exportedAt),
        text,
        summary: summaryOf(exportedAt, data),
      });
    },

    inspect: async (text) => {
      const c = await check(text);
      return c.ok ? ok(summaryOf(c.value.exportedAt, c.value.data)) : c;
    },

    restore: async (text) => {
      const c = await check(text);
      if (!c.ok) return c;
      const repos = await deps.repos();
      if (!repos.ok) return fail(repos.error.code, repos.error.message);
      const previous: AppSettings = await deps.preferences
        .get()
        .then((r) => (r.ok ? r.value : DEFAULT_SETTINGS));
      const { data } = c.value;
      // Orden pensado para no dejar estado parcial: 1) preferencias (reversibles), 2) base (atómica). Si la base falla,
      // se restauran las preferencias anteriores.
      const prefs = await deps.preferences.update(data.settings);
      if (!prefs.ok) return fail(prefs.error.code, prefs.error.message);
      const replaced = await repos.value.backup.replaceAll({
        profile: data.profile,
        activity: data.activity,
        briefs: data.briefs,
        copies: data.copies,
        rules: data.rules,
        entities: data.entities,
        adaptations: data.adaptations,
        audits: data.audits,
      });
      if (!replaced.ok) {
        await deps.preferences.update(previous);
        return fail(replaced.error.code, replaced.error.message);
      }
      await deps.record('backup_imported');
      return ok({ summary: summaryOf(c.value.exportedAt, data), settings: data.settings });
    },
  };
}
