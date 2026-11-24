import { useCallback, useEffect, useRef, useState, type FormEvent } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import {
  ENTITY_KINDS,
  ENTITY_LABELS,
  ENTITY_NAME_MAX,
  ENTITY_NOTE_MAX,
  type EntityKind,
  type EntityRecord,
} from '@/domain/entity';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import type { AppError } from '@/services/contracts';

const messageOf = (e: AppError): string =>
  e.code === 'validation_error' || e.code === 'conflict' ? e.message : describeError(e);

/**
 * Catálogo simple de campañas, productos y ofertas (S2.8). Solo nombre y nota opcional: no se asumen precios,
 * vigencias ni relaciones. Lo único que se relaciona es que un brief puede referenciar una campaña registrada.
 */
export function CatalogPage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const [kind, setKind] = useState<EntityKind>('campaign');
  const [version, setVersion] = useState(0);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [editing, setEditing] = useState<EntityRecord | 'new' | null>(null);
  const [confirm, setConfirm] = useState<string | null>(null);
  const [focusTick, setFocusTick] = useState(0);
  useEffect(() => {
    if (focusTick > 0) heading.current?.focus();
  }, [focusTick]);
  const load = useCallback(async () => {
    void version;
    return services.entities.list(kind);
  }, [services, kind, version]);
  const { state, retry } = useAsyncResource(load);
  const label = ENTITY_LABELS[kind];

  const done = (message: string) => {
    setNotice(message);
    setEditing(null);
    setConfirm(null);
    setVersion((n) => n + 1);
    setFocusTick((n) => n + 1);
  };
  const save = async (name: string, note: string): Promise<void> => {
    setError(null);
    const r =
      editing !== null && editing !== 'new'
        ? await services.entities.update({ id: editing.id, name, note })
        : await services.entities.create({ kind, name, note });
    if (!r.ok) {
      setError(messageOf(r.error));
      return;
    }
    done(editing === 'new' ? label.added : 'Cambios guardados.');
  };
  const remove = async (id: string) => {
    setError(null);
    const r = await services.entities.remove(id);
    if (!r.ok) {
      setError(messageOf(r.error));
      setConfirm(null);
      return;
    }
    done('Registro eliminado.');
  };

  return (
    <section aria-labelledby="titulo-catalogo">
      <h2 id="titulo-catalogo" tabIndex={-1} ref={heading}>
        Catálogo
      </h2>
      <p>
        Campañas, productos y ofertas con nombre y nota opcional. No guardan precios, vigencias ni
        otros datos: solo sirven para nombrar y reutilizar. Los briefs pueden referenciar una
        campaña registrada.
      </p>
      <div role="group" aria-label="Tipo de registro" className="form-actions">
        {ENTITY_KINDS.map((k) => (
          <Button
            key={k}
            variant={k === kind ? 'primary' : 'secondary'}
            aria-pressed={k === kind}
            onClick={() => {
              setKind(k);
              setEditing(null);
              setConfirm(null);
              setError(null);
              setNotice('');
            }}
          >
            {ENTITY_LABELS[k].many}
          </Button>
        ))}
      </div>
      <p role="status" aria-live="polite">
        {notice}
      </p>
      {error && <p role="alert">{error}</p>}
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {state.status === 'success' && (
        <Card title={label.many} headingLevel={3}>
          {editing !== null ? (
            <EntityForm
              key={editing === 'new' ? 'new' : editing.id}
              noun={label.one}
              initial={editing === 'new' ? undefined : editing}
              onSubmit={save}
              onCancel={() => {
                setEditing(null);
                setError(null);
              }}
            />
          ) : (
            <div className="form-actions">
              <Button variant="primary" onClick={() => setEditing('new')}>
                {label.add}
              </Button>
            </div>
          )}
          {state.data.length === 0 ? (
            <p>Aún no hay {label.many.toLowerCase()}.</p>
          ) : (
            <ul className="plain-list" aria-label={label.many}>
              {state.data.map((e) => (
                <li key={e.id}>
                  <p>
                    <strong>{e.name}</strong>
                  </p>
                  {e.note && <p>{e.note}</p>}
                  {confirm === e.id ? (
                    <div role="group" aria-label={`Confirmar eliminación de ${e.name}`}>
                      <p>¿Eliminar este registro? No se puede deshacer.</p>
                      <div className="form-actions">
                        <Button variant="primary" onClick={() => void remove(e.id)}>
                          Sí, eliminar registro
                        </Button>
                        <Button onClick={() => setConfirm(null)}>Cancelar</Button>
                      </div>
                    </div>
                  ) : (
                    <div className="form-actions">
                      <Button onClick={() => setEditing(e)} aria-label={`Editar ${e.name}`}>
                        Editar
                      </Button>
                      <Button onClick={() => setConfirm(e.id)} aria-label={`Eliminar ${e.name}`}>
                        Eliminar
                      </Button>
                    </div>
                  )}
                </li>
              ))}
            </ul>
          )}
        </Card>
      )}
    </section>
  );
}

function EntityForm({
  noun,
  initial,
  onSubmit,
  onCancel,
}: {
  readonly noun: string;
  readonly initial: EntityRecord | undefined;
  readonly onSubmit: (name: string, note: string) => Promise<void>;
  readonly onCancel: () => void;
}) {
  const [name, setName] = useState(initial?.name ?? '');
  const [note, setNote] = useState(initial?.note ?? '');
  const submit = (e: FormEvent) => {
    e.preventDefault();
    void onSubmit(name, note);
  };
  return (
    <form onSubmit={submit} noValidate aria-label={`Formulario de ${noun}`}>
      <div className="field">
        <label htmlFor="catalogo-nombre">Nombre (obligatorio)</label>
        <input
          id="catalogo-nombre"
          type="text"
          autoComplete="off"
          value={name}
          maxLength={ENTITY_NAME_MAX}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
      <div className="field">
        <label htmlFor="catalogo-nota">Nota (opcional)</label>
        <textarea
          id="catalogo-nota"
          rows={3}
          value={note}
          maxLength={ENTITY_NOTE_MAX}
          onChange={(e) => setNote(e.target.value)}
        />
      </div>
      <div className="form-actions">
        <Button type="submit" variant="primary">
          {initial ? 'Guardar cambios' : `Agregar ${noun}`}
        </Button>
        <Button onClick={onCancel}>Cancelar</Button>
      </div>
    </form>
  );
}
