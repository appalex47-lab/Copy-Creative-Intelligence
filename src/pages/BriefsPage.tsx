import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';
import { CopiesPanel } from './CopiesPanel';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import {
  BRIEF_FIELD_LABELS,
  BRIEF_LONG_MAX,
  BRIEF_SHORT_MAX,
  CHANNELS,
  REQUIRED_FIELDS,
  validateBriefText,
  validateChannel,
  validateValidity,
  type BriefField,
} from '@/domain/brief';
import { evaluateRecord, type BriefRecord } from '@/domain/briefRecord';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';

type FormValues = Record<BriefField, string> & { validityFrom: string; validityTo: string };

const TEXT_FIELDS: readonly BriefField[] = [
  'campaign',
  'objective',
  'product',
  'audience',
  'offer',
  'benefit',
  'conditions',
  'tone',
  'message',
  'format',
  'cta',
];
const LONG: ReadonlySet<BriefField> = new Set([
  'objective',
  'audience',
  'offer',
  'benefit',
  'conditions',
  'message',
]);
/** Orden de captura en el formulario. */
const ORDER: readonly BriefField[] = [
  'campaign',
  'objective',
  'product',
  'audience',
  'offer',
  'benefit',
  'validity',
  'conditions',
  'tone',
  'message',
  'channel',
  'format',
  'cta',
];

const emptyValues = (): FormValues => ({
  campaign: '',
  objective: '',
  product: '',
  audience: '',
  offer: '',
  benefit: '',
  validity: '',
  conditions: '',
  tone: '',
  message: '',
  channel: '',
  format: '',
  cta: '',
  validityFrom: '',
  validityTo: '',
});

function valuesOf(record?: BriefRecord): FormValues {
  const v = emptyValues();
  if (!record) return v;
  for (const f of TEXT_FIELDS) v[f] = (record.fields[f] as string | undefined) ?? '';
  v.channel = record.fields.channel ?? '';
  v.validityFrom = record.fields.validity?.from ?? '';
  v.validityTo = record.fields.validity?.to ?? '';
  return v;
}

function fieldsOf(v: FormValues): Record<string, unknown> {
  const out: Record<string, unknown> = { channel: v.channel };
  for (const f of TEXT_FIELDS) out[f] = v[f];
  out['validity'] = { from: v.validityFrom, to: v.validityTo };
  return out;
}

/** Error de un campo (null = sin error). Usa las mismas reglas del dominio que el guardado. */
function errorOf(field: BriefField, v: FormValues): string | null {
  if (field === 'channel') {
    const r = validateChannel(v.channel);
    return r.ok ? null : r.reason;
  }
  if (field === 'validity') {
    const r = validateValidity({ from: v.validityFrom, to: v.validityTo });
    return r.ok ? null : r.reason;
  }
  const r = validateBriefText(field, v[field]);
  return r.ok ? null : r.reason;
}

const titleOf = (r: BriefRecord): string => r.fields.campaign ?? 'Brief sin campaña';

/** Copy Studio: briefs (R-020). Un borrador incompleto se puede guardar, pero siempre se señala qué le falta. */
export function BriefsPage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const [version, setVersion] = useState(0);
  const [editing, setEditing] = useState<'new' | BriefRecord | null>(null);
  const [copying, setCopying] = useState<BriefRecord | null>(null);
  const [notice, setNotice] = useState('');
  const [focusTick, setFocusTick] = useState(0);
  // El foco vuelve al encabezado DESPUÉS de que el formulario desaparece del documento.
  useEffect(() => {
    if (focusTick > 0) heading.current?.focus();
  }, [focusTick]);
  const load = useCallback(async () => {
    void version; // recarga la lista tras guardar o borrar
    return services.briefs.list();
  }, [services, version]);
  const { state, retry } = useAsyncResource(load);
  const back = (message: string) => {
    setEditing(null);
    setNotice(message);
    setVersion((n) => n + 1);
    setFocusTick((n) => n + 1);
  };

  return (
    <section aria-labelledby="titulo-briefs">
      <h2 id="titulo-briefs" tabIndex={-1} ref={heading}>
        Briefs
      </h2>
      <p role="status" aria-live="polite">
        {notice}
      </p>
      {copying !== null ? (
        <CopiesPanel
          brief={copying}
          title={titleOf(copying)}
          onBack={() => {
            setCopying(null);
            setFocusTick((n) => n + 1);
          }}
        />
      ) : editing !== null ? (
        <BriefForm
          initial={editing === 'new' ? undefined : editing}
          onSaved={back}
          onCancel={() => back('')}
        />
      ) : (
        <>
          <AsyncStatus status={state.status} />
          {state.status === 'error' && (
            <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
          )}
          {state.status === 'success' && (
            <BriefList
              briefs={state.data}
              onNew={() => {
                setNotice('');
                setEditing('new');
              }}
              onEdit={(r) => {
                setNotice('');
                setEditing(r);
              }}
              onCopies={(r) => {
                setNotice('');
                setCopying(r);
              }}
              onDeleted={() => back('Brief eliminado.')}
            />
          )}
        </>
      )}
    </section>
  );
}

