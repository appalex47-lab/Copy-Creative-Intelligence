import { useCallback, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { pieceAuditsCsv } from '@/domain/auditExport';
import { downloadTextFile } from '@/lib/download';
import { CHANNELS, type Channel } from '@/domain/brief';
import { CATEGORY_LABELS, SEVERITY_LABELS } from '@/domain/copyRules';
import {
  FINDING_STATUSES,
  ORIGIN_LABELS,
  STATUS_LABELS,
  diffPieceAudits,
  type FindingStatus,
  type PieceAudit,
  type PieceRecord,
} from '@/domain/piece';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import { formatLocalDateTime } from '@/lib/formatDate';
import type { AppError } from '@/services/contracts';

const VERDICTS = { apto: 'Apto', revisar: 'Revisar', no_apto: 'No apto' } as const;
const messageOf = (e: AppError): string =>
  e.code === 'validation_error' || e.code === 'conflict' ? e.message : describeError(e);

/**
 * Piezas creativas (S3.4, funciones 5 a 8 de la Fase 3). Una pieza es una imagen de «Recursos» con nombre y canal.
 * Se audita con las reglas deterministas sobre el texto de la imagen; no hay IA de visión. Una auditoría no aprueba
 * nada. Cada hallazgo muestra su origen y una persona decide su estado (abierto, resuelto o descartado).
 */
export function PiecesPage() {
  const services = useServices();
  const load = useCallback(async () => {
    const [p, r] = await Promise.all([services.pieces.list(), services.resources.list()]);
    if (!p.ok) return p;
    if (!r.ok) return r;
    return { ok: true as const, value: { pieces: p.value, resources: r.value } };
  }, [services]);
  const { state, retry } = useAsyncResource(load);
  const [error, setError] = useState<AppError | null>(null);
  const [name, setName] = useState('');
  const [channel, setChannel] = useState<Channel | ''>('');
  const [resourceId, setResourceId] = useState('');

  const create = async () => {
    setError(null);
    const r = await services.pieces.create({ name, channel, resourceId });
    if (!r.ok) return setError(r.error);
    setName('');
    setChannel('');
    setResourceId('');
    retry();
  };

  return (
    <section aria-labelledby="titulo-piezas">
      <h2 id="titulo-piezas" tabIndex={-1}>
        Piezas
      </h2>
      <p>
        Una pieza es una imagen de Recursos con su canal. Se audita con las mismas reglas de los
        copys, aplicadas al texto de la imagen (el validado por una persona; si no hay, el detectado
        por OCR, y se avisa). No se usa IA de imagen y una auditoría no aprueba ni publica nada.
      </p>
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {state.status === 'success' && (
        <>
          <form
            aria-label="Nueva pieza"
            onSubmit={(e) => {
              e.preventDefault();
              void create();
            }}
          >
            <div className="field">
              <label htmlFor="pie-name">Nombre de la pieza</label>
              <input
                id="pie-name"
                value={name}
                maxLength={120}
                onChange={(e) => setName(e.target.value)}
              />
            </div>
            <div className="field">
              <label htmlFor="pie-channel">Canal</label>
              <select
                id="pie-channel"
                value={channel}
                onChange={(e) => setChannel(e.target.value as Channel | '')}
              >
                <option value="">Elige un canal</option>
                {CHANNELS.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
            </div>
            <div className="field">
              <label htmlFor="pie-res">Imagen (de Recursos)</label>
              <select
                id="pie-res"
                value={resourceId}
                onChange={(e) => setResourceId(e.target.value)}
              >
                <option value="">Elige una imagen</option>
                {state.data.resources.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.name}
                  </option>
                ))}
              </select>
            </div>
            <div className="form-actions">
              <Button variant="primary" type="submit">
                Crear pieza
              </Button>
            </div>
          </form>
          {error && (
            <p role="alert" className="field-error">
              {messageOf(error)}
            </p>
          )}
          {state.data.pieces.length === 0 ? (
            <EmptyState
              title="Aún no hay piezas"
              description={
                state.data.resources.length === 0
                  ? 'Primero agrega una imagen en Recursos.'
                  : 'Crea una pieza con una imagen y un canal.'
              }
            />
          ) : (
            <>
              <ComparisonTable pieces={state.data.pieces} />
              <div className="form-actions">
                <Button
                  onClick={() =>
                    downloadTextFile(
                      `cci-piezas-${new Date().toISOString().slice(0, 10)}.csv`,
                      pieceAuditsCsv(state.data.pieces),
                      'text/csv',
                    )
                  }
                >
                  Descargar CSV de auditorías de piezas
                </Button>
              </div>
              <ul className="plain-list" aria-label="Piezas creativas">
                {state.data.pieces.map((p) => (
                  <li key={p.id}>
                    <PieceCard
                      initial={p}
                      resourceName={
                        state.data.resources.find((r) => r.id === p.resourceId)?.name ??
                        'imagen eliminada'
                      }
                      onRemoved={retry}
                    />
                  </li>
                ))}
              </ul>
            </>
          )}
        </>
      )}
    </section>
  );
}

