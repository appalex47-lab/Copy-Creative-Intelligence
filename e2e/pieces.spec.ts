import { readFileSync } from 'node:fs';
import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

const nav = async (page: Page, name: string) => {
  await page.getByRole('button', { name, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name })).toBeFocused();
};

async function png(page: Page): Promise<Buffer> {
  const url = await page.evaluate(() => {
    const c = document.createElement('canvas');
    c.width = 800;
    c.height = 300;
    const g = c.getContext('2d');
    if (!g) throw new Error('canvas');
    g.fillStyle = '#fff';
    g.fillRect(0, 0, 800, 300);
    return c.toDataURL('image/png');
  });
  return Buffer.from(url.split(',')[1] ?? '', 'base64');
}

test.describe('piezas creativas (modo local, Chrome real)', () => {
  test('crear, auditar, resolver un hallazgo, comparar, respaldar y proteger la imagen', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Recursos');
    await page.getByLabel('Agregar imagen').setInputFiles({
      name: 'promo.png',
      mimeType: 'image/png',
      buffer: await png(page),
    });
    await expect(page.getByRole('list', { name: 'Recursos guardados' })).toContainText('promo.png');
    await page.getByLabel('Texto confirmado de la imagen').fill('Una cura para todo');
    await page.getByRole('button', { name: 'Guardar texto validado' }).click();
    await expect(
      page.getByRole('status').filter({ hasText: 'Texto validado guardado' }),
    ).toBeVisible();

    await nav(page, 'Piezas');
    await expect(page.getByText('Aún no hay piezas')).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);
    await page.getByLabel('Nombre de la pieza').fill('Promo email');
    await page.getByLabel('Canal').selectOption('Email');
    await page.getByLabel('Imagen (de Recursos)').selectOption({ label: 'promo.png' });
    await page.getByRole('button', { name: 'Crear pieza' }).click();
    const card = page.getByRole('list', { name: 'Piezas creativas' });
    await expect(card).toContainText('Promo email');

    await page.getByRole('button', { name: 'Auditar pieza Promo email' }).click();
    await expect(card).toContainText('validado por persona');
    await expect(card).toContainText('«cura»');
    await expect(card).toContainText('origen: regla determinista');
    expect(await axeViolations(page)).toEqual([]);

    await page.getByLabel('Nota del hallazgo 1').fill('Se cambia el texto');
    await page.getByLabel('Estado del hallazgo 1').selectOption('resuelto');
    await expect(card).toContainText('Resuelto el');

    // Persiste; una segunda auditoría se compara con la primera.
    await page.reload();
    await nav(page, 'Piezas');
    await expect(page.getByLabel('Estado del hallazgo 1')).toHaveValue('resuelto');
    await expect(page.getByLabel('Nota del hallazgo 1')).toHaveValue('Se cambia el texto');
    await page.getByRole('button', { name: 'Auditar pieza Promo email' }).click();
    await expect(card).toContainText('Frente a la auditoría anterior');
    await expect(card).toContainText('2 auditorías guardadas');

    // Exportación CSV: una fila por hallazgo, con origen y estado.
    const csvDl = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Descargar CSV de auditorías de piezas' }).click();
    const csvFile = await csvDl;
    expect(csvFile.suggestedFilename()).toMatch(/^cci-piezas-\d{4}-\d{2}-\d{2}\.csv$/);
    const csv = readFileSync((await csvFile.path()) ?? '', 'utf8');
    expect(csv).toContain('Promo email');
    expect(csv).toContain('regla determinista');
    expect(csv).toContain('Resuelto');

    // La imagen en uso no se puede eliminar.
    await nav(page, 'Recursos');
    await page.getByRole('button', { name: 'Eliminar recurso promo.png' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar recurso' }).click();
    await expect(page.getByRole('alert')).toContainText('la usa una pieza creativa');

    // El respaldo de datos avisa lo que no incluye.
    await nav(page, 'Respaldo');
    await expect(page.getByRole('note')).toContainText('NO incluye');
    await expect(page.getByRole('note')).toContainText('1 imágenes');
    await expect(page.getByRole('note')).toContainText('1 piezas');

    // Respaldo de imágenes con piezas: se descarga, se borra todo y se restaura.
    await nav(page, 'Recursos');
    const dl = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Descargar respaldo de imágenes' }).click();
    const path = await (await dl).path();
    await nav(page, 'Piezas');
    await page.getByRole('button', { name: 'Eliminar pieza Promo email' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar pieza' }).click();
    await expect(page.getByText('Aún no hay piezas')).toBeVisible();
    await nav(page, 'Recursos');
    await page.getByRole('button', { name: 'Eliminar recurso promo.png' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar recurso' }).click();
    await page.getByLabel('Restaurar respaldo de imágenes').setInputFiles(path);
    await expect(page.getByText('Piezas restauradas: 1')).toBeVisible();
    await nav(page, 'Piezas');
    await expect(page.getByRole('list', { name: 'Piezas creativas' })).toContainText('Promo email');
    await expect(page.getByRole('list', { name: 'Piezas creativas' })).toContainText(
      '2 auditorías guardadas',
    );
    expect(errors).toEqual([]);
  });

  test('sin texto no se puede auditar', async ({ page }) => {
    await page.goto(LOCAL);
    await nav(page, 'Recursos');
    await page.getByLabel('Agregar imagen').setInputFiles({
      name: 'vacia.png',
      mimeType: 'image/png',
      buffer: await png(page),
    });
    await expect(page.getByRole('list', { name: 'Recursos guardados' })).toContainText('vacia.png');
    await nav(page, 'Piezas');
    await page.getByLabel('Nombre de la pieza').fill('Sin texto');
    await page.getByLabel('Canal').selectOption('Banners');
    await page.getByLabel('Imagen (de Recursos)').selectOption({ label: 'vacia.png' });
    await page.getByRole('button', { name: 'Crear pieza' }).click();
    await page.getByRole('button', { name: 'Auditar pieza Sin texto' }).click();
    await expect(page.getByRole('alert')).toContainText('Primero lee el texto');
  });
});
