# Informe de auditoría integral del expediente — ronda final (2026-11-22)
**Versión:** 3.6 (v3.5 + registro de las aprobaciones 0.1–0.7 y de R-1 por el propietario el 2026-11-22 20:14: 141 archivos; v3.4 + última regularización documental antes de las aprobaciones 0.1–0.7: 134 archivos; v3.3 + regularización posterior a la ratificación y preparación de aprobaciones: 125 archivos; v3.2 + ratificación de la propuesta maestra de cierre de Fase 0 por el propietario, 15:56: 114 archivos; v3.1 + corrección puntual de X4: 111 archivos; v3.0 + ronda de verificación de coherencia posterior: 110 archivos, métrica de avisos de vigencia recalculada y descrita con su alcance real; no cambia ningún estado de CR ni decisión) · **Fecha:** 2026-11-22 · **Estado:** vigente como informe de hechos; subordinado al registro de decisiones · **Base:** HEAD `13b25ca447c0ab17f46b3143615b4c2156661b79` (la v2.0 se redactó sobre `8dc47b24…`) · **Referencias:** `06_REGISTRO_CONTRADICCIONES.md`, `08_INFORME_INTEGRIDAD_ARCHIVOS.md`, `12_REGISTRO_LECTURA_Y_LIMITACIONES.md`.

## 0. Corrección de cifras de la versión anterior (hallazgo 3.5)
- La versión anterior clasificaba **93** archivos y declaraba «93/93 clasificados». El árbol real de la rama en `8dc47b2` (API) tenía **164** blobs = **104** en `evidence/cci-fase0/` (93 previos + 11 documentos de la auditoría integral) + **59** en `docs/fase0/` + **1** `README.md` de la raíz del repositorio.
- La tabla anterior mostraba **99 filas únicas**: los 93 previos más 6 documentos de auditoría; **cinco** documentos de auditoría (05, 06, 07, 08, 10) no estaban clasificados. **93/93 no cubría los 104 archivos actuales** y no debe citarse como cobertura del total.
- Esta versión clasifica **todos** los archivos actuales de `evidence/cci-fase0/` (107, tras añadir en esta ronda `12_REGISTRO_LECTURA_Y_LIMITACIONES.md`, `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt` y `logs/scan_contradicciones.py`). Los 59 archivos de `docs/fase0/` se concilian aparte (`11_`, `12_`).
- **Ronda de verificación de coherencia posterior (2026-11-22; base `580c51f`):** se añaden 3 archivos (`auditoria_integral/13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md`, `logs/verificacion_coherencia_posterior.py` y `logs/verificacion_coherencia_posterior_2026-11-22.txt`) → **110** archivos en el expediente.
- **Corrección puntual de X4 (2026-11-22; base `e049fcd`):** se añade 1 archivo (`logs/verificacion_coherencia_posterior_2026-11-22_x4_corregido.txt`) → **111** archivos. Alcance: solo el control X4 del script y la evidencia directamente afectada; no es una nueva auditoría.
- **Ratificación de la propuesta maestra (2026-11-22 15:56; base `bb2030a`):** se añaden 3 archivos (`entregables_formales/PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md`, `entregables_formales/CONTROL_DE_CAMBIOS_RATIFICACION_PROPUESTA_MAESTRA_2026-11-22.md` y `logs/verificacion_coherencia_posterior_2026-11-22_tras_ratificacion.txt`) → **114** archivos. Alcance: registrar la ratificación del propietario y actualizar la evidencia derivada; no cambia ningún estado de CR ni emite aprobaciones.
- **Registro de las aprobaciones 0.1–0.7 y de R-1 (2026-11-22 20:14; base `cad808a2da6659d68b41578625ed409a4f8ee3d8`):** se añaden 7 archivos (`entregables_formales/CONTROL_DE_CAMBIOS_APROBACIONES_0_1_A_0_7_2026-11-22.md` y 6 en `logs/`) → **141** archivos en el expediente. Alcance: registrar la respuesta del propietario (aprobaciones 0.1–0.7 emitidas, 7/7; 0.5 solo en cuanto a principios; R-1 = aplazamiento aceptado, no resolución) y actualizar verificadores y evidencia; la aceptación de Fase 0 y la autorización de Fase 1 siguen pendientes.
- **Última regularización documental (2026-11-22; base `bf437e4617b253929e1fb7c77bb5f70907471495`):** se añaden 9 archivos (`entregables_formales/CONTROL_DE_CAMBIOS_SEGUNDA_REGULARIZACION_2026-11-22.md`, `auditoria_integral/15_INFORME_FINAL_SEGUNDA_REGULARIZACION.md` y 7 en `logs/`) → **134** archivos en el expediente. Alcance: corregir R-1 (seis cuestiones), mantener D5.a–d fuera del alcance vigente (no incluidas en R-1), reclasificar `06_MODELO_DATOS_CCI.md` y reforzar los verificadores; no cambia ninguna decisión ni estado de CR.

