---
name: informe_cierre_g1_g5_g10
description: Informe de la revisión v15 de G-1, G-5 y G-10 (integridad del evento propio en cada eslabón: asset_version y campo, validación previa del motor, auditor independiente, atomicidad con instantánea completa y cierre de K55); diseño documental con pruebas de modelo en memoria; nada ejecutado en PostgreSQL
---

# INFORME — INTEGRIDAD DEL EVENTO PROPIO EN CADA ESLABÓN (revisión v15)

Sustituye al informe v14 (conservado en `historico/`). Diseño documental con pruebas de modelo en memoria: no se ejecutó SQL, código de producto, Supabase ni PostgreSQL. La «v15» de este documento es la revisión del diseño complementario; no es la Adenda v9 del propietario (PO-05). La corrección documental V16 (commit `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`) solo alinea la identificación de la versión vigente en el roadmap; no es una revisión del diseño y no modifica este informe: el diseño técnico complementario vigente sigue siendo la v15 (ver `REGISTRO_HISTORICO_VERSIONES.md`, nota de trazabilidad V16).

## A. Dictamen ejecutivo

| Nivel | Estado | Alcance |
|---|---|---|
| 1. Fase 0 v3.3 | COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES DOCUMENTADAS | No se reabre ni se modifica; SHA-256 `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` sin cambio |
| 2. Diseño complementario v15 (G-1, G-5, G-10) | COMPLETADO DOCUMENTALMENTE Y PREPARADO PARA ACEPTACIÓN FORMAL DEL PROPIETARIO, CON LIMITACIONES TÉCNICAS EXPLÍCITAS | Pendiente de aceptación formal del propietario; no validado técnicamente; la Adenda v9 sigue sin aceptar (PO-05) |
| 3. Fase 1 | NO INICIADA / NO AUTORIZADA | Requiere autorización expresa; este diseño no la concede |


**Niveles de evidencia usados en este expediente.**

| Nivel de evidencia | Significado | Alcance |
|---|---|---|
| Diseñado | La regla o el escenario está escrito en la especificación | Nada ejecutado |
| Verificado documentalmente | El verificador publicado comprobó coherencia entre los documentos: IDs, referencias, cifras, contratos, orden, estados | Resultado reproducible; no prueba que el diseño funcione en PostgreSQL |
| Validado técnicamente | Ejecución real contra PostgreSQL, RLS y Supabase con las pruebas de la matriz | **Pendiente**: ningún control ni escenario alcanza este nivel |


**Resultado de la verificación (calculado por el verificador publicado).**

| Control | Mutaciones | Detectadas | Casos positivos | Resultado |
|---|---|---|---|---|
| K45 | 27 | 27 | 3 casos positivos aprobados | OK |
| K46 | 12 | 12 | resolutores elegibles aceptados | OK |
| K47 | 36 | 36 | 12/12 escenarios A a L y comprobaciones U, S, X y R aprobados | OK |
| K47 resoluciones inmutables | 12 | 12 | escenario RS y 9 intentos directos rechazados | OK |
| K47 validación previa del origen (A54 a A65) | 12 | 12 | rechazo sin escritura, estado previo idéntico y E nulo en cada una; 20 pruebas de atomicidad aprobadas | OK |
| K47 procedencia e identidad del arte (A01 a A53) | 53 | 53 | 26/26 casos positivos de arte (P01 a P26) aprobados; 16/16 pruebas adversariales aprobadas | OK |
| K56 cadena, atribuciones, asset_version, campo y código del modelo (CHAIN, ATTR, AV, CF, AC, K56-M) | 70 | 70 | ADVC 24/24, AT14 11/11, E14 6/6, AP 8/8, ADV15 8/8 y AT15 8/8 aprobadas | OK |
| FK01 a FK41 (K32, K44, K45 y K55) | 41 | 41 (lo calcula el verificador) | mutaciones estructurales sobre la especificación |  |
| K57 mutaciones documentales de trazabilidad e identidad de controles | 12 | 12 (lo calcula el verificador) | K57-D01 a K57-D12 |  |
| Total estructural | 222 | 222 | más 25 mutaciones documentales M-01 a M-25, 41 mutaciones FK y 12 mutaciones K57-D |  |


