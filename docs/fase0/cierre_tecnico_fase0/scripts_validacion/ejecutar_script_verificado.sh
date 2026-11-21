#!/usr/bin/env bash
# Uso: ejecutar_script_verificado.sh <SHA256_aprobado_de_00_guarda_destino.sql> <ruta/al/script.sql> [opciones de psql: -h/-p/-d/-U/-v ...]
# Verificación TÉCNICA previa a psql: (1) el SHA-256 de la guarda que se va a incluir debe coincidir con el aprobado por el propietario FUERA de este repositorio
# (se pasa como argumento; no se lee de ningún archivo del repo); (2) la guarda debe estar junto al script; (3) el script debe invocar la guarda y comprobar el marcador;
# (4) se ejecuta SIEMPRE con -f y ruta absoluta (nunca stdin) y ON_ERROR_STOP=1. LÍMITE: sólo protege a quien usa este envoltorio; invocar psql directamente lo omite.
set -u; [ $# -ge 2 ] || { echo "uso: $0 <sha256_guarda_aprobado> <script.sql> [opciones psql]" >&2; exit 2; }
APROB="$1"; SC="$2"; shift 2
[[ "$APROB" =~ ^[0-9a-f]{64}$ ]] || { echo "NO EJECUTADO [V-HASH-INVALIDO] el SHA-256 aprobado debe ser 64 hex en minúsculas" >&2; exit 3; }
SC="$(readlink -f -- "$SC" 2>/dev/null)" || exit 3; [ -f "$SC" ] || { echo "NO EJECUTADO [V-SCRIPT-AUSENTE]" >&2; exit 3; }
case "$(basename "$SC")" in 01_inventario_esquema_SOLO_LECTURA.sql|02_rls_privilegios_SOLO_LECTURA.sql|03_pruebas_rls_ROLLBACK.sql|04_trigger_r1_r9_ROLLBACK.sql|05_concurrencia_sesion_A.sql|05_concurrencia_sesion_B.sql) ;; *) echo "NO EJECUTADO [V-SCRIPT-NO-RECONOCIDO]" >&2; exit 3;; esac
G="$(dirname "$SC")/00_guarda_destino.sql"; [ -f "$G" ] || { echo "NO EJECUTADO [V-GUARDA-AUSENTE]" >&2; exit 3; }
REAL="$(sha256sum "$G" | cut -d' ' -f1)"; [ "$REAL" = "$APROB" ] || { echo "NO EJECUTADO [V-GUARDA-HASH-DISTINTO] esperado=${APROB:0:12}… real=${REAL:0:12}…" >&2; exit 3; }
grep -q '^\\ir 00_guarda_destino.sql$' "$SC" && grep -q "pg_temp.cci_guarda_ok" "$SC" || { echo "NO EJECUTADO [V-SCRIPT-SIN-INVOCACION-GUARDA]" >&2; exit 3; }
exec psql -X -v ON_ERROR_STOP=1 "$@" -f "$SC"
