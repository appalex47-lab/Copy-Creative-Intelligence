# Informe de hallazgos y resolución (clasificación sin PARTIAL)
Formato por hallazgo: estado previo · causa raíz · solución · archivos · prueba que reproduce · prueba posterior · resultado · desbloqueo.

## F-01a — AG-18: clon físico de PROD indistinguible de DEV (mecanismo)
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: La guarda SQL no distinguía un clon físico (ID-05: la guarda lo aceptaba); no había identidad externa.
- **Causa raíz**: Todo lo guardado en la base (incluida cualquier identidad) se clona con ella; `system_identifier` también.
- **Solución**: Identidad de entorno firmada Ed25519 verificada fuera de la base: token (entorno+proyecto+endpoint+base+system_identifier+serial+vigencia) y política firmada; clave anclada a SHA-256 externo; denegación por defecto; integrada en el ejecutor antes de ejecutar.
- **Archivos** (`scripts_validacion/…`): cci_dev_NO_EJECUTADOS/ct_identidad_entorno.py, ejecutar_script_verificado.sh, ct_pruebas_identidad_firmada.py, ct_pruebas_ext01_y_e2e_dev.py
- **Prueba que reproduce**: ID-05 (guarda sola acepta el clon) y E2E-06..08 sin identidad firmada no existen en la versión anterior
- **Prueba posterior**: AG-00…AG-41 (42/42; clones físicos reales de DEV y PROD por pg_basebackup, 10 casos obligatorios y más) y E2E-01…14
- **Resultado/evidencia**: evidencia/identidad_firmada_ag18.json, evidencia/aprobacion_firmada_ext01_cadena_dev.json; un PROD clonado nunca se aceptó como DEV (I-ENDPOINT-DISTINTO, I-SYSID-DISTINTO, I-ENTORNO-DISTINTO).
- **Desbloqueo**: ver F-01b

## F-01b — AG-18: autoridad emisora real
**Clasificación: BLOQUEADO_CON_CAUSA_DEMOSTRADA**
- **Estado previo**: No existe autoridad ni clave.
- **Causa raíz**: Decisión del propietario (quién emite); no se inventa.
- **Solución**: Especificación + procedimiento de emisión/rotación.
- **Archivos** (`scripts_validacion/…`): ESPECIFICACION_IDENTIDAD_ENTORNO.md
- **Prueba que reproduce**: —
- **Prueba posterior**: —
- **Resultado/evidencia**: Mecanismo probado con claves efímeras.
- **Desbloqueo**: ESPECIFICACION_IDENTIDAD_ENTORNO.md §Quién emite; EXT-01/EXT-02 en PLAN_DESBLOQUEO_EXTERNOS.md

## F-02a — Autorización de operadores (mecanismo)
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: Los operadores solo se protegían con search_path; cualquier rol con el marcador ejecutaba.
- **Causa raíz**: No había identidad de ejecutor ni mínimo privilegio ni separación de funciones.
- **Solución**: En modo DEV la guarda exige session_user = current_user, rol existente sin privilegios elevados, pertenencia a cci_operador, no pertenencia a cci_custodio/cci_administrador (también indirecta/NOINHERIT), RAISE LOG de auditoría; el ejecutor exige registro de auditoría (archivo regular).
- **Archivos** (`scripts_validacion/…`): cci_dev_NO_EJECUTADOS/00_guarda_destino.sql, ejecutar_script_verificado.sh, ct_pruebas_autorizacion_operadores.py
- **Prueba que reproduce**: Versión anterior: cualquier rol pasaba (sin comprobación)
- **Prueba posterior**: AO-01…AO-18 (22/22) + E2E-10…14 (auditoría /dev/null, enlace, FIFO, ruta relativa, no escribible)
- **Resultado/evidencia**: evidencia/autorizacion_operadores.json
- **Desbloqueo**: ver F-02b

## F-02b — Roles y personas reales
**Clasificación: BLOQUEADO_CON_CAUSA_DEMOSTRADA**
- **Estado previo**: No existen los roles cci_* ni operadores nombrados.
- **Causa raíz**: No se concede ningún privilegio real ni se inventan usuarios.
- **Solución**: PROCEDIMIENTO_ROLES_CCI_DEV.sql (plantilla, NO ejecutada) y MATRIZ_AUTORIZACION_OPERADORES.md.
- **Archivos** (`scripts_validacion/…`): PROCEDIMIENTO_ROLES_CCI_DEV.sql, MATRIZ_AUTORIZACION_OPERADORES.md
- **Prueba que reproduce**: —
- **Prueba posterior**: —
- **Resultado/evidencia**: —
- **Desbloqueo**: El administrador aplica la plantilla con aprobación del propietario; verificar con la consulta de la plantilla (t/f/f).

