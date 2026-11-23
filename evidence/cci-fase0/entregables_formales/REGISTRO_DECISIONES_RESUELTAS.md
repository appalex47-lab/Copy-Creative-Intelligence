# Decisiones resueltas por el propietario (Fase 0, browser-only)
Registro de decisiones respondidas expresamente. Solo se añaden respuestas literales del propietario; nada se infiere. Las decisiones históricas (DEC-D#, F11-D#) no se modifican.

## P1 — Identidad, organización, membresías y roles — RESUELTA el 2026-11-22
**Respuesta literal:** «P1 → (b). Decido adoptar un perfil local opcional, sin UserIdentity, Organization, Membership ni roles en el dominio operativo de CCI.»
**Implicaciones declaradas por el propietario (literal, resumidas en orden):**
1. Sin cuentas, usuarios autenticados, organizaciones, membresías ni administración multiusuario.
2. No se conservan admin, ecommerce, design, marketing y reviewer como roles operativos **ni como etiquetas de autorización** (descarta la opción c).
3. El perfil local incluye únicamente un nombre visible opcional, sin identidad autenticada.
4. `Membership.active` deja de tener aplicación en la arquitectura browser-only.
5. Workflow & Approvals es un flujo de un único usuario local, sin simular aprobadores diferentes.
6. F11-D1–D3 se conservan intactas; esta decisión determina su evolución futura sin reescribir su historia ni invalidar retroactivamente las aceptaciones anteriores.
7. No se modifica código ni repositorio en esta etapa.
**Alcance:** solo P1. No aprueba P4 (modelo de entidades), la aprobación 0.2/0.3, la Fase 0 ni la Fase 1. No se interpreta como respuesta a ninguna otra decisión.
**Consecuencias documentales (aplicadas en este expediente, no en el repositorio):** `13` y `../10` (estado de P1), `FICHA_P1`, `MATRIZ_DECISIONES_PROPIETARIO`, `05` (Identidad/Organización/Membresía/Rol: «no aplica»; nueva fila «Perfil local»), `06` (clave `profile` propuesta), `03` (R-014 propuesto), `12` (AC1-14 propuesto), `11`, `14` (RK-15, RK-16), `APROBACIONES_FASE0`, `CONCILIACION_D1_D9_VERIFICADA`.
**Consecuencias técnicas futuras (solo con Fase 1 autorizada; nada se hace ahora):**
- Retirar de código: `UserIdentity`, `Organization`, `Membership`, `MembershipRole`/`MEMBERSHIP_ROLES`, `NonEmptyReadonlyArray` (si solo se usa ahí), los servicios `identity`/`organizations`/`memberships`, fixtures y validación de roles del adaptador DEMO, el párrafo de membresía de `HomePage` y sus pruebas (7 archivos en `src/`; no hay referencias en `tests/` ni `e2e/`, comprobado por búsqueda). Actualizar `ARQUITECTURA.md` y `SEMANTICA_DE_SERVICIOS.md`.
- Añadir un perfil local opcional (el nombre se trata como texto no confiable: se escapa al mostrarlo).
- Esto retira trabajo ya aceptado (B1–B3) por **evolución**, no por invalidez: debe registrarse en un ADR sin reescribir los expedientes.
**Puntos que sigo tratando como propuesta mía (no decididos):** dónde se guarda el nombre (`settings` en IndexedDB, para que entre en el respaldo, frente a Local Storage), su longitud máxima, y los criterios AC1-14/R-014.
**Limitación aceptada a documentar:** con un solo usuario no hay separación de funciones (quien crea también aprueba); la aprobación sigue siendo una acción humana explícita (RK-16).
**No se marca ninguna aprobación 0.1–0.7, ni la aceptación de Fase 0, ni la autorización de Fase 1.**

## P2 — Sustitución formal de DEC-D2–D4 y «Fuente de verdad» — RESUELTA el 2026-11-22
**Respuesta literal:** «P2 → (a). Decido registrar un ADR de reemplazo que declare históricas las partes incompatibles de DEC-D2, DEC-D3, DEC-D4 y el apartado «Fuente de verdad», conservando íntegramente los registros originales y su trazabilidad.»
**Alcance declarado por el propietario (resumen fiel):**
1. DEC-D2: se conserva la separación contratos/adaptadores; se retira Supabase como implementación prevista o dependencia; un backend futuro requerirá una nueva decisión.
2. DEC-D3: PostgreSQL y Supabase ya no son la fuente de verdad; la persistencia principal es IndexedDB en el navegador.
3. DEC-D4: CCI-DEV y CCI-PROD como proyectos Supabase independientes dejan de ser requisitos; se conserva como antecedente no reutilizar proyectos de RevNavigator.
4. Fuente de verdad: datos operativos locales; sin cuentas, autenticación, backend, servidor ni sincronización multidispositivo; exportación/importación local como parte del respaldo y recuperación.
5. Conservación histórica: sin borrar ni reescribir; el ADR identifica qué queda reemplazado y qué permanece; sin modificar retroactivamente aceptaciones.
**Restricción de ejecución del propietario:** registrar en el expediente; no modificar el repositorio, no crear commits, no tocar ramas, no fusionar ni publicar el ADR en GitHub.
**Resultado:** ADR redactado como `ADR_PROPUESTO_REEMPLAZO_DEC_D2_D3_D4.md` (no publicado).
**Interpretación mía a confirmar:** «conservar como antecedente» la instrucción de no reutilizar RevNavigator significa que consta como antecedente y **no** se convierte en un requisito nuevo.
**Contradicción residual señalada, no decidida:** «Seguridad por diseño» de `ARQUITECTURA.md` (autoridad del backend, RLS) queda fuera del alcance expreso de P2.
**No aprueba** P3, las aprobaciones 0.1–0.7, la Fase 0 ni la Fase 1.

## P3 — Tratamiento de `docs/fase0/` y expedientes Supabase/SQL/RLS/multiusuario — RESUELTA el 2026-11-22
**Respuesta literal:** «P3 → (b). Decido conservar "docs/fase0/" y los expedientes relacionados como antecedentes históricos y permitir su consulta como referencia conceptual no vinculante.»
**Condiciones del propietario (literales, resumidas en orden):**
1. Los documentos originales se conservan íntegros.
2. Pueden consultarse conceptos y vocabulario del dominio, como campañas, piezas creativas, versiones de copy, aprobaciones e historial de actividad.
3. Ninguna entidad, regla, permiso, tabla o mecanismo técnico se incorpora automáticamente al dominio browser-only.
4. Cada concepto que se quiera recuperar debe evaluarse en P4 y someterse a su aprobación cuando corresponda.
5. Los 17 permisos, RLS, SQL, disparadores, restricciones de base de datos y arquitectura multiusuario permanecen sin aprobación y fuera de la arquitectura vigente.
6. El índice debe distinguir entre antecedente histórico y referencia conceptual no vinculante.
7. Las contradicciones históricas C-2 y C-3 se mantienen abiertas; P3 no las resuelve ni las modifica.
**Resultado:** índice creado: `INDICE_ANTECEDENTES_HISTORICOS.md`. **No aprueba** P4, las aprobaciones 0.1–0.7, la Fase 0 ni la Fase 1.

## Aclaración sobre RevNavigator — registrada el 2026-11-22
**Literal:** «Confirmo que la instrucción de no reutilizar proyectos Supabase de RevNavigator se conserva como antecedente histórico, no como requisito operativo de CCI. La arquitectura vigente no utiliza Supabase.»
Confirma la interpretación que había propuesto. Se refleja en el ADR propuesto.

## Ampliación del alcance de P2 — «Seguridad por diseño» — RESUELTA el 2026-11-22
**Respuesta literal:** «También decido extender P2 para incluir el apartado «Seguridad por diseño» de "ARQUITECTURA.md".»
**Alcance declarado:**
- El ADR propuesto identifica como históricos o reemplazados los planteamientos de autoridad del backend, RLS y aislamiento por organización, conservando íntegramente los textos originales.
- La formulación vigente corresponde a una aplicación local de un solo usuario por navegador, sin backend, cuentas ni permisos multiusuario; aborda las amenazas y limitaciones reales de la seguridad local sin prometer confidencialidad frente a otras personas con acceso al dispositivo o navegador.
- **Límite:** no autoriza modificar el repositorio ni publicar el ADR; se limita al expediente documental.
**Resultado:** `ADR_PROPUESTO_REEMPLAZO_DEC_D2_D3_D4.md` actualizado (fila de «Seguridad por diseño» y §2 bis, formulación vigente). Dos puntos para tu verificación, no decididos: (1) de la frase original conservé como vigentes «sin claves en el cliente», «`.env*` ignorados salvo `.env.example`» y «no hay autenticación ni aislamiento por organización simulados» porque son compatibles; (2) los controles técnicos listados en §2 bis son propuestas sujetas a P13, no decisiones.

## P4 — Modelo de entidades — respuestas parciales del 2026-11-22 (P4 NO está cerrada)
**P4.1 — Entidades originales: PENDIENTE.** El propietario pidió la lista original completa con trazabilidad antes de aprobar; entregada en `LISTA_ORIGINAL_18_ENTIDADES.md`. **No está aprobada.** Se señaló además que existen dos listas del propietario (18 en la instrucción de Fase 0, 16 en la maestra).
**P4.2 — RESUELTA → (b).** Literal: «Decido mantener dos entidades independientes: ReglaDeMarca. ReglaComercial. No fusionarlas en una entidad genérica.»
**P4.3 — Entidades añadidas (literal resumido):**
- Evento de actividad: **APROBADA COMO ENTIDAD PROPUESTA**, para registrar actividad real del Command Center; su estructura y eventos concretos **deberán especificarse posteriormente**.
- Etiqueta: **APROBADA** (Copy Studio requiere etiquetar y buscar).
- Perfil local: **APROBADO**, conforme a P1, sin autenticación ni identidad de usuario.
- Colección: **PENDIENTE**; no se aprueba como entidad independiente hasta justificar qué necesidad funcional resuelve que no cubran etiquetas y filtros. (Mi análisis: no encontré justificación en tus instrucciones; la excluí del modelo.)
- «Estas decisiones no autorizan implementación.»
**P4.4 — APLAZADO hasta resolver Q-7.** Literal: «Conserva íntegramente F11-D5. No equipares Project con Campaña ni recuperes Project por inferencia.»
**P4.5 — Convenciones transversales: NO se aprueba el paquete completo.** Posición del propietario, **registrada como preliminar**:
| Convención | Decisión | Limitación / condición |
|---|---|---|
| UUID v4 generado en cliente | APROBADO | — |
| Fechas ISO-8601 UTC | APROBADO **como formato de almacenamiento** | Condición: preservar la semántica de fechas comerciales y zonas horarias |
| `revision` (control optimista) | **NO APROBADO como requisito obligatorio** | Debe justificarse una necesidad real en la arquitectura local (ver abajo) |
| `archivedAt` | APROBADO **condicionalmente** | Archivar y eliminar deben ser operaciones distintas y estar documentadas |
| Importes en unidad menor + moneda | APROBADO | — |
| Valores desconocidos como `null` | APROBADO | Distinguir desconocido de cero, vacío y no aplicable |
| Versiones inmutables con hash | APROBADO **como principio de integridad y trazabilidad** | **No** es una garantía de seguridad |
**Las condiciones se atienden en `CONVENCIONES_P4_5_CONDICIONES.md`** (propuestas mías para tu validación; no se dan por aprobadas). **No aprueba** P5, Q-7, las aprobaciones 0.1–0.7, la Fase 0 ni la Fase 1.

## P4.1 — Lista de referencia del modelo de entidades — RESUELTA PARCIALMENTE el 2026-11-22 (solo nombres)
**Respuesta literal:** «Confirmo que la lista de referencia para el modelo de entidades es la lista de 18 entidades del §7 de la instrucción de Fase 0, líneas 348–365. La lista de 16 conceptos de la instrucción maestra se conserva como antecedente de alcance general, pero no sustituye la lista específica de 18 entidades.»
**Alcance exacto:** aprueba **la lista de nombres** como referencia del modelo. **NO aprueba** las definiciones, relaciones, atributos, dependencias ni asignaciones de fase que yo haya derivado o propuesto. La procedencia (solicitado / derivado / propuesta mía) se mantiene identificada en `LISTA_ORIGINAL_18_ENTIDADES.md`.

## Q-7 — `Campaña` frente a F11-D5 — RESUELTA el 2026-11-22 → (a)
**Respuesta literal:** «Q-7 → (a). Decido incorporar "Campaña" como una entidad nueva del dominio browser-only, definida expresamente en mis instrucciones vigentes.»
**Condiciones (literales, resumidas en orden):**
1. «Campaña» no equivale a «Project».
2. F11-D5 permanece **íntegra y vigente** como registro histórico.
3. «Project» no se recupera ni se incorpora al contrato de aplicación por inferencia.
4. La referencia histórica a «campaigns» en los expedientes de Supabase es únicamente conceptual y no vinculante.
5. Las relaciones de Campaña con Brief, Oferta, Pieza y Resultado deben documentarse como parte del modelo **propuesto**, sin asumir que todos sus atributos o cardinalidades están aprobados.
**Qué aprueba:** la **existencia** de la entidad Campaña. **Qué no aprueba:** sus atributos ni sus cardinalidades. **Nota mía de procedencia:** de las cuatro relaciones citadas, solo Campaña–Brief y Campaña–Resultado tienen apoyo en tus listas de campos (maestra l.347 y l.639); Campaña–Oferta y Campaña–Pieza son **propuesta mía** sin base explícita (ver `DECISIONES_P4_PENDIENTES.md`).

## Colección — decisión mantenida el 2026-11-22
**Literal:** «mantengo la decisión de no incorporarla como entidad independiente mientras no exista una necesidad funcional demostrable que no cubran Etiqueta, filtros y búsqueda.» No forma parte del modelo; se reabriría solo con esa demostración.

## P4.5 — Aprobación preliminar conservada el 2026-11-22
**Literal:** «conserva mi aprobación preliminar y sus condiciones tal como quedaron registradas. No la conviertas todavía en aprobación definitiva de todas las convenciones. Presenta por separado las decisiones que sigan pendientes.» La tabla de P4.5 de arriba permanece **preliminar**.

**No aprueban** P5, las aprobaciones 0.1–0.7, la Fase 0 ni la Fase 1. No autorizan implementación.

## Confirmaciones del propietario — 2026-11-22 11:38
- P4.D: Q-7 = (a) **cierra P4.4**. No se reabre F11-D5 ni se establece equivalencia Campaña–Project.
- P4.A: no se aprueban las 18 definiciones en bloque; se resuelven una por una (ficha por entidad: nombre canónico, definición, cita, clasificación, ambigüedades, recomendación). Ninguna definición derivada se aprueba automáticamente. Entidad 1 presentada: `FICHA_P4A_01_CAMPANA.md` (pendiente).
- P4.B: se conservan como con fundamento solo las relaciones respaldadas expresamente por las instrucciones; sus cardinalidades se presentan y justifican por separado; Campaña–Oferta y Campaña–Pieza = propuestas pendientes, a resolver individualmente después de P4.A.
- P4.C: atributos diferidos a la especificación de cada módulo; solo se presentarán antes los indispensables para el MVP, con justificación; ninguno aprobado.
- P4.E: E1–E5 pendientes; E2 (`revision`) espera a P12; las recomendaciones técnicas no son decisiones del propietario.
- No se fusiona con la vista previa privada; expediente separado. Sin cambios a 0.1–0.7, Fase 0 ni Fase 1.

## P4.A — Entidad 1: Campaña — RESUELTA el 2026-11-22 11:40 → opción (b), definición mínima del propietario
**Definición aprobada (literal):** «Campaña es una entidad propia de CCI, creada por el usuario e identificada por un nombre. Puede ser referenciada por un Brief y por un Resultado de desempeño, y puede utilizarse como criterio de catalogación en Creative Library.»
**Aprueba:** la existencia de Campaña como entidad propia; esta definición mínima y las capacidades expresamente respaldadas por las citas presentadas.
**NO aprueba:** definirla como «agrupador» con implicaciones adicionales; atributos; obligatoriedad de referencias; cardinalidades; estados; vigencia; reglas de ciclo de vida; relaciones Campaña–Oferta y Campaña–Pieza (pendientes); asignación de fase (pendiente de Q-4).
**Se mantiene:** distinción respecto de `Project`; F11-D5 íntegra. No se extiende a código ni implementación; no se fusiona con la vista previa privada.

## P4.A — Entidad 2: Brief — RESUELTA el 2026-11-22 11:41 → opción (b), definición mínima del propietario
**Definición aprobada (literal):** «Brief es una entidad propia de CCI que el usuario completa y que reúne información de partida para la creación de contenido (copy). Puede contener información incompleta.»
**Aprueba:** la existencia de Brief como entidad propia y la definición mínima.
**Reconoce sin aprobar:** los 13 campos de B l.345–359 como contenido contemplado en las instrucciones originales (no como atributos definitivos, ni sus tipos, obligatoriedad, validaciones o estructura); que pueden existir Briefs incompletos (sin estados, reglas de completitud ni mecanismos de validación).
**NO aprueba:** cardinalidades ni relaciones formales con Campaña, Producto, Oferta o Copy; que Brief pertenezca obligatoriamente a una Campaña; asignación de fase (pendiente de Q-4).
**No resuelve:** posible duplicidad entre Vigencia/Condiciones del Brief y datos de Oferta.
No se extiende a código, implementación ni decisiones pendientes; sin fusión con la vista previa privada.

## P4.A — Entidad 3: Producto — RESUELTA el 2026-11-22 11:44 → opción (b), definición mínima del propietario
**Definición aprobada (literal):** «Producto es una entidad propia de CCI que representa un producto comercial referenciado en la información de un Brief y considerado por el proceso de validación promocional.»
**Aprueba:** la existencia de Producto como entidad propia (conforme a la lista confirmada en P4.1) y exclusivamente la definición mínima.
**NO aprueba:** atributos, identificadores comerciales, SKU, catálogo, origen de datos, mecanismos de captura o importación; relaciones formales ni cardinalidades con Brief, Oferta u otras entidades; reutilización mediante catálogo; relación N–N con Oferta; reglas de validación promocional adicionales a reconocer que Producto es considerado por ese proceso; asignación de fase (pendiente de Q-4).
No se extiende a código, implementación ni decisiones pendientes; sin fusión con la vista previa privada.

## P4.A — Entidad 4: Oferta — RESUELTA el 2026-11-22 11:47 → opción (b), definición mínima del propietario
**Definición aprobada (literal):** «Oferta es una entidad propia de CCI que representa una oferta comercial asociada al contenido que se crea o revisa. Su información comercial puede ser relevante para la validación de promociones.»
**Aprueba:** la existencia de Oferta como entidad propia (conforme a P4.1) y exclusivamente la definición mínima.
**Aclara:** no se establece que Oferta y Promoción sean conceptos equivalentes o intercambiables.
**Reconoce sin aprobar:** los elementos de B l.508–517 como aspectos contemplados para la validación promocional, no como atributos de Oferta.
**NO aprueba:** atributos ni estructura de datos; relaciones ni cardinalidades con Campaña, Producto, Brief, Copy u otras; cálculos, fórmulas, tolerancias, redondeos ni reglas concretas del Promotion Validator; asignación de fase (pendiente de Q-4).
**No resuelve:** duplicidad entre Vigencia/Condiciones del Brief e información de Oferta.
No se extiende a código, implementación ni decisiones pendientes; sin fusión con la vista previa privada.

## P4.A — Entidad 5: Copy — RESUELTA el 2026-11-22 11:48 → opción (b), definición mínima del propietario
**Definición aprobada (literal):** «Copy es una entidad propia de CCI que representa contenido textual creado o escrito por el usuario y que puede utilizarse como objeto de edición, auditoría, validación y adaptación a distintos canales.»
**Aprueba:** la existencia de Copy como entidad propia y exclusivamente la definición mínima.
**Reconoce sin aprobar:** titulares, textos principales, descripciones y CTA como componentes mencionados (no atributos obligatorios ni estructura fija); las capacidades de Copy Studio de las fuentes (no se convierten en atributos ni reglas del dominio).
**NO aprueba:** relaciones ni cardinalidades con Brief, Campaña, Oferta, CopyVariant, ContentVersion u otras; estados, estructura interna, obligatoriedad de componentes ni reglas de versionado; reglas de copy, auditoría ni validación (su existencia como funcionalidad no aprueba sus criterios); asignación de fase (pendiente de Q-4).
**No resuelve:** cómo se distingue un Copy escrito por el usuario de uno generado mediante IA.
No se extiende a código, implementación ni decisiones pendientes; sin fusión con la vista previa privada.

## P4.A — Entidad 6: Variante de copy — RESUELTA el 2026-11-22 11:51 → opción (b), definición mínima del propietario
**Definición aprobada (literal):** «Variante de copy es una entidad propia de CCI que representa una alternativa de contenido textual contemplada en el proceso de creación y generación de copy, que el usuario puede administrar y conservar de forma persistente.»
**Aprueba:** la existencia de Variante de copy como entidad propia (conforme a P4.1) y exclusivamente la definición mínima.
**Reconoce sin aprobar:** alternativas de tono, variantes por objetivo y propuestas A/B como modalidades mencionadas (no tipos, categorías ni clasificaciones definitivas).
**NO aprueba:** relación de pertenencia con Copy ni cardinalidades; atributos, estructura interna, estados ni reglas de comparación; equivalencia ni distinción técnica definitiva respecto de ContentVersion (esa delimitación **debe resolverse antes de especificar el modelo**); relaciones con Canal u otras entidades; reglas de experimentación A/B ni mecanismos de medición; asignación de fase (pendiente de Q-4).
No se extiende a código, implementación ni decisiones pendientes; sin fusión con la vista previa privada.

## P4.A — Entidad 7: Pieza creativa — RESUELTA el 2026-11-22 11:52 → opción (b), definición mínima del propietario
**Definición aprobada (literal):** «Pieza creativa es una entidad propia de CCI que representa un recurso visual que puede ser objeto de auditoría visual y conservarse en Creative Library.»
**Aprueba:** la existencia de Pieza creativa como entidad propia (conforme a P4.1) y exclusivamente la definición mínima.
**Reconoce sin aprobar:** que las instrucciones contemplan piezas visuales, auditoría visual y conservación en Creative Library; que contemplan evaluar la congruencia copy-pieza (sin relación formal ni reglas).
**NO aprueba:** tipos de archivo, formatos, dimensiones, metadatos ni estructura interna; mecanismos de incorporación, carga manual, almacenamiento binario, referencias externas ni políticas de almacenamiento; relaciones ni cardinalidades con Copy, Campaña, ContentVersion u otras; versionado, límites de tamaño, cuotas, exportación ni recuperación de archivos; criterios ni reglas de auditoría visual; asignación de fase (pendiente de Q-4).
No se extiende a código, implementación ni decisiones pendientes; sin fusión con la vista previa privada.

## P4.A — Entidad 8: Auditoría creativa — RESUELTA el 2026-11-22 11:55 → opción (b), definición mínima del propietario
**Definición aprobada (literal):** «Auditoría creativa es una entidad propia de CCI que representa una evaluación realizada sobre un copy o una pieza creativa, cuyo resultado puede incluir hallazgos y una puntuación explicable, y que puede conservarse para consulta y seguimiento.»
**Aprueba:** la existencia de Auditoría creativa como entidad propia (conforme a P4.1) y exclusivamente la definición mínima.
**Reconoce sin aprobar:** auditorías de copy y visuales, auditorías repetidas, conservación en Creative Library y auditorías vinculadas a versiones, como capacidades contempladas en las instrucciones.
**NO aprueba:** que toda auditoría deba producir necesariamente una puntuación; criterios, ponderaciones, fórmulas, escalas ni reglas de puntuación; estructura del resultado, tipos de hallazgos ni niveles de severidad; si el objeto auditado se referencia directamente (Copy/Pieza) o mediante una versión; relaciones ni cardinalidades con Copy, Pieza creativa, ContentVersion, Hallazgo, ReglaDeMarca u otras; atributos, estados ni reglas de ciclo de vida; asignación de fase (pendiente de Q-4).
**No resuelve:** si una reauditoría genera un registro nuevo o modifica uno anterior.
No se extiende a código, implementación ni decisiones pendientes; sin fusión con la vista previa privada.

## Ajuste de método de P4.A — 2026-11-22 11:58
El propietario ordena una **revisión integral de coherencia de las 18 entidades** antes de continuar con las entidades 9 a 18. Entidades 1–8: decisiones intactas. Entidad 9 (Hallazgo de auditoría): **sigue pendiente de decisión** hasta revisar la coherencia del conjunto. No se presenta ninguna entidad nueva; no se avanza a P4.B, P4.C, Q-4 ni E1–E5; no se asignan fases como decisión. Entregables: `DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md` y `MATRIZ_CONSOLIDADA_18_ENTIDADES.md` (ambos **propuestas/diagnóstico, sin aprobar nada**).

## Instrucciones del propietario — 2026-11-22 12:01 (tras el diagnóstico integral)
- **Perfil local:** NO se trata como componente de Configuración; su existencia como entidad (P4.3) se mantiene. Cualquier cambio exigiría autorización expresa.
- **Reglas de copy:** NO se incorporan automáticamente a ReglaDeMarca. Las instrucciones distinguen reglas de copy, de marca, comerciales y por canal; la separación ReglaDeMarca/ReglaComercial (P4.2) no resuelve por sí sola las otras dos familias.
- **Aprobación y Métrica:** NO se eliminan ni retiran; sus nombres forman parte de las 18 entidades confirmadas en P4.1. Pueden diferirse sus definiciones y especificaciones; cualquier propuesta para cambiar su condición de entidad sería una revisión explícita de P4.1.
- **Orden controlado:** se resuelve primero D-1 (qué objetos son contenido). D-2 y D-3 no se resuelven aún. No se presenta ninguna entidad nueva; Hallazgo de auditoría (9) sigue sin aprobar. Entregable: `D1_ANALISIS_CONTENIDO.md` (análisis y recomendación; **no aprueba nada**).

## D-1 — Qué objetos son «contenido» — RESUELTA el 2026-11-22 12:04 (exclusivamente D-1)
**D-1.a → A.** «Contenido» es un **concepto paraguas sin entidad propia**: término conceptual que puede abarcar modalidades textuales y visuales. No añade una entidad 19 ni modifica la lista confirmada en P4.1.
**D-1.b → (ii).** La **adaptación** es un concepto propio derivado de un copy fuente, con identidad conceptual y trazabilidad propia. **No aprueba** atributos, relaciones, cardinalidades, estructura interna ni reglas de persistencia adicionales. No es una entidad 19: se mantiene dentro de las 18 entidades confirmadas en P4.1 (se entiende como la entidad `ChannelAdaptation`, nº 13).
**D-1.c → (a).** No se amplía por ahora Auditoría creativa: su definición aprobada sigue limitada a evaluaciones sobre Copy o Pieza creativa. **No se aprueba** auditar adaptaciones; cualquier ampliación requiere decisión expresa.
**D-1.d → (a) parcial.** Copy, Pieza creativa y Adaptación se reconocen como conceptos que **pueden tener versiones**. **No aprueba** estructuras, atributos, relaciones ni mecanismos de versionado. **No se aprueba** que los tres sean necesariamente aprobables: el alcance de la aprobación queda pendiente de **D-5**. La expresión «contenido aprobado» (B l.633) **no** es decisión suficiente para establecer qué entidades tienen aprobación.
**D-1.e → (a), lectura de trabajo provisional.** «Adaptación creativa» y «Channel Adaptation» se tratan como el **mismo concepto**; se documenta la diferencia de orden del flujo en las instrucciones originales (B l.19/A l.44 frente a B l.673). No se crean dos conceptos ni se resuelve la inconsistencia del proceso.
**Preservación:** entidades 1–8 intactas; Hallazgo de auditoría (9) sigue sin aprobar. No se avanza a D-2, D-3, P4.B ni P4.C. Sin cambios a código, documentos históricos ni repositorio.

## D-2 — Variante de copy frente a Versión — PRESENTADA el 2026-11-22 12:07 (pendiente de decisión)
Instrucción del propietario: desarrollar exclusivamente D-2 con evidencia, alternativas (A separados, B unificados, C variante como clasificación de versión) y recomendación, sin cambiar entidades 1–8, D-1, atributos/relaciones/cardinalidades/mecanismos, D-3, D-5, P4.B ni P4.C. Entregable: `D2_VARIANTE_FRENTE_A_VERSION.md` (**no aprueba nada**). Hallazgo de auditoría (9) sigue sin aprobar.

## D-2 — Variante de copy frente a Versión — RESUELTA el 2026-11-22 12:09 (exclusivamente D-2)
**D-2.a → A, conceptos separados.** Distinción conceptual adoptada: **Variante de copy** = alternativa de contenido textual que puede coexistir con otras alternativas; **Versión** = evolución o revisión temporal de un contenido. Ambas tienen propósitos conceptuales diferentes; se mantiene vigente la existencia de Variante de copy aprobada en P4.A. **No aprueba** relaciones, cardinalidades, atributos, estructuras, mecanismos de versionado ni reglas de ciclo de vida.
**D-2.b → (ii), no por ahora, sin excluirlo a futuro.** No se aprueba que Variante de copy tenga su propio historial de versiones; tampoco se prohíbe definitivamente. Queda pendiente de una justificación funcional y de una decisión posterior.
**D-2.c → (a), no ampliar por ahora.** Se conserva exactamente la definición aprobada de la entidad 8 (evaluación sobre un Copy o una Pieza creativa). **No se aprueba** auditar directamente una Variante de copy; cualquier ampliación requiere decisión expresa.
**Preservación:** entidades 1–8 intactas; D-1 sin modificaciones; Hallazgo de auditoría (9) sin aprobar.
**Siguen pendientes:** relaciones y cardinalidades entre Copy, Variante y Versión; presencia de Variante en la Creative Library; definición de ContentVersion (14), de la que solo está confirmado el nombre. No se resuelven D-3 ni D-5; no se avanza a P4.B ni P4.C. Sin cambios a código, documentos históricos ni repositorio.

## D-3 — Familias de reglas — PRESENTADA el 2026-11-22 12:11 (pendiente de decisión)
Autorizada por el propietario como análisis de las cuatro familias (reglas de copy, de marca, comerciales y por canal) con tres alternativas mínimas (A cuatro familias diferenciadas, B dos entidades, C modelo genérico). Restricciones: no presuponer que todas sean entidades; P4.2 no implica que las reglas de copy pertenezcan a ReglaDeMarca ni que las de canal sean entidades independientes; D-1 y D-2 íntegras; sin atributos, relaciones, cardinalidades, prioridades, severidades, fórmulas ni mecanismos; sin D-4, D-5, P4.B ni P4.C; sin entidad nueva. Entregable: `D3_FAMILIAS_DE_REGLAS.md` (**no aprueba nada**).

## D-3 — Familias de reglas — RESUELTA el 2026-11-22 12:14 (exclusivamente D-3)
**D-3.a → (a), cuatro familias distintas:** reglas de copy, reglas de marca, reglas comerciales y reglas por canal. La distinción se fundamenta en propósitos, objetos regulados y contextos funcionales. **No significa** que deban existir cuatro entidades independientes.
**D-3.b → (a).** Se mantienen **únicamente ReglaDeMarca y ReglaComercial** como entidades independientes (P4.1, P4.2). **No se autoriza** agregar entidades para reglas de copy ni para reglas por canal. No se aprueban atributos, estructuras internas, relaciones, cardinalidades ni mecanismos de administración.
**D-3.c — Reglas por canal → (i).** Se reconocen como **dimensión de aplicación del Canal**, sin entidad independiente y sin convertirlas automáticamente en especialización de ReglaDeMarca. No se aprueba cómo se representarán ni cómo se relacionarán con Canal o Adaptación.
**D-3.c — Reglas de copy → (i).** Familia conceptual diferenciada; su **ubicación en el modelo queda pendiente de P4.B**. No se incorporan a ReglaDeMarca ni se convierten en entidad independiente sin decisión posterior.
**D-3.d → aprobado.** Criterios para distinguir las familias: **propósito, objeto regulado y contexto o fase funcional**. Se documenta el **solapamiento** de longitud, formato, tono y CTA entre reglas de copy y reglas por canal; ese solapamiento **no autoriza** duplicar reglas ni establecer prioridades, precedencias o mecanismos de resolución de conflictos.
**Corrección de antecedentes (conservada):** incorporar reglas de copy dentro de ReglaDeMarca fue derivación mía anterior y **queda sin efecto**.
**Limitación de la evidencia (documentada):** las instrucciones originales **no contienen una lista específica de reglas de marca** (a diferencia de reglas de copy, comerciales y por canal); no se inventa una. Solo aparecen «Reglas de marca» como criterio de auditoría (B l.435; A l.589), «Consistencia de marca» (B l.444) y el módulo «Brand Intelligence / Settings».
**Preservación:** P4.1, P4.2, D-1 y D-2 intactas; entidades 1–8 sin cambios; Hallazgo de auditoría (9) sin aprobar. No se avanza a D-4, D-5, P4.B ni P4.C. Sin cambios a código, documentos históricos ni repositorio.

## Recuperación del catálogo D-4 a D-8 — 2026-11-22 12:16 (sin decisiones)
Instrucción del propietario: recuperar y verificar el alcance original de D-4 a D-8 antes de desarrollar D-4; sin desarrollar D-4, sin avanzar a D-5 ni otras dependencias, sin entidades nuevas. Entregable: `CATALOGO_DEPENDENCIAS_D4_D8.md` (**no aprueba nada**). D-3 cerrada con sus límites; P4.1, P4.2, D-1, D-2 y D-3 intactas.

## D-4 reformulada (pendiente) y D-5 presentada — 2026-11-22 12:21
**D-4 — reformulada a asuntos residuales; sigue pendiente; no se desarrolla todavía.** El propietario no la considera completamente resuelta por D-1.b ni mantiene su formulación original. D-1.b queda firme: Adaptación es un concepto propio, derivado de un Copy fuente, con identidad y trazabilidad, que corresponde a la entidad 13 (`ChannelAdaptation`); **no se vuelve a plantear ni se presenta como pendiente.** Asuntos residuales exclusivos: (1) delimitación conceptual entre Adaptación, Copy, Variante de copy y Versión; (2) si una adaptación visual puede vincularse con una Pieza creativa y bajo qué distinción; (3) definición mínima de la entidad 13. No se presupone que toda adaptación tenga Pieza, que sea variante o versión, ni que pueda auditarse (D-1.c: Auditoría solo sobre Copy y Pieza).
**D-5 — autorizada y presentada como propuesta pendiente de decisión.** Análisis exclusivamente de D-5 (representación de la aprobación, objetos aprobables, significado y alcance) con D-1.d y D-2 como antecedentes obligatorios. La asociación del «19» con Evento de actividad es una **inferencia mía no confirmada** y **no se asume**. No se aprueban atributos, relaciones, cardinalidades, estados, flujos, mecanismos ni estructuras. Entregable: `D5_APROBACION.md` (**no aprueba nada**). Sin D-6, D-7, D-8, P4.B ni P4.C; sin entidades nuevas.

## D-5 — Aprobación — RESUELTA el 2026-11-22 12:29 (exclusivamente D-5)
**D-5.1 → R3.** Se distingue conceptualmente el **estado del contenido** (la situación del contenido dentro del flujo) y la **aprobación** (una decisión humana registrada). Tienen propósitos distintos y no se tratan como equivalentes. **No aprueba:** dos entidades independientes, una fuente de verdad, relaciones, cardinalidades, atributos, mecanismos de transición ni estructuras de almacenamiento. **P4.1 se conserva intacta**; si una implementación futura requiere revisar el inventario de entidades, se presentará como decisión independiente.
**D-5.2 → conjunto (b).** **Copy:** aprobable. **Pieza creativa:** aprobable. **Adaptación:** su posible aprobación queda pendiente de D-4 y de una decisión posterior expresa. **Variante de copy, Campaña, Brief, Producto y Oferta:** fuera del alcance actual de aprobación; la exclusión **no** es prohibición permanente ni decisión sobre su aprobación futura. La posibilidad de tener versiones **no** implica automáticamente que un objeto sea aprobable.
**D-5.3 → M-1.** La aprobación es una **decisión humana final por la que se considera que un contenido concreto, en las condiciones en que fue revisado, está conforme para pasar a la Biblioteca.** Límites expresos: no certifica por sí misma el cumplimiento legal, comercial o de marca; no sustituye auditorías ni validaciones; no implica publicación, distribución ni autorización de uso en canales externos; no determina si una auditoría o validación previa es obligatoria; no resuelve qué sucede cuando se modifica el contenido aprobado; no establece cómo se identifica o referencia técnicamente el contenido revisado ni su relación con las versiones.
**Cuestiones que permanecen abiertas (no se resuelven por derivación):** (1) si la aprobación requiere auditoría o validaciones previas; (2) qué sucede cuando se modifica un contenido aprobado; (3) cómo se relaciona la aprobación con las versiones; (4) la identidad exacta del contenido al que se aplica cada aprobación; (5) la relación entre aprobación y los estados documentados en el flujo.
**Preservación:** P4.1, D-1, D-2, D-3 y la reformulación de D-4 intactas; entidades 1–8 sin cambios; Hallazgo de auditoría (9) sin aprobar; definición de la entidad 15 (Aprobación) **no** presentada. No se avanza a D-6, D-7, D-8, D-4, P4.B ni P4.C. Sin cambios a código, documentos históricos ni repositorio.

## Nota (no es decisión) — 2026-11-22: paquete único D-1 a D-8
Se entregó `PAQUETE_DECISION_D1_D8.md` con recomendaciones **[P] no aprobadas**. Discrepancia señalada: D-5 registrada como resuelta (12:29) vs descrita como pendiente (12:30); se mantiene resuelta hasta confirmación (ítem Z-1). Nada nuevo registrado como decisión.

## Nota (no es decisión) — 2026-11-22 12:35
El propietario confirmó D-5 como resuelta (R3, conjunto (b), M-1); D5.a–d siguen abiertas y fuera del paquete. *[SUPERADO — D5.a–d: fuera del alcance vigente, no abiertas; ver la nota de corrección documental posterior.]* Se entregó `PAQUETE_DECISION_D4_D6_D7_D8.md` (11 decisiones, recomendaciones no aprobadas) que sustituye a `PAQUETE_DECISION_D1_D8.md`. Nada nuevo registrado como decisión.

## Nota (no es decisión) — 2026-11-22 12:43
Recibida la **regla permanente de cierre y publicación de evidencia** (aplica a cada tarea; publicación en `appalex47-lab/CCI-Evidence` previa verificación de existencia, `private=true` y permisos de escritura; si hay 403 → detenerse sin alternativas; informe A–E; detenerse tras cada cierre). Complementa y amplía el protocolo de las 12:39. No autoriza avanzar de fase. Verificación 12:43: la API de GitHub respondió 403 para CCI-Evidence → publicación **pendiente**.

## Nota (no es decisión nueva) — 2026-11-22 (corrección documental posterior a la revisión de ChatGPT)
El propietario confirmó como **definitiva**: D-5 resuelta; D5.a–d quedaron fuera del paquete vigente; no son pendientes, no se contabilizan como abiertas, no condicionan D-4 ni otras decisiones y no se vuelven a preguntar. Las «cinco cuestiones abiertas» registradas el 12:29 y la nota de las 12:35 («D5.a–d siguen abiertas») se **conservan como antecedente cronológico**; la clasificación vigente es la de esta nota. No se aprueba ninguna de ellas individualmente. D4.d se evalúa con D-1, D-2 y D-5.3; no está aprobada. *[SUPERADO — D4.d=A fue respondida y registrada; ver «Nota fechada: D4.d».]*

## D-4, D-6, D-7 y D-8 — RESUELTAS por el propietario el 2026-11-22 (11 decisiones; registro AUTORITATIVO)
**Origen:** el propietario confirmó expresamente la selección de la matriz `RONDA_UNICA_D4_D6_D7_D8_MATRIZ_CONSOLIDADA.md` (HEAD `cb653b2`); el encargo de registro se recibió en la conversación del 2026-11-22 a las 13:48. **Estas selecciones son decisiones del propietario, no recomendaciones de Claude.** La hora exacta de la confirmación original no consta en este expediente.
**Selección registrada:** D4.a = A · D4.b = A · D4.c = A · D4.d = A · D6.a = A · D6.b = A · D6.c = A0 · D7.a = A · D7.b = A · D7.c = C · D8 = A.
**Cómo leer cada ítem:** se reproduce literalmente el contenido de la alternativa elegida y su columna de consecuencias en la matriz (que fija qué se aprueba y qué no). Las celdas de la matriz no se rellenan; este registro es la fuente autoritativa y los demás documentos remiten a él.

### D4.a → A — Delimitación entre Adaptación, Copy, Variante de copy y Versión
- **Contenido aceptado:** **A.** Concepto distinto de los tres, separado por criterio: Variante = alternativa del mismo contenido; Versión = evolución temporal; Adaptación = derivado de un copy fuente **para un canal destino**. No se decide si una adaptación puede tener variantes o versiones.
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* el criterio distintivo. *No aprueba:* variantes/versiones propias de la Adaptación, cardinalidad, atributos, persistencia. Coherente con D-1.b y D-2.a. El criterio «canal destino» procede de B l.538/563 [D/I].
- **Dependencias declaradas en la matriz:** D-1.b, D-2

### D4.b → A — Vínculo posible entre Adaptación y Pieza creativa
- **Contenido aceptado:** **A.** Ninguna adaptación presupone una Pieza; el vínculo es **posible**, no presupuesto; su existencia y forma se tratan en P4.B.
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* que el vínculo puede existir. *No aprueba:* relación, obligatoriedad, dirección, cardinalidad ni auditabilidad (D-1.c). Cabe con canales visuales (Banners, Landing; B l.545–546 [D], que sean visuales: [I]).
- **Dependencias declaradas en la matriz:** D-1.c

### D4.c → A — Definición mínima de la entidad conceptual 13 (`ChannelAdaptation`)
- **Contenido aceptado:** **A.** Texto A: «**Adaptación de canal:** contenido derivado de un copy fuente y preparado para un canal destino, con identidad y trazabilidad propias; concepto distinto de Copy, Variante de copy y Versión de contenido. Puede relacionarse con una Pieza creativa cuando el canal sea visual.»
- Texto exacto aprobado: «**Adaptación de canal:** contenido derivado de un copy fuente y preparado para un canal destino, con identidad y trazabilidad propias; concepto distinto de Copy, Variante de copy y Versión de contenido. Puede relacionarse con una Pieza creativa cuando el canal sea visual.»
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* ese texto y solo ese. *No aprueba:* nada de lo listado como silencios.
- **Dependencias declaradas en la matriz:** D4.a = A y D4.b = A (con D4.b = B, C o D es incompatible)

### D4.d → A — ¿Puede la Adaptación ser objeto de aprobación humana?
- **Contenido aceptado:** **A.** Sí, aprobable bajo los mismos límites de D-5.3.
- Base de evaluación (según la matriz): D-1, D-2 y D-5.3 (aprobación humana de un contenido concreto, en las condiciones revisadas, para pasar a la Biblioteca; **no** certifica cumplimiento legal, comercial o de marca; **no** autoriza publicación ni distribución). **No depende de D5.c** ni lo reabre. Qué versión exacta se aprueba y cómo se relaciona con las versiones **no está determinado** y no se pregunta aquí.
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* que puede ser objeto de aprobación humana en esos términos. *No aprueba:* mecanismo, atributos, estados, relación con versiones, auditabilidad (D-1.c sigue: la adaptación no se audita). Consecuencia: puede llegar a la Biblioteca aprobada sin auditoría creativa propia, coherente con M-1 («no sustituye auditorías»).
- **Dependencias declaradas en la matriz:** D-1, D-2, D-5.3

### D6.a → A — Definición de una métrica frente a valor de una métrica
- **Contenido aceptado:** **A.** Sí: definición = qué es el indicador y cómo se documenta; valor = lo que toma en un caso.
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* la distinción conceptual. *No aprueba:* atributos, fórmulas, catálogo. Da lugar a la «fórmula documentada» (B l.651) y al «valor» manual/importado/calculado (B l.649).
- **Dependencias declaradas en la matriz:** P4.1 (sin dependencia de otras decisiones)

### D6.b → A — Significado conceptual de «valor calculado»
- **Contenido aceptado:** **A.** Un valor de métrica **cuyo origen es un cálculo** (frente a manual o importado, B l.649); distinción de origen, no un concepto separado.
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* esa lectura. *No aprueba:* mecanismo de cálculo, persistencia ni indicadores.
- **Dependencias declaradas en la matriz:** D6.a = A o B (debe existir el concepto de valor); incompatible con D6.a = C

### D6.c → A0 — Ubicación conceptual de `Metric` (entidad 17) y de sus valores
- **Contenido aceptado:** **A0.** `Metric` = **definición de una métrica**; los **valores** pertenecen al **Resultado** (entidad 16). No se decide todavía: (i) la clasificación del origen de los valores (manual, importado o calculado), que puede quedar pendiente; (ii) si el valor calculado se conserva en el Resultado (L2) o se deriva al mostrarse sin conservarse (L1); y, de manera independiente, (iii) si el Resultado referencia la definición de la métrica que originó el cálculo (L3). A0 no presupone ni aprueba D6.b = A.
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* solo la asignación conceptual (Metric = definición; los valores pertenecen al Resultado). *Pendiente:* clasificación del origen de los valores (D6.b), L1/L2, L3, relación Métrica–Resultado, cardinalidad, atributos, fórmulas, catálogo, persistencia. *Se gana:* frontera clara sin comprometer almacenamiento; P4.1 intacta. *Se pierde:* nada queda cerrado sobre cómo se guarda el calculado.
- **Dependencias declaradas en la matriz:** D6.a = A; D6.b: cualquier respuesta, incluida C (diferir); no presupone D6.b = A

### D7.a → A — Perfil local frente a Configuración
- **Contenido aceptado:** **A.** Por naturaleza: Perfil local = datos de la persona usuaria local (hoy solo el nombre visible opcional, P1); Configuración = preferencias de la aplicación. Conceptos separados.
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* el criterio de distinción. *No aprueba:* contenido de Configuración, más datos de Perfil, ni Local Storage vs IndexedDB. Conserva tu decisión de mantener Perfil local como concepto propio.
- **Dependencias declaradas en la matriz:** P1, P4.3

### D7.b → A — Ubicación conceptual de las tolerancias
- **Contenido aceptado:** **A.** Son **parámetros de la ReglaComercial** (D-3.b).
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* ubicación conceptual. *No aprueba:* valores, redondeo, interfaz de edición, almacenamiento ni atributos. Mantiene la tolerancia junto a la regla que la usa [I]. **Q-1 sigue abierta:** el valor y el redondeo los decides tú.
- **Dependencias declaradas en la matriz:** D-3.b, Q-1

### D7.c → C — Alcance de la lista de canales y formatos
- **Contenido aceptado:** **C.** Lista inicial (Ecommerce, App, WhatsApp, Email, Redes sociales, Banners, Landing pages) más «otros formatos aprobados» por el propietario; sin mecanismo de ampliación definido.
- Aclaración de la matriz sobre C: los canales B l.538–547 forman una lista inicial; «otros formatos aprobados» (B l.547) queda reconocido como posible ampliación. **El documento no define quién aprueba un formato nuevo, dónde se registra ni si se hace desde la aplicación.** Por eso, bajo C, **no se fija ningún mecanismo**: un canal o formato nuevo entraría solo mediante una **decisión expresa del propietario** (junto con sus reglas, materia de Q-2) y su alta quedaría registrada documentalmente; **no se aprueba ninguna pantalla de edición ni catálogo editable**.
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* el alcance (inicial + ampliable por aprobación del propietario). *No aprueba:* la lista definitiva, reglas de canal, administración, interfaz ni mecanismo. «Aprobados = por el propietario» es [I]. **Q-2 sigue abierta:** canales y reglas reales.
- **Dependencias declaradas en la matriz:** D-3.c, Q-2

### D8 → A — Nombre canónico de la entidad 16 (`PerformanceRecord`)
- **Contenido aceptado:** **A.** «Resultado de desempeño».
- **Alcance y límites (columna «Consecuencia» de la matriz):** *Aprueba:* el nombre. *No aprueba:* definición, atributos, métricas ni estructura. Coincide con la definición aprobada de Campaña y se distingue de «Métrica» (definición).
- **Dependencias declaradas en la matriz:** D6.c

### Efectos y límites del registro (sin inferencias adicionales)
- **Compatibilidad comprobada** (ver `CONTROL_DE_CAMBIOS_REGISTRO_D4_D6_D7_D8_2026-11-22.md`): sin contradicciones con D-1, D-2, D-3, D-5 (R3, conjunto (b), M-1), P1, P2, P3 ni P4.A.
- **D-5.2:** la Adaptación, que quedó «pendiente de D-4», es aprobable por D4.d = A bajo los límites de D-5.3 (no certifica cumplimiento legal, comercial ni de marca; no implica publicación ni distribución). No se reabre D-5; D5.a–d permanecen fuera del alcance vigente.
- **D6.c = A0:** `Metric` es la definición de la métrica y los valores pertenecen al Resultado de desempeño. **No se decide todavía** la clasificación del origen de los valores (manual, importado o calculado); ni si el valor calculado se conserva en el Resultado (L2) o se deriva al mostrarse sin conservarse (L1); ni, de forma independiente, si el Resultado referencia la definición de la métrica que originó el cálculo (L3). L3 es independiente de la elección entre L1 y L2. **A0 no presupone ni aprueba D6.b = A**; D6.b = A se registra como decisión separada (significado conceptual de «valor calculado») y no determina por sí misma la clasificación de origen que A0 deja pendiente.
- **Dependencias D-1 a D-8:** quedan resueltas en su alcance (8 de 8). Las subcuestiones que cada decisión declara expresamente no decididas siguen pendientes (P4.B, P4.C, Q-1, Q-2 y las de A0).
- **Entidades:** este registro no aprueba entidades, atributos, relaciones, cardinalidades, estados, persistencia, fórmulas, catálogo de métricas ni mecanismos técnicos. D4.c aprueba la definición mínima de la entidad 13 y D8 el nombre de la entidad 16 (sin definirla); el conteo formal de P4.A (8 de 18 presentadas una a una) **no se modifica** por este registro y no se determina aquí si D4.c lo eleva a 9. *[SUPERADO — ver «Aclaración documental» posterior: el conteo vigente es 9/18 (50 %) por D4.c=A; marca añadida en la ronda final 2026-11-22, sin alterar el texto original.]*
- **Siguen abiertas:** Q-1, Q-2, P4.B, P4.C, E1–E5, entidad 9 Hallazgo, entidades 10 a 18 (la 13 solo con la definición de D4.c y la 16 solo con el nombre de D8), contradicciones C-2 y C-3, aprobaciones 0.1–0.7, aceptación de Fase 0 y autorización de Fase 1. **Nada de esto se da por aceptado.**
- **No equivale a:** aceptación formal de Fase 0; aprobación de todas las entidades; resolución de P4.B, P4.C, E1–E5, Q-1 o Q-2; autorización de Fase 1 ni de implementar funcionalidades.

## Aclaración documental (no es decisión nueva) — 2026-11-22: efecto de D4.c=A sobre el conteo de P4.A
La revisión documental determinó que D4.c=A aprueba la definición mínima de la entidad 13 (Adaptación de canal); por tanto el conteo formal de P4.A pasa de 8/18 a **9/18 (50 %)**, con 9/18 pendientes (50 %). Esto **sustituye** la frase anterior de este registro que dejaba sin determinar si D4.c elevaba el conteo; el texto de las 11 decisiones no se modifica. Límites: solo definición mínima; sin atributos, relaciones, cardinalidades, estructura interna, persistencia o versionado, mecanismos de generación o adaptación, reglas de auditoría ni fase de implementación. Entidad 9 (Hallazgo) sigue suspendida.

## Nota fechada (superación de nota histórica; no es decisión nueva) — 2026-11-22: D4.d
La nota histórica de D-5.2 («Adaptación: su posible aprobación queda pendiente de D-4 y de una decisión posterior expresa») y cualquier texto anterior que presente la aprobación de Adaptación como no aprobada **quedan superados**: **D4.d fue respondida con A por el propietario** y está registrada en el bloque «D-4, D-6, D-7 y D-8». Su aprobación está **limitada por M-1 y D-5.3**; **no implica** aprobación de auditoría directa de Adaptación (D-1.c intacta), publicación, distribución ni cumplimiento legal, comercial o de marca. El estado de P4.A y de la entidad 13 se interpreta conforme a **D4.c=A** y a la regularización posterior (P4.A 9/18). No se reescribe la nota histórica ni el texto de las decisiones.

## Nota fechada (no es decisión nueva) — 2026-11-22: lectura cronológica del registro
Este registro es acumulativo. Encabezados anteriores como «P4.1 — Entidades originales: PENDIENTE» y «P4.4 — APLAZADO hasta resolver Q-7» describen el estado en su momento y están **superados** por los encabezados posteriores «P4.1 — … RESUELTA PARCIALMENTE (solo nombres)», «Q-7 — RESUELTA → (a)» y «Confirmaciones del propietario — 11:38» (P4.D: Q-7=(a) cierra P4.4). Entidad 1: la mención «presentada (pendiente)» de las confirmaciones de 11:38 está superada por «P4.A — Entidad 1: Campaña — RESUELTA». No se reescribe ninguna decisión.

## Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10) — RESUELTA por el propietario el 2026-11-22 15:56 (registro AUTORITATIVO)
**Origen:** el propietario recibió la propuesta `PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md` (copia literal; SHA-256 `8eb73476310cd98a01d8ec049ca1fd4c165758fc344fa8870b1ed532b7aa3999`), con la pregunta de si quería responder por bloques o publicarla solo como propuesta, y respondió **«Confirmo todo»** (2026-11-22 15:56, hora de Ciudad de México). Este registro toma esa respuesta como **ratificación expresa de los bloques B1–B10** tal como figuran en la propuesta. **Son decisiones del propietario; el texto literal de cada propuesta ratificada está en la copia indicada y prevalece ante cualquier resumen.**
**Cómo se registra (sin inferencias adicionales):**
- Los bloques B1–B9 se registran como decisiones por **su contenido**, no por letra de opción: A0-1 se registra como «no exigir clasificación del origen (manual/importado/calculado) en el modelo inicial», A0-2 como «diferir L1/L2», A0-3 como «sí»; Q-4 como «el MVP termina al concluir Fase 2»; P11 con la redacción por niveles de la propuesta (no es ninguna de las tres opciones (a)/(b)/(c) del registro de decisiones).
- Las **«Recomendaciones iniciales»** de la propuesta para P6, P8, Q-1, Q-2, Q-3, Q-5 y Q-6 **no son decisiones**: solo se ratifica el **aplazamiento** de esas cuestiones (B8). Siguen siendo recomendaciones [Rec. Claude].
- **B10 no emite aprobaciones:** se ratifica el contenido propuesto para 0.1–0.7 como base de revisión; la propuesta declara que ninguna aprobación formal se considera emitida por ella. Las aprobaciones 0.1–0.7, la aceptación de Fase 0 y la autorización de Fase 1 permanecen **PENDIENTES**.

### B1 — P4.A: definiciones mínimas de las entidades 9, 10, 11, 12, 14, 15, 16, 17 y 18
**Aprueba:** la existencia y la definición mínima de cada una (conteo formal P4.A: **18/18**, con las entidades 1–8 y 13 ya aprobadas). **NO aprueba, para ninguna:** atributos, relaciones, cardinalidades, estructura interna, estados, ciclo de vida, persistencia o versionado, mecanismos, reglas, fórmulas, catálogos, asignación de fase ni implementación. La entidad 9 deja de estar suspendida.
- **Entidad 9 — Hallazgo de auditoría.** Definición aprobada (literal de la propuesta ratificada): «Hallazgo de auditoría es una entidad propia de CCI que representa un problema u observación identificado durante una auditoría creativa y que puede explicarse, consultarse y seguirse hasta su resolución.» *Límites ratificados (no aprobado):* No constituye una auditoría independiente; No tiene necesariamente una puntuación propia; No se aprueban niveles de severidad, categorías ni estados; No se presupone que cada hallazgo tenga una regla identificada; No se convierte en una entidad de aprobación.
- **Entidad 10 — ReglaDeMarca.** Definición aprobada (literal de la propuesta ratificada): «ReglaDeMarca es una entidad propia de CCI que representa un criterio de marca aplicable al contenido creativo y que puede utilizarse como referencia durante su evaluación.» *Límites ratificados (no aprobado):* No se inventa un catálogo de reglas; No se incorporan automáticamente reglas de copy; No se definen pesos, prioridades, severidades ni mecanismos; Su contenido concreto deberá justificarse con información de marca aportada por el propietario.
- **Entidad 11 — ReglaComercial.** Definición aprobada (literal de la propuesta ratificada): «ReglaComercial es una entidad propia de CCI que representa un criterio comercial utilizado para evaluar información de ofertas y promociones.» *Límites ratificados (no aprobado):* Sus tolerancias son parámetros de la propia regla, conforme a D7.b; No se aprueban fórmulas ni valores de tolerancia; No se aprueba redondeo ni tratamiento de excepciones; Q-1 se resuelve antes de implementar Promotion Validator.
- **Entidad 12 — Canal.** Definición aprobada (literal de la propuesta ratificada): «Canal es una entidad propia de CCI que representa un medio o formato de comunicación para el que puede prepararse contenido y respecto del cual pueden considerarse reglas específicas de adaptación.» *Límites ratificados (no aprobado):* Se conserva la lista inicial aprobada por D7.c; Las reglas por canal son una dimensión del Canal, no entidades independientes; No se aprueba un catálogo editable ni un mecanismo automático de ampliación; Los canales adicionales requieren decisión expresa del propietario.
- **Entidad 14 — Versión de contenido.** Definición aprobada (literal de la propuesta ratificada): «Versión de contenido es una entidad propia de CCI que representa un estado fechado y trazable de un contenido a lo largo de su evolución o revisión.» *Límites ratificados (no aprobado):* Es distinta de Variante de copy; Copy, Pieza creativa y Adaptación pueden tener versiones, conforme a D1.d; Las variantes no tienen versiones propias por ahora, conforme a D2.b; No se aprueban todavía mecanismos de comparación, almacenamiento ni historial.
- **Entidad 15 — Aprobación.** Definición aprobada (literal de la propuesta ratificada): «Aprobación es una entidad propia de CCI que representa una decisión humana respecto de la conformidad de un contenido específico, en las condiciones en que fue revisado, para permitir su paso a Creative Library.» *Límites ratificados (no aprobado):* La aprobación es humana, nunca automática por IA; El usuario es único y local; no hay aprobadores simulados; No constituye certificación legal, comercial ni de marca; No implica publicación o distribución externa; No se confunde con los estados del contenido; La identificación técnica exacta de la versión aprobada deberá definirse en el diseño del módulo.
- **Entidad 16 — Resultado de desempeño.** Definición aprobada (literal de la propuesta ratificada): «Resultado de desempeño es una entidad propia de CCI que representa información de desempeño proporcionada o registrada por el usuario respecto de una campaña, contenido u otra referencia pertinente.» *Límites ratificados (no aprobado):* Se conserva el nombre aprobado por D8; Los valores de las métricas pertenecen al Resultado; No se aprueban fórmulas, indicadores, atributos ni métodos de importación; A0-1, A0-2 y A0-3 se resuelven por separado.
- **Entidad 17 — Métrica.** Definición aprobada (literal de la propuesta ratificada): «Métrica es una entidad propia de CCI que representa la definición conceptual de un indicador utilizado para describir o evaluar desempeño.» *Límites ratificados (no aprobado):* No almacena los valores de desempeño; No se aprueba un catálogo de métricas; No se aprueban fórmulas ni fuentes de datos; La relación de referencia con Resultado queda sujeta a A0-3.
- **Entidad 18 — Configuración de la aplicación.** Definición aprobada (literal de la propuesta ratificada): «Configuración de la aplicación es una entidad propia de CCI que representa preferencias y parámetros duraderos que determinan el comportamiento o la presentación de la aplicación.» *Límites ratificados (no aprobado):* Es distinta de Perfil local; No representa identidad ni autorización; No se aprueban todavía atributos ni ubicación definitiva de almacenamiento; Local Storage se reserva para preferencias ligeras; la información necesaria para respaldos deberá persistir en IndexedDB.

### B2 — P4.B: relaciones y cardinalidades
**Aprueba:** las dos relaciones con fundamento documental (Campaña puede ser referenciada por Brief y por Resultado de desempeño; «puede» no significa obligatoria) y las once relaciones propuestas, **una por una**: Copy–Variante de copy; Copy–Versión de contenido; Pieza creativa–Versión; Adaptación–Versión; Auditoría creativa–Copy; Auditoría creativa–Pieza; Auditoría creativa–Hallazgo; Aprobación–contenido revisado; Resultado–Métrica; Adaptación–Canal; Adaptación–Pieza (vínculo posible, no presupuesto). **NO aprueba** (no deben darse por aprobadas): Campaña–Oferta, Campaña–Pieza, Brief–Oferta, Brief–Producto, Reglas de copy–ReglaDeMarca, reglas por canal como entidades independientes, ni Evento de actividad con entidad específica salvo que la especificación del módulo lo justifique. **No se establecen cardinalidades obligatorias en esta fase;** se especificarán con los flujos de cada módulo.
### B3 — P4.C: atributos
**Aprueba:** diferir la definición completa de atributos a la especificación de cada módulo; antes de implementar una entidad solo podrán aprobarse los atributos indispensables para el alcance autorizado de esa fase, con necesidad funcional, fuente o justificación, tipo y formato, obligatoriedad, validación y comportamiento ante ausencia o valor desconocido. **No se aprueba** un esquema completo de 18 entidades en Fase 0.
### B4 — P4.E: convenciones transversales E1–E5 (definitivas, con las delimitaciones de la propuesta)
E1 fechas y zonas horarias (instantes técnicos ISO-8601 UTC con «Z»; fechas comerciales `YYYY-MM-DD`; hora local con zona IANA cuando la operación dependa de ella; no convertir fechas comerciales en instantes UTC si cambia su significado). E2 campo `revision` (no obligatorio en todas las entidades; solo cuando un caso de uso demuestre necesidad; política multi-pestaña en P12). E3 archivar y eliminar (operaciones distintas; archivar reversible y por defecto si hay historial dependiente; eliminar físicamente requiere confirmación explícita; no eliminar silenciosamente información referenciada por versiones, auditorías o aprobaciones). E4 valores desconocidos (`null`, campo ausente, `0` y «no aplicable» diferenciados; ningún cálculo interpreta `null` como cero). E5 hash de versiones (versiones inmutables como principio; SHA-256 sobre contenido canónico cuando corresponda; detecta modificaciones o corrupción; no garantiza autoría ni seguridad frente a quien pueda modificar datos y recalcular el hash).
### B5 — D6.c=A0: subdecisiones
**A0-1:** no exigir en el modelo inicial la clasificación del origen del valor (manual/importado/calculado); se añadirá cuando una funcionalidad concreta necesite distinguirlo. **A0-2:** diferir la elección entre L1 y L2 hasta que existan fórmulas y casos de uso reales; no conservar valores calculados sin una decisión de trazabilidad. **A0-3:** sí; el Resultado de desempeño podrá referenciar la definición de la Métrica cuando sea necesario identificar el origen de un valor calculado (independiente de L1/L2).
### B6 — Arquitectura técnica: P5, P9, P11, P12, P13, P14
**P5:** almacenar binarios en IndexedDB como `Blob` o equivalente (no Base64 en registros de texto), separando metadatos y contenido; validar tipo, tamaño y contenido real; consultar cuota cuando el navegador lo permita; advertir y permitir exportar; sin promesa de recuperación automática; límites de producto tras pruebas reales de navegador. **P9:** modo operativo `local`; DEMO solo para pruebas o demostraciones identificadas; el build de producción usa persistencia local real y nunca muestra datos DEMO como del usuario; se mantienen las guardas contra configurar DEMO como producción. **P11:** Chrome/Chromium estable como navegador primario con matriz E2E completa; Edge estable con compatibilidad esperada y validación específica antes de declararlo plenamente soportado; Firefox secundario sujeto a pruebas; Safari/WebKit mejor esfuerzo; ningún soporte completo sin pruebas reales, documentando versión, sistema operativo y resultados. **P12:** una pestaña de escritura y las demás en solo lectura, con aviso visible y recuperación del permiso; mecanismo de coordinación del navegador (evaluar Web Locks y canal entre pestañas); si no puede demostrarse quién tiene el bloqueo, fallar de forma conservadora; sin concurrencia optimista generalizada ni `revision` en todos los registros. **P13:** dependencias mínimas justificadas una por una (APIs nativas preferentes; sin dependencia de ejecución sin justificar necesidad, mantenimiento, licencia y riesgo; versión fijada y pruebas; guardas anti-Supabase/backend; `AppErrorCode` solo con errores reales); IndexedDB nativo salvo evaluación técnica que justifique un wrapper; **no autoriza instalar paquetes durante Fase 0.** **P14:** no realizar PoC ejecutable en Fase 0; IndexedDB se implementará y probará en Fase 1 con evidencia real de navegador.
### B7 — Q-4: definición del MVP
El MVP termina al concluir **Fase 2**: Fase 1 (fundamentos y Command Center: arquitectura local, persistencia real, navegación y sistema visual, Perfil local opcional, preferencias, actividad real, estado del almacenamiento, Command Center con información real y estados vacíos honestos, exportación/importación básica de respaldo si se aprueba dentro del alcance de persistencia) y Fase 2 (Copy Studio: campañas, brief, copy, variantes, editor, etiquetas y búsqueda, reglas deterministas iniciales, flujo de creación y conservación de contenido). **No forman parte del MVP:** auditoría creativa avanzada, Promotion Validator completo, auditoría visual avanzada, Workflow & Approvals completo, Performance Intelligence avanzado, integraciones de backend y colaboración multiusuario. La aceptación del MVP no significa producto completo. **Esto no autoriza ninguna fase.**
### B8 — Cuestiones cuyo aplazamiento se acepta (NO resueltas)
| Cuestión | Se resolverá |
|---|---|
| P6 formato final de exportación | antes de cerrar Fase 2 |
| P7 cifrado local | antes de Fase 5 (no se promete cifrado mientras no se implemente) |
| P8 estrategia de IA | antes de generación en Fase 2 |
| P10 hosting y origen | antes de publicación del producto |
| P15 licencia y pendientes históricos de publicación | antes de publicación externa |
| Q-1 redondeo y tolerancias comerciales | antes de Fase 4 |
| Q-2 reglas y límites por canal | antes de Fase 4 |
| Q-3 estados y transiciones de Workflow & Approvals | antes de Fase 5 |
| Q-5 criterios y ponderaciones de auditoría | antes de Fase 3 |
| Q-6 idioma y diccionario ortográfico | antes de Fase 2 |
### B9 — C-2 y C-3
Se mantienen **abiertas como limitaciones expresas**: no se declara aceptada la Fase 0 v3.3 anterior como línea base vigente sin evidencia primaria (C-2); no se infiere que D-04 aprobara claves técnicas de roles, y P1 descarta los roles operativos en el dominio browser-only (C-3). Los documentos anteriores se conservan íntegros y **no sustituyen** la arquitectura browser-only ni la aceptación de esta Fase 0. Solo podrán cerrarse por decisión expresa o evidencia primaria.
### B10 — Aprobaciones formales 0.1–0.7
Se ratifica el contenido propuesto para su revisión (0.1 diagnóstico; 0.2 arquitectura; 0.3 dominio; 0.4 persistencia; 0.5 IA inicial sin claves privadas; 0.6 MVP hasta el final de Fase 2; 0.7 roadmap Fases 1–5 con puertas de aceptación), con las condiciones de la propuesta. **Ninguna aprobación se emite por este registro: 0.1–0.7 siguen PENDIENTES (0/7).**
### Efectos y límites del registro (sin inferencias adicionales)
- **Resueltas por esta ratificación:** P4 completa (P4.A 18/18, P4.B, P4.C, P4.E), A0-1, A0-2, A0-3, P5, P9, P11, P12, P13, P14 y Q-4. **Aplazadas por decisión (no resueltas):** las diez de B8.
- **Siguen abiertas:** C-2 y C-3 (limitaciones expresas); aprobaciones 0.1–0.7; aceptación formal de Fase 0; autorización de Fase 1. **Nada de esto se da por aceptado ni autorizado.** La aceptación de Fase 0 no autoriza por sí misma la Fase 1, que requiere una autorización independiente con el contenido indicado en la propuesta (§19).
- **No equivale a:** autorización para implementar, instalar dependencias, modificar código o iniciar Fase 1; aprobación de atributos, cardinalidades, fórmulas ni catálogos; resolución de las cuestiones aplazadas.

**Nota cronológica posterior (15:56):** los encabezados anteriores que describen P4.A entidades 9–18, P4.B, P4.C, P4.E, A0, P5, P9, P11–P14 o Q-4 como pendientes describen el estado en su momento y quedan **superados** por la sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)». No se reescribe ninguna decisión anterior.

