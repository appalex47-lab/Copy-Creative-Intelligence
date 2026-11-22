import AxeBuilder from '@axe-core/playwright';
import type { Page } from '@playwright/test';

export const PREVIEW = 'http://localhost:4173';
export const DEV = 'http://localhost:5173';
export const EVIDENCE_DIR = process.env['CCI_EVIDENCE_DIR'] ?? 'test-results/capturas';

/** Registra errores de consola y excepciones de página para comprobar que no ocurren. */
export function trackErrors(page: Page): string[] {
  const errors: string[] = [];
  page.on('pageerror', (e) => errors.push(`pageerror: ${e.name}`));
  page.on('console', (m) => {
    if (m.type() === 'error') errors.push(`console.error: ${m.text().slice(0, 120)}`);
  });
  return errors;
}

export async function axeViolations(page: Page) {
  const results = await new AxeBuilder({ page })
    .withTags(['wcag2a', 'wcag2aa', 'wcag21a', 'wcag21aa', 'wcag22aa', 'best-practice'])
    .analyze();
  return results.violations.map((v) => ({
    id: v.id,
    impact: v.impact,
    nodes: v.nodes.length,
    help: v.help,
  }));
}
