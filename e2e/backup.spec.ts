import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';
import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

async function goto(page: Page, view: string) {
  await page.getByRole('button', { name: view, exact: true }).click();
  await expect(page.getByRole('heading', { level: 2, name: view })).toBeFocused();
}
async function setProfile(page: Page, name: string, theme?: string) {
  await goto(page, 'Perfil y preferencias');
  await page.getByLabel('Nombre visible (opcional)').fill(name);
  await page.getByRole('button', { name: 'Guardar nombre' }).click();
  await expect(page.getByText('Nombre guardado.')).toBeVisible();
  if (theme) await page.getByLabel('Tema').selectOption(theme);
}
async function exportFile(page: Page): Promise<{ path: string; text: string }> {
  await goto(page, 'Respaldo');
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    page.getByRole('button', { name: 'Exportar respaldo' }).click(),
  ]);
  expect(download.suggestedFilename()).toMatch(/^cci-respaldo-\d{8}-\d{6}\.json$/);
  const path = await download.path();
  return { path, text: readFileSync(path, 'utf8') };
}
const pick = (page: Page, name: string, buffer: Buffer) =>
  page
    .getByLabel('Archivo de respaldo (.json)')
    .setInputFiles({ name, mimeType: 'application/json', buffer });

test.describe('respaldo (modo local, Chrome real)', () => {
  test('exporta un archivo con el formato, los datos y la suma de integridad', async ({ page }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await setProfile(page, 'Ana', 'dark');
    const { text } = await exportFile(page);
    interface BackupFile {
      format: string;
      version: number;
      exportedAt: string;
      data: {
        profile: unknown;
        settings: { theme: string; lastBackupAt: string };
        activity: unknown[];
        briefs: unknown[];
        copies: unknown[];
        rules: unknown;
      };
      integrity: { value: string };
    }
    const f = JSON.parse(text) as BackupFile;
    expect(f.format).toBe('cci-backup');
    expect(f.version).toBe(5);
    expect(f.data.rules).toBeNull();
    expect(f.data.briefs).toEqual([]);
    expect(f.data.copies).toEqual([]);
    expect(f.data.profile).toEqual({ displayName: 'Ana' });
    expect(f.data.settings.theme).toBe('dark');
    expect(f.data.settings.lastBackupAt).toBe(f.exportedAt);
    expect(f.integrity.value).toMatch(/^[0-9a-f]{64}$/);
    expect(f.data.activity.length).toBeGreaterThan(0);
    await expect(page.getByRole('status').filter({ hasText: 'Respaldo exportado' })).toBeVisible();
    expect(await axeViolations(page)).toEqual([]);
    expect(errors).toEqual([]);
  });

  test('un respaldo v1 (anterior a los briefs) se sigue pudiendo importar', async ({ page }) => {
    await page.goto(LOCAL);
    await setProfile(page, 'Actual', 'light');
    const data = {
      profile: { displayName: 'Antiguo' },
      settings: {
        theme: 'dark',
        language: 'es',
        lastView: 'inicio',
        seenNotices: [],
        lastBackupAt: '2026-11-22T10:00:00.000Z',
      },
      activity: [],
    };
    const hash = createHash('sha256').update(JSON.stringify(data)).digest('hex');
    const v1 = JSON.stringify({
      format: 'cci-backup',
      version: 1,
      exportedAt: '2026-11-22T12:00:00.000Z',
      data,
      integrity: { algorithm: 'SHA-256', value: hash },
    });
    await goto(page, 'Respaldo');
    await pick(page, 'v1.json', Buffer.from(v1));
    const group = page.getByRole('group', { name: 'Confirmar importación' });
    await expect(group).toContainText('0 briefs');
    await page.getByRole('button', { name: 'Reemplazar todos los datos locales' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Respaldo importado' })).toBeVisible();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
  });

  test('importar reemplaza TODO tras confirmar; los datos persisten al recargar', async ({
    page,
  }) => {
    await page.goto(LOCAL);
    await setProfile(page, 'Ana', 'dark');
    const { text } = await exportFile(page);
    // Se cambian los datos y luego se restaura el respaldo.
    await setProfile(page, 'Cambiado', 'light');
    await goto(page, 'Respaldo');
    await pick(page, 'r.json', Buffer.from(text));
    const group = page.getByRole('group', { name: 'Confirmar importación' });
    await expect(group).toContainText('Importar reemplaza todos los datos locales actuales');
    // Antes de confirmar NO cambió nada.
    await page.reload();
    await goto(page, 'Perfil y preferencias');
    await expect(page.getByText('Nombre visible actual:')).toContainText('Cambiado');
    await goto(page, 'Respaldo');
    await pick(page, 'r.json', Buffer.from(text));
    await page.getByRole('button', { name: 'Reemplazar todos los datos locales' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Respaldo importado' })).toBeVisible();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await goto(page, 'Perfil y preferencias');
    await expect(page.getByText('Nombre visible actual:')).toContainText('Ana');
    await page.getByRole('button', { name: 'Inicio', exact: true }).click();
    await expect(page.getByRole('heading', { level: 2, name: 'Resumen' })).toBeFocused();
    await expect(
      page.locator('main').getByRole('listitem').filter({ hasText: 'Se importó un respaldo' }),
    ).toHaveCount(1);
    // Lo posterior al respaldo (el cambio a «Cambiado») fue reemplazado: solo queda el cambio de perfil del respaldo.
    await expect(
      page.locator('main').getByRole('listitem').filter({ hasText: 'Cambió el perfil local' }),
    ).toHaveCount(1);
  });

  test('un archivo alterado se rechaza (suma distinta) y no cambia nada', async ({ page }) => {
    await page.goto(LOCAL);
    await setProfile(page, 'Ana');
    const { text } = await exportFile(page);
    await setProfile(page, 'Original');
    await goto(page, 'Respaldo');
    await pick(
      page,
      'r.json',
      Buffer.from(text.replace('"displayName": "Ana"', '"displayName": "Eva"')),
    );
    await expect(page.getByRole('alert')).toContainText('dañado o fue modificado');
    await expect(page.getByRole('group', { name: 'Confirmar importación' })).toHaveCount(0);
    await goto(page, 'Perfil y preferencias');
    await expect(page.getByText('Nombre visible actual:')).toContainText('Original');
  });

  test('archivos inválidos (no JSON, otro formato, versión nueva) se rechazan con motivo propio', async ({
    page,
  }) => {
    await page.goto(LOCAL);
    await setProfile(page, 'Ana');
    const { text } = await exportFile(page);
    const cases: [Buffer, string][] = [
      [Buffer.from('esto no es json SECRETO'), 'no es JSON'],
      [Buffer.from('{"format":"otro"}'), 'no es un respaldo de Copy Creative Intelligence'],
      [Buffer.from(text.replace('"version": 5', '"version": 6')), 'versión más reciente'],
    ];
    for (const [buf, motivo] of cases) {
      await pick(page, 'r.json', buf);
      const alert = page.getByRole('alert');
      await expect(alert).toContainText(motivo);
      expect(await alert.textContent()).not.toContain('SECRETO');
      await expect(page.getByRole('group', { name: 'Confirmar importación' })).toHaveCount(0);
    }
  });

  test('cancelar no cambia ningún dato', async ({ page }) => {
    await page.goto(LOCAL);
    await setProfile(page, 'Ana');
    const { text } = await exportFile(page);
    await setProfile(page, 'Otro');
    await goto(page, 'Respaldo');
    await pick(page, 'r.json', Buffer.from(text));
    await page.getByRole('button', { name: 'Cancelar' }).click();
    await expect(page.getByText('Importación cancelada. No se cambió ningún dato.')).toBeVisible();
    await goto(page, 'Perfil y preferencias');
    await expect(page.getByText('Nombre visible actual:')).toContainText('Otro');
  });
});
