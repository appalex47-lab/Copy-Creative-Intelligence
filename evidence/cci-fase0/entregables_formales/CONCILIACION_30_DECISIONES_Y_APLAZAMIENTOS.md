# Conciliación de las 30 decisiones de nivel superior, de los 10 aplazamientos y de las 18 entidades
> Documento de verificación documental, **2026-11-22**. **No es una decisión del propietario ni aprueba nada.** Fuente autoritativa: `REGISTRO_DECISIONES_RESUELTAS.md`. Etiquetas: [S] estado; [Rec. Claude] no vinculante. Verificado con `../logs/verificacion_semantica_fase0.py` (salida en `../logs/verificacion_semantica_fase0_2026-11-22.txt`). Esta conciliación **no cambia** el alcance de ninguna decisión.

## 1. Universo y reglas de conteo
- **30 decisiones de nivel superior:** P1–P15 (15), Q-1–Q-7 (7) y D-1–D-8 (8). Las subdecisiones (D1.a–e, D2.a–c, D3.a–d, D4.a–d, D5.1–3, D6.a–c, D7.a–c, A0-1/2/3, E1–E5, B1–B10) **no se suman** al total.
- C-2 y C-3 **no son decisiones**: son limitaciones expresas abiertas.
- **Resuelta** ≠ **aplazada**: un aplazamiento aceptado no resuelve la cuestión.
- **Resultado:** 20/30 resueltas (66,7 %); 10/30 aplazadas por decisión (33,3 %); 0/30 abiertas sin decisión de aplazamiento; 0/30 pendientes de decisión del propietario como requisito de cierre documental. Este porcentaje describe solo decisiones; **no** es un avance global de Fase 0.

