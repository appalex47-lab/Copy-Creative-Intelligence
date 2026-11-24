import type { CopyRecord } from './copy';
import type { MeasureRecord } from './measure';
import type { PieceRecord } from './piece';
import type { PromoRecord } from './promo';
import type { ReviewRecord } from './review';

/**
 * Tablero de control (S5.1): cuenta lo pendiente con lo ya guardado; no captura nada. «Sin revisar» = copys y piezas
 * sin ninguna revisión de calidad; «por liberar» = revisiones cuya aprobación final sigue pendiente; «liberadas» = con
 * aprobación final y nombre de quien aprueba. Promociones: vencidas (fecha final anterior a hoy) o por vencer (7 días).
 */
export interface Dashboard {
  readonly unreviewed: readonly string[];
  readonly toRelease: number;
  readonly released: number;
  readonly rejected: number;
  readonly promosExpired: readonly string[];
  readonly promosSoon: readonly string[];
  readonly measures: number;
}

export const SOON_DAYS = 7;

const addDays = (day: string, n: number): string => {
  const d = new Date(`${day}T00:00:00Z`);
  d.setUTCDate(d.getUTCDate() + n);
  return d.toISOString().slice(0, 10);
};

export function buildDashboard(input: {
  readonly copies: readonly CopyRecord[];
  readonly pieces: readonly PieceRecord[];
  readonly reviews: readonly ReviewRecord[];
  readonly promos: readonly PromoRecord[];
  readonly measures: readonly MeasureRecord[];
  /** AAAA-MM-DD. */
  readonly today: string;
}): Dashboard {
  const reviewed = new Set(input.reviews.map((r) => `${r.targetType}:${r.targetId}`));
  const unreviewed = [
    ...input.copies.filter((c) => !reviewed.has(`copy:${c.id}`)).map((c) => `Copy: ${c.label}`),
    ...input.pieces.filter((p) => !reviewed.has(`pieza:${p.id}`)).map((p) => `Pieza: ${p.name}`),
  ];
  const limit = addDays(input.today, SOON_DAYS);
  return {
    unreviewed,
    toRelease: input.reviews.filter((r) => r.finalApproval === 'pendiente').length,
    released: input.reviews.filter((r) => r.finalApproval === 'aprobado').length,
    rejected: input.reviews.filter((r) => r.finalApproval === 'rechazado').length,
    promosExpired: input.promos
      .filter((p) => p.to !== undefined && p.to < input.today)
      .map((p) => p.name),
    promosSoon: input.promos
      .filter((p) => p.to !== undefined && p.to >= input.today && p.to <= limit)
      .map((p) => p.name),
    measures: input.measures.length,
  };
}
