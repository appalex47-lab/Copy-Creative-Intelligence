# Paquete de decisión — aprobaciones formales 0.1 a 0.7
> **2026-11-22. Documento de apoyo: no emite ninguna aprobación.** Estado previo a la respuesta de 20:14: 0.1–0.7 = **0/7 emitidas** (todas PENDIENTES); Fase 0 **no aceptada**; Fase 1 **no autorizada**. Las recomendaciones son **[Rec. Claude], no vinculantes**. No se confunden: (1) la ratificación B1–B10 (ya hecha), (2) las aprobaciones 0.1–0.7 (pendientes), (3) la aceptación final de Fase 0 (pendiente) y (4) la autorización de Fase 1 (pendiente, independiente). Ni el silencio ni «Confirmo todo» (que ratificó B1–B10) se interpretan como aprobación. Contenido completo de cada ficha: `APROBACIONES_FASE0.md`. Reconciliación: `CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md`.
> **Nota fechada 2026-11-22 20:14 (respuesta del propietario; registrada en `REGISTRO_DECISIONES_RESUELTAS.md`):** «Apruebo 0.1 a 0.7 según las recomendaciones del paquete (0.5 solo en cuanto a principios; P8 sigue sin resolver y ninguna integración queda aprobada). R-1 sí.» Las siete aprobaciones están **emitidas por el propietario (7/7)** y R-1 queda como **aplazamiento aceptado, no resolución**. **La aceptación formal de Fase 0 y la autorización independiente de Fase 1 siguen PENDIENTES.** Las líneas «PENDIENTE», «0/7 emitidas» y «R-1 pendiente de respuesta» de este documento describen el estado **previo** a esa respuesta y quedan superadas; las recomendaciones pasaron a ser decisión solo por esa respuesta, con el alcance de cada ficha.

## 0.1 Diagnóstico
- **Aprobación:** 0.1 Diagnóstico — APROBADA (2026-11-22 20:14; estado previo: PENDIENTE).
- **Objeto:** Aceptar que el diagnóstico describe fielmente el estado real: el repositorio de la aplicación contiene la fundación comprobada y el producto CCI no existe; la línea `docs/fase0` (Supabase/RLS) es histórica y está superada.
- **Recomendación [Rec. Claude]:** Aprobada, con las limitaciones de la columna 4.
- **Fundamento:** El inventario, las conciliaciones y los controles automáticos del expediente son consistentes entre sí; lo no verificado está declarado.
- **Limitaciones:** C-2 (no se declara aceptada la Fase 0 v3.3 anterior como línea base vigente sin evidencia primaria). No se ejecutaron pruebas, build, E2E ni CI de la aplicación; `CCI-Evidence` devolvió 403 y no se usó; los anexos A/B y los documentos del repositorio de la aplicación no se leyeron.
- **Riesgos:** Aprobar el diagnóstico solo reconoce el estado observado, no la calidad del código.
- **Dependencias:** P3, P14 resueltas; sin dependencia de aplazamientos.
- **Texto de decisión propuesto (el propietario puede copiarlo o cambiarlo):** «Apruebo la ficha 0.1 (Diagnóstico) con las limitaciones expresas C-2 y la lista de lo no verificado.»

## 0.2 Arquitectura
- **Aprobación:** 0.2 Arquitectura — APROBADA (2026-11-22 20:14; estado previo: PENDIENTE).
- **Objeto:** Aprobar la especificación de arquitectura browser-only: un usuario por navegador; sin cuentas, login, backend, Supabase, PostgreSQL, SQL, servidor, multiusuario ni sincronización; IndexedDB como persistencia principal; Local Storage solo para preferencias ligeras; exportación/importación local como respaldo.
- **Recomendación [Rec. Claude]:** Aprobada.
- **Fundamento:** Todas las decisiones de las que depende están resueltas; los aplazamientos (P7, P10) no condicionan la arquitectura de Fase 1.
- **Limitaciones:** P7 (cifrado local) y P10 (hosting y origen) aplazados. Ningún soporte de navegador está probado: la matriz E2E se hará en Fase 1 o posterior. Web Locks, cuotas de IndexedDB y compatibilidad de navegadores no se verificaron técnicamente. La mitigación multi-pestaña depende de una implementación futura.
- **Riesgos:** La aprobación no declara soportado ningún navegador ni garantiza persistencia; son limitaciones documentadas.
- **Dependencias:** P1, P2, P9, P11, P12, P13 resueltas; P7 y P10 aplazadas (no bloquean).
- **Texto de decisión propuesto (el propietario puede copiarlo o cambiarlo):** «Apruebo la ficha 0.2 (Arquitectura browser-only) con las exclusiones y limitaciones indicadas.»

