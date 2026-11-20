#!/bin/bash
# Uso: ejecutar.sh <directorio_socket> <puerto>  (clúster PostgreSQL TEMPORAL; nunca un servicio real ni Supabase)
set -e; export PGHOST="$1" PGPORT="$2" PGUSER=cci_test; D="$(dirname "$0")"
psql -d postgres -qAtc "drop database if exists cci_v20_test" -c "create database cci_v20_test"
psql -d cci_v20_test -q -v ON_ERROR_STOP=1 -f "$D/01_fixture.sql" -f "$D/02_pruebas.sql"
psql -d cci_v20_test -At -F ' | ' -c "select id,regla,esperado,obtenido,resultado,descripcion from resultados order by n"
psql -d cci_v20_test -Atc "select 'TOTAL pruebas='||count(*)||' PASS='||count(*) filter (where resultado='PASS')||' FAIL='||count(*) filter (where resultado='FAIL') from resultados"
psql -d postgres -qAtc "select version()"
