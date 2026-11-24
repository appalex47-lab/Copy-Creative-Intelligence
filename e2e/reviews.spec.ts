import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

const nav = async (page: Page, name: string) => {
  await page.getByRole('button', { name, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name })).toBeFocused();
};

const SCORES: Record<string, string> = {
  'Claridad del mensaje': '15',
  'Fuerza del titular': '14',
  'Beneficio y persuasión': '14',
  'Propuesta comercial': '14',
  'CTA y conversión': '10',
  'UX y legibilidad': '10',
  'Coherencia de marca': '10',
  'Precisión y cumplimiento': '10',
};

test.describe('revisión de calidad CCI (modo local, Chrome real)', () => {
  test('califica, calcula veredicto, exige sustento para aprobar filtros y persiste', async ({
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
    await page.getByLabel(/^Titular/).fill('Aprovecha 20% de descuento');
    await page.getByRole('button', { name: 'Crear copy' }).click();

    await nav(page, 'Revisión');
    expect(await axeViolations(page)).toEqual([]);
    await page.getByLabel('¿Qué vas a revisar?').selectOption({ label: 'Principal' });
    const summary = page.getByRole('status', { name: 'Resumen de la revisión' });
    await expect(summary).toContainText('Sin puntaje');
    await expect(summary).toContainText('PENDIENTE');

    // Califica 7 de 8: sigue pendiente (sin aprobación definitiva).
    for (const [label, v] of Object.entries(SCORES).slice(0, 7))
      await page.getByLabel(new RegExp(`^${label}`)).fill(v);
    await expect(summary).toContainText('PENDIENTE');
    await page.getByLabel(/^Precisión y cumplimiento/).fill('10');
    await expect(summary).toContainText('97 de 100');
    await expect(summary).toContainText('APROBADO');
    await expect(summary).toContainText('No publicable todavía');

    // No se puede aprobar el filtro comercial sin confirmar los 6 puntos.
    await page.getByLabel('Filtro comercial', { exact: true }).selectOption('aprobado');
    await page.getByRole('button', { name: 'Guardar revisión' }).click();
    await expect(page.getByRole('alert')).toContainText('confirma los 6 puntos comerciales');
    for (const c of [
      'El SKU o los productos participan en la promoción.',
      'El porcentaje y el precio son correctos.',
      'La vigencia es correcta.',
      'Hay disponibilidad.',
      'Las restricciones están comunicadas.',
      'El mensaje es consistente entre canales.',
    ])
      await page.getByLabel(c).check();
    await page.getByLabel('Filtro creativo').selectOption('aprobado');
    await expect(summary).toContainText('Lista para publicar');
    await page.getByRole('button', { name: 'Guardar revisión' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Revisión guardada' })).toBeVisible();

    // Un hallazgo bloqueante rechaza aunque el puntaje sea alto y el filtro creativo no se puede aprobar.
    await page.getByRole('button', { name: 'Agregar hallazgo' }).click();
    await page
      .getByLabel(/^Hallazgo \(qué está mal\)/)
      .fill('El descuento no coincide con la oferta');
    await page.getByLabel(/^Impacto/).fill('Publicidad engañosa');
    await page.getByLabel(/^Recomendación/).fill('Corregir al porcentaje vigente');
    await page.getByLabel(/Bloquea la publicación/).check();
    await expect(summary).toContainText('RECHAZADO');
    await expect(summary).toContainText('bloqueante');
    await page.getByRole('button', { name: 'Guardar revisión' }).click();
    await expect(page.getByRole('alert')).toContainText('hallazgos bloqueantes');
    await page.getByLabel('Filtro creativo').selectOption('rechazado');
    await page.getByRole('button', { name: 'Guardar revisión' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Revisión guardada' })).toBeVisible();
    await expect(page.getByRole('list', { name: 'Revisiones guardadas' })).toContainText(
      'RECHAZADO',
    );

    // Persiste tras recargar y avisa en Respaldo.
    await page.reload();
    await nav(page, 'Revisión');
    await page.getByLabel('¿Qué vas a revisar?').selectOption({ label: 'Principal' });
    await expect(page.getByLabel(/^Claridad del mensaje/)).toHaveValue('15');
    await expect(page.getByRole('status', { name: 'Resumen de la revisión' })).toContainText(
      'RECHAZADO',
    );
    await nav(page, 'Respaldo');
    await expect(page.getByRole('note')).toContainText('1 revisiones de calidad');

    await nav(page, 'Revisión');
    await page.getByRole('button', { name: 'Copiar prompt maestro' }).isVisible();
    expect(errors).toEqual([]);
  });
});
