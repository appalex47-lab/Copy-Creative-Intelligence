# Cómo reproducir las pruebas (sólo PostgreSQL local; nunca Supabase/CCI-DEV/CCI-PROD)
Requisitos: PostgreSQL 16 (initdb/pg_ctl/psql), Python 3, bash, git. Ejecutar como usuario no root que pueda lanzar PostgreSQL (aquí se usó `su postgres -c`).
1. Clonar la rama `audit/fase0-remediaciones-h01-h02-h03`; `cd docs/fase0/cierre_tecnico_fase0/scripts_validacion`.
2. Crear un clúster **vacío** (sin roles anon/authenticated/service_role): ver `evidencia/nuevo_cluster.sh <nombre> <puerto>` (socket Unix, rol local `cci_test`).
3. `bash ct_bateria_final.sh <ruta_socket> <puerto>` → 22 pasos; resultado en `resultados/bateria_final/INDICE_BATERIA.csv`. **Ejecutar en serie**: dos baterías simultáneas en árboles distintos interfirieron (el paso `exc_modelo14` falló); se repitieron en serie y dieron 22/22 (`evidencia/` conserva sólo las corridas válidas).
4. Pruebas de la guarda por separado: `python3 -I -B ct_pruebas_guarda_destino.py <socket> <puerto> salida.txt` (109 pruebas).
5. Post-batería (dos pasadas, ver `evidencia/aud_cierre_final.sh <dir cierre_tecnico_fase0>`): cifras, manifiesto (`ct_manifiesto.py gen/dir`), reconciliación (58 controles), consistencia (`ct_verificar_consistencia_informe.py verificar|controles`).
6. Segundo clúster limpio + comparación: `evidencia/aud_comparar_clusteres.py <arbolA> <arbolB> salida.txt` (30 comparaciones).
7. Casos de hueco de la guarda: `evidencia/aud_huecos_guarda.py` (ajustar socket/puerto/ruta al inicio del archivo).
8. Integridad independiente: `evidencia/aud_integridad.py <clon> salida.json`.
Todas las pruebas con identidad simulada usan system_identifier **locales y desechables**; no hay identificadores reales de CCI-DEV/CCI-PROD en el repositorio.
