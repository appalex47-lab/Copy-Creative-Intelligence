# Modelo de datos de CCI (propuesta; nada implementado)
> **ADVERTENCIA DE VIGENCIA (añadida 2026-11-22 tras la revisión de ChatGPT; el contenido original no se altera).** Este documento es **histórico / propuesta anterior** y **no constituye por sí solo el contrato vigente**. Prevalecen, dentro de sus alcances, las decisiones posteriores del propietario D-1, D-2, D-3, D-5, P1, P2, P3 y P4.A registradas en `REGISTRO_DECISIONES_RESUELTAS.md`. Las propuestas de entidades, relaciones, cardinalidades, atributos, reglas, MVP y persistencia **que no hayan sido aprobadas expresamente siguen sin aprobación**. Reglas (D-3): familias de copy, marca, comerciales y canal; **solo ReglaDeMarca y ReglaComercial son entidades independientes**; **no existe una entidad genérica «Regla» vigente**; las reglas de copy no se incluyen automáticamente en ReglaDeMarca. Ver `../00_INDICE_VIGENTES_E_HISTORICOS.md` y `CONTROL_DE_CAMBIOS_CORRECCION_2026-11-22.md`.
Complementa `05_MODELO_DOMINIO_CCI.md` (entidades, relaciones, invariantes) y `07_DISENO_PERSISTENCIA_INDEXEDDB.md` (stores, índices, transacciones). Sujeto a P4, P5, Q-4 (P1 resuelta: sin Organización/Membresía/roles; perfil local opcional).
## Convenciones comunes (**preliminares; P4.5 no aprobada como paquete; ver `CONVENCIONES_P4_5_CONDICIONES.md`**)
`id` UUID v4 (cliente) · `createdAt`/`updatedAt` ISO-8601 UTC · `revision` **no aprobado como requisito obligatorio** (E2 ratificada: solo si un caso de uso demuestra necesidad) · `archivedAt` nullable (borrado lógico) · importes en enteros de unidad menor + `currency` · desconocido = `null`, nunca valor inventado.
## Campos mínimos por entidad MVP (tipos)
| Entidad (store) | Campos propuestos |
|---|---|
| Campaña (`campaigns`) | name:string(1–120) · objective:string · status:enum · validFrom/validTo:date? |
| Producto (`products`) | name:string · sku:string? · basePriceMinor:int≥0? · currency:string? |
| Oferta (`offers`) | campaignId:ref · type:enum · benefit:string · originalPriceMinor:int? · promoPriceMinor:int? · validFrom/validTo:date? · conditions:string? · exclusions:string? |
| Brief (`briefs`) | campaignId:ref · objective · audience · coreMessage · tone · channel · format · cta · offerId:ref? · status |
| Copy (`copies`) | briefId:ref · campaignId:ref · headline? · body? · description? · cta? · status |
| Variante (`variants`) | copyId:ref · label · content · intent:enum(tone/objective/ab) |
| Versión (`versions`) | entityType:enum · entityId:ref · number:int · snapshot:object · hash:string · reason:string · createdAt |
| ReglaDeMarca (`brandRules`) | scope:enum · kind:enum · params:object · severity:enum · enabled:bool |
| ReglaComercial (`commercialRules`, Fase 4) | scope:enum · kind:enum · params:object · tolerancia configurable · severity:enum · enabled:bool |
| Actividad (`activity`) | entityType · entityId · action:enum · createdAt (sin contenido sensible) |
| Configuración (`settings`) | key:string · value:JSON validado |
| Perfil local (clave `profile` en `settings`, **propuesta técnica**) | displayName:string? (opcional; sin identidad autenticada) |
Entidades F3–F5 (pieza, auditoría, hallazgo, canal, adaptación, aprobación, resultado, métrica, etiqueta): campos según `05_MODELO_DOMINIO_CCI.md`; se detallan al iniciar su fase.
## Ejemplo de datos (ilustrativo, no real)
`Oferta{ type:"descuento", originalPriceMinor:10000, promoPriceMinor:8000, currency:"MXN" }` → descuento calculado por código: ((10000−8000)/10000)×100 = 20 %. La moneda de ejemplo no implica decisión del propietario.
## Relaciones (resumen ER)
Campaña 1–N Brief · Campaña 1–N Oferta · Oferta N–N Producto · Brief 1–N Copy · Copy 1–N Variante · Copy/Variante 1–N Versión · cualquier entidad 1–N Actividad.
> **[Alineación 2026-11-22, regularización posterior a B1–B10; no es decisión nueva; el texto anterior se conserva] Estado de cada relación de este resumen frente a P4.B (13 relaciones ratificadas, sin cardinalidades obligatorias):** *Campaña–Brief*: aprobada solo como «Campaña puede ser referenciada por un Brief» (la cardinalidad «1–N» **no** está aprobada). *Campaña–Oferta*: **NO aprobada** (B2). *Oferta–Producto*: **no figura entre las relaciones aprobadas**. *Brief–Copy*: **no figura entre las aprobadas**. *Copy–Variante*: relación aprobada; la cardinalidad no. *Copy–Versión*: relación aprobada; la cardinalidad no. *Variante–Versión*: **no aprobada y contraria a D-2.b** (la Variante no tiene historial de versiones propio por ahora, sin excluirlo a futuro); la expresión «Copy/Variante 1–N Versión» debe leerse solo como Copy–Versión. *Actividad*: «cualquier entidad 1–N Actividad» **no está aprobada** (B2 no aprueba un Evento de actividad con entidades específicas salvo que la especificación del módulo lo justifique). Las referencias de la tabla de campos (`Oferta.campaignId`, `Brief.offerId`, `Copy.briefId`, `Copy.campaignId`) presuponen relaciones no aprobadas. **Ningún campo, tipo ni rango de este documento está aprobado** (P4.C: los atributos se definen en la especificación de cada módulo).
## Validaciones transversales
Referencia existente (verificada en la misma transacción) · fechas validTo ≥ validFrom · promoPrice ≤ originalPrice se **valida y reporta**, no se corrige · esquema validado al importar.
