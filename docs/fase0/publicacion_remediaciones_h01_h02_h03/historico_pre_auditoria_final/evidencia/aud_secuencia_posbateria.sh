#!/usr/bin/env bash
# Repite, SIN abortar ante fallos, la parte posterior a la batería con las herramientas publicadas, sobre la copia de trabajo. Cada comando registra rc.
C="$1"; S="$C/scripts_validacion"; R="$S/resultados"; PY="python3 -I -B"; cd "$S"; REV=bdd4a6d78a68ede6e6f68391e4c2eebbcc34503a
run() { local t0=$(date -u +%FT%TZ); "$@" > /tmp/aud/out/pos_$$_last.txt 2>&1; local rc=$?; echo "rc=$rc | $t0 | $*"; tail -2 /tmp/aud/out/pos_$$_last.txt | cut -c1-200; }
run $PY ct_escaner_seguridad_sql.py texto "$C" "$R/escaner_seguridad_texto_final.txt"
run $PY ct_manifiesto.py gen "$C"
run $PY ct_gen_cifras.py "$C"
run $PY ct_manifiesto.py gen "$C"
run $PY ct_controles_negativos_manifiesto.py "$C" "$R/controles_negativos_manifiesto.txt"
run $PY ct_busqueda_global.py "$C" "$R/busqueda_global.txt"
run $PY ct_reconciliacion_integral.py "$C"
run $PY ct_verificar_consistencia_informe.py verificar "$C"
run $PY ct_verificar_consistencia_informe.py controles "$C" "$R/controles_consistencia_informe.txt"
echo FIN
