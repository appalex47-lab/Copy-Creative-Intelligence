# Fase 2 — cobertura de las 14 funciones (2026-11-23)

Fuente: «Funciones, definiciones y reglas funcionales candidatas para Fase 2» (documento del propietario, vía ChatGPT). Estado según lo construido hasta el commit de S2.6. Claude lo redactó; el propietario no lo ha validado.

| # | Función | Estado | Observación |
|---|---|---|---|
| 1 | Campañas | Construida (S2.8, simple) | Registro con nombre y nota; el brief puede referenciarla (opcional). Atributos reales por definir. |
| 2 | Productos | Construida (S2.8, simple) | Registro con nombre y nota; sin relación con briefs ni ofertas. |
| 3 | Ofertas | Construida (S2.8, simple) | Registro con nombre y nota; sin precios ni vigencia estructurados. |
| 4 | Briefs | Construida (S2.1–S2.3) | Los 13 campos y cuáles son obligatorios son supuestos aprobados bajo delegación; el documento dice que no están aprobados como obligatorios. |
| 5 | Copies | Construida (S2.4) | Versiones inmutables. Sin estados de aprobación (correcto: Fase 5). |
| 6 | Variantes | Construida (S2.7, corregida) | Alternativa de texto dentro del copy, sin versiones propias. Máximo 10 por copy (supuesto). Falta selección y comparación entre variantes. |
| 7 | Adaptación por canal | Construida (S2.8) | Entidad derivada de un copy y su versión; no se audita ni aprueba. |
| 8 | Reglas de marca y comerciales | Parcial | Leyendas y términos de marca configurables (marca). No hay ReglaComercial como entidad; la comparación de porcentajes vive dentro del motor. |
| 9 | Auditoría creativa | Adelantada, parcial | «Revisar reglas» calcula al vuelo; no hay entidad Creative Audit guardada. |
| 10 | Hallazgos | Adelantada, parcial | Se muestran, no se guardan como entidad. |
| 11 | Puntuación | Adelantada | Pesos Q-5 aprobados por el propietario el 2026-11-23; el documento recibido dice «no inventar pesos», lo que está desactualizado frente a Q-5. |
| 12 | IA | Solo IA-A | Plantillas sin IA. IA-B aprobada pero no construida. |
| 13 | Aprobaciones | No construida | Q-3 queda para Fase 5. |
| 14 | Resultados de desempeño | No construida | |

## Decisiones propuestas por Claude (revocables, pendientes de validar)
1. Rediseñar variantes: una variante será una alternativa de texto dentro de un Copy, SIN versiones propias; el Copy conserva el historial de versiones.
2. Entidades Campaña, Producto y Oferta: crearlas como entidades simples (solo nombre y campos mínimos ya usados), con referencia opcional desde el Brief, sin relaciones obligatorias.
3. La puntuación de S2.5a se declara «vista previa de la Fase 3»: no es una auditoría guardada ni una aprobación.
4. La asignación de cada función a una fase sigue sin confirmar por el propietario.

## Actualización S2.7
El propietario aprobó (2026-11-23) las decisiones 1–4 propuestas arriba. La 1 (variantes) quedó hecha en S2.7. Pendiente: entidades Campaña, Producto y Oferta (decisión 2).

## Actualización S2.8
Hechas las funciones 1–3 (entidades simples), 7 (adaptación por canal) y la búsqueda de copys. Siguen sin construir: 8 (ReglaComercial como entidad), 9–10 (auditoría y hallazgos guardados), 12 (IA-B), 13 (aprobaciones, Fase 5), 14 (resultados de desempeño) y la comparación/selección de variantes. Los atributos de Campaña/Producto/Oferta siguen pendientes de definición del propietario.
