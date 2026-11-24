import type { AuditRecord } from './audit';
import { CATEGORY_LABELS, SEVERITY_LABELS, type Verdict } from './copyRules';
import { toCsv } from './csv';
import { ORIGIN_LABELS, STATUS_LABELS, type PieceRecord } from './piece';

const VERDICT: Readonly<Record<Verdict, string>> = {
  apto: 'Apto',
  revisar: 'Revisar',
  no_apto: 'No apto',
};

/** Auditorías de copy: una fila por hallazgo (o una fila sin hallazgo). */
export function copyAuditsCsv(audits: readonly AuditRecord[]): string {
  const rows = audits.flatMap((a) => {
    const base = [
      a.createdAt,
      a.targetLabel,
      a.sourceVersion,
      a.channel,
      a.score,
      VERDICT[a.verdict],
    ];
    return a.findings.length === 0
      ? [[...base, '', '', '']]
      : a.findings.map((f) => [
          ...base,
          SEVERITY_LABELS[f.severity],
          CATEGORY_LABELS[f.category],
          f.message,
        ]);
  });
  return toCsv(
    [
      'Fecha (UTC)',
      'Copy',
      'Versión',
      'Canal',
      'Puntaje',
      'Resultado',
      'Severidad',
      'Categoría',
      'Hallazgo',
    ],
    rows,
  );
}

/** Auditorías de piezas: una fila por hallazgo, con origen, estado y nota. */
export function pieceAuditsCsv(pieces: readonly PieceRecord[]): string {
  const rows = pieces.flatMap((p) =>
    p.audits.flatMap((a) => {
      const base = [
        a.createdAt,
        p.name,
        p.channel,
        a.textSource === 'validado' ? 'validado por persona' : 'detectado por OCR',
        a.score,
        VERDICT[a.verdict],
      ];
      return a.findings.length === 0
        ? [[...base, '', '', '', '', '', '']]
        : a.findings.map((f) => [
            ...base,
            SEVERITY_LABELS[f.severity],
            CATEGORY_LABELS[f.category],
            ORIGIN_LABELS[f.origin],
            STATUS_LABELS[f.status],
            f.note ?? '',
            f.message,
          ]);
    }),
  );
  return toCsv(
    [
      'Fecha (UTC)',
      'Pieza',
      'Canal',
      'Texto auditado',
      'Puntaje',
      'Resultado',
      'Severidad',
      'Categoría',
      'Origen',
      'Estado',
      'Nota',
      'Hallazgo',
    ],
    rows,
  );
}
