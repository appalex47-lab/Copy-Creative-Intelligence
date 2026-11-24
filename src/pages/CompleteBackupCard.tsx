import { useRef, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { RESOURCES_BACKUP_MAX_BYTES } from '@/domain/resourceBackup';
import { useServices } from '@/hooks/ServicesContext';
import { downloadTextFile } from '@/lib/download';
import { applyTheme } from '@/lib/theme';
import type { AppError } from '@/services/contracts';

const FORMAT = 'cci-completo';
const messageFor = (e: AppError) => e.message;

/**
 * Respaldo completo (S4.3): un solo archivo con los datos (briefs, copys, reglas, auditorías…) y TAMBIÉN imágenes,
 * piezas, revisiones, mediciones y promociones. Contiene los dos respaldos existentes tal cual, así que no cambia sus
 * formatos. Al importar: los datos REEMPLAZAN los locales (como el respaldo normal) y los recursos solo se AGREGAN.
 */
export function CompleteBackupCard() {
  const services = useServices();
  const fileInput = useRef<HTMLInputElement>(null);
  const [busy, setBusy] = useState(false);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [pending, setPending] = useState<{ data: string; recursos: string } | null>(null);

  const reset = () => {
    setNotice('');
    setError(null);
  };

  const onExport = async () => {
    reset();
    setBusy(true);
    try {
      const d = await services.backup.export();
      if (!d.ok) return setError(messageFor(d.error));
      const r = await services.resources.exportBackup();
      if (!r.ok) return setError(messageFor(r.error));
      const text = JSON.stringify({
        format: FORMAT,
        version: 1,
        exportedAt: new Date().toISOString(),
        data: d.value.text,
        recursos: await r.value.blob.text(),
      });
      downloadTextFile(`cci-completo-${new Date().toISOString().slice(0, 10)}.json`, text);
      setNotice(
        'Respaldo completo exportado (datos, imágenes, piezas, revisiones, mediciones y promociones).',
      );
    } finally {
      setBusy(false);
    }
  };

  const onFile = async (file: File | undefined) => {
    reset();
    setPending(null);
    if (!file) return;
    if (file.size > RESOURCES_BACKUP_MAX_BYTES + 6 * 1024 * 1024)
      return setError('El archivo supera el tamaño máximo permitido.');
    try {
      const doc: unknown = JSON.parse(await file.text());
      if (
        typeof doc !== 'object' ||
        doc === null ||
        (doc as Record<string, unknown>)['format'] !== FORMAT ||
        typeof (doc as Record<string, unknown>)['data'] !== 'string' ||
        typeof (doc as Record<string, unknown>)['recursos'] !== 'string'
      )
        return setError('El archivo no es un respaldo completo válido.');
      const { data, recursos } = doc as { data: string; recursos: string };
      const i = await services.backup.inspect(data);
      if (!i.ok) return setError(messageFor(i.error));
      setPending({ data, recursos });
    } catch {
      setError('El archivo no es un respaldo completo válido.');
    }
  };

  const onConfirm = async () => {
    if (!pending) return;
    reset();
    setBusy(true);
    try {
      // Primero se valida lo que solo agrega; si falla, no se toca nada (los datos aún no se reemplazaron).
      const r = await services.resources.importBackup(
        new File([pending.recursos], 'recursos.json', { type: 'application/json' }),
      );
      if (!r.ok) return setError(`${messageFor(r.error)} No se cambió ningún dato.`);
      const d = await services.backup.restore(pending.data);
      if (!d.ok)
        return setError(
          `${messageFor(d.error)} Los datos no se reemplazaron; las imágenes y registros del archivo ya se agregaron.`,
        );
      applyTheme(d.value.settings.theme);
      setPending(null);
      if (fileInput.current) fileInput.current.value = '';
      setNotice(
        `Respaldo completo importado: datos reemplazados; se agregaron ${String(r.value.added)} imágenes, ${String(r.value.piecesAdded)} piezas, ${String(r.value.reviewsAdded)} revisiones, ${String(r.value.measuresAdded)} mediciones y ${String(r.value.promosAdded)} promociones.`,
      );
    } finally {
      setBusy(false);
    }
  };

  return (
    <Card title="Respaldo completo (todo en un archivo)" headingLevel={3}>
      <p className="field-hint">
        Incluye también imágenes, piezas, revisiones, mediciones y promociones. El archivo puede
        pesar mucho si tienes muchas imágenes (tope de 150 MB).
      </p>
      <div className="form-actions">
        <Button variant="primary" onClick={() => void onExport()} disabled={busy}>
          Descargar todo en un archivo
        </Button>
      </div>
      <div className="field">
        <label htmlFor="archivo-completo">Archivo con todo (.json)</label>
        <input
          id="archivo-completo"
          ref={fileInput}
          type="file"
          accept=".json,application/json"
          onChange={(e) => void onFile(e.target.files?.[0])}
        />
      </div>
      {pending && (
        <div role="group" aria-label="Confirmar importación completa">
          <p>
            <strong>Importar reemplaza los datos locales</strong> (perfil, preferencias, briefs,
            copys, reglas y auditorías) y agrega las imágenes, piezas, revisiones, mediciones y
            promociones que falten. No se puede deshacer.
          </p>
          <div className="form-actions">
            <Button variant="primary" onClick={() => void onConfirm()} disabled={busy}>
              Restaurar todo desde el archivo
            </Button>
            <Button
              onClick={() => {
                setPending(null);
                if (fileInput.current) fileInput.current.value = '';
              }}
              disabled={busy}
            >
              Cancelar restauración completa
            </Button>
          </div>
        </div>
      )}
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
