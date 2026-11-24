import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

const nav = async (page: Page, name: string) => {
  await page.getByRole('button', { name, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name })).toBeFocused();
};

test.describe('medición, promociones, biblioteca y plantillas (modo local, Chrome real)', () => {
  test('medición: resultado manual, CSV todo-o-nada y experimento A/B con aviso de muestra', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Medición');
    expect(await axeViolations(page)).toEqual([]);

    const form = page.getByRole('form', { name: 'Resultado manual' });
    await form.getByLabel(/^Nombre/).fill('Banner Buen Fin');
    await form.getByLabel(/^Impresiones/).fill('1000');
    await form.getByLabel(/^Clics/).fill('50');
    await form.getByLabel(/^Conversiones/).fill('5');
    await form.getByRole('button', { name: 'Guardar resultado' }).click();
    await expect(page.getByText('Resultado guardado.')).toBeVisible();
    await expect(page.getByRole('list', { name: 'Registros de medición' })).toContainText(
      'Banner Buen Fin',
    );
    await expect(page.getByRole('list', { name: 'Registros de medición' })).toContainText('5');

    // Cifras imposibles se rechazan.
    await form.getByLabel(/^Nombre/).fill('Mal');
    await form.getByLabel(/^Impresiones/).fill('10');
    await form.getByLabel(/^Clics/).fill('50');
    await form.getByLabel(/^Conversiones/).fill('1');
    await form.getByRole('button', { name: 'Guardar resultado' }).click();
    await expect(page.getByRole('alert')).toBeVisible();

    // CSV con una fila mala: no importa nada.
    await page.getByLabel('Archivo CSV de resultados').setInputFiles({
      name: 'malo.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from('objetivo,impresiones,clics,conversiones\nA,100,10,1\nB,10,50,1\n'),
    });
    await expect(page.getByRole('alert')).toContainText('Fila 3');
    await page.getByLabel('Archivo CSV de resultados').setInputFiles({
      name: 'ok.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(
        'objetivo;impresiones;clics;conversiones\nEmail A;2000;100;10\nEmail B;2000;140;20\n',
      ),
    });
    await expect(page.getByText('Se importaron 2 resultados.')).toBeVisible();

    // Experimento con muestra pequeña: se avisa y no se declara ganador.
    const exp = page.getByRole('form', { name: 'Experimento A/B' });
    await exp.getByLabel('Nombre del experimento').fill('Titular con descuento');
    await exp.getByLabel('Hipótesis').fill('El descuento al inicio sube el CTR');
    await exp.getByLabel('Variable que cambia').fill('Titular');
    await exp.getByLabel('Impresiones A').fill('50');
    await exp.getByLabel('Clics A').fill('5');
    await exp.getByLabel('Conversiones A').fill('1');
    await exp.getByLabel('Impresiones B').fill('50');
    await exp.getByLabel('Clics B').fill('9');
    await exp.getByLabel('Conversiones B').fill('2');
    await exp.getByRole('button', { name: 'Guardar experimento' }).click();
    await expect(page.getByText('Experimento guardado.')).toBeVisible();
    await expect(page.getByRole('list', { name: 'Registros de medición' })).toContainText(
      'Muestra pequeña',
    );
    expect(await axeViolations(page)).toEqual([]);

    // Persiste tras recargar y alimenta la Biblioteca.
    await page.reload();
    await nav(page, 'Medición');
    await expect(page.getByRole('list', { name: 'Registros de medición' })).toContainText(
      'Email B',
    );
    await nav(page, 'Biblioteca');
    await expect(page.getByRole('list', { name: 'Mejores resultados' })).toContainText('Email B');
    expect(await axeViolations(page)).toEqual([]);
    expect(errors).toEqual([]);
  });

  test('promociones: CSV, validación contra texto pegado y restauración del respaldo de recursos', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Promociones');
    expect(await axeViolations(page)).toEqual([]);
    await page.getByLabel('Archivo CSV de promociones').setInputFiles({
      name: 'promos.csv',
      mimeType: 'text/csv',
      buffer: Buffer.from(
        'nombre,porcentaje,sku,desde,hasta,restricciones\nBuen Fin,20%,A1,2020-01-01,2099-12-31,Solo en línea\nBuen Fin,,B2,,,\nVieja,10,C3,2020-01-01,2020-02-01,\n',
      ),
    });
    await expect(page.getByText('Se importaron 2 promociones.')).toBeVisible();
    await expect(page.getByRole('list', { name: 'Promociones guardadas' })).toContainText('2 SKUs');

    await page.getByLabel('Promoción', { exact: true }).selectOption({ label: 'Buen Fin' });
    await page.getByLabel('Texto a validar').selectOption('pegado');
    const result = page.getByRole('status', { name: 'Resultado de la validación' });
    await page.getByLabel('Texto pegado').fill('Aprovecha 30% de descuento');
    await expect(result).toContainText('dice 30 %');
    await page
      .getByLabel('Texto pegado')
      .fill('Aprovecha 20% de descuento. Aplican restricciones.');
    await expect(result).toContainText('Sin diferencias');
    await page.getByLabel('Promoción', { exact: true }).selectOption({ label: 'Vieja' });
    await page.getByLabel('Texto pegado').fill('10% de descuento');
    await expect(result).toContainText('venció');
    expect(await axeViolations(page)).toEqual([]);

    // Se informa en Respaldo que las promociones no van en el respaldo de datos.
    await nav(page, 'Respaldo');
    await expect(page.getByRole('note').first()).toContainText('2 promociones');
    expect(errors).toEqual([]);
  });

  test('plantillas: borradores solo con los datos escritos; la urgencia exige vigencia', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await nav(page, 'Plantillas');
    expect(await axeViolations(page)).toEqual([]);
    const drafts = page.getByRole('list', { name: 'Borradores' });
    await expect(page.getByText('Escribe al menos una oferta o un beneficio')).toBeVisible();
    await page.getByLabel(/^Oferta/).fill('20% de descuento');
    await page.getByLabel(/^Producto/).fill('productos participantes');
    await page.getByLabel(/^CTA/).fill('Compra ahora');
    await expect(drafts).toContainText('20% de descuento en productos participantes');
    await expect(drafts).not.toContainText('Últimos días');
    await page.getByLabel(/^Vigencia/).fill('hasta el 30 de noviembre');
    await expect(drafts).toContainText('Últimos días');
    await expect(page.getByRole('table')).toContainText('WhatsApp');
    expect(await axeViolations(page)).toEqual([]);
    expect(errors).toEqual([]);
  });

  test('revisión: flujo con etapa y aprobación final; recordatorio semanal en Inicio', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await expect(page.getByRole('note').filter({ hasText: 'Recordatorio semanal' })).toBeVisible();
    await nav(page, 'Briefs');
    await page.getByRole('button', { name: 'Nuevo brief' }).click();
    await page.getByLabel(/^Campaña/).fill('Flujo');
    await page.getByLabel(/^Canal/).selectOption('Email');
    await page.getByRole('button', { name: 'Guardar brief' }).click();
    await page.getByRole('button', { name: 'Copys de Flujo' }).click();
    await page.getByRole('button', { name: 'Nuevo copy' }).click();
    await page.getByLabel(/^Titular/).fill('Aprovecha 20% de descuento');
    await page.getByRole('button', { name: 'Crear copy' }).click();

    await nav(page, 'Revisión');
    await page.getByLabel('¿Qué vas a revisar?').selectOption({ label: 'Principal' });
    // Liberar sin ser publicable se rechaza.
    await page.getByLabel('Aprobación final').selectOption({ label: 'Liberada para publicar' });
    await page.getByLabel('Quién aprueba').fill('Ana');
    await page.getByRole('button', { name: 'Guardar revisión' }).click();
    await expect(page.getByRole('alert')).toContainText('publicable');
    await page.getByLabel('Aprobación final').selectOption({ label: 'Pendiente' });
    await page.getByLabel('Etapa').selectOption({ label: 'Aprobación' });
    await page.getByRole('button', { name: 'Guardar revisión' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Revisión guardada' })).toBeVisible();
    await expect(page.getByRole('list', { name: 'Revisiones guardadas' })).toContainText(
      'Aprobación',
    );
    // Con una revisión reciente, el recordatorio desaparece.
    await page.getByRole('button', { name: 'Inicio', exact: true }).click();
    await expect(page.getByRole('note').filter({ hasText: 'Recordatorio semanal' })).toHaveCount(0);
    expect(await axeViolations(page)).toEqual([]);
    expect(errors).toEqual([]);
  });
});