function BriefList({
  briefs,
  onNew,
  onEdit,
  onCopies,
  onDeleted,
}: {
  readonly briefs: readonly BriefRecord[];
  readonly onNew: () => void;
  readonly onEdit: (r: BriefRecord) => void;
  readonly onCopies: (r: BriefRecord) => void;
  readonly onDeleted: () => void;
}) {
  return (
    <>
      <div className="form-actions">
        <Button variant="primary" onClick={onNew}>
          Nuevo brief
        </Button>
      </div>
      {briefs.length === 0 ? (
        <EmptyState
          title="Aún no hay briefs"
          description="Crea el primero con «Nuevo brief». Se guarda solo en este navegador."
        />
      ) : (
        <ul className="plain-list" aria-label="Briefs guardados">
          {briefs.map((b) => (
            <BriefItem
              key={b.id}
              brief={b}
              onEdit={() => onEdit(b)}
              onCopies={() => onCopies(b)}
              onDeleted={onDeleted}
            />
          ))}
        </ul>
      )}
    </>
  );
}

function BriefItem({
  brief,
  onEdit,
  onCopies,
  onDeleted,
}: {
  readonly brief: BriefRecord;
  readonly onEdit: () => void;
  readonly onCopies: () => void;
  readonly onDeleted: () => void;
}) {
  const services = useServices();
  const [confirming, setConfirming] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const e = evaluateRecord(brief);
  const title = titleOf(brief);
  const remove = async () => {
    const r = await services.briefs.remove(brief.id);
    if (!r.ok) {
      setError(describeError(r.error));
      setConfirming(false);
      return;
    }
    onDeleted();
  };
  return (
    <li>
      <Card title={title} headingLevel={3}>
        <p>
          <strong>{e.status === 'completo' ? 'Completo' : 'Incompleto'}</strong>
          {brief.fields.channel ? ` · ${brief.fields.channel}` : ''}
        </p>
        {e.status === 'incompleto' && (
          <ul>
            {[...e.missing, ...e.invalid].map((m) => (
              <li key={m.field}>{m.reason}</li>
            ))}
          </ul>
        )}
        {error && <p role="alert">{error}</p>}
        {confirming ? (
          <div role="group" aria-label={`Confirmar eliminación de ${title}`}>
            <p>¿Eliminar este brief? No se puede deshacer.</p>
            <div className="form-actions">
              <Button variant="primary" onClick={() => void remove()}>
                Sí, eliminar
              </Button>
              <Button onClick={() => setConfirming(false)}>Cancelar</Button>
            </div>
          </div>
        ) : (
          <div className="form-actions">
            <Button onClick={onEdit} aria-label={`Editar ${title}`}>
              Editar
            </Button>
            <Button onClick={onCopies} aria-label={`Copys de ${title}`}>
              Copys
            </Button>
            <Button onClick={() => setConfirming(true)} aria-label={`Eliminar ${title}`}>
              Eliminar
            </Button>
          </div>
        )}
      </Card>
    </li>
  );
}

