import {
  DEFAULT_SETTINGS,
  parseSettings,
  validateSettingsPatch,
  type AppSettings,
} from '@/domain/settings';
import { fail, ok, type PreferencesService, type Result } from '@/services/contracts';

/** Clave única de las preferencias ligeras (AC1-09). Nada más se guarda en Local Storage. */
export const PREFS_KEY = 'cci.prefs.v1';
const UNAVAILABLE = 'El almacenamiento local no está disponible.';

type StorageLike = Pick<Storage, 'getItem' | 'setItem' | 'removeItem'>;

/** Preferencias sobre Local Storage (o un sustituto con la misma interfaz). Lee con tolerancia y escribe validado. */
export function createPreferencesStore(storage: StorageLike): PreferencesService {
  const read = (): Result<AppSettings> => {
    try {
      const raw = storage.getItem(PREFS_KEY);
      if (raw === null) return ok(DEFAULT_SETTINGS);
      let parsed: unknown;
      try {
        parsed = JSON.parse(raw);
      } catch {
        return ok(DEFAULT_SETTINGS); // contenido corrupto: se ignora y rigen los valores por defecto
      }
      return ok(parseSettings(parsed));
    } catch {
      return fail('unavailable', UNAVAILABLE);
    }
  };
  const write = (s: AppSettings): Result<AppSettings> => {
    try {
      storage.setItem(PREFS_KEY, JSON.stringify(s));
      return ok(s);
    } catch {
      return fail('unavailable', UNAVAILABLE);
    }
  };
  return {
    get: () => Promise.resolve(read()),
    update: (patch) => {
      const v = validateSettingsPatch(patch);
      if (!v.ok) return Promise.resolve(fail('validation_error', v.reason));
      const current = read();
      if (!current.ok) return Promise.resolve(current);
      return Promise.resolve(write({ ...current.value, ...v.value }));
    },
    reset: () => {
      try {
        storage.removeItem(PREFS_KEY);
        return Promise.resolve(ok(DEFAULT_SETTINGS));
      } catch {
        return Promise.resolve(fail('unavailable', UNAVAILABLE));
      }
    },
  };
}

/** Sustituto en memoria (modo DEMO y pruebas): no persiste nada. */
export function createMemoryStorage(): StorageLike {
  const m = new Map<string, string>();
  return {
    getItem: (k) => m.get(k) ?? null,
    setItem: (k, v) => void m.set(k, v),
    removeItem: (k) => void m.delete(k),
  };
}

/** Almacén de preferencias sobre el Local Storage del navegador (único lugar de `src` que lo toca). */
export function createBrowserPreferencesStore() {
  return createPreferencesStore(window.localStorage);
}
