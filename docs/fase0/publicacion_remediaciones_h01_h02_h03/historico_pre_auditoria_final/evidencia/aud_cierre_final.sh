#!/usr/bin/env bash
C="$1"; S="$C/scripts_validacion"; R="$S/resultados"; PY="python3 -I -B"; cd "$S"; SHA=5b008485706bde3e9cf8407e71c0652cfd0497a5
r() { "$@" >/tmp/aud/out/cf_last.txt 2>&1; echo "rc=$? $(basename $2) $(tail -1 /tmp/aud/out/cf_last.txt | cut -c1-90)"; }
r $PY ct_gen_limitaciones.py "$C"
r $PY ct_gen_trazabilidad_maestra.py "$C" "$C/../ESPECIFICACION_TECNICA_G1_G5_G10.md"
r $PY ct_gen_informe_pruebas.py "$C"
for i in 1 2; do
r $PY ct_gen_cifras.py "$C"
r $PY ct_manifiesto.py gen "$C"
r $PY ct_controles_negativos_manifiesto.py "$C" "$R/controles_negativos_manifiesto.txt"
r $PY ct_gen_resolucion_observaciones.py "$C" $SHA
r $PY ct_gen_auditoria_fechas.py "$C" appalex47-lab/Copy-Creative-Intelligence
done
r $PY ct_busqueda_global.py "$C" "$R/busqueda_global.txt"
r $PY ct_reconciliacion_integral.py "$C"
r $PY ct_verificar_consistencia_informe.py verificar "$C"
r $PY ct_verificar_consistencia_informe.py controles "$C" "$R/controles_consistencia_informe.txt"
r $PY ct_manifiesto.py gen "$C"
r $PY ct_manifiesto.py dir "$C"
