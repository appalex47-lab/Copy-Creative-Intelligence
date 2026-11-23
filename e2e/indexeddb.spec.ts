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

test('el esquema vigente (v2) crea los almacenes, el índice por fecha y registra la versión', async ({
  page,
}) => {
  await page.goto(`${DEV}/e2e/idb.html`);
  const info = await page.evaluate(() => window.__schema());
  expect(info).toEqual({
    version: 2,
    stores: ['activity', 'meta', 'profile'],
    activityIndexes: ['at', 'kind'],
    schemaVersion: 2,
  });
});

const open = async (page: Page) => {
  await page.goto(`${DEV}/e2e/idb.html`);
  await page.waitForFunction(() => window.__idb?.done === true);
};

test.describe('migraciones (AC1-07) en IndexedDB real', () => {
  test('v0 → v2: una instalación nueva crea el esquema completo', async ({ page }) => {
    await open(page);
    expect(await page.evaluate(() => window.__mig.v0ToLatest())).toMatchObject({
      version: 2,
      stores: ['activity', 'meta', 'profile'],
      indexes: ['at', 'kind'],
      schemaVersion: 2,
      profile: undefined,
      ids: [],
    });
  });

  test('v1 → v2 con semillas: conserva los datos y añade el índice `kind`', async ({ page }) => {
    await open(page);
    const r = (await page.evaluate(() => window.__mig.v1ToV2WithSeeds())) as Record<
      string,
      unknown
    >;
    expect(r).toMatchObject({
      version: 2,
      indexes: ['at', 'kind'],
      schemaVersion: 2,
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
    expect(r).toMatchObject({ opened: false, version: 3, stores: ['sentinel'], val: 'intacto' });
    expect((r['error'] as { code: string; message: string }).message).toBe(r['expectedMessage']);
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
});
