# Paquete de decisión — autorización independiente de la Fase 1
> **2026-11-22. Documento de apoyo: NO autoriza la Fase 1 ni emite ninguna decisión.** Estado a la fecha de este paquete: Fase 0 **ACEPTADA** (propietario, 2026-11-22 20:26) con las limitaciones expresas C-2 y C-3 abiertas y los 10 aplazamientos pendientes; Fase 1 **NO autorizada** (autorización PENDIENTE; acto independiente de la aceptación). Las recomendaciones son **[Rec. Claude], no vinculantes**: solo valen si el propietario las adopta con sus propias palabras.

## 0. Fundamento y alcance de este paquete
- **Requisito:** `PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md` §19: «Una vez aceptada Fase 0, deberá emitirse una autorización independiente para iniciar Fase 1». La autorización debe especificar seis elementos (secciones 1 a 6 de este paquete). La aceptación de la Fase 0 no autoriza por sí misma la Fase 1.
- **Fuente del contenido de la Fase 1:** `11_ROADMAP_FASES_0_A_5.md` (Fase 1 «Fundamentos y Command Center») y `12_CRITERIOS_ACEPTACION_FASES.md` (AC1-01 a AC1-13, más AC1-14 propuesto desde P1). Registro vigente: B7 en `REGISTRO_DECISIONES_RESUELTAS.md`.
- **Lo que este paquete NO hace:** no autoriza subfases, ramas ni archivos; no implementa, instala ni ejecuta nada; no resuelve C-2, C-3 ni los 10 aplazamientos; no reabre D5.a–d (fuera de alcance, no pendientes); no aprueba atributos de entidades; no crea ramas, commits ni despliegues en el repositorio de la aplicación; no toca `docs/fase0`, `main` ni la vista previa privada.
- **Qué no se inspeccionó:** la estructura real, las ramas y el estado del repositorio de la aplicación **no se inspeccionaron** en esta ronda; las opciones de rama y áreas son propuestas a validar por el propietario.

## 1. Subfases autorizadas
- **Contenido de la Fase 1 según roadmap:** arquitectura por capas (presentación → aplicación → dominio → contratos → repositorios → adaptadores IndexedDB/memoria/preferencias), sistema visual, navegación, IndexedDB, repositorios, migraciones, configuración, errores y pruebas; Command Center con estado, pendientes y actividad real; pantalla de almacenamiento; preferencias.
- **El roadmap no define subfases numeradas dentro de la Fase 1.** No se inventan: el propietario decide si autoriza la Fase 1 completa como una sola unidad o la parte en tramos que él nombre.
- **Opciones:**
  - **A.** Autorizar la Fase 1 completa (alcance del roadmap).
  - **B.** Autorizar solo un tramo inicial que el propietario defina (p. ej., base técnica sin Command Center) y exigir una nueva autorización para el resto.
- **[Rec. Claude]:** A, con alcance exactamente el del roadmap y sin ampliaciones; la Fase 2 queda excluida («Autoriza: nada; Fase 2 exige autorización expresa»).

## 2. Repositorio y rama permitidos
- **Repositorio de la aplicación:** el propietario debe nombrarlo; no se asume.
- **Rama:** el propietario debe nombrarla. Opciones:
  - **A.** Una rama nueva y dedicada a la Fase 1, nombrada por el propietario, creada desde la línea base que él indique.
  - **B.** Una rama existente que él indique.
- **[Rec. Claude]:** A, rama dedicada y separada de `main` y de la línea `docs/fase0`; así la integración posterior es un acto distinto y revisable.
- **Pendiente de validar:** que la línea base elegida corresponda al diagnóstico aprobado (0.1: existe la fundación comprobada; el producto CCI no existe). No se verificó.

## 3. Archivos o áreas que pueden modificarse
- **Propuesta de áreas [Rec. Claude]** (a confirmar contra la estructura real del repositorio, no inspeccionada): código fuente de la aplicación (`src/`), pruebas, configuración de herramientas (TypeScript, ESLint, Prettier, pruebas), y la documentación de evidencia de la Fase 1.
- **Excluido [Rec. Claude]:** `docs/fase0` (histórico), cualquier rastro de Supabase/PostgreSQL/SQL/servidor/autenticación (fuera de la arquitectura aprobada 0.2), secretos y credenciales, flujos de CI/despliegue salvo que el propietario los incluya expresamente.
- **Dependencias nuevas:** riesgo inherente de la Fase 1 («nuevas dependencias»). **[Rec. Claude]:** exigir que cada dependencia nueva se justifique y se registre en la evidencia, sin lista cerrada inventada aquí.
- **Atributos de entidades:** la regla P4.C vigente solo permite aprobar, antes de implementar una entidad, los atributos indispensables para el alcance autorizado, con necesidad funcional, fuente o justificación. **Ninguno está aprobado.** Si la autorización incluye el dominio inicial (AC1-05), el propietario debe aprobar esos atributos mínimos antes de implementarlos; este paquete no los propone.

