import { readFileSync } from 'node:fs';
import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

const nav = async (page: Page, name: string) => {
  await page.getByRole('button', { name, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name })).toBeFocused();
};

async function copyWithoutLegend(page: Page) {
  await nav(page, 'Briefs');
  await page.getByRole('button', { name: 'Nuevo brief' }).click();
  await page.getByLabel(/^Campaña/).fill('Buen Fin');
  await page.getByLabel(/^Canal/).selectOption('Email');
  await page.getByRole('button', { name: 'Guardar brief' }).click();
  await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
  await page.getByRole('button', { name: 'Nuevo copy' }).click();
  await page.getByLabel(/^Titular/).fill('Tu salud con descuento');
  await page.getByLabel(/^CTA/).fill('Compra ahora');
  await page.getByRole('button', { name: 'Crear copy' }).click();
}

test.describe('reglas configurables (modo local, Chrome real)', () => {
  test('plantilla → capturar leyenda y término → la revisión los usa → persiste → respaldo', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Reglas');
    await expect(page.getByText('plantilla de ejemplo (sin leyendas')).toBeVisible();
    await expect(page.getByRole('list', { name: 'Términos de marca' })).toContainText('cura');
    expect(await axeViolations(page)).toEqual([]);

    // Nueva leyenda obligatoria solo para Email.
    await page.getByRole('button', { name: 'Nueva leyenda' }).click();
    await page.getByLabel(/^Texto de la leyenda/).fill('Consulta a tu médico');
    await page.getByLabel('Email', { exact: true }).check();
    expect(await axeViolations(page)).toEqual([]);
    await page.getByRole('button', { name: 'Agregar leyenda' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Leyenda agregada' })).toBeVisible();
    await expect(page.getByText('plantilla de ejemplo (sin leyendas')).toHaveCount(0);
    await expect(page.getByRole('list', { name: 'Leyendas' })).toContainText(
      'Email · Obligatoria · Activa',
    );

    // Duplicada (sin importar acentos ni mayúsculas): se rechaza con motivo.
    await page.getByRole('button', { name: 'Nueva leyenda' }).click();
    await page.getByLabel(/^Texto de la leyenda/).fill('CONSULTA A TU MEDICO');
    await page.getByRole('button', { name: 'Agregar leyenda' }).click();
    await expect(page.getByRole('alert')).toContainText('repetidas');
    await page.getByRole('button', { name: 'Cancelar' }).click();

    // Nuevo término crítico con sugerencia.
    await page.getByRole('button', { name: 'Nuevo término' }).click();
    await page.getByLabel('Término (obligatorio)').fill('oferta única');
    await page.getByLabel(/^Severidad/).selectOption('critica');
    await page.getByLabel(/^Sugerencia/).fill('oferta especial');
    await page.getByRole('button', { name: 'Agregar término' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Término agregado' })).toBeVisible();

    // Persiste tras recargar.
    await page.reload();
    await nav(page, 'Reglas');
    await expect(page.getByRole('list', { name: 'Leyendas' })).toContainText(
      'Consulta a tu médico',
    );
    await expect(page.getByRole('list', { name: 'Términos de marca' })).toContainText(
      'Sugerencia: oferta especial',
    );

    // La revisión usa la leyenda: falta → crítica; al desactivarla, desaparece.
    await copyWithoutLegend(page);
    await page.getByRole('button', { name: 'Revisar reglas de Principal' }).click();
    const review = page.getByRole('region', { name: 'Revisión de Principal' });
    await expect(review).toContainText('Falta la leyenda obligatoria: «Consulta a tu médico»');
    await expect(review).toContainText('Se usaron las leyendas y términos que capturaste');
    await page.getByRole('button', { name: 'Volver a los briefs' }).click();
    await nav(page, 'Reglas');
    await page.getByRole('button', { name: 'Desactivar leyenda Consulta a tu médico' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Leyenda desactivada' })).toBeVisible();
    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    await page.getByRole('button', { name: 'Revisar reglas de Principal' }).click();
    await expect(page.getByRole('region', { name: 'Revisión de Principal' })).toContainText(
      'Sin hallazgos',
    );

    // Editar y eliminar (con confirmación) un término.
    await nav(page, 'Reglas');
    await page.getByRole('button', { name: 'Editar término oferta única' }).click();
    await page.getByLabel('Término (obligatorio)').fill('oferta irrepetible');
    await page.getByRole('button', { name: 'Guardar término' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Término actualizado' })).toBeVisible();
    await page.getByRole('button', { name: 'Eliminar término oferta irrepetible' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar término' }).click();
    await expect(page.getByRole('list', { name: 'Términos de marca' })).not.toContainText(
      'irrepetible',
    );

    // El respaldo incluye las reglas.
    await nav(page, 'Respaldo');
    const [download] = await Promise.all([
      page.waitForEvent('download'),
      page.getByRole('button', { name: 'Exportar respaldo' }).click(),
    ]);
    const file = JSON.parse(readFileSync(await download.path(), 'utf8')) as {
      version: number;
      data: { rules: { legends: { text: string; active: boolean }[] } };
    };
    expect(file.version).toBe(6);
    expect(file.data.rules.legends).toEqual([
      expect.objectContaining({ text: 'Consulta a tu médico', active: false }),
    ]);

    // Restaurar la plantilla (con confirmación).
    await nav(page, 'Reglas');
    await page.getByRole('button', { name: 'Restaurar plantilla de ejemplo' }).click();
    await page.getByRole('button', { name: 'Sí, restaurar plantilla' }).click();
    await expect(page.getByText('plantilla de ejemplo (sin leyendas')).toBeVisible();
    await expect(page.getByRole('list', { name: 'Términos de marca' })).toContainText('cura');
    expect(errors).toEqual([]);
  });
});
