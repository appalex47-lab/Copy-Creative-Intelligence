import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import ts from 'typescript';
import { describe, expect, it } from 'vitest';

// AC1-07 (S1.6): Local Storage / Session Storage solo se usan desde `src/adapters/localstorage/`. Prueba por AST.
const SRC = join(process.cwd(), 'src');
const files = (dir: string): string[] =>
  readdirSync(dir).flatMap((e) => {
    const p = join(dir, e);
    return statSync(p).isDirectory() ? files(p) : [p];
  });
const sources = files(SRC).filter((p) => /\.(ts|tsx)$/.test(p) && !/\.test\.tsx?$/.test(p));
const NAMES = new Set(['localStorage', 'sessionStorage']);

export function usesWebStorage(source: string): string[] {
  const sf = ts.createSourceFile('f.tsx', source, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const out: string[] = [];
  const visit = (n: ts.Node): void => {
    if (ts.isIdentifier(n) && NAMES.has(n.text)) {
      const p = n.parent;
      const member =
        ts.isPropertyAccessExpression(p) &&
        p.name === n &&
        !(
          ts.isIdentifier(p.expression) &&
          ['window', 'globalThis', 'self'].includes(p.expression.text)
        );
      if (!member) out.push(n.text);
    }
    ts.forEachChild(n, visit);
  };
  visit(sf);
  return out;
}

describe('Local Storage solo mediante su adaptador', () => {
  it('el detector encuentra usos directos y por window/globalThis', () => {
    expect(usesWebStorage('localStorage.getItem("x")')).toEqual(['localStorage']);
    expect(usesWebStorage('window.sessionStorage.clear(); let s: Storage')).toEqual([
      'sessionStorage',
    ]);
    expect(usesWebStorage('const o = { localStorage: 1 }; o.localStorage;')).toEqual([
      'localStorage',
    ]);
  });
  it('ningún archivo de src fuera de adapters/localstorage referencia Local/Session Storage', () => {
    const offenders = sources
      .filter((p) => !relative(SRC, p).split('\\').join('/').startsWith('adapters/localstorage/'))
      .flatMap((p) =>
        usesWebStorage(readFileSync(p, 'utf8')).map((n) => `${relative(SRC, p)}: ${n}`),
      );
    expect(offenders).toEqual([]);
  });
  it('el adaptador sí usa Local Storage (control de que el recorrido no está vacío)', () => {
    const own = sources.filter((p) =>
      relative(SRC, p).split('\\').join('/').startsWith('adapters/localstorage/'),
    );
    expect(own.length).toBeGreaterThan(0);
    expect(own.some((p) => usesWebStorage(readFileSync(p, 'utf8')).length > 0)).toBe(true);
  });
});
