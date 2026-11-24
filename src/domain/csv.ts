/**
 * CSV para Excel (S3.5). Protege contra inyección de fórmulas: una celda que empiece con = + - @ o tabulador se
 * antepone con una comilla simple. Se agrega BOM UTF-8 para que Excel respete acentos. Separador: coma.
 */
export function csvCell(value: string | number | boolean): string {
  let s = String(value);
  if (/^[=+\-@\t\r]/.test(s) && typeof value === 'string') s = `'${s}`;
  return /[",\n\r]/.test(s) ? `"${s.replaceAll('"', '""')}"` : s;
}

export function toCsv(
  header: readonly string[],
  rows: readonly (readonly (string | number | boolean)[])[],
): string {
  const line = (r: readonly (string | number | boolean)[]) => r.map(csvCell).join(',');
  return `\uFEFF${[header, ...rows].map(line).join('\r\n')}\r\n`;
}
