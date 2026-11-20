# VALIDACIÓN DE SERVICIOS EXTERNOS V16 (pendiente E)

> **Documento HISTÓRICO (V21, 2026-11-20):** evidencia de la etapa V16–V19 conservada tal como se produjo. Sus estados de publicación («local», «sin commit», «no publicado»), cifras (p. ej. 363 casos), clasificaciones de reglas (esquema V18/V19) y números de línea corresponden a la fecha de cada documento y **no** son el estado vigente. Estado vigente y fuente de verdad de cada dato: `../expediente_final_v21/INDICE_VIGENCIA_DOCUMENTAL_V21.md` y `../expediente_final_v21/MATRIZ_CONCILIACION_V21.md`.

Regla aplicada: no se simularon conexiones, no se sustituyó PostgreSQL por SQLite, no se usaron mocks para afirmar que Supabase funciona. Cada fila es una clasificación, no un resultado de prueba.

## 1. Evidencia observada sobre el acceso
- Herramientas de Supabase disponibles en la sesión; consulta de solo lectura de metadatos (2026-11-20): una organización («RevNavigator») y dos proyectos: «pruebas» (estado INACTIVE) y «Revnavigator» (ACTIVE_HEALTHY).
- Ninguno está designado para Copy & Creative Intelligence. «Revnavigator» pertenece a otra aplicación del usuario; ejecutar SQL, migraciones o pruebas ahí alteraría datos o esquema ajenos al expediente y contradice las reglas del expediente (sin SQL, migraciones ni Supabase en Fase 0). No se ejecutó ninguna consulta SQL ni migración.
- No hay servidor PostgreSQL local con las extensiones y roles del diseño disponible en el entorno de trabajo (no verificado más allá de la ausencia de configuración en el expediente).

## 2. Matriz
| Área | Pruebas diseñadas relacionadas | Clasificación | Qué falta | Estado |
|---|---|---|---|---|
| PostgreSQL (FK compuestas y diferidas RS-01 a RS-08, restricciones únicas, triggers) | RS-01 a RS-08; FK01–FK41 diseñadas; el verificador solo comprueba el texto y el modelo en memoria | C. No ejecutable | Instancia PostgreSQL dedicada a CCI (versión por definir), rol con permiso DDL, autorización expresa del propietario para Fase 1 | Pendiente |
| Supabase (proyecto, Auth, Storage) | Subfases 1.4, 1.7 | C. No ejecutable | Proyecto Supabase de CCI designado por el propietario; clave de servicio y URL por canal seguro; autorización | Pendiente |
| RLS | Matriz de 17 claves y políticas diseñadas (sección 6.1/6.8) | C. No ejecutable | Esquema creado, usuarios de prueba por rol, proyecto designado | Pendiente |
| Concurrencia | db_txid + attempt_nonce (G-10), unicidad de reutilización, subfase 9.6 | C. No ejecutable | Base real con transacciones concurrentes y arnés de carga | Pendiente |
| Integración externa (Cohere, Storage, hosting) | Subfases 2.2, 3.1, 9.8 | C. No ejecutable | Claves y proveedores no autorizados (P-01, P-03, P-07, P-10 abiertos) | Pendiente |
| Pruebas en memoria del modelo | K45–K59, suites AV/CF/AC/AP/ADV15/AT15, etc. | A. Ejecutada y aprobada (**no** es PostgreSQL ni Supabase) | — | Ejecutadas (ver REPORTE_REGRESION_V16.md) |
| Ninguna prueba | — | B. Ejecutada y fallida: ninguna; D. No aplicable: ninguna | — | — |

