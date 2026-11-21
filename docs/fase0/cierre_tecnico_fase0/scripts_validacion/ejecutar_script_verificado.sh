#!/bin/bash
# ejecutar_script_verificado.sh — EJECUTOR VERIFICADO de los 6 scripts CCI (cierre definitivo, AUD-CIERRE-03).
# Uso: ejecutar_script_verificado.sh <SHA256_del_SHA256SUMS_CCI.txt_APROBADO> <ruta/al/script.sql> [opciones de psql: -h/-p/-d/-U/-v ...]
# RAÍZ DE CONFIANZA: el primer argumento lo entrega EL PROPIETARIO por un canal ajeno a este repositorio (custodio pendiente de definir: ver AUDITORIA_HASH_EXTERNO.md).
# Mientras no exista ese custodio, este ejecutor es un MECANISMO LISTO, no una protección operativa.
# Qué hace (en este orden, fallando cerrado con 'NO EJECUTADO [V-...]' y rc=3, sin ejecutar psql): rechaza symlinks; copia los 10 archivos del conjunto a un directorio privado
# 0700; comprueba que el hash de la COPIA de SHA256SUMS_CCI.txt es el aprobado y que cada archivo copiado coincide (sha256sum -c --strict); exige que el script esté en el conjunto;
# restringe PGOPTIONS a cci.validacion_autorizada / cci.entorno; exige destino aprobado (CCI_DESTINOS_APROBADOS, obligatorio en modo CCI-DEV); sanea el entorno (PATH fijo,
# sin PSQLRC/BASH_ENV/LD_*); ejecuta psql con -X -f sobre la COPIA (TOCTOU: lo que se verificó es lo que se ejecuta) y borra el directorio al terminar (también ante señales).
# LÍMITES: un atacante con el mismo uid puede modificar el directorio privado; quien invoque psql directamente no pasa por este ejecutor (los scripts exigen igualmente
# CCI_DIR + hash de la guarda: ver 00_preflight_guarda.sql); el ejecutor no puede impedir que el propietario/superusuario edite la guarda.
set -u
PATH=/usr/sbin:/usr/bin:/sbin:/bin; export PATH
unset PSQLRC PSQL_HISTORY PSQL_EDITOR BASH_ENV ENV LD_PRELOAD LD_LIBRARY_PATH PGSYSCONFDIR PGSERVICEFILE PGSERVICE
rech(){ echo "NO EJECUTADO [$1] ${2:-}" >&2; exit 3; }
[ $# -ge 2 ] || { echo "uso: $0 <sha256_del_SHA256SUMS_aprobado> <script.sql> [opciones psql]" >&2; exit 2; }
APROB="$1"; SCIN="$2"; shift 2
[[ "$APROB" =~ ^[0-9a-f]{64}$ ]] || rech V-HASH-INVALIDO "el SHA-256 aprobado debe ser 64 hex en minúsculas (ausente o mal formado)"
[ -e "$SCIN" ] || rech V-SCRIPT-AUSENTE; [ ! -L "$SCIN" ] || rech V-SYMLINK "el script es un enlace simbólico"
[ -f "$SCIN" ] || rech V-SCRIPT-AUSENTE
D="$(cd -- "$(dirname -- "$SCIN")" 2>/dev/null && pwd -P)" || rech V-RUTA; NOM="$(basename -- "$SCIN")"
SUMS="$D/SHA256SUMS_CCI.txt"; [ -f "$SUMS" ] && [ ! -L "$SUMS" ] || rech V-SUMS-AUSENTE
for a in "$@"; do case "$a" in -f*|--file*|-c*|--command*|-C*|-L*|--log-file*|-o*|--output*|-v\ cci_*|--set=cci_*|-vcci_*|-X|-1|--single-transaction) rech V-OPCION-NO-PERMITIDA "$a";; esac; done
prev=""; for a in "$@"; do if [ "$prev" = "-v" ] || [ "$prev" = "--set" ]; then case "$a" in cci_*|ON_ERROR_STOP*|ECHO_HIDDEN*|AUTOCOMMIT*) rech V-OPCION-NO-PERMITIDA "-v $a";; esac; fi; prev="$a"; done
P="$(mktemp -d "${TMPDIR:-/tmp}/cci_ev.XXXXXX")" || rech V-TMP; chmod 700 "$P"
trap 'rm -rf -- "$P"' EXIT; trap 'exit 130' INT TERM HUP
cp -- "$SUMS" "$P/SHA256SUMS_CCI.txt" 2>/dev/null || rech V-PERMISOS "no se pudo leer SHA256SUMS"
[ "$(sha256sum < "$P/SHA256SUMS_CCI.txt" | cut -d' ' -f1)" = "$APROB" ] || rech V-SUMS-HASH-DISTINTO "el SHA256SUMS no coincide con el hash aprobado externamente"
OKN=0; while read -r h n; do
  [[ "$h" =~ ^[0-9a-f]{64}$ ]] && [[ "$n" =~ ^[0-9A-Za-z_]+\.sql$ ]] || rech V-SUMS-MALFORMADO "$n"
  [ -f "$D/$n" ] && [ ! -L "$D/$n" ] || rech V-ARCHIVO-AUSENTE-O-SYMLINK "$n"
  cp -- "$D/$n" "$P/$n" 2>/dev/null || rech V-PERMISOS "$n"; chmod 400 "$P/$n"; OKN=$((OKN+1))
