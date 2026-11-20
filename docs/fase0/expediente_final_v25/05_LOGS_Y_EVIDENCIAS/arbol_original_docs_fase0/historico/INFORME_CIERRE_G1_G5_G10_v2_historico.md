---
name: informe_cierre_g1_g5_g10
description: Informe actualizado de la revisión final de G-1, G-5 y G-10 con DG-01 a DG-16 incorporadas; especificación consolidada v2 lista para aceptación formal
---

# INFORME ACTUALIZADO — REVISIÓN FINAL Y CIERRE DE G-1, G-5 Y G-10 (v2)

Sustituye al informe de la v1 (conservado como `INFORME_CIERRE_G1_G5_G10_v1_historico.md`). No se rehicieron los documentos desde cero: se incorporaron tus decisiones y se corrigieron las inconsistencias. Solo diseño; nada ejecutado.

## A. Resultado individual

| Brecha | Resultado | Cambio principal frente a la v1 |
|---|---|---|
| G-1 | Modelo técnico consistente en diseño | `is_master` pasa a `is_adaptation` (una pieza con `master_piece_id` NULL no es necesariamente maestra); canal y formato con tipos y relación con `channel_rules`; clave de adaptación con identidad y única parcial; un nivel; versión y arte de origen por FK compuestas |
| G-5 | Registro y elegibilidad verificables en diseño | La asignación y el evaluador se ligan por FK compuesta; vigencia, permiso e independencia por función y trigger bajo bloqueo; orden único de bloqueo y revalidación |
| G-10 | Registro e idempotencia con fallo honesto | IG10-01 reformulada; cuatro escenarios A–D; `db_txid` para la guarda; sin afirmar filas en transacciones abortadas |

**No declaro cerradas G-1, G-5 ni G-10 oficialmente:** están resueltas en diseño técnico consolidado y listo para tu aceptación formal. No quedan contradicciones detectadas en el contraste documental ni decisiones estructurales sin comportamiento por defecto; las precisiones DG-17 a DG-19 no bloquean.

## B. Decisiones incorporadas

| ID | Estado | Dónde se incorpora |
|---|---|---|
| DG-01 | APROBADA conceptualmente, sujeta a completar tipos, claves, restricciones y justificación | Completada en las secciones 3 a 5 y 9 (tipos de columnas, claves, únicos, CHECK, índices y justificación por elemento). Falta tu aceptación de la especificación |
| DG-02 | APROBADA | 3.4 y 3.13; reglas IG1-03 a IG1-07 |
| DG-03 | APROBADA | 3.1 y 3.6; IG1-15 y IG1-16 |
| DG-04 | APROBADA | 4.4 y 4.4.1; IG5-05 y IG5-06. El caso de versiones intermedias de la maestra no está en DG-04 (DG-17) |
| DG-05 | APROBADA | 4.1, 4.2; IG5-01 a IG5-03. Las precisiones de C3 a C5 (6.2) son consecuencia de DG-05; la v9 que contiene G-7 sigue sin aceptarse |
| DG-06 | APROBADA | 4.5; IG5-15 |
| DG-07 | APROBADA | `piece_reviewer_assignments`; 4.4. Cierra solo la asignación de revisor: **G-9 completo sigue abierto** |
| DG-08 | APROBADA | 5.6; IG10-15 |
| DG-09 | DIFERIDA; no se habilita borrado desde la aplicación y no se inventa política | 5.7 y IG10-18; se eliminó el plazo de la v1 |
| DG-10 | APROBADA | 5.3; IG10-01 y IG10-03 |
| DG-11 | APROBADA | 5.6; IG10-16 |
| DG-12 | DIFERIDA a la subfase 6.6; no es requisito del cierre del diseño actual | 5.7; fuera del modelo |
| DG-13 | APROBADA | C8 en 6.2; categorías inconsistencia_versiones e imposibilidad_verificar |
| DG-14 | APROBADA | 3.13; IG1-13 y IG1-23 |
| DG-15 | APROBADA | 6.3 y 7.12; IP-01 a IP-04; dependencia DEP-RET-01 para el retiro externo |
| DG-16 | DIFERIDA hasta resolver T-03; 30 y 10 caracteres siguen como **propuestas pendientes, no aprobadas** | Se marcan como propuestas en las tablas y reglas; ningún CHECK de longitud es decisión |

Ninguna decisión autoriza SQL, migraciones ni implementación. G-9 completo sigue abierto: DG-07 solo resuelve la asignación del revisor.

## C. Correcciones solicitadas

### C.1 G-10 (IG10-01, IG10-11 y sección 5.8)

