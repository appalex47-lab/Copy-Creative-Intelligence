#!/usr/bin/env bash
# Uso: ct_cierre_suites.sh <socket> <puerto> <dir_salida> <arbol_e0b1d81_cci_dev_NO_EJECUTADOS> <arbol_d365a16_cci_dev_NO_EJECUTADOS>   (PostgreSQL TEMPORAL LOCAL; nunca Supabase)
# Suites del cierre definitivo (adversarial del marcador y del ejecutor verificado, auditoría de search_path y secuestro, permutaciones de orden). Se ejecutan EN SERIE y después de la batería.
set -u; D="$(cd "$(dirname "$0")" && pwd)"; O="$4"; mkdir -p "$3"; OUT="$3"; PY="python3 -I -B"
echo "ADV";  $PY "$D/ct_pruebas_adversariales_cierre.py" "$1" "$2" "$4" "$OUT/adversarial_marcador_ejecutor.json" > "$OUT/adversarial_marcador_ejecutor.txt" 2>&1; echo "rc=$?" >> "$OUT/adversarial_marcador_ejecutor.txt"
echo "SP";   $PY "$D/ct_auditoria_search_path.py" "$1" "$2" "$D/cci_dev_NO_EJECUTADOS" "e0b1d81=$4,d365a16=$5" "$OUT/auditoria_search_path.json" > "$OUT/auditoria_search_path.txt" 2>&1; echo "rc=$?" >> "$OUT/auditoria_search_path.txt"
echo "PERM"; $PY "$D/ct_permutaciones_scripts.py" "$1" "$2" "$OUT/permutaciones.json" > "$OUT/permutaciones.txt" 2>&1; echo "rc=$?" >> "$OUT/permutaciones.txt"
