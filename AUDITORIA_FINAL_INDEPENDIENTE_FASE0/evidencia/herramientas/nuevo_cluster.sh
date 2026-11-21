#!/bin/bash
# Uso: nuevo_cluster.sh <nombre> <puerto>  -> clúster PostgreSQL 16 NUEVO, vacío, solo socket Unix (/tmp/aud/<nombre>/sock). Rol cci_test superusuario local. SIN roles anon/authenticated/service_role (precondición que debe crear la batería).
set -e; N=$1; P=$2; B=/usr/lib/postgresql/16/bin; rm -rf /tmp/aud/$N; mkdir -p /tmp/aud/$N/sock; chown -R postgres:postgres /tmp/aud/$N
su postgres -c "$B/initdb -D /tmp/aud/$N/data -A trust -E UTF8 --locale=C.UTF-8 >/tmp/aud/$N/initdb.txt 2>&1 && $B/pg_ctl -D /tmp/aud/$N/data -o \"-k /tmp/aud/$N/sock -p $P -c listen_addresses=\" -l /tmp/aud/$N/log -w start >/dev/null"
su postgres -c "psql -h /tmp/aud/$N/sock -p $P -d postgres -qAtc \"create role cci_test superuser login\""
echo "cluster $N listo: socket=/tmp/aud/$N/sock puerto=$P sysid=$(psql -h /tmp/aud/$N/sock -p $P -U cci_test -d postgres -qAtc 'select system_identifier from pg_control_system()') roles_supabase_like=$(psql -h /tmp/aud/$N/sock -p $P -U cci_test -d postgres -qAtc "select count(*) from pg_roles where rolname in ('anon','authenticated','service_role')")"
