import { useCallback, useState, type FormEvent } from 'react';
import { Button } from '@/components/Button';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import type { AdaptationRecord } from '@/domain/adaptation';
import { CHANNELS, type Channel } from '@/domain/brief';
import {
  COPY_FIELDS,
  COPY_FIELD_LABELS,
  currentVersion,
  type CopyContent,
  type CopyField,
  type CopyRecord,
} from '@/domain/copy';
import { CHANNEL_RULES } from '@/domain/copyRules';
import { CHANNEL_FIELDS } from '@/domain/copyTemplates';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import type { AppError } from '@/services/contracts';

const messageOf = (e: AppError): string =>
  e.code === 'validation_error' || e.code === 'conflict' ? e.message : describeError(e);
const LONG_FIELDS: ReadonlySet<CopyField> = new Set(['body', 'description']);

/** Campos del copy que el canal usa, con el texto del contenido actual (el usuario puede editarlos). */
function prefill(content: CopyContent, channel: Channel): Record<CopyField, string> {
  const out: Record<CopyField, string> = { headline: '', body: '', description: '', cta: '' };
  for (const f of CHANNEL_FIELDS[channel]) out[f] = content[f] ?? '';
  return out;
}

/**
 * Adaptaciones por canal de un copy (S2.8, función 7). Entidades derivadas con trazabilidad al copy y su versión.
 * Los límites del canal se muestran como información orientativa: la adaptación NO se audita, puntúa ni aprueba.
 */
export function AdaptationsSection({
  copy,
  briefChannel,
  onChanged,
}: {
  readonly copy: CopyRecord;
  readonly briefChannel: Channel | undefined;
  readonly onChanged: (message: string) => void;
}) {
  const services = useServices();
  const [version, setVersion] = useState(0);
  const [mode, setMode] = useState<'none' | 'new' | AdaptationRecord>('none');
  const [confirm, setConfirm] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const load = useCallback(async () => {
    void version;
    return services.adaptations.list(copy.id);
  }, [services, copy.id, version]);
  const { state, retry } = useAsyncResource(load);
  const finish = (message: string) => {
    setMode('none');
    setConfirm(null);
    setError(null);
    setVersion((n) => n + 1);
    onChanged(message);
  };
  const remove = async (id: string) => {
    const r = await services.adaptations.remove(id);
    if (!r.ok) {
      setError(messageOf(r.error));
      setConfirm(null);
      return;
    }
    finish('Adaptación eliminada.');
  };
  const list = state.status === 'success' ? state.data : [];
  return (
    <section aria-label={`Adaptaciones de ${copy.label}`}>
      <h5>Adaptaciones por canal ({list.length})</h5>
      <p className="field-hint">
        Versiones del copy ajustadas a otro canal. Quedan ligadas a este copy y no se revisan ni
        aprueban de forma automática.
      </p>
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {error && <p role="alert">{error}</p>}
      {mode !== 'none' ? (
        <AdaptationForm
          copy={copy}
          initial={mode === 'new' ? undefined : mode}
          startChannel={briefChannel}
          onDone={finish}
          onCancel={() => {
            setMode('none');
            setError(null);
          }}
        />
      ) : (
        <div className="form-actions">
          <Button
            onClick={() => {
              setError(null);
              setMode('new');
            }}
            aria-label={`Adaptar a otro canal ${copy.label}`}
          >
            Adaptar a otro canal
          </Button>
        </div>
      )}
      {list.length > 0 && (
        <ul className="plain-list">
          {list.map((a) => (
            <li key={a.id}>
              <p>
                <strong>{a.channel}</strong> · desde la versión {a.sourceVersion}
                {a.sourceVersion !== currentVersion(copy).n
                  ? ' (el copy ya tiene una versión más nueva)'
                  : ''}
              </p>
              <dl>
                {COPY_FIELDS.filter((f) => a.content[f] !== undefined).map((f) => (
                  <div key={f}>
                    <dt>{COPY_FIELD_LABELS[f]}</dt>
                    <dd style={{ whiteSpace: 'pre-wrap' }}>{a.content[f]}</dd>
                  </div>
                ))}
              </dl>
              {confirm === a.id ? (
                <div
                  role="group"
                  aria-label={`Confirmar eliminación de la adaptación a ${a.channel}`}
                >
                  <p>¿Eliminar esta adaptación? No se puede deshacer.</p>
                  <div className="form-actions">
                    <Button variant="primary" onClick={() => void remove(a.id)}>
                      Sí, eliminar adaptación
                    </Button>
                    <Button onClick={() => setConfirm(null)}>Cancelar</Button>
                  </div>
                </div>
              ) : (
                <div className="form-actions">
                  <Button
                    onClick={() => {
                      setError(null);
                      setMode(a);
                    }}
                    aria-label={`Editar adaptación a ${a.channel}`}
                  >
                    Editar
                  </Button>
                  <Button
                    onClick={() => setConfirm(a.id)}
                    aria-label={`Eliminar adaptación a ${a.channel}`}
                  >
                    Eliminar
                  </Button>
                </div>
              )}
            </li>
          ))}
        </ul>
      )}
    </section>
  );
}

