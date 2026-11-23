import { useCallback, useRef, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { formatBytes, type StorageInfo } from '@/domain/storageInfo';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';

const persistedText = (p: boolean | null) =>
  p === null
    ? 'No disponible'
    : p
      ? 'Sí'
      : 'No (el navegador puede borrar los datos si falta espacio)';

/** Uso, cuota y persistencia del almacenamiento del navegador. Lo que el navegador no expone dice «No disponible». */
export function StoragePage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const load = useCallback(() => services.storage.get(), [services]);
  const { state, retry } = useAsyncResource(load);
  const onRetry = () => {
    heading.current?.focus();
    retry();
  };
  return (
    <section aria-labelledby="titulo-almacenamiento">
      <h2 id="titulo-almacenamiento" tabIndex={-1} ref={heading}>
        Almacenamiento
      </h2>
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? onRetry : undefined} />
      )}
      {state.status === 'success' && <StorageDetails initial={state.data} />}
    </section>
  );
}

function StorageDetails({ initial }: { readonly initial: StorageInfo }) {
  const services = useServices();
  const [info, setInfo] = useState(initial);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState<string | null>(null);

  const onRequest = async () => {
    setNotice('');
    const r = await services.storage.requestPersistence();
    if (!r.ok) {
      setError(describeError(r.error));
      return;
    }
    setError(null);
    setInfo(r.value);
    setNotice(
      r.value.persisted === true
        ? 'Almacenamiento persistente concedido.'
        : r.value.persisted === false
          ? 'El navegador no concedió almacenamiento persistente.'
          : 'Este navegador no informa si el almacenamiento es persistente.',
    );
  };

  return (
    <Card title="Datos en este navegador" headingLevel={3}>
      <dl>
        <dt>Espacio usado</dt>
        <dd>{formatBytes(info.usageBytes)}</dd>
        <dt>Espacio disponible para la aplicación (cuota)</dt>
        <dd>{formatBytes(info.quotaBytes)}</dd>
        <dt>Almacenamiento persistente</dt>
        <dd>{persistedText(info.persisted)}</dd>
      </dl>
      <p className="field-hint">
        Las cifras son estimaciones del navegador. Los datos solo viven en este navegador.
      </p>
      <div className="form-actions">
        <Button
          onClick={() => void onRequest()}
          disabled={info.persisted === true || info.persisted === null}
        >
          Solicitar almacenamiento persistente
        </Button>
      </div>
      {error && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
      <p role="status" aria-live="polite">
        {notice}
      </p>
    </Card>
  );
}
