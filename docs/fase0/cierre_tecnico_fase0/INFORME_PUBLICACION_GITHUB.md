# INFORME DE PUBLICACIÓN EN GITHUB (protocolo estático)

Repositorio: `appalex47-lab/Copy-Creative-Intelligence` · Rama única autorizada: `audit/cierre-tecnico-fase0`.
Publicación exclusivamente para revisión independiente: no implica aprobación, aceptación, fusión ni autorización de la siguiente fase. Sin PR, sin merge, sin `force push`.

Este documento es **estático**: no contiene SHAs de HEAD ni resultados de verificación del commit que lo contiene (no pueden constar en su propio contenido). Los resultados viven en `evidencia_verificacion/` y en el mensaje final.

## Línea base y commits previos
- `main` = `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`; V26 = `439777c9ea7db464fe49299adfeb2112abfd285c` (sin cambios).
- Historial previo: `e6caebf` (primera publicación), `182b832` (corrección final), `490db22`, `51ebb72` (HEAD previo a la ronda actual). Verificaciones históricas de 182b832: `evidencia_verificacion/historico_commit_182b832/`.
- Línea base de esta ronda: `evidencia_verificacion/linea_base_inspeccion.txt`.

## Evidencia de la ronda actual
`evidencia_verificacion/` (vía A, vía B, comandos, SHA, fecha, archivos y resultado por archivo) — ver `INFORME_HASHES_MANIFIESTO.md` para el diseño de punto fijo.

## Documentos de control de esta ronda
`RESOLUCION_OBSERVACIONES_FINALES.md` (causa del 51/51 con FAIL=1 y las cuatro referencias), `INFORME_RECONCILIACION_INTEGRAL.md` (generado junto con su JSON y TXT), `INFORME_CIFRAS_DEFINITIVAS.md`, `INFORME_AUDITORIA_FECHAS_HORAS.md`, `INFORME_PRUEBAS_FINALES.md`. Los commits y HEAD de esta ronda constan en `evidencia_verificacion/` y en `git log` de la rama (no pueden constar en este archivo).

## Alcance
Solo archivos bajo `docs/fase0/cierre_tecnico_fase0/`. CCI-DEV, CCI-PROD y Supabase no se tocaron. El SHA-256 prueba identidad de archivos, no corrección de contenido.
