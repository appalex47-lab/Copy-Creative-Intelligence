#!/bin/bash
# Uso: ct_nuevo_cluster.sh <dir_base> <puerto>  -> clúster PostgreSQL 16 NUEVO y vacío, sólo socket Unix (<dir_base>/sock). Rol cci_test superusuario local. Requiere root (su postgres). LOCAL TEMPORAL; nunca Supabase.
set -e; D="$1"; P="$2"; B=/usr/lib/postgresql/16/bin; rm -rf "$D"; mkdir -p "$D/sock"; chown -R postgres:postgres "$D"
su postgres -c "$B/initdb -D $D/data -A trust -E UTF8 --locale=C.UTF-8 >$D/initdb.txt 2>&1 && $B/pg_ctl -D $D/data -o \"-k $D/sock -p $P -c listen_addresses=\" -l $D/log -w start >/dev/null"
su postgres -c "psql -h $D/sock -p $P -d postgres -qAtc \"create role cci_test superuser login\""
echo "cluster listo: socket=$D/sock puerto=$P sysid=$(psql -h $D/sock -p $P -U cci_test -d postgres -qAtc 'select system_identifier from pg_control_system()')"
