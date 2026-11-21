# Registro de hallazgos
| ID | Hallazgo | Severidad | Estado |
|---|---|---|---|
| HC-01 | Marcador pg_temp.cci_guarda_ok forjable (A, D, E1) | Alta | Corregido (marcador por ejecución, id aleatorio, consumo único, hash externo) |
| HC-02 | Ejecución directa sin verificación de la guarda | Alta | Corregido (preflight exige CCI_DIR y hash aprobado; GD-20) |
| HC-03 | search_path hostil del llamador aceptado | Media | Corregido (G-SEARCH-PATH-NO-SEGURO) |
| HC-04 | 17 llamadas a funciones sin calificar en e0b1d81 (161 en d365a16) | Media | Corregido: 0 |
| HC-05 | Envoltorio: ventana TOCTOU, entorno, symlinks, destino | Alta | Corregido (reescritura; WRAP-01…27) |
| HC-06 | Identidad: clon físico indistinguible (AG-18) | Media | NO corregible; mitigado parcialmente con lista externa |
| HC-07 | Guarda falsa + control del hash aprobado | Media | NO corregible (estructural); depende del custodio externo |
| HC-08 | Operadores sin calificar protegidos sólo por el chequeo | Baja | Residual documentado |
| HC-09 | Documentos históricos con afirmaciones obsoletas | Media | Corregido: marcados superados + estado vigente |
| HC-10 | Reconciliación esperaba `\ir 00_guarda_destino.sql` | Baja | Corregida |
