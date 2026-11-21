# Registro de hallazgos
Total: 13. Críticos: 0 · Altos: 2 · Medios: 4 · Bajos: 4 · Estructurales: 2 · No verificados: 1.

| ID | Severidad | Área | Hallazgo | Evidencia | Estado |
|---|---|---|---|---|---|
| F-01 | ALTO | H-03 | El search_path blindado de la guarda no persiste tras su bloque DO; las instrucciones posteriores resolvían funciones con el search_path del llamador (hijack: 05A y 05B invocaron funciones homónimas) | hijack_PRE_rama_publicada.txt; SP-04 | CORREGIDO (local): calificación pg_catalog + GD-19 |
| F-02 | ALTO | H-03 | Marcador `cci.guarda_ok` preinstalable por PGOPTIONS: guarda vacía + marcador ⇒ los 6 scripts corren sin guarda | matrices_PUB X-10 (6 FAIL) | CORREGIDO (local): tabla temporal + GD-16/X-10 |
| F-03 | MEDIO | H-03 | AUD-G2: el pin de hash sólo existía en documentos del repo; ningún mecanismo de ejecución lo verificaba | LIMITACIONES; INT-10/12 | PARCIAL: envoltorio con hash externo (opcional) + decisión del propietario |
| F-04 | MEDIO | H-03 | AUD-G3 dado por corregido: stdin con guarda homónima forjadora en el cwd pasa en 01/02 | X-07-01A/02A (PARTIAL) | PARCIAL: stdin no soportado; envoltorio fuerza -f |
| F-05 | MEDIO | H-02 | La rama publicada falla su propia reconciliación (alcance contra V26) al evaluarse en git: la carpeta de publicación quedó fuera del alcance admitido | ct_reconciliacion_integral.py; reconciliacion_integral.txt | CORREGIDO (local): ruta autorizada explícita |
| F-06 | MEDIO | H-02 | Contradicciones documentales en la carpeta publicada (85 vs 109 pruebas; hashes 598ad606… vs 07c6673c…; AUD-G1 abierto y corregido; HUECO vs rechaza; condición previa ya aplicada) | AUDITORIA_CONSISTENCIA_H02.md | CORREGIDO (local): documentos vigentes + histórico etiquetado |
| F-07 | BAJO | H-01 | `precondicion_roles.txt` quedaba vacío: sin evidencia del estado de roles antes/después | precondicion_roles_cluster*.txt | CORREGIDO (local) |
| F-08 | BAJO | H-03 | El arnés clasificaba rechazos por subcadena: el eco de un error de sintaxis podía confundirse con un rechazo | INT-05 (primer intento) | CORREGIDO (local): exige `ERROR: NO EJECUTADO` |
| F-09 | BAJO | H-01 | El arnés no soporta ejecución paralela de dos baterías (el paso exc_modelo14 falló en una corrida paralela) | bat2 paralelo (histórico) | ABIERTO: documentado; ejecutar en serie |
| F-10 | BAJO | H-02 | El comparador de clústeres trataba una diferencia de temporización (2.05 s vs 2.06 s) como diferencia de resumen | comparacion_clusteres.txt | CORREGIDO en la herramienta de auditoría (normaliza segundos) |
| F-11 | ESTRUCTURAL | H-03 | Guarda sustituida/forjada, allowlist editada o denylist vaciada: indetectables sin hash externo | INT-06/10/12 | LIMITACIÓN ESTRUCTURAL |
| F-12 | ESTRUCTURAL | H-03 | AG-18: DEV clon/restauración de PROD indistinguible por system_identifier+base | ID-06 | LIMITACIÓN ESTRUCTURAL |
| F-13 | NO VERIFICADO | Supabase | pg_control_system(), TEMP, PGOPTIONS por pooler, project ref | MATRIZ_COMPATIBILIDAD_SUPABASE.md | PENDIENTE de CCI-DEV (sin autorización) |