## 0.3 Dominio
- **Aprobación:** 0.3 Dominio — APROBADA (2026-11-22 20:14; estado previo: PENDIENTE).
- **Objeto:** Aprobar el modelo de dominio conceptual: 18 entidades con existencia y definición mínima (18/18), 13 relaciones sin cardinalidades obligatorias, atributos diferidos a cada módulo y convenciones transversales E1–E5.
- **Recomendación [Rec. Claude]:** Aprobada, con las limitaciones de la columna 4 (R-1 se responde por separado).
- **Fundamento:** Las 18 definiciones del registro coinciden literalmente con las del doc 03 y con la matriz consolidada (verificación automática); las relaciones no aprobadas están excluidas expresamente.
- **Limitaciones:** No se aprueban atributos, cardinalidades obligatorias, estados, ciclos de vida, persistencia, fórmulas, catálogos de métricas ni asignación de fase. Q-1 y Q-2 siguen aplazadas (antes de Fase 4). Cuestiones residuales sin decisión propia: la ubicación conceptual de la familia de reglas de copy (D-3) y las cinco cuestiones residuales de D-5 ((1) si la aprobación requiere auditoría o validaciones previas; (2) qué sucede cuando se modifica un contenido aprobado; (3) cómo se relaciona la aprobación con las versiones; (4) la identidad exacta del contenido al que se aplica cada aprobación; (5) la relación entre aprobación y los estados del flujo). Se plantean en la pregunta R-1 del paquete (aplazamiento, no resolución). D5.a–d permanecen fuera del alcance vigente y no se reabren.
- **Riesgos:** Aprobar el dominio no aprueba un esquema de datos: es un marco conceptual.
- **Dependencias:** P1, Q-7, P4 (B1–B5), D-1…D-8 resueltas; Q-1 y Q-2 aplazadas (no bloquean); R-1 (respondida «sí» a las 20:14: aplazamiento aceptado, no resolución).
- **Texto de decisión propuesto (el propietario puede copiarlo o cambiarlo):** «Apruebo la ficha 0.3 (Dominio) con las exclusiones y limitaciones indicadas.»

## 0.4 Persistencia
- **Aprobación:** 0.4 Persistencia — APROBADA (2026-11-22 20:14; estado previo: PENDIENTE).
- **Objeto:** Aprobar el diseño conceptual de persistencia local: IndexedDB principal, binarios como Blob separados de los metadatos, Local Storage solo para preferencias ligeras, exportación/importación como respaldo y recuperación, política de archivar frente a eliminar y hash SHA-256 de versiones.
- **Recomendación [Rec. Claude]:** Aprobada, con las limitaciones de la columna 4.
- **Fundamento:** Las decisiones de las que depende están resueltas; los tres aplazamientos asociados tienen fase límite declarada.
- **Limitaciones:** El alcance exacto del respaldo en Fase 1 es condicional («si se aprueba dentro del alcance de persistencia», B7) y lo decide el propietario al autorizar Fase 1. P6 (formato final de exportación) antes de cerrar Fase 2; P7 y P10 aplazadas. No hay límites de producto: dependen de pruebas reales de navegador. Cuotas y comportamiento de IndexedDB no se verificaron técnicamente.
- **Riesgos:** No se prometen exportaciones perfectas ni recuperación automática; la pérdida de datos por borrado del navegador es un riesgo documentado.
- **Dependencias:** P5, P9, P11, P12, P13, P4.E resueltas; P6, P7, P10 aplazadas; alcance del respaldo en Fase 1 condicional.
- **Texto de decisión propuesto (el propietario puede copiarlo o cambiarlo):** «Apruebo la ficha 0.4 (Persistencia) con las exclusiones y limitaciones indicadas.»

