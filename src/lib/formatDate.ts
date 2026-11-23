/**
 * Fecha y hora legibles en la zona horaria del navegador (sin dependencias). Si el texto no es una fecha válida,
 * devuelve el texto original para no ocultar el dato. El atributo `dateTime` sigue llevando el valor exacto en UTC.
 */
export function formatLocalDateTime(iso: string, locale = 'es-MX'): string {
  const d = new Date(iso);
  if (Number.isNaN(d.getTime())) return iso;
  return new Intl.DateTimeFormat(locale, { dateStyle: 'medium', timeStyle: 'short' }).format(d);
}
