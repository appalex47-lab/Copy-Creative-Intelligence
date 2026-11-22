# Matriz maestra de decisiones — resueltas y pendientes (2026-11-22)
**Subordinada a** `../entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las recomendaciones de Claude están marcadas **[Rec. Claude]** y **no son decisiones del propietario**. Esta matriz no registra decisiones nuevas.

## A. Decisiones RESUELTAS (vigentes)
| ID | Decisión | Selección registrada | Ubicación en el registro | Límite / nota |
|---|---|---|---|---|
| P1 | Identidad/organización/roles | (b) perfil local opcional; sin UserIdentity/Organization/Membership/roles | Sección P1 | No aprueba P4, 0.x, Fase 0/1 |
| P2 | Sustitución formal DEC-D2–D4 y «Fuente de verdad» (+ ampliación «Seguridad por diseño») | (a) | Secciones P2 y ampliación | ADR propuesto redactado, no publicado |
| P3 | Tratamiento de docs/fase0 y expedientes Supabase/SQL/RLS | (b) antecedentes históricos y referencia conceptual no vinculante, 7 condiciones | Sección P3 | No resuelve C-2/C-3 |
| P4.1 | Lista de referencia de entidades | Resuelta parcialmente: solo nombres de la lista de 18 (A l.348–365) | Sección P4.1 | No aprueba definiciones, relaciones, atributos ni fases |
| P4.2 | Reglas de marca y comerciales | (b) dos entidades independientes | Sección P4 | No fusionar en genérica |
| P4.3 | Entidades añadidas | Evento de actividad (entidad propuesta), Etiqueta, Perfil local aprobados; Colección no incorporada | Sección P4 y «Colección» | Fuera del conteo de 18 (ver CR-06); no autoriza implementación |
| P4.4 / P4.D / Q-7 | Campaña frente a F11-D5 | Q-7=(a); cierra P4.4 | Secciones Q-7 y confirmaciones 11:38 | Solo existencia; sin atributos ni cardinalidades |
| P4.5 | Convenciones transversales | Aprobación PRELIMINAR conservada (no definitiva) | Sección P4.5 | E1–E5 pendientes |
| P4.A e1–e8 | Definiciones mínimas entidades 1–8 | (b) definición mínima del propietario, una por una | Secciones P4.A | Ver matriz 03 |
| P4.A e13 (D4.c) | Definición mínima Adaptación de canal | A (texto literal en registro) | D4.c | Solo existencia y definición mínima |
| D-1 (a–e) | Qué es «contenido» | a=A, b=(ii), c=(a), d=(a) parcial, e=(a) provisional | Sección D-1 | Sin entidad 19; no se audita Adaptación |
| D-2 (a–c) | Variante frente a Versión | a=A separados, b=(ii), c=(a) | Sección D-2 | Variante sin historial de versiones por ahora |
| D-3 (a–d) | Familias de reglas | 4 familias; solo ReglaDeMarca y ReglaComercial son entidades; reglas por canal = dimensión del Canal; reglas de copy → ubicación pendiente de P4.B | Sección D-3 | No aprueba atributos ni relaciones |
| D-5 (1–3) | Aprobación | R3; conjunto (b); M-1 | Sección D-5 | D5.a–d fuera del alcance vigente |
| D4.a | Delimitación Adaptación/Copy/Variante/Versión | A | Bloque D-4/D-6/D-7/D-8 | — |
| D4.b | Vínculo Adaptación–Pieza | A | idem | No define relación ni cardinalidad |
| D4.c | Definición mínima entidad 13 | A | idem | Ver e13 |
| D4.d | ¿Adaptación aprobable por humano? | A | idem + nota fechada | Límites M-1 y D-5.3; sin auditoría directa, publicación ni certificación |
| D6.a | Métrica: definición frente a valor | A | idem | — |
| D6.b | Significado de «valor calculado» | A | idem | Independiente de A0 |
| D6.c | Ubicación de Metric y valores | A0 | idem | Pendientes: origen del valor, L1/L2, L3 |
| D7.a | Perfil local frente a Configuración | A | idem | — |
| D7.b | Ubicación de tolerancias | A (parámetros de ReglaComercial) | idem | Q-1 abierta |
| D7.c | Alcance de canales/formatos | C (lista inicial + otros aprobados por el propietario) | idem | Q-2 abierta; sin mecanismo de ampliación |
| D8 | Nombre canónico entidad 16 | A «Resultado de desempeño» | idem | Solo nombre |

Las 11 decisiones D4/D6/D7/D8 aparecen **una sola vez** como decisiones vigentes en el registro (bloque «D-4, D-6, D-7 y D-8»; verificado por búsqueda: 11 encabezados `### D…`). Las referencias a ellas en otros documentos son remisiones, no duplicados.

