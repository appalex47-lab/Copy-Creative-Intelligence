# Metodología Copy & Creative Intelligence — cobertura por la herramienta

Fuente: documento del propietario (2026-11-23, «Esto debe hacer la herramienta»). Estado al construir S4.2 (actualizado 2026-11-24).
Todas las decisiones marcadas son de Claude bajo delegación y revocables.

| Etapa / módulo del documento | Estado | Cómo |
|---|---|---|
| 1. Brief comercial | Construida (S4.2) | Briefs. Se añadieron «Necesidad» y «Diferenciador» (opcionales) para cubrir los 9 elementos: objetivo, producto, audiencia, necesidad, beneficio, oferta (incentivo), diferenciador, CTA (acción), condiciones (restricciones). |
| 2. Arquitectura del mensaje (atención, interés, justificación, acción, incertidumbre) | Construida (S4.2) | Vista «Plantillas»: guía de las 5 funciones y jerarquía de lectura. |
| 3. Técnicas de copywriting (AIDA, PAS, FAB, 4U, BAB) y 3 propuestas conceptualmente distintas | Construida sin IA (S4.2) | «Plantillas» arma borradores AIDA, PAS, FAB, 4U, BAB, Oferta+beneficio+CTA y Urgencia (solo con vigencia) usando únicamente los datos escritos o cargados de un brief; no inventa nada y no guarda. |
| 4. Adaptación a formato y canal | Construida (S2.8) | Adaptaciones por canal. La tabla de prioridades por formato está como guía en «Plantillas» (S4.2). «Llamadas» sigue fuera del catálogo de canales por decisión previa (Q-2): contradice el documento, a ratificar. |
| 5. Auditoría (8 dimensiones /100, hallazgos de 4 elementos, veredicto) | Construida (S4.1) | Vista «Revisión»: la persona califica las 8 dimensiones; la app calcula puntaje, banda y veredicto y bloquea por hallazgos críticos. Convive con el puntaje automático por reglas (Q-5, pesos distintos): contradicción de políticas a ratificar. |
| 6. Control de calidad: filtro creativo + filtro comercial independientes | Construida (S4.1) | Ambos deben estar «aprobados» y el veredicto ser APROBADO para marcar «publicable». Aprobar el creativo exige las 8 dimensiones y cero bloqueantes; aprobar el comercial exige los 6 puntos confirmados. No valida contra datos de catálogo/SKU (la app no los tiene). Esta marca no publica nada y no hay identidad/roles (Q-3 pendiente). |
| Checklist de 12 puntos | Construida (S4.1) | Con reinicio. |
| Prompt maestro | Construida (S4.1) | Botón para copiarlo y usarlo con una IA externa; la app no llama a ninguna IA. |
| Niveles Creación / Validación / Aprobación | Construida sin cuentas (S4.2) | La revisión tiene etapa (Creación/Validación/Aprobación), aprobación final «Liberada para publicar» y nombre de quien aprueba (texto, sin identidad verificable). Liberar exige revisión publicable y nombre. |
| 7. Medición y aprendizaje (CTR, conversión, ventas; pruebas A/B con hipótesis) | Construida (S4.2) | Vista «Medición»: resultados manuales o CSV y experimentos A/B con hipótesis. CTR = clics/impresiones; conversión = conversiones/clics (SUPUESTO). Comparación orientativa: prueba z de dos proporciones, aviso con menos de 100 en la base, sin ganador si p ≥ 0.05. |
| Biblioteca de aprendizaje (aprobados, rechazados con motivo, mejores titulares/CTA, errores recurrentes) | Construida (S4.2) | Vista «Biblioteca» (solo lectura): aprobados, rechazados con motivo, errores recurrentes (≥2 veces, top 10), mejores resultados (≥100 impresiones) y conclusiones de experimentos. No clasifica titulares ni CTA por separado. |
| Módulo 1 Copy Generator | No construida | IA generativa: fuera por arquitectura sin red. |
| Módulo 2 Creative Auditor | Parcial | OCR + reglas + revisión humana (S3, S4.1). Sin análisis visual automático (sin IA). |
| Módulo 3 Promotion Validator | Construida parcial (S4.2) | Vista «Promociones»: la persona captura o importa por CSV (nombre, porcentaje, SKU, vigencia, restricciones) y la app contrasta el texto de un copy, pieza (validado u OCR) o texto pegado: vencida, no iniciada, porcentaje ausente o distinto (tolerancia 0.5 pp), restricciones sin comunicar. No valida disponibilidad, precios en pesos ni SKUs dentro de imágenes. |
| Módulo 4 Channel Adaptation | Construida | S2.8. |
| Módulo 5 Performance Intelligence | Construida parcial (S4.2) | Ver etapa 7 y Biblioteca. |
| Auditoría semanal (recordatorio) | Construida (S4.2) | Aviso en Inicio al abrir la app si no hay revisión ni auditoría en los últimos 7 días. No hay notificaciones fuera del navegador. |

## Datos de S4.1
- Revisiones: IndexedDB v10 (`reviews`), una por copy o pieza. NO van en el respaldo JSON de datos; van en el archivo `cci-recursos-*.json` v3 junto con imágenes y piezas (la v1 y la v2 se siguen aceptando). «Respaldo» avisa cuántas hay. Pendiente decidir si se integran al respaldo de datos.
- Bandas del documento: 90–100 Excelente; 80–89 Bueno; 70–79 Requiere correcciones; 0–69 Requiere replanteamiento. Veredicto (SUPUESTO): ≥90 APROBADO; 80–89 APROBADO CON AJUSTES; <80 RECHAZADO; bloqueante = RECHAZADO; incompleta = PENDIENTE.

## Datos de S4.2
- IndexedDB v11: `measures` (resultados y experimentos) y `promos`. Tampoco van en el respaldo JSON de datos; van en `cci-recursos-*.json` v4 (se siguen aceptando v1 a v3). «Respaldo» y «Recursos» muestran los conteos.
- Revisiones: nuevos campos `stage`, `finalApproval`, `approver`; los registros anteriores se leen como «Validación» y «Pendiente».
- Puntaje automático y matriz humana: «Revisión» muestra la última auditoría por reglas como «Alerta por reglas (automática)», solo lectura; la matriz humana es la calificación oficial (decisión de Claude bajo delegación, revocable).
- Quedan sin construir: Copy Generator (IA generativa) y análisis visual automático (sin red por arquitectura).

## S5.1 (2026-11-24, decisiones de Claude bajo delegación, revocables)
- Tablero en Inicio; «por vencer» = fecha final dentro de 7 días; la app no sabe qué copy usa qué promoción (no hay vínculo), por eso solo avisa.
- Biblioteca de titulares/CTA: solo con resultados vinculados a un copy y ≥100 impresiones; usa la versión vigente del copy.
- Exportación: CSV de revisiones (con aprobador y etapa).
