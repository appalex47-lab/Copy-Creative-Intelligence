---
name: auditoria_final_g1_g5_g10
description: Auditoría final de las siete correcciones de G-1, G-5 y G-10 (hallazgo, causa raíz, corrección, reglas, pruebas, verificación, riesgos residuales)
---

# AUDITORÍA FINAL — G-1, G-5 Y G-10 (revisión v3)

Documental. Las pruebas son diseños, no ejecuciones.

## 1. Hallazgos, causa raíz y corrección

| Corrección | Hallazgo | Causa raíz | Corrección (resumen) | Referencia spec | Reglas | Pruebas |
|---|---|---|---|---|---|---|
| 1. G-5 aprobación positiva | La v3.3 no tiene un campo que distinga una aprobación positiva de un rechazo o una solicitud de cambio, y C2/C3 no decían qué leían. | Modelo sin campo de decisión; C2/C3 ambiguas | Extensión mínima DG-20: `approvals.decision` NOT NULL con CHECK = 'aprobada'. Rechazo, solicitud de cambio y registro de revisión son transiciones T-02 con come… | 4.13, 3.4, 6.2 (C2/C3), 8.9 | IG5-26, IG5-27, IG5-28, IG5-29, IG5-30 | T-74 a T-84 |
| 2. G-10 db_txid | `db_txid` no tenía mecanismo ni tipo definidos. | Mecanismo de transacción no definido | Columna bigint NOT NULL fijada por trigger BEFORE INSERT con `(pg_current_xact_id())::text::bigint`, junto con `attempted_at = transaction_timestamp()`. Descart… | 5.10, 5.11, 4.x trigger, 7.14 | IG10-01, IG10-19, IG10-20, IG10-22, IG10-23, IG10-24, IG10-25, IG10-26, IG10-27, IG10-29, IG10-30, IS-01, IS-02, IS-03, IS-04, IS-05, IS-08, IS-09 | T-85 a T-104 |
| 3. G-1 canales y formatos | El ciclo de vida de canales y formatos dejaba piezas sin catálogo y una lista de formatos sin normalizar. | Catálogo creado después del primer uso | Se evaluaron tres alternativas y se eligió `channel_rules` (fuente de verdad del canal) más `channel_formats`, creados en 1.8 antes de la primera pieza; FK comp… | 3.14, 7.13, 8.9; roadmap 1.8 y 5.1 | IG1-25, IG1-26, IG1-27, IG1-28, IG1-29, IG1-30, IG1-31, IG1-32, IG1-33 | T-105 a T-119 |
| 4. DG-16 longitudes | Los umbrales de 30 y 10 caracteres estaban como CHECK obligatorios aunque T-03 no los decide. | Umbrales propuestos tratados como restricción | Todos los CHECK de longitud mínima pasan a no vacío (>=1). 30 y 10 quedan como propuestas pendientes (IP-05).… | 3.x, 4.2, 12.3 | IG5-09, IP-05 | T-120 a T-124 |
| 5. DG-17 independencia | La independencia no consideraba a los contribuyentes de versiones intermedias de la maestra. | Intervalo de versiones omitido en el conjunto | E = Ctr(V-A) ∪ Inh(V-A) ∪ ⋃ Ctr(v) para v en el intervalo [V-D, V-B] inclusive; revalidación bajo bloqueo; sin elegible, bloqueo operativo sin autoasignación.… | 4.4.2, 8.9 | IG5-06, IG5-24, IG5-25, IG5-31, IG5-32, IG5-33, IG5-34, IG5-35 | T-125 a T-135 |
| 6. G-5 cadena de evaluaciones | La sustitución de evaluaciones no estaba atada al par exacto ni protegida contra ramas, ciclos y duplicados. | Identidad del par incompleta | Identidad de par de 9 columnas (con arte normalizado), FK compuesta de sustitución con 8 columnas de par, raíz única por par, único sucesor, CHECK supersedes<>i… | 4.14, 7.15 | IG5-13, IG5-36, IG5-37, IG5-38, IG5-39 | T-136 a T-145 |
| 7. correlation_id | `correlation_id` mezclaba identificación, idempotencia y posible evidencia. | Un solo identificador con tres funciones | Siempre generado por el servidor; `client_correlation_id` opcional, validado y descartable; nunca evidencia ni autorización; independiente de `idempotency_key`;… | 5.12, 5.5 | IG10-28, IG10-29, IS-05 | T-146 a T-152 |

## 2. Resultados de verificación

| Verificación | Resultado | Detalle |
|---|---|---|
| V01 | OK |  |
| V02 | OK | [][] |
| V03 | OK | 152 filas vs 152 |
| V04 | OK | [] |
| V05 | OK | [] |
| V06 | OK | [][] |
| V07 | OK | [] |
| V08 | OK | [] |
| V09 | OK | [] |
| V10 | OK |  |
| V11 | OK | [] |
| V12 | OK | [] |
| V13 | OK | {} |
| V14 | OK | [] |
| V15 | OK | [] |
| V16 | OK |  |
| V17 | OK | [] |
| V18 | OK | [] |
| V19 | OK | b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da |
| V20 | OK | [][] |
| V21 | OK | 84 filas, 76 distintas |
| V22 | OK |  |

Mermaid: 17 de 17 con sintaxis válida (parseo; no se verificó el renderizado visual).

## 3. Defectos hallados y corregidos durante la revisión

V14 y V15 del verificador detectaron incoherencias internas del documento v3 durante su construcción; se corrigieron antes de publicar. Nota de nomenclatura: los identificadores T-01..T-11 de las pruebas de esta especificación coinciden en forma con ítems T-01..T-11 de v3.3; no son lo mismo (nota en la sección 11).

## 4. Riesgos residuales

| ID | Riesgo |
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
| RR-17 | approvals.decision es una ampliación propuesta (DG-20): v3.3 no distingue aprobación de rechazo en la fila |
| RR-18 | Los umbrales de 30 y 10 caracteres son propuestas pendientes de T-03 |
| RR-19 | La versión de PostgreSQL del proyecto de Supabase no está verificada; pg_current_xact_id requiere la 13 o posterior |
| RR-20 | El comportamiento real de los bloqueos y del orden de bloqueo no se probó |
| RR-21 | T-04 (definición de contribuyentes) está pendiente en v3.3; DG-17 y la independencia dependen de ella |
| RR-22 | Los valores reales de canales y formatos no existen: sin catálogo cargado no se crean piezas |
| RR-23 | Tras restaurar una copia lógica, un db_txid guardado podría repetirse |
| RR-24 | El orden de versión de la maestra (columna de copy_versions) no está fijado en v3.3 |
| RR-25 | El valor de pg_current_xact_id dentro de un savepoint o bloque EXCEPTION no está verificado |
| RR-26 | La FK no distingue «sin arte» de «otro arte» con columnas anulables |

## 5. Estado por brecha

| Brecha | Estado |
|---|---|
| G-1 | Resuelta documentalmente; lista para aceptación formal |
| G-5 | Resuelta documentalmente; lista para aceptación formal |
| G-10 | Resuelta documentalmente; lista para aceptación formal |

Ninguna está aceptada ni validada técnicamente.
