import { useCallback, useMemo, useState } from 'react';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { Card } from '@/components/Card';
import { CHANNELS, type Channel } from '@/domain/brief';
import { Button } from '@/components/Button';
import { copyAuditsCsv } from '@/domain/auditExport';
import { downloadTextFile } from '@/lib/download';
import { filterAudits } from '@/domain/auditFilter';
import { CATEGORY_LABELS, SEVERITY_LABELS, type Verdict } from '@/domain/copyRules';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { formatLocalDateTime } from '@/lib/formatDate';

const VERDICTS: Readonly<Record<Verdict, string>> = {
  apto: 'Apto',
  revisar: 'Revisar',
  no_apto: 'No apto',
};

/**
 * Consulta de todas las auditorías guardadas (S3.2, función 9 de la Fase 3): filtros por resultado, canal, fecha y
 * texto. Solo lectura: las auditorías se crean y eliminan desde el copy. Consultar no implica aprobar.
 */
export function AuditsPage() {
  const services = useServices();
  const load = useCallback(() => services.audits.list(), [services]);
  const { state, retry } = useAsyncResource(load);
  const [verdict, setVerdict] = useState<Verdict | ''>('');
  const [channel, setChannel] = useState<Channel | ''>('');
  const [from, setFrom] = useState('');
  const [to, setTo] = useState('');
  const [query, setQuery] = useState('');
  const shown = useMemo(
    () =>
      state.status === 'success'
        ? filterAudits(state.data, {
            ...(verdict ? { verdict } : {}),
            ...(channel ? { channel } : {}),
            ...(from ? { from } : {}),
            ...(to ? { to } : {}),
            query,
          })
        : [],
    [state, verdict, channel, from, to, query],
  );
  return (
    <section aria-labelledby="titulo-auditorias">
      <h2 id="titulo-auditorias" tabIndex={-1}>
        Auditorías
      </h2>
      <p>
        Todas las auditorías guardadas de copys, de la más reciente a la más antigua. Se crean y se
        eliminan desde cada copy (Briefs → Copys). Consultarlas no aprueba ni publica nada.
      </p>
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {state.status === 'success' &&
        (state.data.length === 0 ? (
          <EmptyState
            title="Aún no hay auditorías guardadas"
            description="Guarda una desde un copy con «Guardar auditoría»."
          />
        ) : (
          <>
            <form aria-label="Filtros de auditorías" onSubmit={(e) => e.preventDefault()}>
              <div className="field">
                <label htmlFor="aud-verdict">Resultado</label>
                <select
                  id="aud-verdict"
                  value={verdict}
                  onChange={(e) => setVerdict(e.target.value as Verdict | '')}
                >
                  <option value="">Todos</option>
                  {(Object.keys(VERDICTS) as Verdict[]).map((v) => (
                    <option key={v} value={v}>
                      {VERDICTS[v]}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label htmlFor="aud-channel">Canal</label>
                <select
                  id="aud-channel"
                  value={channel}
                  onChange={(e) => setChannel(e.target.value as Channel | '')}
                >
                  <option value="">Todos</option>
                  {CHANNELS.map((c) => (
                    <option key={c} value={c}>
                      {c}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label htmlFor="aud-from">Desde</label>
                <input
                  id="aud-from"
                  type="date"
                  value={from}
                  onChange={(e) => setFrom(e.target.value)}
                />
              </div>
              <div className="field">
                <label htmlFor="aud-to">Hasta</label>
                <input id="aud-to" type="date" value={to} onChange={(e) => setTo(e.target.value)} />
              </div>
              <div className="field">
                <label htmlFor="aud-query">Buscar (copy u hallazgo)</label>
                <input
                  id="aud-query"
                  type="search"
                  autoComplete="off"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                />
              </div>
            </form>
            <p role="status" aria-live="polite">
              {shown.length} de {state.data.length} auditorías.
            </p>
            <div className="form-actions">
              <Button
                onClick={() =>
                  downloadTextFile(
                    `cci-auditorias-${new Date().toISOString().slice(0, 10)}.csv`,
                    copyAuditsCsv(shown),
                    'text/csv',
                  )
                }
                disabled={shown.length === 0}
              >
                Descargar CSV de las auditorías mostradas
              </Button>
            </div>
            <ul className="plain-list" aria-label="Auditorías guardadas">
              {shown.map((a) => (
                <li key={a.id}>
                  <Card title={a.targetLabel} headingLevel={3}>
                    <p>
                      <strong>
                        {a.score} de 100 · {VERDICTS[a.verdict]}
                      </strong>{' '}
                      · versión {a.sourceVersion} · {a.channel} · {formatLocalDateTime(a.createdAt)}
                    </p>
                    {a.blocked && <p>Había hallazgos críticos.</p>}
                    {a.findings.length === 0 ? (
                      <p>Sin hallazgos con las reglas de ese momento.</p>
                    ) : (
                      <ul>
                        {a.findings.map((f, i) => (
                          <li key={`${f.ruleId}-${i}`}>
                            {SEVERITY_LABELS[f.severity]} · {CATEGORY_LABELS[f.category]}:{' '}
                            {f.message}
                          </li>
                        ))}
                      </ul>
                    )}
                  </Card>
                </li>
              ))}
            </ul>
          </>
        ))}
    </section>
  );
}
