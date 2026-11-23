import ts from 'typescript';

/** Una ocupación de una API de red encontrada en el código fuente (analizada con el AST de TypeScript). */
export interface NetworkUse {
  readonly api: string;
  readonly line: number;
}

const GLOBAL_APIS = new Set([
  'fetch',
  'XMLHttpRequest',
  'WebSocket',
  'EventSource',
  'WebTransport',
]);
const GLOBAL_OBJECTS = new Set(['window', 'globalThis', 'self', 'top', 'parent', 'frames']);
/** Clientes HTTP / de tiempo real de terceros; AC1-01 prohíbe SDK de servidor y llamadas de red en `src/`. */
const NETWORK_MODULES =
  /^(axios|ky|got|node-fetch|isomorphic-fetch|cross-fetch|whatwg-fetch|superagent|socket\.io-client|ws|@supabase\/.*|@apollo\/client|graphql-request)(\/|$)/;

const nameOf = (n: ts.Node): string | null =>
  ts.isIdentifier(n) ? n.text : ts.isStringLiteralLike(n) ? n.text : null;

/**
 * Detecta usos de `fetch`, XHR, WebSocket, EventSource, WebTransport, `navigator.sendBeacon`, accesos a
 * través de `window`/`globalThis`/`self` (incluido `globalThis['fetch']`) y módulos de clientes de red.
 * No marca cadenas de texto, comentarios, nombres de propiedades propias ni referencias solo de tipo.
 */
export function findNetworkUses(source: string, fileName = 'file.tsx'): NetworkUse[] {
  const sf = ts.createSourceFile(fileName, source, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const out: NetworkUse[] = [];
  const line = (n: ts.Node) => sf.getLineAndCharacterOfPosition(n.getStart(sf)).line + 1;
  const add = (api: string, n: ts.Node) => out.push({ api, line: line(n) });

  const visit = (node: ts.Node): void => {
    if (ts.isPropertyAccessExpression(node) || ts.isElementAccessExpression(node)) {
      const obj = node.expression;
      const member = ts.isPropertyAccessExpression(node)
        ? nameOf(node.name)
        : nameOf(node.argumentExpression);
      if (ts.isIdentifier(obj) && member !== null) {
        if (GLOBAL_OBJECTS.has(obj.text) && GLOBAL_APIS.has(member))
          add(`${obj.text}.${member}`, node);
        if (obj.text === 'navigator' && member === 'sendBeacon') add('navigator.sendBeacon', node);
        if (GLOBAL_OBJECTS.has(obj.text) && member === 'navigator') {
          // window.navigator.sendBeacon se detecta en el nivel siguiente
        }
      }
      if (
        ts.isPropertyAccessExpression(obj) &&
        ts.isIdentifier(obj.expression) &&
        GLOBAL_OBJECTS.has(obj.expression.text) &&
        obj.name.text === 'navigator' &&
        member === 'sendBeacon'
      )
        add(`${obj.expression.text}.navigator.sendBeacon`, node);
    } else if (ts.isIdentifier(node) && GLOBAL_APIS.has(node.text)) {
      const p = node.parent;
      const isMemberName =
        (ts.isPropertyAccessExpression(p) && p.name === node) ||
        (ts.isPropertyAssignment(p) && p.name === node) ||
        (ts.isPropertySignature(p) && p.name === node) ||
        (ts.isMethodDeclaration(p) && p.name === node) ||
        (ts.isPropertyDeclaration(p) && p.name === node);
      const isTypeOnly = ts.isTypeReferenceNode(p) || ts.isTypeQueryNode(p);
      if (!isMemberName && !isTypeOnly) add(node.text, node);
    } else if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)) {
      if (NETWORK_MODULES.test(node.moduleSpecifier.text))
        add(`módulo:${node.moduleSpecifier.text}`, node);
    } else if (ts.isCallExpression(node)) {
      const isDynamic = node.expression.kind === ts.SyntaxKind.ImportKeyword;
      const isRequire = ts.isIdentifier(node.expression) && node.expression.text === 'require';
      const arg = node.arguments[0];
      if (
        (isDynamic || isRequire) &&
        arg &&
        ts.isStringLiteralLike(arg) &&
        NETWORK_MODULES.test(arg.text)
      )
        add(`módulo:${arg.text}`, node);
    }
    ts.forEachChild(node, visit);
  };
  visit(sf);
  return out;
}
