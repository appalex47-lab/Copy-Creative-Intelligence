#!/usr/bin/env bash
# Uso: ct_bateria_final.sh <socket> <puerto> [dir_docs_fase0]   (PostgreSQL TEMPORAL LOCAL; nunca Supabase/CCI-DEV/CCI-PROD)
# Ejecuta TODA la batería local desde cero: borra antes las salidas regenerables (no reutiliza resultados antiguos), ejecuta, y escribe
# resultados/bateria_final/INDICE_BATERIA.csv (paso, comando, inicio/fin UTC, rc, resumen, sha256 de la salida) + ENTORNO.txt.
set -u; SOCK="$1"; PORT="$2"; D="$(cd "$(dirname "$0")" && pwd)"; C="$D/.."; DOCS="${3:-$(cd "$C/.." && pwd)}"; R="$D/resultados"; B="$R/bateria_final"
export PGHOST="$SOCK" PGPORT="$PORT" PGUSER=cci_test
V20="$DOCS/expediente_final_v26/V25_copia_integra/03_SCRIPTS/PE_POSTGRESQL_V20"; M="$DOCS/herramientas/modelo_estructural.py"; PY="python3 -I -B"
INICIO=$(date -u +%FT%TZ); mkdir -p "$B"; rm -f "$B"/*
# salidas regenerables (se borran); se conservan los históricos (SQL_ASCII, corridas 1/2 del shim, controles de la versión anterior)
for f in base_V20_pe_utf8 base_V20_mutaciones_utf8 ext_utf8 concurrencia_local_utf8 dg19_pk_experimento hash_cadena_referencia revision_estatica_T47_T124 k47_por_escenario t409_t422_individual 22_funciones_reejecucion_local exc_en_mutaciones_modelo14 catalogo_except_y_ramas_muertas arnes_r1r9_autoprueba_local escaner_seguridad_sql escaner_seguridad_texto escaner_seguridad_autoprueba controles_negativos_manifiesto reconciliacion_integral; do rm -f "$R/$f.txt"; done
rm -f "$R"/smoke_*.txt "$R"/04_r1r9_local_bloqueado.txt "$R/k47_por_escenario.csv" "$R/t409_t422_individual.csv" "$R/t409_t422_correspondencia.csv" "$R/22_funciones_conciliacion.csv" "$R/catalogo_except_exception.csv"
{ echo "inicio_bateria_utc=$INICIO"; echo "anfitrion_so=$(uname -sr)"; echo "python=$(python3 -V 2>&1)"; echo "postgres=$(psql -d postgres -Atc 'select version()' 2>&1 | head -1)"; echo "base_local=clúster temporal en socket Unix (no Supabase)"; echo "HEAD_local=$(git -C "$D" rev-parse HEAD 2>/dev/null)"; } > "$B/ENTORNO.txt"
echo "paso,comando,inicio_utc,fin_utc,rc,resumen,salida,sha256_salida" > "$B/INDICE_BATERIA.csv"
paso() { # nombre salida resumen_regex comando...
  local n="$1" out="$2" rx="$3"; shift 3; local t0 t1 rc res
  t0=$(date -u +%FT%TZ); ( "$@" ) > "$out" 2>&1; rc=$?; t1=$(date -u +%FT%TZ)
  res=$(grep -E "$rx" "$out" | tail -n 1 | tr ',' ';' | cut -c1-160)
  printf '%s,"%s",%s,%s,%s,"%s",%s,%s\n' "$n" "$*" "$t0" "$t1" "$rc" "$res" "${out#$C/}" "$(sha256sum "$out" | cut -d' ' -f1)" >> "$B/INDICE_BATERIA.csv"
}
paso v20_pe            "$R/base_V20_pe_utf8.txt"            "TOTAL pruebas="        bash -c "cd '$V20' && bash ejecutar.sh '$SOCK' '$PORT'"
paso v20_mutaciones    "$R/base_V20_mutaciones_utf8.txt"    "TOTAL mutaciones="     bash -c "cd '$V20' && bash mutaciones.sh '$SOCK' '$PORT'"
paso extension_local   "$R/ext_utf8.txt"                    "TOTAL pruebas="        bash -c "cd '$D/local_ext' && bash ejecutar_ext.sh '$SOCK' '$PORT'"
paso concurrencia_local "$R/concurrencia_local_utf8.txt"    "CC-02"                 bash "$D/ct_concurrencia_local.sh" "$SOCK" "$PORT"
paso dg19              "$R/dg19_pk_experimento.txt"         "TOTAL pruebas="        bash "$D/ct_dg19_pk_experimento.sh" "$SOCK" "$PORT"
paso hash_encadenado   "$R/hash_cadena_referencia.txt"      "^TOTAL="               $PY "$D/ct_hash_cadena_referencia.py" --pg "$SOCK" "$PORT"
paso estatica_T47_T124 "$R/revision_estatica_T47_T124.txt"  "^TOTAL="               $PY "$D/ct_revision_estatica_T47_T124.py" "$DOCS"
paso k47_por_escenario "$R/k47_por_escenario.txt"           "TOTAL mutaciones"      $PY "$D/ct_k47_por_escenario.py" "$DOCS/herramientas" "$R/k47_por_escenario.csv"
paso t409_individual   "$R/t409_t422_individual.txt"        "^TOTAL variantes"      $PY "$D/ct_t409_t422_individual.py" "$DOCS" "$R/t409_t422_individual.csv"
paso t409_repro_2a_corrida "$B/t409_repro.txt"              "^TOTAL variantes"      $PY "$D/ct_t409_t422_individual.py" "$DOCS" "$B/t409_repro.csv"
paso t409_repro_comparacion "$B/t409_repro_cmp.txt" "IDENTICO|DIFIERE" bash -c "cmp -s '$R/t409_t422_individual.csv' '$B/t409_repro.csv' && echo IDENTICO_BYTE_A_BYTE || echo DIFIERE"
paso t409_correspondencia "$B/t409_correspondencia.txt"     "con coincidencia"      $PY "$D/ct_t409_t422_correspondencia.py" "$R" "$R/t409_t422_correspondencia.csv"
paso funciones_22      "$B/22_stdout.txt" "^TOTAL funciones"   $PY "$D/ct_reejecucion_22_funciones.py" "$DOCS" "$B/22_tmp.txt" "$R/22_funciones_conciliacion.csv"
mv "$B/22_tmp.txt" "$R/22_funciones_reejecucion_local.txt"
paso exc_modelo14      "$R/exc_en_mutaciones_modelo14.txt"  "TOTAL entradas EXC"    $PY "$D/ct_exc_en_mutaciones_modelo14.py" "$M"
paso catalogo_except   "$R/catalogo_except_y_ramas_muertas.txt" "EQUIVALENCIA"      $PY "$D/ct_catalogo_except_y_ramas_muertas.py" "$M" "$R/catalogo_except_exception.csv"
paso arnes_r1r9        "$R/arnes_r1r9_autoprueba_local.txt" "TOTAL pruebas_arnes"   bash "$D/ct_arnes_r1r9_autoprueba.sh" "$SOCK" "$PORT"
paso smoke_6_scripts   "$B/smoke_stdout.txt"                "."                     bash "$D/ct_smoke_scripts_cci_dev_local.sh" "$SOCK" "$PORT"
paso escaner_sql       "$B/escaner_sql_stdout.txt"          "^TOTAL="               $PY "$D/ct_escaner_seguridad_sql.py" sql "$D/cci_dev_NO_EJECUTADOS" "$R/escaner_seguridad_sql.txt"
paso escaner_texto     "$B/escaner_texto_stdout.txt"        "^TOTAL="               $PY "$D/ct_escaner_seguridad_sql.py" texto "$C" "$R/escaner_seguridad_texto.txt"
paso escaner_autoprueba "$B/escaner_autoprueba_stdout.txt"  "^TOTAL="             $PY "$D/ct_escaner_seguridad_sql.py" autoprueba "$R/escaner_seguridad_autoprueba.txt"
echo "fin_bateria_utc=$(date -u +%FT%TZ)" >> "$B/ENTORNO.txt"
awk -F, 'NR>1 && $5!=0 {n++} END {print "pasos con rc distinto de 0: " n+0}' "$B/INDICE_BATERIA.csv"
