# Informe de auditoría integral del expediente (2026-11-22)
**Alcance total:** 93 archivos de `evidence/cci-fase0/` (estado en HEAD `1bb831a`) + 59 archivos de `docs/fase0/` (conciliados en `11_INDICE_CONCILIACION_DOCS_FASE0.md`) = 152 archivos; los 11 documentos de esta auditoría se añaden después. Verificado por API: HEAD de la rama = `1bb831a32219898616e7a7ad8d12092aac16f253`; `main` = `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` (sin cambios); `docs/fase0` idéntico a `main`.

## 1. Clasificación de los 93 archivos del expediente por vigencia
| Clase | Archivos |
|---|---|
| Antecedente (análisis resuelto) | 4 |
| Antecedente (respondido) | 2 |
| Antecedente / propuesta | 7 |
| Evidencia técnica | 12 |
| Histórico | 2 |
| Histórico (copia previa) | 16 |
| Histórico (ficha resuelta/suspendida) | 14 |
| Informe/control (fechado) | 8 |
| Integridad | 3 |
| Propuesta | 1 |
| Propuesta (subordinada) | 14 |
| Propuesta vigente (no aprobada en bloque) | 1 |
| Superado | 1 |
| VIGENTE AUTORITATIVO | 1 |
| Vigente (derivado) | 6 |
| Vigente (subordinado) | 4 |
| Vigente (índice) | 3 |