## Nota fechada (no es decisión nueva) — 2026-11-22: cuestiones residuales de D-3 y D-5 y pregunta R-1
Registro de las cuestiones que D-3 y D-5 declaran expresamente **no decididas**. **No son decisiones ni resoluciones; ninguna se resuelve por derivación.**
- **D-3 — cuestión residual:** la **ubicación conceptual de la familia de reglas de copy** (D-3.c la dejó «pendiente de P4.B»; la ratificación de P4.B (B2) no aprobó Reglas de copy–ReglaDeMarca ni fijó esa ubicación). No debe confundirse con: la existencia de la familia conceptual de reglas de copy (ya distinguida); ReglaDeMarca y ReglaComercial (separación decidida); las reglas por canal (dimensión del Canal, no entidad independiente aprobada); una ubicación técnica o estructura de datos (no aprobada).
- **D-5 — cinco cuestiones residuales** (texto de D-5.3, arriba): (1) si la aprobación requiere auditoría o validaciones previas; (2) qué sucede cuando se modifica un contenido aprobado; (3) cómo se relaciona la aprobación con las versiones; (4) la identidad exacta del contenido al que se aplica cada aprobación; (5) la relación entre aprobación y los estados documentados en el flujo.
- **D5.a–d:** permanecen **fuera del alcance vigente** (decisión definitiva del propietario, nota anterior): no son pendientes, no se cuentan como abiertas, no condicionan D-4 ni las aprobaciones 0.1–0.7 y no se vuelven a preguntar. Las cinco cuestiones residuales de arriba no los reabren.
- **Pregunta R-1 (respondida «sí» el 2026-11-22 20:14; ver la sección «Aprobaciones formales 0.1–0.7 y respuesta a R-1», al final; el texto de esta nota describe el estado previo a la respuesta):** ¿se aplazan estas **seis** cuestiones hasta la especificación del módulo correspondiente, sin alterar D-3 ni D-5? Una respuesta afirmativa se registrará como **aplazamiento aceptado**, nunca como resolución conceptual; no reabre D-5.1, D-5.2, D-5.3 ni D5.a–d, no modifica M-1 y no aprueba mecanismos de aprobación, auditoría, versionado ni estados. Texto completo: `PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md`.

