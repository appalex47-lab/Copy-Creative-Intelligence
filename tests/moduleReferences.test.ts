import { describe, expect, it } from 'vitest';
import { checkFile, findModuleReferences } from './support/moduleReferences';

const specs = (code: string) => findModuleReferences(code).map((r) => `${r.kind}:${r.specifier}`);
const violations = (code: string, fileRel: string) =>
  checkFile(code, { fileRel }).map((v) => v.reason);

describe('findModuleReferences (AST)', () => {
  it('detecta imports estáticos, efectos laterales, export from, import type e import=', () => {
    expect(
      specs(`
        import a from '@supabase/supabase-js';
        import '@supabase/ssr';
        import type { T } from "@supabase/x";
        export * from '@supabase/y';
        export { z } from '@supabase/z';
        import q = require('@supabase/q');
        type U = import('@supabase/u').U;
      `),
    ).toEqual([
      'import:@supabase/supabase-js',
      'import:@supabase/ssr',
      'import:@supabase/x',
      'export-from:@supabase/y',
      'export-from:@supabase/z',
      'require:@supabase/q',
      'import-type:@supabase/u',
    ]);
  });

  it('detecta imports dinámicos literales, concatenados y con plantilla', () => {
    expect(
      specs(
        'await import("@supabase/a"); await import(`@supabase/b`); await import("@supa" + "base/c"); await import(`@supabase/${n}`); await import(name); const r = require("@supabase/d");',
      ),
    ).toEqual([
      'dynamic-import:@supabase/a',
      'dynamic-import:@supabase/b',
      'dynamic-import:@supabase/c',
      'dynamic-import:@supabase/',
      'dynamic-import:null',
      'require:@supabase/d',
    ]);
  });

  it('detecta literales con forma de módulo Supabase usados indirectamente', () => {
    expect(specs("const m = '@supabase/supabase-js'; load(m);")).toContain(
      'literal:@supabase/supabase-js',
    );
  });

  it('no confunde comentarios ni texto con imports (ventaja sobre regex)', () => {
    expect(specs("// import x from '@supabase/js'\nconst s = \"from '@supabase/js'\";")).toEqual(
      [],
    );
  });
});

describe('checkFile (reglas)', () => {
  const bad = [
    "import { createClient } from '@supabase/supabase-js';",
    "import '@supabase/ssr';",
    "const m = await import('@supabase/supabase-js');",
    "const m = await import('@supa' + 'base/supabase-js');",
    'const m = await import(`@supabase/${x}`);',
    "export * from '@supabase/js';",
  ];

  it.each([
    'pages/X.tsx',
    'components/X.tsx',
    'layouts/X.tsx',
    'hooks/x.ts',
    'domain/x.ts',
    'services/contracts/x.ts',
    'app/App.tsx',
    'services/adapters/demo/x.ts',
  ])('prohíbe Supabase (estático y dinámico) en %s', (file) => {
    for (const code of bad) expect(violations(code, file), code).not.toEqual([]);
  });

  it('permite Supabase únicamente dentro de su adaptador futuro', () => {
    for (const code of bad)
      expect(violations(code, 'services/adapters/supabase/client.ts')).toEqual([]);
  });

  it('la interfaz no puede importar adaptadores, la fábrica ni la raíz de composición (alias o relativo)', () => {
    for (const code of [
      "import { createDemoServices } from '@/services/adapters/demo/demoServices';",
      "import { createServices } from '@/services';",
      "import { createServices } from '@/services/index';",
      "import { x } from '../services/adapters/demo/fixtures';",
      "import { y } from '@/app/env';",
      "const m = await import('@/services/adapters/demo/demoServices');",
    ]) {
      expect(violations(code, 'pages/HomePage.tsx'), code).not.toEqual([]);
    }
  });

  it('la interfaz no puede usar imports dinámicos que no se resuelven estáticamente', () => {
    expect(violations('await import(someVariable);', 'components/X.tsx')).not.toEqual([]);
    expect(violations("await import('@/services/contracts');", 'components/X.tsx')).toEqual([]);
  });

  it('la raíz de composición puede usar la fábrica pero no un adaptador directo', () => {
    expect(violations("import { createServices } from '@/services';", 'app/App.tsx')).toEqual([]);
    expect(
      violations("import { d } from '@/services/adapters/demo/demoServices';", 'app/App.tsx'),
    ).not.toEqual([]);
  });

  it('las dependencias permitidas no generan falsos positivos', () => {
    expect(
      violations(
        "import { useServices } from '@/hooks/ServicesContext';\nimport type { Services } from '@/services/contracts';\nimport type { Project } from '@/domain/entities';\nimport { useState } from 'react';",
        'pages/HomePage.tsx',
      ),
    ).toEqual([]);
  });
});
