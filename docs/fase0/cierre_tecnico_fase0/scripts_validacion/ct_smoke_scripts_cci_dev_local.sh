#!/bin/bash
# Uso: ct_smoke_scripts_cci_dev_local.sh <socket> <puerto> [directorio_salida]. PostgreSQL TEMPORAL LOCAL. Ejecuta los 6 scripts de cci_dev_NO_EJECUTADOS SOLO como smoke local
# (modo SI-LOCAL-TEMPORAL), contra bases locales cci_*; esto NO es validación de CCI-DEV ni de Supabase. Verifica guardas, sintaxis y que los resultados defectuosos den FAIL/BLOCKED.
set -u; export PGHOST="$1" PGPORT="$2" PGUSER=cci_test; D="$(cd "$(dirname "$0")" && pwd)"; O="${3:-$D/resultados}"; S="$D/cci_dev_NO_EJECUTADOS"; mkdir -p "$O"
export CCI_DIR="$S" CCI_GUARDA_SHA256_APROBADO="$(sha256sum "$S/00_guarda_destino.sql" | cut -d' ' -f1)"   # raíz de confianza simulada: en producción lo aporta el propietario fuera del repo
L="-c cci.validacion_autorizada=SI-LOCAL-TEMPORAL -c cci.entorno=LOCAL-TEMPORAL"; U=00000000-0000-0000-0000-0000000000
run() { PGOPTIONS="$L" psql -v ON_ERROR_STOP=1 -P pager=off "$@" 2>&1; }
# 0) guarda: sin autorización cada script debe abortar con NO EJECUTADO
for f in 01_inventario_esquema_SOLO_LECTURA 02_rls_privilegios_SOLO_LECTURA 03_pruebas_rls_ROLLBACK 04_trigger_r1_r9_ROLLBACK 05_concurrencia_sesion_A 05_concurrencia_sesion_B; do
  r=$(PGOPTIONS="" psql -d postgres -v ON_ERROR_STOP=1 -v org=x -v org_a=x -v org_b=x -v uid_a=x -v uid_x=x -v piece=x -v attr=x -f "$S/$f.sql" 2>&1 | grep -c "NO EJECUTADO"); echo "GUARDA $f sin autorizacion -> abortado: $([ "$r" -ge 1 ] && echo SI || echo NO)"; done > "$O/smoke_guardas.txt"
# guarda con autorización pero base/entorno incorrectos (postgres no empieza por cci_)
r=$(PGOPTIONS="$L" psql -d postgres -v ON_ERROR_STOP=1 -f "$S/01_inventario_esquema_SOLO_LECTURA.sql" 2>&1 | grep -c "NO EJECUTADO"); echo "GUARDA 01 en base 'postgres' (no cci_) con modo local -> abortado: $([ "$r" -ge 1 ] && echo SI || echo NO)" >> "$O/smoke_guardas.txt"
# 1-2) inventarios sobre la base local de la extensión (cci_ct_ext)
run -d cci_ct_ext -f "$S/01_inventario_esquema_SOLO_LECTURA.sql" > "$O/smoke_01_inventario.txt"; echo "01 rc=$?" >> "$O/smoke_codigos.txt"
run -d cci_ct_ext -f "$S/02_rls_privilegios_SOLO_LECTURA.sql" > "$O/smoke_02_rls_inventario.txt"; echo "02 rc=$?" >> "$O/smoke_codigos.txt"
# 3) RLS sobre el shim: defectuoso => FAIL esperado; corregido => PASS esperado
for v in defectuosa corregida; do
  PGOPTIONS="$L" psql -d postgres -qAtc "drop database if exists cci_shim" -c "create database cci_shim" >/dev/null
  run -d cci_shim -q -v variante=$v -f "$D/local_ext/30_shim_rls_fixture_LOCAL.sql" > /dev/null
  run -d cci_shim -v org_a=a0000000-0000-0000-0000-000000000001 -v org_b=a0000000-0000-0000-0000-000000000002 -v uid_a=a0000000-0000-0000-0000-0000000000a1 -v uid_x=a0000000-0000-0000-0000-0000000000c1 -f "$S/03_pruebas_rls_ROLLBACK.sql" > "$O/smoke_03_rls_shim_$v.txt"; echo "03-$v rc=$?" >> "$O/smoke_codigos.txt"
done
# 4) R1-R9 sobre cci_ct_ext (no hay implementación): debe quedar BLOQUEADO
run -d cci_ct_ext -v org=${U}01 -v attr=${U}02 -v affected=${U}03 -v requester=${U}04 -v change_actor=${U}05 -v r_ok=${U}06 -v r_nomember=${U}07 -v r_noreview=${U}08 -v r_direct=${U}09 -v r_inherited=${U}10 -v r_othersrc=${U}11 -v r_benef=${U}12 -f "$S/04_trigger_r1_r9_ROLLBACK.sql" > "$O/04_r1r9_local_bloqueado.txt"; echo "04 rc=$?" >> "$O/smoke_codigos.txt"
# 5) concurrencia A/B sobre un smoke local
PGOPTIONS="$L" psql -d postgres -qAtc "drop database if exists cci_conc_smoke" -c "create database cci_conc_smoke" >/dev/null
run -d cci_conc_smoke -q -f "$D/local_ext/31_conc_smoke_fixture_LOCAL.sql" >/dev/null
P=(-v org=${U}01 -v piece=${U}02 -v reviewer_a=${U}0a -v reviewer_b=${U}0b)
( run -d cci_conc_smoke "${P[@]}" -f "$S/05_concurrencia_sesion_A.sql" > "$O/smoke_05_sesion_A.txt" ) & sleep 1.5
run -d cci_conc_smoke "${P[@]}" -f "$S/05_concurrencia_sesion_B.sql" > "$O/smoke_05_sesion_B.txt"; wait
echo "05 rc=$?" >> "$O/smoke_codigos.txt"
echo "05 sin tabla (BLOCKED esperado):" > "$O/smoke_05_sin_tabla.txt"; run -d cci_ct_ext "${P[@]}" -f "$S/05_concurrencia_sesion_B.sql" >> "$O/smoke_05_sin_tabla.txt"
