# Evidencia de verificación remota (commit de contenido `6a041cb9ca7cbd4bcc41a9eed43c9e51a1c2716f`)

Fecha: 2026-11-21 (UTC). Archivos: 119 entradas del manifiesto verificadas al 100 % (123 archivos en el árbol; 4 exclusiones declaradas: el manifiesto y los 3 archivos de este directorio al momento de verificar).

Comandos:
- Vía A: `git clone --branch audit/cierre-tecnico-fase0 <repo>` en directorio nuevo; `python3 -I -B scripts_validacion/ct_manifiesto.py dir <clon>/docs/fase0/cierre_tecnico_fase0 --repo <clon> --detalle viaA_detalle_C_content.txt` (HEAD del clon = commit de contenido).
- Vía B: `python3 -I -B scripts_validacion/ct_manifiesto.py api appalex47-lab/Copy-Creative-Intelligence 6a041cb9ca7cbd4bcc41a9eed43c9e51a1c2716f --detalle viaB_detalle_C_content.txt` (blobs descargados por la API).
- Salidas: `viaA_C_content.txt`, `viaB_C_content.txt` y sus `*_detalle_*` (resultado por archivo).

Verificación del HEAD final (commit posterior que solo agrega este directorio): se repite A y B con `--base 6a041cb9…`; su resultado no puede constar en el propio commit y se reporta en el mensaje final; es reproducible con los mismos comandos más `--base 6a041cb9ca7cbd4bcc41a9eed43c9e51a1c2716f`.