## 2. Tabla de las 30 decisiones
| ID | Tema | Estado | Evidencia de origen (registro) | Alcance exacto | Dependencias y consecuencias | Limitación vigente |
|---|---|---|---|---|---|---|
| P1 | Identidad, organización y roles | RESUELTA | sección P1 | perfil local opcional; sin UserIdentity, Organization, Membership ni roles | habilita arquitectura browser-only; C-3 | no aprueba P4 ni 0.x |
| P2 | Sustitución formal de DEC-D2–D4 y «Fuente de verdad» | RESUELTA | sección P2 y ampliación | (a) | ADR propuesto sin publicar | no es aprobación de Fase 0 |
| P3 | Tratamiento de `docs/fase0` | RESUELTA | sección P3 | antecedente histórico y referencia conceptual no vinculante | fundamenta 0.1 | no resuelve C-2/C-3 |
| P4 | Dominio (P4.A–P4.E) | RESUELTA (por ratificación B1–B4) | secciones P4.A, D4.c, B1–B4 | P4.A 18/18 solo existencia y definición mínima; P4.B 13 relaciones sin cardinalidades obligatorias; P4.C atributos diferidos a cada módulo; P4.E E1–E5 | fundamenta 0.3 | sin atributos, cardinalidades, estados, fórmulas ni catálogos |
| P5 | Binarios | RESUELTA | B6 | Blob en IndexedDB; metadatos separados; validación; cuota si el navegador lo permite | fundamenta 0.4 | sin límites de producto hasta pruebas reales |
| P6 | Formato final de exportación | APLAZADA | B8 | — | antes de cerrar Fase 2 | no resuelta |
| P7 | Cifrado local | APLAZADA | B8 | — | antes de Fase 5 | no se promete cifrado |
| P8 | Estrategia de IA | APLAZADA | B8 | — | antes de generación en Fase 2 | no resuelta; 0.5 no aprueba integración |
| P9 | Modo operativo | RESUELTA | B6 | modo `local`; DEMO solo para pruebas o demostraciones identificadas | fundamenta 0.2 y 0.4 | — |
| P10 | Hosting y origen | APLAZADA | B8 | — | antes de publicación del producto | no resuelta |
| P11 | Navegadores | RESUELTA | B6 | por niveles (Chrome/Chromium primario; Edge a validar; Firefox secundario; Safari mejor esfuerzo) | fundamenta 0.2 | ningún soporte completo sin pruebas reales |
| P12 | Pestañas múltiples | RESUELTA | B6 | una pestaña de escritura y las demás en solo lectura; fallar de forma conservadora | fundamenta 0.2 y 0.4 | mecanismo de coordinación por evaluar |
| P13 | Dependencias | RESUELTA | B6 | mínimas y justificadas una por una | fundamenta 0.2 | — |
| P14 | Prueba de concepto | RESUELTA | B6 | sin PoC ejecutable en Fase 0 | fundamenta 0.1 | — |
| P15 | Licencia y pendientes históricos de publicación | APLAZADA | B8 | — | antes de publicación externa | no resuelta |
| Q-1 | Redondeo y tolerancias comerciales | APLAZADA | B8 | — | antes de Fase 4 | no resuelta |
| Q-2 | Reglas y límites por canal | APLAZADA | B8 | — | antes de Fase 4 | no resuelta |
| Q-3 | Estados y transiciones de Workflow & Approvals | APLAZADA | B8 | — | antes de Fase 5 | no resuelta |
| Q-4 | Definición del MVP | RESUELTA | B7 | el MVP termina al concluir Fase 2 | fundamenta 0.6 | no autoriza ninguna fase |
| Q-5 | Criterios y ponderaciones de auditoría | APLAZADA | B8 | — | antes de Fase 3 | no resuelta |
| Q-6 | Idioma y diccionario ortográfico | APLAZADA | B8 | — | antes de Fase 2 | no resuelta |
| Q-7 | Campaña frente a F11-D5 | RESUELTA | sección Q-7 | (a); solo existencia | cierra P4.4/P4.D | sin atributos ni cardinalidades |
| D-1 | Qué objetos son «contenido» | RESUELTA | sección D-1 (2026-11-22 12:04) | D1.a–e según registro | Copy, Pieza y Adaptación pueden tener versiones (D1.d) | sin entidad 19; no se audita Adaptación |
| D-2 | Variante de copy frente a Versión | RESUELTA | sección D-2 (12:09) | D2.a–c | variantes sin versiones propias por ahora (D2.b) | — |
| D-3 | Familias de reglas | RESUELTA | sección D-3 (12:14) | 4 familias; solo ReglaDeMarca y ReglaComercial son entidades | reglas por canal = dimensión del Canal | ubicación de las reglas de copy: subcuestión residual (pregunta R-1) |
| D-4 | Adaptación de canal | RESUELTA | bloque D4.a–d (2026-11-22) | D4.a=A, D4.b=A, D4.c=A, D4.d=A | entidad 13 | sin auditoría directa, publicación ni certificación |
| D-5 | Aprobación | RESUELTA | sección D-5 (12:29) | R3; conjunto (b); M-1 | entidad 15 | D5.a–d fuera del alcance vigente; subcuestiones 1, 2, 3 y 5 sin decisión propia (R-1) |
| D-6 | Métricas y valores | RESUELTA | bloque D6.a–c; B5 | D6.a=A, D6.b=A, D6.c=A0; A0-1/2/3 por B5 | entidades 16 y 17 | sin fórmulas ni catálogo |
| D-7 | Perfil, tolerancias y canales | RESUELTA | bloque D7.a–c | D7.a=A, D7.b=A, D7.c=C | entidades 11, 12 y 18 | Q-1 y Q-2 aplazadas |
| D-8 | Nombre canónico de la entidad 16 | RESUELTA | bloque D8 | «Resultado de desempeño» (solo el nombre; su definición mínima llega en B1) | entidad 16 | — |

**Control:** 20 «RESUELTA» + 10 «APLAZADA» = 30. Coincide con la matriz maestra (`../auditoria_integral/02_MATRIZ_MAESTRA_DECISIONES.md`), con `13_REGISTRO_DECISIONES_PROPIETARIO.md` y con el control D1 del script semántico. **Contradicciones que exijan una decisión nueva: ninguna.** Hay una consulta residual (R-1) que no bloquea el cierre documental (véase el paquete).