## 4. Pruebas exigidas
- **Criterios de aceptación (de `12_CRITERIOS_ACEPTACION_FASES.md`):**
  - AC1-01 sin `fetch`/XHR/WebSocket/SDK de servidor en `src/` (prueba de arquitectura por AST).
  - AC1-02 `tsc -b`, ESLint y Prettier con 0 errores/advertencias; modo estricto y `noUncheckedIndexedAccess`.
  - AC1-03 navegación, gestión de foco y enlace de salto; E2E.
  - AC1-04 componentes reutilizables con pruebas y sin violaciones axe.
  - AC1-05 dominio inicial con validadores y pruebas unitarias.
  - AC1-06 IndexedDB solo mediante adaptador; repositorios probados contra memoria **y** navegador real.
  - AC1-07 migraciones v0→v1 y v1→v2 con datos semilla; una base de versión mayor se rechaza sin escribir.
  - AC1-08 cada `AppErrorCode` de persistencia con mensaje, prueba y comportamiento de UI.
  - AC1-09 preferencias en Local Storage validadas; nada fuera de la lista permitida.
  - AC1-10 pantalla de almacenamiento con uso/cuota/persistencia del navegador; E2E.
  - AC1-11 Command Center solo desde IndexedDB, estado vacío explícito, sin datos DEMO en el build de producción.
  - AC1-12 los datos persisten tras recarga/reinicio; sin estado parcial tras una transacción abortada.
  - AC1-13 responsive y axe.
  - AC1-14 (propuesto desde P1; solo si se incluye el perfil local, sección 7): perfil local opcional, sin organización, membresía ni roles.
- **Regla de cierre:** regla común más **3 ejecuciones E2E consecutivas** exitosas.
- **Verificación técnica previa [Rec. Claude]:** Web Locks, cuotas de IndexedDB y compatibilidad de navegadores **no están verificados**; deben comprobarse técnicamente al inicio y declararse en la evidencia antes de afirmar soporte alguno. La mitigación multi-pestaña (P12) depende de la implementación futura.
- **Matriz de navegadores:** el propietario decide cuáles se prueban; este paquete no declara ninguno soportado.

## 5. Prohibiciones de commit, merge, push o deploy que siguen vigentes
- Vigente hoy: el propietario ordenó no fusionar con la vista previa privada; la publicación del expediente sigue bloqueada (`CCI-Evidence` 403; `add_repo` denegado); el expediente está solo en commit local.
- **El propietario debe decir qué se permite en la rama de la Fase 1.** Opciones por operación:
  - **commit:** permitido solo en la rama autorizada / no permitido.
  - **push:** permitido solo a la rama autorizada / no permitido.
  - **merge:** no permitido hacia `main` ni hacia la vista previa privada sin acto separado / permitido.
  - **deploy:** no permitido / permitido (P10, hosting y origen, está **aplazado**: debe resolverse antes de publicar, por lo que desplegar no es coherente con el estado actual).
- **[Rec. Claude]:** commit y push solo a la rama dedicada de la Fase 1; merge y deploy prohibidos hasta un acto expreso posterior del propietario.

## 6. Criterios de aceptación y evidencia
- **Criterios:** los de la sección 4. La aceptación de la Fase 1 sería un acto posterior e independiente de esta autorización; la autorización no la anticipa.
- **Evidencia exigida por el roadmap/criterios:** regresión completa, E2E ≥3 ejecuciones consecutivas, logs, capturas de pantalla, manifiesto SHA-256 y expediente de cierre.
- **[Rec. Claude]:** que la evidencia declare expresamente lo no verificado y lo aplazado, como en la Fase 0.

## 7. Decisiones del propietario que condicionan el alcance
- **Respaldo (exportación/importación local) dentro de la Fase 1 — B7.** El roadmap lo incluye **solo si el propietario lo aprueba** dentro del alcance de persistencia. Sin esa aprobación, la recuperación ante pérdida de datos se aplaza a la Fase 5 y el riesgo **RK-01** (pérdida de datos por borrado o expulsión del navegador; mitigaciones: `persist()`, aviso de respaldo, exportación periódica; no se promete recuperación automática) permanece sin mitigar en la Fase 1.
  - Opciones: **sí** incluir respaldo básico / **no**, diferir a la Fase 5.
  - **[Rec. Claude]:** sí, porque los datos son locales y únicos por navegador, de modo que una pérdida no tiene copia. Es una recomendación sobre riesgo, no una decisión; añade alcance y pruebas que el roadmap condiciona a tu aprobación.
