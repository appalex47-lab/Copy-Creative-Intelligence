import { readdirSync, readFileSync, statSync } from 'node:fs';
import { join, relative } from 'node:path';
import { describe, expect, it } from 'vitest';
import { findNetworkUses } from './support/networkApis';

const apis = (code: string) => findNetworkUses(code).map((u) => u.api);

describe('findNetworkUses (AST) — detector de APIs de red', () => {
  it('detecta fetch, XHR, WebSocket, EventSource y WebTransport', () => {
    expect(
      apis(`
        await fetch('/x');
        const x = new XMLHttpRequest();
        const w = new WebSocket('wss://a');
        const e = new EventSource('/s');
        const t = new WebTransport('https://a');
      `),
    ).toEqual(['fetch', 'XMLHttpRequest', 'WebSocket', 'EventSource', 'WebTransport']);
  });

  it('detecta accesos mediante window/globalThis/self, también con corchetes', () => {
    expect(
      apis(
        `window.fetch('/a'); globalThis['fetch']('/b'); self.WebSocket; new window.XMLHttpRequest();`,
      ),
    ).toEqual(['window.fetch', 'globalThis.fetch', 'self.WebSocket', 'window.XMLHttpRequest']);
  });

  it('detecta navigator.sendBeacon y window.navigator.sendBeacon', () => {
    expect(apis(`navigator.sendBeacon('/b'); window.navigator.sendBeacon('/c');`)).toEqual([
      'navigator.sendBeacon',
      'window.navigator.sendBeacon',
    ]);
  });

  it('detecta una referencia por alias (const f = fetch)', () => {
    expect(apis(`const f = fetch; f('/x');`)).toEqual(['fetch']);
  });

  it('detecta módulos de clientes de red e imports dinámicos literales', () => {
    expect(
      apis(
        `import a from 'axios'; import s from 'socket.io-client'; await import('ky'); require('ws');`,
      ),
    ).toEqual(['módulo:axios', 'módulo:socket.io-client', 'módulo:ky', 'módulo:ws']);
  });

  it('no marca cadenas, comentarios, propiedades propias ni referencias solo de tipo', () => {
    expect(
      apis(`
        // fetch('/x') en un comentario
        const texto = 'fetch(/x) y new WebSocket()';
        const o = { fetch: 1, WebSocket: 2 };
        o.fetch; o.WebSocket;
        type T = WebSocket;
        interface I { fetch: () => void }
        import { useState } from 'react';
      `),
    ).toEqual([]);
  });
});

describe('AC1-01: src/ no usa APIs de red ni clientes de servidor (prueba por AST)', () => {
  const SRC = join(process.cwd(), 'src');
  const files = (dir: string): string[] =>
    readdirSync(dir).flatMap((e) => {
      const p = join(dir, e);
      return statSync(p).isDirectory() ? files(p) : [p];
    });
  const sources = files(SRC).filter((p) => /\.(ts|tsx)$/.test(p) && !/\.test\.tsx?$/.test(p));

  it('el recorrido no está vacío', () => {
    expect(sources.length).toBeGreaterThan(10);
  });

  it('ningún archivo de src usa fetch, XHR, WebSocket, EventSource, sendBeacon ni clientes de red', () => {
    const offenders = sources.flatMap((p) =>
      findNetworkUses(readFileSync(p, 'utf8'), p).map(
        (u) => `${relative(SRC, p).split('\\').join('/')}:${u.line} ${u.api}`,
      ),
    );
    expect(offenders).toEqual([]);
  });
});
