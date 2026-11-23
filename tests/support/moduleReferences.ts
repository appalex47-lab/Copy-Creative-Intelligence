import ts from 'typescript';

/** Una referencia a un módulo encontrada en el código fuente (analizada con el AST de TypeScript). */
export interface ModuleReference {
  readonly kind:
    'import' | 'export-from' | 'dynamic-import' | 'require' | 'import-type' | 'literal';
  /** Especificador resuelto estáticamente, o null si no pudo determinarse. */
  readonly specifier: string | null;
}

/** Resuelve un especificador estático: literales, plantillas sin expresiones, concatenaciones y `as`. */
function resolveStatic(node: ts.Expression): string | null {
  if (ts.isStringLiteral(node) || ts.isNoSubstitutionTemplateLiteral(node)) return node.text;
  if (
    ts.isParenthesizedExpression(node) ||
    ts.isAsExpression(node) ||
    ts.isSatisfiesExpression(node)
  )
    return resolveStatic(node.expression);
  if (ts.isBinaryExpression(node) && node.operatorToken.kind === ts.SyntaxKind.PlusToken) {
    const l = resolveStatic(node.left);
    const r = resolveStatic(node.right);
    return l !== null && r !== null ? l + r : null;
  }
  if (ts.isTemplateExpression(node)) {
    let out = node.head.text;
    for (const span of node.templateSpans) {
      const v = resolveStatic(span.expression);
      if (v === null) return null;
      out += v + span.literal.text;
    }
    return out;
  }
  return null;
}

/** Texto estático parcial (prefijo) de una expresión no resoluble; sirve para detectar `@supabase/${x}`. */
function staticPrefix(node: ts.Expression): string {
  if (ts.isTemplateExpression(node)) return node.head.text;
  if (ts.isBinaryExpression(node) && node.operatorToken.kind === ts.SyntaxKind.PlusToken)
    return resolveStatic(node.left) ?? staticPrefix(node.left);
  return '';
}

export function findModuleReferences(source: string, fileName = 'file.tsx'): ModuleReference[] {
  const sf = ts.createSourceFile(fileName, source, ts.ScriptTarget.Latest, true, ts.ScriptKind.TSX);
  const refs: ModuleReference[] = [];
  const consumed = new Set<ts.Node>(); // literales ya reportados como import/export/require
  const add = (kind: ModuleReference['kind'], specifier: string | null) =>
    refs.push({ kind, specifier });

  const visit = (node: ts.Node): void => {
    if (ts.isImportDeclaration(node) && ts.isStringLiteral(node.moduleSpecifier)) {
      consumed.add(node.moduleSpecifier);
      add('import', node.moduleSpecifier.text);
    } else if (
      ts.isExportDeclaration(node) &&
      node.moduleSpecifier &&
      ts.isStringLiteral(node.moduleSpecifier)
    ) {
      consumed.add(node.moduleSpecifier);
      add('export-from', node.moduleSpecifier.text);
    } else if (
      ts.isImportEqualsDeclaration(node) &&
      ts.isExternalModuleReference(node.moduleReference) &&
      ts.isStringLiteral(node.moduleReference.expression)
    ) {
      consumed.add(node.moduleReference.expression);
      add('require', node.moduleReference.expression.text);
    } else if (ts.isCallExpression(node)) {
      const isDynamic = node.expression.kind === ts.SyntaxKind.ImportKeyword;
      const isRequire = ts.isIdentifier(node.expression) && node.expression.text === 'require';
      const arg = node.arguments[0];
      if ((isDynamic || isRequire) && arg) {
        // Si no se resuelve, se conserva el prefijo estático conocido (p. ej. "@supabase/") para el análisis.
        consumed.add(arg);
        const spec = resolveStatic(arg) ?? (staticPrefix(arg) || null);
        add(isDynamic ? 'dynamic-import' : 'require', spec);
      }
    } else if (
      ts.isImportTypeNode(node) &&
      ts.isLiteralTypeNode(node.argument) &&
      ts.isStringLiteral(node.argument.literal)
    ) {
      consumed.add(node.argument.literal);
      add('import-type', node.argument.literal.text);
    } else if (ts.isStringLiteral(node) && !consumed.has(node) && /^@supabase\//.test(node.text)) {
      // Cualquier literal con forma de módulo Supabase (p. ej. pasado a una función o guardado en una variable).
      add('literal', node.text);
    }
    ts.forEachChild(node, visit);
  };
  visit(sf);
  return refs;
}

