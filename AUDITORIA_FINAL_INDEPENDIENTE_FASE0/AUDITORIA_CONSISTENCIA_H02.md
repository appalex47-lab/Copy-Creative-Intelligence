# Auditoría de consistencia documental (H-02)
Fuente única de resultados: `scripts_validacion/resultados/*` generados por la batería; verificador de consistencia 58/58, reconciliación 58/58, manifiesto 138 entradas sin hashes incorrectos (verificación independiente `aud_integridad.py`), controles negativos 7/7 y 36/36. Estados usados: PASS/FAIL/PARTIAL/BLOCKED/NOT VERIFIED; PARTIAL = limitación estructural; NOT VERIFIED = Supabase/CCI-DEV.
## Tabla de conciliación
| # | Documento afectado | Contradicción | Corrección aplicada | Evidencia |
|---|---|---|---|---|
| 1 | DICTAMEN_H03.md (publicado) | Decía '85 pruebas + 25 casos' mientras INVENTARIO_PRUEBAS decía 109 | Reescrito; fuente única `guarda_destino.txt` (139) | INVENTARIO_PRUEBAS.md vigente |
| 2 | DICTAMEN_H03.md / AUDITORIA (publicado) | Hash de guarda 598ad606… (versión previa) vs 07c6673c… (d365a16) | Un solo hash vigente `b30a39d9d6dac497…` en todos los documentos; los antiguos sólo en histórico etiquetado | grep de hashes (tabla inferior) |
| 3 | AUDITORIA_INDEPENDIENTE_GUARDA_DEV_PROD.md (publicado) | AUD-G1 'ALTO, hueco real' en el cuerpo y 'corregido' en el aviso inicial | Versión vigente con estado por hallazgo; cuerpo previo movido a `historico_pre_auditoria_final/` con LEEME | documento vigente |
| 4 | AUDITORIA / DICTAMEN (publicado) | AUD-G3 mitigado 'sólo con -f' / corregido, pero X-07 muestra bypass con guarda forjadora | Estado PARCIAL con evidencia X-07 | MATRIZ_INTEGRIDAD_GUARDA.md |
| 5 | MATRIZ_PRUEBAS_SEGURIDAD_GUARDA.md (publicado) | Filas HUECO y aviso 'rechazan' simultáneos | Reemplazado por enlace a la fuente única y matrices | documento vigente |
| 6 | CONFIGURACION_REQUERIDA_CCI_DEV.md (publicado) | Condición previa 'aplicar AUD-G1' ya aplicada | Reescrito; añade requisito TEMP y hash externo | documento vigente |
| 7 | INFORME_RECONCILIACION / ct_reconciliacion_integral.py | La rama publicada falla el chequeo de alcance contra V26 en git | Ruta autorizada explícita | 58/58 |
| 8 | 'search_path blindado' (varios documentos) | Se leía como protección de todo el script; es local al bloque DO | PROPUESTA_GUARDA_DEV_PROD.md y matriz de persistencia lo acotan | MATRIZ_PERSISTENCIA_SEARCH_PATH.md |
| 9 | INFORME_PRUEBAS_FINALES / LEEME / cifras | 109 antes de añadir pruebas | Regenerados desde resultados (139) | aud_consistencia 58/58 |

## Barrido del hash vigente
Hash vigente de `00_guarda_destino.sql`: `b30a39d9d6dac4974913bf7140a619d1991b599a0c0d12af504f9af0906eb1ec`. Archivos fuera del histórico que aún mencionan los hashes antiguos: ['docs/fase0/publicacion_remediaciones_h01_h02_h03/historico_pre_auditoria_final/DICTAMEN_H03.md', 'docs/fase0/publicacion_remediaciones_h01_h02_h03/historico_pre_auditoria_final/MATRIZ_ARCHIVOS_MODIFICADOS_Y_NUEVOS.csv', 'docs/fase0/publicacion_remediaciones_h01_h02_h03/historico_pre_auditoria_final/AUDITORIA_INDEPENDIENTE_GUARDA_DEV_PROD.md', 'docs/fase0/publicacion_remediaciones_h01_h02_h03/historico_pre_auditoria_final/LEEME_HISTORICO.md'].
## Reglas aplicadas
Resultados históricos etiquetados (carpeta `historico_pre_auditoria_final/` y filas `PUB:`); PostgreSQL local nunca presentado como validación de Supabase; ningún estado se promovió a PASS sin ejecución.
