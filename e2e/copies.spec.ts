import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

async function openCopies(page: Page) {
  await page.getByRole('button', { name: 'Briefs', exact: true }).click();
  await page.getByRole('button', { name: 'Nuevo brief' }).click();
  await page.getByLabel(/^Campaña/).fill('Buen Fin');
  await page.getByLabel(/^Canal/).selectOption('Email');
  await page.getByRole('button', { name: 'Guardar brief' }).click();
  await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
  await expect(page.getByRole('heading', { level: 3, name: 'Copys de Buen Fin' })).toBeVisible();
}

test.describe('copys con versiones (modo local, Chrome real)', () => {
  test('crear → nueva versión → historial → recuperar → duplicar → borrar; brief con copys no se borra', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await openCopies(page);
    await expect(page.getByText('Este brief aún no tiene copys')).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);

    await page.getByRole('button', { name: 'Nuevo copy' }).click();
    await page.getByLabel(/^Titular/).fill('Ahorra en tu Buen Fin');
    expect(await axeViolations(page)).toEqual([]);
    await page.getByRole('button', { name: 'Crear copy' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'versión 1' })).toBeVisible();

    // Sin cambios: no crea versión.
    await page.getByRole('button', { name: 'Editar Principal' }).click();
    await page.getByRole('button', { name: 'Guardar nueva versión' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'No había cambios' })).toBeVisible();

    // Con cambios: versión 2.
    await page.getByRole('button', { name: 'Editar Principal' }).click();
    await page.getByLabel(/^Titular/).fill('Ahorra más en tu Buen Fin');
    await page.getByRole('button', { name: 'Guardar nueva versión' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'versión 2' })).toBeVisible();

    // Historial y recuperar la 1 → versión 3.
    await page.getByRole('button', { name: 'Historial de Principal' }).click();
    await expect(
      page.getByRole('heading', { level: 5, name: /Versión 2 \(vigente\)/ }),
    ).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);
    await page.getByRole('button', { name: 'Recuperar versión 1' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'como versión 3' })).toBeVisible();
    await expect(page.getByRole('listitem').filter({ hasText: 'Versión 3 de 3' })).toContainText(
      'Ahorra en tu Buen Fin',
    );

    // Duplicar como variante.
    await page.getByRole('button', { name: 'Duplicar como variante: Principal' }).click();
    await page.getByLabel('Nombre de la variante nueva').fill('B');
    await page.getByRole('button', { name: 'Crear variante' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Variante «B» creada' })).toBeVisible();

    // Persiste tras recargar.
    await page.reload();
    await page.getByRole('button', { name: 'Briefs', exact: true }).click();
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    await expect(page.getByRole('button', { name: 'Editar B' })).toBeVisible();

    // Revisar reglas en la variante B: «cura» (mayor) y sin CTA en Email.
    await page.getByRole('button', { name: 'Editar B' }).click();
    await page.getByLabel(/^Descripción/).fill('Una cura para todo');
    await page.getByRole('button', { name: 'Guardar nueva versión' }).click();
    await page.getByRole('button', { name: 'Revisar reglas de B' }).click();
    const review = page.getByRole('region', { name: 'Revisión de B' });
    await expect(review).toContainText('término prohibido «cura»');
    await expect(review).toContainText('Puntaje');
    expect(await axeViolations(page)).toEqual([]);
    await page.getByRole('button', { name: 'Cerrar revisión' }).click();

    // Volver: el brief con copys no se puede eliminar.
    await page.getByRole('button', { name: 'Volver a los briefs' }).click();
    await page.getByRole('button', { name: 'Eliminar Buen Fin' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar' }).click();
    await expect(page.getByRole('alert').filter({ hasText: 'datos que dependen' })).toBeVisible();

    // Borrar los copys y luego el brief.
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    for (const name of ['B', 'Principal']) {
      await page.getByRole('button', { name: `Eliminar ${name}`, exact: true }).click();
      await page.getByRole('button', { name: 'Sí, eliminar copy' }).click();
      await expect(page.getByRole('status').filter({ hasText: 'Copy eliminado' })).toBeVisible();
    }
    await page.getByRole('button', { name: 'Volver a los briefs' }).click();
    await page.getByRole('button', { name: 'Eliminar Buen Fin' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar' }).click();
    await expect(page.getByText('Aún no hay briefs')).toBeVisible();
    expect(errors).toEqual([]);
  });

  test('plantilla: precarga solo datos del brief para el canal y se puede editar antes de guardar', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await page.getByRole('button', { name: 'Briefs', exact: true }).click();
    await page.getByRole('button', { name: 'Nuevo brief' }).click();
    await page.getByLabel(/^Campaña/).fill('Buen Fin');
    await page.getByLabel(/^Canal/).selectOption('Email');
    await page.getByLabel(/^Producto/).fill('Vitamina C');
    await page.getByLabel(/^Mensaje central/).fill('Cuida tu salud');
    await page.getByLabel(/^CTA/).fill('Compra ahora');
    await page.getByLabel(/^Oferta/).fill('20% de descuento');
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await page.getByRole('button', { name: 'Copys de Buen Fin' }).click();
    await page.getByRole('button', { name: 'Nuevo copy' }).click();
    expect(await axeViolations(page)).toEqual([]);
    await page.getByLabel(/^Empezar desde una plantilla/).selectOption('oferta');
    await expect(page.getByLabel(/^Titular/)).toHaveValue('20% de descuento en Vitamina C');
    await expect(page.getByLabel(/^Texto/)).toHaveValue('Cuida tu salud');
    await expect(page.getByLabel(/^CTA/)).toHaveValue('Compra ahora');
    await page.getByLabel(/^Titular/).fill('Tu Vitamina C con 20% de descuento');
    await page.getByRole('button', { name: 'Crear copy' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'versión 1' })).toBeVisible();
    await page.getByRole('button', { name: 'Revisar reglas de Principal' }).click();
    await expect(page.getByRole('region', { name: 'Revisión de Principal' })).toContainText(
      'Puntaje',
    );
    expect(errors).toEqual([]);
  });
});
