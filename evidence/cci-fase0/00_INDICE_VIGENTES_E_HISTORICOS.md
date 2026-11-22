# Expediente CCI Fase 0 — índice de revisión (publicado 2026-11-22)
**Qué es:** copia documental del expediente de Fase 0 (auditoría y definición del producto, arquitectura browser-only). **No contiene código fuente ni modifica la aplicación.** No es aceptación de Fase 0 ni autoriza Fase 1: todas las aprobaciones (0.1–0.7), la aceptación final y Fase 1 siguen pendientes del propietario.
**Regla de lectura:** las recomendaciones de Claude **no son decisiones**. Solo valen como decisión las respuestas literales del propietario en `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. D-5 está resuelta (R3, conjunto (b), M-1); **D5.a–d quedaron expresamente fuera del alcance vigente (decisión definitiva del propietario): no son pendientes, no se cuentan como abiertas, no condicionan D-4 ni otras decisiones y no se vuelven a preguntar.** Las menciones anteriores en documentos históricos son antecedente con nota de actualización posterior.

## Documentos vigentes (empezar aquí)
1. `entregables_formales/RONDA_UNICA_D4_D6_D7_D8_MATRIZ_CONSOLIDADA.md` — **único documento vigente que el propietario debe responder** (11 decisiones pendientes; recomendaciones de Claude no aprobadas). D1, D2, D3 y D5 siguen resueltas; D5.a–d permanecen fuera del alcance y no deben reabrirse.
2. `entregables_formales/INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md` y `entregables_formales/MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` — entrega de las 12:35.
3. `entregables_formales/INFORME_CIERRE_2026-11-22_REGLA_PERMANENTE_12_43.md` — entrega de las 12:43.
4. `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` — decisiones literales del propietario (D-1, D-2, D-3, D-5, entidades 1–8).
5. `entregables_formales/DECISIONES_P4_PENDIENTES.md`, `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` (los avisos de actualización prevalecen sobre celdas antiguas), `entregables_formales/CATALOGO_DEPENDENCIAS_D4_D8.md`, `entregables_formales/D1_ANALISIS_CONTENIDO.md`, `entregables_formales/D2_VARIANTE_FRENTE_A_VERSION.md`, `entregables_formales/D3_FAMILIAS_DE_REGLAS.md`, `entregables_formales/D5_APROBACION.md`, `entregables_formales/FICHA_P4A_01_CAMPANA.md` … `entregables_formales/FICHA_P4A_08_AUDITORIA_CREATIVA.md`.
6. `README_ENTREGA.md`, `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md`, `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256`.

6b. `entregables_formales/CONTROL_DE_CAMBIOS_CORRECCION_2026-11-22.md` e `entregables_formales/INFORME_CIERRE_2026-11-22_CORRECCION_DOCUMENTAL.md` — corrección documental posterior (vigentes).

## Antecedentes históricos o sustituidos (conservados sin reescribir)
- `entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md` — **antecedente de análisis** de la matriz vigente; **no es un instrumento alternativo de respuesta**.
- `entregables_formales/PAQUETE_DECISION_D1_D8.md` — **sustituido** por el paquete de D-4/D-6/D-7/D-8.
- `entregables_formales/DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md` — origen de D-1…D-8 (contiene propuestas rechazadas por el propietario, p. ej. fusionar Perfil local con Configuración).
- `entregables_formales/FICHA_P4A_09_HALLAZGO.md` — entidad 9 **suspendida, no aprobada**.
- `00`–`14` y `INFORME_REVISION_COMPLEMENTARIA.md` en la raíz de la carpeta, y `entregables_formales/01`–`15`, `entregables_formales/ADR_PROPUESTO_REEMPLAZO_DEC_D2_D3_D4.md`: propuestas previas del expediente. **Los documentos 05, 06 y 07 (en ambas ubicaciones) llevan ahora una advertencia de vigencia: son propuestas anteriores, no el contrato vigente; prevalecen D-1, D-2, D-3, D-5, P1, P2, P3 y P4.A; no existe entidad genérica «Regla» vigente.**
- `anexos/` y `logs/`: informe original y evidencias de ejecución (162/162 unitarias, 29/29 E2E en una ejecución anterior; no re-ejecutadas hoy). Los logs contienen rutas temporales del entorno de verificación, sin datos sensibles.

## Estado de verificación
Revisión de seguridad previa a la publicación (patrones de claves/tokens/credenciales, correos, URL, identificadores de Supabase, datos personales): sin hallazgos. No se publicó el `.tar.gz` (duplicaría los archivos).
