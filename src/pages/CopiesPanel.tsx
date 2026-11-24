import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import type { AppError } from '@/services/contracts';
import type { BriefRecord } from '@/domain/briefRecord';
import {
  COPY_FIELDS,
  COPY_FIELD_LABELS,
  COPY_LIMITS,
  COPY_MAX_TAGS,
  COPY_TAG_MAX,
  currentVersion,
  type CopyContent,
  type CopyVariant,
  diffContent,
  validateCopyContent,
  validateLabel,
  validateTags,
  type CopyField,
  type CopyRecord,
} from '@/domain/copy';
import { TEMPLATES, applyTemplate, type TemplateId } from '@/domain/copyTemplates';
import { toRulesConfig } from '@/domain/rulesConfig';
import {
  CATEGORY_LABELS,
  SEVERITY_LABELS,
  evaluateCopy,
  type Evaluation,
} from '@/domain/copyRules';
import { AdaptationsSection } from '@/pages/AdaptationsSection';
import { matchesCopy } from '@/domain/copySearch';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import { formatLocalDateTime } from '@/lib/formatDate';

type View =
  { kind: 'list' } | { kind: 'form'; copy?: CopyRecord } | { kind: 'history'; copy: CopyRecord };

const messageOf = (e: AppError): string =>
  e.code === 'validation_error' || e.code === 'conflict' ? e.message : describeError(e);

const LONG_FIELDS: ReadonlySet<CopyField> = new Set(['body', 'description']);
const splitTags = (text: string): string[] => text.split(',');

/** Copys de un brief: variantes con historial de versiones inmutables (AC2-04, AC2-07). */
export function CopiesPanel({
  brief,
  title,
  onBack,
}: {
  readonly brief: BriefRecord;
  readonly title: string;
  readonly onBack: () => void;
}) {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const [view, setView] = useState<View>({ kind: 'list' });
  const [version, setVersion] = useState(0);
  const [notice, setNotice] = useState('');
  const [query, setQuery] = useState('');
  const [focusTick, setFocusTick] = useState(0);
  useEffect(() => {
    if (focusTick > 0) heading.current?.focus();
  }, [focusTick]);
  const load = useCallback(async () => {
    void version;
    return services.copies.list(brief.id);
  }, [services, brief.id, version]);
  const { state, retry } = useAsyncResource(load);
  const done = (message: string) => {
    setView({ kind: 'list' });
    setNotice(message);
    setVersion((n) => n + 1);
    setFocusTick((n) => n + 1);
  };

  return (
    <section aria-labelledby="titulo-copys">
      <h3 id="titulo-copys" tabIndex={-1} ref={heading}>
        Copys de {title}
      </h3>
      <p role="status" aria-live="polite">
        {notice}
      </p>
      {view.kind === 'form' ? (
        <CopyForm
          briefId={brief.id}
          briefFields={brief.fields}
          copy={view.copy}
          onDone={done}
          onCancel={() => done('')}
        />
      ) : view.kind === 'history' ? (
        <History copy={view.copy} onDone={done} onClose={() => done('')} />
      ) : (
        <>
          <div className="form-actions">
            <Button
              variant="primary"
              onClick={() => {
                setNotice('');
                setView({ kind: 'form' });
              }}
            >
              Nuevo copy
            </Button>
            <Button onClick={onBack}>Volver a los briefs</Button>
          </div>
          <AsyncStatus status={state.status} />
          {state.status === 'error' && (
            <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
          )}
          {state.status === 'success' && state.data.length > 1 && (
            <div className="field">
              <label htmlFor="copys-buscar">Buscar copys (nombre, etiqueta o texto)</label>
              <input
                id="copys-buscar"
                type="search"
                autoComplete="off"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
              <p role="status" aria-live="polite" className="field-hint">
                {query.trim() === ''
                  ? ''
                  : `${state.data.filter((c) => matchesCopy(c, query)).length} de ${state.data.length} copys coinciden.`}
              </p>
            </div>
          )}
          {state.status === 'success' &&
            (state.data.length === 0 ? (
              <EmptyState
                title="Este brief aún no tiene copys"
                description="Crea el primero con «Nuevo copy». Cada cambio que guardes queda como una versión."
                headingLevel={4}
              />
            ) : (
              <ul className="plain-list" aria-label="Copys del brief">
                {state.data
                  .filter((c) => matchesCopy(c, query))
                  .map((c) => (
                    <CopyItem
                      key={c.id}
                      copy={c}
                      brief={brief}
                      onEdit={() => {
                        setNotice('');
                        setView({ kind: 'form', copy: c });
                      }}
                      onHistory={() => {
                        setNotice('');
                        setView({ kind: 'history', copy: c });
                      }}
                      onDone={done}
                    />
                  ))}
              </ul>
            ))}
        </>
      )}
    </section>
  );
}

