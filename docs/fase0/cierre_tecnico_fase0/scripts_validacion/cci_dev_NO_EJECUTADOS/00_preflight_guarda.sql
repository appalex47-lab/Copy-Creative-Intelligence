-- ====================================================================================================
-- 00_preflight_guarda.sql — INTEGRIDAD EXTERNA DE LA GUARDA + EJECUCIÓN DE LA COPIA VERIFICADA (cierre definitivo, AUD-CIERRE-01/02).
-- Lo incluyen los 6 scripts con \ir (nunca solo). Antes de ejecutar CUALQUIER SQL: (1) exige el entorno CCI_DIR (directorio de la guarda) y
-- CCI_GUARDA_SHA256_APROBADO (SHA-256 aprobado por el propietario FUERA del repositorio); (2) copia la guarda a un directorio privado (mktemp -d, 0700) y calcula el
-- hash DE LA COPIA; (3) solo si coincide con el aprobado ejecuta ESA COPIA con \i (así no hay ventana entre comprobar y usar: lo que se hashea es lo que se ejecuta).
-- Ausente/vacío/truncado/alterado/sin hash/sin directorio => 'NO EJECUTADO [G-GUARDA-INTEGRIDAD]'. Sólo meta-comandos de psql y shell: no hay SQL (ni operadores
-- ni funciones resolubles por search_path) hasta que la guarda verificada toma el control.
-- LÍMITE: este archivo, el verificador y los scripts se resuelven con \ir (relativo al script); si un atacante los sustituye, sólo ejecutar_script_verificado.sh
-- (hash externo de TODO el conjunto) lo detecta. El hash externo sólo vale si lo custodia alguien distinto de quien edita el repositorio (pendiente de configuración).
-- ====================================================================================================
\if :{?cci_script}
\else
do $x$ begin raise exception 'NO EJECUTADO [G-GUARDA-NO-EJECUTADA] el script no declaró su identidad (cci_script)'; end $x$;
\endif
\unset cci_run
\set cci_g_ok false
\set cci_tmp `mktemp -d "${CCI_TMPDIR:-${TMPDIR:-/tmp}}/cci.XXXXXX" 2>/dev/null`
\set cci_g_ok `h=$(cp -- "$CCI_DIR/00_guarda_destino.sql" ":cci_tmp/g.sql" 2>/dev/null && chmod 400 ":cci_tmp/g.sql" && sha256sum < ":cci_tmp/g.sql" | cut -d' ' -f1); if [ -n "$h" ] && [ -n "$CCI_GUARDA_SHA256_APROBADO" ] && [ "$h" = "$CCI_GUARDA_SHA256_APROBADO" ]; then echo true; else echo false; fi`
\if :cci_g_ok
\else
\set cci_rm `rm -rf -- ":cci_tmp"`
do $x$ begin raise exception 'NO EJECUTADO [G-GUARDA-INTEGRIDAD] la guarda no existe, está vacía/alterada o falta CCI_DIR/CCI_GUARDA_SHA256_APROBADO'; end $x$;
\endif
\i :cci_tmp/g.sql
\set cci_rm `rm -rf -- ":cci_tmp"`
\unset cci_tmp
\unset cci_g_ok
\unset cci_rm
