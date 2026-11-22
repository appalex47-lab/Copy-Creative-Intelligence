import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { describe, expect, it } from 'vitest';
import { checkFile } from './support/moduleReferences';

const SRC = join(process.cwd(), 'src');
function files(dir: string): string[] {
  return readdirSync(dir).flatMap((e) => {
    const p = join(dir, e);
    return statSync(p).isDirectory() ? files(p) : [p];
  });
}
const read = (p: string) => readFileSync(p, 'utf8');
const isTest = (p: string) => /\.test\.tsx?$/.test(p);

describe('contratos desacoplados de proveedores (análisis por AST)', () => {
  const sources = files(SRC).filter((p) => !isTest(p));
  const rel = (p: string) => relative(SRC, p).split('\\').join('/');

  it('ningún archivo de src viola las reglas de arquitectura', () => {
    const offenders = sources.flatMap((p) =>
      checkFile(read(p), { fileRel: rel(p) }).map((v) => `${rel(p)}: ${v.reason}`),
    );
    expect(offenders).toEqual([]);
  });

  it('el análisis cubre las capas esperadas (control de que el recorrido no está vacío)', () => {
    const layers = [
      'domain',
      'components',
      'layouts',
      'pages',
      'hooks',
      'services/contracts',
      'app',
    ];
    for (const l of layers) expect(sources.some((p) => rel(p).startsWith(`${l}/`))).toBe(true);
  });

  it('el paquete no declara dependencias de Supabase en esta fase', () => {
    const pkg = JSON.parse(read(join(process.cwd(), 'package.json'))) as Record<
      string,
      Record<string, string>
    >;
    const all = { ...pkg['dependencies'], ...pkg['devDependencies'] };
    expect(Object.keys(all).filter((d) => /supabase/i.test(d))).toEqual([]);
  });
});
