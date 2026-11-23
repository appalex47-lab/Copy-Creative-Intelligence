# Conciliación verificada de las decisiones históricas D1–D9 (y de la serie D1–D7 de `DECISIONES.md`)
Verificado el 2026-11-22 leyendo los registros originales en el clon auditado (commit `ffb47bc319db0806250bcecf91d390fa59fa0d70`, solo lectura). **No se reabre ni se modifica ninguna decisión histórica**; D1–D9 se conservan tal como constan.

## 0. Hallazgo: dos series distintas usan los mismos identificadores
| Serie | Fuente | Contenido |
|---|---|---|
| **Serie DECISIONES** (D1–D7) | `docs/decisions/DECISIONES.md` (13 líneas) | decisiones arquitectónicas de la fundación |
| **Serie FASE 1.1** (D1–D9) | `evidence/CCI_FASE1_1_20261122T032947Z/06_BRECHAS_Y_DECISIONES.md` (planteadas, D1–D8) y `evidence/CCI_FASE1_1_B4_B5_20261122T061314Z/00_DICTAMEN_B0_B5.md` §«Decisiones D1–D9 y su aplicación» (aplicadas) | decisiones sobre roles, membresías, `Project`, permisos y estado de Fase 0 anterior |
Mi expediente previo mezclaba ambas (p. ej. llamaba «D4» tanto a «CCI-DEV/CCI-PROD» como a «T-01/T-02»). Desde ahora cada cita lleva la serie: **«DEC-D#»** (DECISIONES.md) o **«F11-D#»** (Fase 1.1). **P2 se refiere a DEC-D2/D3/D4; P15 se refiere a F11-D4.**
Limitación: los textos **literales** de tus respuestas a F11-D1…D5 no constan en el repositorio; allí solo consta su *aplicación* (dictamen B0–B5) y el estado «ACEPTADA por el propietario (con limitaciones)» de B1–B3. B4 y B5 constan como «pendiente de aceptación expresa». Tus mensajes originales de esa etapa no están en lo que tengo disponible; si importan, aportarlos.

## 1. Serie FASE 1.1 (F11-D1…D9)
| ID | Decisión (según el dictamen B0–B5) | Estado registrado | Compatibilidad con browser-only | ¿Requiere nueva decisión? |
|---|---|---|---|---|
| F11-D1 | Claves canónicas `admin, ecommerce, design, marketing, reviewer` | aplicada en `MEMBERSHIP_ROLES` (B1–B3 aceptadas con limitaciones) | **Incompatible en alcance, no en forma:** la instrucción vigente excluye usuarios/membresías/permisos multiusuario; las claves solo tienen sentido si los roles sobreviven como etiquetas (P1 opción c) | **Resuelta por P1 = (b)** (2026-11-22): sin aplicación operativa en browser-only; la decisión histórica y sus aceptaciones se conservan intactas |
| F11-D2 | `Membership.active` provisional | aplicada sin cambios (se muestra activa/inactiva) | depende de que exista `Membership` | **Resuelta por P1 = (b)** (2026-11-22): sin aplicación operativa en browser-only; la decisión histórica y sus aceptaciones se conservan intactas |
| F11-D3 | Roles no vacíos; sin unicidad | aplicada (tipo + validación) | ídem | **Resuelta por P1 = (b)** (2026-11-22): sin aplicación operativa en browser-only; la decisión histórica y sus aceptaciones se conservan intactas |
| F11-D4 | T-01/T-02 (17 permisos) NO APROBADOS; sin permisos | vigente (no aprobados) | **Compatible:** coincide con «sin autenticación/permisos» | No (se declararía histórico dentro de P15) |
| F11-D5 | Retirar `Project`; sin `Campaign` | aplicada (retirado de dominio, contrato, DEMO, HomePage, pruebas, docs) | **En tensión:** tu instrucción vigente incluye la entidad `Campaign`. El propio expediente F11 (`05_PROJECT_PENDIENTE_DE_DECISION.md`) dejaba abierta si «proyecto» = campaña | **Resuelta por Q-7 = (a)** (2026-11-22): Campaña es entidad nueva; F11-D5 íntegra y vigente como histórico |
| F11-D6 | R1–R9→RJ001–RJ009, RJ010; F6 no aprobada; 5 `AppErrorCode` sin cambios | solo conceptual; 5 códigos verificados por prueba | Los errores RJ son de base de datos (no aplican); la ampliación de `AppErrorCode` es P13 | Sí, pero ya cubierta: **P13** (y P15 para F6) |
| F11-D7 | F5 y G-1 pendientes | pendientes | pertenecen al diseño de servidor | P15 |
| F11-D8 | Fase 0 NO APROBADA (sin Supabase/PostgreSQL/SQL) | vigente como estado | **Ambigüedad:** designa la «Fase 0» y la especificación v15 **anteriores**; la Fase 0 actual es otra definición. No se traslada ni se reinterpreta | P15 (qué ocurre con la Fase 0 anterior) |
| F11-D9 | C-2 y C-3 abiertas (estado de v3.3; aprobación de D-04 «cinco roles») | abiertas | ligadas a documentos históricos de diseño de servidor | P15 |