## F-03 — 05A/05B: circularidad y autovalidación
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: B podía imprimir PASS midiendo su propia espera, sin prueba independiente de que A retuviera el bloqueo.
- **Causa raíz**: Productor y validador eran la misma sesión; sin fuente independiente.
- **Solución**: A fija application_name y emite pid/xid; B exige en el servidor (pg_stat_activity) la presencia de A o BLOCKED; B solo emite `veredicto_propio`; el PASS lo da `ct_verificar_05.py` con muestras de un observador en otra conexión.
- **Archivos** (`scripts_validacion/…`): 05_concurrencia_sesion_A.sql, 05_concurrencia_sesion_B.sql, ct_verificar_05.py, ct_pruebas_05_secuencia.py, ct_aserciones_smoke.py
- **Prueba que reproduce**: Versión anterior (B imprimía PASS)
- **Prueba posterior**: ct_pruebas_05_secuencia.py: P1–P3 y N1–N12 (borrar, alterar, intercambiar salidas; pid falso; observador ausente/ajeno; evidencia de otra ejecución; B solo; impostores)
- **Resultado/evidencia**: evidencia/secuencia_05.json (15/15)
- **Desbloqueo**: Concurrencia real en CCI-DEV: EXT-04-L06

## F-04 — H-02: integridad de evidencias y circularidad de salidas
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: La reconciliación aceptaba PASS con evidencia vacía; el verificador exceptuaba sus propias salidas (regen) y era evidencia de sí mismo; marcadores para salidas generadas después.
- **Causa raíz**: El verificador y lo verificado compartían directorio y confianza.
- **Solución**: ID único, fuente, método, ejecución, fecha y SHA-256 por comprobación; vacío → FAIL; anclaje EXTERNO (ct_anclas_evidencia.py, ANCLAS_EVIDENCIA.json fuera del directorio de cierre) de SHA-256, totales del stdout e id de ejecución; verificación en I y K.
- **Archivos** (`scripts_validacion/…`): ct_reconciliacion_integral.py, ct_verificar_consistencia_informe.py, ct_anclas_evidencia.py, ct_orquestador_fase0.py
- **Prueba que reproduce**: Ataques del verificador (12) y del anclaje: modificación coherente de JSON+TXT, MD alterado, JSON borrado, comprobación de otra ejecución, anclas ajenas/ausentes, totales del stdout
- **Prueba posterior**: evidencia/ANCLAS_EVIDENCIA.json, pasos/controles_anclas.txt, controles de consistencia
- **Resultado/evidencia**: RECON 58 comprobaciones PASS; controles negativos PASS
- **Desbloqueo**: —

## F-05 — Orquestador fail-fast
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: Sin NOT_TESTED, sin meta-prueba, excepciones sin clasificar.
- **Causa raíz**: No se había demostrado con fallos inducidos.
- **Solución**: Estado NOT_TESTED (nunca PASS), excepción técnica → FAILED, fallo/bloqueo/excepción/mutación inyectados en cada etapa A–K; run id nuevo por ejecución.
- **Archivos** (`scripts_validacion/…`): ct_orquestador_fase0.py, ct_pruebas_orquestador_fallos.py
- **Prueba que reproduce**: —
- **Prueba posterior**: ORQ-S00…ORQ-K-*, ORQ-NT, ORQ-R1 (árbol sucio), ORQ-R2 (SUMS alterado) = 49/49
- **Resultado/evidencia**: pasos/orquestador_meta_fallos.json y corrida real con exit 2
- **Desbloqueo**: —

## F-06 — EXT-01 mecanismo de aprobación firmada
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: Solo hash en argumento, sin firma ni caducidad.
- **Causa raíz**: Sin formato de aprobación ni verificación criptográfica.
- **Solución**: Aprobación Ed25519 (aprobacion_integridad) con clave anclada, caducidad, revocación, rotación.
- **Archivos** (`scripts_validacion/…`): ejecutar_script_verificado.sh
- **Prueba que reproduce**: —
- **Prueba posterior**: EXT01-01…22
- **Resultado/evidencia**: evidencia/aprobacion_firmada_ext01_cadena_dev.json
- **Desbloqueo**: Custodio real: EXT-01 (BLOQUEADO)

