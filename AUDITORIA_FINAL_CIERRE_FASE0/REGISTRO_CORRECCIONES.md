# Registro de correcciones
Parche: `DIFF_COMPLETO_CORRECCIONES.patch` (31 archivos, sin resultados regenerados) frente a e0b1d81.
| Hallazgo | Corrección | Archivos |
|---|---|---|
| HC-01/02 | preflight + verificador + marcador por ejecución | 00_preflight_guarda.sql, 00_verificar_marcador.sql, 00_guarda_destino.sql, 6 scripts |
| HC-03 | chequeo de search_path | 00_guarda_destino.sql |
| HC-04 | calificación pg_catalog restante | 03/04/05A/05B |
| HC-05 | envoltorio reescrito + SHA256SUMS | ejecutar_script_verificado.sh, generar_sha256sums_cci.sh |
| tests | suites nuevas/actualizadas | ct_pruebas_*.py, ct_auditoria_search_path.py, escáner |
| HC-09 | estado documental | ESTADO_DOCUMENTAL_VIGENTE.md, LEEME_HISTORICO.md ×3 |
