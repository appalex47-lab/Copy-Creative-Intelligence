# Instrucciones de reproducción (sólo PostgreSQL local; nunca Supabase/CCI-DEV/CCI-PROD)
Requisitos: PostgreSQL 16 (initdb/pg_ctl/psql), Python 3, bash, git, un usuario no-root para PostgreSQL.
1. Clonar `appalex47-lab/Copy-Creative-Intelligence` rama `audit/fase0-remediaciones-h01-h02-h03` (HEAD d365a16) → es la **rama publicada**. Para el árbol **corregido** aplicar `DIFF_CORRECCIONES_LOCALES.patch` (`git apply`) y, para los resultados, `evidencia/PARCHE_COMPLETO_con_resultados_regenerados.patch` (opcional).
2. Clúster limpio: `evidencia/herramientas/nuevo_cluster.sh <nombre> <puerto>` (ajustar rutas /tmp/aud al entorno).
3. Batería: `bash docs/fase0/cierre_tecnico_fase0/scripts_validacion/ct_bateria_final.sh <socket> <puerto>` — **en serie**, un clúster nuevo por corrida.
4. Guarda: `python3 -I -B ct_pruebas_guarda_destino.py <socket> <puerto> salida.txt` (139 pruebas en el árbol corregido; 109 en la rama publicada).
5. Matrices: `python3 -I -B evidencia/herramientas/aud2_matrices.py <dir cci_dev_NO_EJECUTADOS> <temp|guc> <etiqueta> <sockC1> <puertoC1> <sockC2> <puertoC2> salida.json` (C1 y C2 = dos clústeres distintos; `temp` para el árbol corregido, `guc` para d365a16). `hijack.py` y `persist.py` ídem.
6. Cierre documental (dos pasadas) y verificación: `evidencia/herramientas/aud_cierre_final.sh <dir cierre_tecnico_fase0>` dentro de un clon git (la reconciliación contrasta contra V26 con git); luego `aud_integridad.py`, `aud_consistencia.py`, `aud_comparar_clusteres.py`.
Uso operativo de la guarda: sólo con `-f` y ruta absoluta o con `ejecutar_script_verificado.sh <sha256_aprobado_externo> <script>`.
