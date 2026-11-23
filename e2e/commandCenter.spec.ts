import { expect, test } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

// Centro de comando en modo LOCAL: la actividad sale de IndexedDB real, sin datos inventados.
test.describe('resumen con actividad real (modo local, Chrome real)', () => {
  test('la actividad registrada persiste y aparece de la más nueva a la más antigua', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await expect(page.getByRole('status')).toHaveText('Contenido cargado.');
    // Cambia el nombre y el tema: cada cambio correcto anota un evento.
    await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
    await page.getByLabel('Nombre visible (opcional)').fill('Ale');
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByText('Nombre guardado.')).toBeVisible();
    await page.getByLabel('Tema').selectOption('dark');
    await expect(page.getByText('Tema: Oscuro.')).toBeVisible();
    await page.reload();
    const items = page.locator('main').getByRole('listitem');
    await expect(items.first()).toBeVisible();
    const texts = await items.allTextContents();
    // Más nuevo primero: cambio de preferencia, cambio de perfil, apertura (de la primera carga).
    // La apertura de esta recarga puede o no haberse anotado ya al listar: se ignora para el orden.
    const changes = texts.filter((t) => !t.includes('Se abrió la aplicación'));
    expect(changes[0]).toContain('Cambió una preferencia');
    expect(changes[1]).toContain('Cambió el perfil local');
    expect(texts.some((t) => t.includes('Se abrió la aplicación'))).toBe(true);
    // Ningún contenido del usuario se guarda en la actividad.
    for (const t of texts) expect(t).not.toContain('Ale ');
    expect(await axeViolations(page)).toEqual([]);
    expect(errors).toEqual([]);
  });

  test('un cambio rechazado por validación NO registra actividad', async ({ page }) => {
    await page.goto(LOCAL);
    await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
    await page.getByLabel('Nombre visible (opcional)').fill('x'.repeat(61));
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByRole('alert')).toBeVisible();
    await page.reload();
    const items = page.locator('main').getByRole('listitem');
    await expect(items.first()).toContainText('Se abrió la aplicación');
    const texts = await items.allTextContents();
    expect(texts.join('|')).not.toContain('Cambió el perfil local');
  });
});
