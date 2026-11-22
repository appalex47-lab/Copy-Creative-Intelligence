# 04 — Identificadores: permisos, funciones, etiquetas, claves de rol, claves de prompt

**Validado contra un diseño no aprobado.** Solo se presentan correspondencias respaldadas literalmente por una fuente; la fuente se cita. No se infiere ninguna relación permiso→rol.

## A. Claves de permiso (17) — F2 l.534–535 (v3.3, «PROPUESTA T-01», NO APROBADA en F2)
`content.read`, `comment.write`, `audit.run`, `campaign.write`, `copy.write`, `channel.adapt`, `metrics.write`, `promotion.write`, `asset.upload`, `piece.review`, `piece.approve`, `finding.confirm`, `finding.dismiss`, `piece.publish`, `piece.archive`, `org.manage`, `block.exception.grant` = 17 distintas.
- F3 l.34, l.125, l.3698: «17 claves físicas», marcadas como aprobadas/vigentes. **T-01/T-02 siguen sin resolver: F2 NO APROBADA; F3 APROBADOS.**
- Capacidades conceptuales, **no claves físicas** (F3 l.3698): `delegation.manage`, `block.exception.revoke`.

### Texto literal de F2 sobre qué roles tienen cada permiso (única fuente; no cotejada con otra)
> `content.read`, `comment.write`, `audit.run` (todos los roles); `campaign.write`, `copy.write`, `channel.adapt`, `metrics.write` (Admin, Ecommerce, Marketing; `promotion.write`: Admin, Ecommerce); `asset.upload` (Admin, Diseño, Marketing); `piece.review`, `piece.approve`, `finding.confirm`, `finding.dismiss` (solo Revisor / Aprobador); `piece.publish` (Admin, Ecommerce, Marketing); `piece.archive` (Admin, Revisor); `org.manage` (solo Admin); `block.exception.grant` (ningún rol: concesión por persona por alguien con `org.manage`). Admin no aprueba por defecto.

Reservas (sin resolver): la redacción agrupa varias claves en un mismo paréntesis y usa **etiquetas** («Revisor / Aprobador», «Revisor», «Diseño»), no las claves del enum; `piece.archive` dice «Revisor», no «Revisor / Aprobador». No tradujo a claves ni deduzco la intención. `membership_permission_grants` concede permisos por persona (F2 tabla de modelo); no se cotejó con F3.

## B. Claves de rol — F2 l.952 (sección de modelo de datos)
`memberships.roles` = «arreglo no vacío del enum» `admin`, `ecommerce`, `diseno`, `marketing`, `revisor_aprobador`; D-04 (l.745): «Cinco roles (Admin, Ecommerce, Diseño, Marketing, Revisor / Aprobador)… `memberships.roles` es un arreglo».
- **Clave (enum):** `admin`, `ecommerce`, `diseno`, `marketing`, `revisor_aprobador`.
- **Etiqueta:** Admin, Ecommerce, Diseño, Marketing, Revisor / Aprobador (y «Revisor» abreviado en `piece.archive`).
- **Código actual:** `admin`, `ecommerce`, `design`, `marketing`, `reviewer`.
- **Corrección al expediente original:** allí se dijo que `diseno` y `revisor_aprobador` provenían «de una sola línea (l.424)» y «podrían ser etiquetas»; F2 los define como **valores de enum** en l.952. (El enum sigue sin aprobación formal propia más allá de D-04 «APROBADA», que cita «cinco roles» y no las claves.)
- F3 usa «reviewer» solo en prosa y nombres de evento (`reviewer.assigned`); no como clave de rol.

## C. Nombres de funciones (no son permisos)
F2 menciona, entre otras, `has_permission` (4 veces), `is_member`, `record_approval`, `review_finding`, `transition_piece_status`, `consume_ai_quota`, `verify_assets_integrity`. F3 añade `eligible_evaluators`, `resolve_attribution_discard`. Son funciones/RLS; no se usan como claves de permiso.

## D. Claves de prompt versionado (no son permisos) — F2 l.1157
«Prompts versionados (clave y tarea): `copy.generate`, `copy.analyze`, `copy.compare`, `audit.text`, `audit.image`, `channel.adapt`, `promo.explain`.»
- Resuelve la duda del expediente original: `audit.text`, `audit.image`, `copy.analyze`, `copy.compare`, `copy.generate` son **claves de prompt**, no permisos.
- **Colisión de nombre registrada:** `channel.adapt` aparece **a la vez** como clave de permiso (A) y como clave de prompt (D). Son espacios de nombres distintos según el contexto; ninguna fuente leída declara su separación. No se resuelve.

## E. Otros identificadores que no son claves de permiso
`impact.evaluated`, `reviewer.assigned`, `classification.event` (eventos de `activity_logs`, F3 l.2709).
