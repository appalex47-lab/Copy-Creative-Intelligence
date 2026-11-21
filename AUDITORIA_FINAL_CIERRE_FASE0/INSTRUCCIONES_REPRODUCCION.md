# Instrucciones de reproducción
1. Clon de la rama `audit/fase0-cierre-definitivo`; PostgreSQL 16 local (nunca Supabase). Crear clúster vacío (`scripts_de_prueba/nuevo_cluster.sh <nombre> <puerto>`; rol superusuario `cci_test`).
2. Batería: `bash docs/fase0/cierre_tecnico_fase0/scripts_validacion/ct_bateria_final.sh <socket> <puerto>` (esperado 22/22).
3. Suites: `bash ct_cierre_suites.sh <socket> <puerto> <salida> <árbol e0b1d81> <árbol d365a16>` (árboles en `evidencia/antes_despues/`); y `python3 -I ct_pruebas_identidad_cierre.py`. Ejecutar en serie.
4. Regenerar SHA256SUMS tras cualquier cambio a los 10 archivos: `generar_sha256sums_cci.sh`.
5. Ejecución verificada: `CCI_DESTINOS_APROBADOS=… ejecutar_script_verificado.sh <sha256 de SHA256SUMS_CCI.txt> <script.sql> …`.
6. Cierre documental: `scripts_de_prueba/aud_cierre_final.sh <cierre_tecnico_fase0>` dentro de un repo git (dos pasadas).
Hashes: SUMS `59c1186992bff6cfc752da6d4e71412de6bc9a53a50c535a9b055142a02f83ab`; guarda `8baba67b25862b59cec6fed978e47c318861b90252fe54786b541c8faae45d3b`; envoltorio `8735b7dbaf1d16bdff1484342dc42476b5d0fa75166d265cdbfab26a6d1b634a`.
