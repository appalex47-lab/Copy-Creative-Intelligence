import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

const nav = async (page: Page, name: string) => {
  await page.getByRole('button', { name, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name })).toBeFocused();
};

/** Genera en el navegador un banner PNG con texto grande y legible. */
async function bannerPng(page: Page): Promise<Buffer> {
  const dataUrl = await page.evaluate(() => {
    const c = document.createElement('canvas');
    c.width = 1200;
    c.height = 400;
    const g = c.getContext('2d');
    if (!g) throw new Error('canvas');
    g.fillStyle = '#ffffff';
    g.fillRect(0, 0, c.width, c.height);
    g.fillStyle = '#000000';
    g.font = 'bold 120px Arial, Helvetica, sans-serif';
    g.fillText('OFERTA', 60, 170);
    g.fillText('DESCUENTO', 60, 330);
    return c.toDataURL('image/png');
  });
  return Buffer.from(dataUrl.split(',')[1] ?? '', 'base64');
}

test.describe('recursos y OCR (modo local, Chrome real)', () => {
  test('sube una imagen, lee el texto sin red externa, valida, persiste y elimina', async ({
    page,
  }) => {
    test.setTimeout(120_000);
    const errors = trackErrors(page);
    const external: string[] = [];
    page.on('request', (r) => {
      const u = r.url();
      if (!u.startsWith(LOCAL) && !u.startsWith('blob:') && !u.startsWith('data:'))
        external.push(u);
    });
    await page.goto(LOCAL);
    await nav(page, 'Recursos');
    await expect(page.getByText('Aún no hay recursos')).toBeVisible();
    await expect(page.getByText(/NO van en el\s+respaldo de datos/)).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);

    await page.getByLabel('Agregar imagen').setInputFiles({
      name: 'banner.png',
      mimeType: 'image/png',
      buffer: await bannerPng(page),
    });
    const list = page.getByRole('list', { name: 'Recursos guardados' });
    await expect(list).toContainText('banner.png');
    await expect(list).toContainText('1200×400 px');

    await page.getByRole('button', { name: 'Leer con OCR' }).click();
    await expect(page.getByText('Detectado por OCR (no validado)')).toBeVisible({
      timeout: 90_000,
    });
    const detected = page.getByLabel('Texto detectado');
    await expect(detected).toContainText(/OFERTA/i);
    await expect(detected).toContainText(/DESCUENTO/i);
    expect(await axeViolations(page)).toEqual([]);

    // Lo detectado NO se vuelve "validado" solo.
    await expect(page.getByLabel('Texto confirmado de la imagen')).toHaveValue('');
    await page.getByRole('button', { name: 'Copiar lo detectado para revisarlo' }).click();
    await page.getByLabel('Texto confirmado de la imagen').fill('OFERTA DESCUENTO');
    await page.getByRole('button', { name: 'Guardar texto validado' }).click();
    await expect(
      page.getByRole('status').filter({ hasText: 'Texto validado guardado' }),
    ).toBeVisible();

    // Persiste tras recargar: imagen, texto detectado y texto validado.
    await page.reload();
    await nav(page, 'Recursos');
    await expect(page.getByLabel('Texto confirmado de la imagen')).toHaveValue('OFERTA DESCUENTO');
    await expect(page.getByLabel('Texto detectado')).toContainText(/OFERTA/i);
    expect(external).toEqual([]);

    await page.getByRole('button', { name: 'Eliminar recurso banner.png' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar recurso' }).click();
    await expect(page.getByText('Aún no hay recursos')).toBeVisible();
    expect(errors).toEqual([]);
  });

  test('respaldo de imágenes: descargar, eliminar, restaurar y no duplicar', async ({ page }) => {
    test.setTimeout(60_000);
    await page.goto(LOCAL);
    await nav(page, 'Recursos');
    await page.getByLabel('Agregar imagen').setInputFiles({
      name: 'banner.png',
      mimeType: 'image/png',
      buffer: await bannerPng(page),
    });
    await expect(page.getByRole('list', { name: 'Recursos guardados' })).toContainText(
      'banner.png',
    );
    await page.getByLabel('Texto confirmado de la imagen').fill('Texto validado');
    await page.getByRole('button', { name: 'Guardar texto validado' }).click();
    await expect(
      page.getByRole('status').filter({ hasText: 'Texto validado guardado' }),
    ).toBeVisible();

    const dl = page.waitForEvent('download');
    await page.getByRole('button', { name: 'Descargar respaldo de imágenes' }).click();
    const download = await dl;
    expect(download.suggestedFilename()).toMatch(/^cci-recursos-\d{4}-\d{2}-\d{2}\.json$/);
    const path = await download.path();

    await page.getByRole('button', { name: 'Eliminar recurso banner.png' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar recurso' }).click();
    await expect(page.getByText('Aún no hay recursos')).toBeVisible();

    await page.getByLabel('Restaurar respaldo de imágenes').setInputFiles(path);
    await expect(page.getByText('Restauradas 1 imágenes; 0 ya existían')).toBeVisible();
    await expect(page.getByLabel('Texto confirmado de la imagen')).toHaveValue('Texto validado');
    await expect(page.getByAltText(/Vista previa de banner.png/)).toBeVisible();

    await page.getByLabel('Restaurar respaldo de imágenes').setInputFiles(path);
    await expect(page.getByText('Restauradas 0 imágenes; 1 ya existían')).toBeVisible();

    await page.getByLabel('Restaurar respaldo de imágenes').setInputFiles({
      name: 'malo.json',
      mimeType: 'application/json',
      buffer: Buffer.from('{"format":"otro"}'),
    });
    await expect(page.getByRole('alert')).toContainText('no es un respaldo de imágenes válido');
    expect(await axeViolations(page)).toEqual([]);
  });

  test('rechaza formatos y tamaños no admitidos con un mensaje claro', async ({ page }) => {
    await page.goto(LOCAL);
    await nav(page, 'Recursos');
    await page.getByLabel('Agregar imagen').setInputFiles({
      name: 'a.gif',
      mimeType: 'image/gif',
      buffer: Buffer.from('GIF89a'),
    });
    await expect(page.getByRole('alert')).toContainText('Formato no admitido');
    await page.getByLabel('Agregar imagen').setInputFiles({
      name: 'grande.png',
      mimeType: 'image/png',
      buffer: Buffer.alloc(5 * 1024 * 1024 + 1, 1),
    });
    await expect(page.getByRole('alert')).toContainText('el máximo es 5 MB');
    await page.getByLabel('Agregar imagen').setInputFiles({
      name: 'roto.png',
      mimeType: 'image/png',
      buffer: Buffer.from('no es una imagen'),
    });
    await expect(page.getByRole('alert')).toContainText('no se pudo leer');
  });
});