## B. Cuestiones PENDIENTES (todas requieren decisión expresa del propietario salvo indicación)
Formato por ítem: **Estado · Fuente · Dependencias · Evidencia · Aprobado / No aprobado · Opciones reales · [Rec. Claude] · Consecuencias · Riesgos · ¿Conjunta? · Dónde se registrará.** Los detalles de opciones y consecuencias están en `09_PAQUETE_CONSOLIDADO_DECISIONES_PENDIENTES.md` (no se duplican aquí); esta tabla da el mapa.

| ID | Cuestión | Estado | Fuente | Depende de | Paquete | Requiere decisión expresa | Se registra en |
|---|---|---|---|---|---|---|---|
| PE-09 | Entidad 9 Hallazgo de auditoría | Suspendida; sin aprobar | `FICHA_P4A_09_HALLAZGO.md`; `MATRIZ_CONSOLIDADA_18_ENTIDADES.md` fila 9 | D-1 (resuelta), D-3 (resuelta); frontera con 8 | PAQ-1 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| PE-10 | Entidad 10 ReglaDeMarca | No presentada | Matriz 18 fila 10 | D-3 (resuelta) | PAQ-1 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| PE-11 | Entidad 11 ReglaComercial | No presentada | Fila 11 | D-3, D7.b (resueltas); Q-1 | PAQ-1 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| PE-12 | Entidad 12 Canal | No presentada | Fila 12 | D-3, D7.c (resueltas); Q-2 | PAQ-1 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| PE-14 | Entidad 14 Versión de contenido | No presentada | Fila 14 | D-1, D-2 (resueltas) | PAQ-2 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| PE-15 | Entidad 15 Aprobación | No presentada | Fila 15 | D-5 (resuelta; M-1) | PAQ-2 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| PE-16 | Entidad 16 Resultado de desempeño (nombre fijado por D8) | No presentada (definición) | Fila 16 | D6.c=A0, D8 | PAQ-2 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| PE-17 | Entidad 17 Métrica (= definición, por A0) | No presentada (definición) | Fila 17 | D6.a–c | PAQ-2 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| PE-18 | Entidad 18 Configuración de la aplicación | No presentada | Fila 18 | D7.a | PAQ-2 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| A0-1 | Clasificación del origen del valor (manual/importado/calculado) | Sin decidir | D6.c=A0 | D6.b=A (independiente) | PAQ-2 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| A0-2 | L1 (derivar al mostrar) frente a L2 (conservar en Resultado) | Sin decidir; mutuamente excluyentes | D6.c=A0 | A0-1 | PAQ-2 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| A0-3 | L3 referencia a la definición de métrica que originó el cálculo | Sin decidir; independiente de L1/L2 | D6.c=A0 | — | PAQ-2 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P4.B | Relaciones y cardinalidades | Pendiente (con base solo Campaña–Brief y Campaña–Resultado; Campaña–Oferta/Pieza = propuesta) | `DECISIONES_P4_PENDIENTES.md`; confirmaciones 11:38 | PAQ-1, PAQ-2 (definiciones de entidades) | PAQ-3 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P4.C | Atributos por entidad | Pendiente; el propietario difirió a la especificación de cada módulo, salvo indispensables del MVP | idem | P4.B, Q-4 | PAQ-4 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P4.E | E1–E5 convenciones | Pendiente (E2 espera a P12) | idem | P12 | PAQ-4 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| Q-1 | Redondeo y tolerancias del descuento | Abierta | `13_REGISTRO_DECISIONES_PROPIETARIO.md` | D7.b | PAQ-5 | Sí (valores los aporta el propietario) | `REGISTRO_DECISIONES_RESUELTAS.md` |
| Q-2 | Canales aprobados y reglas por canal | Abierta | idem | D7.c, D-3.c | PAQ-5 | Sí (límites reales los aporta el propietario) | `REGISTRO_DECISIONES_RESUELTAS.md` |
| Q-3 | Estados del flujo Workflow & Approvals | Pendiente | idem | D-5, P1 | PAQ-5 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| Q-4 | Alcance del MVP | Pendiente | idem | P4 | PAQ-5 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| Q-5 | Criterios y ponderaciones de la puntuación de auditoría | Pendiente (antes de Fase 3) | idem | PE-09 | PAQ-5 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| Q-6 | Idioma(s) y diccionario ortográfico | Pendiente (antes de Fase 2) | idem | P13 | PAQ-5 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| C-2 | Estado de la Fase 0 v3.3 anterior (aceptada/no aceptada) | Abierta | `INDICE_ANTECEDENTES_HISTORICOS.md` §5 | P15 | PAQ-5 | Sí; no se resuelve por inferencia | `REGISTRO_DECISIONES_RESUELTAS.md` |
| C-3 | D-04 «APROBADA» (cinco roles) sin aprobación propia localizada | Abierta | idem | P1 (roles descartados) | PAQ-5 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P5 | Binarios en IndexedDB | Pendiente (indispensable para cerrar Fase 0) | `MATRIZ_DECISIONES_PROPIETARIO.md` | P6, P11 | PAQ-6 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P9 | Significado de «producción» en modo local | Pendiente (indispensable) | idem | P10 | PAQ-6 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P11 | Navegadores soportados | Pendiente (indispensable) | idem | — | PAQ-6 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P12 | Política multi-pestaña | Pendiente (indispensable) | idem | P11 | PAQ-6 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P13 | Política de dependencias y AppErrorCode | Pendiente (indispensable) | idem | P5, P6, P8 | PAQ-6 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P14 | PoC de IndexedDB en Fase 0 | Pendiente (el propio expediente la considera resuelta de hecho; requiere confirmación) | idem | — | PAQ-6 | Sí (confirmar) | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P6 | Formato de exportación | Pendiente (antes de Fase 2) | `13_REGISTRO…` | P13 | PAQ-7 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P7 | Cifrado local con frase de paso | Pendiente (antes de Fase 5) | idem | P6 | PAQ-7 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P8 | Alternativa de IA y política de claves | Pendiente (antes de Fase 2) | idem | P13 | PAQ-7 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P10 | Hosting y origen | Pendiente (antes de Fase 5) | idem | P9 | PAQ-7 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| P15 | Pendientes previos (licencia, historial, F11-D4/F5/G-1/F6, Fase 0 anterior) | Pendiente (antes de Fase 5) | idem | P2, P3, C-2 | PAQ-7 | Sí | `REGISTRO_DECISIONES_RESUELTAS.md` |
| AP-0.1…0.7 | Aprobaciones del expediente | Pendientes | `APROBACIONES_FASE0.md` | Resolución previa de PAQ-1…PAQ-6 | Posterior | Sí; **no se solicitan todavía** | `APROBACIONES_FASE0.md` |
| AP-FIN | Aceptación formal de Fase 0 | No aceptada | `APROBACIONES_FASE0.md` | 0.1–0.7 | Posterior | Sí; no es formalidad automática | `APROBACIONES_FASE0.md` |
| AP-F1 | Autorización de Fase 1 | No autorizada | idem | AP-FIN | Posterior | Sí; independiente de AP-FIN | `APROBACIONES_FASE0.md` |

