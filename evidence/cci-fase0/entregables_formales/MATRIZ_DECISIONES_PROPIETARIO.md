# Matriz individual de decisiones indispensables para cerrar Fase 0
Fuente de contenido: `13_REGISTRO_DECISIONES_PROPIETARIO.md` (texto original verificado, no reconstruido). **Ninguna está respondida.** No hay decisiones resueltas por el propietario en este registro; ninguna se reabre. Una recomendación es mía; un silencio no aprueba nada. Cada decisión se responde por separado; una respuesta parcial no se extiende a las relacionadas.
**Nota editorial (a confirmar):** el registro original unía en P4 dos cosas distintas (modelo de entidades y alcance del MVP). Aquí **P4 = solo el modelo de entidades** y **Q-4 = solo el alcance del MVP**, para que puedas responderlas por separado. Es un cambio de presentación mío, no una reinterpretación de tu decisión.
**Antecedentes comunes:** las decisiones históricas se conservan sin reabrir. Hay **dos series con los mismos IDs** (DEC-D1…D7 en `DECISIONES.md`; F11-D1…D9 de Fase 1.1): ver `CONCILIACION_D1_D9_VERIFICADA.md`, que sustituye mis relaciones anteriores. Nueva decisión detectada: **Q-7** (`Campaña` frente a F11-D5). Instrucción vigente: un usuario por navegador, sin cuentas/backend/Supabase/PostgreSQL/SQL/servidor/sincronización, IndexedDB principal, Local Storage ligero.
Formato de respuesta sugerido: `P# → opción (a/b/c) | con cambios: … | rechazada`.

---
## P1 — Identidad, organización, membresías y roles
**RESUELTA (propietario, 2026-11-22): opción (b).** Ver `REGISTRO_DECISIONES_RESUELTAS.md`; el contenido siguiente es el planteamiento original.
- **Pregunta:** ¿Qué pasa con `UserIdentity`, `Organization`, `Membership`, los 5 roles y `Membership.active`?
- **Contexto y problema:** son el modelo multiusuario anterior; hoy el código y `HomePage` los usan. La instrucción vigente prohíbe simular usuarios, permisos o aprobaciones multiusuario.
- **Opciones y consecuencias:**
  - (a) Eliminar del dominio vigente (histórico): máxima simplicidad; se reescriben contratos, fixtures y pruebas.
  - (b) Reducir a un «perfil/espacio local» de un registro: conserva un ancla para preferencias; algo de reescritura.
  - (c) Conservar roles solo como etiquetas informativas en Aprobaciones: añade un catálogo; riesgo de parecer autorización.
- **Recomendación:** (b), con (c) solo si quieres registrar «área revisora». Razón: la instrucción excluye multiusuario, pero una preferencia local necesita dónde vivir; los roles como permisos contradicen la decisión.
- **Afecta:** `05` dominio, `04` arquitectura, `06` datos; Command Center, Settings; código existente (`entities.ts`, `HomePage`).
- **Relación:** define el destino de F11-D1–D3 (aplicadas y aceptadas) sin reabrirlas; F11-D4 compatible; depende de P2 e informa P4. Ficha completa: `FICHA_P1.md`.

## P2 — Sustituir formalmente DEC-D2–D4 y «Fuente de verdad»
**RESUELTA (propietario, 2026-11-22): opción (a).** Ver `REGISTRO_DECISIONES_RESUELTAS.md`; abajo, el planteamiento original.
- **Pregunta:** ¿Se registra un ADR que declare reemplazadas DEC-D2 (parcial), DEC-D3, DEC-D4 y la sección «Fuente de verdad», conservándolas como históricas?
- **Contexto y problema:** `DECISIONES.md` y `ARQUITECTURA.md` siguen diciendo PostgreSQL/Supabase como fuente de verdad (K2/K4); contradicen la decisión vigente.
- **Opciones y consecuencias:** (a) ADR de reemplazo con estado «HISTÓRICA»: documentación coherente y trazable; (b) solo una nota: contradicción visible persiste; (c) no tocar: criterio de cierre «ningún documento vigente declara PG/Supabase como fuente de verdad» no se cumple.
- **Recomendación:** (a). Razón: no borra historia y elimina la contradicción.
- **Afecta:** `DECISIONES.md`, `ARQUITECTURA.md`, README, `ROADMAP.md` (todos del repositorio; **no se modifican sin tu autorización**); `README_PROPUESTA_VIGENTE.md`.
- **Relación:** formaliza la instrucción vigente; depende de P3.

