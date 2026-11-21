# MATRIZ DE ACEPTACIÓN V20 — C01 a C32

> **Superseded (V21, 2026-11-20):** sustituido por `../expediente_final_v21/INFORME_FINAL_V21.md` (criterios de aceptación V21 en su sección de criterios y en `REPORTE_VALIDACION_INTEGRAL_V21.md`). Se conserva sin cambios de contenido como registro histórico de V20; las cifras y los números de línea de la especificación que cita corresponden a la fecha de V20 (la numeración de líneas cambió después) y no deben leerse como estado vigente.

**Versión:** V20 · **Fecha:** 2026-11-20 · **Fuente:** prompt de cierre integral V20 (criterios C01–C32), evidencia de este directorio · **Estado de verificación:** estados permitidos solo APROBADO / NO APROBADO / NO VERIFICABLE POR DEPENDENCIA EXTERNA. Esta matriz **sustituye** a `MATRIZ_FINAL_C01_C30_V16_V19.md` (escala C01–C30 de la pasada anterior, conservada como histórico). Aprobado aquí significa «cumple el criterio documental o de pruebas locales»; **no** es aceptación del propietario.

| ID | Criterio | Estado | Evidencia |
|---|---|---|---|
| C01 | Rama y commit base verificados | APROBADO | Rama `audit/fase0-v19-review`, HEAD c6ef74be… (padre 6a1af24…) al inicio y antes del commit. |
| C02 | `main` permanece intacta | APROBADO | `git ls-remote`: main = 6a1af2424ef39e0960b8f7e09d4e19ec52e6f046 (se repite tras el push; ver informe). |
| C03 | Inventario completo de archivos activos | APROBADO | `MANIFIESTO_EVIDENCIAS_SHA256.txt` (todos los archivos de docs/fase0 con SHA-256). |
| C04 | Reconciliación matemática de los 363/366 casos | APROBADO | 366 = 363 + 3 positivos de K45; causa raíz: el script V18 no contaba los positivos. `MATRIZ_PRUEBAS_22_FUNCIONES_366_CASOS.md`, `REGISTRO_CASOS_22_FUNCIONES_V20.csv` (366 claves únicas, 0 duplicados). |
| C05 | 22 funciones individualizadas | APROBADO | 22 funciones, cada caso con id, esperado, obtenido, PASS/FAIL (registro CSV). |
| C06 | Instrumentación independiente y no circular | APROBADO | El script de instrumentación es externo y no altera la lógica; la independencia del auditor se probó aparte (C17). Limitación: no se hizo una lectura línea a línea de las 22 funciones; la evidencia contra pruebas circulares es la sensibilidad a mutaciones (213 casos de mutación detectados, 300 mutaciones del verificador). |
| C07 | Dos corridas reproducibles comparadas por hash | APROBADO | Dos corridas completas del verificador en copias limpias: salidas idénticas (SHA-256 f71e2c3e3bb0fdcb…); 22 funciones ×2 idénticas (f683969f6b8ecd3d…); PostgreSQL ×2 idéntico (1e56d06637ab1ad1…). `REPORTE_REGRESION_FINAL.md`. |
| C08 | Cero advertencias de formato en archivos modificados | APROBADO | `git diff --cached --check c6ef74b` (índice temporal): RC=0, 0 advertencias; 0 BOM y 0 CR en archivos modificados/nuevos (REPORTE_FORMATO_Y_INTEGRIDAD.md; INFORME_FINAL_V20.md §E). |
| C09 | CSV íntegros después de normalización | APROBADO | Igualdad lógica fila a fila, UTF-8 sin BOM, LF; 0 BOM y 0 CR en los CSV (REPORTE_REGRESION_FINAL.md). |
| C10 | Definición estructural completa de `channel_formats` | APROBADO | Bloque de especificación (columnas, tipos, nulabilidad, clave alternativa única compuesta, FK, CHECK, no DELETE, baja lógica, RLS); PG-CF-01..15 en PostgreSQL temporal. La **clave primaria** sigue NO DETERMINADA (la fuente no la declara y no se inventó); es una decisión técnica identificada, no una omisión. |
| C11 | `attribution_discard_resolutions`: inventario y relaciones completos | APROBADO | Fila 1270 corregida; 22 columnas, 8 FK, uniques, CHECK, triggers revisados; PG-AD-01..20. |
| C12 | `version_contributors` y conjunto E coherentes | APROBADO | K46/K47, ATTR-01..12, E14-01..06 y PG-AD (aceptada → histórica; rechazada permanece activa; reconsideración = fila nueva). |
| C13 | Auditoría semántica individual de las 231 reglas | APROBADO | `MATRIZ_FINAL_231_REGLAS_V16_V19.csv`: A 1, B 8, C 69, D 153, E 0 (esquema V20). |
| C14 | Revisión semántica individual de los 780 escenarios | APROBADO | `MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv`: 258 por ejecución en modelo, 510 por lectura (6 con observación), 12 PARCIAL clasificados como tales. Cobertura real y trazabilidad nominal distinguidas por columna. |
| C15 | Revisión específica de las cinco reglas E | APROBADO | IG1-05, IG1-06, IG1-10, IG1-21, IG5-36 revisadas; ahora con evidencia en PostgreSQL (fixture) → clase B. |
| C16 | PE-01..PE-05 ejecutadas donde el entorno lo permita y preparadas donde no | APROBADO | PostgreSQL 16.15 temporal: 63/63 PASS, mutaciones 14/14; comandos en `PE_POSTGRESQL_V20/`. Contra el esquema real/CCI-DEV: preparado, no ejecutado (falta autorización y esquema). |
| C17 | Independencia real del motor y del auditor | APROBADO | `independencia_auditor_v20.py`: el auditor no llama métodos del Motor (estático) y da el mismo resultado con todos los métodos del motor rotos (48 adversariales; 913 invocaciones; 0 llamadas), con control negativo. |
| C18 | Regresión histórica completa | APROBADO | Verificador completo 59/59, 28/28, 300/300 sin cambios de resultado; 22 funciones 366/366; identificadores descubiertos en la salida (ver reporte); ninguna suite omitida. |
| C19 | K32 estructural y semánticamente coherente | APROBADO | K32 aprueba; revisión V20 halló y corrigió 7 columnas sin FK. |
| C20 | K45 estructural y semánticamente coherente | APROBADO | K45 aprueba; 27 mutaciones + 3 positivos detectados/aceptados. |
| C21 | K55 sin duplicidades ni contradicciones | APROBADO | K55 aprueba; contradicción 363/366 resuelta. |
| C22 | Inventario completo de fuentes físicas | APROBADO | 14 tablas nuevas (5+4+4+1); 27+14=41; `REVISION_FUENTES_FISICAS_K32_K45_K55_V20.md`; prueba estructural 4/4 (y falla contra la especificación anterior, como debe). |
| C23 | Referencias históricas y activas coherentes | APROBADO | 1.148 referencias (H 1.022, A 125, I 0, U 1: PO-05, preservada) + suplemento V20 (A). |
| C24 | PO-05 y otras decisiones pendientes preservadas | APROBADO | `MATRIZ_HV02_PO05_EVIDENCIA.md`, `INVENTARIO_DECISIONES_ABIERTAS_FASE0.md`; PO-05 sin modificar, línea 126 del registro intacta. |
| C25 | Hash V3.3 y línea base protegidos | APROBADO | Original externo recalculado: b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da. |
| C26 | Sin cambios de permisos, roles, transiciones o subfases | APROBADO | Controles del verificador (17 claves, 5 roles, 13 T-02, 76 subfases, 27 tablas base) aprueban; las FK y filas de contrato añadidas no tocan permisos ni transiciones. |
| C27 | Documentación, scripts y pruebas consistentes | APROBADO | Cifras 231/780/41/22/366 iguales en los cinco documentos y la evidencia (grep sin `363 casos`); verificador 59/59. |
| C28 | Historial V3–V19 conservado | APROBADO | `docs/fase0/historico/` sin diferencias frente a c6ef74b; evidencia histórica no sobrescrita (se añadieron notas fechadas y salidas nuevas). |
| C29 | Alcance de pruebas y limitaciones correctamente declarado | APROBADO | Informe sección Q; fixture PostgreSQL ≠ esquema real; nada de RLS/concurrencia/Supabase. |
| C30 | Diff final exclusivamente dentro de `docs/fase0/` | APROBADO | `git diff --cached --name-only c6ef74b`: 59 archivos, 0 fuera de `docs/fase0/`; motor, verificador e `historico/` sin cambios. |
| C31 | Cero regresiones nuevas | APROBADO | Única diferencia frente a V19: K14/K26/K44 con las relaciones añadidas (esperado); ninguna prueba cambió de estado. |
| C32 | Informe final con evidencia verificable | APROBADO | `INFORME_FINAL_V20.md` (secciones A–T) con referencias a la evidencia archivada. |
