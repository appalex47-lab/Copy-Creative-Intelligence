import { useRef, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { BACKUP_MAX_BYTES } from '@/domain/backup';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import { downloadTextFile } from '@/lib/download';
import { applyTheme } from '@/lib/theme';
import type { AppError, BackupSummary } from '@/services/contracts';

/** Los motivos de validación del archivo son textos propios (nunca contenido del archivo) y ayudan a corregir. */
const messageFor = (e: AppError) => (e.code === 'validation_error' ? e.message : describeError(e));

interface Pending {
  readonly text: string;
  readonly summary: BackupSummary;
}

/** Respaldo: exportar a un archivo e importar reemplazando TODOS los datos locales, con confirmación. */
export function BackupPage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState<Pending | null>(null);
  const [busy, setBusy] = useState(false);

  const reset = () => {
    setNotice('');
    setError(null);
  };

  const onExport = async () => {
    reset();
    setBusy(true);
    const r = await services.backup.export();
    setBusy(false);
    if (!r.ok) return setError(messageFor(r.error));
    downloadTextFile(r.value.fileName, r.value.text);
    setNotice(
      `Respaldo exportado (${r.value.summary.activityCount} eventos de actividad): ${r.value.fileName}`,
    );
  };

  const onFile = async (file: File | undefined) => {
    reset();
    setPending(null);
    if (!file) return;
    if (file.size > BACKUP_MAX_BYTES)
      return setError('El archivo supera el tamaño máximo permitido (5 MB).');
    let text: string;
    try {
      text = await file.text();
    } catch {
      return setError('No se pudo leer el archivo.');
    }
    const r = await services.backup.inspect(text);
    if (!r.ok) return setError(messageFor(r.error));
    setPending({ text, summary: r.value });
  };

  const onConfirm = async () => {
    if (!pending) return;
    reset();
    setBusy(true);
    const r = await services.backup.restore(pending.text);
    setBusy(false);
    if (!r.ok) return setError(`${messageFor(r.error)} No se cambió ningún dato.`);
    setPending(null);
    if (fileInput.current) fileInput.current.value = '';
    applyTheme(r.value.settings.theme);
    setNotice('Respaldo importado: los datos locales fueron reemplazados.');
  };

  const onCancel = () => {
    setPending(null);
    if (fileInput.current) fileInput.current.value = '';
    setNotice('Importación cancelada. No se cambió ningún dato.');
  };

  return (
    <section aria-labelledby="titulo-respaldo">
      <h2 id="titulo-respaldo" tabIndex={-1} ref={heading}>
        Respaldo
      </h2>
      <p className="field-hint">
        Tus datos viven solo en este navegador. Exporta un archivo para guardarlos o moverlos; el
        archivo no se envía a ningún servidor.
      </p>
      <Card title="Exportar" headingLevel={3}>
        <Button variant="primary" onClick={() => void onExport()} disabled={busy}>
          Exportar respaldo
        </Button>
      </Card>
      <Card title="Importar" headingLevel={3}>
        <div className="field">
          <label htmlFor="archivo-respaldo">Archivo de respaldo (.json)</label>
          <input
            id="archivo-respaldo"
            ref={fileInput}
            type="file"
            accept=".json,application/json"
            onChange={(e) => void onFile(e.target.files?.[0])}
          />
        </div>
        {pending && (
          <div role="group" aria-label="Confirmar importación">
            <p>
              Respaldo del{' '}
              <time dateTime={pending.summary.exportedAt}>{pending.summary.exportedAt}</time>:{' '}
              {pending.summary.activityCount} eventos de actividad
              {pending.summary.hasName ? ' y un nombre visible' : ''}.
            </p>
            <p>
              <strong>Importar reemplaza todos los datos locales actuales</strong> (perfil,
              preferencias y actividad). Esta acción no se puede deshacer.
            </p>
            <div className="form-actions">
              <Button variant="primary" onClick={() => void onConfirm()} disabled={busy}>
                Reemplazar todos los datos locales
              </Button>
              <Button onClick={onCancel} disabled={busy}>
                Cancelar
              </Button>
            </div>
          </div>
        )}
      </Card>
      {error && (
        <p className="field-error" role="alert">
          {error}
        </p>
      )}
      <p role="status" aria-live="polite">
        {notice}
      </p>
    </section>
  );
}
