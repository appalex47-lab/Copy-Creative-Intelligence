# Índice de evidencias de Fase 0 (revisión complementaria)
Verificar: `sha256sum -c MANIFEST.sha256` en la raíz del expediente (`expediente_fase0/`). Convención de referencias: dentro de `entregables_formales/` las rutas son relativas a esta carpeta; `../NN_*.md` son los documentos base de la entrega previa (00–14, **sin alterar**).
## Correspondencia de nombres (base → formal)
| Base (raíz) | Formal (`entregables_formales/`) |
|---|---|
| `01_INFORME_AUDITORIA.md` + `anexos/` | `01_INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md` |
| `02_INVENTARIO_FUNCIONALIDADES.md` | `02_INVENTARIO_FUNCIONAL_CCI.md` |
| `04_MATRIZ_REQUISITOS.md` | `03_MATRIZ_REQUISITOS_CCI.md` |
| `05_ARQUITECTURA_BROWSER_ONLY.md` | `04_ARQUITECTURA_BROWSER_ONLY.md` |
| `06_MODELO_DE_DOMINIO.md` | `05_MODELO_DOMINIO_CCI.md` |
| (nuevo) | `06_MODELO_DATOS_CCI.md` (**propuesta histórica; no es un esquema de datos aprobado**; ver su clasificación) |
| `07_DISENO_PERSISTENCIA.md` | `07_DISENO_PERSISTENCIA_INDEXEDDB.md` |
| `08_RESPALDO_Y_RECUPERACION.md` | `08_RESPALDO_IMPORTACION_RECUPERACION.md` |
| `09_ANALISIS_IA.md` | `09_ESTRATEGIA_IA_CCI.md` |
| (nuevo) | `10_DEFINICION_MVP_CCI.md` (con marcas [S]/[D]/[P]) |
| `11_ROADMAP_Y_CRITERIOS_FASES_1_A_5.md` | `11_ROADMAP_FASES_0_A_5.md` (reescrito, 12 puntos) y `12_CRITERIOS_ACEPTACION_FASES.md` |
| `10_REGISTRO_DECISIONES.md` | `13_REGISTRO_DECISIONES_PROPIETARIO.md` |
| (nuevo) | `14_MATRIZ_RIESGOS_CCI.md` |
| `12_ESTRATEGIA_DE_PRUEBAS.md` | `15_PLAN_CALIDAD_Y_PRUEBAS.md` |
| (nuevo) | `16_INDICE_EVIDENCIAS_FASE0.md` (este) |
| (nuevo) | `README_PROPUESTA_VIGENTE.md` (17) |
Sin equivalente formal (se quedan en la raíz): `00` dictamen, `03` conciliación, `13` verificación, `14` estado Git. Añadidos en esta revisión: `MATRIZ_DECISIONES_PROPIETARIO.md`, `APROBACIONES_FASE0.md`, `../INFORME_REVISION_COMPLEMENTARIA.md`.
## Evidencias
| Evidencia | Ubicación | Respalda |
|---|---|---|
| Informe browser-only original (íntegro) | `../anexos/` | auditoría previa |
| Verificación ejecutada y logs | `../13_VERIFICACION_EJECUTADA.md`, `../logs/` | 162/162 unit; E2E 29/29 ×3; build; guarda de producción (ejecución del turno anterior; no repetida hoy) |
| Estado Git | `../14_ESTADO_GIT_Y_OPERACIONES.md` + `../INFORME_REVISION_COMPLEMENTARIA.md` §Git | HEAD `ffb47bc`, árbol limpio (comprobado de nuevo en la revisión) |
| Conciliación documental | `../03_CONCILIACION_DOCUMENTAL.md` | K1–K20 |
**No hay evidencia** de ejecución del producto (no existe), `npm audit`, CI real ni otros navegadores.
## Añadidos en la segunda revisión (2026-11-22)
`CONCILIACION_D1_D9_VERIFICADA.md` (lectura de los registros originales; dos series de IDs; nueva decisión Q-7), `FICHA_P1.md` (P1 individual) y correcciones en `../03_CONCILIACION_DOCUMENTAL.md` §2, `13_REGISTRO_DECISIONES_PROPIETARIO.md`/`../10_REGISTRO_DECISIONES.md` (etiquetas DEC-/F11- y fila Q-7), `MATRIZ_DECISIONES_PROPIETARIO.md`, `../00`, `../01` e `INFORME_REVISION_COMPLEMENTARIA.md` §7. Todos son documentos míos; ningún registro histórico del repositorio se modificó.
## Añadidos tras la respuesta a P1 (2026-11-22)
`REGISTRO_DECISIONES_RESUELTAS.md` (P1 literal y consecuencias), `FICHA_P2.md` (siguiente decisión, sin respuesta) y el estado de P1 en los documentos que lo citan.
## Añadidos tras la respuesta a P2 (2026-11-22)
`ADR_PROPUESTO_REEMPLAZO_DEC_D2_D3_D4.md` (redactado, **no publicado**), `FICHA_P3.md` (sin respuesta) y el estado de P2 en los documentos que lo citan.
## Añadidos tras la respuesta a P3 y la ampliación de P2 (2026-11-22)
`INDICE_ANTECEDENTES_HISTORICOS.md`, `FICHA_P4.md` (sin respuesta); ADR propuesto ampliado a «Seguridad por diseño» (aún **no publicado**); correcciones en `05` y `07` (etiquetas en Fase 2).
## Añadidos tras las respuestas parciales a P4 (2026-11-22)
`LISTA_ORIGINAL_18_ENTIDADES.md` (listas A y B leídas de los adjuntos, con líneas), `FICHA_Q7.md` (sin respuesta al elaborarse; **vigente: Q-7 resuelta → (a)**), `CONVENCIONES_P4_5_CONDICIONES.md` (propuestas para las condiciones de P4.5); modelo (`05`, `06`, `07`) actualizado: ReglaDeMarca/ReglaComercial separadas, Etiqueta aprobada, Colección fuera del modelo, `revision` no obligatoria.
- DECISIONES_P4_PENDIENTES.md — decisiones de P4 aún abiertas (2026-11-22; vigente: P4.D/Q-7 resuelta, D4/D6/D7/D8 resueltas)
- FICHA_P4A_01_CAMPANA.md — P4.A entidad 1 (**vigente: RESUELTA, definición mínima aprobada**; «pendiente» = estado al elaborarse la ficha)
- FICHA_P4A_02_BRIEF.md — P4.A entidad 2 (**vigente: RESUELTA, definición mínima aprobada**; «pendiente» = estado al elaborarse la ficha)
- FICHA_P4A_03_PRODUCTO.md — P4.A entidad 3 (**vigente: RESUELTA, definición mínima aprobada**; «pendiente» = estado al elaborarse la ficha)
- FICHA_P4A_04_OFERTA.md — P4.A entidad 4 (**vigente: RESUELTA, definición mínima aprobada**; «pendiente» = estado al elaborarse la ficha)
- FICHA_P4A_05_COPY.md — P4.A entidad 5 (**vigente: RESUELTA, definición mínima aprobada**; «pendiente» = estado al elaborarse la ficha)
- FICHA_P4A_06_COPYVARIANT.md — P4.A entidad 6 (**vigente: RESUELTA, definición mínima aprobada**; «pendiente» = estado al elaborarse la ficha)
- FICHA_P4A_07_PIEZA_CREATIVA.md — P4.A entidad 7 (**vigente: RESUELTA, definición mínima aprobada**; «pendiente» = estado al elaborarse la ficha)
- FICHA_P4A_08_AUDITORIA_CREATIVA.md — P4.A entidad 8 (**vigente: RESUELTA, definición mínima aprobada**; «pendiente» = estado al elaborarse la ficha)
- FICHA_P4A_09_HALLAZGO.md — P4.A entidad 9 (**vigente: SUSPENDIDA, sin aprobar**)
- DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md / MATRIZ_CONSOLIDADA_18_ENTIDADES.md — revisión integral previa a P4.A 9–18
- D1_ANALISIS_CONTENIDO.md — análisis D-1 (**estado histórico al elaborarse:** pendiente de decisión; **estado vigente: D-1 RESUELTA** conforme a las decisiones del propietario; autoritativo: `REGISTRO_DECISIONES_RESUELTAS.md`.)
- D2_VARIANTE_FRENTE_A_VERSION.md — análisis D-2 (**estado histórico al elaborarse:** pendiente de decisión; **estado vigente: D-2 RESUELTA** conforme a las decisiones del propietario; autoritativo: `REGISTRO_DECISIONES_RESUELTAS.md`.)
- D3_FAMILIAS_DE_REGLAS.md — análisis D-3 (**estado histórico al elaborarse:** pendiente de decisión; **estado vigente: D-3 RESUELTA** conforme a las decisiones del propietario; autoritativo: `REGISTRO_DECISIONES_RESUELTAS.md`.)
- CATALOGO_DEPENDENCIAS_D4_D8.md — catálogo recuperado de D-4 a D-8
- D5_APROBACION.md — análisis D-5 (**estado histórico al elaborarse:** pendiente de decisión; **estado vigente: D-5 RESUELTA** conforme a las decisiones del propietario; autoritativo: `REGISTRO_DECISIONES_RESUELTAS.md`. D5.a–d expresamente fuera del alcance vigente.)
- entregables_formales/PAQUETE_DECISION_D1_D8.md — paquete único de decisión D-1 a D-8 (2026-11-22)
- entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md — paquete vigente D-4/D-6/D-7/D-8 (2026-11-22 12:35); sustituye a PAQUETE_DECISION_D1_D8.md
- entregables_formales/INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md y MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt (protocolo permanente)
- entregables_formales/INFORME_CIERRE_2026-11-22_REGLA_PERMANENTE_12_43.md
- entregables_formales/CONTROL_DE_CAMBIOS_CORRECCION_2026-11-22.md e INFORME_CIERRE_2026-11-22_CORRECCION_DOCUMENTAL.md — corrección documental posterior a la publicación (2026-11-22)
- entregables_formales/RONDA_UNICA_D4_D6_D7_D8_MATRIZ_CONSOLIDADA.md — matriz consolidada de la ronda única (2026-11-22)

