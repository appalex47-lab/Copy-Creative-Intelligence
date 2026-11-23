import { expect, test, type Page } from '@playwright/test';
import { axeViolations, DEV, EVIDENCE_DIR, trackErrors } from './support';

// Arnés sobre el servidor de desarrollo (React StrictMode activo): la <App> real con servicios que fallan/retrasan.
const open = (page: Page, s: string) => page.goto(`${DEV}/e2e/harness.html?s=${s}`);
const calls = (page: Page) => page.evaluate(() => window.__cci.calls);

test.describe('estados de carga, error y reintento en Chrome real (StrictMode)', () => {
  test('carga: región de estado anuncia "Cargando…" y luego "Contenido cargado."', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await open(page, 'gated');
    const status = page.getByRole('status');
    await expect(status).toHaveText('Cargando…');
    await expect(status).toHaveAttribute('aria-live', 'polite');
    await page.screenshot({ path: `${EVIDENCE_DIR}/estado_carga_desktop.png` });
    await page.evaluate(() => window.__cci.release());
    await expect(page.getByText('Sin actividad reciente')).toBeVisible();
    await expect(status).toHaveText('Contenido cargado.');
    expect(errors).toEqual([]);
  });

  test('StrictMode: el efecto se ejecuta dos veces en desarrollo pero la UI queda coherente y sin robar foco', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await open(page, 'ok');
    await expect(page.getByText('Sin actividad reciente')).toBeVisible();
    expect((await calls(page)).activity).toBeGreaterThanOrEqual(2); // doble montaje de StrictMode
    expect(await page.evaluate(() => document.activeElement === document.body)).toBe(true);
    await expect(page.getByText('Sin actividad reciente')).toHaveCount(1);
    expect(errors).toEqual([]);
  });

  test('Result fallido "unavailable": alerta sin detalle interno, reintento y recuperación', async ({
    page,
  }) => {
    await open(page, 'unavailable');
    const alert = page.getByRole('alert');
    await expect(alert).toContainText('no está disponible');
    await expect(page.locator('body')).not.toContainText('DETALLE_INTERNO');
    await page.screenshot({ path: `${EVIDENCE_DIR}/estado_error_desktop.png` });
    expect(await axeViolations(page)).toEqual([]);
    await page.evaluate(() => window.__cci.heal());
    await page.getByRole('button', { name: 'Reintentar' }).click();
    await expect(page.getByText('Sin actividad reciente')).toBeVisible();
    await expect(page.getByRole('alert')).toHaveCount(0);
  });

  test('tras reintentar el foco no se pierde (queda en el encabezado)', async ({ page }) => {
    await open(page, 'unavailable');
    await expect(page.getByRole('alert')).toBeVisible();
    await page.evaluate(() => window.__cci.heal());
    await page.getByRole('button', { name: 'Reintentar' }).click();
    await expect(page.getByText('Sin actividad reciente')).toBeVisible();
    await expect(page.getByRole('heading', { level: 2, name: 'Resumen' })).toBeFocused();
  });

  test('excepción del servicio: error genérico, sin detalles, con reintento', async ({ page }) => {
    const errors = trackErrors(page);
    await open(page, 'throw');
    await expect(page.getByRole('alert')).toContainText('Ocurrió un error inesperado');
    await expect(page.locator('body')).not.toContainText('DETALLE_INTERNO');
    await page.evaluate(() => window.__cci.heal());
    await page.getByRole('button', { name: 'Reintentar' }).click();
    await expect(page.getByText('Sin actividad reciente')).toBeVisible();
    // Solo se registra el tipo de error (nombre), nunca el mensaje.
    expect(errors.join('\n')).not.toContain('DETALLE_INTERNO');
  });

  test('not_found: alerta visible y SIN botón de reintento', async ({ page }) => {
    await open(page, 'notfound');
    await expect(page.getByRole('alert')).toContainText('No se encontró');
    await expect(page.getByRole('button', { name: 'Reintentar' })).toHaveCount(0);
  });

  test('Error Boundary: un error real de renderizado se captura, no deja pantalla en blanco y permite reintentar', async ({
    page,
  }) => {
    await open(page, 'render-bomb');
    const alert = page.getByRole('alert');
    await expect(alert).toContainText('Ocurrió un error inesperado');
    await expect(page.getByRole('navigation', { name: 'Navegación principal' })).toBeVisible(); // el layout sigue vivo
    await expect(page.locator('body')).not.toContainText('Objects are not valid');
    // Navegar a otra página (el boundary se reinicia por página) sigue funcionando.
    await page.getByRole('button', { name: 'Estado de conexión' }).click();
    await expect(page.getByRole('note')).toContainText('no está conectada a ningún backend');
  });

  test('respuesta tardía tras cambiar de página: se descarta y no contamina la página nueva', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await open(page, 'gated');
    await expect(page.getByRole('status')).toHaveText('Cargando…');
    await page.getByRole('button', { name: 'Estado de conexión' }).click(); // cambia de página durante la petición
    await expect(page.getByRole('heading', { level: 2, name: 'Estado de conexión' })).toBeFocused();
    await page.evaluate(() => window.__cci.release()); // ahora llegan las respuestas retenidas (también la de Inicio)
    await expect(
      page.getByRole('region', { name: 'Estado de la aplicación (JSON)' }),
    ).toBeVisible();
    await expect(page.getByText('Sin actividad reciente')).toHaveCount(0); // la respuesta tardía de Inicio no aparece aquí
    // Volver a Inicio carga de nuevo (nueva solicitud).
    await page.getByRole('button', { name: 'Inicio' }).click();
    await page.evaluate(() => window.__cci.release());
    await expect(page.getByText('Sin actividad reciente')).toBeVisible();
    expect(errors).toEqual([]);
  });

  test('error en Estado de conexión: el aviso "sin backend" se mantiene visible', async ({
    page,
  }) => {
    await open(page, 'state-unavailable');
    await page.getByRole('button', { name: 'Estado de conexión' }).click();
    await expect(page.getByRole('alert')).toBeVisible();
    await expect(page.getByRole('note')).toContainText('no está conectada a ningún backend');
  });
});
