#!/bin/bash
# Prueba de concurrencia en el clúster PostgreSQL TEMPORAL LOCAL (nunca Supabase). Requiere haber ejecutado local_ext/ejecutar_ext.sh (base cci_ct_ext).
# Uso: ct_concurrencia_local.sh <directorio_socket> <puerto>
set -u; export PGHOST="$1" PGPORT="$2" PGUSER=cci_test; DB=cci_ct_ext; 
PIECE=$(psql -d $DB -qAt -c 'select gen_random_uuid()')  # pieza nueva por ejecución (el historial es inmutable: el script es repetible sin limpiar)
Q() { psql -d $DB -qAt -v ON_ERROR_STOP=1 "$@" 2>&1; }
# Preparación: pieza y miembros propios de esta prueba
Q -c "insert into organizations values ('00000000-0000-0000-0000-0000000000c1') on conflict do nothing; insert into memberships(organization_id,user_id) values ('00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000d1'),('00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000d2'),('00000000-0000-0000-0000-0000000000c1','00000000-0000-0000-0000-0000000000d3') on conflict do nothing; insert into channel_rules values ('00000000-0000-0000-0000-0000000000c1','instagram',true) on conflict do nothing; insert into channel_formats(organization_id,channel,format,created_by) values ('00000000-0000-0000-0000-0000000000c1','instagram','post','00000000-0000-0000-0000-0000000000d1') on conflict do nothing; insert into creative_pieces(id,organization_id,channel,format) values ('$PIECE','00000000-0000-0000-0000-0000000000c1','instagram','post') on conflict do nothing" >/dev/null 2>&1
INS() { echo "insert into piece_reviewer_assignments_x values ('$1','00000000-0000-0000-0000-0000000000c1','$PIECE','$2','00000000-0000-0000-0000-0000000000d1',tstzrange('2028-01-01 00:00+00',null,'[)'),'concurrencia')"; }
# CC-01: dos transacciones insertan asignaciones solapadas para la misma pieza; la segunda debe BLOQUEARSE y luego fallar con 23P01; sólo queda una fila
psql -d $DB -qAt -c "begin; $(INS $(psql -d $DB -qAt -c 'select gen_random_uuid()') 00000000-0000-0000-0000-0000000000d2); select pg_sleep(3); commit;" >/tmp/ct_cc_a.txt 2>&1 &
PA=$!; sleep 1; T0=$(date +%s.%N)
RB=$(psql -d $DB -qAt -c "$(INS $(psql -d $DB -qAt -c 'select gen_random_uuid()') 00000000-0000-0000-0000-0000000000d3)" 2>&1); T1=$(date +%s.%N); wait $PA
EL=$(python3 -I -B -c "print(round($T1-$T0,2))"); N=$(Q -c "select count(*) from piece_reviewer_assignments_x where piece_id='$PIECE'")
if echo "$RB" | grep -q "exclusion constraint" && [ "$N" = "1" ] && python3 -I -B -c "import sys; sys.exit(0 if $EL>=1.5 else 1)"; then R=PASS; else R=FAIL; fi
echo "CC-01 | G-9 exclusión bajo concurrencia | esperado: B bloqueada >=1.5s y luego 23P01; filas=1 | obtenido: espera=${EL}s filas=$N err=$(echo $RB | cut -c1-70) | $R"
# CC-02: dos transacciones insertan la MISMA numeración de versión (unique(organization_id,piece_id,version_no)); la segunda se bloquea y falla con 23505
CV() { echo "insert into copy_versions values ('$1','00000000-0000-0000-0000-0000000000c1','$PIECE',1,null,null)"; }
psql -d $DB -qAt -c "begin; $(CV $(psql -d $DB -qAt -c 'select gen_random_uuid()')); select pg_sleep(3); commit;" >/tmp/ct_cc_a.txt 2>&1 &
PA=$!; sleep 1; T0=$(date +%s.%N)
RB=$(psql -d $DB -qAt -c "$(CV $(psql -d $DB -qAt -c 'select gen_random_uuid()'))" 2>&1); T1=$(date +%s.%N); wait $PA
EL=$(python3 -I -B -c "print(round($T1-$T0,2))"); N=$(Q -c "select count(*) from copy_versions where piece_id='$PIECE' and version_no=1")
if echo "$RB" | grep -q "duplicate key" && [ "$N" = "1" ] && python3 -I -B -c "import sys; sys.exit(0 if $EL>=1.5 else 1)"; then R=PASS; else R=FAIL; fi
echo "CC-02 | IG1-14 numeración de versión única bajo concurrencia | esperado: B bloqueada >=1.5s y luego 23505; filas=1 | obtenido: espera=${EL}s filas=$N err=$(echo $RB | cut -c1-60) | $R"
