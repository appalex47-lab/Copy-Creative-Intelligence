import { expect, test } from '@playwright/test';
import { axeViolations, EVIDENCE_DIR, LOCAL, trackErrors } from './support';

// Cierre de la Fase 1 (S1.11): todas las vistas del modo local, en todos los anchos y en ambos temas.
const WIDTHS = [320, 360, 375, 390, 768, 1024, 1440];
const VIEWS = [
  { nav: 'Inicio', h2: 'Resumen' },
  { nav: 'Estado de conexión', h2: 'Estado de conexión' },
  { nav: 'Perfil y preferencias', h2: 'Perfil y preferencias' },
  { nav: 'Almacenamiento', h2: 'Almacenamiento' },
  { nav: 'Respaldo', h2: 'Respaldo' },
];

for (const width of WIDTHS) {
  test(`local ${width}px: todas las vistas sin desbordes, controles ≥24px y texto ≥16px`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height: 800 });
    await page.goto(LOCAL);
    for (const [i, v] of VIEWS.entries()) {
      await page.getByRole('button', { name: v.nav, exact: true }).click();
      // El foco se mueve al encabezado solo al CAMBIAR de vista (Inicio ya está activa al cargar).
      if (i > 0) await expect(page.getByRole('heading', { level: 2, name: v.h2 })).toBeFocused();
      else await expect(page.getByRole('heading', { level: 2, name: v.h2 })).toBeVisible();
      await expect(page.getByRole('status').first()).toBeAttached();
      const m = await page.evaluate(() => {
        const doc = document.documentElement;
        const vw = doc.clientWidth;
        const overflowing = [...document.body.querySelectorAll<HTMLElement>('*')]
          .filter((el) => {
            const r = el.getBoundingClientRect();
            if (r.width === 0 || r.right <= vw + 0.5) return false;
            for (let p: HTMLElement | null = el.parentElement; p; p = p.parentElement) {
              const o = getComputedStyle(p).overflowX;
              if (o === 'auto' || o === 'scroll') return false;
            }
            return true;
          })
          .map((el) => el.tagName.toLowerCase() + '.' + el.className);
        const small = [...document.querySelectorAll<HTMLElement>('button, input, select')]
          .filter((el) => el.getAttribute('type') !== 'file')
          .map((el) => el.getBoundingClientRect())
          .filter((r) => r.height < 24 || r.width < 24).length;
        return {
          scrollW: doc.scrollWidth,
          vw,
          overflowing,
          small,
          font: parseFloat(getComputedStyle(document.body).fontSize),
        };
      });
      expect(m.scrollW, `${v.nav}: scroll horizontal`).toBeLessThanOrEqual(m.vw);
      expect(m.overflowing, `${v.nav}: elementos fuera del viewport`).toEqual([]);
      expect(m.small, `${v.nav}: controles pequeños`).toBe(0);
      expect(m.font).toBeGreaterThanOrEqual(16);
    }
    await page.screenshot({ path: `${EVIDENCE_DIR}/local_${width}_respaldo.png`, fullPage: true });
  });
}

for (const theme of ['light', 'dark'] as const) {
  test(`axe (WCAG 2.2 AA) en todas las vistas con tema ${theme}, sin errores de consola`, async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await page.getByRole('button', { name: 'Perfil y preferencias', exact: true }).click();
    await page.getByLabel('Tema').selectOption(theme);
    await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
    for (const v of VIEWS) {
      await page.getByRole('button', { name: v.nav, exact: true }).click();
      await expect(page.getByRole('heading', { level: 2, name: v.h2 })).toBeVisible();
      await expect(page.getByRole('status').first()).toBeAttached();
      expect(await axeViolations(page), v.nav).toEqual([]);
    }
    expect(errors).toEqual([]);
  });
}

test('teclado: cada vista se activa con Enter desde su botón y el foco pasa a su encabezado', async ({
  page,
}) => {
  await page.goto(LOCAL);
  await page.keyboard.press('Tab'); // enlace de salto
  await page.keyboard.press('Tab'); // primer botón de navegación (Inicio, ya activa)
  for (const [i, v] of VIEWS.entries()) {
    await expect(page.getByRole('button', { name: v.nav, exact: true })).toBeFocused();
    await page.keyboard.press('Enter');
    if (i > 0) {
      await expect(page.getByRole('heading', { level: 2, name: v.h2 })).toBeFocused();
      // Hacia atrás desde el encabezado: último botón de la navegación, y así hasta el de esta vista.
      for (let k = 0; k < VIEWS.length - i; k++) await page.keyboard.press('Shift+Tab');
      await expect(page.getByRole('button', { name: v.nav, exact: true })).toBeFocused();
    }
    await page.keyboard.press('Tab'); // al siguiente botón de navegación
  }
});
