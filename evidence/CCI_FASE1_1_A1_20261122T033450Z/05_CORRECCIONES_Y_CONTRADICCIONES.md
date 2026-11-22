# 05 — Correcciones al expediente 1.1-A original y contradicciones abiertas

El expediente original (`CCI_FASE1_1_20261122T032947Z`) **no se modificó**; este documento lo complementa. Validado contra un diseño no aprobado.

## Correcciones (errores míos hallados al revisar F2 de nuevo, solo lectura)
| # | Afirmación original | Corrección |
|---|---|---|
| K1 | «Ni F2 ni F3 definen columnas de `profiles`, `organizations`, `memberships`» (03, 07) | F2 §modelo (l.950–957) define parcialmente: `organizations` (organización, `slug` único, ajustes), `profiles` (`id = auth.users.id`, sin `organization_id`), `memberships` (`unique(organization_id, user_id)`, `roles` arreglo no vacío de enum), `campaigns` (nombre, categoría, objetivo, vigencia, responsable). Siguen sin definirse nombre visible de persona, nombre de organización como columna ni actividad de la membresía |
| K2 | «PK (org,user) solo en el fixture» (02 T09) | También en F2: `unique(organization_id, user_id)` |
| K3 | `diseno`/`revisor_aprobador` «podrían ser etiquetas» (03, 07) | Son valores de enum en F2 l.952 |
| K4 | T10 `active` vs `activo` como DISCREPANCIA | `activo` solo está en el fixture; el diseño no define la columna → SIN_DISEÑO (ver 02) |
| K5 | `audit.image`, `copy.analyze`… «¿permisos o funciones?» | Son claves de prompt (F2 l.1157) |
| K6 | Sección de «posible adición futura» a `AppErrorCode` (04) | Retirada como propuesta |
| K7 | «Aparecen nominalmente las 17» presentado sin la reserva de etiquetas vs claves | Ver 04 §A |

## Contradicciones abiertas (no resueltas)
| ID | Contradicción | Fuentes |
|---|---|---|
| C-1 | T-01 (17 permisos) y T-02 «NO APROBADA» frente a «APROBADOS/vigentes» | F2 l.186 vs F3 l.34 |
| C-2 | **Estado de v3.3:** su propio encabezado dice «NO está aceptada… No se inició la Fase 1» (F2 l.3, fecha 2026-11-15); F3 dice que v3.3 es «COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES» y F1 dice Fase 0 NO ACEPTADA. Pudo haber una aceptación posterior no localizada; no la verifiqué |
| C-3 | D-04 «APROBADA» (cinco roles) en F2 mientras el enum con claves concretas no tiene aprobación propia localizada | F2 l.745/952 |

Decisiones pendientes del propietario (sin cambio respecto al expediente original): D1 (mapeo/identificador de roles), D2 (obsoleta como discrepancia; sigue siendo cuestión de nomenclatura si se modela actividad), D3 (roles no vacío), D4 (C-1), D5 (Project), D6 (F6), D7 (G-1 y demás), D8 (aprobación de Fase 0). Se añade D9: aclarar C-2 y C-3.

## No verificado
Aprobación posterior de T-01/T-02/v3.3; coherencia permiso→rol fuera de F2.

Verificado por lectura: `validateDemoDataset` no valida `roles` vacío (grep de `roles` en `fixtures.ts`: solo la línea 27, `['admin']`).
