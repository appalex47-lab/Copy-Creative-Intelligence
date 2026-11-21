# Auditoría independiente de la guarda DEV/PROD (H-03) — estado VIGENTE
**Sustituye** a la versión de `historico_pre_auditoria_final/` (histórica). Detalle completo en `AUDITORIA_FINAL_INDEPENDIENTE_FASE0/AUDITORIA_TECNICA_GUARDA_H03.md`.
SHA-256 vigente de `00_guarda_destino.sql`: `b30a39d9d6dac4974913bf7140a619d1991b599a0c0d12af504f9af0906eb1ec`.
| Hallazgo | Estado vigente |
|---|---|
| AUD-G1 guarda vacía/truncada ⇒ scripts sin guarda | **CORREGIDO y probado localmente** (marcador de ejecución completa; INT-02…05, GD-13) |
| AUD-G2 pin de integridad de la guarda | **PARCIAL**: control técnico opcional `ejecutar_script_verificado.sh` con hash aprobado FUERA del repo; no es obligatorio (invocar `psql` directo lo omite). Un hash dentro del repo no es independiente |
| AUD-G3 ejecución por stdin | **PARCIAL**: guarda homónima vacía en el cwd ⇒ rechazo (X-06); guarda homónima que forja el marcador ⇒ pasa en 01/02 (X-07). stdin no soportado |
| AUD-FINAL-01 search_path no persiste tras el bloque DO | **CORREGIDO** calificando con `pg_catalog.` las funciones de los scripts (GD-19, hijack PRE/POST); el search_path de la guarda sigue siendo local a su bloque (por diseño) |
| AUD-FINAL-02 marcador preinstalable por PGOPTIONS | **CORREGIDO** (tabla temporal; X-10, GD-16) |
| Clon/restauración (AG-18) | **LIMITACIÓN ESTRUCTURAL** (ID-06 = PARTIAL, no aprobación) |
| Compatibilidad Supabase | **NO VERIFICADA** |
