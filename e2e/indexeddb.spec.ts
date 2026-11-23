import { expect, test } from '@playwright/test';
import { DEV } from './support';

// AC1-06: el contrato de repositorios se cumple en IndexedDB REAL (Chrome), no solo en memoria.
test('repositorios sobre IndexedDB real cumplen el mismo contrato que los de memoria', async ({
  page,
}) => {
  await page.goto(`${DEV}/e2e/idb.html`);
  await page.waitForFunction(() => window.__idb?.done === true);
  expect(await page.evaluate(() => window.__idb.failures)).toEqual([]);
});

test('el esquema v1 crea los almacenes, el índice por fecha y registra la versión', async ({
  page,
}) => {
  await page.goto(`${DEV}/e2e/idb.html`);
  const info = await page.evaluate(() => window.__schema());
  expect(info).toEqual({
    version: 1,
    stores: ['activity', 'meta', 'profile'],
    activityIndexes: ['at'],
    schemaVersion: 1,
  });
});
