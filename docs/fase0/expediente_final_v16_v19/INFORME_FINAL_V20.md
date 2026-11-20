# INFORME FINAL V20 — CIERRE INTEGRAL Y RECONCILIACIÓN DEL EXPEDIENTE G-1, G-5 Y G-10

**Versión:** V20 · **Fecha:** 2026-11-20 · **Fuente:** evidencia de este directorio · **Estado de verificación:** ver cada sección; V20 **no** equivale a aceptación del propietario, a validación de infraestructura real ni a autorización de Fase 1.

**A. Estado inicial.** Repositorio `appalex47-lab/Copy-Creative-Intelligence`, rama `audit/fase0-v19-review`, HEAD y commit base `c6ef74be4db185ac3e4fd36810f24619e6f51fcf` (padre `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` = V16). `main` = 6a1af24 (`git ls-remote`).

**B. Estado final.** `main` sin cambios (se reverifica tras el push). Rama de auditoría: un único commit nuevo sobre c6ef74b (mensaje autorizado); SHA remoto verificado en la respuesta final (un commit no puede contener su propio SHA).

**C. Archivos.** Respecto de c6ef74b: 42 creados, 17 modificados, 0 eliminados; todos bajo `docs/fase0/`. Modificados: los 5 documentos activos; 7 documentos de `evidencia_v16/` (notas fechadas y cifras 363→366); 4 CSV normalizados + `.gitattributes`. Creados: `expediente_final_v16_v19/` (informes, matrices de 231 reglas, 780 escenarios, trazabilidad, 366 casos, C01–C32, HV-02, datos, PostgreSQL, decisiones, fuentes físicas, regresión, formato, manifiesto, salidas, `PE_POSTGRESQL_V20/`) y 3 scripts de auditoría en `evidencia_v16/`. Conservados sin cambio: motor, verificador, `historico/`, salidas históricas, v3.3. Lista completa con SHA-256: `MANIFIESTO_EVIDENCIAS_SHA256.txt`.

**D. Reconciliación 363/366.** Total real **366** resultados individuales (366 PASS). Causa raíz: `instrumentar_22_funciones_v18.py` imprimía los 3 positivos de K45 pero no los sumaba (TOTAL 363); el inventario V18 sumaba 366 en sus renglones y declaraba 363 «incluyendo los positivos». Casos únicos (`función:id`): 366; duplicados reales: 0; IDs 01–09 compartidos entre guarda y atomicidad: casos distintos; 27 descripciones repetidas en 54 casos de funciones distintas: ejecuciones distintas. Invocaciones: una por función en la instrumentación (el verificador las invoca desde varios puntos sin casos adicionales). Por función: `MATRIZ_PRUEBAS_22_FUNCIONES_366_CASOS.md`. Evidencia: `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, `salida_22_funciones_V20_corrida1/2.txt`. Cifra corregida en todos los documentos que la reproducían.

**E. Formato.** 4 CSV originales: UTF-8 sin BOM, LF; igualdad lógica verificada; 2.177 CRLF y 40 espacios finales corregidos; convención documentada en `REPORTE_FORMATO_Y_INTEGRIDAD.md`. `git diff --cached --check c6ef74b` (índice temporal, todo `docs/`): **RC=0, 0 advertencias**; 0 BOM y 0 CR en los archivos modificados/nuevos.

**F. `channel_formats`.** Definición formal (7 columnas, tipos, nulabilidad, clave única compuesta, FK a `channel_rules` y `memberships`, CHECK de normalización, sin DELETE, inmutabilidad de canal/formato, baja lógica con `RETIRO_CON_PIEZAS_ACTIVAS`, RLS y permisos) derivada solo de fuentes citadas. **No determinado (no inventado):** clave primaria propia, índices adicionales, valores reales (DG-19, pendiente del propietario/organización). Probada en PostgreSQL temporal: PG-CF-01..15.

**G. `attribution_discard_resolutions`.** Añadida a la fila 1270; 22 columnas, 8 FK compuestas, 4 uniques, CHECK de independencia del resolutor (≠ afectado, solicitante y actor del cambio), evidencia no vacía, igualdad de atribución, versión exacta, sello SHA-256, inmutabilidad (UPDATE/DELETE/TRUNCATE) y reconsideración como fila nueva solo sobre una rechazada de la misma atribución. PostgreSQL temporal: PG-AD-01..20 PASS. Limitación: el trigger de elegibilidad completa R1–R9 no se implementó en el fixture (solo en el modelo en memoria).

**H. 231 reglas (esquema V20).** A 1, B 8, C 69, D 153, E 0. Las 5 reglas E de V19 (IG1-05, IG1-06, IG1-10, IG1-21, IG5-36) pasaron a B por su ejecución en PostgreSQL (fixture). 153 reglas D siguen condicionadas por G-1/G-5/G-10 sin aceptar; no se convirtieron en decisiones. `MATRIZ_FINAL_231_REGLAS_V16_V19.csv`.

**I. 780 escenarios.** 258 demostrados por ejecución en el modelo (criterios E1/E2/E3), 510 por lectura (6 con observación), **12 PARCIAL** (no demuestran toda la obligación); 6 escenarios (T-03, T-04, T-06, T-10, T-47, T-136) anotan además la ejecución en PostgreSQL de su obligación. T-409..T-422 sin vínculo de ejecución individual. Cobertura real y trazabilidad nominal separadas por columna.

**J. PE-01..PE-05.** Ejecutadas en PostgreSQL 16.15 temporal con un fixture derivado del diseño: PE-01 5, PE-02 5, PE-03 4, PE-04 5, PE-05 9 pruebas, todas PASS (más 35 de canales y resoluciones = 63); 14/14 mutaciones del fixture detectadas. **No** contra el esquema real ni CCI-DEV (no existe ni está autorizado). Una primera corrida tuvo 2 FAIL por errores del arnés (corregidos y documentados en `PE_POSTGRESQL_V20/README.md`, evidencia conservada).

**K. 22 funciones y suites.** 22 funciones / 366 casos / 0 fallos. Verificador completo: 59/59, 28/28, 300/300. Independencia motor/auditor: 6/6. Prueba estructural de FK: 4/4 (y 0/4 contra la especificación de c6ef74b: detecta las 7 columnas sin FK que ahora tienen FK). Suites históricas descubiertas en la salida real (K01–K59, A01–A65, FK01–41, CHAIN, ATTR, K56-M, M01–M27 y las de las 22 funciones) todas aprueban.

**L. K32, K45, K55.** Los tres aprueban. La revisión halló y corrigió 7 columnas `*_id` sin FK (`impact_evaluations` ×2, `publication_attempts` ×3, `brief_field_attributions.brief_id`, `promotion_field_attributions.promotion_line_id`): FK compuestas añadidas, +2 relaciones al contrato 4.4.9 y +2 aristas del diagrama (K14: 65→67; K26: 34→36; K44: 117→126). Detalle: `REVISION_FUENTES_FISICAS_K32_K45_K55_V20.md`.

**M. Dos corridas reproducibles.** Verificador completo en copias limpias, en paralelo: A = B (hash idéntico, 0 líneas de diferencia); 22 funciones ×2 idénticas; PostgreSQL ×2 idéntico. Detalle y hashes: `REPORTE_REGRESION_FINAL.md`. Frente a V19 solo difieren 3 líneas esperadas (K14, K26, K44).

**N. Decisiones pendientes del propietario.** PO-05 (confirmar que se refiere a la Adenda v9 y aceptarla o corregirla; HV-02 **NO VERIFICABLE** sin esa confirmación; línea 126 del registro y PO-05 sin tocar); aceptación del diseño G-1/G-5/G-10; DG-19 y la clave primaria de `channel_formats`; las 7 FK añadidas en V20 (parte del diseño no aceptado); RP-01, G-9, P-01..P-05, P-10, OD-13, DEP-RET-01, DG-09, DG-12, DG-16, DG-18, DG-20; autorizar CCI-DEV. `MATRIZ_HV02_PO05_EVIDENCIA.md`, `INVENTARIO_DECISIONES_ABIERTAS_FASE0.md`.

**O. V3.3.** SHA-256 recalculado sobre el original externo: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da`; sin cambio.

