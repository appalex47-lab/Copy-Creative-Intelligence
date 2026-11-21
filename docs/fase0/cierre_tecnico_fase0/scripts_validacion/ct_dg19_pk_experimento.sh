#!/bin/bash
# Experimento local DG-19: ¿la PK natural (organization_id, channel, format) es compatible con las 63 pruebas V20? Clúster TEMPORAL local. Uso: ct_dg19_pk_experimento.sh <socket> <puerto>
set -e; export PGHOST="$1" PGPORT="$2" PGUSER=cci_test; D="$(cd "$(dirname "$0")" && pwd)"; B="$D/../../expediente_final_v26/V25_copia_integra/03_SCRIPTS/PE_POSTGRESQL_V20"
T=$(mktemp -d); sed 's/^  unique(organization_id,channel,format),$/  primary key(organization_id,channel,format),/' "$B/01_fixture.sql" > $T/fx.sql
grep -c "primary key(organization_id,channel,format)" $T/fx.sql | sed 's/^/líneas modificadas del fixture (copia temporal): /'
psql -d postgres -qAtc "drop database if exists cci_dg19_pk" -c "create database cci_dg19_pk" >/dev/null 2>&1
psql -d cci_dg19_pk -q -v ON_ERROR_STOP=1 -f $T/fx.sql -f "$B/02_pruebas.sql" >/dev/null 2>&1
psql -d cci_dg19_pk -Atc "select 'DG-19 PK natural: TOTAL pruebas='||count(*)||' PASS='||count(*) filter (where resultado='PASS')||' FAIL='||count(*) filter (where resultado='FAIL') from resultados"
psql -d cci_dg19_pk -Atc "select id||' esperado='||esperado||' obtenido='||obtenido from resultados where resultado='FAIL'"
rm -rf $T