## Aprobaciones formales 0.1–0.7 y respuesta a R-1 — RESUELTAS por el propietario el 2026-11-22 20:14 (registro AUTORITATIVO)
**Texto literal del propietario:** «Apruebo 0.1 a 0.7 según las recomendaciones del paquete (0.5 solo en cuanto a principios; P8 sigue sin resolver y ninguna integración queda aprobada). R-1 sí.»

**Lectura registrada (sin inferencias adicionales):** el propietario adopta como propias las recomendaciones del paquete `PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md` (las recomendaciones eran [Rec. Claude], no vinculantes; pasan a ser decisión solo por esta respuesta, con el alcance y las limitaciones que el paquete indica para cada ficha).
| Ficha | Estado | Alcance y límites de la aprobación (según el paquete) |
|---|---|---|
| 0.1 Diagnóstico | APROBADA | con las limitaciones indicadas en la ficha; no valida el diseño ni certifica que el código funcione |
| 0.2 Arquitectura | APROBADA | arquitectura browser-only/local/un usuario por navegador, según la ficha |
| 0.3 Dominio | APROBADA | con las exclusiones indicadas en la ficha: no se aprueban atributos, cardinalidades obligatorias, estados, ciclos de vida, persistencia, fórmulas, catálogos de métricas ni asignación de fase |
| 0.4 Persistencia | APROBADA | con las limitaciones indicadas en la ficha; no aprueba cifrado, hosting, formato final de exportación ni límites de producto |
| 0.5 IA inicial | APROBADA **solo en cuanto a principios** | **P8 sigue sin resolver** (aplazamiento aceptado, antes de generación en Fase 2); **ninguna integración, proveedor, clave ni llamada remota queda aprobada** |
| 0.6 MVP | APROBADA | el MVP termina al concluir la Fase 2; las columnas marcadas [P] siguen sin validar |
| 0.7 Roadmap | APROBADA | Fases 1–5 y criterios AC como puertas de aceptación; no autoriza ninguna fase |

