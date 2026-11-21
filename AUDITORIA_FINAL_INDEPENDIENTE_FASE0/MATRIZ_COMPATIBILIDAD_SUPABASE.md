# Matriz de compatibilidad con Supabase (sin conexión a ningún proyecto)
Clasificación: **CONF** = confirmado por documentación pública consultada; **LOCAL** = probado en PostgreSQL local (no es Supabase); **INF** = inferido técnicamente; **NV** = no verificado; **CCI-DEV** = requiere prueba en CCI-DEV (con autorización).
| Tema | Clase | Detalle |
|---|---|---|
| Disponibilidad de `pg_control_system()` | NV / CCI-DEV | No hallé documentación de Supabase que lo confirme ni lo niegue. LOCAL: ejecutable por superusuario; con `REVOKE EXECUTE` ⇒ la guarda rechaza (`G-IDENTIDAD-NO-VERIFICABLE`). |
| Permisos para ejecutarlo | NV / CCI-DEV | Depende del rol de conexión; prueba E0 de sólo lectura (ver CONFIGURACION). |
| Rol `postgres` de Supabase | CONF | No es superusuario; `supabase_admin` es el superusuario reservado. |
| Conexión directa | CONF | Mantiene estado de sesión. |
| Supavisor modo sesión | CONF | Mantiene estado de sesión (la doc de cadenas de conexión). |
| Supavisor modo transacción | CONF | Pierde el estado de sesión (SET, etc.). INF: la guarda crea una tabla temporal por sesión; en modo transacción el marcador no sobreviviría ⇒ los scripts rechazarían (fail-closed, inoperable). Los scripts 05A/B requieren sesión. |
| Reenvío de `PGOPTIONS`/opciones de arranque por el pooler | NV / CCI-DEV | La doc consultada no menciona startup options; un issue público de Supavisor sugiere que la opción puede ignorarse (estado actual no verificado). INF: si no llega, `G-CONFIG-INCOMPLETA` (fail-closed). |
| Persistencia de parámetros de sesión | CONF/INF | Según modo (arriba). |
| Identidad confiable del proyecto desde SQL | NV | No hallé mecanismo documentado (discusión pública sin respuesta confirmada). El project ref está en el host/usuario de conexión del cliente, no en el servidor. |
| Privilegio TEMP del rol (nuevo requisito de la guarda corregida) | NV / CCI-DEV | La guarda crea `pg_temp.cci_guarda_ok`; sin TEMP rechaza (fail-closed). |
| Riesgo de un marcador configurable por el operador | LOCAL | Variable `cci.guarda_ok` preinstalable por PGOPTIONS (X-10 en la rama publicada, 6/6 bypass) ⇒ sustituida por tabla temporal (no preinstalable). |
| Distinguir DEV y PROD en todos los escenarios | LOCAL/estructural | No es posible con sólo `system_identifier`+base si DEV es clon de PROD; riesgo residual: ejecución en un clon indistinguible. Mitigación sólo por decisión/controles externos (registro de PROD en denylist, hash externo). |
Nada de lo anterior se convirtió en PASS: toda fila NV/CCI-DEV está pendiente de validación física con autorización expresa.
