import { expect, test } from '@playwright/test';
import { EVIDENCE_DIR, PREVIEW } from './support';

const WIDTHS = [360, 375, 390, 768, 1024, 1440];
const PAGES = [
  { id: 'inicio', nombre: 'Inicio' },
  { id: 'conexion', nombre: 'Estado de conexión' },
];

for (const width of WIDTHS) {
  for (const pagina of PAGES) {
    test(`responsive ${width}px — ${pagina.id}`, async ({ page }) => {
      await page.setViewportSize({ width, height: 800 });
      await page.goto(PREVIEW);
      if (pagina.id !== 'inicio') await page.getByRole('button', { name: pagina.nombre }).click();
      await expect(page.getByRole('status')).toHaveText('Contenido cargado.');

      const m = await page.evaluate(() => {
        const doc = document.documentElement;
        const vw = doc.clientWidth;
        // Elementos que se salen del viewport y NO están dentro de un contenedor con desplazamiento propio.
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
        const buttons = [...document.querySelectorAll<HTMLElement>('nav button')].map((b) => {
          const r = b.getBoundingClientRect();
          return { w: Math.round(r.width), h: Math.round(r.height) };
        });
        const fonts = parseFloat(getComputedStyle(document.body).fontSize);
        return { scrollW: doc.scrollWidth, vw, overflowing, buttons, fonts };
      });

      expect(m.scrollW, 'sin scroll horizontal del documento').toBeLessThanOrEqual(m.vw);
      expect(m.overflowing, 'ningún elemento se sale del viewport').toEqual([]);
      expect(m.fonts).toBeGreaterThanOrEqual(16);
      for (const b of m.buttons) {
        expect(b.h, 'altura mínima de control (WCAG 2.2 AA: 24px)').toBeGreaterThanOrEqual(24);
        expect(b.w).toBeGreaterThanOrEqual(24);
      }
      await page.screenshot({
        path: `${EVIDENCE_DIR}/responsive_${width}_${pagina.id}.png`,
        fullPage: true,
      });
    });
  }
}

test('responsive 360px — estado de error (arnés) sin desbordes', async ({ page }) => {
  await page.setViewportSize({ width: 360, height: 800 });
  await page.goto('http://localhost:5173/e2e/harness.html?s=unavailable');
  await expect(page.getByRole('alert')).toBeVisible();
  const sw = await page.evaluate(() => [
    document.documentElement.scrollWidth,
    document.documentElement.clientWidth,
  ]);
  expect(sw[0]).toBeLessThanOrEqual(sw[1] as number);
  await page.screenshot({ path: `${EVIDENCE_DIR}/responsive_360_error.png`, fullPage: true });
});
