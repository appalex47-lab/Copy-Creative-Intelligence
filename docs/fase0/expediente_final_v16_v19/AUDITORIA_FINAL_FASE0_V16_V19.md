# AUDITORÍA FINAL — FASE 0 (V16–V19, cierre V20)

> **Superseded (V20, 2026-11-20):** sustituido por `INFORME_FINAL_V20.md` (cierre con el prompt de reconciliación integral). Se conserva como histórico de la pasada anterior.

**Versión:** V20 · **Fecha:** 2026-11-19 · **Fuente:** rama `audit/fase0-v19-review` (c6ef74b) más árbol local V20; matrices de este directorio · **Estado de verificación:** auditoría documental y en modelo en memoria; **sin** validación en PostgreSQL/Supabase; **sin** aceptación del propietario.

## 1. Alcance y base
Rama `audit/fase0-v19-review`, HEAD c6ef74b (padre 6a1af24 = V16); `main` en V16. Motor, verificador, históricos y v3.3 sin modificar (hashes en el manifiesto).

## 2. Reglas (231)
Clasificación V20 computada de la evidencia: **A 1, B 8, C 69, D 153, E 0** (= 231; las 5 reglas E de V19 pasaron a B tras ejecutarse en PostgreSQL temporal, ver `PE_POSTGRESQL_V20/`). Definiciones: A implementada y probada; B parcial; C diseño sin implementación demostrable; D condicionada por decisión abierta (G-1/G-5/G-10); E evidencia insuficiente. Las 5 E (IG1-05, IG1-06, IG1-10, IG1-21, IG5-36) **siguen E**: ningún escenario demuestra IG1-05, IG1-06 ni IG1-10; IG1-21 solo indirecta; IG5-36 cubre 4 de 9 columnas. Pruebas PE-01..PE-05 diseñadas, no ejecutadas. Detalle: `MATRIZ_FINAL_231_REGLAS_V16_V19.csv`.

## 3. Escenarios (780)
Todos con reglas citadas existentes y cobertura bidireccional (1.592 pares, 0 inconsistentes). Veredictos: 258 demostrados por ejecución en modelo (criterios E1/E2/E3), 510 demuestran por lectura (6 con observación), **12 PARCIAL**. T-409..T-422 sin vínculo de ejecución individual. Detalle: `MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv`; trazabilidad: `MATRIZ_TRAZABILIDAD_REGLAS_ESCENARIOS_V16_V19.csv`.

## 4. Discrepancias
| ID | Hallazgo | Resolución |
|---|---|---|
| HV-01 | Ningún documento activo mencionaba V16 | Corregido (V16–V17) |
| S1/S1b | «14 tablas» listaba 13 (l.3620 y l.38) | Corregido (V18–V19) |
| Fila 1270 | «Fuentes físicas» omitía `attribution_discard_resolutions` | Corregido en V20 |
| `channel_formats` | Sin definición formal | Definida solo con lo derivable; PK, índices y valores quedan **no determinados** |
| 2.217 advertencias `git diff --check` | 2.177 CRLF + 40 espacios finales | Corregidas; RC=0 (REPORTE_FORMATO_Y_INTEGRIDAD.md) |
| Estados de publicación obsoletos | «local/no publicado» en evidencia V16–V19 | Notas V20 fechadas; historia conservada |
| HV-02 | PO-05 cita «addendum v3» | **NO VERIFICABLE** sin confirmación del propietario; no se alteró PO-05 |

## 5. Pruebas
22 funciones / 366 casos reejecutados: salida idéntica a la histórica (SHA-256 2b858619…2f4). Verificador: 59/59, 28/28, 300/300, ver `REPORTE_REGRESION_FINAL.md`. Todo en memoria.

## 6. Decisiones abiertas
Ver `INVENTARIO_DECISIONES_ABIERTAS_FASE0.md`. G-1, G-5 y G-10 no se cierran; las 153 reglas D dependen de su aceptación.

## 7. PostgreSQL/Supabase
Solo plan (`PLAN_VALIDACION_POSTGRESQL_SUPABASE_CCI.md`); nada ejecutado.

## 8. Conclusión
El expediente documental es internamente consistente según los controles ejecutados. Persisten limitaciones externas (infraestructura real) y decisiones del propietario; no hay aceptación del propietario de ninguna versión.