function ComparisonTable({ pieces }: { readonly pieces: readonly PieceRecord[] }) {
  const rows = pieces
    .map((p) => ({ p, a: p.audits[0] }))
    .filter((r): r is { p: PieceRecord; a: PieceAudit } => r.a !== undefined)
    .sort((x, y) => y.a.score - x.a.score);
  if (rows.length < 2) return null;
  return (
    <table aria-label="Comparación de piezas auditadas">
      <caption>Comparación de la última auditoría de cada pieza (mayor puntaje primero)</caption>
      <thead>
        <tr>
          <th scope="col">Pieza</th>
          <th scope="col">Canal</th>
          <th scope="col">Puntaje</th>
          <th scope="col">Resultado</th>
          <th scope="col">Hallazgos abiertos</th>
        </tr>
      </thead>
      <tbody>
        {rows.map(({ p, a }) => (
          <tr key={p.id}>
            <th scope="row">{p.name}</th>
            <td>{p.channel}</td>
            <td>{a.score}</td>
            <td>{VERDICTS[a.verdict]}</td>
            <td>{a.findings.filter((f) => f.status === 'abierto').length}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function PieceCard({
  initial,
  resourceName,
  onRemoved,
}: {
  readonly initial: PieceRecord;
  readonly resourceName: string;
  readonly onRemoved: () => void;
}) {
  const services = useServices();
  const [piece, setPiece] = useState(initial);
  const [error, setError] = useState<AppError | null>(null);
  const [confirming, setConfirming] = useState(false);
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [msg, setMsg] = useState<string | null>(null);

  const audit = async () => {
    setError(null);
    setMsg(null);
    const r = await services.pieces.audit(piece.id);
    if (!r.ok) return setError(r.error);
    setPiece(r.value);
    setMsg('Auditoría guardada.');
  };
  const setStatus = async (a: PieceAudit, index: number, status: FindingStatus) => {
    setError(null);
    const r = await services.pieces.setFindingStatus({
      pieceId: piece.id,
      auditId: a.id,
      index,
      status,
      note: notes[`${a.id}-${String(index)}`] ?? a.findings[index]?.note ?? '',
    });
    if (!r.ok) return setError(r.error);
    setPiece(r.value);
  };
  const del = async () => {
    const r = await services.pieces.remove(piece.id);
    if (!r.ok) return setError(r.error);
    onRemoved();
  };

  const latest = piece.audits[0];
  const previous = piece.audits[1];
  const diff = latest && previous ? diffPieceAudits(previous, latest) : undefined;
  return (
    <Card title={piece.name} headingLevel={3}>
      <p className="field-hint">
        {piece.channel} · imagen: {resourceName}
      </p>
      <div className="form-actions">
        <Button
          variant="primary"
          onClick={() => void audit()}
          aria-label={`Auditar pieza ${piece.name}`}
        >
          Auditar pieza
        </Button>
      </div>
      {msg && (
        <p role="status" aria-live="polite">
          {msg}
        </p>
      )}
      {error && (
        <p role="alert" className="field-error">
          {messageOf(error)}
        </p>
      )}
      {latest && (
        <>
          <h4>Última auditoría</h4>
          <p>
            <strong>
              {latest.score} de 100 · {VERDICTS[latest.verdict]}
            </strong>{' '}
            · texto{' '}
            {latest.textSource === 'validado'
              ? 'validado por persona'
              : 'detectado por OCR (sin validar)'}{' '}
            · {formatLocalDateTime(latest.createdAt)}
          </p>
          {latest.blocked && <p>Había hallazgos críticos.</p>}
          {diff && (
            <p>
              Frente a la auditoría anterior:{' '}
              {diff.scoreDelta === 0
                ? 'mismo puntaje'
                : `${diff.scoreDelta > 0 ? '+' : ''}${String(diff.scoreDelta)} puntos`}
              ; {diff.added.length} hallazgos nuevos y {diff.resolved.length} que ya no aparecen.
            </p>
          )}
          {latest.findings.length === 0 ? (
            <p>Sin hallazgos con las reglas de ese momento.</p>
          ) : (
            <ul>
              {latest.findings.map((f, i) => {
                const id = `${latest.id}-${String(i)}`;
                return (
                  <li key={id}>
                    <p>
                      {SEVERITY_LABELS[f.severity]} · {CATEGORY_LABELS[f.category]}: {f.message}{' '}
                      <span className="field-hint">(origen: {ORIGIN_LABELS[f.origin]})</span>
                    </p>
                    <div className="field">
                      <label htmlFor={`st-${id}`}>Estado del hallazgo {String(i + 1)}</label>
                      <select
                        id={`st-${id}`}
                        value={f.status}
                        onChange={(e) => void setStatus(latest, i, e.target.value as FindingStatus)}
                      >
                        {FINDING_STATUSES.map((s) => (
                          <option key={s} value={s}>
                            {STATUS_LABELS[s]}
                          </option>
                        ))}
                      </select>
                    </div>
                    <div className="field">
                      <label htmlFor={`nt-${id}`}>Nota del hallazgo {String(i + 1)}</label>
                      <input
                        id={`nt-${id}`}
                        maxLength={300}
                        value={notes[id] ?? f.note ?? ''}
                        onChange={(e) => setNotes({ ...notes, [id]: e.target.value })}
                        onBlur={() => void setStatus(latest, i, f.status)}
                      />
                    </div>
                    {f.resolvedAt && (
                      <p className="field-hint">
                        {STATUS_LABELS[f.status]} el {formatLocalDateTime(f.resolvedAt)}
                      </p>
                    )}
                  </li>
                );
              })}
            </ul>
          )}
          {piece.audits.length > 1 && (
            <p className="field-hint">{piece.audits.length} auditorías guardadas de esta pieza.</p>
          )}
        </>
      )}
      {confirming ? (
        <div role="group" aria-label={`Confirmar eliminación de la pieza ${piece.name}`}>
          <p>¿Eliminar esta pieza y sus auditorías? La imagen en Recursos no se borra.</p>
          <div className="form-actions">
            <Button variant="primary" onClick={() => void del()}>
              Sí, eliminar pieza
            </Button>
            <Button onClick={() => setConfirming(false)}>Cancelar</Button>
          </div>
        </div>
      ) : (
        <div className="form-actions">
          <Button onClick={() => setConfirming(true)} aria-label={`Eliminar pieza ${piece.name}`}>
            Eliminar
          </Button>
        </div>
      )}
    </Card>
  );
}
