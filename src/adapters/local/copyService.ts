import {
  appendVersion,
  currentVersion,
  validateCopyRecord,
  validateLabel,
  validateTags,
  type CopyRecord,
} from '@/domain/copy';
import type { BriefRepository, CopyRepository } from '@/repositories/contracts';
import { valid } from '@/domain/validation';
import { fail, type CopyService, type Result } from '@/services/contracts';

export interface CopyServiceDeps {
  readonly copies: () => Promise<Result<CopyRepository>>;
  readonly briefs: () => Promise<Result<BriefRepository>>;
  /** Toda escritura espera el permiso de escritura de esta pestaña (P12). */
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

const defaultId = (): string => `cpy_${crypto.randomUUID().replaceAll('-', '')}`;

/** Casos de uso de copys. Sin red. Ids y fechas los pone el servicio. Las versiones solo se añaden. */
export function createCopyService(deps: CopyServiceDeps): CopyService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? defaultId;
  const repo = async <T>(run: (r: CopyRepository) => Promise<Result<T>>): Promise<Result<T>> => {
    const r = await deps.copies();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  const stamp = () => now().toISOString();
  /** Lee, transforma (función pura del dominio) y guarda; si la transformación falla, no se guarda nada. */
  const change = (
    id: string,
    transform: (c: CopyRecord) => { ok: true; value: CopyRecord } | { ok: false; reason: string },
  ) =>
    deps.writable(() =>
      repo(async (r) => {
        const cur = await r.get(id);
        if (!cur.ok) return cur;
        const t = transform(cur.value);
        return t.ok ? r.put(t.value) : fail('validation_error', t.reason);
      }),
    );
  const create = (briefId: string, label: unknown, content: unknown, tags: unknown) =>
    deps.writable(async () => {
      const b = await deps.briefs();
      if (!b.ok) return fail<CopyRecord>(b.error.code, b.error.message);
      const brief = await b.value.get(briefId);
      if (!brief.ok) return fail<CopyRecord>('not_found', 'El brief no existe.');
      const at = stamp();
      const candidate: unknown = {
        id: newId(),
        briefId,
        label,
        tags: tags ?? [],
        createdAt: at,
        updatedAt: at,
        versions: [{ n: 1, createdAt: at, content }],
      };
      const v = validateCopyRecord(candidate);
      if (!v.ok) return fail<CopyRecord>('validation_error', v.reason);
      return repo((r) => r.put(v.value));
    });

  return {
    list: (briefId) => repo((r) => r.list(briefId)),
    get: (id) => repo((r) => r.get(id)),
    create: (i) => create(i.briefId, i.label, i.content, i.tags),
    saveVersion: (i) =>
      change(i.id, (c) => {
        const r = appendVersion(c, i.content, stamp());
        return r.ok ? valid(r.value) : { ok: false, reason: r.reason };
      }),
    restoreVersion: (i) =>
      change(i.id, (c) => {
        const old = c.versions.find((v) => v.n === i.version);
        if (!old) return { ok: false, reason: 'La versión no existe.' };
        const r = appendVersion(c, old.content, stamp(), old.n);
        return r.ok ? valid(r.value) : { ok: false, reason: r.reason };
      }),
    updateMeta: (i) =>
      change(i.id, (c) => {
        const label = validateLabel(i.label);
        if (!label.ok) return { ok: false, reason: label.reason };
        const tags = validateTags(i.tags);
        if (!tags.ok) return { ok: false, reason: tags.reason };
        const at = stamp();
        const updatedAt = at < c.updatedAt ? c.updatedAt : at;
        return valid({ ...c, label: label.value, tags: tags.value, updatedAt });
      }),
    duplicate: (i) =>
      deps.writable(async () => {
        const src = await repo((r) => r.get(i.id));
        if (!src.ok) return src;
        return create(
          src.value.briefId,
          i.label,
          currentVersion(src.value).content,
          src.value.tags,
        );
      }),
    remove: (id) => deps.writable(() => repo((r) => r.remove(id))),
  };
}