**Fuera de alcance (no pendientes):** D5.a–d (decisión definitiva del propietario). **No son decisiones:** C-2 y C-3 son contradicciones históricas abiertas, listadas por ser cuestiones que el propietario debe resolver; se excluyen de las bases de cálculo de decisiones.

## B.2 Campos adicionales por ítem pendiente (complemento de la tabla B; ronda final)
| IDs | Aprobado / No aprobado | Opciones reales | Consecuencias / riesgos | Contradicciones relacionadas | ¿Conjunta? | Detalle (opciones, [Rec. Claude] separadas) |
|---|---|---|---|---|---|---|
| PE-09 … PE-12 | No aprobado (9 suspendida; 10–12 sin aprobación vigente) | (a) aprobar definición mínima propuesta; (b) con cambios; (c) mantener sin aprobar | Aprobar solo existencia y definición mínima (no atributos, relaciones, estructura, persistencia, mecanismos, reglas ni fase); riesgo: frontera 9↔8, reglas de marca sin lista (D-3) | CR-01/CR-03 | Sí (PAQ-1, una respuesta) | 09 §PAQ-1 |
| PE-14 … PE-18 | No aprobado | (a)/(b)/(c) como arriba; 15 y 17 con límites de D-5/M-1 y A0 | Idem; riesgo: duplicar 14 con Variante/Evento (D-2), 15 con estados (D-5.1), 16/17 con A0 | CR-16 (resuelta), CR-15 (resuelta) | Sí (PAQ-2) | 09 §PAQ-2 |
| A0-1, A0-2, A0-3 | No decidido (A0 deja abiertas las tres) | A0-1: clasificar / no clasificar aún / otra; A0-2: L1 o L2 (excluyentes) o diferir; A0-3: sí/no/diferir (independiente de L1/L2) | Sin decisión no puede cerrarse la relación Métrica–Resultado; D6.b=A no las resuelve | CR-16 (resuelta: independientes) | Sí (PAQ-2) | 09 §PAQ-2 |
| P4.B | No aprobado (solo existencia de Campaña por Q-7; vínculo posible Adaptación–Pieza por D4.b) | Aprobar relación por relación con su cardinalidad; no aprobar | Cardinalidades condicionan P4.C y modelo de datos; Campaña–Oferta/Pieza = propuestas | — | Parcial (por bloques) | 09 §PAQ-3 |
| P4.C, P4.E | No aprobado (P4.5 preliminar) | Atributos solo indispensables del MVP o diferir; E1–E5 una a una | E2 espera a P12; recomendaciones técnicas no son decisiones | — | Sí (PAQ-4) | 09 §PAQ-4 |
| Q-1 … Q-6 | No decididas | Datos o criterios que solo aporta el propietario (Q-1, Q-2, Q-5) u opciones del paquete | Bloquean fases posteriores, no la preparación documental | CR-12 (referencias no verificables) | Sí (PAQ-5) | 09 §PAQ-5 |
| C-2, C-3 | Abiertas (no resueltas por inferencia; P3 cond. 7) | Declarar estado de la Fase 0 v3.3 anterior; confirmar/descartar D-04 | La línea anterior declara «ACEPTADA» y puede inducir a error sin el índice de conciliación | CR-09, CR-17 | Sí (PAQ-5) | 09 §PAQ-5 |
| P5, P9, P11–P14 | No decididas (indispensables según el propio expediente) | Opciones por decisión en `MATRIZ_DECISIONES_PROPIETARIO.md` | Sin ellas no se pueden aprobar 0.2 y 0.4 | — | Sí (PAQ-6) | 09 §PAQ-6 |
| P6, P7, P8, P10, P15 | No decididas (antes de su fase) | Opciones en `13_REGISTRO_DECISIONES_PROPIETARIO.md` | No bloquean la preparación del cierre | CR-09 | Sí (PAQ-7) | 09 §PAQ-7 |
| AP-0.1…0.7, AP-FIN, AP-F1 | Pendientes / no aceptada / no autorizada | Aprobar, rechazar o con cambios, **una por una**; no se solicitan todavía | FIN y F1 son independientes | — | No | `APROBACIONES_FASE0.md` |

La recomendación de Claude de cada ítem está **separada** en `09_…` y marcada **[Rec. Claude]**; no es una decisión. Todos los ítems requieren decisión expresa del propietario y se registran en `REGISTRO_DECISIONES_RESUELTAS.md` (aprobaciones en `APROBACIONES_FASE0.md`).
