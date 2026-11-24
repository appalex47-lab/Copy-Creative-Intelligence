import { normalize } from './copyRules';
import type { Channel } from './brief';
import type { AuditRecord } from './audit';
import type { Verdict } from './copyRules';

/** Filtros de la consulta global de auditorías (S3.2). Vacío = sin filtrar por ese criterio. */
export interface AuditFilter {
  readonly verdict?: Verdict;
  readonly channel?: Channel;
  /** Fechas locales YYYY-MM-DD, ambas inclusive. */
  readonly from?: string;
  readonly to?: string;
  readonly query?: string;
}

/** YYYY-MM-DD en la zona local del navegador. */
export function localDay(iso: string): string {
  const d = new Date(iso);
  const p = (n: number) => String(n).padStart(2, '0');
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())}`;
}

export function filterAudits(list: readonly AuditRecord[], f: AuditFilter): AuditRecord[] {
  const words = normalize(f.query ?? '')
    .split(/\s+/)
    .filter(Boolean);
  return list.filter((a) => {
    if (f.verdict && a.verdict !== f.verdict) return false;
    if (f.channel && a.channel !== f.channel) return false;
    const day = localDay(a.createdAt);
    if (f.from && day < f.from) return false;
    if (f.to && day > f.to) return false;
    if (words.length > 0) {
      const hay = normalize([a.targetLabel, ...a.findings.map((x) => x.message)].join(' \n '));
      if (!words.every((w) => hay.includes(w))) return false;
    }
    return true;
  });
}
