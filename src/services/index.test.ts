import { describe, expect, it } from 'vitest';
import type { AppEnv } from '@/app/env';
import { createServices } from './index';

describe('createServices', () => {
  it('crea los servicios DEMO para el modo demo', () => {
    expect(Object.keys(createServices({ appEnv: 'test', dataMode: 'demo' })).sort()).toEqual([
      'activity',
      'adaptations',
      'appState',
      'audits',
      'backup',
      'briefs',
      'coordination',
      'copies',
      'entities',
      'preferences',
      'profile',
      'resources',
      'rules',
      'storage',
    ]);
  });
  it('falla de forma explícita ante un modo no soportado (no devuelve undefined)', () => {
    const bad = { appEnv: 'test', dataMode: 'supabase' } as unknown as AppEnv;
    expect(() => createServices(bad)).toThrow('Modo de datos no soportado');
  });
});
