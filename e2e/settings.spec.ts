import { expect, test, type Page } from '@playwright/test';
import { axeViolations, LOCAL, trackErrors } from './support';

// Modo de datos LOCAL (IndexedDB + Local Storage reales). Cada test usa un contexto nuevo (almacenamiento limpio).
async function openSettings(page: Page) {
  await page.goto(LOCAL);
  await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
  await expect(
    page.getByRole('heading', { level: 2, name: 'Perfil y preferencias' }),
  ).toBeFocused();
}

test.describe('perfil y preferencias (modo local, Chrome real)', () => {
  test('sin aviso DEMO y con el modo real indicado', async ({ page }) => {
    await page.goto(LOCAL);
    await expect(page.getByRole('region', { name: 'Aviso de modo DEMO' })).toHaveCount(0);
    await expect(page).not.toHaveTitle(/DEMO/);
    await page.getByRole('button', { name: 'Estado de conexión' }).click();
    await expect(page.getByText('Modo de datos:')).toContainText('LOCAL');
  });

  test('guardar el nombre persiste tras recargar; borrarlo lo elimina', async ({ page }) => {
    const errors = trackErrors(page);
    await openSettings(page);
    await page.getByLabel('Nombre visible (opcional)').fill('  Alejandro  ');
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByRole('status').filter({ hasText: 'Nombre guardado.' })).toBeVisible();
    await page.reload();
    await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
    await expect(page.getByText('Nombre visible actual:')).toContainText('Alejandro');
    await expect(page.getByLabel('Nombre visible (opcional)')).toHaveValue('Alejandro');
    await page.getByRole('button', { name: 'Borrar nombre' }).click();
    await expect(page.getByText('Nombre visible actual:')).toContainText('sin nombre');
    await page.reload();
    await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
    await expect(page.getByText('Nombre visible actual:')).toContainText('sin nombre');
    expect(errors).toEqual([]);
  });

  test('un nombre inválido muestra el motivo y no se guarda; el texto se muestra escapado', async ({
    page,
  }) => {
    await openSettings(page);
    await page.getByLabel('Nombre visible (opcional)').fill('x'.repeat(61));
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByRole('alert')).toContainText('60');
    await expect(page.getByText('Nombre visible actual:')).toContainText('sin nombre');
    await page.getByLabel('Nombre visible (opcional)').fill('<img src=x onerror=alert(1)>');
    await page.getByRole('button', { name: 'Guardar nombre' }).click();
    await expect(page.getByText('Nombre visible actual:')).toContainText('<img src=x');
    await expect(page.locator('main img')).toHaveCount(0);
  });

  test('el tema oscuro se aplica y persiste tras recargar', async ({ page }) => {
    await openSettings(page);
    await page.getByLabel('Tema').selectOption('dark');
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await page.reload();
    await expect(page.locator('html')).toHaveAttribute('data-theme', 'dark');
    await page.getByRole('button', { name: 'Perfil y preferencias' }).click();
    await expect(page.getByLabel('Tema')).toHaveValue('dark');
    await page.getByLabel('Tema').selectOption('system');
    await expect(page.locator('html')).not.toHaveAttribute('data-theme', /.+/);
  });

  for (const theme of ['light', 'dark'] as const) {
    test(`accesibilidad (axe) de Perfil y preferencias con tema ${theme}`, async ({ page }) => {
      await openSettings(page);
      await page.getByLabel('Tema').selectOption(theme);
      await expect(page.locator('html')).toHaveAttribute('data-theme', theme);
      await page.getByLabel('Nombre visible (opcional)').fill('x'.repeat(61));
      await page.getByRole('button', { name: 'Guardar nombre' }).click();
      await expect(page.getByRole('alert')).toBeVisible();
      expect(await axeViolations(page)).toEqual([]);
    });
  }

  test('sin desbordamiento horizontal en anchos de 320 a 1440', async ({ page }) => {
    await openSettings(page);
    for (const width of [320, 375, 768, 1440]) {
      await page.setViewportSize({ width, height: 800 });
      const overflow = await page.evaluate(
        () => document.documentElement.scrollWidth > document.documentElement.clientWidth,
      );
      expect(overflow, `ancho ${width}`).toBe(false);
    }
  });

  test('AC1-08: base con esquema más nuevo → mensaje propio, sin reintento y sin modificar nada', async ({
    page,
  }) => {
    // Se siembra desde una página del mismo origen que no abre la base 'cci' (si no, su conexión bloquearía la siembra).
    await page.goto(`${LOCAL}/e2e/idb.html`);
    await page.evaluate(
      () =>
        new Promise<void>((resolve, reject) => {
          const r = indexedDB.open('cci', 99);
          r.onupgradeneeded = () => r.result.createObjectStore('centinela');
          r.onsuccess = () => {
            r.result.close();
            resolve();
          };
          r.onerror = () => reject(new Error('no se pudo crear'));
        }),
    );
    await page.goto(LOCAL);
    const alert = page.getByRole('alert');
    await expect(alert).toContainText('versión más reciente de la aplicación');
    await expect(alert.getByRole('button', { name: 'Reintentar' })).toHaveCount(0);
    const version = await page.evaluate(
      () =>
        new Promise<number>((resolve) => {
          const r = indexedDB.open('cci');
          r.onsuccess = () => {
            const v = r.result.version;
            r.result.close();
            resolve(v);
          };
        }),
    );
    expect(version).toBe(99);
  });

  test('AC1-08: Local Storage sin espacio → mensaje de espacio y el tema no cambia', async ({
    page,
  }) => {
    await page.addInitScript(() => {
      Storage.prototype.setItem = () => {
        throw new DOMException('interno', 'QuotaExceededError');
      };
    });
    await openSettings(page);
    await page.getByLabel('Tema').selectOption('dark');
    await expect(page.getByRole('alert')).toContainText('No hay espacio suficiente');
    await expect(page.locator('html')).not.toHaveAttribute('data-theme', /.+/);
    expect(await axeViolations(page)).toEqual([]);
  });

  test('Almacenamiento: muestra cifras del navegador o «No disponible», sin errores', async ({
    page,
  }) => {
    const errors = trackErrors(page);
    await page.goto(LOCAL);
    await page.getByRole('button', { name: 'Almacenamiento' }).click();
    await expect(page.getByRole('heading', { level: 2, name: 'Almacenamiento' })).toBeFocused();
    const dd = page.locator('dd');
    await expect(dd).toHaveCount(3);
    for (const text of await dd.allTextContents()) expect(text).not.toMatch(/NaN|undefined|null/);
    expect(await axeViolations(page)).toEqual([]);
    expect(errors).toEqual([]);
  });

  test('Almacenamiento: navegador que no expone datos → «No disponible» en las tres filas', async ({
    page,
  }) => {
    await page.addInitScript(() => {
      Object.defineProperty(navigator, 'storage', { value: undefined, configurable: true });
    });
    await page.goto(LOCAL);
    await page.getByRole('button', { name: 'Almacenamiento' }).click();
    await expect(page.locator('dd')).toHaveText([
      'No disponible',
      'No disponible',
      'No disponible',
    ]);
    await expect(
      page.getByRole('button', { name: 'Solicitar almacenamiento persistente' }),
    ).toBeDisabled();
  });

  test('Almacenamiento: cifras simuladas y solicitud de persistencia concedida', async ({
    page,
  }) => {
    await page.addInitScript(() => {
      let persisted = false;
      Object.defineProperty(navigator, 'storage', {
        configurable: true,
        value: {
          estimate: () => Promise.resolve({ usage: 5 * 1024 * 1024, quota: 2 * 1024 ** 3 }),
          persisted: () => Promise.resolve(persisted),
          persist: () => {
            persisted = true;
            return Promise.resolve(true);
          },
        },
      });
    });
    await page.goto(LOCAL);
    await page.getByRole('button', { name: 'Almacenamiento' }).click();
    await expect(page.locator('dd')).toHaveText(['5.0 MB', '2.0 GB', /^No/]);
    await page.getByRole('button', { name: 'Solicitar almacenamiento persistente' }).click();
    await expect(page.getByText('Almacenamiento persistente concedido.')).toBeVisible();
    await expect(page.locator('dd').nth(2)).toHaveText('Sí');
    await expect(
      page.getByRole('button', { name: 'Solicitar almacenamiento persistente' }),
    ).toBeDisabled();
  });
});