function BriefForm({
  initial,
  onSaved,
  onCancel,
}: {
  readonly initial: BriefRecord | undefined;
  readonly onSaved: (message: string) => void;
  readonly onCancel: () => void;
}) {
  const services = useServices();
  const [values, setValues] = useState<FormValues>(() => valuesOf(initial));
  const [errors, setErrors] = useState<Partial<Record<BriefField, string>>>({});
  const [saveError, setSaveError] = useState<string | null>(null);
  const form = useRef<HTMLFormElement>(null);

  // Un error aparece al guardar (no al salir del campo: eso movería el botón justo antes de pulsarlo) y se
  // revalida mientras se escribe, para que desaparezca en cuanto el valor es correcto.
  const set = (field: BriefField, patch: Partial<FormValues>) => {
    const next = { ...values, ...patch };
    setValues(next);
    if (errors[field] !== undefined) validateOne(field, next);
  };
  const validateOne = (field: BriefField, v: FormValues = values) =>
    setErrors((prev) => {
      const msg = errorOf(field, v);
      const rest = Object.fromEntries(Object.entries(prev).filter(([k]) => k !== field));
      return msg === null ? rest : { ...rest, [field]: msg };
    });

  const onSubmit = async (ev: FormEvent) => {
    ev.preventDefault();
    setSaveError(null);
    const found: Partial<Record<BriefField, string>> = {};
    for (const f of ORDER) {
      const m = errorOf(f, values);
      if (m !== null) found[f] = m;
    }
    setErrors(found);
    const firstBad = ORDER.find((f) => found[f] !== undefined);
    if (firstBad !== undefined) {
      form.current?.querySelector<HTMLElement>(`[data-field="${firstBad}"]`)?.focus();
      return;
    }
    const r = await services.briefs.save({
      ...(initial ? { id: initial.id } : {}),
      fields: fieldsOf(values),
    });
    if (!r.ok) {
      setSaveError(describeError(r.error));
      return;
    }
    const e = evaluateRecord(r.value);
    onSaved(
      e.status === 'completo'
        ? 'Brief guardado. Está completo.'
        : `Brief guardado como incompleto: ${e.missing.map((m) => m.reason).join(' ')}`,
    );
  };

  const describedBy = (f: BriefField) => (errors[f] ? `${f}-ayuda ${f}-error` : `${f}-ayuda`);
  const label = (f: BriefField) =>
    `${BRIEF_FIELD_LABELS[f]}${(REQUIRED_FIELDS as readonly string[]).includes(f) ? ' (obligatorio)' : ' (opcional)'}`;
  const hint = (f: BriefField) =>
    f === 'channel'
      ? 'Solo canales aprobados.'
      : f === 'validity'
        ? 'Fechas de inicio y fin, si aplican.'
        : `Hasta ${LONG.has(f) ? BRIEF_LONG_MAX : BRIEF_SHORT_MAX} caracteres.`;
  const errorNode = (f: BriefField) =>
    errors[f] ? (
      <p id={`${f}-error`} className="field-error" role="alert">
        {errors[f]}
      </p>
    ) : null;

  return (
    <Card title={initial ? 'Editar brief' : 'Nuevo brief'} headingLevel={3}>
      <form ref={form} onSubmit={(e) => void onSubmit(e)} noValidate>
        {ORDER.map((f) =>
          f === 'channel' ? (
            <div className="field" key={f}>
              <label htmlFor={`brief-${f}`}>{label(f)}</label>
              <select
                id={`brief-${f}`}
                data-field={f}
                value={values.channel}
                aria-describedby={describedBy(f)}
                aria-invalid={errors[f] ? true : undefined}
                onChange={(e) => set(f, { channel: e.target.value })}
              >
                <option value="">Selecciona un canal</option>
                {CHANNELS.map((c) => (
                  <option key={c} value={c}>
                    {c}
                  </option>
                ))}
              </select>
              <p id={`${f}-ayuda`} className="field-hint">
                {hint(f)}
              </p>
              {errorNode(f)}
            </div>
          ) : f === 'validity' ? (
            <fieldset className="field" key={f}>
              <legend>{label(f)}</legend>
              <label htmlFor="brief-validity-from">Desde</label>
              <input
                id="brief-validity-from"
                data-field={f}
                type="date"
                value={values.validityFrom}
                aria-describedby={describedBy(f)}
                aria-invalid={errors[f] ? true : undefined}
                onChange={(e) => set(f, { validityFrom: e.target.value })}
              />
              <label htmlFor="brief-validity-to">Hasta</label>
              <input
                id="brief-validity-to"
                type="date"
                value={values.validityTo}
                aria-describedby={describedBy(f)}
                aria-invalid={errors[f] ? true : undefined}
                onChange={(e) => set(f, { validityTo: e.target.value })}
              />
              <p id={`${f}-ayuda`} className="field-hint">
                {hint(f)}
              </p>
              {errorNode(f)}
            </fieldset>
          ) : (
            <div className="field" key={f}>
              <label htmlFor={`brief-${f}`}>{label(f)}</label>
              {LONG.has(f) ? (
                <textarea
                  id={`brief-${f}`}
                  data-field={f}
                  rows={3}
                  value={values[f]}
                  aria-describedby={describedBy(f)}
                  aria-invalid={errors[f] ? true : undefined}
                  onChange={(e) => set(f, { [f]: e.target.value })}
                />
              ) : (
                <input
                  id={`brief-${f}`}
                  data-field={f}
                  type="text"
                  autoComplete="off"
                  value={values[f]}
                  aria-describedby={describedBy(f)}
                  aria-invalid={errors[f] ? true : undefined}
                  onChange={(e) => set(f, { [f]: e.target.value })}
                />
              )}
              <p id={`${f}-ayuda`} className="field-hint">
                {hint(f)}
              </p>
              {errorNode(f)}
            </div>
          ),
        )}
        {saveError && (
          <p className="field-error" role="alert">
            {saveError}
          </p>
        )}
        <div className="form-actions">
          <Button type="submit" variant="primary">
            Guardar brief
          </Button>
          <Button onClick={onCancel}>Cancelar</Button>
        </div>
      </form>
    </Card>
  );
}
