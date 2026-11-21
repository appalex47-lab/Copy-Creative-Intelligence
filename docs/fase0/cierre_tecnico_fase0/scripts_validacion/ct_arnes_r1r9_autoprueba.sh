#!/bin/bash
# Uso: ct_arnes_r1r9_autoprueba.sh <directorio_socket> <puerto>. PostgreSQL TEMPORAL LOCAL (nunca Supabase). Autoprueba del ARNÉS (no de R1–R9).
set -e; export PGHOST="$1" PGPORT="$2" PGUSER=cci_test; D="$(cd "$(dirname "$0")" && pwd)"
export PGOPTIONS="-c cci.entorno=LOCAL-TEMPORAL"
psql -d postgres -qAtc "drop database if exists cci_arnes_local" -c "create database cci_arnes_local" >/dev/null
psql -d cci_arnes_local -q -v ON_ERROR_STOP=1 -P pager=off -f "$D/local_ext/20_arnes_r1r9_autoprueba_LOCAL.sql" 2>&1 | grep -v '^CREATE\|^INSERT\|^DO$\|^SELECT'
