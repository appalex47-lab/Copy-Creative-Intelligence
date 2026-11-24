# Metodología Copy & Creative Intelligence — cobertura por la herramienta

Fuente: documento del propietario (2026-11-23, «Esto debe hacer la herramienta»). Estado al construir S4.1.
Todas las decisiones marcadas son de Claude bajo delegación y revocables.

| Etapa / módulo del documento | Estado | Cómo |
|---|---|---|
| 1. Brief comercial | Construida parcial | Briefs (S2.2). El documento pide 9 elementos (objetivo, producto, audiencia, necesidad, beneficio, incentivo, diferenciador, acción, restricciones): verificar contra los campos reales del brief y completar los faltantes (pendiente). |
| 2. Arquitectura del mensaje (atención, interés, justificación, acción, incertidumbre) | No construida | Pendiente: guía/estructura en el editor de copy. |
| 3. Técnicas de copywriting (AIDA, PAS, FAB, 4U, BAB) y 3 propuestas conceptualmente distintas | No construida | Es generación de texto (IA) o plantillas; sin IA por la arquitectura sin red. Posible: plantillas manuales. |
| 4. Adaptación a formato y canal | Construida (S2.8) | Adaptaciones por canal. La tabla de prioridades por formato del documento no está como guía. «Llamadas» sigue fuera del catálogo de canales por decisión previa (Q-2): contradice el documento, a ratificar. |
| 5. Auditoría (8 dimensiones /100, hallazgos de 4 elementos, veredicto) | Construida (S4.1) | Vista «Revisión»: la persona califica las 8 dimensiones; la app calcula puntaje, banda y veredicto y bloquea por hallazgos críticos. Convive con el puntaje automático por reglas (Q-5, pesos distintos): contradicción de políticas a ratificar. |
| 6. Control de calidad: filtro creativo + filtro comercial independientes | Construida (S4.1) | Ambos deben estar «aprobados» y el veredicto ser APROBADO para marcar «publicable». Aprobar el creativo exige las 8 dimensiones y cero bloqueantes; aprobar el comercial exige los 6 puntos confirmados. No valida contra datos de catálogo/SKU (la app no los tiene). Esta marca no publica nada y no hay identidad/roles (Q-3 pendiente). |
| Checklist de 12 puntos | Construida (S4.1) | Con reinicio. |
| Prompt maestro | Construida (S4.1) | Botón para copiarlo y usarlo con una IA externa; la app no llama a ninguna IA. |
| Niveles Creación / Validación / Aprobación | No construida | Requiere roles; la app no tiene cuentas. Hoy: campo opcional «quién revisa». |
| 7. Medición y aprendizaje (CTR, conversión, ventas; pruebas A/B con hipótesis) | No construida | Requiere cargar resultados (importación) y definir fuentes; pendiente. |
| Biblioteca de aprendizaje (aprobados, rechazados con motivo, mejores titulares/CTA, errores recurrentes) | No construida | Base disponible: auditorías, revisiones y hallazgos guardados. Falta consultarlos como biblioteca. |
| Módulo 1 Copy Generator | No construida | IA generativa: fuera por arquitectura sin red. |
| Módulo 2 Creative Auditor | Parcial | OCR + reglas + revisión humana (S3, S4.1). Sin análisis visual automático (sin IA). |
| Módulo 3 Promotion Validator | No construida | Requiere datos de promoción (SKU, vigencia, disponibilidad) que la app no tiene. |
| Módulo 4 Channel Adaptation | Construida | S2.8. |
| Módulo 5 Performance Intelligence | No construida | Ver etapa 7. |
| Auditoría semanal (recordatorio) | No construida | Sin servidor no hay avisos fuera del navegador; posible: recordatorio al abrir la app. |

## Datos de S4.1
- Revisiones: IndexedDB v10 (`reviews`), una por copy o pieza. NO van en el respaldo JSON de datos; van en el archivo `cci-recursos-*.json` v3 junto con imágenes y piezas (la v1 y la v2 se siguen aceptando). «Respaldo» avisa cuántas hay. Pendiente decidir si se integran al respaldo de datos.
- Bandas del documento: 90–100 Excelente; 80–89 Bueno; 70–79 Requiere correcciones; 0–69 Requiere replanteamiento. Veredicto (SUPUESTO): ≥90 APROBADO; 80–89 APROBADO CON AJUSTES; <80 RECHAZADO; bloqueante = RECHAZADO; incompleta = PENDIENTE.
