# Informe de privilegios efectivos

Todos los resultados provienen de comprobaciones del servidor (`has_schema_privilege`, `has_database_privilege`, `pg_has_role`, `pg_roles`, `pg_default_acl`), no de las declaraciones originales de los roles. Los roles son fixtures de un PostgreSQL local efímero; **no se inspeccionó ningún CCI-DEV real ni Supabase**.

## Casos (modo DEV, guarda NEW frente a guarda VULN = 404f5adc)
| ID | Descripción | Rol | Esperado (NEW) | Observado (NEW) | VULN acepta al rol | Estado |
|---|---|---|---|---|---|---|
| P-00 | línea base: operador legítimo (miembro de cci_operador, sin CREATE en public/base) | t_ok | operador legítimo ACEPTADO (sin regresión) | GUARDA OK | True | PASS |
| P-01 | CREATE en public por concesión directa | t_ok | rechazo G-OPERADOR-CREATE-EN-PUBLIC sin canario | G-OPERADOR-CREATE-EN-PUBLIC | True | PASS |
| P-02 | CREATE en public concedido a PUBLIC (efectivo para todos los roles) | t_ok | rechazo G-OPERADOR-CREATE-EN-PUBLIC sin canario | G-OPERADOR-CREATE-EN-PUBLIC | True | PASS |
| P-03 | CREATE en public HEREDADO por pertenencia (INHERIT) a un grupo | t_herd | rechazo G-OPERADOR-CREATE-EN-PUBLIC sin canario | G-OPERADOR-CREATE-EN-PUBLIC | True | PASS |
| P-04 | grupo con CREATE en public con el operador NOINHERIT (podría recuperarlo con SET ROLE; además un rol ajeno con CREATE queda detectado) | t_noinh | rechazo G-PUBLIC-CREATE-AJENO sin canario | G-PUBLIC-CREATE-AJENO | True | PASS |
| P-05 | operador NOINHERIT miembro de un rol SUPERUSER (recupera todo con SET ROLE) | t_nosu | rechazo G-OPERADOR-MEMBRESIA-PRIVILEGIADA sin canario | G-OPERADOR-MEMBRESIA-PRIVILEGIADA | True | PASS |
| P-06 | miembro (heredando) de un rol CREATEROLE: efectivo e indirecto | t_cr_m | rechazo G-OPERADOR-MEMBRESIA-PRIVILEGIADA sin canario | G-OPERADOR-MEMBRESIA-PRIVILEGIADA | True | PASS |
| P-07 | CREATE sobre la BASE (permite crear esquemas auxiliares, p. ej. uno con su propio nombre) | t_db | rechazo G-OPERADOR-CREATE-EN-BASE sin canario | G-OPERADOR-CREATE-EN-BASE | True | PASS |
| P-08 | operador PROPIETARIO del esquema public (CREATE implícito por propiedad) | t_own | rechazo G-OPERADOR-CREATE-EN-PUBLIC sin canario | G-OPERADOR-CREATE-EN-PUBLIC | True | PASS |
| P-09 | OTRO rol (no el operador) con CREATE en public puede plantar operadores entre la comprobación y la ejecución | t_ok | rechazo G-PUBLIC-CREATE-AJENO sin canario | G-PUBLIC-CREATE-AJENO | True | PASS |
| P-10 | ALTER DEFAULT PRIVILEGES sobre tablas/funciones de public NO confiere CREATE sobre el esquema (informativo: el operador sigue aceptado) | t_ok | operador legítimo ACEPTADO (sin regresión) | GUARDA OK | True | PASS |
| P-11 | E2E: operador AUTORIZADO con CREATE residual en public crea el operador y, con la guarda anterior, el siguiente script resuelve al operador hostil; con la guarda nueva se rechaza antes | t_ok | rechazo G-OPERADOR-CREATE-EN-PUBLIC | G-OPERADOR-CREATE-EN-PUBLIC | True | PASS |
| P-12 | tras superar la guarda, el operador (sin CREATE) intenta crear una función/operador en public: rechazado por PostgreSQL | t_ok | permission denied for schema public | permission denied | True | PASS |
| P-13 | CREATE/TEMP en pg_temp: el operador conserva TEMP (lo necesita el marcador); la resolución ignora pg_temp para operadores (ver G-01) | t_ok | TEMP concedido; sin efecto sobre la resolución | TEMP=t; ver G-01 | True | PASS |

