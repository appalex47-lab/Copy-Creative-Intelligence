import { TEMPLATE_DOC, type RulesDoc } from '@/domain/rulesConfig';
import type { RulesRepository } from '@/repositories/contracts';
import { fail, ok, type Result, type RulesService } from '@/services/contracts';

export interface RulesServiceDeps {
  readonly repo: () => Promise<Result<RulesRepository>>;
  /** Envuelve toda escritura (P12: solo la pestaña escritora guarda). */
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
}

/** Casos de uso de la configuración de reglas. Sin red. */
export function createRulesService(deps: RulesServiceDeps): RulesService {
  const withRepo = async <T>(
    run: (r: RulesRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  return {
    get: () =>
      withRepo(async (r) => {
        const got = await r.get();
        if (!got.ok) return got;
        const doc: RulesDoc = got.value ?? TEMPLATE_DOC;
        return ok({ doc, isTemplate: got.value === null });
      }),
    save: (doc) => deps.writable(() => withRepo((r) => r.save(doc))),
    resetToTemplate: () => deps.writable(() => withRepo((r) => r.clear())),
  };
}
