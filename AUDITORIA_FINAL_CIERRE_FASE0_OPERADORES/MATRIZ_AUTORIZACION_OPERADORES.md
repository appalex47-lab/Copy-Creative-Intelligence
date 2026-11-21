# MATRIZ DE AUTORIZACIÓN DE OPERADORES (modo CCI-DEV)

Estado: **implementada en la guarda SQL y probada** (22/22, `ct_pruebas_autorizacion_operadores.py`). **No se creó ningún usuario ni se concedió ningún privilegio real**: los roles son fixtures de un PostgreSQL local temporal. El SQL a aplicar está en `PROCEDIMIENTO_ROLES_CCI_DEV.sql` (plantilla, no ejecutada).

## Problema (causa raíz)
Proteger a los operadores sólo con `search_path` no demuestra *quién* ejecuta ni limita *qué* puede hacer. La guarda aceptaba a cualquier rol que llegara con el marcador correcto.

## Roles
| Rol | Quién | Puede | No puede |
|---|---|---|---|
| `cci_operador` (grupo) | Personas que ejecutan los 6 scripts | Ejecutar scripts aprobados por el ejecutor; lectura/ROLLBACK | Ser superusuario, CREATEROLE, CREATEDB, BYPASSRLS, REPLICATION; ser custodio o administrador |
| `cci_custodio` (grupo) | Persona/sistema que firma la aprobación del SHA-256 | Firmar el manifiesto de integridad | Ejecutar scripts |
| `cci_administrador` (grupo) | Administra roles y esquema de CCI-DEV | Crear/retirar operadores | Ejecutar scripts |

## Controles en la guarda (denegación por defecto) y códigos
| Control | Código |
|---|---|
| `session_user = current_user` (sin `SET ROLE` ni `SET SESSION AUTHORIZATION` previos) | `G-ROL-CAMBIADO` |
| El rol existe | `G-OPERADOR-DESCONOCIDO` |
| Sin SUPERUSER/CREATEROLE/CREATEDB/BYPASSRLS/REPLICATION | `G-OPERADOR-PRIVILEGIO-EXCESIVO` |
| Los grupos `cci_*` existen (los creó el administrador) | `G-OPERADOR-ROLES-NO-CONFIGURADOS` |
| Miembro (directo o indirecto) de `cci_operador` | `G-OPERADOR-NO-AUTORIZADO` |
| No miembro de `cci_custodio`/`cci_administrador` (ni con NOINHERIT ni por cadena) | `G-SEPARACION-FUNCIONES` |
| CREATE efectivo sobre `public` (directo, por PUBLIC, heredado o por propiedad) | `G-OPERADOR-CREATE-EN-PUBLIC` |
| CREATE efectivo sobre la base | `G-OPERADOR-CREATE-EN-BASE` |
| Ningún OTRO rol no superusuario con CREATE en `public` (no pueden plantar operadores entre la comprobación y la ejecución) | `G-PUBLIC-CREATE-AJENO` |
| Sin membresía (aunque NOINHERIT/indirecta) de roles con SUPERUSER/CREATEROLE/CREATEDB/BYPASSRLS/REPLICATION | `G-OPERADOR-MEMBRESIA-PRIVILEGIADA` |
| Sin operadores en `public`/temporales (salvo extensiones con símbolo no estándar) ni casts de usuario (todos los modos) | `G-OPERADOR-AJENO-EN-SEARCH-PATH`, `G-CAST-AJENO` |
| Registro de quién ejecuta: `RAISE LOG 'CCI-AUDITORIA operador=… pid=…'` (servidor) + `CCI_AUDITORIA_LOG` (INICIO/FIN con usuario del SO, usuario de BD, destino, script, SHA-256, run id) | `V-AUDITORIA-NO-CONFIGURADA` si falta |

## Pruebas (22/22)
Sin roles configurados; operador autorizado + registro de auditoría; rol sin pertenencia; superusuario; CREATEROLE, CREATEDB, BYPASSRLS, REPLICATION; operador+custodio; operador+administrador; membresía indirecta; NOINHERIT; `SET ROLE`; `search_path` hostil (con y sin el chequeo de search_path: sólo la calificación `pg_catalog.` ya bloquea); GUC `cci.*` preinstaladas por PGOPTIONS; parámetros de sesión (`row_security=off`, `default_transaction_read_only=off`); `session_replication_role=replica` (lo rechaza PostgreSQL antes de la guarda); `application_name` impostor; ausencia de efectos persistentes. En todos los rechazos: el cuerpo del script **no** se ejecuta (canario ausente).

## Procedimiento de incorporación de un operador (propietario/administrador)
1. El propietario autoriza por escrito a la persona. 2. El administrador (≠ operador) crea el rol de login y lo agrega a `cci_operador` (SQL de la plantilla). 3. Verificar con la consulta de la plantilla (esperado t/f/f) y archivar la salida. 4. La autoridad de identidad emite/renueva el token del entorno. 5. El operador ejecuta **sólo** mediante `ejecutar_script_verificado.sh`. 6. Baja: `revoke cci_operador from <rol>; drop role <rol>` y archivar.

## Límites
- Las contraseñas/credenciales de login y la asignación de personas reales no se definieron aquí.
- La guarda no puede impedir que un superusuario/propietario de la base edite la propia guarda; lo mitigan el hash aprobado y la separación de funciones.
- Los privilegios exactos para 03/04/05 sobre el esquema físico dependen de L04/L05 (no existe esquema físico aprobado).
