import {
  MAX_PIECE_AUDITS,
  MAX_PIECES,
  evaluatePiece,
  validatePieceInput,
  validatePieceRecord,
  withFindingStatus,
  type PieceRecord,
} from '@/domain/piece';
import { toRulesConfig, TEMPLATE_DOC } from '@/domain/rulesConfig';
import type {
  PieceRepository,
  ResourceRepository,
  RulesRepository,
} from '@/repositories/contracts';
import { fail, type PieceService, type Result } from '@/services/contracts';

export interface PieceServiceDeps {
  readonly repo: () => Promise<Result<PieceRepository>>;
  readonly resources: () => Promise<Result<ResourceRepository>>;
  readonly rules: () => Promise<Result<RulesRepository>>;
  readonly writable: <T>(run: () => Promise<Result<T>>) => Promise<Result<T>>;
  readonly now?: () => Date;
  readonly newId?: () => string;
}

const rand = () => crypto.randomUUID().replaceAll('-', '');

/** Casos de uso de piezas creativas (S3.4). El servicio calcula la auditoría; la interfaz no aporta puntajes. */
export function createPieceService(deps: PieceServiceDeps): PieceService {
  const now = deps.now ?? (() => new Date());
  const newId = deps.newId ?? (() => `pie_${rand()}`);
  const newAuditId = () => `pau_${rand()}`;
  const withRepo = async <T>(
    run: (r: PieceRepository) => Promise<Result<T>>,
  ): Promise<Result<T>> => {
    const r = await deps.repo();
    return r.ok ? run(r.value) : fail(r.error.code, r.error.message);
  };
  return {
    list: () => withRepo((r) => r.list()),
    create: (input) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          const v = validatePieceInput(input);
          if (!v.ok) return fail<PieceRecord>('validation_error', v.reason);
          const rr = await deps.resources();
          if (!rr.ok) return fail<PieceRecord>(rr.error.code, rr.error.message);
          const res = await rr.value.get(input.resourceId);
          if (!res.ok)
            return fail<PieceRecord>('validation_error', 'Elige una imagen de Recursos.');
          const n = await repo.count();
          if (!n.ok) return fail<PieceRecord>(n.error.code, n.error.message);
          if (n.value >= MAX_PIECES)
            return fail<PieceRecord>(
              'validation_error',
              'Se alcanzó el máximo de piezas; elimina alguna.',
            );
          const at = now().toISOString();
          return repo.put({
            id: newId(),
            name: v.value.name,
            channel: v.value.channel,
            resourceId: input.resourceId,
            createdAt: at,
            updatedAt: at,
            audits: [],
          });
        }),
      ),
    audit: (id) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          const cur = await repo.get(id);
          if (!cur.ok) return cur;
          if (cur.value.audits.length >= MAX_PIECE_AUDITS)
            return fail<PieceRecord>(
              'validation_error',
              'Esta pieza ya tiene el máximo de auditorías; elimina la pieza y créala de nuevo si necesitas más.',
            );
          const rr = await deps.resources();
          if (!rr.ok) return fail<PieceRecord>(rr.error.code, rr.error.message);
          const res = await rr.value.get(cur.value.resourceId);
          if (!res.ok)
            return fail<PieceRecord>('not_found', 'La imagen de esta pieza ya no existe.');
          const rules = await deps.rules();
          if (!rules.ok) return fail<PieceRecord>(rules.error.code, rules.error.message);
          const saved = await rules.value.get();
          if (!saved.ok) return fail<PieceRecord>(saved.error.code, saved.error.message);
          const ev = evaluatePiece(
            cur.value.channel,
            res.value,
            toRulesConfig(saved.value ?? TEMPLATE_DOC),
          );
          if (!ev.ok) return fail<PieceRecord>('validation_error', ev.reason);
          const at = now().toISOString();
          const next = {
            ...cur.value,
            updatedAt: at,
            audits: [{ ...ev.value, id: newAuditId(), createdAt: at }, ...cur.value.audits],
          };
          const v = validatePieceRecord(next);
          if (!v.ok) return fail<PieceRecord>('validation_error', v.reason);
          return repo.put(v.value);
        }),
      ),
    setFindingStatus: (i) =>
      deps.writable(() =>
        withRepo(async (repo) => {
          const cur = await repo.get(i.pieceId);
          if (!cur.ok) return cur;
          const r = withFindingStatus(
            cur.value,
            i.auditId,
            i.index,
            i.status,
            i.note,
            now().toISOString(),
          );
          if (!r.ok) return fail<PieceRecord>('validation_error', r.reason);
          return repo.put(r.value);
        }),
      ),
    remove: (id) => deps.writable(() => withRepo((r) => r.remove(id))),
  };
}
