import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

// Modo de datos LOCAL (IndexedDB + Local Storage reales). Cada test usa un contexto nuevo (almacenamiento limpio).
async function openSettings(page: Page) {
  await page.goto(LOCAL);
  await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
  await expect(
    page.getByRole('heading', { level: 2, name: 'Perfil y preferencias' }),
  ).toBeFocused();
}

test.describe('perfil y preferencias (modo local, Chrome real)', () => {
  test('sin aviso DEMO y con el modo real indicado', async ({ page }) => {
    await page.goto(LOCAL);
    await expect(page.getByRole('region', { name: 'Aviso de modo DEMO' })).toHaveCount(0);
    await expect(page).not.toHaveTitle(/DEMO/);
    await page.getByRole('button', { name: 'Estado de conexión' }).click();
    await expect(page.getByText('Modo de datos:')).toContainText('LOCAL');
  });

  test('guardar el nombre persiste tras recargar; borrarlo lo elimina', async ({ page }) => {
    const errors = trackErrors(page);
    await openSettings(page);
    await page.getByLabel('Nombre visible (opcional)').fill('  Alejandro  ');
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Nombre guardado.' })).toBeVisible();
    await page.reload();
    await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
    await expect(page.getByText('Nombre visible actual:')).toContainText('Alejandro');
    await expect(page.getByLabel('Nombre visible (opcional)')).toHaveValue('Alejandro');
    await page.getByRole('button', { name: 'Borrar nombre' }).click();
    await expect(page.getByText('Nombre visible actual:')).toContainText('sin nombre');
    await page.reload();
    await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
    await expect(page.getByText('Nombre visible actual:')).toContainText('sin nombre');
    expect(errors).toEqual([]);
  });

  test('un nombre inválido muestra el motivo y no se guarda; el texto se muestra escapado', async ({
    page,
  }) => {
    await openSettings(page);
    await page.getByLabel('Nombre visible (opcional)').fill('x'.repeat(61));
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByRole('alert')).toContainText('60');
    await expect(page.getByText('Nombre visible actual:')).toContainText('sin nombre');
    await page.getByLabel('Nombre visible (opcional)').fill('<img src=x onerror=alert(1)>');
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByText('Nombre visible actual:')).toContainText('<img src=x');
    await expect(page.locator('main img')).toHaveCount(0);
  });

  test('el tema oscuro se aplica y persiste tras recargar', async ({ page }) => {
    await openSettings(page);
    await page.getByLabel('Tema').selectOption('dark');
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
    await expect(page.getByLabel('Tema')).toHaveValue('dark');
    await page.getByLabel('Tema').selectOption('system');
    await expect(page.locator('html')).not.toHaveAttribute('data-theme', /.+/);
  });

  for (const theme of ['light', 'dark'] as const) {
    test(`accesibilidad (axe) de Perfil y preferencias con tema ${theme}`, async ({ page }) => {
      await openSettings(page);
      await page.getByLabel('Tema').selectOption(theme);
      await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
      await page.getByLabel('Nombre visible (opcional)').fill('x'.repeat(61));
      await page.getByRole('button', { name: 'Guardar nombre' }).click();
      await expect(page.getByRole('alert')).toBeVisible();
      expect(await axeViolations(page)).toEqual([]);
    });
  }

  test('sin desbordamiento horizontal en anchos de 320 a 1440', async ({ page }) => {
    await openSettings(page);
    for (const width of [320, 375, 768, 1440]) {
      await page.setViewportSize({ width, height: 800 });
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
      );
      expect(overflow, `ancho ${width}`).toBe(false);
    }
  });
});
