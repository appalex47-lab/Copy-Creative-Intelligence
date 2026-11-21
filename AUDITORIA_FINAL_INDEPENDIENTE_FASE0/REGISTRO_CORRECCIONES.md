# Registro de correcciones locales (no publicadas; en una sola ronda)
Base corregida: rama publicada d365a16 + parche local (`DIFF_CORRECCIONES_LOCALES.patch`, 47 archivos; el parche completo con resultados regenerados está en `evidencia/`). Nada se hizo commit ni push.

| ID | Hallazgo | Corrección | Archivos | Prueba que la sostiene |
|---|---|---|---|---|
| C-01 | F-01 | Calificar con `pg_catalog.` 144 llamadas a funciones del catálogo en 01–05B y 04_lib | scripts_validacion/cci_dev_NO_EJECUTADOS/*.sql | GD-19 (6), hijack POST 0/6, batería 22/22 |
| C-02 | F-02 | Marcador = tabla temporal `pg_temp.cci_guarda_ok` creada al final de la guarda; aserción `to_regclass` en cada script | 00_guarda_destino.sql; 6 scripts | GD-13/16, X-10 (6 PASS), INT-02..08 |
| C-03 | F-03/F-04 | `ejecutar_script_verificado.sh`: hash externo, -f absoluta, guarda junto al script, sin stdin | scripts_validacion/ejecutar_script_verificado.sh | GD-18a-f |
| C-04 | F-01/02/03 | 30 pruebas nuevas (GD-15…GD-19): 109 → 139; pin de la batería actualizado | ct_pruebas_guarda_destino.py; ct_bateria_final.sh | guarda_destino 139/139 |
| C-05 | F-08 | Rechazo exige `ERROR: NO EJECUTADO [código]` | ct_pruebas_guarda_destino.py | 139/139 |
| C-06 | F-05 | Ruta autorizada `docs/fase0/publicacion_remediaciones_h01_h02_h03/` en el chequeo de alcance | ct_reconciliacion_integral.py | reconciliación 58/58 |
| C-07 | F-07 | Registro antes/después de roles en la precondición | ct_bateria_final.sh | precondicion_roles_cluster*.txt |
| C-08 | F-06 | Documentos vigentes reescritos; versión previa a `historico_pre_auditoria_final/` con LEEME; hash único | publicacion_remediaciones_h01_h02_h03/*; PROPUESTA_GUARDA_DEV_PROD.md | AUDITORIA_CONSISTENCIA_H02.md |
| C-09 | — | Cifras, informes, manifiesto (138 entradas) y reconciliación regenerados desde la fuente única, dos pasadas | scripts_validacion/ct_gen_*, ct_manifiesto.py | hash_incorrecto 0; 58/58 |
| C-10 | F-10 | Normalización de segundos en el comparador | herramienta de auditoría | comparación 30/30 |
