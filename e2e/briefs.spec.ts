import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

async function goto(page: Page, view: string) {
  await page.getByRole('button', { name: view, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name: view })).toBeFocused();
}
const fill = (page: Page, label: RegExp, value: string) => page.getByLabel(label).fill(value);

async function newBrief(page: Page, fields: Partial<Record<string, string>>) {
  await page.getByRole('button', { name: 'Nuevo brief' }).click();
  for (const [label, value] of Object.entries(fields))
    if (label === 'Canal') await page.getByLabel(/^Canal/).selectOption(value as string);
    else await fill(page, new RegExp(`^${label}`), value as string);
}

test.describe('briefs (modo local, Chrome real)', () => {
  test('vacío → crear incompleto (se señala qué falta) → persiste → completar → borrar', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await goto(page, 'Briefs');
    await expect(page.getByText('Aún no hay briefs')).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);

    // Borrador incompleto: se guarda, pero se señala con el motivo por campo.
    await newBrief(page, { Campaña: 'Buen Fin', Canal: 'Email' });
    expect(await axeViolations(page)).toEqual([]);
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await expect(page.getByRole('heading', { level: 2, name: 'Briefs' })).toBeFocused();
    await expect(
      page.getByRole('status').filter({ hasText: 'guardado como incompleto' }),
    ).toBeVisible();
    const item = page.getByRole('listitem').filter({ hasText: 'Buen Fin' }).first();
    await expect(item).toContainText('Incompleto');
    await expect(item).toContainText('Falta Objetivo (obligatorio).');
    await expect(item).toContainText('Falta CTA (obligatorio).');
    expect(await axeViolations(page)).toEqual([]);

    // Persiste tras recargar.
    await page.reload();
    await goto(page, 'Briefs');
    await expect(page.getByRole('listitem').filter({ hasText: 'Buen Fin' }).first()).toContainText(
      'Incompleto',
    );

    // Completarlo.
    await page.getByRole('button', { name: 'Editar Buen Fin' }).click();
    await fill(page, /^Objetivo/, 'Aumentar conversión');
    await fill(page, /^Producto/, 'Vitamina C');
    await fill(page, /^Audiencia/, 'Clientes recurrentes');
    await fill(page, /^Mensaje central/, 'Cuida tu salud');
    await fill(page, /^CTA/, 'Compra ahora');
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Está completo' })).toBeVisible();
    await expect(page.getByRole('listitem').filter({ hasText: 'Buen Fin' }).first()).toContainText(
      'Completo',
    );

    // Borrar con confirmación; cancelar no borra.
    await page.getByRole('button', { name: 'Eliminar Buen Fin' }).click();
    await page.getByRole('button', { name: 'Cancelar' }).click();
    await expect(page.getByRole('button', { name: 'Editar Buen Fin' })).toBeVisible();
    await page.getByRole('button', { name: 'Eliminar Buen Fin' }).click();
    await page.getByRole('button', { name: 'Sí, eliminar' }).click();
    await expect(page.getByText('Aún no hay briefs')).toBeVisible();
    await expect(page.getByRole('status').filter({ hasText: 'Brief eliminado' })).toBeVisible();
    expect(errors).toEqual([]);
  });

  test('un campo inválido no se guarda: error por campo, foco en el primero y accesible', async ({
    page,
  }) => {
    await page.goto(LOCAL);
    await goto(page, 'Briefs');
    await newBrief(page, { Campaña: 'x'.repeat(121) });
    await page
      .getByLabel(/^Vigencia|Desde/)
      .first()
      .fill('2026-11-30');
    await page.getByLabel('Hasta').fill('2026-11-01');
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await expect(page.getByLabel(/^Campaña/)).toBeFocused();
    await expect(page.getByLabel(/^Campaña/)).toHaveAttribute('aria-invalid', 'true');
    await expect(page.getByRole('alert').filter({ hasText: 'como máximo 120' })).toBeVisible();
    await expect(
      page.getByRole('alert').filter({ hasText: 'no puede ser posterior' }),
    ).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);
    // Nada se guardó.
    await page.getByRole('button', { name: 'Cancelar' }).click();
    await expect(page.getByText('Aún no hay briefs')).toBeVisible();
  });

  test('la segunda pestaña ve los briefs pero no puede guardar (solo lectura)', async ({
    context,
  }) => {
    const a = await context.newPage();
    await a.goto(LOCAL);
    await goto(a, 'Briefs');
    await newBrief(a, { Campaña: 'Desde A' });
    await a.getByRole('button', { name: 'Guardar brief' }).click();
    await expect(a.getByRole('status').filter({ hasText: 'guardado' })).toBeVisible();

    const b = await context.newPage();
    await b.goto(LOCAL);
    await expect(b.getByTestId('solo-lectura')).toContainText('Solo lectura');
    await goto(b, 'Briefs');
    await expect(b.getByRole('listitem').filter({ hasText: 'Desde A' }).first()).toBeVisible();
    await newBrief(b, { Campaña: 'Intruso' });
    await b.getByRole('button', { name: 'Guardar brief' }).click();
    await expect(b.getByRole('alert')).toContainText('solo lectura');
    await b.getByRole('button', { name: 'Cancelar' }).click();
    await expect(b.getByText('Intruso')).toHaveCount(0);
  });
});
