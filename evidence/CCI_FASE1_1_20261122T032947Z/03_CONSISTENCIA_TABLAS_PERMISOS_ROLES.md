# 03 — Consistencia documental: 27 tablas, 41 tablas, 17 permisos, 5 roles

Verificación por script sobre el texto de F2, F3 y F4 (`docs/fase0`, solo lectura). **Validado contra diseño no aprobado.**

## 1. Tablas base (27) vs matriz (41)
- F3 §9 enumera 22 «reutilizables sin cambio» + 5 «con cambio» (`creative_pieces`, `copy_versions`, `channel_rules`, `creative_assets`, `approvals`) = **27 nombres distintos**.
- F4 §5 enumera 41 filas numeradas. Las filas 1–27 son exactamente esos 27 nombres (diferencia de conjuntos: vacía en ambos sentidos). Las filas 28–41 son 14 nombres nuevos, ninguno en las 27.
- Las 14 nuevas (F4): `piece_classification_events`, `piece_reviewer_assignments`, `impact_evaluations`, `publication_attempts`, `channel_formats`, `brief_versions`, `contribution_events`, `copy_version_provenance`, `promotion_snapshots`, `brief_field_changes`, `brief_field_attributions`, `promotion_field_changes`, `promotion_field_attributions`, `attribution_discard_resolutions`. F3 l.36 las enumera con «las cuatro tablas de cambio y atribución» agrupadas; el recuento 14 coincide.
- F2 §4 numera las 27 (l.576–603) y declara «27 tablas, ninguna agregada ni eliminada».
- **Resultado: COINCIDE (27 + 14 = 41) en nombres y cifras.**
- **Limitación:** se verificó la correspondencia de **nombres y cifras**, no las columnas. F3 RR-33 reconoce que «las columnas exactas v3.3 no define». Para `profiles`, `organizations` y `memberships` no hay columnas definidas en la especificación; solo el fixture (11 tablas, parcial) aporta `id`, `org`, `user`, `activo`.
- Dato de la propia matriz F4: 11 de 41 tablas con reflejo en el fixture, 2 con prototipo local, **28 sin prueba alguna**.

## 2. Permisos (17)
- F2 (l.534–535) enumera: `content.read`, `comment.write`, `audit.run`, `campaign.write`, `copy.write`, `channel.adapt`, `metrics.write`, `promotion.write`, `asset.upload`, `piece.review`, `piece.approve`, `finding.confirm`, `finding.dismiss`, `piece.publish`, `piece.archive`, `org.manage`, `block.exception.grant` = **17 distintas**.
- Aparecen nominalmente en F2 las 17. En F3 aparecen 8 de las 17 por nombre (el resto no se cita porque no se modifican). F3 menciona además `block.exception.revoke` y `delegation.manage` como «capacidades conceptuales» (no son claves físicas, F3 l.3698).
- **DISCREPANCIA documental registrada (PENDIENTE_DE_DECISIÓN):** F3 l.34 declara «27 tablas; 17 claves físicas; T-02 con 13 transiciones — APROBADOS / vigentes», mientras F2 declara T-01 (matriz de 17 permisos) y T-02 «NO APROBADA». No se encontró en lo leído una fuente que registre la aprobación posterior de T-01/T-02. No la resuelvo: **el propietario debe indicar si T-01 y T-02 fueron aprobadas y dónde consta.**
- **No verificado:** correspondencia de roles por permiso entre documentos más allá de F2 (la matriz permiso→rol solo se leyó en F2). F2 incluye además cadenas tipo `audit.image`, `audit.text`, `copy.analyze`, `copy.compare`, `copy.generate` que no están entre las 17; no verifiqué si son nombres de función/módulo o permisos.

## 3. Cifra de «13 transiciones» (T-02)
No fue objeto de verificación (no afecta a los contratos de 1.0). Solo se anota su estado contradictorio de aprobación (ver §2).

## 4. Roles (5)
- F2 l.424: «5 roles (**admin, ecommerce, diseno, marketing, revisor_aprobador**)»; en la matriz de permisos: Admin, Ecommerce, Marketing, Diseño, **Revisor / Aprobador**.
- F3: no define las claves; usa «reviewer» solo en prosa/eventos (`reviewer.assigned`).
- Código actual (`MembershipRole`): `admin`, `ecommerce`, **`design`**, `marketing`, **`reviewer`**.
- **DISCREPANCIA:** 2 de 5 claves difieren (`design` ≠ `diseno`; `reviewer` ≠ `revisor_aprobador`). F2 tampoco establece que `diseno` y `revisor_aprobador` sean los **identificadores físicos** definitivos (podrían ser etiquetas). Decisión necesaria: identificador canónico y si se mantiene en español/sin tilde.
- Cifra «5 roles»: COINCIDE en F2, F3 y el código.
