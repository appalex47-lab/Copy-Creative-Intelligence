import { formatLocalDateTime } from '@/lib/formatDate';
import { useCallback, useRef } from 'react';
import { buildDashboard } from '@/domain/dashboard';
import { isReviewDue } from '@/domain/reminder';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import type { ActivityKind } from '@/domain/activity';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';

const KIND_LABEL: Record<ActivityKind, string> = {
  app_opened: 'Se abrió la aplicación',
  profile_changed: 'Cambió el perfil local',
  setting_changed: 'Cambió una preferencia',
  backup_exported: 'Se exportó un respaldo',
  backup_imported: 'Se importó un respaldo',
  storage_error: 'Error de almacenamiento',
};

/** Resumen: la actividad local real, o un estado vacío explícito. Consume solo contratos. */
export function HomePage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const load = useCallback(() => services.activity.listRecent(), [services]);
  const { state, retry } = useAsyncResource(load);
  // Recordatorio semanal (S4.2): sin cuentas ni notificaciones, solo un aviso al abrir la app.
  const loadDue = useCallback(async () => {
    const [r, a] = await Promise.all([services.reviews.list(), services.audits.list()]);
    if (!r.ok || !a.ok) return { ok: true as const, value: false };
    return {
      ok: true as const,
      value: isReviewDue(
        [...r.value.map((x) => x.updatedAt), ...a.value.map((x) => x.createdAt)],
        new Date(),
      ),
    };
  }, [services]);
  const { state: due } = useAsyncResource(loadDue);
  const loadBoard = useCallback(async () => {
    const [c, p, r, pr, m] = await Promise.all([
      services.copies.list(),
      services.pieces.list(),
      services.reviews.list(),
      services.promos.list(),
      services.measures.list(),
    ]);
    if (!c.ok) return c;
    if (!p.ok) return p;
    if (!r.ok) return r;
    if (!pr.ok) return pr;
    if (!m.ok) return m;
    return {
      ok: true as const,
      value: buildDashboard({
        copies: c.value,
        pieces: p.value,
        reviews: r.value,
        promos: pr.value,
        measures: m.value,
        today: new Date().toISOString().slice(0, 10),
      }),
    };
  }, [services]);
  const { state: board } = useAsyncResource(loadBoard);

  // Tras reintentar, el botón desaparece: el foco se devuelve al encabezado para no perderlo.
  const onRetry = () => {
    heading.current?.focus();
    retry();
  };

  return (
    <section aria-labelledby="titulo-inicio">
      <h2 id="titulo-inicio" tabIndex={-1} ref={heading}>
        Resumen
      </h2>
      {due.status === 'success' && due.data && (
        <p role="note">
          <strong>Recordatorio semanal:</strong> no hay revisiones ni auditorías de los últimos 7
          días. Revisa las piezas que vayan a publicarse.
        </p>
      )}
      {board.status === 'success' && (
        <section aria-label="Tablero de control">
          <h3>Tablero de control</h3>
          <dl aria-label="Pendientes">
            <dt>Sin revisar</dt>
            <dd>{board.data.unreviewed.length}</dd>
            <dt>Revisiones por liberar</dt>
            <dd>{board.data.toRelease}</dd>
            <dt>Liberadas para publicar</dt>
            <dd>{board.data.released}</dd>
            <dt>Rechazadas</dt>
            <dd>{board.data.rejected}</dd>
            <dt>Mediciones registradas</dt>
            <dd>{board.data.measures}</dd>
          </dl>
          {board.data.unreviewed.length > 0 && (
            <p className="field-hint">
              Sin revisar: {board.data.unreviewed.slice(0, 5).join(', ')}
              {board.data.unreviewed.length > 5 ? '…' : ''}
            </p>
          )}
          {board.data.promosExpired.length > 0 && (
            <p role="note">
              <strong>Promociones vencidas:</strong> {board.data.promosExpired.join(', ')}. Verifica
              que ningún copy o pieza las siga usando.
            </p>
          )}
          {board.data.promosSoon.length > 0 && (
            <p role="note">
              <strong>Promociones por vencer (7 días):</strong> {board.data.promosSoon.join(', ')}.
            </p>
          )}
        </section>
      )}
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? onRetry : undefined} />
      )}
      {state.status === 'success' &&
        (state.data.length === 0 ? (
          <EmptyState
            title="Sin actividad reciente"
            description="Aún no hay acciones locales registradas en este navegador."
          />
        ) : (
          <>
            <h3>Actividad reciente</h3>
            <ul>
              {state.data.map((e) => (
                <li key={e.id}>
                  {KIND_LABEL[e.kind]} · <time dateTime={e.at}>{formatLocalDateTime(e.at)}</time>
                </li>
              ))}
            </ul>
          </>
        ))}
    </section>
  );
}
