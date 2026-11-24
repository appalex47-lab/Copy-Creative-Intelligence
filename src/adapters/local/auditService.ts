import {
  auditFromEvaluation,
  MAX_AUDITS,
  validateAuditRecord,
  type AuditRecord,
} from '@/domain/audit';
import { currentVersion } from '@/domain/copy';
import { evaluateCopy } from '@/domain/copyRules';
import { toRulesConfig } from '@/domain/rulesConfig';
import { TEMPLATE_DOC } from '@/domain/rulesConfig';
import type {
  AuditRepository,
  BriefRepository,
  CopyRepository,
  RulesRepository,
} from '@/repositories/contracts';
import { fail, type AuditService, type Result } from '@/services/contracts';

export interface AuditServiceDeps {
  readonly repo: () => Promise<Result<AuditRepository>>;
  readonly copies: () => Promise<Result<CopyRepository>>;
  readonly briefs: () => Promise<Result<BriefRepository>>;
  readonly rules: () => Promise<Result<RulesRepository>>;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

const defaultId = (): string => `aud_${crypto.randomUUID().replaceAll('-', '')}`;

/**
 * Casos de uso de auditorías guardadas (S3.1). El servicio mismo calcula la evaluación con las reglas vigentes:
 * la interfaz no aporta puntaje ni hallazgos. Las auditorías nunca se editan; solo se crean o eliminan.
 */
export function createAuditService(deps: AuditServiceDeps): AuditService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? defaultId;
  const withRepo = async <T>(
    run: (r: AuditRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  return {
    list: (copyId) => withRepo((r) => r.list(copyId)),
    create: (i) =>
      deps.writable(() =>
        withRepo(async (r) => {
          const cr = await deps.copies();
          if (!cr.ok) return fail<AuditRecord>(cr.error.code, cr.error.message);
          const copy = await cr.value.get(i.copyId);
          if (!copy.ok) return fail<AuditRecord>('not_found', 'El copy no existe.');
          const br = await deps.briefs();
          if (!br.ok) return fail<AuditRecord>(br.error.code, br.error.message);
          const brief = await br.value.get(copy.value.briefId);
          if (!brief.ok) return fail<AuditRecord>('not_found', 'El brief del copy no existe.');
          const channel = brief.value.fields.channel;
          if (!channel)
            return fail<AuditRecord>(
              'validation_error',
              'El brief no tiene canal: elige uno para auditar.',
            );
          const cur = currentVersion(copy.value);
          const content = cur.content;
          const targetLabel = copy.value.label;
          const rr = await deps.rules();
          if (!rr.ok) return fail<AuditRecord>(rr.error.code, rr.error.message);
          const saved = await rr.value.get();
          if (!saved.ok) return fail<AuditRecord>(saved.error.code, saved.error.message);
          const doc = saved.value ?? TEMPLATE_DOC;
          const evaluation = evaluateCopy(
            { channel, offer: brief.value.fields.offer },
            content,
            toRulesConfig(doc),
          );
          const all = await r.count();
          if (!all.ok) return fail<AuditRecord>(all.error.code, all.error.message);
          if (all.value >= MAX_AUDITS)
            return fail<AuditRecord>(
              'validation_error',
              'Se alcanzó el máximo de auditorías guardadas; elimina algunas.',
            );
          const v = validateAuditRecord(
            auditFromEvaluation(evaluation, {
              id: newId(),
              copyId: copy.value.id,
              sourceVersion: cur.n,
              targetLabel,
              channel,
              rules: {
                isTemplate: saved.value === null,
                legends: doc.legends.length,
                brandTerms: doc.brandTerms.length,
              },
              createdAt: now().toISOString(),
            }),
          );
          if (!v.ok) return fail<AuditRecord>('validation_error', v.reason);
          return r.put(v.value);
        }),
      ),
    remove: (id) => deps.writable(() => withRepo((r) => r.remove(id))),
  };
}