La v15 audita la v14 y corrige la validación del evento propio de cada eslabón: `asset_version` contra la versión exacta del asset de destino y `campo` igual a arte, con diagnóstico estructurado por vínculo, rechazo previo a escritura, atomicidad con instantánea completa en ocho momentos, auditor independiente reforzado y el identificador K55 duplicado resuelto (K55 y K55-V12). Las pruebas son de modelo en memoria y comprobaciones documentales; **ninguna es una prueba en PostgreSQL ni Supabase** y la aceptación del propietario sigue pendiente.

## B. Qué se corrigió

### H-01 El asset_version del evento propio de reutilización no se validaba contra la versión exacta del asset de destino

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | `Motor._verificar_reutilizado` y `Motor._datos_evento` de la v14 comprobaban `source_asset_version` pero no que `asset_version` coincidiera con la versión exacta del asset que produjo el evento: una corrupción en cualquier eslabón se aceptaba y el evento del destino guardaba la versión del origen. |
| Corrección | `Motor._chk_asset_version` valida por identidad exacta (`asset_version_id`) en todos los eslabones; `registrar_asset` escribe la versión 1 del destino; `source_asset_version` se valida aparte; las 15 validaciones por evento propio (sección 4.4.17 C) rechazan antes de escribir. |
| Documento y sección | ESPECIFICACION 4.4.17 A, B y C |
| Reglas | IG5-111, IE-12 |
| Evidencia | AV-01 a AV-08; K56-M09 |
| Escenarios diseñados | T-727 a T-734 (8; ninguno ejecutado) |

### H-02 El campo del evento propio no se validaba como «arte» en cada eslabón

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | La v14 no comprobaba el campo del evento propio en la reconstrucción de la cadena: un evento vinculado a otro campo (por ejemplo headline o precio), ausente o nulo se aceptaba. |
| Corrección | `Motor._chk_campo` y `Motor._campos_permitidos` exigen campo = arte en reutilizaciones, cargas modificadas y raíz, antes de escribir y también después de construida una cadena posterior. |
| Documento y sección | ESPECIFICACION 4.4.17 C y F |
| Reglas | IG5-112, IE-12 |
| Evidencia | CF-01 a CF-08; K56-M10 |
| Escenarios diseñados | T-735 a T-742 (8; ninguno ejecutado) |

### H-03 El rechazo no identificaba el vínculo, el evento, el campo, lo esperado ni lo hallado

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Un rechazo no permitía distinguir qué relación fallaba ni descartar que otra excepción lo hubiera provocado. |
| Corrección | `ReutilizacionInvalida.detalles` informa eslabón, evento, campo, esperado, hallado y motivo; `mensaje_usuario` no expone datos internos; una excepción ajena nunca cuenta como detección; mutaciones combinadas AC-01 a AC-06. |
| Documento y sección | ESPECIFICACION 4.4.17 D y G |
| Reglas | IG5-113, IE-12 |
| Evidencia | AC-01 a AC-06; K56-M12 |
| Escenarios diseñados | T-743 a T-748 (6; ninguno ejecutado) |

### H-04 Faltaban suites negativas con doce condiciones por mutación

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Las mutaciones de la v14 no exigían, juntas, estado inicial válido, cambio real, rechazo, causa concreta, ausencia de asset, evento, atribución y relación parciales, estado completo idéntico, procedencia incompleta, E no completo y bloqueo de impacto, aprobación y publicación. |
| Corrección | AV-01 a AV-08, CF-01 a CF-08 y AC-01 a AC-06, cada una con las doce condiciones; ninguna se acepta por una excepción ajena. |
| Documento y sección | ESPECIFICACION 4.4.17 E, F y G |
| Reglas | IG5-111 a IG5-114 |
| Evidencia | AV-01 a AV-08; CF-01 a CF-08; AC-01 a AC-06 |
| Escenarios diseñados | T-727 a T-748 (22; ninguno ejecutado) |

