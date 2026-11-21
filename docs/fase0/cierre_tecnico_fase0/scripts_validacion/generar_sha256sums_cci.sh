#!/bin/bash
# Genera cci_dev_NO_EJECUTADOS/SHA256SUMS_CCI.txt (los 10 archivos del conjunto ejecutable). El hash de ESTE archivo es el que el propietario debe custodiar FUERA del repo.
cd "$(dirname "$0")/cci_dev_NO_EJECUTADOS" || exit 1
sha256sum 00_guarda_destino.sql 00_preflight_guarda.sql 00_verificar_marcador.sql 01_inventario_esquema_SOLO_LECTURA.sql 02_rls_privilegios_SOLO_LECTURA.sql 03_pruebas_rls_ROLLBACK.sql 04_lib_clasificador.sql 04_trigger_r1_r9_ROLLBACK.sql 05_concurrencia_sesion_A.sql 05_concurrencia_sesion_B.sql > SHA256SUMS_CCI.txt
sha256sum SHA256SUMS_CCI.txt
