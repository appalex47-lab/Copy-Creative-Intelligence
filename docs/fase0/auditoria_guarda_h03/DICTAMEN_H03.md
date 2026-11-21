# DICTAMEN H-03 — Guarda DEV/PROD

**DICTAMEN: B — GUARDIA CORRECTA, PENDIENTE DE VALIDACIÓN EN SUPABASE**
(con condición obligatoria: corregir AUD-G1 antes de cualquier operación en CCI-DEV)

Evidencia: 85 pruebas del parche + 25 casos de esta auditoría, en clústeres locales. Identidad sysid+base, denylist precedente, comparación exacta, search_path blindado, listas vacías ⇒ rechaza todo. Sin bypass por variables, search_path, nombre de base, privilegios ni flags de psql.

Limitaciones: (1) hueco real AUD-G1: guarda vacía/truncada deja correr los 6 scripts sin protección (mitigación validada en copia, no incorporada al parche); (2) sin pin de hash (AUD-G2); (3) stdin (AUD-G3); (4) sysid no distingue clones (AG-18); (5) NO verificado en Supabase: ejecución de pg_control_system(), reenvío de PGOPTIONS por pooler, project ref.
No se autoriza ninguna operación en CCI-DEV ni Fase 1. No se aceptó Fase 0. SHA-256 guarda auditada: 598ad606071be717070cd4c3031bfd69184e09059406320c4edf25bc3dfe6f08
