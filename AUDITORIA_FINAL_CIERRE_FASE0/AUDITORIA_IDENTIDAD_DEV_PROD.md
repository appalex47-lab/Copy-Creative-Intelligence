# Auditoría de identidad DEV/PROD y AG-18
| ID | Ataque | Esperado | Observado | Estado | Justificación |
|---|---|---|---|---|---|
| ID-00 | comparar system_identifier | distintos | distintos | PASS | huella md5 DEV=67e8231f PROD=3b9283bd |
| ID-01 | script 01 contra DEV | GUARDA OK | rc=0 GUARDA OK | PASS |  |
| ID-02 | script 01 contra PROD declarando DEV | [G-PROD-RECHAZADO] | rc=3 G-PROD-RECHAZADO | PASS |  |
| ID-03 | script 01 contra PROD con base del mismo nombre | [G-DESTINO-DESCONOCIDO] (identidad por system_identifier+base) | rc=3 G-DESTINO-DESCONOCIDO | PASS | la allowlist por sí sola ya rechaza cualquier otro clúster |
| ID-04 | leer system_identifier del clon | IGUAL al de DEV (la identidad técnica se hereda) | igual | PASS | comprueba la premisa de AG-18: un clon físico NO cambia system_identifier |
| ID-05 | ejecutar el script 01 contra el CLON con variables DEV (AG-18) | el clon es indistinguible: la guarda lo ACEPTA (no es una aprobación; límite estructural) | rc=0 GUARDA OK (aceptado) | PARTIAL | LIMITACIÓN ESTRUCTURAL AG-18: system_identifier+base no distinguen un clon físico/restauración de su origen |
| ID-06 | ejecutar contra el 'DEV' y contra el clon | ambos RECHAZADOS (falla cerrada) pero se bloquea también el DEV legítimo | DEV: G-PROD-RECHAZADO; clon: G-PROD-RECHAZADO | PARTIAL | seguro pero inservible: sin una identidad externa no se pueden distinguir |
| ID-07 | ejecutor verificado contra DEV | ejecuta | rc=0 GUARDA OK | PASS |  |
| ID-08 | ejecutor verificado contra el CLON con la lista externa que sólo aprueba el endpoint de DEV | [V-DESTINO-NO-APROBADO] | rc=3 V-DESTINO-NO-APROBADO | PASS | la identidad EXTERNA (endpoint aprobado por el propietario) sí distingue el clon, con límites: alias DNS/poolers y restauraciones en el mismo endpoint (ver ID-09) |
| ID-09 | ejecutor contra el clon sin lista externa | [V-DESTINO-NO-CONFIGURADO] | rc=3 V-DESTINO-NO-CONFIGURADO | PASS | si el propietario no configura la lista externa, el modo DEV no opera por el ejecutor |
| ID-10 | ejecutor contra el clon con endpoint aprobado | pasa (error de configuración del propietario: no es defensa) | rc=0 GUARDA OK | PARTIAL | la protección es tan buena como la lista externa; una restauración sobre el MISMO endpoint no se distingue |
| ID-11 | script 01 contra el clúster PROD con el contenido de DEV | [G-DESTINO-DESCONOCIDO] (otro system_identifier) | rc=3 G-DESTINO-DESCONOCIDO | PASS | un clon lógico no hereda system_identifier |
| ID-12 | inyectar cci.system_identifier y cci.dev_allow | ignoradas: [G-DESTINO-DESCONOCIDO] | rc=3 G-DESTINO-DESCONOCIDO | PASS |  |
| ID-13 | system_identifier/pg_control_system() y project ref desde SQL en Supabase | NOT TESTED | NOT TESTED | NOT TESTED | requiere CCI-DEV con autorización; el project ref no es consultable desde SQL según la documentación consultada (sin confirmar) |

**Qué distingue la arquitectura:** `system_identifier` + nombre de base identifican el clúster físico. Un clon físico (pg_basebackup) conserva la misma identidad → no se distingue (AG-18, PARTIAL estructural). Un clon lógico (dump/restore) sí difiere. **Qué no distingue:** DEV vs PROD tras clon físico; project ref de Supabase (no obtenible desde SQL; no verificado).
**Identidad externa:** lista `CCI_DESTINOS_APROBADOS` comprobada por el envoltorio (límites: alias DNS/pooler, restauración en el mismo endpoint). **Requisitos del propietario:** poblar listas allow/deny (hoy vacías), definir endpoints aprobados, decidir si CCI-DEV es clon de PROD, custodio del hash.
