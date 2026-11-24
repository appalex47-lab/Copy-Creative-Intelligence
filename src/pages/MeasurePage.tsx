import { useCallback, useRef, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import {
  METRICS,
  METRIC_LABELS,
  analyzeExperiment,
  conversionRate,
  ctr,
  pct,
  type ExperimentRecord,
  type MeasureRecord,
  type Metric,
} from '@/domain/measure';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import type { AppError } from '@/services/contracts';

const messageOf = (e: AppError): string =>
  e.code === 'validation_error' ? e.message : describeError(e);
const num = (s: string): number => (s.trim() === '' ? Number.NaN : Number(s.replace(/,/g, '')));

/**
 * Medición (S4.2): resultados capturados a mano o importados por CSV, y experimentos A/B con hipótesis. Nada se
 * consulta en plataformas externas: tú escribes o importas las cifras. La comparación A/B es orientativa.
 */
export function MeasurePage() {
  const services = useServices();
  const load = useCallback(() => services.measures.list(), [services]);
  const { state, retry } = useAsyncResource(load);
  const [error, setError] = useState<AppError | null>(null);
  const [msg, setMsg] = useState<string | null>(null);
  const fileInput = useRef<HTMLInputElement>(null);

  const done = (m: string) => {
    setError(null);
    setMsg(m);
    retry();
  };

  const [r, setR] = useState({
    label: '',
    impressions: '',
    clicks: '',
    conversions: '',
    sales: '',
    from: '',
    to: '',
  });
  const saveResult = async () => {
    setMsg(null);
    const res = await services.measures.saveResult({
      label: r.label,
      impressions: num(r.impressions),
      clicks: num(r.clicks),
      conversions: num(r.conversions),
      ...(r.sales.trim() !== '' ? { sales: num(r.sales) } : {}),
      ...(r.from ? { from: r.from } : {}),
      ...(r.to ? { to: r.to } : {}),
    });
    if (!res.ok) return setError(res.error);
    setR({ label: '', impressions: '', clicks: '', conversions: '', sales: '', from: '', to: '' });
    done('Resultado guardado.');
  };

  const onCsv = async (file: File | undefined) => {
    setMsg(null);
    if (!file) return;
    if (file.size > 1_000_000) {
      setError({ code: 'validation_error', message: 'El CSV supera 1 MB.' } as AppError);
      return;
    }
    const res = await services.measures.importResults(await file.text());
    if (fileInput.current) fileInput.current.value = '';
    if (!res.ok) return setError(res.error);
    done(`Se importaron ${String(res.value)} resultados.`);
  };

  const emptyVar = { label: '', impressions: '', clicks: '', conversions: '' };
  const [e, setE] = useState({
    name: '',
    hypothesis: '',
    variable: '',
    primary: 'ctr' as Metric,
    secondary: '' as '' | Metric,
    conclusion: '',
    a: { ...emptyVar, label: 'A' },
    b: { ...emptyVar, label: 'B' },
  });
  const saveExperiment = async () => {
    setMsg(null);
    const v = (x: typeof emptyVar) => ({
      label: x.label,
      impressions: num(x.impressions),
      clicks: num(x.clicks),
      conversions: num(x.conversions),
    });
    const res = await services.measures.saveExperiment({
      name: e.name,
      hypothesis: e.hypothesis,
      variable: e.variable,
      primary: e.primary,
      ...(e.secondary ? { secondary: e.secondary } : {}),
      variants: [v(e.a), v(e.b)],
      ...(e.conclusion.trim() ? { conclusion: e.conclusion } : {}),
    });
    if (!res.ok) return setError(res.error);
    setE({
      ...e,
      name: '',
      hypothesis: '',
      variable: '',
      conclusion: '',
      a: { ...emptyVar, label: 'A' },
      b: { ...emptyVar, label: 'B' },
    });
    done('Experimento guardado.');
  };

  const remove = async (id: string) => {
    const res = await services.measures.remove(id);
    if (!res.ok) return setError(res.error);
    done('Registro eliminado.');
  };

  const field = (
    id: string,
    label: string,
    value: string,
    onChange: (v: string) => void,
    extra: { type?: string; hint?: string } = {},
  ) => (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <input
        id={id}
        value={value}
        type={extra.type ?? 'text'}
        inputMode={
          extra.type === 'date' ? undefined : extra.type === 'number' ? 'numeric' : undefined
        }
        onChange={(ev) => onChange(ev.target.value)}
      />
      {extra.hint && <p className="field-hint">{extra.hint}</p>}
    </div>
  );

  const metricSelect = (
    id: string,
    label: string,
    value: string,
    onChange: (v: string) => void,
    optional = false,
  ) => (
    <div className="field">
      <label htmlFor={id}>{label}</label>
      <select id={id} value={value} onChange={(ev) => onChange(ev.target.value)}>
        {optional && <option value="">Ninguno</option>}
        {METRICS.map((m) => (
          <option key={m} value={m}>
            {METRIC_LABELS[m]}
          </option>
        ))}
      </select>
    </div>
  );

  return (
    <section aria-labelledby="titulo-medicion">
      <h2 id="titulo-medicion" tabIndex={-1}>
        Medición
      </h2>
      <p>
        Registra qué resultados tuvo una pieza o copy y compara dos versiones con un experimento
        A/B. La app no se conecta a ninguna plataforma: tú capturas o importas las cifras. CTR =
        clics ÷ impresiones; conversión = conversiones ÷ clics.
      </p>

      <Card title="Resultado manual" headingLevel={3}>
        <form
          aria-label="Resultado manual"
          onSubmit={(ev) => {
            ev.preventDefault();
            void saveResult();
          }}
        >
          {field('res-label', 'Nombre (pieza, copy o campaña)', r.label, (v) =>
            setR({ ...r, label: v }),
          )}
          {field('res-imp', 'Impresiones', r.impressions, (v) => setR({ ...r, impressions: v }), {
            type: 'number',
          })}
          {field('res-clk', 'Clics', r.clicks, (v) => setR({ ...r, clicks: v }), {
            type: 'number',
          })}
          {field('res-cnv', 'Conversiones', r.conversions, (v) => setR({ ...r, conversions: v }), {
            type: 'number',
          })}
          {field('res-sales', 'Ventas (opcional)', r.sales, (v) => setR({ ...r, sales: v }), {
            type: 'number',
          })}
          {field('res-from', 'Desde (opcional)', r.from, (v) => setR({ ...r, from: v }), {
            type: 'date',
          })}
          {field('res-to', 'Hasta (opcional)', r.to, (v) => setR({ ...r, to: v }), {
            type: 'date',
          })}
          <div className="form-actions">
            <Button variant="primary" type="submit">
              Guardar resultado
            </Button>
          </div>
        </form>
      </Card>

      <Card title="Importar resultados desde CSV" headingLevel={3}>
        <p className="field-hint">
          Columnas: objetivo, impresiones, clics, conversiones; opcionales: ventas, desde, hasta,
          nota. Hasta 500 filas. Si una fila falla, no se importa nada.
        </p>
        <div className="field">
          <label htmlFor="res-csv">Archivo CSV de resultados</label>
          <input
            id="res-csv"
            ref={fileInput}
            type="file"
            accept=".csv,text/csv"
            onChange={(ev) => void onCsv(ev.target.files?.[0])}
          />
        </div>
      </Card>

      <Card title="Experimento A/B" headingLevel={3}>
        <form
          aria-label="Experimento A/B"
          onSubmit={(ev) => {
            ev.preventDefault();
            void saveExperiment();
          }}
        >
          {field('exp-name', 'Nombre del experimento', e.name, (v) => setE({ ...e, name: v }))}
          {field('exp-hyp', 'Hipótesis', e.hypothesis, (v) => setE({ ...e, hypothesis: v }), {
            hint: 'Por ejemplo: un titular con el descuento por delante aumentará el CTR.',
          })}
          {field('exp-var', 'Variable que cambia', e.variable, (v) => setE({ ...e, variable: v }))}
          {metricSelect('exp-primary', 'Indicador principal', e.primary, (v) =>
            setE({ ...e, primary: v as Metric }),
          )}
          {metricSelect(
            'exp-secondary',
            'Indicador secundario (opcional)',
            e.secondary,
            (v) => setE({ ...e, secondary: v as '' | Metric }),
            true,
          )}
          {(['a', 'b'] as const).map((k) => (
            <fieldset key={k}>
              <legend>Variante {k.toUpperCase()}</legend>
              {field(`exp-${k}-label`, `Nombre variante ${k.toUpperCase()}`, e[k].label, (v) =>
                setE({ ...e, [k]: { ...e[k], label: v } }),
              )}
              {field(
                `exp-${k}-imp`,
                `Impresiones ${k.toUpperCase()}`,
                e[k].impressions,
                (v) => setE({ ...e, [k]: { ...e[k], impressions: v } }),
                { type: 'number' },
              )}
              {field(
                `exp-${k}-clk`,
                `Clics ${k.toUpperCase()}`,
                e[k].clicks,
                (v) => setE({ ...e, [k]: { ...e[k], clicks: v } }),
                { type: 'number' },
              )}
              {field(
                `exp-${k}-cnv`,
                `Conversiones ${k.toUpperCase()}`,
                e[k].conversions,
                (v) => setE({ ...e, [k]: { ...e[k], conversions: v } }),
                { type: 'number' },
              )}
            </fieldset>
          ))}
          {field('exp-concl', 'Conclusión (opcional, la escribes tú)', e.conclusion, (v) =>
            setE({ ...e, conclusion: v }),
          )}
          <div className="form-actions">
            <Button variant="primary" type="submit">
              Guardar experimento
            </Button>
          </div>
        </form>
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
        (state.data.length === 0 ? (
          <EmptyState
            title="Aún no hay mediciones"
            description="Captura un resultado o importa un CSV."
          />
        ) : (
          <Card title="Registros" headingLevel={3}>
            <ul aria-label="Registros de medición">
              {state.data.map((m) => (
                <li key={m.id}>
                  <MeasureLine m={m} /> <Button onClick={() => void remove(m.id)}>Eliminar</Button>
                </li>
              ))}
            </ul>
          </Card>
        ))}
    </section>
  );
}

function MeasureLine({ m }: { m: MeasureRecord }) {
  if (m.kind === 'resultado')
    return (
      <span>
        <strong>{m.label}</strong>: {m.impressions} impresiones · CTR {pct(ctr(m))} · conversión{' '}
        {pct(conversionRate(m))}
        {m.sales !== undefined ? ` · ventas ${String(m.sales)}` : ''}
      </span>
    );
  return <ExperimentLine e={m} />;
}

function ExperimentLine({ e }: { e: ExperimentRecord }) {
  const a = analyzeExperiment(e);
  return (
    <span>
      <strong>Experimento: {e.name}</strong> — {e.hypothesis} ({METRIC_LABELS[e.primary]}):{' '}
      {a.message}
      {a.smallSample ? ' Muestra pequeña: toma el resultado con cautela.' : ''}
      {e.conclusion ? ` Conclusión: ${e.conclusion}` : ''}
    </span>
  );
}
