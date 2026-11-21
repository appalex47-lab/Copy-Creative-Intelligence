# Evidencia de verificación remota (ronda final)

Esquema de punto fijo: `C_content` = commit con el expediente completo (`942a7f66bfd2cb2b2a240c9a79069dc88934c6b8`); los commits siguientes solo agregan este directorio (excluido del manifiesto y comprobado con `--base`).

| Archivo | Qué prueba |
|---|---|
| `viaA_C_content.txt`, `viaA_detalle_C_content.txt` | Vía A (clon fresco, HEAD del clon = `C_content`): 133/133 entradas del manifiesto verificadas, resultado por archivo |
| `viaB_C_content.txt`, `viaB_detalle_C_content.txt` | Vía B (API de GitHub, blobs descargados, REF = `C_content`): 133/133 |
| `viaA_C_evid.txt`, `viaB_C_evid.txt` (+ `_detalle_`) | Vías A y B sobre el HEAD posterior que solo agregó los archivos de arriba, con `--base 942a7f66…` (comprueba que solo cambió este directorio) |
| `linea_base_ronda_final.txt`, `linea_base_inspeccion.txt` | Estado remoto antes de actuar (ronda final y ronda anterior) |
| `historico_commit_6a041cb/`, `historico_commit_182b832/` | Verificaciones HISTÓRICAS de commits anteriores (no vigentes) |

Cada salida incluye fecha UTC y local, comando, HEAD verificado, número de archivos y resultado por archivo (`*_detalle_*`). Comandos:
`python3 -I -B scripts_validacion/ct_manifiesto.py dir <clon>/docs/fase0/cierre_tecnico_fase0 --repo <clon> [--base SHA] [--detalle f]` y
`python3 -I -B scripts_validacion/ct_manifiesto.py api appalex47-lab/Copy-Creative-Intelligence <SHA> [--base SHA] [--detalle f]`.

Limitación del diseño: la verificación del último commit (que contiene su propia predecesora) no puede constar en ese mismo commit; se reporta en el mensaje final y es reproducible con los comandos anteriores y `--base 942a7f66bfd2cb2b2a240c9a79069dc88934c6b8`.