## F-07 — EXT-01/EXT-02/EXT-03 — insumos reales
**Clasificación: BLOQUEADO_CON_CAUSA_DEMOSTRADA**
- **Estado previo**: No existen custodio, CCI-DEV accesible ni identificadores de destino.
- **Causa raíz**: Son insumos del propietario; PROD no puede consultarse.
- **Solución**: Fichas + herramientas: ct_validar_listas_destinos.py (34/34), ct_ext02_validar_supabase_dev.py (7/7 local simulada).
- **Archivos** (`scripts_validacion/…`): PLAN_DESBLOQUEO_EXTERNOS.md
- **Prueba que reproduce**: —
- **Prueba posterior**: —
- **Resultado/evidencia**: Etapa K: BLOCKED/NOT_TESTED
- **Desbloqueo**: Ver fichas EXT-01, EXT-02, EXT-03

## F-08 — EXT-04 L04, L05, L06, L07, L08 (individuales)
**Clasificación: BLOQUEADO_CON_CAUSA_DEMOSTRADA**
- **Estado previo**: NOT VERIFIED en la matriz V26 (no se modificó).
- **Causa raíz**: L04 sin esquema físico aprobado; L05/L06 sin CCI-DEV; L07 sin trigger físico (G-1/G-5/G-10 no aceptados); L08: la Adenda v9 no está en el repositorio (solo referencias de estado; el registro menciona además 'addendum v3': inconsistencia de versión sin documento).
- **Solución**: Una ficha por control con razón, procedimiento y criterio.
- **Archivos** (`scripts_validacion/…`): PLAN_DESBLOQUEO_EXTERNOS.md
- **Prueba que reproduce**: —
- **Prueba posterior**: —
- **Resultado/evidencia**: K: EXT-04-L04…L08 BLOCKED por separado
- **Desbloqueo**: Ver fichas L04…L08

## F-11 — Operadores sin calificar en los 6 scripts SQL (SPD7)
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: Con el chequeo de search_path eliminado, 4/6 scripts eran secuestrables por operadores hostiles (= y ||).
- **Causa raíz**: Los operadores (=, ||, IN, joins) no pueden calificarse uno a uno de forma fiable; resolvían por el search_path del llamador.
- **Solución**: La guarda fija, tras superar sus comprobaciones, el search_path de SESIÓN a pg_catalog, public, pg_temp (\gset). Además se corrigió un defecto latente en 04 (`'||:post_count||'` con -1 se lexaba como operador ||-) usando casts y espacios.
- **Archivos** (`scripts_validacion/…`): cci_dev_NO_EJECUTADOS/00_guarda_destino.sql, 04_trigger_r1_r9_ROLLBACK.sql
- **Prueba que reproduce**: Versiones anteriores: operadores hostiles ejecutados (SPD8, control positivo)
- **Prueba posterior**: SPD6/SPD7: 0 secuestros de operador por script; SPD1-SPD5 sin regresión
- **Resultado/evidencia**: evidencia/auditoria_search_path.json
- **Desbloqueo**: Residuo: homónimos EXACTOS de pg_catalog no pueden ser superados desde public (el orden pone pg_catalog primero); homónimos más específicos en public siguen siendo un límite aceptado de un esquema permitido

## F-09 — Registro de auditoría anulable (hallado en la revisión adversarial de esta operación)
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: CCI_AUDITORIA_LOG=/dev/null (o enlace/FIFO) permitía ejecutar sin registro real.
- **Causa raíz**: Solo se comprobaba que la escritura no fallara.
- **Solución**: El ejecutor exige archivo regular, ruta absoluta, no enlace/dispositivo/FIFO y verifica que la línea de inicio quedó registrada.
- **Archivos** (`scripts_validacion/…`): ejecutar_script_verificado.sh
- **Prueba que reproduce**: E2E-10 (con el comportamiento anterior `>> /dev/null` siempre tiene éxito)
- **Prueba posterior**: E2E-10…14
- **Resultado/evidencia**: evidencia/aprobacion_firmada_ext01_cadena_dev.json
- **Desbloqueo**: —

## F-10 — Pruebas heredadas que fallaban con los cambios (arnés, no defecto de seguridad)
**Clasificación: RESUELTO_VERIFICADO**
- **Estado previo**: WRAP-*, GD-01/GD-11 e ID-01/07 fallaron al exigir 11 archivos / operador / auditoría.
- **Causa raíz**: Las pruebas asumían 10 archivos y un superusuario como operador DEV.
- **Solución**: Adaptadas (fixtures de operador, 11 archivos); la detección se mantiene.
- **Archivos** (`scripts_validacion/…`): ct_pruebas_adversariales_cierre.py, ct_pruebas_guarda_destino.py, ct_pruebas_identidad_cierre.py, ct_escaner_seguridad_sql.py
- **Prueba que reproduce**: Corrida 5 (FAILED en C)
- **Prueba posterior**: Corridas 6–9
- **Resultado/evidencia**: Corrida final
- **Desbloqueo**: —

