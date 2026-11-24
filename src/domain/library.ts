import type { AuditRecord } from './audit';
import { conversionRate, ctr, MIN_SAMPLE, type MeasureRecord } from './measure';
import type { PieceRecord } from './piece';
import { summarizeReview, type ReviewRecord } from './review';

/**
 * Biblioteca de aprendizaje (S4.2): resume lo que ya está guardado, sin captura nueva. Revisiones aprobadas y
 * rechazadas con motivo, errores recurrentes entre auditorías (copys y piezas) y revisiones, y mejores resultados
 * medidos. «Mejores» exige al menos 100 impresiones; un clic alto sin ventas no basta, por eso se muestra también la conversión.
 */
export interface LibraryEntry {
  readonly label: string;
  readonly type: string;
  readonly score: number | null;
  readonly reasons: readonly string[];
}
export interface Recurring {
  readonly text: string;
  readonly count: number;
}
export interface BestResult {
  readonly label: string;
  readonly ctr: number | null;
  readonly conversion: number | null;
  readonly impressions: number;
}
export interface Library {
  readonly approved: readonly LibraryEntry[];
  readonly rejected: readonly LibraryEntry[];
  readonly recurring: readonly Recurring[];
  readonly best: readonly BestResult[];
  readonly experiments: readonly { readonly name: string; readonly conclusion: string }[];
}

const norm = (s: string) => s.trim().toLowerCase().replace(/\s+/g, ' ');

export function buildLibrary(input: {
  readonly reviews: readonly ReviewRecord[];
  readonly copyAudits: readonly AuditRecord[];
  readonly pieces: readonly PieceRecord[];
  readonly measures: readonly MeasureRecord[];
}): Library {
  const approved: LibraryEntry[] = [];
  const rejected: LibraryEntry[] = [];
  for (const r of input.reviews) {
    const s = summarizeReview(r);
    const entry: LibraryEntry = {
      label: r.targetLabel,
      type: r.targetType,
      score: s.score,
      reasons: [
        ...r.findings.filter((f) => f.bloqueante).map((f) => f.hallazgo),
        ...r.findings.filter((f) => !f.bloqueante).map((f) => f.hallazgo),
      ].slice(0, 3),
    };
    if (s.verdict === 'aprobado') approved.push(entry);
    else if (s.verdict === 'rechazado') rejected.push(entry);
  }
  const counts = new Map<string, { text: string; count: number }>();
  const bump = (text: string) => {
    const k = norm(text);
    const cur = counts.get(k);
    if (cur) cur.count += 1;
    else counts.set(k, { text: text.trim(), count: 1 });
  };
  for (const a of input.copyAudits) for (const f of a.findings) bump(f.message);
  for (const p of input.pieces)
    for (const a of p.audits) for (const f of a.findings) bump(f.message);
  for (const r of input.reviews) for (const f of r.findings) bump(f.hallazgo);
  const recurring = [...counts.values()]
    .filter((x) => x.count >= 2)
    .sort((a, b) => b.count - a.count || a.text.localeCompare(b.text, 'es'))
    .slice(0, 10);
  const best = input.measures
    .flatMap((m) => (m.kind === 'resultado' && m.impressions >= MIN_SAMPLE ? [m] : []))
    .map((m) => ({
      label: m.label,
      ctr: ctr(m),
      conversion: conversionRate(m),
      impressions: m.impressions,
    }))
    .sort((a, b) => (b.ctr ?? -1) - (a.ctr ?? -1))
    .slice(0, 5);
  const experiments = input.measures.flatMap((m) =>
    m.kind === 'experimento' && m.conclusion ? [{ name: m.name, conclusion: m.conclusion }] : [],
  );
  return { approved, rejected, recurring, best, experiments };
}
