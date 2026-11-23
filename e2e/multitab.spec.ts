import { expect, test } from '@playwright/test';
import { axeViolations, LOCAL } from './support';

// P12: una pestaña escribe; las demás quedan en solo lectura con aviso visible y recuperan el permiso solas.
test.describe('varias pestañas (modo local, Chrome real)', () => {
  test('la segunda pestaña queda en solo lectura; al cerrar la primera recibe el control', async ({
    context,
  }) => {
    const a = await context.newPage();
    await a.goto(LOCAL);
    await a.getByRole('button', { name: 'Perfil y preferencias', exact: true }).click();
    await a.getByLabel('Nombre visible (opcional)').fill('Ana');
    await a.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(a.getByText('Nombre guardado.')).toBeVisible();
    await expect(a.getByTestId('solo-lectura')).toHaveCount(0);

    const b = await context.newPage();
    await b.goto(LOCAL);
    const aviso = b.getByTestId('solo-lectura');
    await expect(aviso).toContainText('Solo lectura');
    expect(await axeViolations(b)).toEqual([]);
    // En solo lectura se PUEDEN ver los datos...
    await b.getByRole('button', { name: 'Perfil y preferencias', exact: true }).click();
    await expect(b.getByText('Nombre visible actual:')).toContainText('Ana');
    // ...pero NO cambiarlos: el intento falla y no escribe nada.
    await b.getByLabel('Nombre visible (opcional)').fill('Intruso');
    await b.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(b.getByRole('alert')).toContainText('solo lectura');
    await b.getByLabel('Tema').selectOption('dark');
    await expect(b.getByRole('alert').last()).toContainText('solo lectura');
    await expect(b.locator('html')).not.toHaveAttribute('data-theme', /.+/);

    // La pestaña A sigue escribiendo.
    await a.getByLabel('Nombre visible (opcional)').fill('Ana María');
    await a.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(a.getByText('Nombre guardado.')).toBeVisible();

    // Al cerrar A, B recibe el control automáticamente y ya puede escribir.
    await a.close();
    await expect(aviso).toHaveCount(0, { timeout: 10_000 });
    await b.getByLabel('Nombre visible (opcional)').fill('Eva');
    await b.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(b.getByText('Nombre guardado.')).toBeVisible();
    await b.reload();
    await b.getByRole('button', { name: 'Perfil y preferencias', exact: true }).click();
    await expect(b.getByText('Nombre visible actual:')).toContainText('Eva');
  });

  test('recargar la pestaña escritora no la deja en solo lectura', async ({ page }) => {
    await page.goto(LOCAL);
    await page.reload();
    await page.reload();
    await page.getByRole('button', { name: 'Perfil y preferencias', exact: true }).click();
    await page.getByLabel('Nombre visible (opcional)').fill('Ana');
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByText('Nombre guardado.')).toBeVisible();
    await expect(page.getByTestId('solo-lectura')).toHaveCount(0);
  });

  test('el respaldo no se puede importar desde una pestaña de solo lectura', async ({
    context,
  }) => {
    const a = await context.newPage();
    await a.goto(LOCAL);
    await a.getByRole('button', { name: 'Respaldo', exact: true }).click();
    const [download] = await Promise.all([
      a.waitForEvent('download'),
      a.getByRole('button', { name: 'Exportar respaldo' }).click(),
    ]);
    const path = await download.path();
    const b = await context.newPage();
    await b.goto(LOCAL);
    await expect(b.getByTestId('solo-lectura')).toBeVisible();
    await b.getByRole('button', { name: 'Respaldo', exact: true }).click();
    await b.getByLabel('Archivo de respaldo (.json)').setInputFiles(path);
    await b.getByRole('button', { name: 'Reemplazar todos los datos locales' }).click();
    await expect(b.getByRole('alert')).toContainText('solo lectura');
    await expect(b.getByText('Respaldo importado')).toHaveCount(0);
  });
});
