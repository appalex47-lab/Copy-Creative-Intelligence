import { useCallback, useState } from 'react';
import { Button } from '@/components/Button';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { diffAudits, previousOf, type AuditRecord } from '@/domain/audit';
import type { CopyRecord } from '@/domain/copy';
import { CATEGORY_LABELS, SEVERITY_LABELS } from '@/domain/copyRules';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import { formatLocalDateTime } from '@/lib/formatDate';
import type { AppError } from '@/services/contracts';

const VERDICTS = { apto: 'Apto', revisar: 'Revisar', no_apto: 'No apto' } as const;
const messageOf = (e: AppError): string =>
  e.code === 'validation_error' || e.code === 'conflict' ? e.message : describeError(e);

/**
 * Auditorías guardadas de un copy (S3.1). Cada una es una foto inmutable de la revisión por reglas; se compara con
 * la anterior del mismo objetivo. No son aprobaciones.
 */
export function AuditsSection({
  copy,
  onChanged,
}: {
  readonly copy: CopyRecord;
  readonly onChanged: (message: string) => void;
}) {
  const services = useServices();
  const [version, setVersion] = useState(0);
  const [confirm, setConfirm] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const load = useCallback(async () => {
    void version;
    return services.audits.list(copy.id);
  }, [services, copy.id, version]);
  const { state, retry } = useAsyncResource(load);
  const list = state.status === 'success' ? state.data : [];

  const save = async () => {
    setError(null);
    const r = await services.audits.create({ copyId: copy.id });
    if (!r.ok) {
      setError(messageOf(r.error));
      return;
    }
    setVersion((n) => n + 1);
    onChanged(`Auditoría guardada: ${r.value.score} de 100 · ${VERDICTS[r.value.verdict]}.`);
  };
  const remove = async (id: string) => {
    setError(null);
    const r = await services.audits.remove(id);
    if (!r.ok) {
      setError(messageOf(r.error));
      setConfirm(null);
      return;
    }
    setConfirm(null);
    setVersion((n) => n + 1);
    onChanged('Auditoría eliminada.');
  };

  return (
    <section aria-label={`Auditorías de ${copy.label}`}>
      <h5>Auditorías guardadas ({list.length})</h5>
      <p className="field-hint">
        Cada auditoría es una foto de la revisión por reglas de la versión vigente del copy: no se
        edita, no incluye variantes ni adaptaciones y no aprueba nada.
      </p>
      <div className="form-actions">
        <Button onClick={() => void save()} aria-label={`Guardar auditoría de ${copy.label}`}>
          Guardar auditoría
        </Button>
      </div>
      {error && <p role="alert">{error}</p>}
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {list.length > 0 && (
        <ul className="plain-list">
          {list.map((a) => (
            <AuditItem
              key={a.id}
              audit={a}
              previous={previousOf(list, a)}
              confirming={confirm === a.id}
              onAskDelete={() => setConfirm(a.id)}
              onCancel={() => setConfirm(null)}
              onDelete={() => void remove(a.id)}
            />
          ))}
        </ul>
      )}
    </section>
  );
}

function AuditItem({
  audit,
  previous,
  confirming,
  onAskDelete,
  onCancel,
  onDelete,
}: {
  readonly audit: AuditRecord;
  readonly previous: AuditRecord | undefined;
  readonly confirming: boolean;
  readonly onAskDelete: () => void;
  readonly onCancel: () => void;
  readonly onDelete: () => void;
}) {
  const diff = previous ? diffAudits(previous, audit) : undefined;
  return (
    <li>
      <p>
        <strong>
          {audit.score} de 100 · {VERDICTS[audit.verdict]}
        </strong>{' '}
        · {audit.targetLabel} · versión {audit.sourceVersion} · {audit.channel} ·{' '}
        {formatLocalDateTime(audit.createdAt)}
      </p>
      {audit.blocked && <p>Había hallazgos críticos.</p>}
      {audit.findings.length === 0 ? (
        <p>Sin hallazgos con las reglas de ese momento.</p>
      ) : (
        <ul>
          {audit.findings.map((f, i) => (
            <li key={`${f.ruleId}-${i}`}>
              {SEVERITY_LABELS[f.severity]} · {CATEGORY_LABELS[f.category]}: {f.message}
            </li>
          ))}
        </ul>
      )}
      <p className="field-hint">
        {audit.rules.isTemplate
          ? 'Reglas: plantilla de ejemplo.'
          : `Reglas: ${audit.rules.legends} leyendas y ${audit.rules.brandTerms} términos.`}
      </p>
      {diff && (
        <p>
          Frente a la auditoría anterior:{' '}
          {diff.scoreDelta === 0
            ? 'mismo puntaje'
            : `${diff.scoreDelta > 0 ? '+' : ''}${diff.scoreDelta} puntos`}
          ; {diff.added.length} hallazgos nuevos y {diff.resolved.length} resueltos.
          {diff.added.length > 0 && ` Nuevos: ${diff.added.map((f) => f.message).join(' · ')}`}
          {diff.resolved.length > 0 &&
            ` Resueltos: ${diff.resolved.map((f) => f.message).join(' · ')}`}
        </p>
      )}
      {confirming ? (
        <div
          role="group"
          aria-label={`Confirmar eliminación de la auditoría del ${formatLocalDateTime(audit.createdAt)}`}
        >
          <p>¿Eliminar esta auditoría? No se puede deshacer.</p>
          <div className="form-actions">
            <Button variant="primary" onClick={onDelete}>
              Sí, eliminar auditoría
            </Button>
            <Button onClick={onCancel}>Cancelar</Button>
          </div>
        </div>
      ) : (
        <div className="form-actions">
          <Button
            onClick={onAskDelete}
            aria-label={`Eliminar auditoría de ${audit.targetLabel} del ${formatLocalDateTime(audit.createdAt)}`}
          >
            Eliminar
          </Button>
        </div>
      )}
    </li>
  );
}
