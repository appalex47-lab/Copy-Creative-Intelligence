#!/bin/bash
# Control de sensibilidad: cada mutación elimina UN mecanismo del fixture; la prueba asociada DEBE pasar a FAIL (si no, la prueba no detecta la corrupción).
# Uso: mutaciones.sh <directorio_socket> <puerto>
export PGHOST="$1" PGPORT="$2" PGUSER=cci_test; D="$(dirname "$0")"; ok=0; n=0
m() { # prueba_esperada_en_FAIL | sql de mutación
  n=$((n+1)); psql -d postgres -qAtc "drop database if exists cci_v20_mut" -c "create database cci_v20_mut" >/dev/null
  psql -d cci_v20_mut -q -v ON_ERROR_STOP=1 -f "$D/01_fixture.sql" >/dev/null 2>&1
  if ! psql -d cci_v20_mut -q -v ON_ERROR_STOP=1 -c "$2" >/dev/null 2>&1; then echo "MUT-$n | MUTACIÓN NO APLICADA: $2 | ERROR DEL ARNÉS"; continue; fi
  r=$(psql -d cci_v20_mut -q -f "$D/02_pruebas.sql" -At -c "select resultado from resultados where id='$1'" 2>&1 | tail -1)
  if [ "$r" = "FAIL" ]; then ok=$((ok+1)); echo "MUT-$n | $1 pasa a FAIL al quitar: $2 | DETECTADA"; else echo "MUT-$n | $1 sigue en '$r' al quitar: $2 | NO DETECTADA"; fi; }
m PE-01a "alter table creative_pieces drop constraint creative_pieces_organization_id_master_piece_id_fkey"
m PE-02a "drop trigger t_master on creative_pieces"
m PE-03a "drop trigger t_cv_imm on copy_versions"
m PE-04a "alter table approvals drop constraint approvals_organization_id_piece_id_copy_version_id_fkey"
m PE-05b "alter table impact_evaluations drop constraint impact_evaluations_organization_id_adaptation_piece_id_adap_key"
m PE-05f "alter table impact_evaluations drop constraint impact_evaluations_organization_id_adaptation_piece_id_ada_fkey"
m PG-CF-05 "alter table channel_formats drop constraint channel_formats_format_check"
m PG-CF-12 "drop trigger t_cf_upd on channel_formats"
m PG-CF-08 "alter table channel_formats drop constraint channel_formats_organization_id_channel_fkey"
m PG-AD-05 "drop trigger t_adr_imm on attribution_discard_resolutions"
m PG-AD-07 "drop trigger t_adr_trunc on attribution_discard_resolutions"
m PG-AD-08 "alter table attribution_discard_resolutions drop constraint attribution_discard_resolutions_check1"
m PG-AD-04 "drop index u_adr_aceptada"
m PG-AD-15 "alter table attribution_discard_resolutions disable trigger t_adr_ins"
echo "TOTAL mutaciones=$n DETECTADAS=$ok"; psql -d postgres -qAtc "drop database if exists cci_v20_mut" >/dev/null