## 3. Procedimiento preparado para cuando exista infraestructura (no ejecutado)
1. El propietario designa un proyecto Supabase/PostgreSQL exclusivo de CCI y autoriza por escrito Fase 1 o una validación técnica acotada.
2. Crear el esquema desde las subfases del roadmap (1.5, 1.6, 1.8, 2.7, 5.3, 6.5), sin datos reales (restricción P-09: solo DEMO).
3. Ejecutar por orden: (a) existencia de las 41 tablas propuestas y de las FK compuestas con sus acciones y diferimiento; (b) cada mutación FK01–FK41 y cada relación RS-01 a RS-08 contra restricciones reales; (c) rechazos de reutilización y atomicidad (A01–A65, AT14, AT15) contra funciones reales; (d) políticas RLS con un usuario por rol y por organización; (e) concurrencia con transacciones simultáneas sobre G-10 y las aprobaciones.
4. Registrar por prueba: identificador, comando, versión de PostgreSQL, resultado, SHA-256 de la salida; sin mocks.

Pendiente de autorización: designación del proyecto, credenciales, ejecución de SQL y cualquier migración.

## Actualización V17
Sin cambios: no se usó Supabase ni ningún servicio externo, no se desplegó nada. Todas las validaciones reales (PostgreSQL, RLS, concurrencia, integración) siguen sin ejecutarse.

## Actualización V18: arquitectura de dos entornos e inventario de pruebas para Fase 1
**Estado:** diseño documentado, **no implementado**. Este repositorio no mencionaba CCI-DEV ni CCI-PROD antes de V18; se registran aquí como arquitectura objetivo indicada por la misión. No existen proyectos, y no se usó, creó ni modificó ningún proyecto de Supabase.

| Entorno | Propósito (diseño) | Estado |
|---|---|---|
| CCI-DEV | Desarrollo y todas las pruebas destructivas/concurrentes de Fase 1, con datos sintéticos | No existe; requiere autorización |
| CCI-PROD | Producción; sin pruebas destructivas; recibe migraciones solo tras aprobarlas en CCI-DEV | No existe; requiere autorización |

Los dos son independientes (proyectos, claves, bases y Storage separados; ninguna credencial compartida). No se muestran ni piden secretos.

| Área de prueba para Fase 1 | Qué debe probarse (ejemplos ligados a reglas/escenarios) | Evidencia hoy |
|---|---|---|
| PostgreSQL | FK compuestas, UNIQUE parciales, CHECK, triggers (IG1-03..07, IG5-37/38, IG10-13) | Solo modelo en memoria y escenarios «Ejecutable futura» |
| Migraciones | Orden único 14.1, fail-closed ante fase no ejecutada (IM-01..IM-12; T-153..T-164) | Solo documental |
| Auth | auth.uid() como único actor (IG5-82, IS-05, T-43) | Ninguna |
| RLS | Aislamiento por organization_id; tablas con RLS y sin privilegios (IM-09, IS-07, IS-12) | Ninguna |
| Roles y privilegios | Propietario dedicado, EXECUTE solo authenticated (IS-01..IS-04, IS-15) | Ninguna |
| Concurrencia | Orden de bloqueo, idempotencia, nonce (IG5-25, IG5-39, IG10-06, IG10-20; T-35, T-56, T-142) | Escenarios «Infraestructura real», sin ejecutar |
| Storage | Hash y verificación de artes, no transaccional con Storage (C8) | Ninguna |
| Edge Functions | Funciones de publicación y evaluación; no desplegadas | Ninguna |

Distinción: lo documentado (reglas, escenarios, arquitectura) no es integración implementada; ninguna fila de esta tabla está ejecutada.

## Actualización V19
Sin cambios: arquitectura objetivo CCI-DEV / CCI-PROD documentada y no implementada; no se usó Supabase, no se ejecutó SQL ni se desplegó nada; no se reutilizaron proyectos de otros productos. Se añaden al inventario de Fase 1, bajo PostgreSQL: PE-01 a PE-05 (FK compuesta entre organizaciones, inmutabilidad de master_piece_id y master_copy_version_id, aprobación por pieza y nueve columnas del par), todas pendientes hasta que exista autorización e infraestructura dedicada.
