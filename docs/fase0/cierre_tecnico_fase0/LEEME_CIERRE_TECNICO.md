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

**No** hay validación física en CCI-DEV (ni en CCI-PROD): nada se ejecutó contra Supabase. **No** hay aceptación formal de Fase 0. **No** se autoriza Fase 1. Ninguna decisión arquitectónica está aprobada (ver cifras generadas más abajo: todas pendientes del propietario).

## Estado de verificación (local, no físico)
<!-- CIFRAS:INICIO -->
_Generado por `ct_gen_cifras.py` desde `resultados/cifras_definitivas.json`; todo resultado es LOCAL/PROTOTIPO/ESTÁTICO: PASS_PHYSICAL = 0._

- PostgreSQL 16 temporal: V20 63 pruebas PASS y 14 mutaciones detectadas; extensión 80 PASS; DG-19 63 PASS; hash encadenado 16 PASS; concurrencia local CC-01/CC-02 (ver batería); arnés R1–R9 28 PASS (prueba el arnés, no R1–R9).
- Modelo en memoria: K47 25 mapeadas detectadas; T-409..T-422 26 variantes detectadas; 22 funciones: 366 evaluaciones, 354 fixtures distintos; 23 bloques `except Exception` (19 SEGURO, 4 RIESGO_TECNICO).
- Escáneres estáticos: SQL 137 comprobaciones (0 FAIL), texto 736 en la batería y 771 en el árbol final (0 FAIL), autoprueba 37 (0 FAIL).
- Smoke de los 6 scripts: 12 aserciones de contenido (12 PASS). Guarda DEV/PROD (H-03): 139 pruebas (139 PASS, 0 FAIL) sobre los 6 scripts.
- Batería: 22 pasos, 22 con estado OK (rc=0 **y** contenido esperado). Manifiesto: 138 entradas.
- Limitaciones: 27 (vigentes 18, parcialmente resueltas 4, resueltas 5). Decisiones: 21 (aprobadas: 0). Escenarios parciales: 12 (PASS_PROTOTYPE 5, PASS_STATIC 1, PARTIAL 6). Trazabilidad: 54 filas.
- Reconciliación integral y verificación A/B: `INFORME_RECONCILIACION_INTEGRAL.md`, `evidencia_verificacion/`.
<!-- CIFRAS:FIN -->

## Estado histórico (superado, conservado)
La versión inicial de este expediente se redactó en una rama local `local/cierre-tecnico-fase0` desde `439777c9…`, «sin commit, push ni merge». Después se publicó (e6caebf…) y luego se aplicó la corrección final (defecto del script R1–R9 con falsos PASS, revisión de los seis scripts, reclasificación de evidencias, trazabilidad). El script anterior se conserva en `scripts_validacion/historico_defectos/`.

## Orden de lectura
1. DICTAMEN_PREPARACION_FASE0.md → 2. INFORME_CIERRE_TECNICO_FASE0.md → 3. INFORME_DECISIONES_ARQUITECTONICAS.md (+ REGISTRO_DECISIONES_RECOMENDADAS.csv) → 4. MATRIZ_LIMITACIONES_RESIDUALES.csv → 5. MATRIZ_TRAZABILIDAD_MAESTRA.csv.
Control del cierre: INFORME_CIFRAS_DEFINITIVAS.md (cifras generadas desde los resultados), INFORME_RECONCILIACION_INTEGRAL.md, INFORME_PRUEBAS_FINALES.md, INFORME_AUDITORIA_FECHAS_HORAS.md, RESOLUCION_OBSERVACIONES_FINALES.md, INFORME_HASHES_MANIFIESTO.md, INFORME_PUBLICACION_GITHUB.md, `evidencia_verificacion/`.
Detalle: MATRIZ_12_ESCENARIOS_PARCIALES.csv, EXPEDIENTE_T409_T422.md, REVISION_22_FUNCIONES.md, MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv, MATRIZ_MODELO_LOGICO_FISICO.md, PLAN_VALIDACION_CCI_DEV.md, PLAN_VALIDACION_TRIGGER_R1_R9.md, PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md, INFORME_SEGURIDAD_SCRIPTS.md.

## scripts_validacion/
- Locales (solo clústeres PostgreSQL temporales; usar `python3 -I -B`): `local_ext/ejecutar_ext.sh <socket> <puerto>`; `ct_concurrencia_local.sh`, `ct_dg19_pk_experimento.sh <socket> <puerto>`; `ct_hash_cadena_referencia.py --pg <socket> <puerto>`; `ct_revision_estatica_T47_T124.py <docs/fase0>`; `ct_k47_por_escenario.py <herramientas> [csv]`; `ct_t409_t422_individual.py <docs/fase0> [csv]`; `ct_reejecucion_22_funciones.py <docs/fase0> [txt] [csv]`; `ct_arnes_r1r9_autoprueba.sh <socket> <puerto>`; `ct_smoke_scripts_cci_dev_local.sh <socket> <puerto>`; `ct_escaner_seguridad_sql.py <dir_sql>`; `ct_reconciliacion_integral.py <dir_cierre>`; `ct_manifiesto.py gen|dir|api` (manifiesto y verificación A/B); `ct_aserciones_smoke.py`; `ct_gen_cifras.py`; `ct_verificar_consistencia_informe.py`; `ct_gen_auditoria_fechas.py`; `ct_gen_resolucion_observaciones.py`; `ct_cierre_final.sh` (secuencia completa); `ct_controles_negativos_manifiesto.py`; `ct_busqueda_global.py`; `ct_bateria_final.sh` (batería completa); generadores `ct_gen_*.py`.
- `cci_dev_NO_EJECUTADOS/`: seis scripts v2 para CCI-DEV. **NO EJECUTADOS — REQUIEREN AUTORIZACIÓN Y CCI-DEV.** Guarda compartida `00_guarda_destino.sql` (identidad efectiva + allowlist/denylist literales, vacías hasta que el propietario entregue los identificadores; falla cerrada: LR-22 parcialmente resuelta) además de `cci.validacion_autorizada` + `cci.entorno`.
- `resultados/`: salidas de las corridas locales (UTF8 autoritativo; SQL_ASCII, contraste).

## Integridad
`MANIFIESTO_SHA256_CIERRE.txt` lista el SHA-256 de todos los archivos del dossier **excepto** sí mismo y el directorio `evidencia_verificacion/` (salidas de la verificación del commit de contenido; diseño de punto fijo, ver `INFORME_HASHES_MANIFIESTO.md`). Verificación: `scripts_validacion/ct_manifiesto.py dir|api`.

## Pendiente del propietario / no verificado
Pendiente: aprobación de decisiones (G-1, G-5, G-10, DG-19, DG-20, DG-12, DG-16, DG-18, G-9, RP-01, P-01..P-05, P-10, PO-05, DG-09, DEP-RET-01, OD-13, HV-02), contrato de error de R1–R9, CCI-DEV y su autorización, Adenda v9 y OD-13. No verificado: cualquier comportamiento en Supabase.
