import { readFileSync } from 'node:fs';
import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

const nav = async (page: Page, name: string) => {
  await page.getByRole('button', { name, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name })).toBeFocused();
};

test.describe('catálogo, campaña en brief, adaptaciones y búsqueda (modo local, Chrome real)', () => {
  test('catálogo: crear, duplicado, editar, tipos separados y borrar con confirmación', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Catálogo');
    await expect(page.getByText('Aún no hay campañas.')).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);

    await page.getByRole('button', { name: 'Nueva campaña' }).click();
    await page.getByLabel('Nombre (obligatorio)').fill('Buen Fin');
    await page.getByLabel('Nota (opcional)').fill('Solo nombre');
    expect(await axeViolations(page)).toEqual([]);
    await page.getByRole('button', { name: 'Agregar campaña' }).click();
    await expect(
      page.getByRole('status').filter({ hasText: 'Se agregó la campaña' }),
    ).toBeVisible();
    await expect(page.getByRole('list', { name: 'Campañas' })).toContainText('Buen Fin');

    // Duplicado (sin acentos ni mayúsculas): se rechaza con motivo.
    await page.getByRole('button', { name: 'Nueva campaña' }).click();
    await page.getByLabel('Nombre (obligatorio)').fill('BUEN FIN');
    await page.getByRole('button', { name: 'Agregar campaña' }).click();
    await expect(page.getByRole('alert')).toContainText('Ya existe un registro con ese nombre');
    await page.getByRole('button', { name: 'Cancelar' }).click();

    // Otro tipo con el mismo nombre es válido y las listas están separadas.
    await page.getByRole('button', { name: 'Productos' }).click();
    await expect(page.getByText('Aún no hay productos.')).toBeVisible();
    await page.getByRole('button', { name: 'Nuevo producto' }).click();
    await page.getByLabel('Nombre (obligatorio)').fill('Buen Fin');
    await page.getByRole('button', { name: 'Agregar producto' }).click();
    await expect(page.getByRole('list', { name: 'Productos' })).toContainText('Buen Fin');
    await page.getByRole('button', { name: 'Ofertas' }).click();
    await expect(page.getByText('Aún no hay ofertas.')).toBeVisible();

    // Persiste tras recargar; editar; borrar con confirmación.
    await page.reload();
    await nav(page, 'Catálogo');
    await expect(page.getByRole('list', { name: 'Campañas' })).toContainText('Buen Fin');
    await page.getByRole('button', { name: 'Editar Buen Fin' }).click();
    await page.getByLabel('Nombre (obligatorio)').fill('Buen Fin 2026');
    await page.getByRole('button', { name: 'Guardar cambios' }).click();
    await expect(page.getByRole('list', { name: 'Campañas' })).toContainText('Buen Fin 2026');
    await page.getByRole('button', { name: 'Eliminar Buen Fin 2026' }).click();
    await expect(page.getByText('¿Eliminar este registro? No se puede deshacer.')).toBeVisible();
    await page.getByRole('button', { name: 'Sí, eliminar registro' }).click();
    await expect(page.getByText('Aún no hay campañas.')).toBeVisible();
    expect(errors).toEqual([]);
  });

  test('un brief referencia una campaña; la campaña en uso no se borra hasta quitar la referencia', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Catálogo');
    await page.getByRole('button', { name: 'Nueva campaña' }).click();
    await page.getByLabel('Nombre (obligatorio)').fill('Verano Salud');
    await page.getByRole('button', { name: 'Agregar campaña' }).click();

    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Nuevo brief' }).click();
    await page
      .getByLabel('Elegir de campañas registradas (opcional)')
      .selectOption({ label: 'Verano Salud' });
    await expect(page.getByLabel(/^Campaña/)).toHaveValue('Verano Salud');
    expect(await axeViolations(page)).toEqual([]);
    await page.getByLabel(/^Canal/).selectOption('Email');
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Brief guardado' })).toBeVisible();

    await nav(page, 'Catálogo');
    await page.getByRole('button', { name: 'Eliminar Verano Salud' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar registro' }).click();
    await expect(page.getByRole('alert')).toContainText('en uso por briefs');
    await expect(page.getByRole('list', { name: 'Campañas' })).toContainText('Verano Salud');

    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Editar Verano Salud' }).click();
    await expect(page.getByLabel('Elegir de campañas registradas (opcional)')).toHaveValue(/^cmp_/);
    await page.getByLabel('Elegir de campañas registradas (opcional)').selectOption('');
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Brief guardado' })).toBeVisible();

    await nav(page, 'Catálogo');
    await page.getByRole('button', { name: 'Eliminar Verano Salud' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar registro' }).click();
    await expect(page.getByText('Aún no hay campañas.')).toBeVisible();
    expect(errors).toEqual([]);
  });

  test('adaptar un copy a otro canal, persistir, impedir borrar el copy y respaldar', async ({
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
    await page.getByLabel(/^Titular/).fill('Ahorra en tu Buen Fin');
    await page.getByLabel(/^CTA/).fill('Compra ahora');
    await page.getByRole('button', { name: 'Crear copy' }).click();

    await page.getByRole('button', { name: 'Adaptar a otro canal Principal' }).click();
    await page.getByLabel('Canal de destino').selectOption('WhatsApp');
    // WhatsApp usa Texto y CTA: el CTA llega prellenado; el titular no se muestra.
    await expect(page.getByLabel(/^CTA/)).toHaveValue('Compra ahora');
    await expect(page.getByLabel(/^Titular/)).toHaveCount(0);
    await page.getByLabel(/^Texto/).fill('Hola, ahorra en tu Buen Fin');
    await expect(
      page.getByText(/de 600 caracteres \(límite orientativo de WhatsApp/),
    ).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);
    await page.getByRole('button', { name: 'Guardar adaptación' }).click();
    const section = page.getByRole('region', { name: 'Adaptaciones de Principal' });
    await expect(section).toContainText('Adaptaciones por canal (1)');
    await expect(section).toContainText('WhatsApp · desde la versión 1');
    await expect(section).toContainText('Hola, ahorra en tu Buen Fin');

    // Borrar el copy con adaptaciones se rechaza.
    await page.getByRole('button', { name: 'Eliminar Principal', exact: true }).click();
    await page.getByRole('button', { name: 'Sí, eliminar copy' }).click();
    await expect(page.getByRole('alert')).toContainText('adaptaciones');

    // Persiste tras recargar y se puede editar (el canal no cambia).
    await page.reload();
    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    await expect(page.getByRole('region', { name: 'Adaptaciones de Principal' })).toContainText(
      'WhatsApp',
    );
    await page.getByRole('button', { name: 'Editar adaptación a WhatsApp' }).click();
    await expect(page.getByLabel('Canal de destino')).toBeDisabled();
    await page.getByLabel(/^Texto/).fill('Texto ajustado');
    await page.getByRole('button', { name: 'Guardar adaptación' }).click();
    await expect(page.getByRole('region', { name: 'Adaptaciones de Principal' })).toContainText(
      'Texto ajustado',
    );

    // El respaldo incluye la adaptación.
    await nav(page, 'Respaldo');
    const [dl] = await Promise.all([
      page.waitForEvent('download'),
      page.getByRole('button', { name: 'Exportar respaldo' }).click(),
    ]);
    const text = readFileSync(await dl.path(), 'utf8');
    const f = JSON.parse(text) as { version: number; data: { adaptations: { channel: string }[] } };
    expect(f.version).toBe(6);
    expect(f.data.adaptations.map((a) => a.channel)).toEqual(['WhatsApp']);

    // Eliminar la adaptación y luego el copy.
    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    await page.getByRole('button', { name: 'Eliminar adaptación a WhatsApp' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar adaptación' }).click();
    await page.getByRole('button', { name: 'Eliminar Principal', exact: true }).click();
    await page.getByRole('button', { name: 'Sí, eliminar copy' }).click();
    await expect(page.getByText('Copy eliminado.')).toBeVisible();
    expect(errors).toEqual([]);
  });

  test('búsqueda de copys por nombre, etiqueta y texto', async ({ page }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Nuevo brief' }).click();
    await page.getByLabel(/^Campaña/).fill('Buen Fin');
    await page.getByLabel(/^Canal/).selectOption('Email');
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    for (const [name, headline] of [
      ['Principal', 'Ahorra en tu Buen Fin'],
      ['Secundario', 'Vitaminas con descuento'],
    ] as const) {
      await page.getByRole('button', { name: 'Nuevo copy' }).click();
      await page.locator('#copy-label').fill(name);
      await page.getByLabel(/^Titular/).fill(headline);
      await page.getByRole('button', { name: 'Crear copy' }).click();
      await expect(page.getByRole('status').filter({ hasText: 'versión 1' })).toBeVisible();
    }
    const list = page.getByRole('list', { name: 'Copys del brief' });
    await expect(list.getByRole('heading', { level: 4 })).toHaveCount(2);
    expect(await axeViolations(page)).toEqual([]);
    await page.getByLabel('Buscar copys (nombre, etiqueta o texto)').fill('VITAMINAS');
    await expect(list.getByRole('heading', { level: 4 })).toHaveCount(1);
    await expect(list).toContainText('Secundario');
    await expect(page.getByText('1 de 2 copys coinciden.')).toBeVisible();
    await page.getByLabel('Buscar copys (nombre, etiqueta o texto)').fill('nada');
    await expect(list.getByRole('heading', { level: 4 })).toHaveCount(0);
    await page.getByLabel('Buscar copys (nombre, etiqueta o texto)').fill('');
    await expect(list.getByRole('heading', { level: 4 })).toHaveCount(2);
    expect(errors).toEqual([]);
  });
});