### H-05 Faltaban casos positivos de las nuevas validaciones

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Sin casos válidos no se demuestra que las validaciones no bloqueen relaciones correctas. |
| Corrección | AP-01 a AP-08: cadenas de dos y tres niveles, versiones iguales de assets distintos, reutilización tras una modificación, uploader original distinto, atribución directa exacta, campo arte en todos los eventos y coincidencia motor-auditor. |
| Documento y sección | ESPECIFICACION 4.4.17 H |
| Reglas | IG5-111 a IG5-113 |
| Evidencia | AP-01 a AP-08 |
| Escenarios diseñados | T-749 a T-756 (8; ninguno ejecutado) |

### H-06 El auditor independiente no comparaba asset_version ni campo por eslabón

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Un motor que aceptaba una corrupción de esas referencias no era detectado por el auditor. |
| Corrección | `_hall_cadena` compara asset_version y campo por eslabón sin funciones del motor (`_compartidas()` vacío); ADV15-01 a ADV15-08 fuerzan la aceptación y exigen detección, E bloqueado y fallo cerrado de impacto y publicación. |
| Documento y sección | ESPECIFICACION 4.4.17 I |
| Reglas | IG5-115 |
| Evidencia | ADV15-01 a ADV15-08; K56-M11 |
| Escenarios diseñados | T-757 a T-764 (8; ninguno ejecutado) |

### H-07 La atomicidad no se probaba con instantánea completa en cada momento de fallo

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Un fallo en la validación de asset_version, campo, actor o atribución, o durante el registro, no comparaba el estado completo ni los datos derivados. |
| Corrección | AT15-01 a AT15-08 inyectan el fallo en ocho momentos, comparan el estado completo y los datos derivados y repiten sin fallo con un registro válido. |
| Documento y sección | ESPECIFICACION 4.4.17 J |
| Reglas | IG5-114 |
| Evidencia | AT15-01 a AT15-08 |
| Escenarios diseñados | T-765 a T-772 (8; ninguno ejecutado) |

### H-08 El identificador K55 estaba asignado a dos controles del verificador

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Un identificador repetido impedía citar y mutar cada control de forma inequívoca. |
| Corrección | El segundo control pasa a K55-V12 sin eliminar ninguna condición; equivalencia documentada; K58 exige identificadores únicos y que los documentos citen K55-V12; K57-D09 reintroduce el duplicado y es detectada. |
| Documento y sección | ESPECIFICACION 4.4.17 N |
| Reglas | IG5-116 |
| Evidencia | K58; K57-D09 |
| Escenarios diseñados | T-777 a T-777 (1; ninguno ejecutado) |

### H-09 La comparación estructural no cubría las nuevas validaciones ni las suites

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Las validaciones, el auditor, las suites AV, CF, AC y AP y la cobertura debían contrastarse con el modelo y el documento. |
| Corrección | K56 ejecuta las doce baterías y verifica la estructura del código (validaciones existentes e invocadas, auditor sin llamadas al motor, pruebas históricas conservadas, sin skip ni xfail); K57 compara reglas, validaciones y tablas; K59 comprueba la cobertura v15; K56-M09 a K56-M12 y K57-D09 a K57-D12 degradan código y documento. |
| Documento y sección | ESPECIFICACION 4.4.17 K, L y M |
| Reglas | IG5-116 |
| Evidencia | K56-M09 a K56-M12; K57-D09 a K57-D12 |
| Escenarios diseñados | T-773 a T-776 (4; ninguno ejecutado) |

