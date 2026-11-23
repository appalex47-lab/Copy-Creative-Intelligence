import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import ts from 'typescript';
import { describe, expect, it } from 'vitest';

// AC1-06: IndexedDB solo se usa desde el adaptador (`src/adapters/indexeddb/`). Prueba por AST.
const SRC = join(process.cwd(), 'src');
const files = (dir: string): string[] =>
  readdirSync(dir).flatMap((e) => {
    const p = join(dir, e);
    return statSync(p).isDirectory() ? files(p) : [p];
  });
const sources = files(SRC).filter((p) => /\.(ts|tsx)$/.test(p) && !/\.test\.tsx?$/.test(p));
const NAMES = new Set([
  'indexedDB',
  'IDBDatabase',
  'IDBFactory',
  'IDBObjectStore',
  'IDBTransaction',
  'IDBKeyRange',
]);

export function usesIndexedDb(source: string): string[] {
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

describe('AC1-06: IndexedDB solo mediante el adaptador', () => {
  it('el detector encuentra usos directos y por window/globalThis', () => {
    expect(usesIndexedDb('indexedDB.open("x")')).toEqual(['indexedDB']);
    expect(usesIndexedDb('let d: IDBDatabase; window.indexedDB.open("x")')).toEqual([
      'IDBDatabase',
      'indexedDB',
    ]);
    expect(usesIndexedDb('const o = { indexedDB: 1 }; o.indexedDB;')).toEqual(['indexedDB']);
  });
  it('ningún archivo de src fuera de adapters/indexeddb referencia IndexedDB', () => {
    const offenders = sources
      .filter((p) => !relative(SRC, p).split('\\').join('/').startsWith('adapters/indexeddb/'))
      .flatMap((p) =>
        usesIndexedDb(readFileSync(p, 'utf8')).map((n) => `${relative(SRC, p)}: ${n}`),
      );
    expect(offenders).toEqual([]);
  });
  it('el adaptador sí usa IndexedDB (control de que el recorrido no está vacío)', () => {
    const own = sources.filter((p) =>
      relative(SRC, p).split('\\').join('/').startsWith('adapters/indexeddb/'),
    );
    expect(own.length).toBeGreaterThan(0);
    expect(own.some((p) => usesIndexedDb(readFileSync(p, 'utf8')).length > 0)).toBe(true);
  });
});
