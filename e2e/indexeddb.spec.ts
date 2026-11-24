import { expect, test, type Page } from '@playwright/test';
import { DEV } from './support';

// AC1-06: el contrato de repositorios se cumple en IndexedDB REAL (Chrome), no solo en memoria.
test('repositorios sobre IndexedDB real cumplen el mismo contrato que los de memoria', async ({
  page,
}) => {
  await page.goto(`${DEV}/e2e/idb.html`);
  await page.waitForFunction(() => window.__idb?.done === true);
  expect(await page.evaluate(() => window.__idb.failures)).toEqual([]);
});

test('el esquema vigente (v7) crea los almacenes, el índice por fecha y registra la versión', async ({
  page,
}) => {
  await page.goto(`${DEV}/e2e/idb.html`);
  const info = await page.evaluate(() => window.__schema());
  expect(info).toEqual({
    version: 11,
    stores: [
      'activity',
      'adaptations',
      'audits',
      'briefs',
      'copies',
      'entities',
      'measures',
      'meta',
      'pieces',
      'profile',
      'promos',
      'resources',
      'reviews',
      'rules',
    ],
    activityIndexes: ['at', 'kind'],
    schemaVersion: 11,
  });
});

const open = async (page: Page) => {
  await page.goto(`${DEV}/e2e/idb.html`);
  await page.waitForFunction(() => window.__idb?.done === true);
};

test.describe('migraciones (AC1-07) en IndexedDB real', () => {
  test('v0 → v11: una instalación nueva crea el esquema completo', async ({ page }) => {
    await open(page);
    expect(await page.evaluate(() => window.__mig.v0ToLatest())).toMatchObject({
      version: 11,
      stores: [
        'activity',
        'adaptations',
        'audits',
        'briefs',
        'copies',
        'entities',
        'measures',
        'meta',
        'pieces',
        'profile',
        'promos',
        'resources',
        'reviews',
        'rules',
      ],
      indexes: ['at', 'kind'],
      schemaVersion: 11,
      profile: undefined,
      ids: [],
    });
  });

  test('v1 → v7 con semillas: conserva los datos, añade el índice `kind` y el almacenes de briefs y copys', async ({
    page,
  }) => {
    await open(page);
    const r = (await page.evaluate(() => window.__mig.v1ToV2WithSeeds())) as Record<
      string,
      unknown
    >;
    expect(r).toMatchObject({
      version: 11,
      indexes: ['at', 'kind'],
      schemaVersion: 11,
      profile: { displayName: 'Ana' },
      ids: ['evt_seed0001', 'evt_seed0002'],
      byKind: ['evt_seed0002'],
    });
    expect((r['viaRepo'] as { value: { id: string }[] }).value.map((e) => e.id)).toEqual([
      'evt_seed0002',
      'evt_seed0001',
    ]);
  });

  test('una base de versión mayor se rechaza SIN escribir', async ({ page }) => {
    await open(page);
    const r = (await page.evaluate(() => window.__mig.newerVersionRejected())) as Record<
      string,
      unknown
    >;
    expect(r).toMatchObject({ opened: false, version: 12, stores: ['sentinel'], val: 'intacto' });
    expect((r['error'] as { code: string; message: string }).message).toBe(r['expectedMessage']);
    expect((r['error'] as { code: string }).code).toBe('storage_newer_schema');
  });

  test('una migración que falla se revierte: versión, índices y datos quedan como antes', async ({
    page,
  }) => {
    await open(page);
    expect(await page.evaluate(() => window.__mig.failingMigrationRollsBack())).toEqual({
      opened: false,
      version: 1,
      indexes: ['at'],
      ids: ['evt_seed0001', 'evt_seed0002'],
      schemaVersion: 1,
    });
  });

  test('catálogo de errores: otra conexión abierta → storage_blocked; migración fallida → storage_failed', async ({
    page,
  }) => {
    await open(page);
    expect(await page.evaluate(() => window.__mig.blockedByOtherConnection())).toEqual({
      opened: false,
      code: 'storage_blocked',
    });
    expect(await page.evaluate(() => window.__mig.failingMigrationCode())).toEqual({
      opened: false,
      code: 'storage_failed',
    });
  });

  test('respaldo (AC1-12): reemplazo correcto; y una escritura que falla a mitad aborta TODO sin estado parcial', async ({
    page,
  }) => {
    await open(page);
    expect(await page.evaluate(() => window.__backup.replaceThenExport())).toEqual({
      ok: true,
      after: { profile: {}, ids: ['evt_00000009'] },
    });
    const r = (await page.evaluate(() => window.__backup.atomicReplaceAborts())) as {
      result: { ok: boolean; error: { code: string } };
      puts: number;
      after: unknown;
    };
    expect(r.result.ok).toBe(false);
    expect(r.puts).toBe(3); // falló en la tercera escritura, a mitad de la sustitución
    expect(r.after).toEqual({
      profile: { displayName: 'Ana' },
      ids: ['evt_00000002', 'evt_00000001'],
    });
  });
});