## 3. Hoja de cada aplazamiento (cinco campos)
Ninguno de los diez está resuelto. Ninguna cifra, cuota, límite, tolerancia o ponderación se inventa aquí. «Riesgo» describe el efecto de dejarla abierta; no es una decisión.
| Aplazamiento | 1 Qué se aplaza | 2 Por qué no bloquea el cierre documental actual | 3 Cuándo debe resolverse | 4 Riesgo de dejarla abierta | 5 Decisión nueva necesaria antes de implementar |
|---|---|---|---|---|---|
| P6 | formato final de exportación | Fase 1 puede limitarse al respaldo básico si el propietario lo incluye (B7); el formato definitivo llega después | antes de cerrar Fase 2 | un formato provisional podría exigir migración | elegir y aprobar el formato final y su versionado |
| P7 | cifrado local | no se promete cifrado mientras no se implemente; no es requisito de Fase 1 | antes de Fase 5 | datos locales sin cifrar en el navegador | decidir si se cifra, qué alcance y su política de claves |
| P8 | estrategia de IA | Fase 1 no genera contenido con IA | antes de generación en Fase 2 | bloquear la generación en Fase 2 si no se resuelve a tiempo | decidir modo (reglas, flujo manual u otro) y proveedor, en su caso |
| P10 | hosting y origen | la app puede desarrollarse local sin decidir dónde se publica | antes de publicación del producto | el origen del sitio condiciona el aislamiento del almacenamiento del navegador | decidir hosting y origen |
| P15 | licencia y pendientes históricos de publicación | no se publica externamente en Fase 1 | antes de publicación externa | publicar sin licencia definida | decidir licencia y cerrar los pendientes de publicación |
| Q-1 | redondeo y tolerancias comerciales | Promotion Validator es de Fase 4 | antes de Fase 4 | validación de promociones sin criterio de tolerancia | fijar reglas de redondeo y tolerancias |
| Q-2 | reglas y límites por canal | la Adaptación de canal es de Fase 4 | antes de Fase 4 | adaptaciones sin límites por canal | fijar reglas y límites por canal |
| Q-3 | estados y transiciones de Workflow & Approvals | el flujo completo es de Fase 5 | antes de Fase 5 | flujo de aprobación sin estados definidos | aprobar estados y transiciones |
| Q-5 | criterios y ponderaciones de auditoría | la auditoría creativa es de Fase 3 | antes de Fase 3 | auditorías sin criterios comparables | aprobar criterios y ponderaciones |
| Q-6 | idioma y diccionario ortográfico | Fase 1 no incluye el editor | antes de Fase 2 | correcciones ortográficas inconsistentes en Copy Studio | decidir idioma(s) y diccionario |

## 4. Las 18 entidades, una por una (control automatizado E1–E5)
- **E1:** el registro contiene la definición literal de las 18 entidades (18/18). **E2:** las definiciones de las entidades 9–12 y 14–18 son idénticas al texto de la propuesta ratificada (9/9). **E3:** la tabla A del doc 03 reproduce las 18 definiciones del registro sin discrepancia (18/18). **E4:** la matriz consolidada muestra 18/18 con estado «Aprobada». **E5:** ninguna definición contiene vocabulario de atributos, cardinalidades u obligatoriedad (0 casos para revisión humana).
- Alcance exacto: **solo existencia y definición mínima**; no son modelos de datos completos ni autorizan implementar. Condicionadas o con límites: entidad 13 (solo la definición de D4.c y límites de D4.d), 16 (nombre por D8; definición por B1; A0), 17 (A0-3), 11 (Q-1), 12 (Q-2), 15 (identificación de la versión aprobada se define en el módulo).
- **Fuera del conteo de 18** y aprobadas antes: Evento de actividad (propuesta), Etiqueta, Perfil local; Colección no incorporada.
- Prueba negativa: al alterar una definición en una copia, el control E3 la detecta (`../logs/verificacion_semantica_fase0_prueba_mutacion_2026-11-22.txt`).

## 5. P4.B, P4.C, P4.E: revisión de alcance
- **P4.B:** 13 relaciones (2 documentadas + 11 una por una), verificado contra B2 (control R1). No aprobadas: Campaña–Oferta, Campaña–Pieza, Brief–Oferta, Brief–Producto, Reglas de copy–ReglaDeMarca, reglas por canal como entidades independientes, Evento de actividad con entidad específica. Sin cardinalidades obligatorias. Variante ≠ Versión (D2.b). Copy, Pieza y Adaptación son entidades separadas; la auditoría se limita a Copy y Pieza (no hay auditoría directa de Adaptación).
- **P4.C:** atributos diferidos a cada módulo; no hay esquema completo de 18 entidades aprobado.
- **P4.E:** E1–E5 conforme a B4; `revision` no es obligatorio (solo con un caso de uso que lo justifique); el hash SHA-256 no garantiza autoría ni seguridad.
- **Descripciones más amplias que lo ratificado:** corregidas en la regularización con nota fechada de alineación y el texto anterior conservado (docs 05, 06, 07, 14 y `CONVENCIONES_P4_5_CONDICIONES.md`). Barrido de los 31 documentos vigentes o de propuesta con 9 controles semánticos: 0 errores reales tras las correcciones.

## 6. Qué no verifica esta conciliación
Pruebas, build, E2E o CI de la aplicación; contenido técnico (Web Locks, cuotas de IndexedDB, navegadores); anexos A/B; `CCI-Evidence` (403). La verificación la realiza la misma sesión que redactó (sin reproducción independiente).
