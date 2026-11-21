# INFORME DE CONCILIACIÓN DE CONTROLES V26

**Fecha:** 2026-11-20 (fecha local, America/Mexico_City; las salidas remotas llevan su sello en UTC) · **Rama:** `audit/fase0-v26-review` · **Base:** `audit/fase0-v25-review`, HEAD de publicación `c3adaf97588ce3b8fef075a44aff6336f4e8c266` (commit del expediente V25 `f235768135175ce3fcd9405a3a4d3a3a68311d3e`).

**V26 no constituye aceptación formal de Fase 0** (corresponde exclusivamente al propietario), no autoriza Fase 1 (NO INICIADA) y no toca Supabase, CCI-DEV ni CCI-PROD.

## 1. Tabla de conciliación (única)
<!-- CONCILIACION:INICIO -->
| Concepto | Valor |
|---|---|
| Total de controles únicos | 94 |
| Total de ejecuciones | 238 |
| Controles PASS | 85 |
| Controles FAIL | 0 |
| Controles BLOCKED | 0 |
| Controles NOT VERIFIED | 5 |
| Controles PARTIAL | 4 |
| Ejecuciones PASS | 236 |
| Ejecuciones FAIL | 1 |
| Ejecuciones BLOCKED | 0 |
| Ejecuciones NOT VERIFIED | 0 |
| Ejecuciones PARTIAL | 1 |
<!-- CONCILIACION:FIN -->

### Por categoría
| Categoría | Controles únicos | Ejecuciones | PASS | FAIL | BLOCKED | NOT VERIFIED | PARTIAL |
|---|---|---|---|---|---|---|---|
| Documental | 54 | 168 | 54 | 0 | 0 | 0 | 0 |
| Verificación remota | 22 | 51 | 22 | 0 | 0 | 0 | 0 |
| Prueba técnica histórica | 10 | 19 | 9 | 0 | 0 | 0 | 1 |
| Alcance técnico (limitación) | 8 | 0 | 0 | 0 | 0 | 5 | 3 |

## 2. Cómo se cuenta
- **Control único:** una fila de `MATRIZ_CONTROLES_V26.csv` con ID propio. 18 controles documentales de V24 (C01–C18) + 16 de V25 (P01–P14 y Q01–Q02) + 20 de V26 (S01–S20) = 54 controles documentales; verificaciones remotas: 8 de V24 (R01–R08) + 11 de V25 (RV01–RV11) + 3 previas de V26 (W01–W03) = 22; 10 pruebas técnicas históricas (HT01–HT10); 8 limitaciones declaradas (L01–L08).
- **Ejecución:** una corrida con salida cruda archivada (`EJECUCIONES_CONTROLES_V26.csv`, línea exacta). Repetir un control es una ejecución nueva del mismo control, nunca otro control.
- **Estado de un control:** el de su última ejecución. Los controles L no tienen ejecución propia y conservan el estado declarado (PARTIAL o NOT VERIFIED).
- **Fechas:** fecha local (America/Mexico_City). Las salidas de verificación remota llevan además su sello UTC.

## 3. Reconciliación con las cifras anteriores
| Cifra histórica | Qué era | Dónde está en V26 |
|---|---|---|
| V24 «16» y «18» | Mismo conjunto C01–C18 en dos pasadas (A: C01–C16; C: C01–C18) | C01–C18: 1 control cada uno; ejecuciones: 70 (A 16 + C 18 + re-ejecución V25 18 + re-ejecución V26 18) |
| V24 «8 verificaciones» | R01–R08 | R01–R08: ejecuciones nuevas V25 y V26 (16); las originales no se cuentan |
| V25 «26 PASS» | 18 C + 8 R de la matriz V25, sin los controles propios de V25 | Reemplazado por la tabla de §1 (D03, D04) |
| V25 «16 controles» | P01–P14 (pasada A) y P01–P14 + Q01–Q02 (pasada C) | P01–Q02: 16 controles, 60 ejecuciones (A, A2, C y re-ejecución V26) |
| V25 «11 verificaciones» | RV01–RV11 (10 con salida archivada; RV07 sin ella) | RV01–RV11: 32 ejecuciones (original V25 10 + V26 corrida 1 11 + corrida 2 11); RV07 solo en V26 (2 ejecuciones: FAIL por defecto del script y PASS) |
| V21/V22 pruebas técnicas | 59/59, 28/28, 300/300, 366 casos, 63/63, 14/14, 46/46, 26/26, integridad, 8 de 9 | HT01–HT10: 19 ejecuciones históricas, sin re-ejecución en V26 |

La diferencia entre los 640 blobs del reporte de publicación V24 y los 641 de la re-ejecución R03 no es contradicción: son dos refs distintas (commit del expediente V24 y HEAD de publicación, que añade un archivo).

## 4. Declaraciones sin evidencia (no cuentan como ejecuciones)
| Versión | Declaración | Dónde consta | Tratamiento |
|---|---|---|---|
| V24 | Ejecución intermedia del validador V24 con 15/16 PASS (defecto de mayúsculas del propio validador, ya corregido) | solo en la transcripción de la sesión V24 | no resoluble: la salida no existe; no se cuenta como ejecución |
| V24 | Ejecución intermedia del validador V24 con 16/16 PASS antes de existir INFORME_CORRECCIONES_V24.md | solo en la transcripción de la sesión V24 | no resoluble: la salida no existe; no se cuenta como ejecución |
| V24 | Verificaciones remotas R01–R08 originales (declaradas en REPORTE_PUBLICACION_V24_GITHUB.md) | reporte de publicación V24 (sin salida cruda) | re-ejecutadas en V25 y V26 como ejecuciones nuevas; las originales no se cuentan |
| V25 | RV07 declarada ejecutada tras el segundo commit de V25 | respuesta de entrega de V25 (sin salida cruda; solo restos de descargas sin comando ni resultado) | ejecutada de nuevo en V26 con salida cruda; la de V25 no se cuenta |

## 5. Estados no PASS (visibles)
- **FAIL:** ningún control. Hay **una ejecución FAIL** (RV07, corrida 1 de V26, por un defecto del propio script de comprobación), archivada en `evidencia_reconstruccion_V26/reejecucion_V26_RV01_RV11_corrida1_RV07e_FAIL_por_defecto_del_script.txt`.
- **BLOCKED:** ninguno.
- **PARTIAL:** 4 controles (HT10, L01, L02, L03).
- **NOT VERIFIED:** 5 controles (L04–L08).

## 6. Controles posteriores al manifiesto (S19 y S20)
Se ejecutan sobre el paquete definitivo; su salida cruda va en `REPORTE_PUBLICACION_V26_GITHUB.md` (fuera del expediente, porque un archivo no puede contener el hash de sí mismo ni de un manifiesto que lo incluya). Su estado se consigna tras ejecutarlos (punto fijo documentado en el informe de auditoría).
