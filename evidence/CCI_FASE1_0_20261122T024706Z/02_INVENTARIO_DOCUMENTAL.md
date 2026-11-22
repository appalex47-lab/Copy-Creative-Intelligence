# Inventario documental (preservado, sin cambios)
- Archivos versionados: 2214 (1485 en `docs/fase0`).
- `docs/fase0/`: especificación técnica G1/G5/G10, estado documental vigente, registro histórico, reportes de publicación V23–V26, expedientes V16–V26, `cierre_tecnico_fase0/` (informe de decisiones arquitectónicas, matrices de trazabilidad/limitaciones/modelo lógico-físico, scripts de validación, paquete solo lectura CCI-DEV, informe de acceso CCI-DEV), `herramientas/`, `historico/`, `revision_independiente/`.
- Raíz: `AUDITORIA_FINAL_*` (varios expedientes y zips), `ARTEFACTOS_REVISION_PUBLICACION/`.
- `evidencia/` (no versionado, 31 archivos): FASE0_PG17_RUN_20261122T021332Z, FASE0_PG17_CONTAINER_PRECHECK_20261122T021534Z, AUDITORIA_ARQUITECTURA_CCI_20261122T022450Z.
- Coexistencia: `docs/fase0` se queda donde está; `docs/architecture|decisions|roadmap|product` son nuevas. `evidencia/` (Fase 0) y `evidence/` (app) conviven. Referencias internas no se reubicaron (no hubo movimientos).
- Verificación: `git diff --name-only` = solo `README.md`; 0 eliminaciones.
