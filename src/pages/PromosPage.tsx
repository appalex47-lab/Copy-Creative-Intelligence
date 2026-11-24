import { useCallback, useRef, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { currentVersion } from '@/domain/copy';
import { checkTextAgainstPromo } from '@/domain/promo';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import type { AppError } from '@/services/contracts';

const messageOf = (e: AppError): string =>
  e.code === 'validation_error' ? e.message : describeError(e);
const today = () => new Date().toISOString().slice(0, 10);

/**
 * Validador de promociones (S4.2): importas o capturas las promociones (nombre, porcentaje, SKUs, vigencia,
 * restricciones) y la app contrasta con ellas el TEXTO de un copy, de una pieza (texto validado u OCR) o uno pegado.
 * No consulta catálogos ni precios, ni lee SKUs dentro de imágenes.
 */
export function PromosPage() {
  const services = useServices();
  const load = useCallback(async () => {
    const [p, c, pi, rs] = await Promise.all([
      services.promos.list(),
      services.copies.list(),
      services.pieces.list(),
      services.resources.list(),
    ]);
    if (!p.ok) return p;
    if (!c.ok) return c;
    if (!pi.ok) return pi;
    if (!rs.ok) return rs;
    return {
      ok: true as const,
      value: { promos: p.value, copies: c.value, pieces: pi.value, resources: rs.value },
    };
  }, [services]);
  const { state, retry } = useAsyncResource(load);
  const [error, setError] = useState<AppError | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);
  const [f, setF] = useState({ name: '', pct: '', skus: '', from: '', to: '', restrictions: '' });
  const [promoId, setPromoId] = useState('');
  const [source, setSource] = useState('');
  const [pasted, setPasted] = useState('');

  const done = (m: string) => {
    setError(null);
    setMsg(m);
    retry();
  };

  const save = async () => {
    setMsg(null);
    const pctN = f.pct.trim() === '' ? undefined : Number(f.pct.replace(',', '.').replace('%', ''));
    const r = await services.promos.save({
      name: f.name,
      ...(pctN !== undefined ? { discountPct: pctN } : {}),
      skus: f.skus.split(/[\s,;]+/).filter(Boolean),
      ...(f.from ? { from: f.from } : {}),
      ...(f.to ? { to: f.to } : {}),
      ...(f.restrictions.trim() ? { restrictions: f.restrictions } : {}),
    });
    if (!r.ok) return setError(r.error);
    setF({ name: '', pct: '', skus: '', from: '', to: '', restrictions: '' });
    done('Promoción guardada.');
  };

  const onCsv = async (file: File | undefined) => {
    setMsg(null);
    if (!file) return;
    if (file.size > 2_000_000) {
      setError({ code: 'validation_error', message: 'El CSV supera 2 MB.' } as AppError);
      return;
    }
    const r = await services.promos.importCsv(await file.text());
    if (fileInput.current) fileInput.current.value = '';
    if (!r.ok) return setError(r.error);
    done(`Se importaron ${String(r.value)} promociones.`);
  };

  const textOf = (): string => {
    if (state.status !== 'success') return '';
    if (source === 'pegado') return pasted;
    const [type, id] = source.split(':');
    if (type === 'copy') {
      const c = state.data.copies.find((x) => x.id === id);
      return c ? Object.values(currentVersion(c).content).join('\n') : '';
    }
    const p = state.data.pieces.find((x) => x.id === id);
    const res = p ? state.data.resources.find((x) => x.id === p.resourceId) : undefined;
    return res?.reviewedText ?? res?.ocr?.text ?? '';
  };

  const promo =
    state.status === 'success' ? state.data.promos.find((p) => p.id === promoId) : undefined;
  const text = textOf();
  const checks = promo && text.trim() !== '' ? checkTextAgainstPromo(text, promo, today()) : null;

  return (
    <section aria-labelledby="titulo-promos">
      <h2 id="titulo-promos" tabIndex={-1}>
        Promociones
      </h2>
      <p>
        Registra las promociones vigentes y valida que el texto de un copy o pieza diga lo mismo:
        porcentaje, vigencia y restricciones. La app no consulta catálogos ni precios: las
        promociones las capturas o importas tú.
      </p>
      <Card title="Nueva promoción" headingLevel={3}>
        <form
          aria-label="Nueva promoción"
          onSubmit={(ev) => {
            ev.preventDefault();
            void save();
          }}
        >
          {(
            [
              ['promo-name', 'Nombre', 'name', 'text'],
              ['promo-pct', 'Porcentaje de descuento (opcional)', 'pct', 'text'],
              ['promo-skus', 'SKUs (separados por coma o espacio)', 'skus', 'text'],
              ['promo-from', 'Vigente desde', 'from', 'date'],
              ['promo-to', 'Vigente hasta', 'to', 'date'],
              ['promo-res', 'Restricciones (opcional)', 'restrictions', 'text'],
            ] as const
          ).map(([id, label, key, type]) => (
            <div className="field" key={id}>
              <label htmlFor={id}>{label}</label>
              <input
                id={id}
                type={type}
                value={f[key]}
                onChange={(ev) => setF({ ...f, [key]: ev.target.value })}
              />
            </div>
          ))}
          <div className="form-actions">
            <Button variant="primary" type="submit">
              Guardar promoción
            </Button>
          </div>
        </form>
      </Card>
      <Card title="Importar promociones desde CSV" headingLevel={3}>
        <p className="field-hint">
          Columnas: nombre; opcionales: porcentaje, sku, desde, hasta (AAAA-MM-DD), restricciones.
          Las filas con el mismo nombre se unen y juntan sus SKUs. Si una fila falla, no se importa
          nada.
        </p>
        <div className="field">
          <label htmlFor="promo-csv">Archivo CSV de promociones</label>
          <input
            id="promo-csv"
            ref={fileInput}
            type="file"
            accept=".csv,text/csv"
            onChange={(ev) => void onCsv(ev.target.files?.[0])}
          />
        </div>
      </Card>
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
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
      )}
      {state.status === 'success' &&
        (state.data.promos.length === 0 ? (
          <EmptyState title="Aún no hay promociones" description="Captura una o importa un CSV." />
        ) : (
          <>
            <Card title="Promociones guardadas" headingLevel={3}>
              <ul aria-label="Promociones guardadas">
                {state.data.promos.map((p) => (
                  <li key={p.id}>
                    <strong>{p.name}</strong>
                    {p.discountPct !== undefined ? ` · ${String(p.discountPct)} %` : ''} ·{' '}
                    {p.skus.length} SKUs
                    {p.from || p.to ? ` · ${p.from ?? '…'} a ${p.to ?? '…'}` : ''}{' '}
                    <Button
                      onClick={() =>
                        void services.promos
                          .remove(p.id)
                          .then((r) => (r.ok ? done('Promoción eliminada.') : setError(r.error)))
                      }
                    >
                      Eliminar {p.name}
                    </Button>
                  </li>
                ))}
              </ul>
            </Card>
            <Card title="Validar un texto" headingLevel={3}>
              <div className="field">
                <label htmlFor="val-promo">Promoción</label>
                <select
                  id="val-promo"
                  value={promoId}
                  onChange={(ev) => setPromoId(ev.target.value)}
                >
                  <option value="">Elige una promoción</option>
                  {state.data.promos.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>
              </div>
              <div className="field">
                <label htmlFor="val-source">Texto a validar</label>
                <select
                  id="val-source"
                  value={source}
                  onChange={(ev) => setSource(ev.target.value)}
                >
                  <option value="">Elige el texto</option>
                  <option value="pegado">Texto pegado</option>
                  <optgroup label="Copys">
                    {state.data.copies.map((c) => (
                      <option key={c.id} value={`copy:${c.id}`}>
                        {c.label}
                      </option>
                    ))}
                  </optgroup>
                  <optgroup label="Piezas (texto validado u OCR)">
                    {state.data.pieces.map((p) => (
                      <option key={p.id} value={`pieza:${p.id}`}>
                        {p.name}
                      </option>
                    ))}
                  </optgroup>
                </select>
              </div>
              {source === 'pegado' && (
                <div className="field">
                  <label htmlFor="val-text">Texto pegado</label>
                  <textarea
                    id="val-text"
                    rows={4}
                    value={pasted}
                    onChange={(ev) => setPasted(ev.target.value)}
                  />
                </div>
              )}
              {promo && source !== '' && text.trim() === '' && (
                <p role="status">El texto elegido está vacío o la pieza aún no tiene texto.</p>
              )}
              {checks && (
                <div role="status" aria-live="polite" aria-label="Resultado de la validación">
                  {checks.length === 0 ? (
                    <p>Sin diferencias con la promoción en lo que la app puede comprobar.</p>
                  ) : (
                    <ul>
                      {checks.map((c) => (
                        <li key={c.message}>
                          <strong>{c.severity}</strong>: {c.message}
                        </li>
                      ))}
                    </ul>
                  )}
                </div>
              )}
            </Card>
          </>
        ))}
    </section>
  );
}
