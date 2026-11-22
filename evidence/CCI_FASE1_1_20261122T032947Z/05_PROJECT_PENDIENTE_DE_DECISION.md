# 05 — «Project»: PENDIENTE_DE_DECISIÓN

Por instrucción del propietario no se asume que `Project` equivale a `campaigns`. **Validado contra un diseño no aprobado.**

## Hechos
- Ninguna de las 27 tablas (F2/F3) ni de las 41 (F4) se llama `project`/`projects`. En F2 «proyecto» aparece solo como **proyecto de Supabase** (P-01, D-02) o «organización y proyecto». En F5/F7 «project ref» = identificador de proyecto de Supabase.
- `campaigns` (F2 #7): «agrupa el trabajo — padre de briefs, piezas, promociones — RLS; `campaign.write`»; F3 l.4870: FK `campaigns → organizations`. F2 §5.2 describe un caso de promociones con «campaña de origen opcional» (T-11, no aprobada).
- Código actual: `Project { id, organizationId, name }` y `ProjectService.listForOrganization`.

## Alternativas e implicaciones
| Alt. | Descripción | Implicaciones |
|---|---|---|
| P-A | `Project` = `campaigns` (renombrar a `Campaign` en la app) | Alinea con el diseño; el permiso asociado sería `campaign.write`. Requiere confirmar que «proyecto» del lenguaje de producto = campaña. El nombre/columnas de `campaigns` no están definidos (solo su rol y FK a `organizations`). Impacto: renombrar tipos, servicio, fixtures, pantallas y pruebas (1.1-B) |
| P-B | `Project` = concepto superior a campaña (agrupa campañas) | No existe en el diseño: exigiría **nueva tabla** → fuera del alcance de Fase 0 aprobada; nueva decisión de diseño y revisión de RLS/FK |
| P-C | `Project` = concepto distinto (p. ej. un nivel de organización o producto) | Igual que P-B; ninguna fuente lo define |
| P-D | Eliminar `Project` del contrato hasta que exista el diseño (mantener solo organizaciones, membresías) | Evita contratos sin respaldo; la pantalla/servicio de proyectos dejaría de existir en DEMO. Reduce deuda; pierde la demostración de listados por padre (se puede mantener con `Membership`) |
| P-E | Mantener `Project` provisional, marcado «sin respaldo de diseño» | Sin cambios de código; riesgo de que se consolide por inercia |

## Estado
**PENDIENTE_DE_DECISIÓN.** Este documento no resuelve. La recomendación no vinculante está en `06_BRECHAS_Y_DECISIONES.md`.
