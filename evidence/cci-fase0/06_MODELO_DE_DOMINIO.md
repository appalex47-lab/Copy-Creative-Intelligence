# Modelo de dominio (propuesta; sujeta a decisiones P1, P4, P5)
Clasificación: **MVP** = imprescindible para el MVP propuesto (fin de Fase 2: Command Center + Copy Studio persistentes) · **F3/F4/F5** = necesaria en esa fase posterior · **Futura** = no necesaria para el alcance vigente. El MVP es **propuesto**, no aprobado (decisión adicional Q-4).
Convenciones: `id` UUID v4 generado en cliente; `createdAt`/`updatedAt` ISO-8601 UTC; `revision` entero para control optimista; borrado lógico por `archivedAt`; importes como enteros en unidad menor (centavos) + moneda; ningún dato comercial inventado: un campo desconocido es `null`/ausente, no un valor por defecto.

| Entidad | Clase | Descripción y atributos clave | Relaciones | Invariantes principales |
|---|---|---|---|---|
| Configuración | MVP | claves de preferencias duraderas no ligeras (marca, idioma, canales activos, tolerancias) | — | un registro por clave; valores validados |
| Campaña | MVP | nombre, objetivo, estado (borrador/en revisión/…), vigencia | 1–N Brief, Copy, Pieza | nombre no vacío; estado dentro del flujo aprobado |
| Producto | MVP | nombre, identificador comercial, precio base (opcional) | N–N Oferta/Brief | precio ≥ 0 si existe |
| Oferta | MVP | tipo, beneficio, precio original/promocional, vigencia, condiciones, exclusiones | pertenece a Campaña; N–N Producto | si hay ambos precios, promocional ≤ original (se **valida**, no se corrige); fechas coherentes |
| Brief | MVP | objetivo, audiencia, mensaje central, tono, canal, formato, CTA, oferta | pertenece a Campaña | campos obligatorios definidos; incompleto = estado explícito |
| Copy | MVP | contenido principal (titular, texto, descripción, CTA), estado | pertenece a Brief/Campaña; 1–N Variante, Versión | contenido validado por reglas |
| Variante | MVP | alternativa de un Copy (tono, objetivo, A/B) | pertenece a Copy | referencia a copy existente |
| Versión | MVP | instantánea **inmutable** (tipo de entidad, id, número, contenido, hash, motivo, fecha) | de Copy/Variante/Pieza/Adaptación | no se sobrescribe contenido aprobado; número creciente |
| Regla | MVP (copy) / F3 (auditoría) | regla determinista (longitud, palabras obligatorias/prohibidas, formato, CTA…), severidad, ámbito | aplica a Copy/Canal/Pieza | definición validable; bloqueante o advertencia |
| Evento de actividad | MVP | registro local de acciones (para «actividad real» del Command Center) | referencia a cualquier entidad | no contiene contenido sensible del usuario salvo identificadores |
| Pieza creativa | F3 | archivo (binario o referencia), formato, dimensiones, versión | pertenece a Campaña; N–1 Copy | tipo/tamaño permitido (P5) |
| Auditoría | F3 | ejecución de reglas sobre Copy/Pieza (fecha, versión auditada, puntuación, ponderaciones) | 1–N Hallazgo | puntuación calculada de forma determinista y reproducible |
| Hallazgo | F3 | id, elemento afectado, evidencia, categoría, severidad, regla, recomendación, estado, resolución | pertenece a Auditoría | campos obligatorios; estado ∈ flujo |
| Adaptación | F4 | copy fuente → canal, contenido adaptado, reglas de canal, diferencias | de Copy; por Canal | traza al copy fuente y a su versión |
| Canal | F4 | definición del canal (longitud, estructura, formato, tono, CTA, restricciones) | usado por Adaptación/Regla | catálogo de canales aprobados (decisión Q-2) |
| Aprobación | F5 | decisión **humana** (aprobado/rechazado/requiere corrección), motivo, fecha, versión aprobada | de Copy/Pieza/Adaptación | solo el usuario local; sin identidad multiusuario simulada |
| Resultado | F5 | datos de desempeño dados por el usuario (campaña, canal, contenido, fecha, impresiones, clics, conversiones, inversión, ventas) | pertenece a Campaña | origen ∈ manual/importado; no negativos |
| Métrica | F5 | indicador **calculado** a partir de Resultados con fórmula documentada | deriva de Resultado | no se muestra si faltan datos necesarios |
| Biblioteca/Etiqueta | F5 | etiquetas y colecciones para búsqueda y reutilización | N–N con entidades | nombres únicos por ámbito |
| Identidad/Organización/Membresía/Rol | **Futura / no aplica** | entidades de la arquitectura anterior | — | ver P1; no se simulan usuarios |

## Estados propuestos del flujo (a confirmar, Q-3)
Borrador → En revisión → Requiere corrección → Corregido → Aprobado → Archivado; Rechazado como salida alterna. Una transición se registra como Evento; Aprobado exige Aprobación humana explícita.

## Principios de dominio
(1) Las reglas y cálculos son funciones puras y deterministas, con casos de prueba. (2) La IA solo sugiere; ninguna promoción se aprueba por sugerencia de IA. (3) Hallazgos explicables (regla + evidencia). (4) Versiones trazables e inmutables. (5) Datos desconocidos se representan como desconocidos, nunca inventados.