> **NOTA DE ACTUALIZACIÓN 2026-11-22 (registro D4/D6/D7/D8).** El propietario confirmó las 11 decisiones D4.a–d, D6.a–c, D7.a–c y D8; el registro autoritativo es `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` (sección «D-4, D-6, D-7 y D-8 — RESUELTAS»). Nuevos: `CONTROL_DE_CAMBIOS_REGISTRO_D4_D6_D7_D8_2026-11-22.md` e `INFORME_CIERRE_2026-11-22_REGISTRO_D4_D6_D7_D8.md`. Este documento se conserva como antecedente; si alguna celda o texto lo contradice, prevalece el registro. Sin inferir aprobaciones de entidades, atributos, relaciones, cardinalidades, fases ni mecanismos técnicos.

## ESTADO VIGENTE (regularización 2026-11-22)
**P4.A (conteo formal vigente): 9/18 aprobadas (50 %); 9/18 pendientes (50 %).** Aprobadas con definición mínima: entidades 1–8 y entidad 13 (Adaptación de canal), esta última por D4.c=A y **exclusivamente su definición mínima** (sin atributos, relaciones, cardinalidades, estructura interna, persistencia, versionado, mecanismos de generación o adaptación, reglas de auditoría ni fase de implementación). Entidad 9 (Hallazgo): suspendida, sin aprobar. Entidades 10–12 y 14–18: sin presentar o sin aprobar. Cambio 2026-11-22: de 8/18 a 9/18, fundamento D4.c=A.
Las entradas de las fichas P4.A de arriba indican ahora el estado vigente (fichas 01–08 aprobadas; 09 suspendida); el «pendiente» original se conserva dentro de cada ficha como antecedente. Autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Matriz de la ronda D4/D6/D7/D8: antecedente respondido. Nuevo: `CONTROL_DE_CAMBIOS_REGULARIZACION_P4A_9_18_2026-11-22.md`.