## 1. Alcance real
| Concepto | Cantidad |
|---|---|
| Archivos en `evidence/cci-fase0/` (tras el registro de las aprobaciones 0.1–0.7) | 141 |
| Archivos en `docs/fase0/` (sin modificar; idénticos a `main`) | 59 |
| `README.md` de la raíz del repositorio (fuera del expediente; sin modificar) | 1 |
| Total de blobs esperado en la rama tras publicar | 201 |

## 2. Clasificación por vigencia de los 141 archivos del expediente
| Clase | Archivos |
|---|---|
| Antecedente (análisis resuelto) | 4 |
| Antecedente (respondido) | 2 |
| Antecedente / propuesta | 7 |
| Evidencia técnica | 38 |
| Histórico | 2 |
| Histórico (copia previa) | 16 |
| Histórico (ficha resuelta/suspendida) | 14 |
| Informe de auditoría (derivado) | 5 |
| Informe/control (fechado) | 14 |
| Integridad | 3 |
| Integridad (informe) | 1 |
| Propuesta | 1 |
| Propuesta (ratificada; copia literal) | 1 |
| Propuesta (subordinada) | 15 |
| Propuesta vigente (no aprobada en bloque) | 1 |
| Superado | 1 |
| VIGENTE AUTORITATIVO | 1 |
| Vigente (derivado) | 8 |
| Vigente (subordinado) | 4 |
| Vigente (índice) | 3 |

**Aviso de vigencia en el propio archivo** (cifras de la ronda de 114 archivos, **no recalculadas** en la última regularización; clases histórica, antecedente, superado e informe: 58 archivos en esas clases; **55 de 55 aplicables** con marca; 3 «n/a»: el archivo de hashes `anexos/MANIFEST_informe_browser_only.sha256` y los informes derivados vigentes `05_` y `12_`; el nuevo `13_` también figura «n/a»). **Alcance de la métrica:** detección automática a nivel de **archivo** (basta una marca en cualquier parte del archivo); no verifica que cada afirmación histórica del archivo esté individualmente marcada. Dentro de las 46 filas de clase histórica/antecedente/superado: 45 con marca y 1 «n/a» (el archivo de hashes); `FICHA_P4A_09` se detecta por su encabezado «SUSPENDIDA».

Detalle archivo por archivo (ruta · clase · motivo · aviso de vigencia en el archivo):