La contradicción era real: la v1 afirmaba una fila por solicitud y a la vez que un intento fallido «quedaba» en la plataforma. PostgreSQL no confirma filas dentro de una transacción abortada. Formulación final de IG10-01: *«Toda solicitud autenticada, de un miembro de la organización y aceptada por el mecanismo de publicación termina en una de dos formas excluyentes: (a) exactamente una fila confirmada de `publication_attempts`, permitida o bloqueada, o (b) la transacción falla, sin publicación y sin fila confirmada»*. Es tu fórmula con dos precisiones: que en el segundo caso tampoco hay fila, y que lo no autenticado o sin membresía queda fuera porque no es un intento de negocio.

| Escenario | Resultado |
|---|---|
| A. Procesada | Exactamente una fila; la clave de idempotencia evita duplicados |
| B. Error técnico capturado | Fila bloqueada con `error_tecnico` y código controlado; no publica. Tiempos de espera y pérdidas de conexión abortan todo y caen en C |
| C. Falla el registro | La transacción falla; no hay Publicado ni fila confirmada; la evidencia de plataforma, si existe y no verificada, **no** se presenta como fila |
| D. Sin autenticación o membresía | Evento de seguridad de plataforma, no intento de negocio; sin actor inventado (`actor_id` NOT NULL con FK) |

`idempotency_key` identifica una acción del usuario; `correlation_id` identifica la solicitud y no es clave. Con la misma clave y una fila existente se devuelve el resultado almacenado; sin fila se evalúa desde cero; tras corregir un bloqueo se usa una clave nueva.

### C.2 G-5 (integridad de asignaciones y evaluadores)

Cada garantía indica su mecanismo (4.4.1): correspondencia de asignación y evaluador por FK compuesta con UNIQUE y una constante; vigencia, permiso e independencia por función y trigger bajo bloqueo; historia por tabla de solo inserción. Ninguna FK aislada se presenta como garantía de elegibilidad. Orden de bloqueo único: maestra, adaptaciones por `id`, membresía del actor; matriz de revalidación para reasignación, evaluación, cambio de la maestra y publicación (4.10).

### C.3 G-1 (canal, formato y relación)

v3.3 define `channel_rules` sin formatos y sin catálogo real de canales (pendiente). Se propone `allowed_formats` y la FK de canal en la Fase 5, sin inventar valores. `is_master` se renombra a `is_adaptation`.

### C.4 Seguridad (rutas de publicación)

Matriz de acceso por rol (8.7) y demostración documental de diez garantías con su mecanismo, regla, prueba y dependencia de infraestructura (8.8): dos propietarios de funciones (estado y registros), UPDATE de `status` revocado, EXECUTE solo para `authenticated`, `auth.uid()` dentro de la función. Lo que depende de Supabase real queda marcado como no verificado.

### C.5 DG-15 (piezas publicadas)

T-02 intacta. Una pieza Publicada no se modifica; una nueva versión comercial es una pieza nueva y la anterior se archiva por #13. Se distingue el estado interno de la disponibilidad externa: archivar no retira contenido externo. **DEP-RET-01:** no existe procedimiento operativo para el retiro externo; queda como dependencia, sin transición inventada (6.3 y 7.12).

## D. Modelo propuesto frente a las 27 tablas

| Concepto | Detalle |
|---|---|
| Tablas nuevas (4) | `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts` |
| Tablas con columnas o restricciones nuevas | creative_pieces, copy_versions, creative_assets, approvals y channel_rules (al crearse en la Fase 5) |
| Función ampliada | transition_piece_status |
| Sin cambio | 22 de las 27, las 17 claves y las 13 transiciones de T-02 |
| Total | 31 tablas propuestas sujetas a aprobación; las 27 permanecen como línea base histórica |

## E. Validación

| Concepto | Resultado |
|---|---|
| Reglas de integridad | 84 (eran 59; +25) |
| Pruebas | 73 (eran 52; +21: las 15 solicitadas y 6 adicionales) |
| Diseño / Ejecutable futura / Infraestructura real | 4 / 53 / 16 |
| Cobertura | Toda regla tiene al menos una prueba; las 27 pruebas mínimas del primer encargo siguen cubiertas; las 15 nuevas cubiertas |
| Verificación por script | FK con aridad y destino que coincide con una clave única o primaria declarada; categorías, condiciones y reglas; 13 diagramas |
| Pruebas ejecutadas | Ninguna: todo es verificación documental |

## F. Decisiones y pendientes

**Pendientes que se mantienen:** DG-09 (retención, sin plazo), DG-12 (hash, a 6.6), DG-16 (umbrales 30 y 10 pendientes de T-03), RP-01, P-01 a P-05, P-10, OD-13, PO-05 y la aceptación de la Adenda v9; G-9 completo.