const isSupabase = (s: string) => /supabase/i.test(s);

export interface Violation {
  readonly reason: string;
  readonly ref: ModuleReference;
}

export interface Policy {
  /** Ruta relativa a src/ del archivo analizado, con separador "/". */
  readonly fileRel: string;
}

/** Normaliza un especificador relativo/alias a una ruta relativa a src/ (o null si es externo). */
function toSrcPath(specifier: string, fileRel: string): string | null {
  if (specifier.startsWith('@/')) return specifier.slice(2);
  if (specifier.startsWith('.')) {
    const parts = fileRel.split('/').slice(0, -1);
    for (const seg of specifier.split('/')) {
      if (seg === '.' || seg === '') continue;
      if (seg === '..') parts.pop();
      else parts.push(seg);
    }
    return parts.join('/');
  }
  return null;
}

const UI_LAYERS = ['domain/', 'components/', 'layouts/', 'pages/', 'hooks/', 'services/contracts/'];
const SUPABASE_ADAPTER = 'services/adapters/supabase/';

/**
 * Reglas de arquitectura:
 *  - Solo `src/services/adapters/supabase/` (futuro, aún inexistente) puede referenciar Supabase.
 *  - La interfaz (domain, components, layouts, pages, hooks, contratos) no puede importar adaptadores,
 *    la fábrica `services/index` ni usar imports dinámicos no resolubles estáticamente.
 *  - La raíz de composición (src/app) no importa adaptadores directamente.
 *  - El dominio no importa otras capas; los contratos solo importan dominio y contratos.
 */
export function checkFile(source: string, { fileRel }: Policy): Violation[] {
  const out: Violation[] = [];
  const inSupabaseAdapter = fileRel.startsWith(SUPABASE_ADAPTER);
  const isUi = UI_LAYERS.some((l) => fileRel.startsWith(l));
  const isApp = fileRel.startsWith('app/');
  const isDomain = fileRel.startsWith('domain/');
  const isContracts = fileRel.startsWith('services/contracts/');
  for (const ref of findModuleReferences(source, fileRel)) {
    const spec = ref.specifier;
    if (spec !== null && isSupabase(spec) && !inSupabaseAdapter) {
      out.push({ reason: 'referencia a Supabase fuera de su adaptador', ref });
      continue;
    }
    if (isUi) {
      const dynamic = ref.kind === 'dynamic-import' || ref.kind === 'require';
      if (dynamic && spec === null) {
        out.push({
          reason: 'import dinámico no resoluble estáticamente en la capa de interfaz',
          ref,
        });
        continue;
      }
      const target = spec === null ? null : toSrcPath(spec, fileRel);
      if (
        target !== null &&
        (target.startsWith('services/adapters') ||
          target.startsWith('adapters/') ||
          target === 'adapters' ||
          target === 'services' ||
          target === 'services/index' ||
          target.startsWith('app/'))
      ) {
        out.push({
          reason: 'la interfaz depende de un adaptador, de la fábrica o de la raíz de composición',
          ref,
        });
      }
    }
    // Dirección de dependencias (S1.1): el dominio no depende de nada interno salvo de sí mismo,
    // y los contratos solo dependen del dominio y de otros contratos.
    if ((isDomain || isContracts) && spec !== null) {
      const target = toSrcPath(spec, fileRel);
      if (target !== null) {
        const allowed = isDomain
          ? target.startsWith('domain/') || target === 'domain'
          : target.startsWith('domain/') ||
            target === 'domain' ||
            target.startsWith('services/contracts');
        if (!allowed) {
          out.push({
            reason: isDomain
              ? 'el dominio depende de otra capa'
              : 'los contratos dependen de una capa distinta del dominio y los contratos',
            ref,
          });
        }
      }
    }
    if (isApp && spec !== null) {
      const target = toSrcPath(spec, fileRel);
      if (target?.startsWith('services/adapters')) {
        out.push({ reason: 'la raíz de composición importa un adaptador directamente', ref });
      }
    }
  }
  return out;
}