| Ruta | Clase | Motivo | Aviso |
|---|---|---|---|
| `00_DICTAMEN_Y_CIERRE_FASE0.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `00_INDICE_VIGENTES_E_HISTORICOS.md` | Vigente (índice) | Índice/guía; refleja el registro | n/a |
| `01_INFORME_AUDITORIA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `02_INVENTARIO_FUNCIONALIDADES.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `03_CONCILIACION_DOCUMENTAL.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `04_MATRIZ_REQUISITOS.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `05_ARQUITECTURA_BROWSER_ONLY.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `06_MODELO_DE_DOMINIO.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `07_DISENO_PERSISTENCIA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `08_RESPALDO_Y_RECUPERACION.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `09_ANALISIS_IA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `10_REGISTRO_DECISIONES.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `11_ROADMAP_Y_CRITERIOS_FASES_1_A_5.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `12_ESTRATEGIA_DE_PRUEBAS.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `13_VERIFICACION_EJECUTADA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `14_ESTADO_GIT_Y_OPERACIONES.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `INFORME_REVISION_COMPLEMENTARIA.md` | Histórico (copia previa) | Versión previa del expediente (raíz); prevalece entregables_formales y el registro | Sí |
| `INVENTARIO_PUBLICADO.sha256` | Integridad | Manifiesto/inventario (regenerado al publicar) | n/a |
| `MANIFEST.sha256` | Integridad | Manifiesto/inventario (regenerado al publicar) | n/a |
| `README_ENTREGA.md` | Vigente (índice) | Índice/guía; refleja el registro | n/a |
| `anexos/INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md` | Histórico | Anexo probatorio del informe de auditoría browser-only; fecha anterior al registro de decisiones | Sí |
| `anexos/MANIFEST_informe_browser_only.sha256` | Histórico | Anexo probatorio del informe de auditoría browser-only; fecha anterior al registro de decisiones | n/a |
| `auditoria_integral/01_INDICE_MAESTRO_FASE0.md` | Vigente (derivado) | Índice maestro de la auditoría; subordinado al registro | n/a |
| `auditoria_integral/02_MATRIZ_MAESTRA_DECISIONES.md` | Vigente (derivado) | Matriz maestra de decisiones; subordinada al registro | n/a |
| `auditoria_integral/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md` | Vigente (derivado) | Matriz de las 18 entidades; subordinada al registro | n/a |
| `auditoria_integral/04_MATRIZ_MAESTRA_DEPENDENCIAS.md` | Vigente (derivado) | Matriz de dependencias; subordinada al registro | n/a |
| `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md` | Informe de auditoría (derivado) | Informe de la auditoría integral y clasificación de todos los archivos | n/a |
| `auditoria_integral/06_REGISTRO_CONTRADICCIONES.md` | Vigente (derivado) | Registro de contradicciones y su resolución | n/a |
| `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | Informe/control (fechado) | Control de cambios de la auditoría y de la ronda final | Sí |
| `auditoria_integral/08_INFORME_INTEGRIDAD_ARCHIVOS.md` | Integridad (informe) | Informe de integridad y verificación de hashes/tamaños | n/a |
| `auditoria_integral/09_PAQUETE_CONSOLIDADO_DECISIONES_PENDIENTES.md` | Vigente (derivado) | Paquetes de decisiones pendientes para el propietario; subordinado al registro | n/a |
| `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md` | Informe/control (fechado) | Informe ejecutivo de preparación para el cierre (no es aceptación) | Sí |
| `auditoria_integral/11_INDICE_CONCILIACION_DOCS_FASE0.md` | Vigente (derivado) | Conciliación de docs/fase0 (59 archivos, tamaño y SHA-256) | n/a |
| `auditoria_integral/12_REGISTRO_LECTURA_Y_LIMITACIONES.md` | Informe de auditoría (derivado) | Registro de lectura real y limitaciones; ficha de los 52 históricos | n/a |
| `auditoria_integral/13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md` | Informe de auditoría (derivado) | Informe de la verificación final de coherencia posterior a la regularización | n/a |
| `entregables_formales/01_INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/02_INVENTARIO_FUNCIONAL_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/03_MATRIZ_REQUISITOS_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/04_ARQUITECTURA_BROWSER_ONLY.md` | Propuesta vigente (no aprobada en bloque) | Arquitectura browser-only vigente por decisión del propietario; aprobación 0.2 pendiente | n/a |
| `entregables_formales/05_MODELO_DOMINIO_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/06_MODELO_DATOS_CCI.md` | Propuesta (subordinada) | Propuesta histórica **no aprobada**; no es un esquema de datos aprobado (clasificación y marcas en el propio documento); aprobaciones 0.x pendientes | n/a |
| `entregables_formales/07_DISENO_PERSISTENCIA_INDEXEDDB.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/08_RESPALDO_IMPORTACION_RECUPERACION.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/09_ESTRATEGIA_IA_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/10_DEFINICION_MVP_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/11_ROADMAP_FASES_0_A_5.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/12_CRITERIOS_ACEPTACION_FASES.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/13_REGISTRO_DECISIONES_PROPIETARIO.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/14_MATRIZ_RIESGOS_CCI.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/15_PLAN_CALIDAD_Y_PRUEBAS.md` | Propuesta (subordinada) | Entregable formal propuesto; aprobaciones 0.x pendientes; con advertencias donde aplica | n/a |
| `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md` | Vigente (índice) | Índice/guía; refleja el registro | n/a |
| `entregables_formales/ADR_PROPUESTO_REEMPLAZO_DEC_D2_D3_D4.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro | Sí |
| `entregables_formales/APROBACIONES_FASE0.md` | Vigente (subordinado) | Estado vigente al inicio; texto anterior conservado como antecedente | n/a |
| `entregables_formales/CATALOGO_DEPENDENCIAS_D4_D8.md` | Vigente (subordinado) | Estado vigente al inicio; texto anterior conservado como antecedente | n/a |
| `entregables_formales/CONCILIACION_D1_D9_VERIFICADA.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro | Sí |
| `entregables_formales/CONTROL_DE_CAMBIOS_CORRECCION_2026-11-22.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado | Sí |
| `entregables_formales/CONTROL_DE_CAMBIOS_CORRECCION_INTEGRAL_P4A_9_18_2026-11-22.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado | Sí |
| `entregables_formales/CONTROL_DE_CAMBIOS_RATIFICACION_PROPUESTA_MAESTRA_2026-11-22.md` | Informe/control (fechado) | Control de cambios de la ratificación: interpretaciones, archivos modificados, estado de los criterios del §18 de la propuesta | n/a |
| `entregables_formales/CONTROL_DE_CAMBIOS_REGISTRO_D4_D6_D7_D8_2026-11-22.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado | Sí |
| `entregables_formales/CONTROL_DE_CAMBIOS_REGULARIZACION_P4A_9_18_2026-11-22.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado | Sí |
| `entregables_formales/CONVENCIONES_P4_5_CONDICIONES.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro | Sí |
| `entregables_formales/D1_ANALISIS_CONTENIDO.md` | Antecedente (análisis resuelto) | Análisis previo a la decisión; ver registro | Sí |
| `entregables_formales/D2_VARIANTE_FRENTE_A_VERSION.md` | Antecedente (análisis resuelto) | Análisis previo a la decisión; ver registro | Sí |
| `entregables_formales/D3_FAMILIAS_DE_REGLAS.md` | Antecedente (análisis resuelto) | Análisis previo a la decisión; ver registro | Sí |
| `entregables_formales/D5_APROBACION.md` | Antecedente (análisis resuelto) | Análisis previo a la decisión; ver registro | Sí |
| `entregables_formales/DECISIONES_P4_PENDIENTES.md` | Vigente (subordinado) | Estado vigente al inicio; texto anterior conservado como antecedente | n/a |
| `entregables_formales/DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro | Sí |
| `entregables_formales/FICHA_P1.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P2.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P3.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_01_CAMPANA.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_02_BRIEF.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_03_PRODUCTO.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_04_OFERTA.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_05_COPY.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_06_COPYVARIANT.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_07_PIEZA_CREATIVA.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_08_AUDITORIA_CREATIVA.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_P4A_09_HALLAZGO.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/FICHA_Q7.md` | Histórico (ficha resuelta/suspendida) | Planteamiento original conservado; estado en su encabezado y en el registro | Sí |
| `entregables_formales/INDICE_ANTECEDENTES_HISTORICOS.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro | Sí |
| `entregables_formales/INFORME_CIERRE_2026-11-22_CORRECCION_DOCUMENTAL.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado | Sí |
| `entregables_formales/INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado | Sí |
| `entregables_formales/INFORME_CIERRE_2026-11-22_REGISTRO_D4_D6_D7_D8.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado | Sí |
| `entregables_formales/INFORME_CIERRE_2026-11-22_REGLA_PERMANENTE_12_43.md` | Informe/control (fechado) | Estado a su hora; con nota fechada si fue superado | Sí |
| `entregables_formales/LISTA_ORIGINAL_18_ENTIDADES.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro | Sí |
| `entregables_formales/MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` | Integridad | Manifiesto/inventario (regenerado al publicar) | n/a |
| `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` | Vigente (subordinado) | Estado vigente al inicio; texto anterior conservado como antecedente | n/a |
| `entregables_formales/MATRIZ_DECISIONES_PROPIETARIO.md` | Antecedente / propuesta | Análisis o propuesta; no prevalece sobre el registro | Sí |
| `entregables_formales/PAQUETE_DECISION_D1_D8.md` | Superado | Sustituido por PAQUETE_DECISION_D4_D6_D7_D8 | Sí |
| `entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md` | Antecedente (respondido) | Instrumento ya respondido; no se usa para volver a preguntar | Sí |
| `entregables_formales/PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md` | Propuesta (ratificada; copia literal) | Copia literal (SHA-256 `8eb73476…3999`) de la propuesta maestra que el propietario ratificó con «Confirmo todo» (15:56); fuente literal de las definiciones PE-09…PE-18; prevalece ante cualquier resumen | n/a |
| `entregables_formales/README_PROPUESTA_VIGENTE.md` | Propuesta | README propuesto; no sustituye el README del repositorio | n/a |
| `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` | VIGENTE AUTORITATIVO | Fuente de verdad de decisiones del propietario (nivel 2) | n/a |
| `entregables_formales/RONDA_UNICA_D4_D6_D7_D8_MATRIZ_CONSOLIDADA.md` | Antecedente (respondido) | Instrumento ya respondido; no se usa para volver a preguntar | Sí |
| `logs/build.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/build_production_esperado_FALLO.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/check_secrets.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/e2e_corrida1.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/e2e_corrida2.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/e2e_corrida3.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt` | Evidencia técnica | Resultado del escaneo automático de contradicciones (ronda final; reproducible con el script adjunto) | n/a |
| `logs/format_check.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/lint.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/resumen_1.txt` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/scan_contradicciones.py` | Evidencia técnica | Script del escaneo automático de contradicciones (solo lectura) | n/a |
| `logs/test_run.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/typecheck.log` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `logs/verificacion_coherencia_posterior.py` | Evidencia técnica | Script de la verificación de coherencia posterior (solo lectura; reproducible; X4 corregido en la ronda puntual) | n/a |
| `logs/verificacion_coherencia_posterior_2026-11-22.txt` | Evidencia técnica | Salida original (commit `e049fcd`) con el X4 defectuoso; se conserva como antecedente | n/a |
| `logs/verificacion_coherencia_posterior_2026-11-22_tras_ratificacion.txt` | Evidencia técnica | Salida del script de coherencia tras registrar la ratificación (incluye el control V13 añadido) (registro de hechos) | n/a |
| `logs/verificacion_coherencia_posterior_2026-11-22_x4_corregido.txt` | Evidencia técnica | Salida del script con X4 corregido, pruebas de regresión y detalle por CR y documento (registro de hechos) | n/a |
| `logs/verificaciones_documentales_2026-11-22_correccion.txt` | Evidencia técnica | Evidencia de ejecución previa (no reejecutada); registro de hechos | n/a |
| `entregables_formales/CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md` | Vigente (derivado) | Conciliación de las 30 decisiones, hojas de los 10 aplazamientos y verificación de las 18 entidades; deriva del registro autoritativo | Sí (declara que no decide) |
| `entregables_formales/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md` | Propuesta (subordinada) | Paquete de decisión de las aprobaciones 0.1–0.7 con recomendaciones no vinculantes; no emite aprobaciones (las emitió el propietario el 2026-11-22 20:14, ver el registro) | Sí |
| `entregables_formales/CONTROL_DE_CAMBIOS_PREPARACION_APROBACIONES_2026-11-22.md` | Informe/control (fechado) | Control de cambios de la regularización posterior a la ratificación y preparación de aprobaciones | Sí |
| `auditoria_integral/14_INFORME_FINAL_REGULARIZACION_Y_PREPARACION_APROBACIONES.md` | Informe de auditoría (derivado) | Informe ejecutivo final con anexos A–J y métricas separadas | Sí |
| `logs/verificacion_semantica_fase0.py` | Evidencia técnica | Script de control semántico (S1–S14, E1–E5, R1–R4, D1–D4, A1–A2) con 59 pruebas positivas y negativas (ampliado en la última regularización) | n/a |
| `logs/verificacion_semantica_fase0_2026-11-22.txt` | Evidencia técnica | Salida del control semántico de la ronda anterior (32 pruebas; conservada como antecedente de la segunda regularización) (registro de hechos) | n/a |
| `logs/verificacion_semantica_fase0_prueba_mutacion_2026-11-22.txt` | Evidencia técnica | Salida del control semántico sobre una copia deliberadamente alterada (prueba de que detecta defectos) | n/a |
| `logs/verificacion_coherencia_posterior_2026-11-22_regularizacion.txt` | Evidencia técnica | Salida del script de coherencia tras la regularización (registro de hechos) | n/a |
| `logs/escaneo_contradicciones_2026-11-22_regularizacion.txt` | Evidencia técnica | Salida de `scan_contradicciones.py` v2 (clasificación por párrafo) (registro de hechos) | n/a |
| `entregables_formales/CONTROL_DE_CAMBIOS_SEGUNDA_REGULARIZACION_2026-11-22.md` | Informe/control (fechado) | Control de cambios de la última regularización documental antes de las aprobaciones 0.1–0.7 | Sí |
| `auditoria_integral/15_INFORME_FINAL_SEGUNDA_REGULARIZACION.md` | Informe de auditoría (derivado) | Informe final de la última regularización (resultado, R-1, métricas separadas, verificaciones, pendientes) | Sí |
| `logs/prueba_mutacion_semantica.py` | Evidencia técnica | Prueba de mutación reproducible: siembra 8 defectos documentales sintéticos y comprueba que el verificador semántico los detecta | n/a |
| `logs/prueba_mutacion_semantica_2026-11-22_segunda_regularizacion.txt` | Evidencia técnica | Salida de la prueba de mutación (8/8 detectadas; control sin mutación) (registro de hechos) | n/a |
| `logs/verificacion_semantica_fase0_2026-11-22_segunda_regularizacion.txt` | Evidencia técnica | Salida del control semántico (59 pruebas) sobre el expediente real (registro de hechos) | n/a |
| `logs/verificacion_coherencia_posterior_2026-11-22_segunda_regularizacion.txt` | Evidencia técnica | Salida del script de coherencia tras la última regularización (registro de hechos) | n/a |
| `logs/escaneo_contradicciones_2026-11-22_segunda_regularizacion.txt` | Evidencia técnica | Salida de `scan_contradicciones.py` v2 tras la última regularización (registro de hechos) | n/a |
| `logs/relectura_completa_2026-11-22_segunda_regularizacion.txt` | Evidencia técnica | Registro de relectura completa de cada archivo modificado (archivo, líneas, bytes, resultado) (registro de hechos) | n/a |
| `logs/integridad_y_clon_limpio_2026-11-22_segunda_regularizacion.txt` | Evidencia técnica | Integridad (hashes, tamaños, enlaces) y reproducción de verificadores desde un clon limpio local (registro de hechos) | n/a |
| `entregables_formales/CONTROL_DE_CAMBIOS_APROBACIONES_0_1_A_0_7_2026-11-22.md` | Informe/control (fechado) | Control de cambios del registro de las aprobaciones 0.1–0.7 y de la respuesta a R-1 | Sí |
| `logs/prueba_mutacion_semantica_2026-11-22_aprobaciones_0_1_a_0_7.txt` | Evidencia técnica | Salida de la prueba de mutación (13/13 detectadas; control sin mutación) (registro de hechos) | n/a |
| `logs/verificacion_semantica_fase0_2026-11-22_aprobaciones_0_1_a_0_7.txt` | Evidencia técnica | Salida del control semántico (70 pruebas) sobre el expediente real (registro de hechos) | n/a |
| `logs/verificacion_coherencia_posterior_2026-11-22_aprobaciones_0_1_a_0_7.txt` | Evidencia técnica | Salida del script de coherencia tras el registro de las aprobaciones (registro de hechos) | n/a |
| `logs/escaneo_contradicciones_2026-11-22_aprobaciones_0_1_a_0_7.txt` | Evidencia técnica | Salida de `scan_contradicciones.py` v2 tras el registro de las aprobaciones (registro de hechos) | n/a |
| `logs/relectura_completa_2026-11-22_aprobaciones_0_1_a_0_7.txt` | Evidencia técnica | Registro de relectura de los cambios de cada archivo modificado (archivo, líneas, bytes, resultado) (registro de hechos) | n/a |
| `logs/integridad_y_clon_limpio_2026-11-22_aprobaciones_0_1_a_0_7.txt` | Evidencia técnica | Integridad (hashes, tamaños, enlaces) y reproducción de verificadores desde un clon limpio local (registro de hechos) | n/a |
| `logs/verificar_expediente_historico_2026-11-22.txt` | Evidencia técnica | Salida de la herramienta histórica sobre copia de `docs/fase0`; solo aplica a esa línea (registro de hechos) | n/a |
| `logs/modelo_estructural_historico_2026-11-22.txt` | Evidencia técnica | Salida de la herramienta histórica de modelo estructural; solo aplica a la línea Supabase (registro de hechos) | n/a |

