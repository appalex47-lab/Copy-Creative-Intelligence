import { UNKNOWN_STORAGE } from '@/domain/storageInfo';
import { createMemoryRepositories } from '@/adapters/memory/memoryRepositories';
import {
  createMemoryStorage,
  createPreferencesStore,
} from '@/adapters/localstorage/preferencesStore';
import type { AppState } from '@/domain/entities';
import { createCopyService } from '@/adapters/local/copyService';
import { createEntityService } from '@/adapters/local/entityService';
import { createResourceService } from '@/adapters/local/resourceService';
import { readImageSize } from '@/adapters/ocr/imageSize';
import { createAuditService } from '@/adapters/local/auditService';
import { createAdaptationService } from '@/adapters/local/adaptationService';
import { createRulesService } from '@/adapters/local/rulesService';
import { createBriefService } from '@/adapters/local/briefService';
import { fail, ok } from '@/services/contracts';
import type { Services } from '@/services/contracts';

/**
 * Adaptador DEMO: en memoria y de solo lectura. No simula autenticación ni persistencia y NO inventa actividad:
 * la actividad reciente está vacía y el perfil y las preferencias viven solo en memoria
 * (se pierden al recargar). La persistencia real es el modo `local`.
 */
/** Marca no enumerable del adaptador DEMO: permite comprobar que NO está en el bundle de producción. */
export const DEMO_ADAPTER_MARKER = 'cci-adaptador-demo-v1';

export function createDemoServices(environment: AppState['environment']): Services {
  const memory = createMemoryRepositories();
  const services: Services = {
    appState: {
      getState: () => Promise.resolve(ok({ dataMode: 'demo', environment, isDemo: true })),
    },
    activity: {
      listRecent: () => Promise.resolve(ok([])),
      record: () => Promise.resolve(ok(undefined)), // DEMO no guarda actividad
    },
    profile: memory.profile,
    briefs: createBriefService({
      repo: () => Promise.resolve(ok(memory.briefs)),
      copies: () => Promise.resolve(ok(memory.copies)),
      entities: () => Promise.resolve(ok(memory.entities)),
      writable: (run) => run(),
    }),
    copies: createCopyService({
      copies: () => Promise.resolve(ok(memory.copies)),
      briefs: () => Promise.resolve(ok(memory.briefs)),
      adaptations: () => Promise.resolve(ok(memory.adaptations)),
      audits: () => Promise.resolve(ok(memory.audits)),
      writable: (run) => run(),
    }),
    audits: createAuditService({
      repo: () => Promise.resolve(ok(memory.audits)),
      copies: () => Promise.resolve(ok(memory.copies)),
      briefs: () => Promise.resolve(ok(memory.briefs)),
      rules: () => Promise.resolve(ok(memory.rules)),
      writable: (run) => run(),
    }),
    resources: createResourceService({
      repo: () => Promise.resolve(ok(memory.resources)),
      engine: () => ({
        recognize: () =>
          Promise.resolve(fail('unavailable', 'El OCR solo funciona en el modo local.')),
      }),
      readSize: readImageSize,
      engineName: 'demo',
      writable: (run) => run(),
    }),
    entities: createEntityService({
      repo: () => Promise.resolve(ok(memory.entities)),
      briefs: () => Promise.resolve(ok(memory.briefs)),
      writable: (run) => run(),
    }),
    adaptations: createAdaptationService({
      repo: () => Promise.resolve(ok(memory.adaptations)),
      copies: () => Promise.resolve(ok(memory.copies)),
      writable: (run) => run(),
    }),
    rules: createRulesService({
      repo: () => Promise.resolve(ok(memory.rules)),
      writable: (run) => run(),
    }),
    preferences: createPreferencesStore(createMemoryStorage()),
    // DEMO no usa almacenamiento real: no se inventan cifras.
    // DEMO es solo memoria de una pestaña: siempre puede escribir.
    coordination: {
      getState: () => 'writer',
      subscribe: () => () => undefined,
      whenWriter: () => Promise.resolve(true),
    },
    backup: {
      export: () =>
        Promise.resolve(fail('not_implemented', 'DEMO no tiene datos reales que respaldar.')),
      inspect: () => Promise.resolve(fail('not_implemented', 'DEMO no admite respaldos.')),
      restore: () => Promise.resolve(fail('not_implemented', 'DEMO no admite respaldos.')),
    },
    storage: {
      get: () => Promise.resolve(ok(UNKNOWN_STORAGE)),
      requestPersistence: () => Promise.resolve(ok(UNKNOWN_STORAGE)),
    },
  };
  return Object.defineProperty(services, '__adapter', { value: DEMO_ADAPTER_MARKER });
}
