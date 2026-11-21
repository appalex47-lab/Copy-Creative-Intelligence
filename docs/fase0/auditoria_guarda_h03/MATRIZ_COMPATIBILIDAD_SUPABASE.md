# Matriz de compatibilidad Supabase (sin conexión real; nada simulado como respuesta de Supabase)
| Capacidad | Estado | Fuente / nota |
|---|---|---|
| pg_control_system() disponible | **NO VERIFICADO** | En PostgreSQL 16 estándar tiene EXECUTE a PUBLIC (probado local). No encontré documentación de Supabase que confirme ni niegue su ejecución por el rol \`postgres\`. |
| Ejecutable por el rol usado | **NO VERIFICADO** | Depende de privilegios por base. Prueba E0 de lectura del propietario (abajo). |
| No ejecutable | Comportamiento de la guarda: rechaza (G-IDENTIDAD-NO-VERIFICABLE), probado local AG-19 | Falla cerrada. |
| Rol postgres no es superusuario | Documentado por Supabase | supabase_admin es el superusuario de arranque y está reservado. |
| Project ref desde SQL | No encontré mecanismo documentado | Discusión supabase#12639 sin respuesta confirmada. El ref está en el host/usuario de conexión (db.<ref>.supabase.co, usuario postgres.<ref>) que conoce el cliente, no el servidor. |
| Conexión directa 5432 / pooler modo sesión | Mantienen estado de sesión | Documentación de cadenas de conexión de Supabase. |
| Pooler modo transacción (6543) | Pierde estado de sesión (SET, etc.) | Misma doc. 05A/05B necesitan sesión. |
| PGOPTIONS / startup options vía pooler | **NO VERIFICADO** (issue Supavisor #206 sugiere que puede ignorarse) | Falla cerrada si no llegan. |
| Alternativa: marcador en la base | Propuesta, no probada en Supabase | El propietario fija \`ALTER DATABASE postgres SET cci.proyecto='<ref>'\` en CCI-DEV (cambio de DEV: requiere su autorización) y la guarda lo compara. Un marcador es declaración, no prueba, salvo que PROD no lo tenga y se combine con sysid. |

## Prueba E0 (solo lectura, la ejecuta el propietario sólo en CCI-DEV)
select system_identifier from pg_catalog.pg_control_system(); select current_database(), current_user, has_function_privilege(current_user,'pg_catalog.pg_control_system()','execute'); select rolname from pg_roles where rolname like 'supabase%';
Devolver los resultados (sin contraseñas ni claves).