**Auditoría integral 2026-11-22:** índice maestro y documentos de auditoría en `auditoria_integral/` (`01_INDICE_MAESTRO_FASE0.md` y siguientes). Esta lista conserva la redacción histórica; el estado vigente es el del índice maestro y el registro.

> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; el texto original no se altera):** el «P4.A 9/18» de este índice es antecedente; vigente: 18/18. Fuente y texto literal: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)». Aprobaciones 0.1–0.7, aceptación de Fase 0 y autorización de Fase 1 siguen pendientes.

> **Nota fechada 2026-11-22 (regularización posterior a la ratificación y preparación de aprobaciones; no es decisión nueva):** el expediente incorpora `entregables_formales/CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md`, `entregables_formales/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md`, `entregables_formales/CONTROL_DE_CAMBIOS_PREPARACION_APROBACIONES_2026-11-22.md` y `auditoria_integral/14_INFORME_FINAL_REGULARIZACION_Y_PREPARACION_APROBACIONES.md`. Estado vigente: aprobaciones 0.1–0.7 = 0/7 emitidas (pendientes); Fase 0 no aceptada; Fase 1 no autorizada; 20/30 decisiones resueltas y 10/30 aplazadas; P4.A 18/18 (solo existencia y definición mínima).

> **Nota fechada 2026-11-22 (segunda regularización; no es decisión nueva):** R-1 corregida: incluye **seis** cuestiones residuales (la ubicación conceptual de la familia de reglas de copy, de D-3, y las cinco de D-5: auditoría o validaciones previas; modificación de un contenido aprobado; relación con las versiones; identidad exacta del contenido aprobado; relación con los estados del flujo); una respuesta afirmativa se registra como aplazamiento, nunca como resolución. D5.a–d siguen fuera del alcance vigente y no se reabren. `06_MODELO_DATOS_CCI.md` es una propuesta histórica, no un esquema de datos aprobado. Estado: aprobaciones 0.1–0.7 = 0/7 emitidas; Fase 0 no aceptada; Fase 1 no autorizada.

> **Nota fechada 2026-11-22 20:14 (respuesta del propietario; no es decisión nueva de este documento):** el propietario emitió las aprobaciones 0.1–0.7 (7/7; la 0.5 solo en cuanto a principios, con P8 sin resolver y sin ninguna integración aprobada) y respondió «sí» a R-1 (aplazamiento aceptado de las seis cuestiones residuales, no resolución). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «0/7», «PENDIENTES» o «R-1 pendiente» describen el estado previo y quedan superadas en ese punto; el resto del texto no se altera. **La aceptación formal de Fase 0 y la autorización independiente de Fase 1 siguen PENDIENTES.** Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.