## 2. Serie DECISIONES (DEC-D1…D7)
| ID | Texto original | Compatibilidad con browser-only | Decisión requerida |
|---|---|---|---|
| DEC-D1 | React + TypeScript estricto + Vite (mandato) | compatible | ninguna |
| DEC-D2 | Contratos tipados + adaptadores intercambiables; DEMO ahora, Supabase futuro no conectado | **parcial:** contratos/adaptadores siguen valiendo; «Supabase futuro» queda fuera del alcance | **Resuelta por P2 = (a)** (2026-11-22; ADR propuesto) |
| DEC-D3 | PostgreSQL/Supabase como fuente de verdad; caché local solo después | **incompatible** (IndexedDB es el almacenamiento principal) | **Resuelta por P2 = (a)**: declarada histórica |
| DEC-D4 | Entornos CCI-DEV y CCI-PROD independientes; no reutilizar RevNavigator | **parcial:** el texto no menciona Supabase, pero en el repositorio CCI-DEV/CCI-PROD designan los proyectos Supabase (verificado en `INTEGRACION_SUPABASE_ESTADO.md` y `ROADMAP.md`), que quedan fuera del alcance; «no reutilizar RevNavigator» sigue válido; el alcance de «entornos» para builds locales se trata en P9 | **Resuelta por P2 = (a)** (proyectos Supabase ya no son requisito; RevNavigator queda como antecedente); P9 pendiente |
| DEC-D5 | TypeScript 6.0.3 (7.x incompatible con typescript-eslint) | compatible | ninguna |
| DEC-D6 | Herramientas acotadas a rutas de la app para preservar documentación de Fase 0 | compatible (se refiere a la documentación histórica) | ninguna |
| DEC-D7 | Navegación por estado (sin router) hasta que existan rutas de producto | compatible | decisión de router (pendiente en el mismo archivo) en Fase 1 |
Pendientes del mismo archivo: «Modelo definitivo de datos» (→ P4), «Auth/multi-organización» (→ P1/P2: no aplica), «router», «sistema de diseño», «CI».

## 3. Nueva decisión detectada
**Q-7 — ¿La entidad `Campaña` de la instrucción vigente sustituye el retiro de `Project` (F11-D5)?** Opciones: (a) sí, `Campaña` es una entidad nueva del dominio local y F11-D5 queda como antecedente; (b) no, `Project` y `Campaña` se reconcilian de otra forma; (c) diferir. Antes dije que D5 «queda sustituida» y que `Campaign` «vuelve a considerarse»: **era una conclusión mía, no tuya**. Condiciona P4; se presenta después de P1 si la apruebas.

## 4. Correcciones a mi expediente previo
1. `INFORME_REVISION_COMPLEMENTARIA.md` §7 atribuía «D4 = CCI-DEV/PROD» dentro de «D1–D9»: **era incorrecto** (D4 de la serie F11 es T-01/T-02; CCI-DEV/PROD es DEC-D4).
2. `../03_CONCILIACION_DOCUMENTAL.md` §2 y la matriz de decisiones afirmaban que P1 «reemplaza» F11-D1–D3 y que Q-4/P4 «sustituyen» D5: corregido; ahora solo declaran la relación.
3. Mis «relaciones con decisiones anteriores» de la matriz se habían tomado de mi expediente, no de los registros; esta conciliación las sustituye.
