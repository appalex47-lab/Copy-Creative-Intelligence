#!/usr/bin/env bash
# Uso: ct_cierre_final.sh <socket> <puerto> <sha_commit_revisado> <owner/repo>   (PostgreSQL TEMPORAL LOCAL; nunca Supabase/CCI-DEV/CCI-PROD)
# Secuencia completa del cierre: batería desde cero → informes generados desde resultados → controles negativos → reconciliación (JSON→TXT+MD) → consistencia → manifiesto.
# Dos pasadas para llegar a punto fijo (el segundo recorrido ve el conjunto final de archivos). No hace commit ni push.
set -u; SOCK="$1"; PORT="$2"; REV="$3"; REPO="$4"; D="$(cd "$(dirname "$0")" && pwd)"; C="$(cd "$D/.." && pwd)"; R="$D/resultados"; PY="python3 -I -B"
export PGHOST="$SOCK" PGPORT="$PORT" PGUSER=cci_test; ESPEC="$C/../ESPECIFICACION_TECNICA_G1_G5_G10.md"
paso() { echo ">> $*"; "$@" || { echo "ERROR: falló: $*"; exit 1; }; }
[ "${SALTAR_BATERIA:-0}" = 1 ] && echo "(reanudación: batería ya ejecutada y con estado OK en este mismo árbol)" || paso bash "$D/ct_bateria_final.sh" "$SOCK" "$PORT"
cd "$D"; paso $PY ct_gen_limitaciones.py "$C"; paso $PY ct_gen_trazabilidad_maestra.py "$C" "$ESPEC"; paso $PY ct_gen_informe_pruebas.py "$C"
for pasada in 1 2; do
  echo "=== pasada $pasada ==="
  paso $PY ct_escaner_seguridad_sql.py texto "$C" "$R/escaner_seguridad_texto_final.txt" >/dev/null
  paso $PY ct_manifiesto.py gen "$C" >/dev/null   # fija el conjunto de archivos antes de calcular las cifras (el recuento de entradas sale de este manifiesto)
  paso $PY ct_gen_cifras.py "$C"
  paso $PY ct_manifiesto.py gen "$C"
  paso $PY ct_controles_negativos_manifiesto.py "$C" "$R/controles_negativos_manifiesto.txt"
  paso $PY ct_busqueda_global.py "$C" "$R/busqueda_global.txt" >/dev/null
  paso $PY ct_gen_resolucion_observaciones.py "$C" "$REV"
  paso $PY ct_gen_auditoria_fechas.py "$C" "$REPO"
  if [ "$pasada" = 1 ]; then $PY ct_reconciliacion_integral.py "$C" >/dev/null || echo "(pasada 1: la reconciliación puede fallar solo por archivos que esta misma pasada aún no ha generado; la pasada 2 es la que cuenta)"; else paso $PY ct_reconciliacion_integral.py "$C" >/dev/null; fi
  [ "$pasada" = 1 ] || paso $PY ct_verificar_consistencia_informe.py verificar "$C"
  paso $PY ct_verificar_consistencia_informe.py controles "$C" "$R/controles_consistencia_informe.txt" >/dev/null
done
paso $PY ct_manifiesto.py gen "$C"; paso $PY ct_manifiesto.py dir "$C"
echo "CIERRE_FINAL_OK"