## Privilegios efectivos encontrados en la base de prueba al final de la suite (tras limpiar los roles fixture)
Propietario del esquema `public`: `pg_database_owner` · ACL por defecto: `ERROR:  operator is not unique: text || "char"
LINE 1: ...ng_agg(pg_catalog.pg_get_userbyid(defaclrole)||':'||defaclob...
                                                             ^
HINT:  Could not choose a best candidate operator. You might need to add explicit type casts.`.
| Rol | super | createrole | createdb | bypassrls | replication | inherit | CREATE public (efectivo) | USAGE public | CREATE base (efectivo) | TEMP base | miembro de (efectivo) |
|---|---|---|---|---|---|---|---|---|---|---|---|
| cci_test | t | f | f | f | f | t | t | t | t | t | anon,authenticated,cci_administrador,cci_custodio,cci_operador,postgres,service_role,t_cr_grp,t_cr_m,t_db,t_grp,t_herd,t_id_op,t_noinh,t_nosu,t_ok,t_otro,t_own,t_su_grp |
| postgres | t | t | t | t | t | t | t | t | t | t | anon,authenticated,cci_administrador,cci_custodio,cci_operador,cci_test,service_role,t_cr_grp,t_cr_m,t_db,t_grp,t_herd,t_id_op,t_noinh,t_nosu,t_ok,t_otro,t_own,t_su_grp |
| t_cr_m | f | f | f | f | f | t | f | t | f | t | cci_operador,t_cr_grp |
| t_db | f | f | f | f | f | t | f | t | f | t | cci_operador |
| t_herd | f | f | f | f | f | t | f | t | f | t | cci_operador,t_grp |
| t_noinh | f | f | f | f | f | f | f | t | f | t | cci_operador,t_grp |
| t_nosu | f | f | f | f | f | f | f | t | f | t | cci_operador,t_su_grp |
| t_ok | f | f | f | f | f | t | f | t | f | t | cci_operador |
| t_own | f | f | f | f | f | t | f | t | f | t | cci_operador |
| t_su_grp | t | f | f | f | f | t | t | t | t | t | anon,authenticated,cci_administrador,cci_custodio,cci_operador,cci_test,postgres,service_role,t_cr_grp,t_cr_m,t_db,t_grp,t_herd,t_id_op,t_noinh,t_nosu,t_ok,t_otro,t_own |

## Concesiones residuales identificadas y su efecto
- **CREATE por PUBLIC / directo / heredado / propiedad sobre `public`** (P-01, P-02, P-03, P-08): la guarda anterior aceptaba al rol; P-11 demuestra el efecto (el operador autorizado plantó el operador y secuestró el script). Ahora `G-OPERADOR-CREATE-EN-PUBLIC`.
- **Grupo con CREATE + operador NOINHERIT** (P-04) y **otro rol con CREATE** (P-09): `has_schema_privilege(operador)` es falso, pero el rol puede recuperar el privilegio (SET ROLE) o plantar operadores en paralelo → `G-PUBLIC-CREATE-AJENO`.
- **Operador NOINHERIT miembro de un rol SUPERUSER/CREATEROLE** (P-05, P-06): la guarda anterior sólo miraba los atributos del rol de login → ahora `G-OPERADOR-MEMBRESIA-PRIVILEGIADA`.
- **CREATE sobre la base** (P-07): permite crear un esquema con el nombre del rol (`"$user"`) → `G-OPERADOR-CREATE-EN-BASE`.
- **ALTER DEFAULT PRIVILEGES** (P-10): sólo afecta a tablas/funciones; no confiere CREATE sobre el esquema (informativo; el operador legítimo sigue aceptado).
- **pg_temp** (P-13, G-01): el operador conserva TEMP (lo necesita el marcador); PostgreSQL no resuelve operadores en `pg_temp`.
- **Separación de funciones**: 22/22 pruebas de autorización de operadores siguen pasando (ver INFORME_REGRESION.md).

## No verificado
Privilegios reales de los roles de plataforma de Supabase en CCI-DEV (`anon`, `authenticated`, `service_role`, `postgres`, `supabase_admin`…); permisos de ejecución de funciones del lado del servidor distintos de los comprobados; ACL de objetos del esquema físico aprobado (no existe). Instrucciones: ficha ampliada en `PLAN_DESBLOQUEO_EXTERNOS.md`.