## P3 — Tratamiento de `docs/fase0/` y expedientes Supabase/SQL/RLS
**RESUELTA (propietario, 2026-11-22): opción (b), con condiciones.** Ver `REGISTRO_DECISIONES_RESUELTAS.md`; abajo, el planteamiento original.
- **Pregunta:** ¿Solo histórico, o también referencia para el dominio local?
- **Contexto y problema:** 59 archivos (41 tablas, 231 reglas, 780 escenarios, 17 permisos), **no aprobados**; contienen vocabulario de producto reutilizable.
- **Opciones y consecuencias:** (a) solo histórico: limpio, pierde ideas; (b) histórico + referencia no vinculante al dominio: aprovecha vocabulario sin presentarlo como trabajo aceptado; (c) migrar partes: reintroduce complejidad de servidor.
- **Recomendación:** (b).
- **Afecta:** `../03_CONCILIACION_DOCUMENTAL.md`, `05` dominio; ningún código.
- **Relación:** sigue a P2; informa P4.

## P4 — Modelo de entidades del dominio (sin el alcance del MVP)
**PARCIAL (2026-11-22; actualizado):** P4.1 aprobó solo la lista de nombres; Q-7 = (a); lo pendiente: `DECISIONES_P4_PENDIENTES.md`. Antes: P4.1 pendiente; P4.2 → (b); P4.3 respondida; P4.4 aplazado a Q-7; P4.5 preliminar. Ver `REGISTRO_DECISIONES_RESUELTAS.md`.
- **Pregunta:** ¿Apruebas las entidades, relaciones y responsabilidades de `05_MODELO_DOMINIO_CCI.md` y `06_MODELO_DATOS_CCI.md`, incluida la entidad adicional «Evento de actividad» (no está en tu lista)?
- **Contexto y problema:** tu lista de entidades no fija atributos ni clasificación; F11-D5 retiró `Project` sin `Campaign` y tu instrucción incluye `Campaña`: tensión que se decide en **Q-7**, no aquí.
- **Opciones y consecuencias:** (a) aprobar tal cual: Fase 1 puede definir stores; (b) aprobar con cambios por entidad: más precisión, más tiempo; (c) rechazar: Fase 1 bloqueada.
- **Recomendación:** (a) pidiendo cambios entidad por entidad si los hay. «Evento de actividad» es necesaria para la «actividad real» del Command Center; puedes rechazarla solo a ella.
- **Afecta:** `05`, `06`, `07` (stores), `03` (R-005); todos los módulos.
- **Relación:** F11-D5 sigue vigente hasta que decidas Q-7; depende de P1 y Q-7; condiciona P5.

## P5 — Binarios (imágenes/archivos) en IndexedDB
- **Pregunta:** ¿Se guardan piezas creativas como Blobs en IndexedDB, o solo metadatos?
- **Contexto y problema:** Fase 3 audita imágenes y necesita los píxeles; cuotas varían por navegador (no verificadas); afecta tamaño de exportaciones.
- **Opciones y consecuencias:** (a) Blobs con tope configurable: auditoría visual autónoma; riesgo de cuota y respaldos grandes; (b) solo metadatos: ligero; el usuario reabre archivos, auditoría menos práctica; (c) diferir a Fase 3: el esquema de `pieces` y exportación queda abierto, Fase 3 bloqueada hasta decidir.
- **Recomendación:** (a) con tope y avisos de cuota. Razón: sin píxeles locales no hay auditoría visual repetible.
- **Afecta:** `07`, `08`, `05` (Pieza); Creative Auditor, Library.
- **Relación:** independiente de decisiones anteriores; liga con P6 (formato de exportación) y P11.

## P9 — Qué significa «producción» en modo local
- **Pregunta:** ¿Se redefine la política de entorno para que `build:production` sea un build local legítimo sin DEMO?
- **Contexto y problema:** hoy `build:production` falla por diseño y `VITE_DATA_MODE=supabase` se rechaza como `not_implemented` (verificado: falla como se espera). Con persistencia local `demo` deja de ser el único modo.
- **Opciones y consecuencias:** (a) modo `local` real + `demo` solo en test, producción permitida con `local`; (b) mantener el bloqueo hasta Fase 5; (c) eliminar la política (riesgo de publicar datos ficticios).
- **Recomendación:** (a), manteniendo el bloqueo de DEMO en producción.
- **Afecta:** `envPolicy.ts`, `vite.config.ts`, `.env.example`, pruebas de build, README.
- **Relación:** actualiza lo aceptado en Fase 1.1 (política de entorno); depende de P10 (en Fase 1 basta localhost).

## P11 — Navegadores soportados
- **Pregunta:** ¿Qué navegadores y versiones se soportan y prueban?
- **Contexto y problema:** solo Chrome está verificado (Playwright `channel: 'chrome'`); IndexedDB, cuotas y Web Locks varían.
- **Opciones y consecuencias:** (a) Chromium (Chrome/Edge); (b) + Firefox; (c) + Safari/WebKit. Cada nivel añade matriz E2E y requiere instalar navegadores de prueba (no autorizado en Fase 0).
- **Recomendación:** (a) completo, (b) con pruebas, (c) esfuerzo documentado. Razón: es la cobertura realista sin prometer lo no verificado.
- **Afecta:** `15` plan de pruebas, `12` AC1/AC5, configuración Playwright.
- **Relación:** ninguna previa; condiciona P12.

