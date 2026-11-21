#!/usr/bin/env bash
# Uso: ct_bateria_final.sh <socket> <puerto> [dir_docs_fase0]   (PostgreSQL TEMPORAL LOCAL; nunca Supabase/CCI-DEV/CCI-PROD)
# Ejecuta TODA la batería local desde cero: borra antes las salidas regenerables (no reutiliza resultados antiguos), ejecuta, y escribe
# resultados/bateria_final/INDICE_BATERIA.csv (paso, comando, inicio/fin UTC, rc, resumen, sha256 de la salida) + ENTORNO.txt.
set -u; SOCK="$1"; PORT="$2"; D="$(cd "$(dirname "$0")" && pwd)"; C="$(cd "$D/.." && pwd)"; DOCS="${3:-$(cd "$C/.." && pwd)}"; R="$D/resultados"; B="$R/bateria_final"
export PGHOST="$SOCK" PGPORT="$PORT" PGUSER=cci_test
V20="$DOCS/expediente_final_v26/V25_copia_integra/03_SCRIPTS/PE_POSTGRESQL_V20"; M="$DOCS/herramientas/modelo_estructural.py"; PY="python3 -I -B"
INICIO=$(date -u +%FT%TZ); mkdir -p "$B"; [ -z "${CCI_PASO_SOLO:-}" ] && rm -f "$B"/*
if [ -z "${CCI_PASO_SOLO:-}" ]; then   # modo completo: limpieza y cabecera; con CCI_PASO_SOLO (orquestador) las gestiona el orquestador
# salidas regenerables (se borran); se conservan los históricos (SQL_ASCII, corridas 1/2 del shim, controles de la versión anterior)
for f in base_V20_pe_utf8 base_V20_mutaciones_utf8 ext_utf8 concurrencia_local_utf8 dg19_pk_experimento hash_cadena_referencia revision_estatica_T47_T124 k47_por_escenario t409_t422_individual 22_funciones_reejecucion_local exc_en_mutaciones_modelo14 catalogo_except_y_ramas_muertas arnes_r1r9_autoprueba_local escaner_seguridad_sql escaner_seguridad_texto escaner_seguridad_autoprueba controles_negativos_manifiesto reconciliacion_integral aserciones_smoke guarda_destino busqueda_global controles_consistencia_informe; do rm -f "$R/$f.txt"; done
rm -f "$R"/reconciliacion_integral.json "$R"/cifras_definitivas.json "$R"/smoke_*.txt "$R"/04_r1r9_local_bloqueado.txt "$R/k47_por_escenario.csv" "$R/t409_t422_individual.csv" "$R/t409_t422_correspondencia.csv" "$R/22_funciones_conciliacion.csv" "$R/catalogo_except_exception.csv"
{ echo "inicio_bateria_utc=$INICIO"; echo "inicio_bateria_local=$(date +%FT%T%z)"; echo "zona_horaria_entorno_TZ=${TZ:-<sin TZ>} ($(date +%Z) $(date +%z))"; echo "epoch_inicio=$(date +%s)"; echo "reloj_sistema=hora obtenida con date(1) del entorno; sin verificación contra fuente NTP externa (no acreditable aquí)"; echo "anfitrion_so=$(uname -sr)"; echo "python=$(python3 -V 2>&1)"; echo "postgres=$(psql -d postgres -Atc 'select version()' 2>&1 | head -1)"; echo "base_local=clúster temporal en socket Unix (no Supabase)"; echo "commit_base_git=$(git -C "$C" rev-parse HEAD 2>/dev/null)"; echo "arbol_con_cambios_sin_commit=$(git -C "$C" status --porcelain -- "$C" 2>/dev/null | grep -v resultados/ | wc -l) archivos (fuera de resultados/); la batería se ejecuta sobre el árbol de trabajo"; echo "digest_entradas_sha256=$(cd "$C" && find . -type f ! -path './scripts_validacion/resultados/*' ! -path './evidencia_verificacion/*' ! -name MANIFIESTO_SHA256_CIERRE.txt ! -name 'INFORME_*' ! -name 'LEEME*' -print0 | sort -z | xargs -0 sha256sum | sha256sum | cut -d' ' -f1)"; } > "$B/ENTORNO.txt"
echo "paso,comando,inicio_utc,fin_utc,inicio_local,fin_local,zona_local,rc,esperado,estado,resumen,salida,sha256_salida" > "$B/INDICE_BATERIA.csv"
fi
declare -A EXP=( [v20_pe]="TOTAL pruebas=63 PASS=63 FAIL=0" [v20_mutaciones]="TOTAL mutaciones=14 DETECTADAS=14" [extension_local]="TOTAL pruebas=80 PASS=80 FAIL=0" [concurrencia_local]="^CC-01 .*23P01.*err=ERROR" [dg19]="TOTAL pruebas=63 PASS=63 FAIL=0" [hash_encadenado]="TOTAL=16 PASS=16 FAIL=0" [estatica_T47_T124]="TOTAL=12 PASS=10 FAIL=0 SIN_DATOS=2" [k47_por_escenario]="DETECTADAS=25 .*todas_detectadas_con_estado_inicial_valido=True" [t409_individual]="DETECTADAS=26 escenarios=14 .*todo_ok=True" [t409_repro_2a_corrida]="DETECTADAS=26 escenarios=14 .*todo_ok=True" [t409_repro_comparacion]="IDENTICO_BYTE_A_BYTE" [t409_correspondencia]="14 .*0 no establecidas" [funciones_22]="TOTAL funciones=22 casos_reportados=366 fallos=0" [exc_modelo14]="TOTAL entradas EXC en las 12 mutaciones=0" [catalogo_except]="EQUIVALENCIA_RAMAS_MUERTAS=True" [arnes_r1r9]="TOTAL pruebas_arnes=28 PASS=28 FAIL=0" [smoke_6_scripts]="SMOKE_RC=0" [aserciones_smoke]="TOTAL=12 PASS=12 FAIL=0" [guarda_destino]="TOTAL=187 PASS=187 FAIL=0" [escaner_sql]="TOTAL=176 FAIL=0" [escaner_texto]="^TOTAL=[0-9]+ FAIL=0" [escaner_autoprueba]="TOTAL=39 FAIL=0" )
paso() { # nombre salida resumen_regex comando...   (estado = OK solo si rc=0 Y la salida contiene lo ESPERADO; rc=0 solo no basta)
  local n="$1" out="$2" rx="$3"; shift 3; local t0 t1 l0 l1 rc res est e="${EXP[$n]:-}"
  if [ -n "${CCI_PASO_SOLO:-}" ] && [ "$CCI_PASO_SOLO" != "$n" ]; then return 0; fi
  t0=$(date -u +%FT%TZ); l0=$(date +%FT%T%z); ( "$@" ) > "$out" 2>&1; rc=$?; t1=$(date -u +%FT%TZ); l1=$(date +%FT%T%z)
  res=$(grep -E "$rx" "$out" | tail -n 1 | tr ',' ';' | cut -c1-160)
  if [ "$rc" = 0 ] && [ -n "$e" ] && grep -Eq "$e" "$out"; then est=OK; else est=FALLO; fi
  printf '%s,"%s",%s,%s,%s,%s,%s,%s,"%s",%s,"%s",%s,%s\n' "$n" "$*" "$t0" "$t1" "$l0" "$l1" "$(date +%Z)" "$rc" "$e" "$est" "$res" "${out#$C/}" "$(sha256sum "$out" | cut -d' ' -f1)" >> "$B/INDICE_BATERIA.csv"
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
[ -z "${CCI_PASO_SOLO:-}" ] || [ "$CCI_PASO_SOLO" = "funciones_22" ] && mv "$B/22_tmp.txt" "$R/22_funciones_reejecucion_local.txt"
paso exc_modelo14      "$R/exc_en_mutaciones_modelo14.txt"  "TOTAL entradas EXC"    $PY "$D/ct_exc_en_mutaciones_modelo14.py" "$M"
paso catalogo_except   "$R/catalogo_except_y_ramas_muertas.txt" "EQUIVALENCIA"      $PY "$D/ct_catalogo_except_y_ramas_muertas.py" "$M" "$R/catalogo_except_exception.csv"
paso arnes_r1r9        "$R/arnes_r1r9_autoprueba_local.txt" "TOTAL pruebas_arnes"   bash "$D/ct_arnes_r1r9_autoprueba.sh" "$SOCK" "$PORT"
# PRECONDICIÓN DETERMINISTA (parche de auditoría H-01): el inventario 02 depende de los roles anon/authenticated/service_role, que el shim crea más tarde y que persisten en el clúster entre ejecuciones; se crean aquí (sin privilegios, sin login) para que el resultado no dependa del historial del clúster.
if [ -z "${CCI_PASO_SOLO:-}" ] || [ "$CCI_PASO_SOLO" = "__precondicion_roles" ]; then
echo "ANTES de la precondicion: roles_no_sistema=$(psql -d postgres -Atc "select coalesce(string_agg(rolname||'(super='||rolsuper||',login='||rolcanlogin||')',',' order by rolname),'(ninguno)') from pg_roles where rolname !~ '^pg_' and rolname <> 'cci_test'")" >> "$B/precondicion_roles.txt" 2>&1
psql -d postgres -v ON_ERROR_STOP=1 -qAt -c "do \$\$ declare r text; begin foreach r in array array['anon','authenticated','service_role'] loop if not exists (select 1 from pg_roles where rolname=r) then execute format('create role %I nologin', r); end if; end loop; end \$\$" >> "$B/precondicion_roles.txt" 2>&1; echo "DESPUES de la precondicion: roles_no_sistema=$(psql -d postgres -Atc "select coalesce(string_agg(rolname||'(super='||rolsuper||',login='||rolcanlogin||')',',' order by rolname),'(ninguno)') from pg_roles where rolname !~ '^pg_' and rolname <> 'cci_test'")" >> "$B/precondicion_roles.txt" 2>&1; echo "roles_stand_in_presentes=$(psql -d postgres -Atc "select count(*) from pg_roles where rolname in ('anon','authenticated','service_role') and not rolsuper and not rolcanlogin")" >> "$B/ENTORNO.txt"
fi
paso smoke_6_scripts   "$B/smoke_stdout.txt"                "SMOKE_RC="             bash -c "bash '$D/ct_smoke_scripts_cci_dev_local.sh' '$SOCK' '$PORT'; echo SMOKE_RC=\$?"
paso aserciones_smoke  "$R/aserciones_smoke.txt"            "^TOTAL="               $PY "$D/ct_aserciones_smoke.py" "$R"
paso guarda_destino   "$R/guarda_destino.txt"            "^TOTAL="               $PY "$D/ct_pruebas_guarda_destino.py" "$SOCK" "$PORT" /dev/null   # H-03: pruebas negativas/positivas de la guarda DEV/PROD sobre los 6 scripts
paso escaner_sql       "$B/escaner_sql_stdout.txt"          "^TOTAL="               $PY "$D/ct_escaner_seguridad_sql.py" sql "$D/cci_dev_NO_EJECUTADOS" "$R/escaner_seguridad_sql.txt"
paso escaner_texto     "$B/escaner_texto_stdout.txt"        "^TOTAL="               $PY "$D/ct_escaner_seguridad_sql.py" texto "$C" "$R/escaner_seguridad_texto.txt"
paso escaner_autoprueba "$B/escaner_autoprueba_stdout.txt"  "^TOTAL="             $PY "$D/ct_escaner_seguridad_sql.py" autoprueba "$R/escaner_seguridad_autoprueba.txt"
if [ -z "${CCI_PASO_SOLO:-}" ]; then
echo "fin_bateria_utc=$(date -u +%FT%TZ)" >> "$B/ENTORNO.txt"; echo "fin_bateria_local=$(date +%FT%T%z)" >> "$B/ENTORNO.txt"
python3 -I -B - "$B/INDICE_BATERIA.csv" <<'PY'
import csv,sys
r=list(csv.DictReader(open(sys.argv[1],encoding="utf-8"))); bad=[x["paso"] for x in r if x["estado"]!="OK"]
print("pasos=%d con estado distinto de OK: %s" % (len(r), bad)); sys.exit(1 if bad else 0)
PY

fi