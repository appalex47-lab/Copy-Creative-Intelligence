# Compatibilidad Supabase — NO VERIFICADA
| Aspecto | Estado | Nota |
|---|---|---|
| `postgres` no es superusuario | documental, no verificado en vivo | la guarda no requiere superusuario |
| Conexión directa/sesión conserva estado | documental | el marcador de sesión funciona |
| Modo transacción del pooler | rechazo esperado | la tabla temporal no sobrevive; simulado, no real |
| PGOPTIONS vía Supavisor | NO VERIFICADO | puede no reenviarse |
| `pg_control_system()` | NO VERIFICADO | permiso desconocido |
| Privilegio TEMP | NO VERIFICADO | nuevo requisito |
| project ref desde SQL | NO obtenible | no verificado |
Sin validación real no se declara compatibilidad.
