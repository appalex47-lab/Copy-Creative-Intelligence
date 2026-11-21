# Datos requeridos para habilitar la allowlist real de CCI-DEV — VIGENTE
No inventar valores; no enviar contraseñas, tokens ni claves service_role. Todo lo siguiente lo aporta el propietario, en CCI-DEV y en sólo lectura:
| Dato | Obtención | Uso |
|---|---|---|
| system_identifier de CCI-DEV | `select system_identifier from pg_catalog.pg_control_system();` | allowlist `sysid|base` |
| system_identifier de CCI-PROD | misma consulta, sólo con autorización expresa y por el propietario | denylist |
| Base y rol de conexión | `select current_database(), current_user;` | allowlist |
| EXECUTE del rol sobre `pg_control_system()` | `select has_function_privilege(current_user,'pg_catalog.pg_control_system()','execute');` | si es falso, la guarda rechaza (fail-closed) |
| Permiso TEMP del rol | `select has_database_privilege(current_user,current_database(),'temp');` | la guarda crea la tabla temporal marcador; sin TEMP rechaza |
| Project ref de CCI-DEV/PROD | panel / host de conexión | contraste manual (no verificable desde el servidor) |
| Modo de conexión | directa o pooler en modo sesión; confirmar que PGOPTIONS llega | operabilidad |
| SHA-256 aprobado de la guarda | `sha256sum 00_guarda_destino.sql` tras insertar los valores, **guardado fuera del repositorio** | argumento de `ejecutar_script_verificado.sh` |
| ¿CCI-DEV es clon/restauración de PROD? | decisión del propietario | si sí, la guarda no los distingue |
Ejecutar siempre con `-f` y ruta absoluta o con el envoltorio verificado.
