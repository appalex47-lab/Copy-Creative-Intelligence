# Índice de antecedentes históricos y referencia conceptual (P3 = b)
Todos los materiales de esta tabla se conservan **íntegros e intactos** en el repositorio y no se modifican. Este índice es un documento nuevo del expediente. Verificado sobre el commit `ffb47bc319db0806250bcecf91d390fa59fa0d70` (solo lectura).
## 1. Dos categorías (no se mezclan)
- **Antecedente histórico:** consta como parte de la historia del proyecto; no vincula a la arquitectura vigente.
- **Referencia conceptual no vinculante:** puede consultarse solo por **conceptos y vocabulario**; **nada se incorpora automáticamente**. Cada concepto que se quiera recuperar se evalúa en **P4** y se somete a aprobación del propietario cuando corresponda.
## 2. Materiales
| Material | Contenido | Antecedente histórico | Referencia conceptual (solo vocabulario) |
|---|---|---|---|
| `docs/fase0/` (59 archivos: 5 principales + 52 `historico/` + 2 `herramientas/`) | diseño de servidor (41 tablas, 231 reglas, 780 escenarios, 17 permisos) | Sí | Sí |
| `evidence/CCI_*` (11 expedientes) y `evidence/public/` | evidencia de Fases 1.0–1.1 y revisiones | Sí | Sí (cuando mencionan los conceptos de la lista §3) |
| `docs/architecture/INTEGRACION_SUPABASE_ESTADO.md` | estado de la integración Supabase (no integrada) | Sí | No |
| `supabase/README.md`, `database/README.md` | espacios reservados para el backend | Sí | No |
| `docs/decisions/DECISIONES.md`, `ARQUITECTURA.md` (partes reemplazadas por el ADR propuesto) | textos originales | Sí (partes reemplazadas) | No |
## 3. Conceptos consultables (vocabulario) y su posible entidad en `05_MODELO_DOMINIO_CCI.md`
Nombres de la especificación verificados por búsqueda; su existencia no implica que apliquen.
| Concepto en el material histórico | Candidata browser-only (P4) | Verificación |
|---|---|---|
| `campaigns` | Campaña (sujeta a Q-7) | nombre listado en la especificación («reutilizable sin cambio») |
| `creative_pieces`, `creative_assets` | Pieza creativa | citados en la especificación |
| `copy_versions`, `briefs`, `brief_versions` | Versión / Copy / Brief | citados en la especificación |
| `approvals` | Aprobación | citado en la especificación |
| `activity_logs` | Evento de actividad | citado en la especificación |
| `audits`, `audit_findings`, `performance_metrics`, `promotion_rules`, `brand_guidelines` | Auditoría, Hallazgo, Métrica, Regla | listados como «reutilizables» en la especificación |
Sin equivalente claro por nombre: Producto y Oferta (`products`/`offers` no aparecen; `promotion_snapshots`/`promotion_rules` podrían relacionarse: **no verificado**).
## 4. Excluido: sin aprobación y fuera de la arquitectura vigente
Los **17 permisos** (T-01/T-02, F11-D4), **RLS**, **SQL**, **disparadores**, **restricciones de base de datos**, claves foráneas compuestas, `organizations`, `profiles`, `memberships`, `role_permissions`, `membership_permission_grants` y la **arquitectura multiusuario**. No se aprueban ni se consultan como modelo.
## 5. Contradicciones que permanecen **abiertas** (P3 no las resuelve ni modifica)
- **C-2:** estado de la Fase 0 v3.3 (su encabezado dice «NO está aceptada»; el informe de cierre dice «aceptada como línea base documental, con limitaciones»; otro documento dice «NO ACEPTADA»; no se localizó una aceptación posterior).
- **C-3:** D-04 «APROBADA» (cinco roles) sin aprobación propia localizada para el enum con claves concretas.
Fuente: `evidence/CCI_FASE1_1_A1_20261122T033450Z/05_CORRECCIONES_Y_CONTRADICCIONES.md`; F11-D9 las mantiene abiertas.
