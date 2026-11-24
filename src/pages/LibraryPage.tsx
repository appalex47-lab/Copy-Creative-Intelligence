import { useCallback } from 'react';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { buildLibrary, type LibraryEntry } from '@/domain/library';
import { pct } from '@/domain/measure';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';

/** Biblioteca de aprendizaje (S4.2): resume lo ya guardado (revisiones, auditorías, mediciones). No captura nada nuevo. */
export function LibraryPage() {
  const services = useServices();
  const load = useCallback(async () => {
    const [r, a, p, m] = await Promise.all([
      services.reviews.list(),
      services.audits.list(),
      services.pieces.list(),
      services.measures.list(),
    ]);
    if (!r.ok) return r;
    if (!a.ok) return a;
    if (!p.ok) return p;
    if (!m.ok) return m;
    return {
      ok: true as const,
      value: buildLibrary({
        reviews: r.value,
        copyAudits: a.value,
        pieces: p.value,
        measures: m.value,
      }),
    };
  }, [services]);
  const { state, retry } = useAsyncResource(load);
  const list = (title: string, items: readonly LibraryEntry[], empty: string) => (
    <Card title={title} headingLevel={3}>
      {items.length === 0 ? (
        <p className="field-hint">{empty}</p>
      ) : (
        <ul aria-label={title}>
          {items.map((e) => (
            <li key={`${e.type}-${e.label}`}>
              <strong>{e.label}</strong> ({e.type}) · {e.score ?? 'sin puntaje'}
              {e.reasons.length > 0 ? ` — ${e.reasons.join('; ')}` : ''}
            </li>
          ))}
        </ul>
      )}
    </Card>
  );
  return (
    <section aria-labelledby="titulo-biblioteca">
      <h2 id="titulo-biblioteca" tabIndex={-1}>
        Biblioteca
      </h2>
      <p>
        Lo que ya aprendiste con tus propias revisiones, auditorías y mediciones: qué se aprobó, qué
        se rechazó y por qué, los errores que más se repiten y los mejores resultados. Se arma sola
        con lo guardado; no se escribe aquí.
      </p>
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {state.status === 'success' &&
        (state.data.approved.length +
          state.data.rejected.length +
          state.data.recurring.length +
          state.data.best.length +
          state.data.experiments.length ===
        0 ? (
          <EmptyState
            title="La biblioteca está vacía"
            description="Se llenará con revisiones aprobadas o rechazadas, auditorías repetidas y mediciones."
          />
        ) : (
          <>
            {list('Aprobados', state.data.approved, 'Aún no hay revisiones aprobadas.')}
            {list('Rechazados y por qué', state.data.rejected, 'Aún no hay revisiones rechazadas.')}
            <Card title="Errores recurrentes" headingLevel={3}>
              {state.data.recurring.length === 0 ? (
                <p className="field-hint">Ningún hallazgo se ha repetido todavía.</p>
              ) : (
                <ol aria-label="Errores recurrentes">
                  {state.data.recurring.map((x) => (
                    <li key={x.text}>
                      {x.text} ({x.count} veces)
                    </li>
                  ))}
                </ol>
              )}
            </Card>
            <Card title="Mejores resultados (mín. 100 impresiones)" headingLevel={3}>
              {state.data.best.length === 0 ? (
                <p className="field-hint">Aún no hay resultados con muestra suficiente.</p>
              ) : (
                <ol aria-label="Mejores resultados">
                  {state.data.best.map((b) => (
                    <li key={b.label}>
                      {b.label}: CTR {pct(b.ctr)} · conversión {pct(b.conversion)} ({b.impressions}{' '}
                      impresiones)
                    </li>
                  ))}
                </ol>
              )}
            </Card>
            {state.data.experiments.length > 0 && (
              <Card title="Conclusiones de experimentos" headingLevel={3}>
                <ul aria-label="Conclusiones de experimentos">
                  {state.data.experiments.map((x) => (
                    <li key={x.name}>
                      <strong>{x.name}</strong>: {x.conclusion}
                    </li>
                  ))}
                </ul>
              </Card>
            )}
          </>
        ))}
    </section>
  );
}