### H-10 La regresión debía conservar todas las pruebas históricas y ser reproducible

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Una corrección no debe reducir cobertura ni producir resultados distintos entre ejecuciones. |
| Corrección | Se conservan CHAIN, ADVC, ATTR, AT14, E14, K45, K46, K47, FK y K57-D01 a K57-D12; dos ejecuciones limpias con `env -i` producen salidas --md y --json idénticas. |
| Documento y sección | ESPECIFICACION 4.4.17 O; AUDITORIA 3 |
| Reglas | IG5-116 |
| Evidencia | K41 y la comparación de salidas de la publicación |
| Escenarios diseñados | T-779 a T-779 (1; ninguno ejecutado) |

### H-11 Los documentos debían describir la v15 sin contradicciones

| Concepto | Detalle |
|---|---|
| Defecto en la v14 | Especificación, informe, auditoría, roadmap, registro y herramientas debían contar lo mismo. |
| Corrección | Los cinco documentos se regeneran con las mismas cifras; se conservan las copias históricas v14 y las anteriores con su SHA-256 en el manifiesto. |
| Documento y sección | todos |
| Reglas | IG5-116, IE-12 |
| Evidencia | K09, K22, K25, K27, K28 |
| Escenarios diseñados | T-780 a T-780 (1; ninguno ejecutado) |

## C. Modelo y relaciones

| Elemento | Detalle |
|---|---|
| Tablas | 27 históricas sin cambio; 14 nuevas propuestas: `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats`, `brief_versions`, `promotion_snapshots`, `contribution_events`, `copy_version_provenance`, `brief_field_changes`, `brief_field_attributions`, `promotion_field_changes`, `promotion_field_attributions`, `attribution_discard_resolutions`; la v15 no crea tablas |
| Orden definitivo | 1.8 → 2.x → 2.1 → 2.3 → 2.5 → 2.7 → 3.x → 4.x → 5.1 → 5.3 → 6.x → 6.1 → 6.5 → 6.6 → 8.x |
| Atribución por campo | 12 campos materiales de brief y 9 de promoción; las atribuciones se conservan siempre; solo una resolución aceptada de `attribution_discard_resolutions` (independiente y con evidencia) las vuelve históricas; el historial no se reactiva sin resolución (regla I15) |
| Integridad | Toda FK es compuesta e incluye organization_id; RS-01 a RS-08 fijan la identidad exacta del origen; solo RS-06 es diferida; `unique(organization_id, reuse_event_id)` impide que un evento de reutilización pertenezca a dos assets |
| Funciones | create_brief_version, create_promotion_snapshot, create_copy_version, verify_field_provenance (interna), version_contributors y las anteriores; sin funciones ni triggers nuevos en la v15 |
| Límites | IS-11: superusuario, propietario, desactivación de triggers y edición manual no los impide el diseño |

## D. Fórmula de contribuyentes y elegibilidad

**E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v ∈ [V-D, V-B] ∪ P.** La fórmula, la exclusión del proponente de la clasificación vigente (DT-02) y la ausencia de autoevaluación y de asignación automática a Admin no cambian. E solo se reconstruye desde cadenas verificadas; un evaluador es elegible si cumple E1 a E7 (sección 4.4.16 H) y ante cualquier cadena incompleta se bloquean E, la evaluación, la confirmación de independencia y la aprobación o publicación, sin excepción de Admin. Quién puede registrar la asignación en `piece_reviewer_assignments` sigue en G-9 (abierto).

## E. Verificación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 231 |
| Pruebas diseñadas | 780 (documental 450 / técnica futura ejecutable 281 / infraestructura real 49); **ninguna ejecutada**; cobertura regla↔escenario completa según el verificador |
| Tablas propuestas | 41 (27 históricas + 14 nuevas) |
| Verificación documental y estructural | 59 comprobaciones y 300 mutaciones del verificador publicado; resultado real en AUDITORIA_FINAL_G1_G5_G10.md, sección 3 |
| Pruebas de modelo en memoria ejecutadas | K45 (15 controles), K47 (12 escenarios, 26 casos positivos de arte, 16 adversariales, 28 invariantes), K46, CHAIN 24, ADVC 24, ATTR 12, AT14 11, E14 6, AV 8, CF 8, AC 6, AP 8, ADV15 8, AT15 8 y K56-M 12, con datos ficticios; resultado real en la auditoría |
| Pruebas técnicas pendientes | Todas las de PostgreSQL, RLS, Supabase, transacciones, concurrencia, bloqueos y rollback: nada de eso se ejecutó |

