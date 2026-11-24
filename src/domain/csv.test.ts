import { describe, expect, it } from 'vitest';
import { copyAuditsCsv, pieceAuditsCsv } from './auditExport';
import { csvCell, toCsv } from './csv';

describe('csv', () => {
  it('escapa comillas, comas y saltos', () => {
    expect(csvCell('a,"b"\nc')).toBe('"a,""b""\nc"');
    expect(csvCell(5)).toBe('5');
  });
  it('neutraliza fórmulas pero no números negativos', () => {
    expect(csvCell('=SUM(A1)')).toBe("'=SUM(A1)");
    expect(csvCell('@x')).toBe("'@x");
    expect(csvCell(-3)).toBe('-3');
  });
  it('incluye BOM y encabezado', () => {
    const t = toCsv(['A', 'B'], [[1, 'x']]);
    expect(t.startsWith('﻿A,B\r\n1,x')).toBe(true);
  });
  it('exporta auditorías vacías solo con encabezado', () => {
    expect(copyAuditsCsv([]).split('\r\n')[0]).toContain('Copy');
    expect(pieceAuditsCsv([]).split('\r\n')[0]).toContain('Origen');
  });
  it('una fila por hallazgo', () => {
    const csv = copyAuditsCsv([
      {
        id: 'aud_abcdefgh1234',
        copyId: 'cpy_x',
        sourceVersion: 1,
        targetLabel: '=Principal',
        channel: 'Email',
        score: 70,
        verdict: 'revisar',
        blocked: false,
        findings: [
          { ruleId: 'a', category: 'marca', severity: 'mayor', message: 'uno' },
          { ruleId: 'b', category: 'precios', severity: 'menor', message: 'dos' },
        ],
        rules: { isTemplate: true, legends: 0, brandTerms: 0 },
        createdAt: '2026-11-23T10:00:00.000Z',
      } as never,
    ]);
    expect(csv.trim().split('\r\n')).toHaveLength(3);
    expect(csv).toContain("'=Principal");
  });
});
