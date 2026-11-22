# 02 — Matriz de trazabilidad normalizada (25 filas, mismos identificadores T01–T25)

**Validada contra un diseño todavía NO aprobado.** Estado principal uniforme: `COINCIDE` · `DISCREPANCIA` · `SIN_DISEÑO` · `REQUIERE_DECISIÓN_DEL_PROPIETARIO`. `NO_APLICA` solo como clasificación complementaria (concepto exclusivo de la aplicación). Las observaciones secundarias se conservan.
Fuentes: F2 = v3.3 (`fase0_v3_3_integral.md`), F3 = especificación v15, F4 = matriz del modelo, F5 = registro de decisiones, F6 = propuesta de errores R1–R9 (NO APROBADA).

## Criterios de normalización
- Lo que el diseño define y el contrato no expresa por **decisión deliberada de alcance** (Fase 1.0 sin autorización ni escritura) **no** se cuenta como discrepancia de implementación: se registra como `REQUIERE_DECISIÓN_DEL_PROPIETARIO` solo si depende de una decisión abierta, con complemento `FUERA_DE_ALCANCE_DELIBERADO`.
- Un nombre que solo aparece en el **fixture** (esquema temporal de pruebas) no es diseño: no genera `DISCREPANCIA` contra el diseño.
- `DISCREPANCIA` exige que el diseño defina el dato de forma explícita y el contrato difiera.

| ID | Contrato | Estado principal | Complementaria | Observaciones secundarias y justificación |
|---|---|---|---|---|
| T01 | `UserIdentity` (entidad) | COINCIDE | — | F2: `profiles`, «datos del usuario; `id` = `auth.users.id`». Sin prueba (F4 #2 SIN_PRUEBA) |
| T02 | `UserIdentity.id` | COINCIDE | — | `profiles.id = auth.users.id` (F2). Tipo físico no definido |
| T03 | `UserIdentity.displayName` | SIN_DISEÑO | — | F2 describe `profiles` solo como «datos del usuario»; no define columna de nombre visible |
| T04 | `UserIdentity.origin` | SIN_DISEÑO | NO_APLICA | Marca DEMO/backend de la app |
| T05 | `Organization` (entidad) | COINCIDE | — | F2 `organizations`: organización, `slug` único, ajustes. El contrato no representa `slug` ni ajustes (alcance de 1.0) |
| T06 | `Organization.name` | SIN_DISEÑO | — | F2 no nombra una columna «nombre»; el fixture solo tiene `id` |
| T07 | `OrganizationService.listForCurrentUser` | COINCIDE | — | Concepto de RLS «solo miembros» (F2). RLS sin probar (F4) |
| T08 | `Membership` (entidad) | COINCIDE | — | F2 `memberships`; F4 #3 |
| T09 | `Membership.userId/organizationId` | COINCIDE | — | F2: `unique(organization_id, user_id)`. F4: el fixture usa PK (org,user) |
| T10 | `Membership.active` | SIN_DISEÑO | — | Ni F2 ni F3 definen una columna de baja/actividad de la membresía; F3 solo usa el concepto «miembro activo». `activo` aparece **solo en el fixture** (F4 #3). **Cambio respecto al expediente original** (allí DISCREPANCIA): el diseño no define el nombre, el fixture no es diseño |
| T11 | `Membership.roles` | DISCREPANCIA | — | F2 l.952: «arreglo **no vacío**». El tipo `readonly MembershipRole[]` admite vacío. Menor; el contrato provisional no expresa la restricción (verificado por lectura de `src/services/adapters/demo/fixtures.ts`: `validateDemoDataset` no comprueba `roles` vacío y la única membresía DEMO tiene `['admin']`) |
| T12 | `MembershipRole` valor `design` | DISCREPANCIA | REQUIERE_DECISIÓN (D1: criterio de mapeo) | F2 l.952 define el **enum** `diseno`. Fortalece el expediente original (allí «podrían ser etiquetas»: **no**; hay un enum explícito) |
| T13 | `MembershipRole` valor `reviewer` | DISCREPANCIA | REQUIERE_DECISIÓN (D1) | F2 l.952: enum `revisor_aprobador` (etiqueta «Revisor / Aprobador»). F3 usa «reviewer» solo en prosa/eventos |
| T14 | `admin`, `ecommerce`, `marketing` | COINCIDE | — | Mismo valor en el enum de F2 |
| T15 | Permisos (`role_permissions`, `membership_permission_grants`) | REQUIERE_DECISIÓN_DEL_PROPIETARIO | FUERA_DE_ALCANCE_DELIBERADO | Dependen de T-01 (D4, sin resolver). La Fase 1.0 declara que la UI no autoriza; no es defecto |
| T16 | `Project` | REQUIERE_DECISIÓN_DEL_PROPIETARIO | — | No existe `project` en las 27/41 tablas. Alternativas en `05_PROJECT…` del expediente original. No se asume `campaigns` |
| T17 | `ProjectService.listForOrganization` | REQUIERE_DECISIÓN_DEL_PROPIETARIO | — | Depende de T16 |
| T18 | `AppState.dataMode` | SIN_DISEÑO | NO_APLICA | Concepto de la app |
| T19 | `AppState.environment` | SIN_DISEÑO | NO_APLICA | F2/F7 hablan de proyectos DEV/PROD de base de datos (no de entornos de la app) |
| T20 | `AppState.isDemo` | SIN_DISEÑO | NO_APLICA | Concepto de la app |
| T21 | `DataOrigin` | SIN_DISEÑO | NO_APLICA | Concepto de la app |
| T22 | `Result<T>`, `ok`, `fail` | SIN_DISEÑO | NO_APLICA | Patrón de la app |
| T23 | `AppErrorCode` | SIN_DISEÑO | — | El diseño no define errores de lectura de la UI. R1–R9 son otra capa (ver `03_R1_R9.md`) |
| T24 | Semántica `validation_error` / `not_found` / lista vacía | SIN_DISEÑO | — | Decisión propia de la app |
| T25 | Servicios de escritura (funciones `transition_piece_status`, `record_approval`, `resolve_attribution_discard`…) | REQUIERE_DECISIÓN_DEL_PROPIETARIO | FUERA_DE_ALCANCE_DELIBERADO | Sin escritura en 1.0; el diseño los tiene y dependen de decisiones abiertas (F5, F6 NO APROBADA) |

## Conteo (suma 25)
| Estado principal | Filas | n |
|---|---|---|
| COINCIDE | T01, T02, T05, T07, T08, T09, T14 | 7 |
| DISCREPANCIA | T11, T12, T13 | 3 |
| SIN_DISEÑO | T03, T04, T06, T10, T18, T19, T20, T21, T22, T23, T24 | 11 |
| REQUIERE_DECISIÓN_DEL_PROPIETARIO | T15, T16, T17, T25 | 4 |
| NO_APLICA como complementaria | T04, T18, T19, T20, T21, T22 | 6 (solapa con SIN_DISEÑO) |

Cambios de estado frente al expediente original: T04, T18, T19, T20, T21, T22, T23, T24 (SIN_DISEÑO/NO_APLICA → principal SIN_DISEÑO); T10 DISCREPANCIA → SIN_DISEÑO; T15 y T25 «SIN_REPRESENTACIÓN» → REQUIERE_DECISIÓN con complemento de alcance; T16/T17 PENDIENTE_DE_DECISIÓN → REQUIERE_DECISIÓN (mismo significado). Las filas T01–T03, T05–T09, T11–T14 no cambian de clasificación; el original contaba «DISCREPANCIA» = T10–T13, ahora T11–T13.
