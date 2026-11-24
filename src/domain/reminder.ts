/** Recordatorio semanal (S4.2): corresponde si la última revisión o auditoría tiene más de 7 días, o no existe ninguna. */
export const REMINDER_DAYS = 7;

export function isReviewDue(timestamps: readonly string[], now: Date): boolean {
  const times = timestamps.map((t) => Date.parse(t)).filter((n) => !Number.isNaN(n));
  if (times.length === 0) return true;
  return now.getTime() - Math.max(...times) > REMINDER_DAYS * 24 * 3600 * 1000;
}