**R-1 = «sí».** Se registra como **aplazamiento aceptado**, nunca como resolución: las **seis** cuestiones residuales (la ubicación conceptual de la familia de reglas de copy, de D-3, y las cinco de D-5: auditoría o validaciones previas; modificación de un contenido aprobado; relación con las versiones; identidad exacta del contenido aprobado; relación con los estados del flujo) se aplazan hasta la especificación del módulo correspondiente, sin modificar D-3 ni D-5. No reabre D-5.1, D-5.2, D-5.3, M-1 ni D5.a–d (fuera del alcance vigente, sin cambio); no aprueba mecanismos de aprobación, auditoría, versionado ni estados. **R-1 no se suma a las 20/30 resueltas ni a las 10/30 aplazadas:** son cuestiones residuales dentro de D-3 y D-5, que siguen resueltas en los términos ya registrados.

**Conteos tras esta respuesta:** aprobaciones 0.1–0.7 emitidas por el propietario: **7/7**. Decisiones conceptuales: 20/30 resueltas; 10/30 con aplazamiento aceptado (P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6); 0 abiertas. P4.A 18/18 (existencia y definición mínima). Sin cambio en el estado de los CR.

**Lo que esta respuesta NO hace:**
- **No acepta la Fase 0.** La aceptación formal («cerrar formalmente Fase 0») es un acto distinto y sigue **PENDIENTE**; requiere respuesta expresa del propietario.
- **No autoriza la Fase 1.** Es una autorización independiente, con el contenido indicado en la propuesta (§19), y sigue **PENDIENTE**.
- No resuelve P8 ni ningún otro aplazamiento; no aprueba integración de IA, proveedor, clave ni llamada remota.
- No cierra C-2 ni C-3 (siguen como limitaciones expresas, B9).
- No reabre D5.a–d ni ninguna decisión ratificada; no aprueba atributos, cardinalidades, fórmulas ni catálogos.
- No autoriza implementar, instalar dependencias, modificar código, modificar `docs/fase0` ni `main`, ni fusionar con la vista previa privada (el propietario ya indicó que no se fusiona).
- No acredita pruebas, build, E2E ni CI de la aplicación, ni acceso a `CCI-Evidence` (403 en este entorno).

**Nota cronológica posterior (20:14):** los textos anteriores de este registro que dicen «0.1–0.7 PENDIENTES (0/7)» (B10, «Efectos y límites» y la nota de R-1) describen el estado en su momento y quedan **superados** por esta sección en lo relativo a las aprobaciones 0.1–0.7 y a R-1; siguen vigentes en todo lo demás (aceptación de Fase 0 y autorización de Fase 1 pendientes). No se reescribe ninguna decisión anterior.
