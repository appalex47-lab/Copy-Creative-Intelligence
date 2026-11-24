/** Lector de CSV (S4.2) para importar resultados y promociones. Acepta coma o punto y coma, comillas y BOM. */
export function parseCsv(
  text: string,
): { readonly header: readonly string[]; readonly rows: readonly (readonly string[])[] } | null {
  const src = text.replace(/^\uFEFF/, '');
  const firstLine = src.split(/\r?\n/, 1)[0] ?? '';
  const delim = firstLine.includes(';') && !firstLine.includes(',') ? ';' : ',';
  const rows: string[][] = [];
  let row: string[] = [];
  let cell = '';
  let quoted = false;
  for (let i = 0; i < src.length; i++) {
    const c = src[i] ?? '';
    if (quoted) {
      if (c === '"' && src[i + 1] === '"') {
        cell += '"';
        i++;
      } else if (c === '"') quoted = false;
      else cell += c;
    } else if (c === '"') quoted = true;
    else if (c === delim) {
      row.push(cell);
      cell = '';
    } else if (c === '\n' || c === '\r') {
      if (c === '\r' && src[i + 1] === '\n') i++;
      row.push(cell);
      cell = '';
      if (row.some((x) => x.trim() !== '')) rows.push(row);
      row = [];
    } else cell += c;
  }
  if (quoted) return null;
  row.push(cell);
  if (row.some((x) => x.trim() !== '')) rows.push(row);
  const [header, ...rest] = rows;
  if (!header) return null;
  return { header: header.map((h) => h.trim().toLowerCase()), rows: rest };
}

/** Busca una columna por varios nombres posibles; -1 si no existe. */
export const columnIndex = (header: readonly string[], ...names: string[]): number =>
  header.findIndex((h) => names.includes(h));