## P12 — Política multi-pestaña
- **Pregunta:** ¿Bloqueo exclusivo, aviso y solo lectura, o varias pestañas con control optimista?
- **Contexto y problema:** sin coordinación hay escrituras cruzadas; Web Locks no está verificado en todos los motores.
- **Opciones y consecuencias:** (a) Web Locks: simple de razonar, depende de soporte; (b) aviso + solo lectura en las demás: seguro y claro; (c) `revision` optimista: más flexible, más conflictos que resolver.
- **Recomendación:** (b), con (c) como respaldo.
- **Afecta:** `07` (revision), repositorios, E2E multi-pestaña, Command Center.
- **Relación:** depende de P11.

## P13 — Política de dependencias y ampliación de `AppErrorCode`
- **Pregunta:** ¿Se permiten dependencias de ejecución/desarrollo nuevas, se amplía `AppErrorCode` y se conservan las guardas anti-Supabase?
- **Contexto y problema:** hoy solo `react`/`react-dom` en ejecución; instalar exige autorización; `npm audit` no se ha ejecutado.
- **Opciones y consecuencias:** (a) cero nuevas: IndexedDB y validadores propios, mayor trabajo; (b) conjunto mínimo aprobado una por una con versión exacta; (c) libre: más superficie de cadena de suministro.
- **Recomendación:** (b); ampliar `AppErrorCode`; conservar guardas como control genérico.
- **Afecta:** `package.json`, `04`, `07`, `08`, `09`; Copy Studio (diccionario), exportación (ZIP).
- **Relación:** depende de P5, P6, P8; las guardas vienen de la política aceptada en Fase 1.x.

## P14 — Prueba de concepto de IndexedDB dentro de Fase 0
- **Pregunta:** ¿Se incluye un PoC?
- **Contexto y problema:** tu instrucción prohíbe modificar código en Fase 0 y asigna IndexedDB a Fase 1; en la práctica ya está resuelta en sentido (a), **pero requiere tu confirmación**.
- **Opciones y consecuencias:** (a) no: supuestos de navegador (cuota, Web Locks) quedan sin verificar hasta Fase 1; (b) PoC aislado fuera del repositorio: reduce incertidumbre; cuesta tiempo y requiere autorización de ejecución.
- **Recomendación:** (a).
- **Afecta:** `07`, `14_MATRIZ_RIESGOS_CCI.md` (RK-01, RK-04, RK-10).
- **Relación:** coherente con la instrucción vigente.

## Q-4 — Alcance del MVP
- **Pregunta:** ¿El MVP es el fin de la Fase 2 (Command Center + Copy Studio persistentes)?
- **Contexto y problema:** tu instrucción pide definir el MVP sin ampliar alcance; no fija dónde termina.
- **Opciones y consecuencias:** (a) fin de Fase 2: valor útil temprano; auditoría y promociones quedan fuera; (b) fin de Fase 3 (con Creative Auditor): más completo, más tardío y exige P5/Q-5; (c) producto completo (Fase 5): sin hito intermedio.
- **Recomendación:** (a).
- **Afecta:** `10_DEFINICION_MVP_CCI.md`, `11`, `12`, `05` (clasificación MVP).
- **Relación:** se apoya en P4; las columnas de módulos 6–9 del MVP son propuestas no sustentadas (ver el documento).

> **Nota fechada 2026-11-22 (auditoría cruzada):** «Ninguna está respondida» es el estado al elaborarse; varias decisiones (P1, P2, P3, P4 parcial, Q-7) fueron respondidas después. Estado vigente y fuente: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`; P4.A 9/18 a la fecha de esta nota (**vigente actual: 18/18**, ratificación B1; ver `REGISTRO_DECISIONES_RESUELTAS.md`); D-1…D-8 resueltas en su alcance. Este documento se conserva como evidencia histórica.

> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; el texto original no se altera):** las decisiones P4, P5, P9, P11, P12, P13 y P14 de esta matriz quedaron **resueltas** por la ratificación (la ratificación fija su contenido; las opciones (a)/(b)/(c) de esta matriz no coinciden con la redacción ratificada de P11: ver el registro); P6, P7, P8, P10 y P15 tienen aplazamiento aceptado (no resueltas). Fuente y texto literal: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)». Aprobaciones 0.1–0.7, aceptación de Fase 0 y autorización de Fase 1 siguen pendientes.
