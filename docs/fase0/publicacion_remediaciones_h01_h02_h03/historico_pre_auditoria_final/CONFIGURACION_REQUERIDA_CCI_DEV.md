> **ACTUALIZACIÓN:** la condición previa 'aplicar mitigación AUD-G1' ya está aplicada en el parche. Siguen pendientes los datos de esta tabla, que sólo puede aportar el propietario.

---

# Datos requeridos para habilitar la allowlist real de CCI-DEV
No inventar valores. No enviar contraseñas, tokens ni claves service_role.
| Dato | Cómo obtenerlo (propietario, sólo lectura, sólo CCI-DEV) | Uso |
|---|---|---|
| system_identifier de CCI-DEV | select system_identifier from pg_catalog.pg_control_system(); | allowlist \`sysid|base\` |
| system_identifier de CCI-PROD | misma consulta, **sólo con autorización explícita del propietario y por su propia mano**; esta auditoría no se conecta a PROD | denylist |
| Nombre de base | select current_database(); | allowlist |
| Rol de conexión y su privilegio EXECUTE | select current_user, has_function_privilege(current_user,'pg_catalog.pg_control_system()','execute'); | confirma identidad verificable |
| Project ref de CCI-DEV (y de PROD) | Panel Supabase / host de conexión | contraste manual; no verificable desde el servidor |
| Evidencia de propiedad | captura del panel que muestre ref + nombre del proyecto, y aprobación escrita | trazabilidad |
| Modo de conexión | directa o pooler en modo sesión; confirmar si PGOPTIONS llega | operabilidad |
| SHA-256 aprobado de 00_guarda_destino.sql | calculado tras insertar los valores | pin de integridad (AUD-G2) |
| ¿CCI-DEV es clon/restauración de PROD? | decisión del propietario | si sí, sysid coincide: guarda no distingue |
Condiciones previas: aplicar mitigación AUD-G1; ejecutar sólo con \`-f\` y ruta absoluta.
