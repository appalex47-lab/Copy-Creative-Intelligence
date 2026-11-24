import { readFileSync } from 'node:fs';
import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

const nav = async (page: Page, name: string) => {
  await page.getByRole('button', { name, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name })).toBeFocused();
};

test.describe('auditorías guardadas de copy (modo local, Chrome real)', () => {
  test('guardar, comparar con la anterior, persistir, respaldar, impedir borrar el copy y eliminar', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Nuevo brief' }).click();
    await page.getByLabel(/^Campaña/).fill('Buen Fin');
    await page.getByLabel(/^Canal/).selectOption('Email');
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    await page.getByRole('button', { name: 'Nuevo copy' }).click();
    await page.getByLabel(/^Titular/).fill('Una cura para todo');
    await page.getByRole('button', { name: 'Crear copy' }).click();

    const section = page.getByRole('region', { name: 'Auditorías de Principal' });
    await expect(section).toContainText('Auditorías guardadas (0)');
    expect(await axeViolations(page)).toEqual([]);
    await page.getByRole('button', { name: 'Guardar auditoría de Principal' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Auditoría guardada' })).toBeVisible();
    await expect(section).toContainText('Auditorías guardadas (1)');
    await expect(section).toContainText('versión 1');
    await expect(section).toContainText('Email');
    await expect(section).toContainText('«cura»');

    // Corrige el copy y audita otra vez: compara con la anterior sin borrarla.
    await page.getByRole('button', { name: 'Editar Principal' }).click();
    await page.getByLabel(/^Titular/).fill('Cuida tu salud con descuento');
    await page.getByLabel(/^CTA/).fill('Compra ahora');
    await page.getByRole('button', { name: 'Guardar nueva versión' }).click();
    await page.getByRole('button', { name: 'Guardar auditoría de Principal' }).click();
    await expect(section).toContainText('Auditorías guardadas (2)');
    await expect(section).toContainText('versión 2');
    await expect(section).toContainText('Frente a la auditoría anterior');
    await expect(section).toContainText('resueltos');
    expect(await axeViolations(page)).toEqual([]);

    // Persisten tras recargar.
    await page.reload();
    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    await expect(page.getByRole('region', { name: 'Auditorías de Principal' })).toContainText(
      'Auditorías guardadas (2)',
    );

    // El respaldo las incluye.
    await nav(page, 'Respaldo');
    const [dl] = await Promise.all([
      page.waitForEvent('download'),
      page.getByRole('button', { name: 'Exportar respaldo' }).click(),
    ]);
    const f = JSON.parse(readFileSync(await dl.path(), 'utf8')) as {
      version: number;
      data: { audits: { sourceVersion: number }[] };
    };
    expect(f.version).toBe(7);
    expect(f.data.audits.map((a) => a.sourceVersion).sort()).toEqual([1, 2]);

    // El copy con auditorías no se borra; al eliminarlas sí.
    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    await page.getByRole('button', { name: 'Eliminar Principal', exact: true }).click();
    await page.getByRole('button', { name: 'Sí, eliminar copy' }).click();
    await expect(page.getByRole('alert')).toContainText('auditorías guardadas');
    for (let i = 0; i < 2; i++) {
      await page
        .getByRole('button', { name: /^Eliminar auditoría de Principal/ })
        .first()
        .click();
      await page.getByRole('button', { name: 'Sí, eliminar auditoría' }).click();
      await expect(
        page.getByRole('status').filter({ hasText: 'Auditoría eliminada' }),
      ).toBeVisible();
    }
    await page.getByRole('button', { name: 'Eliminar Principal', exact: true }).click();
    await page.getByRole('button', { name: 'Sí, eliminar copy' }).click();
    await expect(page.getByText('Copy eliminado.')).toBeVisible();
    expect(errors).toEqual([]);
  });
});