**Precisiones nuevas con valor por defecto:**

| ID | Precisión | Recomendación | Efecto de no decidir |
|---|---|---|---|
| DG-17 | Independencia respecto de los contribuyentes de las versiones **intermedias** de la maestra entre V-D y V-B | Incluirlos (más estricto y coherente con «no evaluar su propia modificación») | Si no decides, el diseño aplica DG-04 literal (solo V-A y V-B). No bloquea |
| DG-18 | Columna opcional `replaces_piece_id` para ligar la pieza nueva con la anterior (DG-15) | Aprobarla | Sin ella el reemplazo solo se reconstruye por campaña o texto; el diseño funciona igual. No bloquea |
| DG-19 | Representar los formatos permitidos como columna `allowed_formats` de channel_rules (no como quinta tabla) | Columna | Los valores reales de canales y formatos siguen pendientes; el diseño no inventa ningún catálogo. No bloquea |

## G. Limitaciones reales

| ID | Limitación |
|---|---|
| RR-01 | La FK declarativa de un solo nivel con columnas generadas no está verificada |
| RR-02 | Todo es diseño: ninguna restricción, trigger ni función se ejecutó |
| RR-03 | Si falla la inserción del registro, no hay fila confirmada del intento; la evidencia de plataforma, si existe, no es un registro confirmado y su conservación no está verificada |
| RR-04 | Un superusuario o propietario de la base puede alterar cualquier tabla |
| RR-05 | Los bytes de un arte no son transaccionales con la base (C8) |
| RR-06 | No hay análisis semántico: el juicio de impacto es humano |
| RR-07 | Equipos pequeños pueden no tener un revisor elegible |
| RR-08 | El costo de verificar C1 a C9 en cada publicación no está medido |
| RR-09 | La suficiencia de activity_logs sigue sin demostrarse (DA-01) |
| RR-10 | Retiro de contenido externo sin procedimiento (DEP-RET-01) |
| RR-11 | Los privilegios por defecto de Supabase pueden conceder escritura amplia |
| RR-12 | Una pieza escrita por IA cuenta como autoría de quien la pidió (T-04) |
| RR-13 | Los dos propietarios de funciones y la revocación de EXECUTE no se han comprobado en Supabase |
| RR-14 | auth.uid() depende de la sesión de la solicitud: quien tenga credenciales de administración de la base puede fijar otra identidad |
| RR-15 | Los tiempos de espera, cancelaciones y pérdidas de conexión abortan toda la transacción y no dejan fila |
| RR-16 | La conservación y el contenido de los registros de la plataforma no están verificados |
| RR-17 | La columna que distingue aprobaciones de rechazos en approvals no está fijada en v3.3 |
| RR-18 | Los umbrales de 30 y 10 caracteres son propuestas pendientes de T-03 |

## H. Archivos

| Tipo | Archivos |
|---|---|
| Actualizados | `ESPECIFICACION_TECNICA_G1_G5_G10.md` (v2), `INFORME_CIERRE_G1_G5_G10.md`, `ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md`, `REGISTRO_HISTORICO_VERSIONES.md` (entrada nueva) |
| Conservados como histórico | las tres versiones v1 con sufijo `_v1_historica` o `_v1_historico` |
| No modificados | v3.3, Adenda v9, control, matriz, trazabilidad, auditoría, matriz de notificaciones y las demás versiones históricas |

## I. Integridad

SHA-256 de v3.3: `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` (igual).

Se compararon los archivos .md de la línea base previa (78, incluidas las copias v1). Sin diferencias no previstas: sí. Modificados previstos: `ESPECIFICACION_TECNICA_G1_G5_G10.md`, `REGISTRO_HISTORICO_VERSIONES.md`, `ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md`. Las tres copias v1 son idénticas a las versiones entregadas antes.

Las 17 claves, las 27 tablas históricas, las 13 transiciones de T-02 y las 76 subfases no cambian; no existe subfase 77.

## J. Roadmap

En `ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md`: trazabilidad actualizada, DEP-RET-01 y el roadmap de 76 subfases con los estados de v9 sin cambio.

## K. Declaración

G-1, G-5 y G-10 están resueltas en **diseño técnico consolidado**, con tus decisiones incorporadas, coherente entre reglas, tablas, funciones y pruebas, y **lista para aceptación formal**. No están aceptadas ni validadas técnicamente y no se declaran cerradas oficialmente. Fase 0 no se declara cerrada y Fase 1 no se inicia.

## L. Límites

No se ejecutó SQL, migraciones, código, Edge Functions, RLS real, infraestructura, Supabase, repositorios, Git ni despliegues.
