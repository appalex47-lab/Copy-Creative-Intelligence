# 02 — Matriz de trazabilidad: contratos provisionales ↔ diseño de Fase 0

Estados: **COINCIDE** · **DISCREPANCIA** · **SIN_DISEÑO** (el diseño no define el dato) · **PENDIENTE_DE_DECISIÓN** (requiere decisión del propietario) · **NO_APLICA** (concepto solo de la aplicación).
**Todas las filas: validadas contra un diseño NO aprobado.** Fuentes: F2…F7 de `01_INVENTARIO_FUENTES.md`.

| ID | Contrato (código actual) | Elemento | Diseño de referencia | Estado | Detalle |
|---|---|---|---|---|---|
| T01 | `UserIdentity` | Existencia de la entidad | F2 tabla `profiles` («datos de la persona, 1:1 con auth.users»); F4 #2 | COINCIDE (concepto) | `profiles` existe en diseño; ausente en el fixture (SIN_PRUEBA) |
| T02 | `UserIdentity.id` | Identificador | `profiles` 1:1 `auth.users` | COINCIDE (concepto) | Tipo físico (uuid) no definido en F2/F3 |
| T03 | `UserIdentity.displayName` | Nombre visible | — | SIN_DISEÑO | Columnas de `profiles` no definidas (F3 RR-33: «columnas exactas v3.3 no define») |
| T04 | `UserIdentity.origin` | Marca DEMO/backend | — | NO_APLICA | Concepto de la UI |
| T05 | `Organization` | Entidad | F2 `organizations` («raíz del aislamiento»); F4 #1 | COINCIDE | |
| T06 | `Organization.name` | Nombre | F4 #1: el fixture solo tiene `id` | SIN_DISEÑO | Columna no definida |
| T07 | `OrganizationService.listForCurrentUser` | Alcance «del usuario actual» | F2: RLS solo miembros | COINCIDE (concepto) | Sin RLS probada (F4: SIN_PRUEBA) |
| T08 | `Membership` | Entidad (persona en organización) | F2 #3 `memberships`; F4 #3 (PK org,user en fixture) | COINCIDE | |
| T09 | `Membership.userId/organizationId` | Clave compuesta | F4 #3: PK (org, user) **solo en el fixture** | COINCIDE (fixture) | No hay PK definida en la especificación |
| T10 | `Membership.active` | Membresía activa | F4 #3: columna **`activo`** (fixture); F3 usa «miembro activo» y, en `channel_formats`, `active` | DISCREPANCIA (nombre) | `active` vs `activo`. La FK no comprueba `activo` (F4 EX-G9j). Convención de nombres → decisión |
| T11 | `Membership.roles` | Varios roles por persona | F2 D-04 «varios por persona»; F4 #3 «roles no vacío» | DISCREPANCIA (menor) | El tipo `readonly MembershipRole[]` admite lista vacía; el diseño exige no vacío |
| T12 | `MembershipRole` `'design'` | Clave de rol | F2 l.424: **`diseno`** | DISCREPANCIA (nombre) | Ver `03_CONSISTENCIA.md` §4 |
| T13 | `MembershipRole` `'reviewer'` | Clave de rol | F2 l.424: **`revisor_aprobador`** («Revisor / Aprobador» en la matriz de permisos) | DISCREPANCIA (nombre) | F3 usa «reviewer» solo en prosa/eventos (`reviewer.assigned`), no como clave de rol |
| T14 | `MembershipRole` `admin`, `ecommerce`, `marketing` | Claves de rol | F2 l.424 | COINCIDE | |
| T15 | `Membership` | Permisos por persona (`membership_permission_grants`) y por rol (`role_permissions`) | F2 #4, #5; F4 #4, #5 | SIN_REPRESENTACIÓN | El contrato no modela permisos. Coherente con Fase 1.0 (no definía autorización); registrar como brecha futura |
| T16 | `Project` | Entidad | No existe «project» en las 27 ni en las 41 tablas | **PENDIENTE_DE_DECISIÓN** | Ver `05_PROJECT_PENDIENTE_DE_DECISION.md`. No se asume equivalencia con `campaigns` |
| T17 | `ProjectService.listForOrganization` | Consulta por organización | Depende de T16 | PENDIENTE_DE_DECISIÓN | |
| T18 | `AppState.dataMode` | demo/backend | — | NO_APLICA | |
| T19 | `AppState.environment` ∈ development/test/preview/production | Entornos de la app | F7 habla de CCI-DEV / CCI-PROD (proyectos de base de datos), F2 D-02 «organización y proyecto de Supabase exclusivos»; F5 P-01, P-10 pendientes | SIN_DISEÑO | El diseño no define entornos de la **aplicación** (`preview`, `test`). No hay contradicción; no hay respaldo |
| T20 | `AppState.isDemo` | Bandera DEMO | — | NO_APLICA | |
| T21 | `DataOrigin` | Procedencia | — | NO_APLICA | |
| T22 | `Result<T>` / `ok` / `fail` | Patrón de resultado | — | NO_APLICA | Patrón de la app; el diseño solo define errores de base de datos (F6) |
| T23 | `AppErrorCode` (5 códigos) | Contrato de errores | F6 (R1–R9 + evidencia: SQLSTATE `RJ001…RJ010`) | SIN_DISEÑO / capas distintas | Ver `04_ERRORES_R1_R9.md`: no son comparables 1:1 |
| T24 | Semántica `validation_error` / `not_found` / lista vacía | Comportamiento de consultas | F3: `fail-closed`, atomicidad en funciones (l.3625 según F6) | SIN_DISEÑO | El diseño no define el contrato de errores de lectura de la UI |
| T25 | Servicios de **lectura** únicamente | Operaciones | F3 define funciones de escritura (`transition_piece_status`, `record_approval`, `resolve_attribution_discard`…) | SIN_REPRESENTACIÓN | Fuera del alcance de 1.0 (no hay escritura) |

## Conteo
| Estado | Filas |
|---|---|
| COINCIDE (incl. conceptual / fixture) | T01, T02, T05, T07, T08, T09, T14 = **7** |
| DISCREPANCIA | T10, T11, T12, T13 = **4** |
| SIN_DISEÑO | T03, T06, T19, T23, T24 = **5** |
| SIN_REPRESENTACIÓN (el diseño tiene algo que el contrato no modela) | T15, T25 = **2** |
| PENDIENTE_DE_DECISIÓN | T16, T17 = **2** |
| NO_APLICA | T04, T18, T20, T21, T22 = **5** |
| **Total** | **25** |

«COINCIDE» significa que el concepto coincide con un diseño no aprobado; no que el esquema físico exista ni haya sido probado.