function AdaptationForm({
  copy,
  initial,
  startChannel,
  onDone,
  onCancel,
}: {
  readonly copy: CopyRecord;
  readonly initial: AdaptationRecord | undefined;
  readonly startChannel: Channel | undefined;
  readonly onDone: (message: string) => void;
  readonly onCancel: () => void;
}) {
  const services = useServices();
  const source = currentVersion(copy);
  const first = CHANNELS.find((c) => c !== startChannel) ?? CHANNELS[0];
  const [channel, setChannel] = useState<Channel>(initial?.channel ?? first);
  const [dirty, setDirty] = useState(false);
  const [values, setValues] = useState<Record<CopyField, string>>(() =>
    initial
      ? {
          headline: initial.content.headline ?? '',
          body: initial.content.body ?? '',
          description: initial.content.description ?? '',
          cta: initial.content.cta ?? '',
        }
      : prefill(source.content, first),
  );
  const [error, setError] = useState<string | null>(null);
  const shown = COPY_FIELDS.filter(
    (f) => CHANNEL_FIELDS[channel].includes(f) || values[f].trim() !== '',
  );
  const limits = CHANNEL_RULES[channel].limits;
  const pickChannel = (c: Channel) => {
    setChannel(c);
    if (!dirty) setValues(prefill(source.content, c));
  };
  const submit = async (ev: FormEvent) => {
    ev.preventDefault();
    setError(null);
    const content = Object.fromEntries(COPY_FIELDS.map((f) => [f, values[f]]));
    const r = initial
      ? await services.adaptations.update({ id: initial.id, content })
      : await services.adaptations.create({
          copyId: copy.id,
          channel,
          content,
          sourceVersion: source.n,
        });
    if (!r.ok) {
      setError(messageOf(r.error));
      return;
    }
    onDone(initial ? 'Adaptación actualizada.' : `Adaptación a ${channel} guardada.`);
  };
  return (
    <form onSubmit={(e) => void submit(e)} noValidate aria-label="Formulario de adaptación">
      <div className="field">
        <label htmlFor="adaptacion-canal">Canal de destino</label>
        <select
          id="adaptacion-canal"
          value={channel}
          disabled={initial !== undefined}
          onChange={(e) => pickChannel(e.target.value as Channel)}
        >
          {CHANNELS.map((c) => (
            <option key={c} value={c}>
              {c}
            </option>
          ))}
        </select>
        <p className="field-hint">
          Parte de la versión {source.n} del copy. Se rellenan los campos que usa el canal; puedes
          editarlos.
        </p>
      </div>
      {shown.map((f) => {
        const limit = limits[f];
        const len = values[f].length;
        return (
          <div className="field" key={f}>
            <label htmlFor={`adaptacion-${f}`}>{COPY_FIELD_LABELS[f]} (opcional)</label>
            {LONG_FIELDS.has(f) ? (
              <textarea
                id={`adaptacion-${f}`}
                rows={3}
                value={values[f]}
                onChange={(e) => {
                  setDirty(true);
                  setValues((v) => ({ ...v, [f]: e.target.value }));
                }}
              />
            ) : (
              <input
                id={`adaptacion-${f}`}
                type="text"
                autoComplete="off"
                value={values[f]}
                onChange={(e) => {
                  setDirty(true);
                  setValues((v) => ({ ...v, [f]: e.target.value }));
                }}
              />
            )}
            {limit !== undefined && (
              <p className="field-hint">
                {len} de {limit} caracteres (límite orientativo de {channel}
                {len > limit ? '; lo excede' : ''}).
              </p>
            )}
          </div>
        );
      })}
      {error && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
      <div className="form-actions">
        <Button type="submit" variant="primary">
          {initial ? 'Guardar adaptación' : 'Guardar adaptación'}
        </Button>
        <Button onClick={onCancel}>Cancelar</Button>
      </div>
    </form>
  );
}
