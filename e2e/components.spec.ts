import { expect, test } from '@playwright/test';
import { axeViolations, DEV, EVIDENCE_DIR } from './support';

// AC1-04 y la parte de componentes de AC1-13: axe y teclado reales sobre la galería de componentes.
const WIDTHS = [320, 768, 1440];

for (const width of WIDTHS) {
  test(`galería de componentes ${width}px: sin violaciones axe, sin desbordamiento`, async ({
    page,
  }) => {
    await page.setViewportSize({ width, height: 800 });
    await page.goto(`${DEV}/e2e/gallery.html`);
    await expect(
      page.getByRole('heading', { level: 1, name: 'Galería de componentes' }),
    ).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);
    const overflow = await page.evaluate(
      () => document.documentElement.scrollWidth - document.documentElement.clientWidth,
    );
    expect(overflow).toBeLessThanOrEqual(0);
    await page.screenshot({ path: `${EVIDENCE_DIR}/galeria_${width}.png`, fullPage: true });
  });
}

test('galería de componentes: foco visible de al menos 3px en cada botón habilitado', async ({
  page,
}) => {
  await page.goto(`${DEV}/e2e/gallery.html`);
  await expect(page.getByRole('heading', { level: 1 })).toBeVisible();
  for (const name of ['Principal', 'Secundario', 'Entendido']) {
    await page.getByRole('button', { name }).focus();
    const o = await page.evaluate(() => {
      const cs = getComputedStyle(document.activeElement as Element);
      return { style: cs.outlineStyle, width: parseFloat(cs.outlineWidth) };
    });
    expect(o.style, name).not.toBe('none');
    expect(o.width, name).toBeGreaterThanOrEqual(3);
  }
  await expect(page.getByRole('button', { name: 'Deshabilitado' })).toBeDisabled();
});