## F. Pendientes

PO-05 y aceptación de la Adenda v9; aceptación formal de esta revisión; DG-09, DG-12, DG-16, DG-18, DG-19, DG-20; RP-01; P-01 a P-05; P-10; OD-13; G-9 completo; DEP-RET-01; valores reales de canal y formato; validación de infraestructura; pruebas reales de PostgreSQL, RLS y Supabase; pruebas reales de concurrencia, bloqueos y rollback; validación externa y operativa. Ninguno se resuelve en esta revisión.

## G. Integridad y GitHub

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (sin cambio). Publicación en `main` de `appalex47-lab/Copy-Creative-Intelligence`, carpeta `docs/fase0/`. Commit anterior `1d14e51a539bca3e8b938288bd63c6d8aba0d0ed`. El commit nuevo y los SHA-256 de los cinco documentos se informan en el mensaje final.

## H. Declaración de alcance

Sin código de aplicación, sin SQL ejecutable, sin migraciones, sin recursos Supabase, sin infraestructura ni despliegue; v3.3 sin alterar; T-02 conserva sus 13 transiciones y no hay permisos nuevos (17 claves físicas); Fase 1 no iniciada; ninguna decisión del propietario se da por tomada y no se declara aceptación del propietario.


## Nota de estado V20 (2026-11-19) — bloque uniforme en los cinco documentos activos

Esta nota no modifica ni reemplaza lo anterior; distingue seis estados que no deben confundirse.

| Estado | Situación |
|---|---|
| Histórico | Fase 0 v3.3 conservada como línea base documental (SHA-256 b5dccdc7…c1da, sin cambio); el diseño complementario vigente es la revisión v15; las notas V16 a V19 son trabajo de auditoría documental. |
| Publicación | Rama `audit/fase0-v19-review`, commit `c6ef74be4db185ac3e4fd36810f24619e6f51fcf` (V16–V19, padre `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`). `main` permanece en V16 (`6a1af24`). El trabajo V20 (`expediente_final_v16_v19/`) está solo en el árbol local, sin commit. Sin pull request ni merge. |
| Auditoría | Cierre integral V16–V20 (segunda pasada V20 con prompt de reconciliación) documentado en `expediente_final_v16_v19/` (231 reglas, 780 escenarios, 22 funciones / 366 casos, matriz C01–C30). Solo documental y en modelo en memoria. |
| Aceptación del propietario | Ni V15–V20, ni la Adenda v9 (PO-05), ni G-1, G-5 y G-10 están aceptados; todo sigue pendiente del propietario. |
| Integración | No integrado con la vista previa privada. |
| Producción | Sin despliegue, sin Supabase, sin migraciones ni esquema físico; solo un fixture SQL de prueba ejecutado en un PostgreSQL temporal aislado (`expediente_final_v16_v19/PE_POSTGRESQL_V20/`); Fase 1 NO INICIADA / NO AUTORIZADA. |

Limitaciones vigentes: 153 reglas condicionadas por diseño no aceptado (G-1, G-5, G-10); las 5 reglas antes con evidencia insuficiente (IG1-05, IG1-06, IG1-10, IG1-21, IG5-36) pasaron a B: PE-01 a PE-05 se ejecutaron en un PostgreSQL 16 temporal con un fixture derivado del diseño (63/63 PASS), sin esquema físico aprobado ni Supabase; 12 escenarios parciales; sin validación contra un esquema físico real, RLS, concurrencia ni Supabase; HV-02 (PO-05 «v3» frente a Adenda v9) no verificable sin confirmación del propietario; decisiones reservadas abiertas (RP-01, G-9, P-01 a P-05, P-10, OD-13, DEP-RET-01, DG-09, DG-12, DG-16, DG-18, DG-19, DG-20).