test('tablero: cuenta lo pendiente y avisa de promociones vencidas; resultado vinculado alimenta la biblioteca', async ({
  page,
}) => {
  const errors = trackErrors(page);
  await page.goto(LOCAL);
  await nav(page, 'Briefs');
  await page.getByRole('button', { name: 'Nuevo brief' }).click();
  await page.getByLabel(/^Campaña/).fill('Tablero');
  await page.getByLabel(/^Canal/).selectOption('Email');
  await page.getByRole('button', { name: 'Guardar brief' }).click();
  await page.getByRole('button', { name: 'Copys de Tablero' }).click();
  await page.getByRole('button', { name: 'Nuevo copy' }).click();
  await page.getByLabel(/^Titular/).fill('Ahorra hoy en tu salud');
  await page.getByLabel(/^CTA/).fill('Compra ahora');
  await page.getByRole('button', { name: 'Crear copy' }).click();

  await nav(page, 'Promociones');
  await page.getByLabel('Archivo CSV de promociones').setInputFiles({
    name: 'p.csv',
    mimeType: 'text/csv',
    buffer: Buffer.from('nombre,porcentaje,desde,hasta\nVieja,10,2020-01-01,2020-02-01\n'),
  });
  await expect(page.getByText('Se importaron 1 promociones.')).toBeVisible();

  await nav(page, 'Medición');
  const form = page.getByRole('form', { name: 'Resultado manual' });
  await form.getByLabel(/^Nombre/).fill('Email Tablero');
  await form.getByLabel('Vinculado a (opcional)').selectOption({ label: 'Principal' });
  await form.getByLabel(/^Impresiones/).fill('1000');
  await form.getByLabel(/^Clics/).fill('80');
  await form.getByLabel(/^Conversiones/).fill('8');
  await form.getByRole('button', { name: 'Guardar resultado' }).click();
  await expect(page.getByText('Resultado guardado.')).toBeVisible();

  await nav(page, 'Biblioteca');
  await expect(page.getByRole('list', { name: 'Titulares y CTA con mejor CTR' })).toContainText(
    'Ahorra hoy en tu salud',
  );

  await page.getByRole('button', { name: 'Inicio', exact: true }).click();
  const board = page.getByRole('region', { name: 'Tablero de control' });
  await expect(board).toContainText('Sin revisar1');
  await expect(board).toContainText('Mediciones registradas1');
  await expect(board).toContainText('Promociones vencidas: Vieja');
  expect(await axeViolations(page)).toEqual([]);
  expect(errors).toEqual([]);
});
