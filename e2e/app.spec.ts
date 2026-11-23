import { expect, test } from '@playwright/test';
import { axeViolations, PREVIEW, trackErrors } from './support';

// Build de PREVIEW (modo "preview", DEMO) servido con `vite preview`: no es producción ni tiene backend.
test.describe('aplicación (build preview) en Chrome real', () => {
  test('arranca, muestra aviso DEMO, identidad ficticia y estado "sin backend"', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(PREVIEW);
    await expect(
      page.getByRole('heading', { level: 1, name: 'Copy Creative Intelligence' }),
    ).toBeVisible();
    await expect(page.getByRole('region', { name: 'Aviso de modo DEMO' })).toContainText(
      'MODO DEMO',
    );
    await expect(page.getByText('Sin actividad reciente')).toBeVisible();
    await expect(page.getByRole('status')).toHaveText('Contenido cargado.');
    expect(errors).toEqual([]);
  });

  test('navega a Estado de conexión: foco en el encabezado, título, aria-current y aviso de no conexión', async ({
    page,
  }) => {
    await page.goto(PREVIEW);
    await page.getByRole('button', { name: 'Estado de conexión' }).click();
    const h2 = page.getByRole('heading', { level: 2, name: 'Estado de conexión' });
    await expect(h2).toBeFocused();
    await expect(page).toHaveTitle(/Estado de conexión/);
    await expect(page.getByRole('button', { name: 'Estado de conexión' })).toHaveAttribute(
      'aria-current',
      'page',
    );
    await expect(page.getByRole('note')).toContainText('no está conectada a ningún backend');
    await expect(page.getByText('Entorno:')).toContainText('preview');
    await expect(
      page.getByRole('region', { name: 'Estado de la aplicación (JSON)' }),
    ).toContainText('"isDemo": true');
  });

  test('teclado: enlace de salto, orden de tabulación y activación con Enter/Espacio', async ({
    page,
  }) => {
    await page.goto(PREVIEW);
    await expect(page.getByRole('status')).toHaveText('Contenido cargado.');
    await page.keyboard.press('Tab');
    const skip = page.getByRole('link', { name: 'Saltar al contenido' });
    await expect(skip).toBeFocused();
    await expect(skip).toBeInViewport(); // visible al recibir foco
    await page.keyboard.press('Enter');
    expect(await page.evaluate(() => document.activeElement?.id)).toBe('contenido');

    await page.keyboard.press('Tab'); // continúa desde el contenido
    await page.goto(PREVIEW);
    await expect(page.getByRole('status')).toHaveText('Contenido cargado.');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Inicio' })).toBeFocused();
    await page.keyboard.press('Tab');
    await expect(page.getByRole('button', { name: 'Estado de conexión' })).toBeFocused();
    await page.keyboard.press('Enter');
    await expect(page.getByRole('heading', { level: 2, name: 'Estado de conexión' })).toBeFocused();
    // Desde el encabezado, hacia atrás: Respaldo → Almacenamiento → Perfil y preferencias → Estado de conexión → Inicio.
    for (let i = 0; i < 5; i++) await page.keyboard.press('Shift+Tab');
    await expect(page.getByRole('button', { name: 'Inicio' })).toBeFocused();
    await page.keyboard.press('Space');
    await expect(page.getByRole('heading', { level: 2, name: 'Resumen' })).toBeFocused();
  });

  test('foco visible: contorno de al menos 3px en botones y enlace de salto con teclado', async ({
    page,
  }) => {
    await page.goto(PREVIEW);
    // Esperar a que la interfaz esté montada: si Tab se pulsa antes, se pierde y el foco queda en <body> o en el
    // enlace de salto (causa verificada: 4 de 60 corridas sin espera; 0 de 60 con espera; ver evidencia S1.2).
    await expect(page.getByRole('status')).toHaveText('Contenido cargado.');
    await page.keyboard.press('Tab');
    await page.keyboard.press('Tab');
    const outline = await page.evaluate(() => {
      const cs = getComputedStyle(document.activeElement as Element);
      return { style: cs.outlineStyle, width: parseFloat(cs.outlineWidth) };
    });
    expect(outline.style).not.toBe('none');
    expect(outline.width).toBeGreaterThanOrEqual(3);
  });

  test('región JSON desplazable es accesible por teclado', async ({ page }) => {
    await page.goto(PREVIEW);
    await page.getByRole('button', { name: 'Estado de conexión' }).click();
    const region = page.getByRole('region', { name: 'Estado de la aplicación (JSON)' });
    await region.focus();
    await expect(region).toBeFocused();
  });

  for (const nombre of ['Inicio', 'Estado de conexión']) {
    test(`axe-core (WCAG 2.x A/AA + best-practice) sin violaciones: ${nombre}`, async ({
      page,
    }) => {
      await page.goto(PREVIEW);
      if (nombre !== 'Inicio') await page.getByRole('button', { name: nombre }).click();
      await expect(page.getByRole('status')).toHaveText('Contenido cargado.');
      expect(await axeViolations(page)).toEqual([]);
    });
  }
});
