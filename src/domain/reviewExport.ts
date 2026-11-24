import { toCsv } from './csv';
import {
  FINAL_LABELS,
  STAGE_LABELS,
  VERDICT_LABELS,
  summarizeReview,
  type ReviewRecord,
} from './review';

/** Revisiones de calidad: una fila por revisión, con puntaje, veredicto, etapa, aprobación final y quién aprobó. */
export function reviewsCsv(reviews: readonly ReviewRecord[]): string {
  return toCsv(
    [
      'Actualizada',
      'Objetivo',
      'Tipo',
      'Puntaje',
      'Veredicto',
      'Filtro creativo',
      'Filtro comercial',
      'Hallazgos',
      'Bloqueantes',
      'Etapa',
      'Aprobación final',
      'Quién revisa',
      'Quién aprueba',
    ],
    reviews.map((r) => {
      const s = summarizeReview(r);
      return [
        r.updatedAt,
        r.targetLabel,
        r.targetType,
        s.score ?? '',
        VERDICT_LABELS[s.verdict],
        r.creativeFilter,
        r.commercialFilter,
        r.findings.length,
        s.blocking,
        STAGE_LABELS[r.stage],
        FINAL_LABELS[r.finalApproval],
        r.reviewer ?? '',
        r.approver ?? '',
      ];
    }),
  );
}