## 0.5 IA inicial
- **Aprobación:** 0.5 IA inicial — APROBADA solo en cuanto a principios (2026-11-22 20:14; estado previo: PENDIENTE).
- **Objeto:** Aprobar solo los principios de IA: la IA ayuda a crear, analizar y sugerir; reglas y cálculos deterministas; la aprobación final es humana; no hay claves privadas en el frontend ni secretos en Local Storage o IndexedDB. No es una aprobación de integración.
- **Recomendación [Rec. Claude]:** Aprobada con cambios: aprobar únicamente los principios, redactando expresamente que P8 sigue sin resolver y que ninguna integración queda aprobada.
- **Fundamento:** El doc 09 declara estado de propuesta; aprobarlo íntegro podría leerse como aprobar una alternativa de IA concreta.
- **Limitaciones:** P8 (estrategia de IA) está aplazada hasta antes de generación en Fase 2. La viabilidad de llamadas directas desde el navegador (CORS del proveedor) no fue verificada; el doc 09 es una propuesta de alternativas, no una decisión de proveedor.
- **Riesgos:** Aprobar los principios no aprueba un proveedor ni un modo de integración.
- **Dependencias:** Principios del propietario; P8 aplazada (antes de generación en Fase 2).
- **Texto de decisión propuesto (el propietario puede copiarlo o cambiarlo):** «Apruebo la ficha 0.5 (IA inicial) solo en cuanto a los principios de privacidad; P8 sigue sin resolver y no se aprueba ninguna integración.»

## 0.6 MVP
- **Aprobación:** 0.6 MVP — APROBADA (2026-11-22 20:14; estado previo: PENDIENTE).
- **Objeto:** Aprobar la definición del MVP: termina al concluir Fase 2 (Fase 1 Fundamentos y Command Center; Fase 2 Copy Studio).
- **Recomendación [Rec. Claude]:** Aprobada.
- **Fundamento:** Q-4 está resuelta y los documentos 10, 11 y 12 están alineados (control semántico S8).
- **Limitaciones:** Q-6 (idioma y diccionario) antes de Fase 2; P8 antes de generación en Fase 2; P6 antes de cerrar Fase 2. Las columnas de prioridad marcadas [P] siguen sin validar.
- **Riesgos:** La definición se limita a lo ratificado; las prioridades [P] no son decisiones.
- **Dependencias:** Q-4 resuelta; Q-6, P8 y P6 aplazadas con fase límite.
- **Texto de decisión propuesto (el propietario puede copiarlo o cambiarlo):** «Apruebo la ficha 0.6 (MVP hasta el final de Fase 2) con las exclusiones indicadas.»

## 0.7 Roadmap
- **Aprobación:** 0.7 Roadmap — APROBADA (2026-11-22 20:14; estado previo: PENDIENTE).
- **Objeto:** Aprobar el roadmap Fases 1–5 y sus criterios de aceptación como puertas de aceptación de referencia.
- **Recomendación [Rec. Claude]:** Aprobada.
- **Fundamento:** Las dependencias del roadmap coinciden con los aplazamientos de B8.
- **Limitaciones:** Diez aplazamientos aceptados, cada uno con fase límite: P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6. Los criterios de aceptación y las estimaciones son propuestas hasta aprobarse. P10 y P15 se resuelven antes de publicación, no antes de Fase 1.
- **Riesgos:** Aprobar el roadmap no es autorizar Fase 1: esa es una autorización aparte.
- **Dependencias:** Q-4 y las decisiones de arquitectura resueltas; diez aplazamientos con fase límite; C-2 y C-3 abiertas como limitaciones.
- **Texto de decisión propuesto (el propietario puede copiarlo o cambiarlo):** «Apruebo la ficha 0.7 (Roadmap Fases 1–5) como referencia; no autoriza el inicio de ninguna fase.»

## Detalle de la única recomendación «con cambios» (0.5)
Cambio exacto: aprobar solo el párrafo de principios (la IA ayuda a crear, analizar y sugerir; reglas y cálculos deterministas; aprobación final humana; sin claves privadas en el frontend ni secretos en Local Storage o IndexedDB) y añadir la frase «P8 sigue sin resolver y no se aprueba ninguna integración de IA». Motivo: el doc 09 contiene alternativas (IA-A, IA-B, IA-C) en estado de propuesta y aprobarlo entero podría leerse como aprobar una de ellas. Si el propietario prefiere aprobar sin cambios, la ficha lo permite y las exclusiones de la ficha siguen vigentes.

## Pregunta R-1 — aplazamiento de las cuestiones residuales de D-3 y D-5 (única; no bloquea 0.1–0.7) — respondida «sí» el 2026-11-22 20:14 (aplazamiento aceptado, no resolución)
**Qué se pregunta.** D-3 y D-5 son decisiones resueltas; cada una declara, además, cuestiones que expresamente **no decidió**. R-1 pide **una sola confirmación**: si esas **seis** cuestiones se aplazan hasta la especificación del módulo correspondiente, **sin alterar D-3 ni D-5**.

