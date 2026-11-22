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
| (nuevo) | `06_MODELO_DATOS_CCI.md` |
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
`LISTA_ORIGINAL_18_ENTIDADES.md` (listas A y B leídas de los adjuntos, con líneas), `FICHA_Q7.md` (sin respuesta), `CONVENCIONES_P4_5_CONDICIONES.md` (propuestas para las condiciones de P4.5); modelo (`05`, `06`, `07`) actualizado: ReglaDeMarca/ReglaComercial separadas, Etiqueta aprobada, Colección fuera del modelo, `revision` no obligatoria.
- DECISIONES_P4_PENDIENTES.md — decisiones de P4 aún abiertas (2026-11-22)
- FICHA_P4A_01_CAMPANA.md — P4.A entidad 1 (pendiente)
- FICHA_P4A_02_BRIEF.md — P4.A entidad 2 (pendiente)
- FICHA_P4A_03_PRODUCTO.md — P4.A entidad 3 (pendiente)
- FICHA_P4A_04_OFERTA.md — P4.A entidad 4 (pendiente)
- FICHA_P4A_05_COPY.md — P4.A entidad 5 (pendiente)
- FICHA_P4A_06_COPYVARIANT.md — P4.A entidad 6 (pendiente)
- FICHA_P4A_07_PIEZA_CREATIVA.md — P4.A entidad 7 (pendiente)
- FICHA_P4A_08_AUDITORIA_CREATIVA.md — P4.A entidad 8 (pendiente)
- FICHA_P4A_09_HALLAZGO.md — P4.A entidad 9 (pendiente)
- DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md / MATRIZ_CONSOLIDADA_18_ENTIDADES.md — revisión integral previa a P4.A 9–18
- D1_ANALISIS_CONTENIDO.md — análisis D-1 (pendiente de decisión)
- D2_VARIANTE_FRENTE_A_VERSION.md — análisis D-2 (pendiente de decisión)
- D3_FAMILIAS_DE_REGLAS.md — análisis D-3 (pendiente de decisión)
- CATALOGO_DEPENDENCIAS_D4_D8.md — catálogo recuperado de D-4 a D-8
- D5_APROBACION.md — análisis D-5 (pendiente de decisión)
- entregables_formales/PAQUETE_DECISION_D1_D8.md — paquete único de decisión D-1 a D-8 (2026-11-22)
- entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md — paquete vigente D-4/D-6/D-7/D-8 (2026-11-22 12:35); sustituye a PAQUETE_DECISION_D1_D8.md
- entregables_formales/INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md y MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt (protocolo permanente)
- entregables_formales/INFORME_CIERRE_2026-11-22_REGLA_PERMANENTE_12_43.md
