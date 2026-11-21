# PLAN DE VALIDACIÓN EN CCI-DEV — **NO EJECUTADO**

> **Estado: PREPARADO, NO EJECUTADO.** Nada de este plan se ha ejecutado contra Supabase. Requiere (1) que exista el esquema físico en CCI-DEV, (2) autorización expresa y escrita del propietario, y (3) que el objetivo sea **CCI-DEV** (nunca CCI-PROD, nunca proyectos de RevNavigator). Los scripts están en `scripts_validacion/cci_dev_NO_EJECUTADOS/` y llevan una guarda que aborta si no se declara `cci.validacion_autorizada='SI-CCI-DEV'`.

## 1. Precondiciones y puertas de autorización

| Puerta | Condición | Quién decide |
|---|---|---|
| P0 | Existe el esquema físico (migraciones de Fase 1 aplicadas en CCI-DEV por una decisión previa del propietario) | Propietario |
| P1 | El propietario confirma por escrito el ID del proyecto CCI-DEV y que es independiente de CCI-PROD y de RevNavigator | Propietario |
| P2 | Autorización de lectura de catálogos (bloques INV y PRIV; sin escritura) | Propietario |
| P3 | Autorización de escritura en transacción con ROLLBACK (bloques RLS, R1–R9, CONC) con datos de prueba aislados | Propietario |
| P4 | Credenciales proporcionadas **por el propietario por canal seguro**; Claude no las pide ni las busca | Propietario |

Si P0 no se cumple, los bloques que dependen de tablas inexistentes quedan **BLOQUEADOS_POR_IMPLEMENTACIÓN** (no «fallidos»).

## 2. Bloques, orden y criterio de aceptación

| Bloque | Archivo | Tipo | Qué obtiene | Criterio de aceptación |
|---|---|---|---|---|
| INV | `01_inventario_esquema_SOLO_LECTURA.sql` | Lectura | Tablas, columnas/tipos, PK/FK/UNIQUE/CHECK/EXCLUDE, índices, triggers, funciones (propietario, SECURITY DEFINER, search_path), grafo de FK, extensiones, versión, recuento de tablas, columnas `*_id` sin FK | 41 tablas; todas las FK de la matriz FK01–FK41 presentes y validadas (`convalidated`); INV-10 sin filas inesperadas; funciones críticas `SECURITY DEFINER` con `search_path` fijo y propietario `cci_records_owner` |
| PRIV | `02_rls_privilegios_SOLO_LECTURA.sql` | Lectura | Políticas RLS, grants, matriz S/I/U/D/T efectiva, EXECUTE de funciones, atributos de roles, privilegios por defecto | RLS activa en todas las tablas con `organization_id`; `anon` sin privilegios sobre tablas de negocio; ningún INSERT/UPDATE/DELETE/TRUNCATE directo para `authenticated` en tablas inmutables; `service_role` sin acceso directo a tablas con escritura restringida a funciones |
| RLS | `03_pruebas_rls_ROLLBACK.sql` | Escritura con ROLLBACK | Fuga de lectura entre organizaciones (dinámica sobre todas las tablas), usuario sin membresía, anon, escritura cruzada, escalada | RLS-01..RLS-05 todas PASS |
| R19 | `04_trigger_r1_r9_ROLLBACK.sql` | Escritura con ROLLBACK | Nueve reglas de elegibilidad con casos negativos y positivo | Ver `PLAN_VALIDACION_TRIGGER_R1_R9.md` |
| CONC | `05_concurrencia_sesion_A/B.sql` | Escritura con ROLLBACK (dos sesiones) | Bloqueo y resolución de condiciones de carrera | Ver `PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md` |
| ATR | (por escribir tras existir las funciones de atribución) | Escritura con ROLLBACK | Equivalente físico de las 25 mutaciones K47 de T-409..T-422 | Rechazo de cada alteración equivalente |

## 3. Inventario físico: lista de verificación

Para cada tabla de `MATRIZ_MODELO_LOGICO_FISICO.md` (41): columnas y tipos exactos; nulabilidad; defaults; PK; FK compuestas con `organization_id` (y comprobar `MATCH SIMPLE` con columnas nulas); UNIQUE y destinos únicos de las FK; CHECK; índices (incluido el índice parcial `u_adr_aceptada`); triggers (inmutabilidad, elegibilidad, `asset_match`, independencia del aprobador); funciones autorizadas de escritura (`record_approval`, `transition_piece_status`, `review_finding`, `consume_ai_quota`…); y dependencias de creación (orden de subfases).

## 4. Evidencia y reproducibilidad

- Registrar: fecha, versión de PostgreSQL (`INV-08`), identificador del proyecto (el propietario lo confirma), SHA-256 de cada script ejecutado y salida íntegra sin editar.
- Cada resultado se archiva como un archivo nuevo; **no se sobrescribe** ningún resultado previo (los FAIL históricos se conservan).
- Un FAIL se reporta tal cual; no se «corrige» el script para obtener PASS sin documentar el cambio como nueva versión.

## 5. Qué NO debe hacerse en esta validación

No crear/alterar/borrar objetos permanentes; no ejecutar en CCI-PROD; no desplegar; no cambiar RLS ni privilegios (sólo observarlos); no reutilizar credenciales ni proyectos de RevNavigator; no iniciar Fase 1.

## 6. Resultado esperado y estados

Cada bloque termina como `PASS`, `FAIL`, `BLOQUEADO_POR_IMPLEMENTACIÓN` o `NO_EJECUTADO`. Mientras ningún bloque se ejecute, **todos** permanecen `NO_EJECUTADO` y el dictamen de preparación no puede pasar de `PREPARADO_CON_LIMITACIONES`.

## 7. Qué se validó localmente de estos scripts (y qué no)

- Guarda: sin autorización aborta (probado en el clúster local).
- `01` y `02`: ejecutan sin error en el clúster PostgreSQL temporal local (catálogos estándar).
- `03`: validado en un **shim local** (roles `anon/authenticated/service_role` simulados): detecta fuga y grants permisivos (corrida 1, FAIL esperado) y da PASS con el shim corregido (corrida 2) — `scripts_validacion/resultados/shim_rls_*.txt`. **No** equivale a Supabase (en Supabase hay `auth.uid()`, `authenticator`, políticas reales y grants por defecto distintos).
- `04`: **plantilla** no ejecutada ni siquiera en shim (depende de la función real `resolve_attribution_discard`, que no existe).
- `05`: la lógica de bloqueo se validó con el prototipo local (CC-01, CC-02); los archivos A/B no se ejecutaron.