## 3. Método (qué se hizo realmente)
- **Procesamiento automático** de los archivos de texto de `evidence/cci-fase0/` (salvo `auditoria_integral/` y `logs/`): búsquedas de patrón (8/18, D4.d pendiente, «Adaptación pendiente de D-4», «Prevalece este aviso», «cinco cuestiones», Supabase/PostgreSQL/RLS, multiusuario, «Fase 0 aceptada», Q-7/P4.4, D5.a–d, «Fase 1 autorizada») con indicación de si el archivo tiene marca de vigencia: `logs/scan_contradicciones.py` y su salida. **Es escaneo, no lectura.**
- **Lectura efectiva** con registro de cobertura en bytes: ver `12_REGISTRO_LECTURA_Y_LIMITACIONES.md` v2.1. Según `12_` (§2), el expediente cuenta 104 LEÍDO_COMPLETO y 37 NO_APLICABLE de 141 archivos; en esa lectura se leyeron **por completo** los archivos de lectura aplicable de `evidence/cci-fase0/` y los 59 de `docs/fase0/` (estos últimos **por líneas únicas**: se mostró cada línea distinta; no se re-mostraron duplicados exactos de líneas ya vistas ni líneas genéricas repetidas). Los dos manifiestos de hashes, el manifiesto del anexo y el propio `12_` son NO_APLICABLE.
- **52 históricos de `docs/fase0/historico/`:** leídos por líneas únicas (ver `12_` §5, con bytes de líneas nuevas por archivo); los conteos de vocabulario de la ficha son indicadores por escaneo, no lectura.
- **Correcciones de contenido de esta ronda:** ver `07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` (sección «Ronda final»).
## 4. Resultados
- Archivos del expediente clasificados: **141/141** (100 % del conjunto actual; antes 134/134 y 114/114; no equivale a lectura íntegra ni a corrección de contenido).
- Contradicciones: **22 registradas** en `06_` v3.0: 13 RESUELTA_DOCUMENTALMENTE, 5 HISTORICA_CON_ADVERTENCIA, 2 RESUELTA_POR_DECISION_PROPIETARIO (CR-07 y CR-16), 1 PENDIENTE_PROPIETARIO (CR-17: C-2/C-3), 1 NO_RESOLUBLE_POR_FALTA_DE_EVIDENCIA (CR-12). Nuevas: CR-19…CR-22 (CR-21 es una regresión propia restaurada).
- Duplicados de nombre en el expediente: ver verificación en `08_`.
## 5. Archivos no accesibles y limitaciones
- **Ningún archivo de la rama resultó inaccesible.** No están en la rama (no se leyeron): adjuntos A (`de49cc27-attachment.txt`) y B (`5a9f5585-attachment.txt`) del propietario; documentos del repositorio de la aplicación citados por nombre (`ARQUITECTURA.md`, `DECISIONES.md`, `ROADMAP.md`, `CI.md`, `INTEGRACION_SUPABASE_ESTADO.md`, `SEMANTICA_DE_SERVICIOS.md`, `ENTORNOS_Y_MODO_DEMO.md`, `INDICE.md`, `CONTROL_DE_SECRETOS.md`) y expedientes `evidence/CCI_FASE1_1_A1_…`.
- El repositorio `CCI-Evidence` es inaccesible (API 403); no se usó ni se rodeó.
- **Lectura:** completa para los archivos legibles y aplicables, con la limitación del método de líneas únicas en `docs/fase0/` (≈10,3 MB; 2,2 MB de líneas únicas mostradas, el resto duplicado exacto). Detalle en `12_`. Esto no equivale a aceptar Fase 0.
- No se ejecutaron pruebas, build, E2E ni CI de la aplicación; los resultados de `logs/` son de ejecuciones previas.
- La arquitectura browser-only se comprobó por texto (índice, README, `04_ARQUITECTURA_BROWSER_ONLY.md` leído íntegro), no por revisión técnica de código.

## 6. Archivos históricos/antecedentes sin aviso de vigencia detectado
Ninguno.

> **Nota fechada 2026-11-22 20:14 (respuesta del propietario; no es decisión nueva de este documento):** el propietario emitió las aprobaciones 0.1–0.7 (7/7; la 0.5 solo en cuanto a principios, con P8 sin resolver y sin ninguna integración aprobada) y respondió «sí» a R-1 (aplazamiento aceptado de las seis cuestiones residuales, no resolución). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a aprobaciones «PENDIENTES» o «abiertas» describen el estado previo y quedan superadas en ese punto. **La aceptación formal de Fase 0 y la autorización independiente de Fase 1 siguen PENDIENTES.**