**Cuestiones incluidas (lista completa; fuente: `REGISTRO_DECISIONES_RESUELTAS.md`, D-3 y D-5, y la nota fechada de este registro):**
| N.º | Origen | Cuestión residual |
|---|---|---|
| 1 | D-3 | La **ubicación conceptual de la familia de reglas de copy** (D-3 la dejó «pendiente de P4.B»; la ratificación de P4.B no la fijó) |
| 2 | D-5, cuestión (1) | Si la aprobación requiere auditoría o validaciones previas |
| 3 | D-5, cuestión (2) | Qué sucede cuando se modifica un contenido aprobado |
| 4 | D-5, cuestión (3) | Cómo se relaciona la aprobación con las versiones |
| 5 | D-5, cuestión (4) | La identidad exacta del contenido al que se aplica cada aprobación |
| 6 | D-5, cuestión (5) | La relación entre aprobación y los estados del flujo |
La cuestión 1 **no es** la existencia de la familia de reglas de copy (ya distinguida por D-3), ni la separación entre ReglaDeMarca y ReglaComercial (decidida), ni las reglas por canal (dimensión del Canal, no entidad independiente aprobada), ni una ubicación técnica o estructura de datos (no aprobada).

**Redacción final (el propietario puede copiarla):** «R-1. Confirmo que se aplazan hasta la especificación del módulo correspondiente, sin modificar D-3 ni D-5, las seis cuestiones residuales listadas: la ubicación conceptual de la familia de reglas de copy (D-3) y las cinco cuestiones residuales de D-5 (auditoría o validaciones previas; modificación de un contenido aprobado; relación con las versiones; identidad exacta del contenido aprobado; relación con los estados del flujo).» Respuestas posibles: «R-1 sí» o «R-1 no: quiero decidir antes: …».

**Recomendación [Rec. Claude], no vinculante:** sí (aplazar), porque las seis cuestiones dependen de la especificación del módulo y decidirlas ahora ampliaría D-3 y D-5.

**Cómo se registraría la respuesta.** «Sí» = **aplazamiento aceptado** de subcuestiones (siguen **no decididas**; no es resolución conceptual; no se suman a las 20 decisiones resueltas ni a los 10 aplazamientos de nivel superior). «No» = se presentarán como decisiones nuevas y separadas, una por una.

**Lo que R-1 no hace.** No reabre D-5.1 (R3), D-5.2 (conjunto (b)) ni D-5.3 (M-1). No reabre D5.a–d: siguen fuera del alcance vigente, no son pendientes y no aparecen en R-1. No modifica la aprobación humana M-1. No aprueba mecanismos de aprobación, auditoría, versionado ni estados. No convierte ninguna cuestión aplazada en decisión tomada.

## Tabla compacta de las siete decisiones
| Ficha | Recomendación [Rec. Claude] | Texto que el propietario puede responder |
|---|---|---|
| 0.1 Diagnóstico | Aprobada (con C-2 y lo no verificado) | «Apruebo 0.1 con las limitaciones indicadas.» |
| 0.2 Arquitectura | Aprobada | «Apruebo 0.2.» |
| 0.3 Dominio | Aprobada con limitaciones (R-1 aparte) | «Apruebo 0.3 con las exclusiones indicadas.» |
| 0.4 Persistencia | Aprobada con limitaciones | «Apruebo 0.4 con las limitaciones indicadas.» |
| 0.5 IA inicial | Aprobada con cambios (solo principios) | «Apruebo 0.5 solo en cuanto a principios; P8 sigue sin resolver y ninguna integración queda aprobada.» |
| 0.6 MVP | Aprobada | «Apruebo 0.6 (MVP hasta el final de Fase 2).» |
| 0.7 Roadmap | Aprobada como referencia | «Apruebo 0.7; no autoriza ninguna fase.» |

Formato de respuesta único: «0.1 aprobada/rechazada/con cambios: …» y así hasta 0.7. Responder también, si se quiere, a R-1. Después, la aceptación final de Fase 0 y la autorización de Fase 1 son actos separados que se piden aparte.

## Qué falta de evidencia (para que la decisión sea informada)
No se ejecutaron pruebas, build, E2E ni CI de la aplicación; no se verificaron técnicamente Web Locks, cuotas de IndexedDB ni compatibilidad de navegadores; los anexos A/B y los documentos del repositorio de la aplicación no se leyeron; `CCI-Evidence` devolvió 403. La verificación es propia de la sesión, sin reproducción independiente. Estas carencias no impiden aprobar fichas conceptuales, pero sí limitan lo que la aprobación significa.
