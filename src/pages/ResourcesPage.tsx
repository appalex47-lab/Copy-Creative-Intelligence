import { useCallback, useEffect, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { countUncertain, RESOURCE_LIMITS, type ResourceRecord } from '@/domain/resource';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import { formatLocalDateTime } from '@/lib/formatDate';
import type { AppError } from '@/services/contracts';

const messageOf = (e: AppError): string =>
  e.code === 'validation_error' ? e.message : describeError(e);
const MB = (n: number) => `${String(Math.round((n / 1024 / 1024) * 10) / 10)} MB`;
const FORMATS = RESOURCE_LIMITS.mimes.map((m) => m.replace('image/', '').toUpperCase()).join(', ');

/**
 * Recursos visuales y OCR (S3.3, funciones 1 y 2 de la Fase 3). La imagen se guarda sin modificar solo en este
 * navegador (no va en el respaldo). El OCR corre aquí mismo, sin enviar nada a internet. Lo que el OCR detecta se
 * muestra aparte de lo que una persona valida: el OCR no aprueba nada y las palabras dudosas se marcan, no se corrigen.
 */
export function ResourcesPage() {
  const services = useServices();
  const load = useCallback(() => services.resources.list(), [services]);
  const { state, retry } = useAsyncResource(load);
  const [error, setError] = useState<AppError | null>(null);
  const [busy, setBusy] = useState(false);

  const onFile = async (file: File | undefined) => {
    if (!file) return;
    setError(null);
    setBusy(true);
    const r = await services.resources.add(file);
    setBusy(false);
    if (!r.ok) setError(r.error);
    else retry();
  };

  return (
    <section aria-labelledby="titulo-recursos">
      <h2 id="titulo-recursos" tabIndex={-1}>
        Recursos
      </h2>
      <p>
        Sube imágenes (banners, posts) y lee su texto con OCR. Todo ocurre en este navegador: la
        imagen y el texto no salen de tu equipo.
      </p>
      <p className="field-hint">
        Formatos: {FORMATS}. Máximo {MB(RESOURCE_LIMITS.maxBytes)} por imagen y{' '}
        {RESOURCE_LIMITS.maxResources} recursos (valores vigentes, ajustables). Las imágenes NO van
        en el respaldo de datos (Respaldo): tienen su propio respaldo, abajo.
      </p>
      <div className="field">
        <label htmlFor="res-file">Agregar imagen</label>
        <input
          id="res-file"
          type="file"
          accept={RESOURCE_LIMITS.mimes.join(',')}
          disabled={busy}
          onChange={(e) => {
            const input = e.currentTarget;
            const f = input.files?.[0];
            void onFile(f).then(() => {
              input.value = '';
            });
          }}
        />
      </div>
      {error && (
        <p role="alert" className="field-error">
          {messageOf(error)}
        </p>
      )}
      <BackupBox onRestored={retry} />
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {state.status === 'success' &&
        (state.data.length === 0 ? (
          <EmptyState title="Aún no hay recursos" description="Agrega una imagen para empezar." />
        ) : (
          <ul className="plain-list" aria-label="Recursos guardados">
            {state.data.map((r) => (
              <li key={r.id}>
                <ResourceCard resource={r} onChanged={retry} />
              </li>
            ))}
          </ul>
        ))}
    </section>
  );
}

function BackupBox({ onRestored }: { readonly onRestored: () => void }) {
  const services = useServices();
  const [msg, setMsg] = useState<string | null>(null);
  const [error, setError] = useState<AppError | null>(null);
  const [busy, setBusy] = useState(false);
  const download = async () => {
    setError(null);
    setMsg(null);
    setBusy(true);
    const r = await services.resources.exportBackup();
    setBusy(false);
    if (!r.ok) return setError(r.error);
    const url = URL.createObjectURL(r.value.blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = r.value.fileName;
    a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    setMsg('Respaldo de imágenes descargado.');
  };
  const restore = async (file: File | undefined) => {
    if (!file) return;
    setError(null);
    setMsg(null);
    setBusy(true);
    const r = await services.resources.importBackup(file);
    setBusy(false);
    if (!r.ok) return setError(r.error);
    setMsg(
      `Restauradas ${String(r.value.added)} imágenes; ${String(r.value.skipped)} ya existían y se omitieron.`,
    );
    onRestored();
  };
  return (
    <fieldset>
      <legend>Respaldo de imágenes</legend>
      <p className="field-hint">
        Archivo aparte del respaldo de datos. Al restaurar solo se agregan las imágenes que faltan;
        no se reemplaza ni se borra nada.
      </p>
      <div className="form-actions">
        <Button onClick={() => void download()} disabled={busy}>
          Descargar respaldo de imágenes
        </Button>
      </div>
      <div className="field">
        <label htmlFor="res-restore">Restaurar respaldo de imágenes</label>
        <input
          id="res-restore"
          type="file"
          accept="application/json,.json"
          disabled={busy}
          onChange={(e) => {
            const input = e.currentTarget;
            void restore(input.files?.[0]).then(() => {
              input.value = '';
            });
          }}
        />
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
    </fieldset>
  );
}

function ResourceCard({
  resource: initial,
  onChanged,
}: {
  readonly resource: ResourceRecord;
  readonly onChanged: () => void;
}) {
  const services = useServices();
  const [resource, setResource] = useState(initial);
  const [url, setUrl] = useState<string | null>(null);
  const [progress, setProgress] = useState<number | null>(null);
  const [error, setError] = useState<AppError | null>(null);
  const [draft, setDraft] = useState(resource.reviewedText ?? '');
  const [confirming, setConfirming] = useState(false);
  const [saved, setSaved] = useState(false);

  useEffect(() => {
    const u = URL.createObjectURL(resource.blob);
    let live = true;
    void Promise.resolve().then(() => {
      if (live) setUrl(u);
    });
    return () => {
      live = false;
      URL.revokeObjectURL(u);
    };
  }, [resource.blob]);

  const run = async () => {
    setError(null);
    setProgress(0);
    const r = await services.resources.runOcr(resource.id, setProgress);
    setProgress(null);
    if (!r.ok) setError(r.error);
    else setResource(r.value);
  };
  const save = async () => {
    setError(null);
    setSaved(false);
    const r = await services.resources.saveReview(resource.id, draft);
    if (!r.ok) setError(r.error);
    else {
      setSaved(true);
      setResource(r.value);
    }
  };
  const del = async () => {
    const r = await services.resources.remove(resource.id);
    if (!r.ok) setError(r.error);
    else onChanged();
  };

  const ocr = resource.ocr;
  const uncertain = ocr ? countUncertain(ocr.words) : 0;
  return (
    <Card title={resource.name} headingLevel={3}>
      <p className="field-hint">
        {resource.width}×{resource.height} px · {MB(resource.size)} ·{' '}
        {formatLocalDateTime(resource.createdAt)}
      </p>
      {url && (
        <img
          src={url}
          alt={`Vista previa de ${resource.name} (imagen original sin modificar)`}
          style={{ maxWidth: '100%', maxHeight: 240 }}
        />
      )}
      <div className="form-actions">
        <Button variant="primary" onClick={() => void run()} disabled={progress !== null}>
          {ocr ? 'Volver a leer con OCR' : 'Leer con OCR'}
        </Button>
      </div>
      {progress !== null && (
        <p role="status" aria-live="polite">
          Leyendo texto… {Math.round(progress * 100)} %
        </p>
      )}
      {error && (
        <p role="alert" className="field-error">
          {messageOf(error)}
        </p>
      )}
      {ocr && (
        <>
          <h4>Detectado por OCR (no validado)</h4>
          <p className="field-hint">
            {ocr.engine} · idiomas {ocr.langs} · {formatLocalDateTime(ocr.ranAt)}.{' '}
            {uncertain === 0
              ? 'Sin palabras dudosas.'
              : `${String(uncertain)} palabras dudosas (confianza menor a ${String(ocr.threshold)}): revísalas contra la imagen; no se corrigen solas.`}
          </p>
          {ocr.words.length === 0 ? (
            <p>No se detectó texto.</p>
          ) : (
            <p aria-label="Texto detectado">
              {ocr.words
                .map((w, i) =>
                  w.uncertain ? (
                    <mark key={i} title={`Confianza ${String(w.confidence)} %`}>
                      {w.text}
                      <span className="sr-only"> (dudosa, confianza {w.confidence} %)</span>
                    </mark>
                  ) : (
                    <span key={i}>{w.text}</span>
                  ),
                )
                .flatMap((el, i) => (i === 0 ? [el] : [' ', el]))}
            </p>
          )}
        </>
      )}
      <h4>Validado por persona</h4>
      <div className="field">
        <label htmlFor={`rev-${resource.id}`}>Texto confirmado de la imagen</label>
        <textarea
          id={`rev-${resource.id}`}
          rows={4}
          maxLength={RESOURCE_LIMITS.maxReviewedLength}
          value={draft}
          onChange={(e) => {
            setDraft(e.target.value);
            setSaved(false);
          }}
        />
      </div>
      <div className="form-actions">
        {ocr && (
          <Button onClick={() => setDraft(ocr.text)}>Copiar lo detectado para revisarlo</Button>
        )}
        <Button variant="primary" onClick={() => void save()}>
          Guardar texto validado
        </Button>
      </div>
      {saved && (
        <p role="status" aria-live="polite">
          {draft.trim() === '' ? 'Validación quitada.' : 'Texto validado guardado.'}
        </p>
      )}
      {resource.reviewedAt && (
        <p className="field-hint">Validado el {formatLocalDateTime(resource.reviewedAt)}.</p>
      )}
      {confirming ? (
        <div role="group" aria-label={`Confirmar eliminación de ${resource.name}`}>
          <p>¿Eliminar esta imagen y su texto? No se puede deshacer.</p>
          <div className="form-actions">
            <Button variant="primary" onClick={() => void del()}>
              Sí, eliminar recurso
            </Button>
            <Button onClick={() => setConfirming(false)}>Cancelar</Button>
          </div>
        </div>
      ) : (
        <div className="form-actions">
          <Button
            onClick={() => setConfirming(true)}
            aria-label={`Eliminar recurso ${resource.name}`}
          >
            Eliminar
          </Button>
        </div>
      )}
    </Card>
  );
}
