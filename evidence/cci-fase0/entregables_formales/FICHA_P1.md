# Ficha P1 — Identidad, organización, membresías y roles
Estado: **RESUELTA por el propietario el 2026-11-22 → (b)**. Ver `REGISTRO_DECISIONES_RESUELTAS.md`. La ficha se conserva como estaba al decidir.
**Pregunta:** bajo «un usuario por navegador, sin cuentas ni autenticación», ¿qué ocurre con `UserIdentity`, `Organization`, `Membership`, los cinco roles (`admin`, `ecommerce`, `design`, `marketing`, `reviewer`) y `Membership.active`?
## Contexto y problema (verificado en el commit `ffb47bc`)
- Existen en código en 7 archivos: `entities.ts`, `services/contracts/services.ts`, `adapters/demo/{fixtures,demoServices,demoServices.test}.ts`, `pages/HomePage.tsx`, `pages/pages.errors.test.tsx`; y en 2 documentos vigentes: `ARQUITECTURA.md`, `SEMANTICA_DE_SERVICIOS.md`.
- Tres servicios de lectura (`identity`, `organizations`, `memberships`); `HomePage` muestra la membresía del usuario con su organización y etiquetas legibles de rol.
- Las decisiones F11-D1 (claves de rol), F11-D2 (`active`) y F11-D3 (roles no vacíos, sin unicidad) se **aplicaron** y B1–B3 constan «aceptadas por el propietario (con limitaciones)»; B4 y B5 constan «pendientes de aceptación expresa». F11-D4 (permisos T-01/T-02 no aprobados, sin permisos) sigue vigente.
- La instrucción vigente exige no simular usuarios, permisos ni aprobaciones multiusuario. El modelo existente nació para multiusuario/multiorganización.
- Para preferencias ya hay lugar: Local Storage (preferencias ligeras) y el almacén `settings`; no dependen de P1.
## Opciones y consecuencias
| Opción | Qué implica | Consecuencias |
|---|---|---|
| (a) Retirar del dominio vigente | Se eliminan entidades, 3 servicios, fixtures, párrafo de membresía y pruebas asociadas; F11-D1–D3 quedan como histórico | Dominio mínimo y sin ambigüedad; **rehace trabajo ya aceptado (B1–B3)** cuando se autorice Fase 1; pierde el nombre visible del usuario |
| (b) Reducir a «perfil local» de un registro | Un perfil (p. ej. nombre visible opcional) sin organización, membresía, roles ni `active`; F11-D1–D3 histórico | Menos rehacer que (a) en la pantalla de inicio; añade una entidad pequeña; equivale a (a) si no quieres nombre visible |
| (c) (b) + roles como **etiquetas informativas** | Se conservan las 5 claves de F11-D1 como catálogo de «área» (p. ej. «revisado por área: Diseño») dentro de Aprobaciones, sin permisos | Compatible con F11-D4 y reutiliza F11-D1; **F11-D3 y F11-D2 perderían su sentido** (no hay `Membership`) y habría que acotar su alcance; riesgo de que una etiqueta parezca autorización |
| (d) Conservar el modelo actual (añadida por mí; no estaba en el registro) | Sin cambios hasta Fase 5 | **En tensión con «no simular capacidades multiusuario»**; mantiene lo aceptado; la tensión quedaría registrada |
## Recomendación razonada
**(b)**, con **(c)** solo si necesitas registrar el área que revisa. Razones: la instrucción vigente excluye multiusuario, así que `Organization`, `Membership` y `active` no tienen función; un perfil mínimo evita rehacer toda la pantalla de inicio y deja dónde mostrar un nombre; los roles solo aportan valor como etiquetas si la aprobación necesita registrar el área. Si no quieres nombre visible, **(a) es equivalente** y más simple. Es mi criterio técnico, no un hecho verificado de uso real.
## Documentos y módulos afectados
`05_MODELO_DOMINIO_CCI.md`, `06_MODELO_DATOS_CCI.md`, `04_ARQUITECTURA_BROWSER_ONLY.md`, `02_INVENTARIO_FUNCIONAL_CCI.md` (filas B2/B3); repositorio: los 7 archivos y 2 documentos arriba (**no se tocan** sin autorización); módulos: Command Center (pantalla de inicio), Settings, Workflow & Approvals (si c).
## Relación con decisiones anteriores
F11-D1, D2, D3: aplicadas y aceptadas; esta decisión define su destino en la arquitectura vigente **sin reabrirlas**. F11-D4: compatible con las cuatro opciones. F11-D5/Q-7: independiente. DEC-D2–D4/P2: la serie de Auth/multi-organización de `DECISIONES.md` queda «pendiente» allí; P1 la contesta para el alcance vigente.
## Dependencias y efecto de no decidir
Depende de P2 (marco histórico) e informa P4 (entidades). Sin respuesta, Fase 1 no puede fijar el dominio inicial ni retirar o conservar `Organization/Membership`.
## Respuesta
`P1 → (b)` — **respondida** (2026-11-22).
