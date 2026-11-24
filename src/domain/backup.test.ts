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
  briefs: [
    {
      id: 'brf_abcdefgh1',
      createdAt: '2026-11-22T09:00:00.000Z',
      updatedAt: '2026-11-22T09:30:00.000Z',
      fields: { campaign: 'Buen Fin', channel: 'Email' },
    },
  ],
  copies: [
    {
      id: 'cpy_abcdefgh1',
      briefId: 'brf_abcdefgh1',
      label: 'Principal',
      tags: ['promo'],
      createdAt: '2026-11-22T09:10:00.000Z',
      updatedAt: '2026-11-22T09:40:00.000Z',
      versions: [
        { n: 1, createdAt: '2026-11-22T09:10:00.000Z', content: { headline: 'Hola' } },
        {
          n: 2,
          createdAt: '2026-11-22T09:40:00.000Z',
          content: { headline: 'Hola', cta: 'Compra' },
        },
      ],
    },
  ],
  rules: {
    legends: [{ text: 'Consulta a tu médico', channels: ['Email'], required: true, active: true }],
    brandTerms: [{ text: 'cura', kind: 'prohibido', severity: 'mayor' }],
  },
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

describe('respaldo v2 con briefs (S2.2)', () => {
  it('los briefs viajan en el archivo y se interpretan igual', () => {
    const r = parseBackupText(file());
    expect(r.ok && r.value.data.briefs).toEqual(data.briefs);
    expect(r.ok && r.value.version).toBe(5);
    expect(r.ok && r.value.data.copies).toEqual(data.copies);
  });
  it('un respaldo v1 (sin briefs) sigue siendo válido y su suma se calcula con la forma v1', () => {
    const v1 = file((o) => {
      o['version'] = 1;
      delete (o['data'] as Record<string, unknown>)['briefs'];
      delete (o['data'] as Record<string, unknown>)['copies'];
      delete (o['data'] as Record<string, unknown>)['rules'];
    });
    const r = parseBackupText(v1);
    expect(r.ok && r.value.data.briefs).toEqual([]);
    expect(r.ok && r.value.version).toBe(1);
    expect(canonicalData(data, 1)).not.toContain('briefs');
    expect(canonicalData(data, 2)).toContain('briefs');
  });
  it('v2 exige la sección briefs; v1 no la admite', () => {
    expect(reason(file((o) => delete (o['data'] as Record<string, unknown>)['briefs']))).toContain(
      'datos',
    );
    expect(reason(file((o) => (o['version'] = 1)))).toContain('datos');
  });
  it('rechaza briefs inválidos, repetidos o en exceso', () => {
    const withBriefs = (b: unknown) =>
      file((o) => ((o['data'] as Record<string, unknown>)['briefs'] = b));
    expect(reason(withBriefs('x'))).toContain('briefs');
    expect(reason(withBriefs([{ id: 'x' }]))).toContain('briefs');
    expect(reason(withBriefs([data.briefs[0], data.briefs[0]]))).toContain('briefs');
    expect(reason(withBriefs([{ ...data.briefs[0], fields: { channel: 'Llamadas' } }]))).toContain(
      'briefs',
    );
  });
  it('el orden de claves de los campos no cambia la suma canónica', () => {
    const [b] = data.briefs;
    if (!b) throw new Error('falta brief de prueba');
    const swapped = {
      ...data,
      briefs: [{ ...b, fields: { channel: 'Email', campaign: 'Buen Fin' } as typeof b.fields }],
    };
    expect(canonicalData(swapped)).toBe(canonicalData(data));
  });
});

describe('respaldo v4 con reglas (S2.5b)', () => {
  it('las reglas viajan en el archivo y se interpretan igual', () => {
    const r = parseBackupText(file());
    expect(r.ok && r.value.data.rules).toEqual(data.rules);
    expect(canonicalData(data, 3)).not.toContain('rules');
    expect(canonicalData(data, 4)).toContain('rules');
  });
  it('rules: null (nunca configuradas) es válido; v3 no trae reglas y da null', () => {
    const none = file((o) => ((o['data'] as Record<string, unknown>)['rules'] = null));
    expect(
      parseBackupText(none).ok &&
        (parseBackupText(none) as { value: { data: BackupData } }).value.data.rules,
    ).toBe(null);
    const v3 = file((o) => {
      o['version'] = 3;
      delete (o['data'] as Record<string, unknown>)['rules'];
    });
    const r = parseBackupText(v3);
    expect(r.ok && r.value.version).toBe(3);
    expect(r.ok && r.value.data.rules).toBe(null);
  });
  it('v4 exige la sección rules y rechaza reglas inválidas', () => {
    expect(reason(file((o) => delete (o['data'] as Record<string, unknown>)['rules']))).toContain(
      'datos',
    );
    const bad = file((o) => ((o['data'] as Record<string, unknown>)['rules'] = { legends: 'x' }));
    expect(reason(bad)).toContain('reglas');
  });
});

describe('respaldo v5 con variantes (S2.7)', () => {
  const variant = {
    id: 'var_abcdefgh1',
    label: 'B',
    content: { headline: 'Otro' },
    createdAt: '2026-11-22T09:10:00.000Z',
    updatedAt: '2026-11-22T09:10:00.000Z',
  };
  const withVariant: BackupData = {
    ...data,
    copies: data.copies.map((c) => ({ ...c, variants: [variant] })),
  };
  it('las variantes viajan en el copy y entran en la suma canónica solo desde v5', () => {
    expect(canonicalData(withVariant, 5)).toContain('"variants"');
    expect(canonicalData(withVariant, 4)).not.toContain('variants');
    const text = serializeBackup(withVariant, '2026-11-22T12:00:00.000Z', HASH);
    const r = parseBackupText(text);
    expect(r.ok && r.value.data.copies[0]?.variants).toEqual([variant]);
  });
  it('un archivo de versión anterior a la 5 no puede traer variantes', () => {
    const o = JSON.parse(serializeBackup(withVariant, '2026-11-22T12:00:00.000Z', HASH)) as Record<
      string,
      unknown
    >;
    o['version'] = 4;
    const r = parseBackupText(JSON.stringify(o));
    expect(r.ok).toBe(false);
  });
});

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
    expect(reason(file((o) => (o['version'] = 6)))).toContain('más reciente');
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
