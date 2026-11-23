import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { CHANNELS, type Channel } from '@/domain/brief';
import { SEVERITY_LABELS, type BrandTerm, type Legend, type Severity } from '@/domain/copyRules';
import {
  LEGEND_TEXT_MAX,
  SEVERITIES,
  TERM_SUGGESTION_MAX,
  TERM_TEXT_MAX,
  type RulesDoc,
} from '@/domain/rulesConfig';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import type { AppError } from '@/services/contracts';

const messageOf = (e: AppError): string =>
  e.code === 'validation_error' ? e.message : describeError(e);

type Editing =
  | { readonly kind: 'legend'; readonly index: number | null }
  | { readonly kind: 'term'; readonly index: number | null }
  | null;

/** Leyendas y términos de marca configurables (S2.5b). Cada cambio se guarda al instante en este navegador. */
export function RulesPage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const [version, setVersion] = useState(0);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<Editing>(null);
  const [confirm, setConfirm] = useState<string | null>(null);
  const [focusTick, setFocusTick] = useState(0);
  useEffect(() => {
    if (focusTick > 0) heading.current?.focus();
  }, [focusTick]);
  const load = useCallback(async () => {
    void version;
    return services.rules.get();
  }, [services, version]);
  const { state, retry } = useAsyncResource(load);

  const persist = async (next: RulesDoc, message: string): Promise<boolean> => {
    setError(null);
    const r = await services.rules.save(next);
    if (!r.ok) {
      setError(messageOf(r.error));
      return false;
    }
    setNotice(message);
    setEditing(null);
    setConfirm(null);
    setVersion((n) => n + 1);
    setFocusTick((n) => n + 1);
    return true;
  };

  const reset = async () => {
    const r = await services.rules.resetToTemplate();
    if (!r.ok) {
      setError(messageOf(r.error));
      return;
    }
    setNotice('Se restauró la plantilla de ejemplo.');
    setConfirm(null);
    setEditing(null);
    setVersion((n) => n + 1);
    setFocusTick((n) => n + 1);
  };

  return (
    <section aria-labelledby="titulo-reglas">
      <h2 id="titulo-reglas" tabIndex={-1} ref={heading}>
        Reglas
      </h2>
      <p role="status" aria-live="polite">
        {notice}
      </p>
      {error && <p role="alert">{error}</p>}
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {state.status === 'success' && (
        <>
          {state.data.isTemplate && (
            <p>
              Estás viendo la plantilla de ejemplo (sin leyendas y con términos de ejemplo no
              validados). Lo primero que guardes aquí la reemplaza.
            </p>
          )}
          <Card title="Leyendas" headingLevel={3}>
            <p>
              Una leyenda obligatoria y activa debe aparecer en el copy de los canales que elijas
              (sin canales = todos). Si falta, la revisión la marca como crítica. El permiso o aviso
              de publicidad no se revisa.
            </p>
            {editing?.kind === 'legend' ? (
              <LegendForm
                initial={editing.index === null ? undefined : state.data.doc.legends[editing.index]}
                onCancel={() => {
                  setEditing(null);
                  setError(null);
                }}
                onSubmit={(l) =>
                  persist(
                    {
                      ...state.data.doc,
                      legends:
                        editing.index === null
                          ? [...state.data.doc.legends, l]
                          : state.data.doc.legends.map((x, i) => (i === editing.index ? l : x)),
                    },
                    editing.index === null ? 'Leyenda agregada.' : 'Leyenda actualizada.',
                  )
                }
              />
            ) : (
              <div className="form-actions">
                <Button
                  variant="primary"
                  onClick={() => setEditing({ kind: 'legend', index: null })}
                >
                  Nueva leyenda
                </Button>
              </div>
            )}
            {state.data.doc.legends.length === 0 ? (
              <p>Aún no hay leyendas.</p>
            ) : (
              <ul className="plain-list" aria-label="Leyendas">
                {state.data.doc.legends.map((l, i) => (
                  <li key={l.text}>
                    <p>
                      <strong>{l.text}</strong>
                    </p>
                    <p>
                      {l.channels.length === 0 ? 'Todos los canales' : l.channels.join(', ')} ·{' '}
                      {l.required ? 'Obligatoria' : 'Opcional'} · {l.active ? 'Activa' : 'Inactiva'}
                    </p>
                    {confirm === `l${i}` ? (
                      <div
                        role="group"
                        aria-label={`Confirmar eliminación de la leyenda ${l.text}`}
                      >
                        <p>¿Eliminar esta leyenda? No se puede deshacer.</p>
                        <div className="form-actions">
                          <Button
                            variant="primary"
                            onClick={() =>
                              void persist(
                                {
                                  ...state.data.doc,
                                  legends: state.data.doc.legends.filter((_, j) => j !== i),
                                },
                                'Leyenda eliminada.',
                              )
                            }
                          >
                            Sí, eliminar leyenda
                          </Button>
                          <Button onClick={() => setConfirm(null)}>Cancelar</Button>
                        </div>
                      </div>
                    ) : (
                      <div className="form-actions">
                        <Button
                          onClick={() => setEditing({ kind: 'legend', index: i })}
                          aria-label={`Editar leyenda ${l.text}`}
                        >
                          Editar
                        </Button>
                        <Button
                          onClick={() =>
                            void persist(
                              {
                                ...state.data.doc,
                                legends: state.data.doc.legends.map((x, j) =>
                                  j === i ? { ...x, active: !x.active } : x,
                                ),
                              },
                              l.active ? 'Leyenda desactivada.' : 'Leyenda activada.',
                            )
                          }
                          aria-label={`${l.active ? 'Desactivar' : 'Activar'} leyenda ${l.text}`}
                        >
                          {l.active ? 'Desactivar' : 'Activar'}
                        </Button>
                        <Button
                          onClick={() => setConfirm(`l${i}`)}
                          aria-label={`Eliminar leyenda ${l.text}`}
                        >
                          Eliminar
                        </Button>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </Card>

          <Card title="Términos de marca" headingLevel={3}>
            <p>
              Un término prohibido se busca por palabra completa, sin distinguir mayúsculas ni
              acentos. La sugerencia solo se muestra: nunca se reescribe el copy.
            </p>
            {editing?.kind === 'term' ? (
              <TermForm
                initial={
                  editing.index === null ? undefined : state.data.doc.brandTerms[editing.index]
                }
                onCancel={() => {
                  setEditing(null);
                  setError(null);
                }}
                onSubmit={(t) =>
                  persist(
                    {
                      ...state.data.doc,
                      brandTerms:
                        editing.index === null
                          ? [...state.data.doc.brandTerms, t]
                          : state.data.doc.brandTerms.map((x, i) => (i === editing.index ? t : x)),
                    },
                    editing.index === null ? 'Término agregado.' : 'Término actualizado.',
                  )
                }
              />
            ) : (
              <div className="form-actions">
                <Button variant="primary" onClick={() => setEditing({ kind: 'term', index: null })}>
                  Nuevo término
                </Button>
              </div>
            )}
            {state.data.doc.brandTerms.length === 0 ? (
              <p>Aún no hay términos.</p>
            ) : (
              <ul className="plain-list" aria-label="Términos de marca">
                {state.data.doc.brandTerms.map((t, i) => (
                  <li key={`${t.kind}-${t.text}`}>
                    <p>
                      <strong>{t.text}</strong> ·{' '}
                      {t.kind === 'prohibido' ? 'Prohibido' : 'Preferido'}
                      {t.kind === 'prohibido' ? ` · ${SEVERITY_LABELS[t.severity]}` : ''}
                      {t.suggestion ? ` · Sugerencia: ${t.suggestion}` : ''}
                    </p>
                    {confirm === `t${i}` ? (
                      <div role="group" aria-label={`Confirmar eliminación del término ${t.text}`}>
                        <p>¿Eliminar este término? No se puede deshacer.</p>
                        <div className="form-actions">
                          <Button
                            variant="primary"
                            onClick={() =>
                              void persist(
                                {
                                  ...state.data.doc,
                                  brandTerms: state.data.doc.brandTerms.filter((_, j) => j !== i),
                                },
                                'Término eliminado.',
                              )
                            }
                          >
                            Sí, eliminar término
                          </Button>
                          <Button onClick={() => setConfirm(null)}>Cancelar</Button>
                        </div>
                      </div>
                    ) : (
                      <div className="form-actions">
                        <Button
                          onClick={() => setEditing({ kind: 'term', index: i })}
                          aria-label={`Editar término ${t.text}`}
                        >
                          Editar
                        </Button>
                        <Button
                          onClick={() => setConfirm(`t${i}`)}
                          aria-label={`Eliminar término ${t.text}`}
                        >
                          Eliminar
                        </Button>
                      </div>
                    )}
                  </li>
                ))}
              </ul>
            )}
          </Card>

          {confirm === 'reset' ? (
            <div role="group" aria-label="Confirmar restauración de la plantilla">
              <p>
                ¿Restaurar la plantilla de ejemplo? Se pierden las leyendas y términos que
                capturaste.
              </p>
              <div className="form-actions">
                <Button variant="primary" onClick={() => void reset()}>
                  Sí, restaurar plantilla
                </Button>
                <Button onClick={() => setConfirm(null)}>Cancelar</Button>
              </div>
            </div>
          ) : (
            <div className="form-actions">
              <Button onClick={() => setConfirm('reset')}>Restaurar plantilla de ejemplo</Button>
            </div>
          )}
        </>
      )}
    </section>
  );
}

function LegendForm({
  initial,
  onSubmit,
  onCancel,
}: {
  readonly initial: Legend | undefined;
  readonly onSubmit: (l: Legend) => Promise<boolean>;
  readonly onCancel: () => void;
}) {
  const [text, setText] = useState(initial?.text ?? '');
  const [channels, setChannels] = useState<readonly Channel[]>(initial?.channels ?? []);
  const [required, setRequired] = useState(initial?.required ?? true);
  const [active, setActive] = useState(initial?.active ?? true);
  const submit = (e: FormEvent) => {
    e.preventDefault();
    void onSubmit({ text, channels, required, active });
  };
  return (
    <form onSubmit={submit} noValidate aria-label="Formulario de leyenda">
      <div className="field">
        <label htmlFor="leyenda-texto">Texto de la leyenda (obligatorio)</label>
        <textarea
          id="leyenda-texto"
          rows={3}
          value={text}
          maxLength={LEGEND_TEXT_MAX}
          onChange={(e) => setText(e.target.value)}
        />
      </div>
      <fieldset>
        <legend>Canales (sin marcar = todos)</legend>
        {CHANNELS.map((c) => (
          <label key={c} style={{ display: 'block' }}>
            <input
              type="checkbox"
              checked={channels.includes(c)}
              onChange={(e) =>
                setChannels((cur) => (e.target.checked ? [...cur, c] : cur.filter((x) => x !== c)))
              }
            />{' '}
            {c}
          </label>
        ))}
      </fieldset>
      <label style={{ display: 'block' }}>
        <input type="checkbox" checked={required} onChange={(e) => setRequired(e.target.checked)} />{' '}
        Obligatoria
      </label>
      <label style={{ display: 'block' }}>
        <input type="checkbox" checked={active} onChange={(e) => setActive(e.target.checked)} />{' '}
        Activa
      </label>
      <div className="form-actions">
        <Button type="submit" variant="primary">
          {initial ? 'Guardar leyenda' : 'Agregar leyenda'}
        </Button>
        <Button onClick={onCancel}>Cancelar</Button>
      </div>
    </form>
  );
}

function TermForm({
  initial,
  onSubmit,
  onCancel,
}: {
  readonly initial: BrandTerm | undefined;
  readonly onSubmit: (t: BrandTerm) => Promise<boolean>;
  readonly onCancel: () => void;
}) {
  const [text, setText] = useState(initial?.text ?? '');
  const [kind, setKind] = useState<BrandTerm['kind']>(initial?.kind ?? 'prohibido');
  const [severity, setSeverity] = useState<Severity>(initial?.severity ?? 'mayor');
  const [suggestion, setSuggestion] = useState(initial?.suggestion ?? '');
  const submit = (e: FormEvent) => {
    e.preventDefault();
    void onSubmit({ text, kind, severity, ...(suggestion.trim() ? { suggestion } : {}) });
  };
  return (
    <form onSubmit={submit} noValidate aria-label="Formulario de término">
      <div className="field">
        <label htmlFor="termino-texto">Término (obligatorio)</label>
        <input
          id="termino-texto"
          type="text"
          autoComplete="off"
          value={text}
          maxLength={TERM_TEXT_MAX}
          onChange={(e) => setText(e.target.value)}
        />
      </div>
      <div className="field">
        <label htmlFor="termino-tipo">Tipo</label>
        <select
          id="termino-tipo"
          value={kind}
          onChange={(e) => setKind(e.target.value as BrandTerm['kind'])}
        >
          <option value="prohibido">Prohibido</option>
          <option value="preferido">Preferido</option>
        </select>
      </div>
      <div className="field">
        <label htmlFor="termino-severidad">Severidad (si es prohibido)</label>
        <select
          id="termino-severidad"
          value={severity}
          onChange={(e) => setSeverity(e.target.value as Severity)}
        >
          {SEVERITIES.map((s) => (
            <option key={s} value={s}>
              {SEVERITY_LABELS[s]}
            </option>
          ))}
        </select>
      </div>
      <div className="field">
        <label htmlFor="termino-sugerencia">Sugerencia (opcional)</label>
        <input
          id="termino-sugerencia"
          type="text"
          autoComplete="off"
          value={suggestion}
          maxLength={TERM_SUGGESTION_MAX}
          onChange={(e) => setSuggestion(e.target.value)}
        />
      </div>
      <div className="form-actions">
        <Button type="submit" variant="primary">
          {initial ? 'Guardar término' : 'Agregar término'}
        </Button>
        <Button onClick={onCancel}>Cancelar</Button>
      </div>
    </form>
  );
}