Detalle archivo por archivo (ruta · clase · motivo):
| Ruta | Clase | Motivo |
|---|---|---|
| `00_DICTAMEN_Y_CIERRE_FASE0.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `00_INDICE_VIGENTES_E_HISTORICOS.md` | Vigente (índice) | Índice/guía; refleja el registro |
| `01_INFORME_AUDITORIA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `02_INVENTARIO_FUNCIONALIDADES.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `03_CONCILIACION_DOCUMENTAL.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `04_MATRIZ_REQUISITOS.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `05_ARQUITECTURA_BROWSER_ONLY.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `06_MODELO_DE_DOMINIO.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `07_DISENO_PERSISTENCIA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `08_RESPALDO_Y_RECUPERACION.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `09_ANALISIS_IA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `10_REGISTRO_DECISIONES.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `11_ROADMAP_Y_CRITERIOS_FASES_1_A_5.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `12_ESTRATEGIA_DE_PRUEBAS.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `13_VERIFICACION_EJECUTADA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `14_ESTADO_GIT_Y_OPERACIONES.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `INFORME_REVISION_COMPLEMENTARIA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro |
| `INVENTARIO_PUBLICADO.sha256` | Integridad | Manifiesto/inventario (regenerado al publicar) |
| `MANIFEST.sha256` | Integridad | Manifiesto/inventario (regenerado al publicar) |
| `README_ENTREGA.md` | Vigente (índice) | Índice/guía; refleja el registro |
| `anexos/INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md` | Histórico | Anexo probatorio del informe de auditoría browser-only; fecha anterior al registro de decisiones |
| `anexos/MANIFEST_informe_browser_only.sha256` | Histórico | Anexo probatorio del informe de auditoría browser-only; fecha anterior al registro de decisiones |
| `auditoria_integral/01_INDICE_MAESTRO_FASE0.md` | Vigente (derivado) | Documento de la auditoría integral 2026-11-22; subordinado al registro |
| `auditoria_integral/02_MATRIZ_MAESTRA_DECISIONES.md` | Vigente (derivado) | Documento de la auditoría integral 2026-11-22; subordinado al registro |
| `auditoria_integral/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md` | Vigente (derivado) | Documento de la auditoría integral 2026-11-22; subordinado al registro |
| `auditoria_integral/04_MATRIZ_MAESTRA_DEPENDENCIAS.md` | Vigente (derivado) | Documento de la auditoría integral 2026-11-22; subordinado al registro |
| `auditoria_integral/09_PAQUETE_CONSOLIDADO_DECISIONES_PENDIENTES.md` | Vigente (derivado) | Documento de la auditoría integral 2026-11-22; subordinado al registro |
| `auditoria_integral/11_INDICE_CONCILIACION_DOCS_FASE0.md` | Vigente (derivado) | Documento de la auditoría integral 2026-11-22; subordinado al registro |
| `entregables_formales/01_INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/02_INVENTARIO_FUNCIONAL_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/03_MATRIZ_REQUISITOS_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/04_ARQUITECTURA_BROWSER_ONLY.md` | Propuesta vigente (no aprobada en bloque) | Arquitectura browser-only vigente por decisión del propietario; aprobación 0.2 pendiente |
| `entregables_formales/05_MODELO_DOMINIO_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/06_MODELO_DATOS_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/07_DISENO_PERSISTENCIA_INDEXEDDB.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/08_RESPALDO_IMPORTACION_RECUPERACION.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/09_ESTRATEGIA_IA_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/10_DEFINICION_MVP_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/11_ROADMAP_FASES_0_A_5.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/12_CRITERIOS_ACEPTACION_FASES.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/13_REGISTRO_DECISIONES_PROPIETARIO.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/14_MATRIZ_RIESGOS_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/15_PLAN_CALIDAD_Y_PRUEBAS.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica |
| `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md` | Vigente (índice) | Índice/guía; refleja el registro |
| `entregables_formales/ADR_PROPUESTO_REEMPLAZO_DEC_D2_D3_D4.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro |
| `entregables_formales/APROBACIONES_FASE0.md` | Vigente (subordinado) | Estado vigente al inicio; texto anterior conservado como antecedente |
| `entregables_formales/CATALOGO_DEPENDENCIAS_D4_D8.md` | Vigente (subordinado) | Estado vigente al inicio; texto anterior conservado como antecedente |
| `entregables_formales/CONCILIACION_D1_D9_VERIFICADA.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro |
| `entregables_formales/CONTROL_DE_CAMBIOS_CORRECCION_2026-11-22.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado |
| `entregables_formales/CONTROL_DE_CAMBIOS_CORRECCION_INTEGRAL_P4A_9_18_2026-11-22.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado |
| `entregables_formales/CONTROL_DE_CAMBIOS_REGISTRO_D4_D6_D7_D8_2026-11-22.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado |
| `entregables_formales/CONTROL_DE_CAMBIOS_REGULARIZACION_P4A_9_18_2026-11-22.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado |
| `entregables_formales/CONVENCIONES_P4_5_CONDICIONES.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro |
| `entregables_formales/D1_ANALISIS_CONTENIDO.md` | Antecedente (análisis resuelto) | Análisis previo a la decisión; ver registro |
| `entregables_formales/D2_VARIANTE_FRENTE_A_VERSION.md` | Antecedente (análisis resuelto) | Análisis previo a la decisión; ver registro |
| `entregables_formales/D3_FAMILIAS_DE_REGLAS.md` | Antecedente (análisis resuelto) | Análisis previo a la decisión; ver registro |
| `entregables_formales/D5_APROBACION.md` | Antecedente (análisis resuelto) | Análisis previo a la decisión; ver registro |
| `entregables_formales/DECISIONES_P4_PENDIENTES.md` | Vigente (subordinado) | Estado vigente al inicio; texto anterior conservado como antecedente |
| `entregables_formales/DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro |
| `entregables_formales/FICHA_P1.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P2.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P3.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_01_CAMPANA.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_02_BRIEF.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_03_PRODUCTO.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_04_OFERTA.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_05_COPY.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_06_COPYVARIANT.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_07_PIEZA_CREATIVA.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_08_AUDITORIA_CREATIVA.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_P4A_09_HALLAZGO.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/FICHA_Q7.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro |
| `entregables_formales/INDICE_ANTECEDENTES_HISTORICOS.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro |
| `entregables_formales/INFORME_CIERRE_2026-11-22_CORRECCION_DOCUMENTAL.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado |
| `entregables_formales/INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado |
| `entregables_formales/INFORME_CIERRE_2026-11-22_REGISTRO_D4_D6_D7_D8.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado |
| `entregables_formales/INFORME_CIERRE_2026-11-22_REGLA_PERMANENTE_12_43.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado |
| `entregables_formales/LISTA_ORIGINAL_18_ENTIDADES.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro |
| `entregables_formales/MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` | Integridad | Manifiesto/inventario (regenerado al publicar) |
| `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` | Vigente (subordinado) | Estado vigente al inicio; texto anterior conservado como antecedente |
| `entregables_formales/MATRIZ_DECISIONES_PROPIETARIO.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro |
| `entregables_formales/PAQUETE_DECISION_D1_D8.md` | Superado | Sustituido por PAQUETE_DECISION_D4_D6_D7_D8 |
| `entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md` | Antecedente (respondido) | Instrumento ya respondido; no se usa para volver a preguntar |
| `entregables_formales/README_PROPUESTA_VIGENTE.md` | Propuesta | README propuesto; no sustituye el README del repositorio |
| `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` | VIGENTE AUTORITATIVO | Fuente de verdad de decisiones del propietario (nivel 2) |
| `entregables_formales/RONDA_UNICA_D4_D6_D7_D8_MATRIZ_CONSOLIDADA.md` | Antecedente (respondido) | Instrumento ya respondido; no se usa para volver a preguntar |
| `logs/build.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/build_production_esperado_FALLO.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/check_secrets.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/e2e_corrida1.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/e2e_corrida2.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/e2e_corrida3.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/format_check.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/lint.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/resumen_1.txt` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/test_run.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/typecheck.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |
| `logs/verificaciones_documentales_2026-11-22_correccion.txt` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos |

## 2. Método (qué se hizo realmente)
- **Procesamiento automático del 100 % de los archivos de texto:** búsquedas de patrón (`8/18`, `10/18`, D-4…D-8 pendientes, Q-7, Supabase/PostgreSQL/RLS/multiusuario, «Fase 0 aceptada», «Fase 1 autorizada», «pendiente de decisión», etc.) con indicación de si el archivo tiene nota de vigencia; comprobación de referencias a archivos (backticks y enlaces `.md`); cobertura de índices; duplicados por nombre.
- **Lectura manual (parcial, por extractos de contexto)** de: `REGISTRO_DECISIONES_RESUELTAS.md` (secciones P1, P3, P4, Q-7, D-1, D-3, D-5, D4/D6/D7/D8, notas), `DECISIONES_P4_PENDIENTES.md`, `MATRIZ_CONSOLIDADA_18_ENTIDADES.md`, `MATRIZ_DECISIONES_PROPIETARIO.md` (P5, P9, P11–P14, Q-4), `13_REGISTRO_DECISIONES_PROPIETARIO.md` (P6–P8, P10, P14, P15, Q-1…Q-7), encabezados de las fichas P1–P4A y de D1/D2/D3/D5, `INDICE_ANTECEDENTES_HISTORICOS.md` §4–5, `README_PROPUESTA_VIGENTE.md`, `FICHA_P4A_09`, `MANIFIESTO_ENTREGA…txt`, y los contextos de cada coincidencia de la búsqueda.
- **No se leyó línea a línea** el contenido completo de cada archivo del expediente (≈600 kB) ni de `docs/fase0/` (≈10 MB). No se afirma lectura íntegra.
## 3. Resultados
- Archivos del expediente clasificados: 93/93 (ninguno «sin clasificar»). Duplicados de nombre: 0.
- Archivos de texto no mencionados en ningún índice (00_INDICE, README_ENTREGA, 16_INDICE): 0 antes de esta auditoría (ejecutado).
- Referencias a archivos que **no existen en la rama**: ver `06_REGISTRO_CONTRADICCIONES.md` CR-12 (documentos del repositorio de la aplicación no publicados, adjuntos del propietario y abreviaturas). No son enlaces rotos internos del expediente.
- Contradicciones: ver `06_REGISTRO_CONTRADICCIONES.md` (16 registradas).
## 4. Archivos no accesibles y limitaciones
- **Ningún archivo de la rama resultó inaccesible.** Son inaccesibles (no están publicados en la rama; no se afirma haberlos leído): los adjuntos del propietario citados como A (`de49cc27-attachment.txt`) y B (`5a9f5585-attachment.txt`) de `LISTA_ORIGINAL_18_ENTIDADES.md`; los documentos del repositorio de la aplicación citados por nombre (`ARQUITECTURA.md`, `DECISIONES.md`, `ROADMAP.md`, `CI.md`, `INTEGRACION_SUPABASE_ESTADO.md`, `SEMANTICA_DE_SERVICIOS.md`, `ENTORNOS_Y_MODO_DEMO.md`, `INDICE.md`, `CONTROL_DE_SECRETOS.md`) y los expedientes `evidence/CCI_FASE1_1_A1_…` (`00_DICTAMEN_B0_B5.md`, `05_*`, `06_*`). **Limitación:** las citas «A l.N»/«B l.N» y las afirmaciones sobre esos documentos no pudieron contrastarse con su fuente aquí; se conservan como las registró el expediente.
- El repositorio `CCI-Evidence` es inaccesible (API 403, informado antes); no se usó.
- No se ejecutaron pruebas, build, E2E ni CI de la aplicación; los resultados de `logs/` son de ejecuciones previas, no reejecutadas.
- Los 52 históricos y los 5 archivos raíz de `docs/fase0` se conciliaron por clasificación, tamaño y SHA-256, y por búsquedas de patrón y lectura de encabezados de los 5 archivos raíz; no por lectura íntegra.
- La arquitectura browser-only se comprobó por coincidencias de texto en índice, README y `04_ARQUITECTURA_BROWSER_ONLY.md`, no por revisión técnica de código.