function CopyItem({
  copy,
  brief,
  onEdit,
  onHistory,
  onDone,
}: {
  readonly copy: CopyRecord;
  readonly brief: BriefRecord;
  readonly onEdit: () => void;
  readonly onHistory: () => void;
  readonly onDone: (message: string) => void;
}) {
  const services = useServices();
  const [mode, setMode] = useState<'none' | 'delete' | 'variant'>('none');
  const [variantEdit, setVariantEdit] = useState<CopyVariant | 'new' | null>(null);
  const [delVariant, setDelVariant] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [review, setReview] = useState<{
    evaluation: Evaluation;
    isTemplate: boolean;
    name: string;
  } | null>(null);
  const cur = currentVersion(copy);
  const runReview = async (content: CopyContent, name: string) => {
    const f = brief.fields;
    if (!f.channel) {
      setError('El brief no tiene canal: elige uno para revisar las reglas.');
      return;
    }
    const cfg = await services.rules.get();
    if (!cfg.ok) {
      setError(describeError(cfg.error));
      return;
    }
    setError(null);
    setReview({
      evaluation: evaluateCopy(
        { channel: f.channel, offer: f.offer },
        content,
        toRulesConfig(cfg.value.doc),
      ),
      isTemplate: cfg.value.isTemplate,
      name,
    });
  };
  const remove = async () => {
    const r = await services.copies.remove(copy.id);
    if (!r.ok) {
      setError(messageOf(r.error));
      setMode('none');
      return;
    }
    onDone('Copy eliminado.');
  };
  const removeVariantNow = async (variantId: string) => {
    const r = await services.copies.removeVariant({ id: copy.id, variantId });
    if (!r.ok) {
      setError(messageOf(r.error));
      setDelVariant(null);
      return;
    }
    onDone('Variante eliminada.');
  };
  return (
    <li>
      <Card title={copy.label} headingLevel={4}>
        <p>
          Versión {cur.n} de {copy.versions.length} · {formatLocalDateTime(copy.updatedAt)}
          {copy.tags.length > 0 ? ` · Etiquetas: ${copy.tags.join(', ')}` : ''}
        </p>
        <ContentView content={cur.content} />
        {error && <p role="alert">{error}</p>}
        {mode === 'delete' ? (
          <div role="group" aria-label={`Confirmar eliminación de ${copy.label}`}>
            <p>¿Eliminar este copy y todo su historial? No se puede deshacer.</p>
            <div className="form-actions">
              <Button variant="primary" onClick={() => void remove()}>
                Sí, eliminar copy
              </Button>
              <Button onClick={() => setMode('none')}>Cancelar</Button>
            </div>
          </div>
        ) : mode === 'variant' && variantEdit !== null ? (
          <VariantForm
            copyId={copy.id}
            initial={variantEdit === 'new' ? undefined : variantEdit}
            onDone={onDone}
            onCancel={() => {
              setMode('none');
              setVariantEdit(null);
              setError(null);
            }}
          />
        ) : (
          <div className="form-actions">
            <Button onClick={onEdit} aria-label={`Editar ${copy.label}`}>
              Editar
            </Button>
            <Button
              onClick={() => void runReview(cur.content, copy.label)}
              aria-label={`Revisar reglas de ${copy.label}`}
            >
              Revisar reglas
            </Button>
            <Button onClick={onHistory} aria-label={`Historial de ${copy.label}`}>
              Historial
            </Button>
            <Button
              onClick={() => {
                setError(null);
                setVariantEdit('new');
                setMode('variant');
              }}
              aria-label={`Agregar variante a ${copy.label}`}
            >
              Agregar variante
            </Button>
            <Button
              onClick={() => {
                setError(null);
                setMode('delete');
              }}
              aria-label={`Eliminar ${copy.label}`}
            >
              Eliminar
            </Button>
          </div>
        )}
        {(copy.variants ?? []).length > 0 && (
          <section aria-label={`Variantes de ${copy.label}`}>
            <h5>Variantes ({(copy.variants ?? []).length})</h5>
            <p className="field-hint">
              Alternativas de texto que conviven con el copy. No tienen versiones propias.
            </p>
            <ul className="plain-list">
              {(copy.variants ?? []).map((v) => (
                <li key={v.id}>
                  <p>
                    <strong>{v.label}</strong>
                  </p>
                  <ContentView content={v.content} />
                  {delVariant === v.id ? (
                    <div
                      role="group"
                      aria-label={`Confirmar eliminación de la variante ${v.label}`}
                    >
                      <p>¿Eliminar esta variante? No se puede deshacer.</p>
                      <div className="form-actions">
                        <Button variant="primary" onClick={() => void removeVariantNow(v.id)}>
                          Sí, eliminar variante
                        </Button>
                        <Button onClick={() => setDelVariant(null)}>Cancelar</Button>
                      </div>
                    </div>
                  ) : (
                    <div className="form-actions">
                      <Button
                        onClick={() => {
                          setError(null);
                          setVariantEdit(v);
                          setMode('variant');
                        }}
                        aria-label={`Editar variante ${v.label}`}
                      >
                        Editar
                      </Button>
                      <Button
                        onClick={() => void runReview(v.content, `${copy.label} · ${v.label}`)}
                        aria-label={`Revisar reglas de la variante ${v.label}`}
                      >
                        Revisar reglas
                      </Button>
                      <Button
                        onClick={() => setDelVariant(v.id)}
                        aria-label={`Eliminar variante ${v.label}`}
                      >
                        Eliminar
                      </Button>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          </section>
        )}
        <AdaptationsSection copy={copy} briefChannel={brief.fields.channel} onChanged={onDone} />
        {review && (
          <ReviewView
            review={review.evaluation}
            isTemplate={review.isTemplate}
            onClose={() => setReview(null)}
            label={review.name}
          />
        )}
      </Card>
    </li>
  );
}

const VERDICT_LABELS = { apto: 'Apto', revisar: 'Revisar', no_apto: 'No apto' } as const;

function ReviewView({
  review,
  isTemplate,
  label,
  onClose,
}: {
  readonly review: Evaluation;
  readonly isTemplate: boolean;
  readonly label: string;
  readonly onClose: () => void;
}) {
  return (
    <div role="region" aria-label={`Revisión de ${label}`}>
      <p>
        <strong>
          Puntaje {review.score} de 100 · {VERDICT_LABELS[review.verdict]}
        </strong>
        {review.blocked ? ' · Hay hallazgos críticos: bloquean la aprobación.' : ''}
      </p>
      {review.findings.length === 0 ? (
        <p>Sin hallazgos con las reglas actuales.</p>
      ) : (
        <ul>
          {review.findings.map((f, i) => (
            <li key={`${f.ruleId}-${i}`}>
              {SEVERITY_LABELS[f.severity]} · {CATEGORY_LABELS[f.category]}: {f.message}
            </li>
          ))}
        </ul>
      )}
      <p className="field-hint">
        Reglas orientativas: las longitudes por canal no están verificadas contra las plataformas y
        no se revisa ortografía.{' '}
        {isTemplate
          ? 'Usas la plantilla de ejemplo: aún no hay leyendas y los términos de marca son ejemplos sin validar. Captúralos en «Reglas».'
          : 'Se usaron las leyendas y términos que capturaste en «Reglas».'}
      </p>
      <Button onClick={onClose}>Cerrar revisión</Button>
    </div>
  );
}

function VariantForm({
  copyId,
  initial,
  onDone,
  onCancel,
}: {
  readonly copyId: string;
  readonly initial: CopyVariant | undefined;
  readonly onDone: (message: string) => void;
  readonly onCancel: () => void;
}) {
  const services = useServices();
  const [label, setLabel] = useState(initial?.label ?? '');
  const [values, setValues] = useState<Record<CopyField, string>>({
    headline: initial?.content.headline ?? '',
    body: initial?.content.body ?? '',
    description: initial?.content.description ?? '',
    cta: initial?.content.cta ?? '',
  });
  const [error, setError] = useState<string | null>(null);
  const submit = async (ev: FormEvent) => {
    ev.preventDefault();
    setError(null);
    const content = Object.fromEntries(COPY_FIELDS.map((f) => [f, values[f]]));
    const r = initial
      ? await services.copies.updateVariant({ id: copyId, variantId: initial.id, label, content })
      : await services.copies.addVariant({ id: copyId, label, content });
    if (!r.ok) {
      setError(messageOf(r.error));
      return;
    }
    onDone(initial ? 'Variante actualizada.' : `Variante «${label.trim()}» agregada.`);
  };
  return (
    <form onSubmit={(e) => void submit(e)} noValidate aria-label="Formulario de variante">
      <div className="field">
        <label htmlFor="variante-nombre">Nombre de la variante (obligatorio)</label>
        <input
          id="variante-nombre"
          type="text"
          autoComplete="off"
          value={label}
          onChange={(e) => setLabel(e.target.value)}
        />
      </div>
      {COPY_FIELDS.map((f) => (
        <div className="field" key={f}>
          <label htmlFor={`variante-${f}`}>{COPY_FIELD_LABELS[f]} (opcional)</label>
          {LONG_FIELDS.has(f) ? (
            <textarea
              id={`variante-${f}`}
              rows={3}
              value={values[f]}
              onChange={(e) => setValues((v) => ({ ...v, [f]: e.target.value }))}
            />
          ) : (
            <input
              id={`variante-${f}`}
              type="text"
              autoComplete="off"
              value={values[f]}
              onChange={(e) => setValues((v) => ({ ...v, [f]: e.target.value }))}
            />
          )}
        </div>
      ))}
      {error && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
      <div className="form-actions">
        <Button type="submit" variant="primary">
          {initial ? 'Guardar variante' : 'Agregar variante'}
        </Button>
        <Button onClick={onCancel}>Cancelar</Button>
      </div>
    </form>
  );
}

function ContentView({ content }: { readonly content: Partial<Record<CopyField, string>> }) {
  return (
    <dl>
      {COPY_FIELDS.filter((f) => content[f] !== undefined).map((f) => (
        <div key={f}>
          <dt>{COPY_FIELD_LABELS[f]}</dt>
          <dd style={{ whiteSpace: 'pre-wrap' }}>{content[f]}</dd>
        </div>
      ))}
    </dl>
  );
}

function History({
  copy,
  onDone,
  onClose,
}: {
  readonly copy: CopyRecord;
  readonly onDone: (message: string) => void;
  readonly onClose: () => void;
}) {
  const services = useServices();
  const [error, setError] = useState<string | null>(null);
  const current = currentVersion(copy);
  const versions = [...copy.versions].reverse();
  const restore = async (n: number) => {
    const r = await services.copies.restoreVersion({ id: copy.id, version: n });
    if (!r.ok) {
      setError(describeError(r.error));
      return;
    }
    onDone(`Se recuperó la versión ${n} como versión ${r.value.versions.length}.`);
  };
  return (
    <Card title={`Historial de ${copy.label}`} headingLevel={4}>
      <p>
        Las versiones no se modifican: recuperar una crea una versión nueva y conserva todo el
        historial.
      </p>
      {error && <p role="alert">{error}</p>}
      <ol className="plain-list" aria-label="Versiones">
        {versions.map((v) => {
          const prev = copy.versions[v.n - 2];
          const changes = prev ? diffContent(prev.content, v.content) : [];
          return (
            <li key={v.n}>
              <h5>
                Versión {v.n}
                {v.n === current.n ? ' (vigente)' : ''}
              </h5>
              <p>
                {formatLocalDateTime(v.createdAt)}
                {v.restoredFrom !== undefined
                  ? ` · recuperada de la versión ${v.restoredFrom}`
                  : ''}
              </p>
              <ContentView content={v.content} />
              {prev && changes.length > 0 && (
                <p>
                  Cambios respecto de la versión {prev.n}:{' '}
                  {changes.map((c) => COPY_FIELD_LABELS[c.field]).join(', ')}.
                </p>
              )}
              {v.n !== current.n && (
                <Button onClick={() => void restore(v.n)} aria-label={`Recuperar versión ${v.n}`}>
                  Recuperar versión {v.n}
                </Button>
              )}
            </li>
          );
        })}
      </ol>
      <div className="form-actions">
        <Button onClick={onClose}>Cerrar historial</Button>
      </div>
    </Card>
  );
}

function CopyForm({
  briefId,
  briefFields,
  copy,
  onDone,
  onCancel,
}: {
  readonly briefId: string;
  readonly briefFields: BriefRecord['fields'];
  readonly copy: CopyRecord | undefined;
  readonly onDone: (message: string) => void;
  readonly onCancel: () => void;
}) {
  const services = useServices();
  const cur = copy ? currentVersion(copy).content : {};
  const [label, setLabel] = useState(copy?.label ?? 'Principal');
  const [tags, setTags] = useState(copy?.tags.join(', ') ?? '');
  const [values, setValues] = useState<Record<CopyField, string>>({
    headline: cur.headline ?? '',
    body: cur.body ?? '',
    description: cur.description ?? '',
    cta: cur.cta ?? '',
  });
  const [errors, setErrors] = useState<Record<string, string>>({});
  const [saveError, setSaveError] = useState<string | null>(null);
  const form = useRef<HTMLFormElement>(null);

  const validate = (): Record<string, string> => {
    const found: Record<string, string> = {};
    const l = validateLabel(label);
    if (!l.ok) found['label'] = l.reason;
    const t = validateTags(splitTags(tags));
    if (!t.ok) found['tags'] = t.reason;
    for (const f of COPY_FIELDS) {
      if (values[f].trim() === '') continue;
      const v = validateCopyContent({ [f]: values[f] });
      if (!v.ok) found[f] = v.reason;
    }
    if (COPY_FIELDS.every((f) => values[f].trim() === ''))
      found['headline'] = 'Escribe al menos un campo del copy.';
    return found;
  };
  const revalidate = (key: string, next: () => Record<string, string>) => {
    if (errors[key] !== undefined) setErrors(next());
  };

  const onSubmit = async (ev: FormEvent) => {
    ev.preventDefault();
    setSaveError(null);
    const found = validate();
    setErrors(found);
    const first = ['label', ...COPY_FIELDS, 'tags'].find((k) => found[k] !== undefined);
    if (first !== undefined) {
      form.current?.querySelector<HTMLElement>(`[data-field="${first}"]`)?.focus();
      return;
    }
    const content = Object.fromEntries(COPY_FIELDS.map((f) => [f, values[f]]));
    const tagList = splitTags(tags);
    if (!copy) {
      const r = await services.copies.create({ briefId, label, content, tags: tagList });
      if (!r.ok) return setSaveError(describeError(r.error));
      return onDone(`Copy «${r.value.label}» creado (versión 1).`);
    }
    const changed = diffContent(
      cur,
      validateCopyContent(content).ok
        ? (validateCopyContent(content) as { ok: true; value: typeof cur }).value
        : cur,
    );
    const l = validateLabel(label);
    const t = validateTags(tagList);
    const metaChanged =
      (l.ok && l.value !== copy.label) ||
      (t.ok && t.value.join('\u0000') !== copy.tags.join('\u0000'));
    if (changed.length === 0 && !metaChanged) return onDone('No había cambios que guardar.');
    let message = '';
    if (changed.length > 0) {
      const r = await services.copies.saveVersion({ id: copy.id, content });
      if (!r.ok) return setSaveError(describeError(r.error));
      message = `Se guardó la versión ${r.value.versions.length}.`;
    }
    if (metaChanged) {
      const r = await services.copies.updateMeta({ id: copy.id, label, tags: tagList });
      if (!r.ok) return setSaveError(describeError(r.error));
      message = `${message} Nombre y etiquetas actualizados.`.trim();
    }
    onDone(message);
  };

  const err = (k: string) =>
    errors[k] ? (
      <p id={`copy-${k}-error`} className="field-error" role="alert">
        {errors[k]}
      </p>
    ) : null;
  const desc = (k: string) => (errors[k] ? `copy-${k}-ayuda copy-${k}-error` : `copy-${k}-ayuda`);

  return (
    <Card title={copy ? `Editar ${copy.label}` : 'Nuevo copy'} headingLevel={4}>
      <form ref={form} onSubmit={(e) => void onSubmit(e)} noValidate>
        {!copy && (
          <div className="field">
            <label htmlFor="copy-plantilla">Empezar desde una plantilla (opcional)</label>
            <select
              id="copy-plantilla"
              defaultValue=""
              aria-describedby="copy-plantilla-ayuda"
              onChange={(e) => {
                const id = e.target.value as TemplateId | '';
                if (id === '') return;
                const c = applyTemplate(id, briefFields);
                setValues({
                  headline: c.headline ?? '',
                  body: c.body ?? '',
                  description: c.description ?? '',
                  cta: c.cta ?? '',
                });
                setErrors({});
              }}
            >
              <option value="">Sin plantilla</option>
              {TEMPLATES.map((t) => (
                <option key={t.id} value={t.id}>
                  {t.name}
                </option>
              ))}
            </select>
            <p id="copy-plantilla-ayuda" className="field-hint">
              Solo ordena datos de tu brief para el canal; no inventa nada. Reemplaza lo que ya
              escribiste y puedes editarlo todo.
            </p>
          </div>
        )}
        <div className="field">
          <label htmlFor="copy-label">Nombre de la variante (obligatorio)</label>
          <input
            id="copy-label"
            data-field="label"
            type="text"
            autoComplete="off"
            value={label}
            aria-describedby={desc('label')}
            aria-invalid={errors['label'] ? true : undefined}
            onChange={(e) => {
              setLabel(e.target.value);
              const v = validateLabel(e.target.value);
              revalidate('label', () => {
                const { label: _drop, ...rest } = errors;
                void _drop;
                return v.ok ? rest : { ...rest, label: v.reason };
              });
            }}
          />
          <p id="copy-label-ayuda" className="field-hint">
            Por ejemplo «Principal» o «B».
          </p>
          {err('label')}
        </div>
        {COPY_FIELDS.map((f) => (
          <div className="field" key={f}>
            <label htmlFor={`copy-${f}`}>{COPY_FIELD_LABELS[f]} (opcional)</label>
            {LONG_FIELDS.has(f) ? (
              <textarea
                id={`copy-${f}`}
                data-field={f}
                rows={3}
                value={values[f]}
                aria-describedby={desc(f)}
                aria-invalid={errors[f] ? true : undefined}
                onChange={(e) => setValues((v) => ({ ...v, [f]: e.target.value }))}
              />
            ) : (
              <input
                id={`copy-${f}`}
                data-field={f}
                type="text"
                autoComplete="off"
                value={values[f]}
                aria-describedby={desc(f)}
                aria-invalid={errors[f] ? true : undefined}
                onChange={(e) => setValues((v) => ({ ...v, [f]: e.target.value }))}
              />
            )}
            <p id={`copy-${f}-ayuda`} className="field-hint">
              Hasta {COPY_LIMITS[f]} caracteres. Escribe al menos un campo.
            </p>
            {err(f)}
          </div>
        ))}
        <div className="field">
          <label htmlFor="copy-tags">Etiquetas (opcional)</label>
          <input
            id="copy-tags"
            data-field="tags"
            type="text"
            autoComplete="off"
            value={tags}
            aria-describedby={desc('tags')}
            aria-invalid={errors['tags'] ? true : undefined}
            onChange={(e) => setTags(e.target.value)}
          />
          <p id="copy-tags-ayuda" className="field-hint">
            Separadas por comas. Hasta {COPY_MAX_TAGS}, de {COPY_TAG_MAX} caracteres como máximo.
          </p>
          {err('tags')}
        </div>
        {saveError && (
          <p className="field-error" role="alert">
            {saveError}
          </p>
        )}
        <div className="form-actions">
          <Button type="submit" variant="primary">
            {copy ? 'Guardar nueva versión' : 'Crear copy'}
          </Button>
          <Button onClick={onCancel}>Cancelar</Button>
        </div>
      </form>
    </Card>
  );
}
