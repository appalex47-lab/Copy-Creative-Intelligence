import { useCallback, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import type { AuditRecord } from '@/domain/audit';
import type { PieceRecord } from '@/domain/piece';
import { MASTER_PROMPT } from '@/domain/masterPrompt';
import {
  CHECKLIST,
  COMMERCIAL_CHECKS,
  DIMENSIONS,
  FILTER_LABELS,
  FILTER_STATES,
  FINAL_LABELS,
  FINAL_STATES,
  STAGES,
  STAGE_LABELS,
  VERDICT_LABELS,
  summarizeReview,
  type FilterState,
  type FinalApproval,
  type ReviewStage,
  type ReviewFinding,
  type ReviewRecord,
  type ReviewTargetType,
} from '@/domain/review';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import { formatLocalDateTime } from '@/lib/formatDate';
import type { AppError } from '@/services/contracts';

const messageOf = (e: AppError): string =>
  e.code === 'validation_error' ? e.message : describeError(e);

interface Draft {
  scores: Record<string, string>;
  checklist: boolean[];
  commercial: boolean[];
  findings: ReviewFinding[];
  creativeFilter: FilterState;
  commercialFilter: FilterState;
  reviewer: string;
  stage: ReviewStage;
  finalApproval: FinalApproval;
  approver: string;
}

const blankDraft = (r?: ReviewRecord): Draft => ({
  scores: Object.fromEntries(DIMENSIONS.map((d) => [d.id, r?.scores[d.id]?.toString() ?? ''])),
  checklist: r ? [...r.checklist] : CHECKLIST.map(() => false),
  commercial: r ? [...r.commercial] : COMMERCIAL_CHECKS.map(() => false),
  findings: r ? [...r.findings] : [],
  creativeFilter: r?.creativeFilter ?? 'pendiente',
  commercialFilter: r?.commercialFilter ?? 'pendiente',
  reviewer: r?.reviewer ?? '',
  stage: r?.stage ?? 'validacion',
  finalApproval: r?.finalApproval ?? 'pendiente',
  approver: r?.approver ?? '',
});

/**
 * Revisión de calidad (S4.1): la persona califica con la matriz CCI de 8 dimensiones, el checklist de 12 puntos, los
 * hallazgos de 4 elementos y los dos filtros (creativo y comercial). La app calcula puntaje, banda y veredicto y dice
 * qué falta; no inventa calificaciones ni datos comerciales y no publica nada.
 */
export function ReviewsPage() {
  const services = useServices();
  const load = useCallback(async () => {
    const [c, p, r, a] = await Promise.all([
      services.copies.list(),
      services.pieces.list(),
      services.reviews.list(),
      services.audits.list(),
    ]);
    if (!c.ok) return c;
    if (!p.ok) return p;
    if (!r.ok) return r;
    if (!a.ok) return a;
    return {
      ok: true as const,
      value: { copies: c.value, pieces: p.value, reviews: r.value, audits: a.value },
    };
  }, [services]);
  const { state, retry } = useAsyncResource(load);
  const [target, setTarget] = useState('');
  const [draft, setDraft] = useState<Draft | null>(null);
  const [error, setError] = useState<AppError | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const [copied, setCopied] = useState(false);

  const choose = (value: string, reviews: readonly ReviewRecord[]) => {
    setTarget(value);
    setError(null);
    setMsg(null);
    if (!value) return setDraft(null);
    const [type, id] = value.split(':') as [ReviewTargetType, string];
    setDraft(blankDraft(reviews.find((r) => r.targetType === type && r.targetId === id)));
  };

  const save = async () => {
    if (!draft || !target) return;
    setError(null);
    setMsg(null);
    const [type, id] = target.split(':') as [ReviewTargetType, string];
    const r = await services.reviews.save({
      targetType: type,
      targetId: id,
      body: {
        scores: Object.fromEntries(
          DIMENSIONS.map((d) => {
            const t = draft.scores[d.id]?.trim() ?? '';
            return [d.id, t === '' ? null : Number(t.replace(',', '.'))];
          }),
        ),
        checklist: draft.checklist,
        commercial: draft.commercial,
        findings: draft.findings,
        creativeFilter: draft.creativeFilter,
        commercialFilter: draft.commercialFilter,
        reviewer: draft.reviewer,
        stage: draft.stage,
        finalApproval: draft.finalApproval,
        approver: draft.approver,
      },
    });
    if (!r.ok) return setError(r.error);
    setMsg('Revisión guardada.');
    retry();
  };

  const copyPrompt = async () => {
    try {
      await navigator.clipboard.writeText(MASTER_PROMPT);
      setCopied(true);
    } catch {
      setCopied(false);
    }
  };

  return (
    <section aria-labelledby="titulo-revision">
      <h2 id="titulo-revision" tabIndex={-1}>
        Revisión
      </h2>
      <p>
        Califica un copy o una pieza con la metodología Copy &amp; Creative Intelligence: matriz de
        8 dimensiones, checklist, hallazgos con impacto y recomendación, y dos filtros
        independientes (creativo y comercial) que deben estar aprobados para poder publicar. Tú
        pones las calificaciones; la app no las inventa ni publica nada.
      </p>
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {state.status === 'success' && (
        <>
          <div className="field">
            <label htmlFor="rev-target">¿Qué vas a revisar?</label>
            <select
              id="rev-target"
              value={target}
              onChange={(e) => choose(e.target.value, state.data.reviews)}
            >
              <option value="">Elige un copy o una pieza</option>
              <optgroup label="Copys">
                {state.data.copies.map((c) => (
                  <option key={c.id} value={`copy:${c.id}`}>
                    {c.label}
                  </option>
                ))}
              </optgroup>
              <optgroup label="Piezas">
                {state.data.pieces.map((p) => (
                  <option key={p.id} value={`pieza:${p.id}`}>
                    {p.name}
                  </option>
                ))}
              </optgroup>
            </select>
          </div>
          {state.data.copies.length + state.data.pieces.length === 0 && (
            <EmptyState
              title="Aún no hay nada que revisar"
              description="Crea un copy en Briefs o una pieza en Piezas."
            />
          )}
          {draft && (
            <ReviewEditor
              draft={draft}
              setDraft={setDraft}
              onSave={() => void save()}
              error={error}
              msg={msg}
              saved={state.data.reviews.find((r) => `${r.targetType}:${r.targetId}` === target)}
              auto={autoAlert(target, state.data.audits, state.data.pieces)}
            />
          )}
          {state.data.reviews.length > 0 && (
            <Card title="Revisiones guardadas" headingLevel={3}>
              <ul aria-label="Revisiones guardadas">
                {state.data.reviews.map((r) => {
                  const s = summarizeReview(r);
                  return (
                    <li key={r.id}>
                      {r.targetLabel} ({r.targetType}) · {s.score ?? 'sin puntaje'} ·{' '}
                      {VERDICT_LABELS[s.verdict]} · {s.publishable ? 'publicable' : 'no publicable'}{' '}
                      · {STAGE_LABELS[r.stage]} · {FINAL_LABELS[r.finalApproval]} ·{' '}
                      {formatLocalDateTime(r.updatedAt)}
                    </li>
                  );
                })}
              </ul>
            </Card>
          )}
        </>
      )}
      <Card title="Prompt maestro para auditar con una IA" headingLevel={3}>
        <p className="field-hint">
          La app no usa ninguna IA. Copia este texto para usarlo tú con la IA que elijas. Revisa qué
          información de tus piezas compartes con ella.
        </p>
        <div className="form-actions">
          <Button onClick={() => void copyPrompt()}>Copiar prompt maestro</Button>
        </div>
        {copied && (
          <p role="status" aria-live="polite">
            Prompt copiado.
          </p>
        )}
      </Card>
    </section>
  );
}

function ReviewEditor({
  draft,
  setDraft,
  onSave,
  error,
  msg,
  saved,
  auto,
}: {
  readonly draft: Draft;
  readonly setDraft: (d: Draft) => void;
  readonly onSave: () => void;
  readonly error: AppError | null;
  readonly msg: string | null;
  readonly saved: ReviewRecord | undefined;
  readonly auto: string | null;
}) {
  // Resumen en vivo con lo que hay escrito (sin guardar); un valor inválido simplemente cuenta como sin calificar.
  const live = summarizeReview({
    scores: Object.fromEntries(
      DIMENSIONS.map((d) => {
        const n = Number((draft.scores[d.id] ?? '').replace(',', '.'));
        const empty = (draft.scores[d.id] ?? '').trim() === '';
        return [d.id, empty || !Number.isFinite(n) || n < 0 || n > d.max ? null : n];
      }),
    ) as ReviewRecord['scores'],
    checklist: draft.checklist,
    findings: draft.findings,
    creativeFilter: draft.creativeFilter,
    commercialFilter: draft.commercialFilter,
  });
  const set = (patch: Partial<Draft>) => setDraft({ ...draft, ...patch });
  const setFinding = (i: number, patch: Partial<ReviewFinding>) =>
    set({ findings: draft.findings.map((f, j) => (j === i ? { ...f, ...patch } : f)) });

  return (
    <form
      aria-label="Revisión de calidad"
      onSubmit={(e) => {
        e.preventDefault();
        onSave();
      }}
    >
      {auto && (
        <p role="note">
          <strong>Alerta por reglas (automática):</strong> {auto} Es solo una alerta de apoyo; la
          calificación oficial es esta matriz.
        </p>
      )}
      <fieldset>
        <legend>Matriz de evaluación (0 a 100 puntos)</legend>
        {DIMENSIONS.map((d) => (
          <div className="field" key={d.id}>
            <label htmlFor={`dim-${d.id}`}>
              {d.label} (máx. {d.max})
            </label>
            <input
              id={`dim-${d.id}`}
              inputMode="decimal"
              value={draft.scores[d.id] ?? ''}
              onChange={(e) => set({ scores: { ...draft.scores, [d.id]: e.target.value } })}
              aria-describedby={`dim-h-${d.id}`}
            />
            <p className="field-hint" id={`dim-h-${d.id}`}>
              {d.hint} Déjalo vacío si aún no lo evalúas.
            </p>
          </div>
        ))}
      </fieldset>

      <fieldset>
        <legend>Checklist de aprobación ({live.checklistDone}/12)</legend>
        {CHECKLIST.map((c, i) => (
          <label key={c} style={{ display: 'block' }}>
            <input
              type="checkbox"
              checked={draft.checklist[i] ?? false}
              onChange={(e) =>
                set({ checklist: draft.checklist.map((v, j) => (j === i ? e.target.checked : v)) })
              }
            />{' '}
            {c}
          </label>
        ))}
        <Button onClick={() => set({ checklist: CHECKLIST.map(() => false) })}>
          Reiniciar checklist
        </Button>
      </fieldset>

      <fieldset>
        <legend>Hallazgos</legend>
        {draft.findings.length === 0 && <p className="field-hint">Sin hallazgos.</p>}
        {draft.findings.map((f, i) => (
          <div key={i} role="group" aria-label={`Hallazgo ${String(i + 1)}`}>
            {(
              [
                ['hallazgo', 'Hallazgo (qué está mal)'],
                ['impacto', 'Impacto (por qué importa)'],
                ['recomendacion', 'Recomendación (qué hacer)'],
                ['correccion', 'Corrección propuesta (opcional)'],
              ] as const
            ).map(([k, label]) => (
              <div className="field" key={k}>
                <label htmlFor={`f-${String(i)}-${k}`}>
                  {label} {String(i + 1)}
                </label>
                <input
                  id={`f-${String(i)}-${k}`}
                  maxLength={500}
                  value={f[k] ?? ''}
                  onChange={(e) => setFinding(i, { [k]: e.target.value })}
                />
              </div>
            ))}
            <label style={{ display: 'block' }}>
              <input
                type="checkbox"
                checked={f.bloqueante}
                onChange={(e) => setFinding(i, { bloqueante: e.target.checked })}
              />{' '}
              Bloquea la publicación (error comercial crítico) {String(i + 1)}
            </label>
            <Button onClick={() => set({ findings: draft.findings.filter((_, j) => j !== i) })}>
              Quitar hallazgo {String(i + 1)}
            </Button>
          </div>
        ))}
        <Button
          onClick={() =>
            set({
              findings: [
                ...draft.findings,
                { hallazgo: '', impacto: '', recomendacion: '', bloqueante: false },
              ],
            })
          }
        >
          Agregar hallazgo
        </Button>
      </fieldset>

      <fieldset>
        <legend>Filtro comercial (confirma cada punto con la información real)</legend>
        {COMMERCIAL_CHECKS.map((c, i) => (
          <label key={c} style={{ display: 'block' }}>
            <input
              type="checkbox"
              checked={draft.commercial[i] ?? false}
              onChange={(e) =>
                set({
                  commercial: draft.commercial.map((v, j) => (j === i ? e.target.checked : v)),
                })
              }
            />{' '}
            {c}
          </label>
        ))}
      </fieldset>

      <fieldset>
        <legend>Decisión de los filtros</legend>
        <div className="field">
          <label htmlFor="rev-cf">Filtro creativo</label>
          <select
            id="rev-cf"
            value={draft.creativeFilter}
            onChange={(e) => set({ creativeFilter: e.target.value as FilterState })}
          >
            {FILTER_STATES.map((s) => (
              <option key={s} value={s}>
                {FILTER_LABELS[s]}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="rev-mf">Filtro comercial</label>
          <select
            id="rev-mf"
            value={draft.commercialFilter}
            onChange={(e) => set({ commercialFilter: e.target.value as FilterState })}
          >
            {FILTER_STATES.map((s) => (
              <option key={s} value={s}>
                {FILTER_LABELS[s]}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="rev-who">Quién revisa (opcional)</label>
          <input
            id="rev-who"
            maxLength={60}
            value={draft.reviewer}
            onChange={(e) => set({ reviewer: e.target.value })}
          />
        </div>
      </fieldset>

      <fieldset>
        <legend>Flujo: Creación → Validación → Aprobación</legend>
        <div className="field">
          <label htmlFor="rev-stage">Etapa</label>
          <select
            id="rev-stage"
            value={draft.stage}
            onChange={(e) => set({ stage: e.target.value as ReviewStage })}
          >
            {STAGES.map((s) => (
              <option key={s} value={s}>
                {STAGE_LABELS[s]}
              </option>
            ))}
          </select>
        </div>
        <div className="field">
          <label htmlFor="rev-final">Aprobación final</label>
          <select
            id="rev-final"
            value={draft.finalApproval}
            onChange={(e) => set({ finalApproval: e.target.value as FinalApproval })}
          >
            {FINAL_STATES.map((s) => (
              <option key={s} value={s}>
                {FINAL_LABELS[s]}
              </option>
            ))}
          </select>
          <p className="field-hint">
            Solo se puede liberar si la revisión es publicable y escribes quién aprueba.
          </p>
        </div>
        <div className="field">
          <label htmlFor="rev-approver">Quién aprueba</label>
          <input
            id="rev-approver"
            maxLength={60}
            value={draft.approver}
            onChange={(e) => set({ approver: e.target.value })}
          />
        </div>
      </fieldset>

      <div role="status" aria-live="polite" aria-label="Resumen de la revisión">
        <p>
          <strong>
            {live.score === null ? 'Sin puntaje' : `${String(live.score)} de 100`} · {live.band} ·{' '}
            {VERDICT_LABELS[live.verdict]}
          </strong>
        </p>
        <p>
          {live.publishable ? 'Lista para publicar según esta revisión.' : 'No publicable todavía.'}
        </p>
        {live.reasons.length > 0 && (
          <ul>
            {live.reasons.map((r) => (
              <li key={r}>{r}</li>
            ))}
          </ul>
        )}
      </div>
      <div className="form-actions">
        <Button variant="primary" type="submit">
          Guardar revisión
        </Button>
      </div>
      {saved && (
        <p className="field-hint">Última modificación: {formatLocalDateTime(saved.updatedAt)}.</p>
      )}
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
    </form>
  );
}

const VERDICT_TEXT: Readonly<Record<string, string>> = {
  apto: 'apto',
  revisar: 'revisar',
  no_apto: 'no apto',
};

/** Última auditoría automática del copy o pieza elegido (solo lectura). */
function autoAlert(
  target: string,
  audits: readonly AuditRecord[],
  pieces: readonly PieceRecord[],
): string | null {
  const [type, id] = target.split(':');
  if (type === 'copy') {
    const a = audits.find((x) => x.copyId === id);
    return a
      ? `última auditoría de reglas ${String(a.score)}/100 (${VERDICT_TEXT[a.verdict] ?? a.verdict}).`
      : null;
  }
  const a = pieces.find((p) => p.id === id)?.audits[0];
  return a
    ? `última auditoría de reglas ${String(a.score)}/100 (${VERDICT_TEXT[a.verdict] ?? a.verdict}).`
    : null;
}
