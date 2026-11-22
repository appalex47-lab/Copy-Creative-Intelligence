# Modelo de dominio de CCI

> Documento formal del §14. Fuente de contenido: `../06_MODELO_DE_DOMINIO.md` (sin cambios de fondo). Estado: propuesta para revisión; nada aprobado ni implementado.

Clasificación: **MVP** = imprescindible para el MVP propuesto (fin de Fase 2: Command Center + Copy Studio persistentes) · **F3/F4/F5** = necesaria en esa fase posterior · **Futura** = no necesaria para el alcance vigente. El MVP es **propuesto**, no aprobado (decisión adicional Q-4).
Procedencia del vocabulario (P3 = b): los nombres que coinciden con `docs/fase0/` son referencia conceptual **no vinculante**; ver `INDICE_ANTECEDENTES_HISTORICOS.md`. Nada se incorpora sin aprobación en P4.
Estado de P4 (2026-11-22): **P4.1: lista de nombres confirmada; definiciones, relaciones, atributos y fases NO aprobados**; P4.2 y P4.3 respondidas; **Q-7 = (a)**: Campaña incorporada como entidad nueva (≠ `Project`; F11-D5 íntegra; sus atributos y cardinalidades NO aprobados); P4.5 con posición preliminar (ver `CONVENCIONES_P4_5_CONDICIONES.md`). La entidad Campaña no está aprobada en firme (Q-7); F11-D5 se conserva íntegra.
Convenciones (**preliminares; el paquete NO está aprobado**): `id` UUID v4 generado en cliente; `createdAt`/`updatedAt` ISO-8601 UTC; `revision` entero para control optimista; borrado lógico por `archivedAt`; importes como enteros en unidad menor (centavos) + moneda; ningún dato comercial inventado: un campo desconocido es `null`/ausente, no un valor por defecto.

| Entidad | Clase | Descripción y atributos clave | Relaciones | Invariantes principales |
|---|---|---|---|---|
| Configuración | MVP | claves de preferencias duraderas no ligeras (marca, idioma, canales activos, tolerancias) | — | un registro por clave; valores validados |
| Campaña (**Q-7 = a**: entidad nueva; no equivale a `Project`) | MVP | nombre, objetivo, estado (borrador/en revisión/…), vigencia | 1–N Brief, Copy, Pieza | nombre no vacío; estado dentro del flujo aprobado |
| Producto | MVP | nombre, identificador comercial, precio base (opcional) | N–N Oferta/Brief | precio ≥ 0 si existe |
| Oferta | MVP | tipo, beneficio, precio original/promocional, vigencia, condiciones, exclusiones | pertenece a Campaña; N–N Producto | si hay ambos precios, promocional ≤ original (se **valida**, no se corrige); fechas coherentes |
| Brief | MVP | objetivo, audiencia, mensaje central, tono, canal, formato, CTA, oferta | pertenece a Campaña | campos obligatorios definidos; incompleto = estado explícito |
| Copy | MVP | contenido principal (titular, texto, descripción, CTA), estado | pertenece a Brief/Campaña; 1–N Variante, Versión | contenido validado por reglas |
| Variante | MVP | alternativa de un Copy (tono, objetivo, A/B) | pertenece a Copy | referencia a copy existente |
| Versión | MVP | instantánea **inmutable** (tipo de entidad, id, número, contenido, hash, motivo, fecha) | de Copy/Variante/Pieza/Adaptación | no se sobrescribe contenido aprobado; número creciente |
| ReglaDeMarca | MVP (Fase 2) / F3 | regla determinista de marca y de copy: longitud, palabras obligatorias/prohibidas, tono, CTA, formato; severidad; ámbito (**P4.2 = b**) | aplica a Copy/Pieza | definición validable; bloqueante o advertencia |
| ReglaComercial | F4 | regla determinista comercial: precios, descuento, vigencia, exclusiones, tolerancias configurables (**P4.2 = b**) | aplica a Oferta | cálculos deterministas; datos faltantes se reportan como faltantes |
| Evento de actividad | MVP — **aprobada como entidad propuesta (P4.3)**; estructura y eventos por especificar | registro local de acciones para la «actividad real» del Command Center | referencia a cualquier entidad | sin contenido sensible del usuario; **no implementar hasta especificar** |
| Pieza creativa | F3 | archivo (binario o referencia), formato, dimensiones, versión | pertenece a Campaña; N–1 Copy | tipo/tamaño permitido (P5) |
| Auditoría | F3 | ejecución de reglas sobre Copy/Pieza (fecha, versión auditada, puntuación, ponderaciones) | 1–N Hallazgo | puntuación calculada de forma determinista y reproducible |
| Hallazgo | F3 | id, elemento afectado, evidencia, categoría, severidad, regla, recomendación, estado, resolución | pertenece a Auditoría | campos obligatorios; estado ∈ flujo |
| Adaptación | F4 | copy fuente → canal, contenido adaptado, reglas de canal, diferencias | de Copy; por Canal | traza al copy fuente y a su versión |
| Canal | F4 | definición del canal (longitud, estructura, formato, tono, CTA, restricciones) | usado por Adaptación/Regla | catálogo de canales aprobados (decisión Q-2) |
| Aprobación | F5 | decisión **humana** (aprobado/rechazado/requiere corrección), motivo, fecha, versión aprobada | de Copy/Pieza/Adaptación | la acción la realiza el usuario local único (sin aprobadores distintos simulados; P1) |
| Resultado | F5 | datos de desempeño dados por el usuario (campaña, canal, contenido, fecha, impresiones, clics, conversiones, inversión, ventas) | pertenece a Campaña | origen ∈ manual/importado; no negativos |
| Métrica | F5 | indicador **calculado** a partir de Resultados con fórmula documentada | deriva de Resultado | no se muestra si faltan datos necesarios |
| Etiqueta | MVP — **aprobada (P4.3)** | etiquetas para etiquetar y buscar contenido en Copy Studio | N–N con Copy/Variante/otras | nombres únicos por ámbito |
| Colección | **PENDIENTE (P4.3); no forma parte del modelo** | sin justificación funcional frente a etiquetas y filtros | — | no se aprueba como entidad independiente hasta justificarla |
| Identidad/Organización/Membresía/Rol | **No aplica (P1 = b, 2026-11-22)** | entidades de la arquitectura anterior; excluidas del dominio operativo, también como etiquetas de autorización | — | no se simulan usuarios; `Membership.active` sin aplicación |
| Perfil local (opcional) | MVP — **aprobado (P4.3, conforme a P1)** | `displayName` opcional; **sin autenticación ni identidad de usuario** | — | puede no existir; longitud máxima por definir (propuesta mía) |

## Estados propuestos del flujo (a confirmar, Q-3)
Borrador → En revisión → Requiere corrección → Corregido → Aprobado → Archivado; Rechazado como salida alterna. Una transición se registra como Evento; Aprobado exige Aprobación humana explícita.

## Principios de dominio
(1) Las reglas y cálculos son funciones puras y deterministas, con casos de prueba. (2) La IA solo sugiere; ninguna promoción se aprueba por sugerencia de IA. (3) Hallazgos explicables (regla + evidencia). (4) Versiones trazables e inmutables. (5) Datos desconocidos se representan como desconocidos, nunca inventados.
