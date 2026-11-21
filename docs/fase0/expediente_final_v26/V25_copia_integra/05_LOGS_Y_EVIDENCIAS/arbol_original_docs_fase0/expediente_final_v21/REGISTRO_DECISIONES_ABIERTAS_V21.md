# REGISTRO DE DECISIONES ABIERTAS Y LIMITACIONES EXTERNAS (V21)

**Versión:** V21 · **Fecha:** 2026-11-20 · **Fuente:** `../expediente_final_v16_v19/INVENTARIO_DECISIONES_ABIERTAS_FASE0.md` (corregido en V21), `../ESPECIFICACION_TECNICA_G1_G5_G10.md`, `../REGISTRO_HISTORICO_VERSIONES.md`, `../expediente_final_v16_v19/MATRIZ_HV02_PO05_EVIDENCIA.md` · **Estado de verificación:** cada fila se contrastó con su fuente; la prueba V21-E06 comprueba que ninguna decisión figura como aprobada, aceptada o cerrada.

**Decisiones nuevas creadas en V21: ninguna. Decisiones marcadas como aprobadas o cerradas en V21: ninguna.** Este registro no interpreta ni resuelve; reproduce el estado según las fuentes. Es la fuente de verdad vigente de las decisiones abiertas; el inventario V20 corregido conserva el detalle por familia de reglas.

## A. Decisiones exclusivas del propietario (abiertas)
| ID | Qué se debe decidir (según fuentes) | Fuente | Estado | Qué evidencia existe | Qué la desbloquea |
|---|---|---|---|---|---|
| PO-05 / HV-02 | Confirmar que «aceptación formal del addendum» se refiere hoy a la Adenda v9 y aceptarla o devolver correcciones | Registro histórico, línea 126; `MATRIZ_HV02_PO05_EVIDENCIA.md` | **NO VERIFICABLE** sin confirmación expresa; la Adenda v9 **no está aceptada** | La fila 126 dice «addendum v3»: redacción de su época; ninguna adenda se marca aceptada | Declaración expresa del propietario (aceptar, o corregir) |
| G-1, G-5, G-10 | Aceptación formal del diseño complementario (tablas, funciones, reglas) | Especificación (diseño); registro histórico | **Diseño NO aceptado** | 231 reglas, 780 escenarios, 366 casos en modelo, 63 pruebas en PostgreSQL temporal: que pasen **no equivale a aceptación** | Aceptación o rechazo expreso; de ella dependen las 153 reglas de clase D y las 7 FK compuestas añadidas en V20 |
| DG-19 | Canales y formatos reales de la organización; catálogo `channel_rules` + `channel_formats` desde la subfase 1.8 | Especificación IG1-32, sección 3.14 | **Pendiente** de la organización/propietario | `channel_formats` tiene definición formal derivada; sin valores reales | Catálogo real aprobado |
| `channel_formats` — clave primaria y columnas definitivas | Elegir la PK y confirmar columnas | Especificación, definición formal de `channel_formats` | **No determinada** a propósito (la especificación no la fija) | Clave única compuesta derivada; PK no elegida | Decisión del propietario (junto con DG-19) |
| DG-20 | Ampliación mínima de v3.3: columna `approvals.decision` (CHECK = 'aprobada') | Especificación, tabla de decisiones y sección «Ampliación mínima» | Resuelta técnicamente en la especificación pero **sujeta a la aceptación** del propietario | Spec | Aceptación o rechazo |
| DG-09 | Retención | Especificación, línea 40 | Diferida | Spec | Decisión de retención |
| DG-12 | Hash encadenado (6.6) | Especificación, línea 40 | Diferida | Spec | Diseño de 6.6 |
| DG-16 | Umbrales, hasta resolver T-03 | Especificación, línea 40 | Diferida | Spec | Resolver T-03 |
| DG-18 | `replaces_piece_id` opcional | Especificación, línea 117 | Sujeta a decisión | Spec | Decisión del propietario |
| DEP-RET-01 | Dependencia de retención (procedimiento operativo) | Especificación | Diferida | Spec | Resolver DG-09 |
| G-9 | Historial de revisor asignado (`piece_reviewer_assignments`), solo la asignación | Especificación, línea 415 y siguientes | Abierta/condicionada (G-9 completo sigue abierto) | Diseño, sin SQL de producción | Aceptación del diseño |
| RP-01 | Designar responsable del nivel 3 con identidad real | Registro histórico, línea 117; especificación sección P | Pendiente del propietario | Adendas v4–v8 | Nombre del responsable |
| P-01..P-05, P-10 | Pendientes del propietario de las adendas | Adenda v9, sección «Pendiente» | Pendiente | Adenda v9 | Decisión expresa de cada uno |
| OD-13 | Decisión original reservada | Adenda v9; especificación sección P | Pendiente | Adenda v9 | Decisión del propietario |

## B. Autorizaciones y estados que siguen siendo del propietario
| Elemento | Estado | Condición para cambiar |
|---|---|---|
| Fase 1 | **NO INICIADA y NO AUTORIZADA** | Aceptación formal de lo anterior y autorización expresa del propietario |
| Validación física en **CCI-DEV** (proyecto Supabase propio de CCI) | **No realizada; no autorizada** | Autorización expresa del propietario; esquema físico revisado |
| Promoción a **CCI-PROD** | **No realizada; no autorizada** | Validación en CCI-DEV con evidencia archivada y aceptaciones del apartado A (ver `../expediente_final_v16_v19/PLAN_VALIDACION_POSTGRESQL_SUPABASE_CCI.md`) |
| Proyectos de RevNavigator | **No se reutilizan ni se conectan** | — |
| Publicación (commit/push) de V21 | **No realizada** | Autorización expresa del propietario |

## C. Limitaciones externas reales (no son defectos documentales)
1. **No existe esquema físico ni CCI-DEV**: no se puede validar RLS, privilegios, concurrencia real, triggers sobre el esquema real, PE-01..PE-05 contra el esquema real, ni Supabase/Storage. Lo ejecutado (63 pruebas y 14 mutaciones) corre sobre un fixture derivado del diseño en un PostgreSQL 16 temporal y **no equivale al esquema físico aprobado ni a una validación de Supabase**.
2. **Trigger de elegibilidad R1–R9**: requiere las 12 tablas restantes que el fixture no incluye.
3. **12 escenarios PARCIAL**: no demuestran toda su obligación sin esquema físico (listados en `../expediente_final_v16_v19/MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv`, veredicto «PARCIAL / NO DEMUESTRA TODO»).
4. **T-409..T-422**: sin ejecución individual propia; su obligación se cubre por lectura (según la matriz de escenarios).
5. **Lectura de las 22 funciones**: la evidencia de que sus pruebas no son circulares es la sensibilidad a mutaciones y la independencia del auditor (6/6); no se afirma una lectura línea a línea de su código.