**P. Línea base.** 17 claves físicas, 5 roles, 13 transiciones T-02, 76 subfases y 27 tablas base: controles del verificador aprueban; no se añadieron permisos, roles, transiciones ni subfases (las FK añadidas reutilizan destinos únicos existentes y no son una tabla nueva).

**Q. No ejecutado y razón.** Pruebas contra un esquema físico real, RLS, privilegios, concurrencia, Supabase/Storage y cualquier integración externa: no existe esquema físico ni CCI-DEV y no están autorizados. Trigger de elegibilidad R1–R9 en PostgreSQL: requiere las 12 tablas restantes. Lectura línea a línea del código de las 22 funciones: no realizada; la evidencia contra pruebas circulares es la sensibilidad a mutaciones y la prueba de independencia. T-409..T-422 y los 12 escenarios PARCIAL: sin ejecución individual que los demuestre.

**R. Criterios C01–C32.** `MATRIZ_ACEPTACION_V20_C01_C32.md` (estado y evidencia uno por uno).

**S. Diff y commit.** Diff exclusivamente dentro de `docs/fase0/` (0 archivos fuera). SHA del commit y verificación remota: en la respuesta final de la intervención.

**T. Declaración final.** Los 32 criterios C01–C32 pasan en el ámbito documental y de pruebas locales (ninguno NO APROBADO ni NO VERIFICABLE).

V20 — AUDITORÍA INTEGRAL Y RECONCILIACIÓN DEL EXPEDIENTE G-1, G-5 Y G-10: COMPLETADA EN EL ÁMBITO DOCUMENTAL Y DE PRUEBAS LOCALES. Se reconciliaron los resultados de las 22 funciones, se corrigieron las inconsistencias de formato y referencias, se completaron las definiciones e inventarios estructurales, se ejecutó la auditoría semántica y se reprodujeron las pruebas locales. Las dependencias de aprobación del propietario y las validaciones reales de PostgreSQL/Supabase se mantienen expresamente pendientes cuando corresponda. V20 no equivale a aceptación formal del propietario, ni a validación de infraestructura real, ni a autorización de Fase 1.
