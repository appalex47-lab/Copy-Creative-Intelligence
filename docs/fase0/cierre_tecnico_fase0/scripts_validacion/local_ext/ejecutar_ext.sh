#!/bin/bash
# Uso: ejecutar_ext.sh <directorio_socket> <puerto>. Clúster PostgreSQL TEMPORAL LOCAL (nunca Supabase). Carga el fixture V20 sin modificar + la extensión.
set -e; export PGHOST="$1" PGPORT="$2" PGUSER=cci_test; D="$(dirname "$0")"
B="${3:-$D/../../../expediente_final_v26/V25_copia_integra/03_SCRIPTS/PE_POSTGRESQL_V20}"
psql -d postgres -qAtc "drop database if exists cci_ct_ext" -c "create database cci_ct_ext"
psql -d cci_ct_ext -q -v ON_ERROR_STOP=1 -f "$B/01_fixture.sql" -f "$D/10_ext_fixture.sql" -f "$D/11_ext_pruebas.sql" -f "$D/12_ext2_fixture.sql" -f "$D/13_ext2_pruebas.sql" >/dev/null
psql -d cci_ct_ext -At -F ' | ' -c "select id,regla,esperado,obtenido,resultado from resultados order by n"
psql -d cci_ct_ext -Atc "select 'TOTAL pruebas='||count(*)||' PASS='||count(*) filter (where resultado='PASS')||' FAIL='||count(*) filter (where resultado='FAIL') from resultados"
