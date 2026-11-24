import { useCallback, useState } from 'react';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { BRIEF_FIELD_LABELS } from '@/domain/brief';
import type { BriefRecord } from '@/domain/briefRecord';
import {
  CHANNEL_PRIORITIES,
  MESSAGE_ARCHITECTURE,
  UX_HIERARCHY,
  draftAll,
  type FormulaInput,
} from '@/domain/copyFormulas';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';

const EMPTY: FormulaInput = {
  product: '',
  need: '',
  benefit: '',
  offer: '',
  differentiator: '',
  cta: '',
  validity: '',
  conditions: '',
};
const KEYS = [
  'product',
  'need',
  'benefit',
  'offer',
  'differentiator',
  'cta',
  'validity',
  'conditions',
] as const;
const LABEL: Record<(typeof KEYS)[number], string> = {
  product: BRIEF_FIELD_LABELS.product,
  need: BRIEF_FIELD_LABELS.need,
  benefit: BRIEF_FIELD_LABELS.benefit,
  offer: BRIEF_FIELD_LABELS.offer,
  differentiator: BRIEF_FIELD_LABELS.differentiator,
  cta: BRIEF_FIELD_LABELS.cta,
  validity: 'Vigencia (texto libre, por ejemplo «hasta el 30 de noviembre»)',
  conditions: BRIEF_FIELD_LABELS.conditions,
};

function fromBrief(b: BriefRecord): FormulaInput {
  const f = b.fields;
  const v = f.validity;
  return {
    product: f.product ?? '',
    need: f.need ?? '',
    benefit: f.benefit ?? '',
    offer: f.offer ?? '',
    differentiator: f.differentiator ?? '',
    cta: f.cta ?? '',
    validity: v?.to ? `hasta el ${v.to}` : '',
    conditions: f.conditions ?? '',
  };
}

/**
 * Plantillas (S4.2): guía de arquitectura del mensaje y borradores armados con fórmulas clásicas (AIDA, PAS, FAB, 4U,
 * Antes-Después-Puente…) usando SOLO los datos que escribes o traes de un brief. No es IA, no inventa nada y no guarda.
 */
export function TemplatesPage() {
  const services = useServices();
  const load = useCallback(() => services.briefs.list(), [services]);
  const { state, retry } = useAsyncResource(load);
  const [input, setInput] = useState<FormulaInput>(EMPTY);
  const [copied, setCopied] = useState<string | null>(null);
  const drafts = draftAll(input);
  const copy = async (text: string, key: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(key);
    } catch {
      setCopied(null);
    }
  };
  return (
    <section aria-labelledby="titulo-plantillas">
      <h2 id="titulo-plantillas" tabIndex={-1}>
        Plantillas
      </h2>
      <p>
        Guía para estructurar el mensaje y borradores con fórmulas de copy. Los borradores usan
        únicamente los datos que escribes aquí o cargas desde un brief; son un punto de partida para
        editar, no copy final. Nada se guarda.
      </p>
      <Card title="Arquitectura del mensaje" headingLevel={3}>
        <ol aria-label="Arquitectura del mensaje">
          {MESSAGE_ARCHITECTURE.map((s) => (
            <li key={s.step}>
              <strong>{s.step}:</strong> {s.guide}
            </li>
          ))}
        </ol>
        <p>Jerarquía para el usuario: {UX_HIERARCHY.join(' → ')}</p>
      </Card>
      <Card title="Prioridad por canal" headingLevel={3}>
        <table>
          <caption>Qué priorizar según el formato</caption>
          <thead>
            <tr>
              <th scope="col">Formato</th>
              <th scope="col">Objetivo</th>
              <th scope="col">Prioridad</th>
            </tr>
          </thead>
          <tbody>
            {CHANNEL_PRIORITIES.map((c) => (
              <tr key={c.format}>
                <th scope="row">{c.format}</th>
                <td>{c.goal}</td>
                <td>{c.priority}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </Card>
      <Card title="Datos para los borradores" headingLevel={3}>
        <AsyncStatus status={state.status} />
        {state.status === 'error' && (
          <ErrorNotice message={state.message} onRetry={state.retryable ? retry : undefined} />
        )}
        {state.status === 'success' && state.data.length > 0 && (
          <div className="field">
            <label htmlFor="tpl-brief">Cargar desde un brief</label>
            <select
              id="tpl-brief"
              defaultValue=""
              onChange={(e) => {
                const b = state.data.find((x) => x.id === e.target.value);
                setInput(b ? fromBrief(b) : EMPTY);
              }}
            >
              <option value="">Elige un brief (opcional)</option>
              {state.data.map((b) => (
                <option key={b.id} value={b.id}>
                  {b.fields.campaign ?? b.id}
                </option>
              ))}
            </select>
          </div>
        )}
        {KEYS.map((k) => (
          <div className="field" key={k}>
            <label htmlFor={`tpl-${k}`}>{LABEL[k]}</label>
            <input
              id={`tpl-${k}`}
              value={input[k]}
              onChange={(e) => setInput({ ...input, [k]: e.target.value })}
            />
          </div>
        ))}
      </Card>
      <Card title="Borradores" headingLevel={3}>
        {drafts.length === 0 ? (
          <p className="field-hint">
            Escribe al menos una oferta o un beneficio para ver borradores.
          </p>
        ) : (
          <ul aria-label="Borradores">
            {drafts.map((d) => {
              const text = [d.headline, d.body, d.cta].filter(Boolean).join('\n');
              return (
                <li key={d.formula}>
                  <strong>{d.formula}</strong> — {d.concept}
                  <pre style={{ whiteSpace: 'pre-wrap' }}>{text}</pre>
                  <Button onClick={() => void copy(text, d.formula)}>Copiar {d.formula}</Button>
                  {copied === d.formula && (
                    <span role="status" aria-live="polite">
                      {' '}
                      Copiado.
                    </span>
                  )}
                </li>
              );
            })}
          </ul>
        )}
      </Card>
    </section>
  );
}