done < <(sed 's/^\([0-9a-f]*\)  *\*\?/\1 /' "$P/SHA256SUMS_CCI.txt")
[ "$OKN" -eq 10 ] || rech V-SUMS-CONJUNTO "el conjunto aprobado debe listar exactamente 10 archivos"
( cd "$P" && sha256sum -c --strict --quiet SHA256SUMS_CCI.txt >/dev/null 2>&1 ) || rech V-ARCHIVO-ALTERADO "algún archivo del conjunto no coincide con el SHA256SUMS aprobado"
case "$NOM" in 01_inventario_esquema_SOLO_LECTURA.sql|02_rls_privilegios_SOLO_LECTURA.sql|03_pruebas_rls_ROLLBACK.sql|04_trigger_r1_r9_ROLLBACK.sql|05_concurrencia_sesion_A.sql|05_concurrencia_sesion_B.sql) ;; *) rech V-SCRIPT-NO-RECONOCIDO "$NOM";; esac
GH="$(grep -E ' \*?00_guarda_destino\.sql$' "$P/SHA256SUMS_CCI.txt" | cut -d' ' -f1)"; [[ "$GH" =~ ^[0-9a-f]{64}$ ]] || rech V-SUMS-SIN-GUARDA
# PGOPTIONS: sólo las dos variables de intención del operador
PO="${PGOPTIONS:-}"; if [ -n "$PO" ]; then set -- "$@"; rest="$(printf '%s' "$PO" | sed -E 's/-c +cci\.(validacion_autorizada|entorno)=[A-Za-z0-9-]+//g' | tr -d ' ')"; [ -z "$rest" ] || rech V-PGOPTIONS-NO-PERMITIDO "sólo se permiten -c cci.validacion_autorizada=… y -c cci.entorno=…"; fi
# destino (identidad EXTERNA): host de conexión declarado por el cliente
HOST="${PGHOST:-}"; prev=""; for a in "$@"; do case "$a" in --host=*) HOST="${a#--host=}";; -h*) [ "$a" = "-h" ] || HOST="${a#-h}";; esac; [ "$prev" = "-h" ] || [ "$prev" = "--host" ] && HOST="$a"; prev="$a"; done
if [[ "$PO" == *"cci.entorno=CCI-DEV"* ]] && [ -z "${CCI_DESTINOS_APROBADOS:-}" ]; then rech V-DESTINO-NO-CONFIGURADO "modo CCI-DEV exige CCI_DESTINOS_APROBADOS (lista de hosts aprobada por el propietario)"; fi
if [ -n "${CCI_DESTINOS_APROBADOS:-}" ]; then [ -n "$HOST" ] || rech V-DESTINO-NO-DECLARADO "falta -h/PGHOST"; case ":$CCI_DESTINOS_APROBADOS:" in *":$HOST:"*) ;; *) rech V-DESTINO-NO-APROBADO "el host no está en CCI_DESTINOS_APROBADOS";; esac; fi
PSQL=/usr/bin/psql; [ -x "$PSQL" ] || rech V-PSQL-AUSENTE
CCI_DIR="$P" CCI_TMPDIR="$P" CCI_GUARDA_SHA256_APROBADO="$GH" "$PSQL" -X -v ON_ERROR_STOP=1 "$@" -f "$P/$NOM"; rc=$?
exit $rc
