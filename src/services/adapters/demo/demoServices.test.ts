import { describe, expect, it } from 'vitest';
import { createDemoServices } from './demoServices';

describe('adaptador DEMO', () => {
  it('declara el estado DEMO con el entorno recibido', async () => {
    const r = await createDemoServices('test').appState.getState();
    expect(r).toEqual({ ok: true, value: { dataMode: 'demo', environment: 'test', isDemo: true } });
  });
  it('no inventa actividad: la lista reciente está vacía (éxito, no error)', async () => {
    expect(await createDemoServices('test').activity.listRecent()).toEqual({ ok: true, value: [] });
  });
  it('no expone identidad, organizaciones, membresías ni proyectos (P1)', () => {
    expect(Object.keys(createDemoServices('test')).sort()).toEqual([
      'activity',
      'appState',
      'backup',
      'briefs',
      'coordination',
      'copies',
      'preferences',
      'profile',
      'storage',
    ]);
  });
});