- **Perfil local opcional (P1; AC1-14).** P1 ya está resuelto (perfil local opcional, sin identidad, organización, membresías ni roles). Falta decidir si entra en la Fase 1.
  - Opciones: **sí** / **no** (queda para una fase posterior).
  - **[Rec. Claude]:** sí, por ser decisión ya tomada y de bajo alcance; puede excluirse sin afectar el resto.
- **Decisiones listadas para la Fase 1 en el roadmap:** P1, P2, P3, P4, P5, P9, P11, P12, P13 y Q-4. Constan resueltas en el registro; este paquete no las reabre.

## 8. Limitaciones heredadas (siguen abiertas; no se resuelven aquí)
- **C-2 y C-3:** abiertas por decisión expresa del propietario (aceptación del 20:26).
- **10 aplazamientos y su plazo según el registro:** P6 antes de cerrar la Fase 2; P7 antes de la Fase 5; P8 antes de la generación en la Fase 2; P10 antes de publicar; P15 antes de publicar externamente; Q-1 y Q-2 antes de la Fase 4; Q-3 antes de la Fase 5; Q-5 antes de la Fase 3; Q-6 antes de la Fase 2. **Ninguno vence antes de la Fase 1**, pero P10 condiciona cualquier despliegue.
- **Riesgos técnicos heredados (no verificados):** cuotas y expulsión de IndexedDB, Web Locks y multi-pestaña, compatibilidad de navegadores, esquema mal definido, nuevas dependencias. La integración de IA/CORS afecta a la Fase 2, no a la Fase 1.

## 9. Texto de decisión propuesto por Claude (el propietario puede copiarlo, cambiarlo o responder con el suyo)
> **Propuesta de Claude, NO es una decisión del propietario hasta que él la emita.** Los campos entre corchetes los completa el propietario; Claude no los rellena.
>
> «Autorizo el inicio de la Fase 1 («Fundamentos y Command Center») con este alcance: **[subfases: la Fase 1 completa del roadmap / el tramo que indico]**. Repositorio: **[nombre]**. Rama: **[nombre]**, creada desde **[línea base]**. Áreas modificables: **[lista]**; excluido `docs/fase0` y todo componente de servidor, base de datos remota o autenticación. Pruebas exigidas: AC1-01 a AC1-13 **[y AC1-14 si incluyo el perfil local]**, con 3 ejecuciones E2E consecutivas y verificación previa de Web Locks, cuotas de IndexedDB y compatibilidad de navegadores. Respaldo básico dentro de la Fase 1: **[sí/no]**. Perfil local en la Fase 1: **[sí/no]**. Commit y push: **[permitido solo en la rama de la Fase 1 / no permitido]**; merge y deploy: **no permitidos** salvo acto expreso posterior mío. La autorización no resuelve C-2, C-3 ni los 10 aplazamientos, no autoriza la Fase 2 y no implica la aceptación de la Fase 1, que exigirá evidencia y acto aparte.»

## 10. Estado tras este paquete
- Autorización de la Fase 1: **PENDIENTE** (sin cambio). Este documento no cambia ningún estado de decisión, aprobación, aceptación ni aplazamiento.
- Se mantiene la distinción entre ratificación B1–B10, aprobaciones 0.1–0.7, aceptación formal de la Fase 0 y autorización independiente de la Fase 1.
- Ya indicaste que no fusionamos con la vista previa privada; lo dejo solo como registro.

> **Nota fechada 2026-11-22 20:59 (respuesta del propietario; no es decisión nueva de este documento):** el propietario autorizó **únicamente la subfase S1.0** de la Fase 1 (auditoría técnica y definición del alcance ejecutable; rama `fase1/s1-0-auditoria` desde `7bcba74e05577761081d68ca14fdc19f2400248d`; solo lectura, pruebas existentes sin modificar y documentación/evidencia). Las subfases S1.1 y S1.2 quedan autorizadas solo tras su aprobación expresa de los resultados de S1.0 (no activas). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Autorización de la subfase S1.0». Las menciones anteriores de este documento a la autorización de la Fase 1 como pendiente o a «Fase 1 no autorizada» describen el estado previo y quedan superadas en ese punto; la Fase 1 en su conjunto NO está autorizada. **C-2, C-3 y los 10 aplazamientos siguen abiertos.**
