import { expect, test } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

test('respaldo completo: descarga un archivo con promociones y las restaura tras borrarlas', async ({
  page,
}, testInfo) => {
  const errors = trackErrors(page);
  await page.goto(LOCAL);
  await page.getByRole('button', { name: 'Promociones', exact: true }).click();
  await page.getByLabel('Archivo CSV de promociones').setInputFiles({
    name: 'p.csv',
    mimeType: 'text/csv',
    buffer: Buffer.from('nombre,porcentaje\nBuen Fin,20\n'),
  });
  await expect(page.getByText('Se importaron 1 promociones.')).toBeVisible();
  await page.getByRole('button', { name: 'Respaldo', exact: true }).click();
  expect(await axeViolations(page)).toEqual([]);
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Descargar todo en un archivo' }).click(),
  ]);
  const file = testInfo.outputPath('completo.json');
  await download.saveAs(file);
  await expect(page.getByText('Respaldo completo exportado')).toBeVisible();

  await page.getByRole('button', { name: 'Promociones', exact: true }).click();
  await page.getByRole('button', { name: 'Eliminar Buen Fin' }).click();
  await expect(page.getByText('Aún no hay promociones')).toBeVisible();

  await page.getByRole('button', { name: 'Respaldo', exact: true }).click();
  await page.getByLabel('Archivo con todo (.json)').setInputFiles(file);
  await page.getByRole('button', { name: 'Restaurar todo desde el archivo' }).click();
  await expect(page.getByText('Respaldo completo importado')).toContainText('1 promociones');
  await page.getByRole('button', { name: 'Promociones', exact: true }).click();
  await expect(page.getByRole('list', { name: 'Promociones guardadas' })).toContainText('Buen Fin');
  expect(errors).toEqual([]);
});
