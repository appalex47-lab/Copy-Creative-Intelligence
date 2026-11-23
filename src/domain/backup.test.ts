import { describe, expect, it } from 'vitest';
import { DEFAULT_SETTINGS } from './settings';
import {
  backupFileName,
  BACKUP_MAX_BYTES,
  canonicalData,
  parseBackupText,
  serializeBackup,
  type BackupData,
} from './backup';

const data: BackupData = {
  profile: { displayName: 'Ana' },
  settings: { ...DEFAULT_SETTINGS, theme: 'dark', lastBackupAt: '2026-11-22T10:00:00.000Z' },
  activity: [
    { id: 'evt_00000002', at: '2026-11-22T11:00:00.000Z', kind: 'profile_changed' },
    { id: 'evt_00000001', at: '2026-11-22T10:00:00.000Z', kind: 'app_opened' },
  ],
};
const HASH = 'a'.repeat(64);
const file = (mutate?: (o: Record<string, unknown>) => void) => {
  const o = JSON.parse(serializeBackup(data, '2026-11-22T12:00:00.000Z', HASH)) as Record<
    string,
    unknown
  >;
  mutate?.(o);
  return JSON.stringify(o);
};
const reason = (t: string) => {
  const r = parseBackupText(t);
  return r.ok ? null : r.reason;
};

describe('respaldo (dominio)', () => {
  it('un archivo válido se interpreta tal cual', () => {
    const r = parseBackupText(file());
    expect(r.ok && r.value.data).toEqual(data);
    expect(r.ok && r.value.exportedAt).toBe('2026-11-22T12:00:00.000Z');
    expect(r.ok && r.value.declaredHash).toBe(HASH);
  });
  it('la forma canónica no depende del orden de claves del archivo', () => {
    expect(canonicalData(data)).toBe(canonicalData(JSON.parse(JSON.stringify(data)) as BackupData));
  });
  it('rechaza texto que no es JSON, otros formatos y versiones nuevas o inválidas', () => {
    expect(reason('no json')).toContain('no es JSON');
    expect(reason('{"format":"otro"}')).toContain('no es un respaldo');
    expect(reason(file((o) => (o['version'] = 2)))).toContain('más reciente');
    expect(reason(file((o) => (o['version'] = 0)))).toContain('versión');
    expect(reason(file((o) => (o['version'] = '1')))).toContain('versión');
  });
  it('rechaza claves desconocidas en cualquier nivel', () => {
    expect(reason(file((o) => (o['x'] = 1)))).toContain('campos no permitidos');
    expect(reason(file((o) => ((o['data'] as Record<string, unknown>)['x'] = 1)))).toContain(
      'datos del respaldo',
    );
    expect(
      reason(
        file((o) => ((o['data'] as { profile: Record<string, unknown> }).profile['rol'] = 'admin')),
      ),
    ).toContain('perfil');
  });
  it('rechaza fecha, integridad, perfil, configuración y actividad inválidos', () => {
    expect(reason(file((o) => (o['exportedAt'] = 'ayer')))).toContain('fecha');
    expect(reason(file((o) => (o['integrity'] = { algorithm: 'MD5', value: HASH })))).toContain(
      'integridad',
    );
    expect(
      reason(file((o) => (o['integrity'] = { algorithm: 'SHA-256', value: 'xyz' }))),
    ).toContain('integridad');
    expect(
      reason(
        file(
          (o) =>
            ((o['data'] as { profile: Record<string, unknown> }).profile['displayName'] =
              'x'.repeat(61)),
        ),
      ),
    ).toContain('nombre');
    expect(
      reason(
        file(
          (o) => ((o['data'] as { settings: Record<string, unknown> }).settings['theme'] = 'neón'),
        ),
      ),
    ).toContain('configuración');
    expect(
      reason(
        file((o) => delete (o['data'] as { settings: Record<string, unknown> }).settings['theme']),
      ),
    ).toContain('configuración');
    expect(
      reason(file((o) => ((o['data'] as Record<string, unknown>)['activity'] = 'no'))),
    ).toContain('actividad');
    expect(
      reason(
        file(
          (o) =>
            ((o['data'] as { activity: unknown[] }).activity[0] = { id: 'x', at: 'y', kind: 'z' }),
        ),
      ),
    ).toContain('eventos no válidos');
    expect(
      reason(
        file(
          (o) =>
            ((o['data'] as { activity: unknown[] }).activity[1] = (
              o['data'] as { activity: unknown[] }
            ).activity[0]),
        ),
      ),
    ).toContain('eventos no válidos');
  });
  it('rechaza archivos demasiado grandes y demasiados eventos, sin reproducir contenido', () => {
    expect(reason(' '.repeat(BACKUP_MAX_BYTES + 1))).toContain('tamaño máximo');
    const many = Array.from({ length: 10_001 }, (_, i) => ({
      id: `evt_${String(i).padStart(8, '0')}`,
      at: '2026-11-22T10:00:00.000Z',
      kind: 'app_opened',
    }));
    expect(
      reason(file((o) => ((o['data'] as Record<string, unknown>)['activity'] = many))),
    ).toContain('demasiados');
    expect(reason(file((o) => (o['format'] = 'SECRETO_DEL_ARCHIVO')))).not.toContain('SECRETO');
  });
  it('nombre de archivo estable y seguro', () => {
    expect(backupFileName('2026-11-22T12:34:56.789Z')).toBe('cci-respaldo-20261122-123456.json');
  });
});
