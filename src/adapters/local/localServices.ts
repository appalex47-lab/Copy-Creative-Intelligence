import {
  createIndexedDbRepositories,
  openDatabase,
} from '@/adapters/indexeddb/indexedDbRepositories';
import { createBrowserTabCoordinator } from '@/adapters/tabs/tabCoordinator';
import { createBackupService } from './backupService';
import { createBriefService } from './briefService';
import { createRulesService } from './rulesService';
import { createCopyService } from './copyService';
import { createEntityService } from './entityService';
import { createAuditService } from './auditService';
import { createMeasureService } from './measureService';
import { createPromoService } from './promoService';
import { createReviewService } from './reviewService';
import { createPieceService } from './pieceService';
import { createResourceService } from './resourceService';
import { createTesseractEngine, OCR_ENGINE } from '@/adapters/ocr/tesseractEngine';
import { readImageSize } from '@/adapters/ocr/imageSize';
import { createAdaptationService } from './adaptationService';
import { createBrowserStorageInfoService } from '@/adapters/storage/browserStorageInfo';
import { createBrowserPreferencesStore } from '@/adapters/localstorage/preferencesStore';
import type { ActivityKind } from '@/domain/activity';
import type { AppState } from '@/domain/entities';
import type { Repositories } from '@/repositories/contracts';
import {
  fail,
  ok,
  type BackupService,
  type PreferencesService,
  type Result,
  type Services,
} from '@/services/contracts';

/**
 * Servicios de datos REALES del navegador: IndexedDB (actividad y perfil) y Local Storage (preferencias).
 * No hay backend, cuentas ni sincronización. La base se abre de forma perezosa en el primer uso; si falla, cada
 * operación devuelve el error (nunca datos vacíos) y se reintenta en la siguiente.
 */
export function createLocalServices(environment: AppState['environment']): Services {
  let opening: Promise<Result<Repositories>> | undefined;
  const repos = (): Promise<Result<Repositories>> => {
    opening ??= openDatabase().then((r) => {
      if (r.ok) return ok(createIndexedDbRepositories(r.value));
      opening = undefined; // permite reintentar
      return fail(r.error.code, r.error.message);
    });
    return opening;
  };
  const via =
    <A extends unknown[], T>(pick: (r: Repositories) => (...a: A) => Promise<Result<T>>) =>
    async (...args: A): Promise<Result<T>> => {
      const r = await repos();
      return r.ok ? pick(r.value)(...args) : fail(r.error.code, r.error.message);
    };
  const coordination = createBrowserTabCoordinator();
  /** Toda escritura espera el permiso de escritura de esta pestaña (P12); si no lo obtiene, falla sin escribir. */
  const writable = async <T>(run: () => Promise<Result<T>>): Promise<Result<T>> =>
    (await coordination.whenWriter())
      ? run()
      : fail('storage_read_only', 'Esta pestaña está en solo lectura.');
  const basePreferences = createBrowserPreferencesStore();
  const preferences: PreferencesService = {
    get: () => basePreferences.get(),
    update: (patch) => writable(() => basePreferences.update(patch)),
    reset: () => writable(() => basePreferences.reset()),
  };
  const saveProfile = via((r) => (name: unknown) => writable(() => r.profile.save(name)));
  const clearProfile = via((r) => () => writable(() => r.profile.clear()));
  const add = via(
    (r) => (kind: ActivityKind) =>
      writable(() =>
        r.activity.add({
          id: `evt_${crypto.randomUUID().replaceAll('-', '')}`,
          at: new Date().toISOString(),
          kind,
        }),
      ),
  );
  const record = async (kind: ActivityKind): Promise<Result<void>> => {
    const r = await add(kind);
    return r.ok ? ok(undefined) : fail(r.error.code, r.error.message);
  };
  /** Tras un cambio correcto, anota el evento. Es secundario: si no se puede anotar, el cambio igual vale. */
  const noting = async <T>(result: Result<T>, kind: ActivityKind): Promise<Result<T>> => {
    if (result.ok) await record(kind);
    return result;
  };
  const backupBase = createBackupService({ repos, preferences, record });
  const backup: BackupService = {
    ...backupBase,
    restore: (text) => writable(() => backupBase.restore(text)),
  };
  const briefs = createBriefService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.briefs) : fail(r.error.code, r.error.message);
    },
    copies: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.copies) : fail(r.error.code, r.error.message);
    },
    entities: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.entities) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const rules = createRulesService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.rules) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const copies = createCopyService({
    copies: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.copies) : fail(r.error.code, r.error.message);
    },
    briefs: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.briefs) : fail(r.error.code, r.error.message);
    },
    adaptations: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.adaptations) : fail(r.error.code, r.error.message);
    },
    audits: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.audits) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const entities = createEntityService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.entities) : fail(r.error.code, r.error.message);
    },
    briefs: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.briefs) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const adaptations = createAdaptationService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.adaptations) : fail(r.error.code, r.error.message);
    },
    copies: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.copies) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const audits = createAuditService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.audits) : fail(r.error.code, r.error.message);
    },
    copies: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.copies) : fail(r.error.code, r.error.message);
    },
    briefs: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.briefs) : fail(r.error.code, r.error.message);
    },
    rules: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.rules) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const resources = createResourceService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.resources) : fail(r.error.code, r.error.message);
    },
    pieces: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.pieces) : fail(r.error.code, r.error.message);
    },
    reviews: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.reviews) : fail(r.error.code, r.error.message);
    },
    measures: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.measures) : fail(r.error.code, r.error.message);
    },
    promos: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.promos) : fail(r.error.code, r.error.message);
    },
    engine: () => createTesseractEngine(),
    readSize: readImageSize,
    engineName: OCR_ENGINE,
    writable,
  });
  const reviews = createReviewService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.reviews) : fail(r.error.code, r.error.message);
    },
    copies: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.copies) : fail(r.error.code, r.error.message);
    },
    pieces: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.pieces) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const measures = createMeasureService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.measures) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const promos = createPromoService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.promos) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  const pieces = createPieceService({
    repo: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.pieces) : fail(r.error.code, r.error.message);
    },
    resources: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.resources) : fail(r.error.code, r.error.message);
    },
    rules: async () => {
      const r = await repos();
      return r.ok ? ok(r.value.rules) : fail(r.error.code, r.error.message);
    },
    writable,
  });
  return {
    appState: {
      getState: () => Promise.resolve(ok({ dataMode: 'local', environment, isDemo: false })),
    },
    activity: {
      listRecent: via((r) => (limit?: number) => r.activity.listRecent(limit)),
      record,
    },
    profile: {
      get: via((r) => () => r.profile.get()),
      save: async (name: unknown) => noting(await saveProfile(name), 'profile_changed'),
      clear: async () => noting(await clearProfile(), 'profile_changed'),
    },
    preferences: {
      get: () => preferences.get(),
      update: async (patch: unknown) => noting(await preferences.update(patch), 'setting_changed'),
      reset: async () => noting(await preferences.reset(), 'setting_changed'),
    },
    storage: createBrowserStorageInfoService(),
    backup,
    briefs,
    copies,
    rules,
    entities,
    adaptations,
    audits,
    resources,
    pieces,
    reviews,
    measures,
    promos,
    coordination,
  };
}
