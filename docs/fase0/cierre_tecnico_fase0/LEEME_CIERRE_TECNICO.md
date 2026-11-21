# LEEME — Cierre técnico, arquitectónico y documental de Fase 0 (CCI)

## Estado actual (vigente)
| Dato | Valor |
|---|---|
| Rama de publicación | `audit/cierre-tecnico-fase0` (repositorio `appalex47-lab/Copy-Creative-Intelligence`) |
| Primera publicación | commit `e6caebf61947d94ac8867ecd62f6ebe079fe64ef` (padre: V26) |
| Corrección final consolidada | commit(s) posteriores en la misma rama; el SHA vigente no puede ir dentro de este archivo: ver `INFORME_PUBLICACION_GITHUB.md` y `git log` de la rama |
| Base V26 (intacta) | `audit/fase0-v26-review` = `439777c9ea7db464fe49299adfeb2112abfd285c` |
| `main` (intacta) | `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` |
| Alcance | Solo `docs/fase0/cierre_tecnico_fase0/`. Complementa a V26; **no es V27**; no reinicia la auditoría. |
| PR / merge | Ninguno. Publicación exclusiva para revisión independiente. |
| Dictamen | **PREPARADO_CON_LIMITACIONES** (`DICTAMEN_PREPARACION_FASE0.md`) |

**No** hay validación física en CCI-DEV (ni en CCI-PROD): nada se ejecutó contra Supabase. **No** hay aceptación formal de Fase 0. **No** se autoriza Fase 1. Ninguna decisión arquitectónica está aprobada (21 registradas, todas pendientes del propietario).

## Estado de verificación (local, no físico)
PostgreSQL 16.15 temporal: V20 63/63 y 14/14; extensión 80/80; concurrencia local 2/2; hash 16/16; arnés R1–R9 28/28; 22 funciones 366 evaluaciones/0 fallos; T-409..T-422 26/26 en modelo; escáner de seguridad SQL 64/0; reconciliación integral y manifiesto: ver `INFORME_RECONCILIACION_INTEGRAL.md`, `INFORME_PRUEBAS_FINALES.md`, `INFORME_HASHES_MANIFIESTO.md`. Limitaciones: `MATRIZ_LIMITACIONES_RESIDUALES.csv` (28).

## Estado histórico (superado, conservado)
La versión inicial de este expediente se redactó en una rama local `local/cierre-tecnico-fase0` desde `439777c9…`, «sin commit, push ni merge». Después se publicó (e6caebf…) y luego se aplicó la corrección final (defecto del script R1–R9 con falsos PASS, revisión de los seis scripts, reclasificación de evidencias, trazabilidad). El script anterior se conserva en `scripts_validacion/historico_defectos/`.

## Orden de lectura
1. DICTAMEN_PREPARACION_FASE0.md → 2. INFORME_CIERRE_TECNICO_FASE0.md → 3. INFORME_DECISIONES_ARQUITECTONICAS.md (+ REGISTRO_DECISIONES_RECOMENDADAS.csv) → 4. MATRIZ_LIMITACIONES_RESIDUALES.csv → 5. MATRIZ_TRAZABILIDAD_MAESTRA.csv.
Detalle: MATRIZ_12_ESCENARIOS_PARCIALES.csv, EXPEDIENTE_T409_T422.md, REVISION_22_FUNCIONES.md, MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv, MATRIZ_MODELO_LOGICO_FISICO.md, PLAN_VALIDACION_CCI_DEV.md, PLAN_VALIDACION_TRIGGER_R1_R9.md, PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md, INFORME_SEGURIDAD_SCRIPTS.md.

## scripts_validacion/
- Locales (solo clústeres PostgreSQL temporales; usar `python3 -I -B`): `local_ext/ejecutar_ext.sh <socket> <puerto>`; `ct_concurrencia_local.sh`, `ct_dg19_pk_experimento.sh <socket> <puerto>`; `ct_hash_cadena_referencia.py --pg <socket> <puerto>`; `ct_revision_estatica_T47_T124.py <docs/fase0>`; `ct_k47_por_escenario.py <herramientas> [csv]`; `ct_t409_t422_individual.py <docs/fase0> [csv]`; `ct_reejecucion_22_funciones.py <docs/fase0> [txt] [csv]`; `ct_arnes_r1r9_autoprueba.sh <socket> <puerto>`; `ct_smoke_scripts_cci_dev_local.sh <socket> <puerto>`; `ct_escaner_seguridad_sql.py <dir_sql>`; `ct_reconciliacion_integral.py <dir_cierre>`; `ct_manifiesto.py gen|dir|api` (manifiesto y verificación A/B); `ct_controles_negativos_manifiesto.py`; `ct_busqueda_global.py`; `ct_bateria_final.sh` (batería completa); generadores `ct_gen_*.py`.
- `cci_dev_NO_EJECUTADOS/`: seis scripts v2 para CCI-DEV. **NO EJECUTADOS — REQUIEREN AUTORIZACIÓN Y CCI-DEV.** Guarda `cci.validacion_autorizada='SI-CCI-DEV'` + `cci.entorno='CCI-DEV'` (la guarda no puede distinguir DEV de PROD: LR-22).
- `resultados/`: salidas de las corridas locales (UTF8 autoritativo; SQL_ASCII, contraste).

## Integridad
`MANIFIESTO_SHA256_CIERRE.txt` lista el SHA-256 de todos los archivos del dossier **excepto** sí mismo y el directorio `evidencia_verificacion/` (salidas de la verificación del commit de contenido; diseño de punto fijo, ver `INFORME_HASHES_MANIFIESTO.md`). Verificación: `scripts_validacion/ct_manifiesto.py dir|api`.

## Pendiente del propietario / no verificado
Pendiente: aprobación de decisiones (G-1, G-5, G-10, DG-19, DG-20, DG-12, DG-16, DG-18, G-9, RP-01, P-01..P-05, P-10, PO-05, DG-09, DEP-RET-01, OD-13, HV-02), contrato de error de R1–R9, CCI-DEV y su autorización, Adenda v9 y OD-13. No verificado: cualquier comportamiento en Supabase.
