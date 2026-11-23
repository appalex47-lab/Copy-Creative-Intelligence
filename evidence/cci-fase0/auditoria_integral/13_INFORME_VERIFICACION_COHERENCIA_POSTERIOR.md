# Informe de verificación final de coherencia posterior a la regularización de Fase 0 (2026-11-22)
**Versión:** 1.0 · **Fecha:** 2026-11-22 · **Estado:** informe de hechos; subordinado a `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` · **Base:** HEAD `580c51f3d0e2e54695a431352957f34f9418b067` (rama `evidence/cci-fase0-review`) · **Alcance:** verificación acotada de coherencia, **no** re-auditoría de los 166 documentos · **Este informe no acepta Fase 0, no autoriza Fase 1 y no es una autorización para continuar con el desarrollo de CCI.**
**Quién verificó qué:** todo lo que se afirma aquí lo ejecutó Claude con las herramientas de la sesión (lectura de diffs, `git`, scripts de `logs/verificacion_coherencia_posterior.py`). **Nada fue reproducido de forma independiente.** Lo no comprobado se marca «no verificado» (§13).

## 0. Resultado en una línea
Se hallaron **8 hallazgos editoriales** (anotaciones desactualizadas o referencias erróneas; F1–F8) y se corrigieron sin alterar ninguna decisión del propietario, ningún estado de CR ni el texto original de los archivos históricos. Siguen abiertos los puntos que solo el propietario puede resolver (§7, §17).

## 1. Commit inicial y final
| Dato | Valor |
|---|---|
| Commit inicial (HEAD de la rama al empezar) | `580c51f3d0e2e54695a431352957f34f9418b067` (verificado por API y por `git rev-parse` del clon: remoto sin cambios ajenos) |
| Commit final | **Se informa en la entrega y se comprueba por API**: el hash de un commit no puede constar dentro de los archivos que contiene |
| `main` | `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`, sin cambios; sin PR abiertos |

## 2. Estado de la rama y comparación con `main`
- Antes de publicar: la rama estaba en `580c51f` (publicada, sincronizada). Cambios locales de esta ronda: **solo** rutas bajo `evidence/cci-fase0/` (0 rutas fuera; comprobado con `git diff --name-only` y archivos sin seguimiento).
- Respecto de `main`: `docs/fase0/` idéntico (huella `git ls-tree` 5be2c1e469d5bf49); sin diferencias fuera de `evidence/` salvo lo ya publicado en rondas previas (`README.md` raíz sin modificar). La comparación `main…rama` posterior a la publicación se informa en la entrega (por API).

## 3. Archivos revisados
Archivos modificados o creados desde el inicio de la regularización (`004a736^` → árbol de trabajo): **57** (39 modificados, 18 creados), más **3 archivos nuevos de esta ronda** (este informe y los dos de `logs/verificacion_coherencia_posterior*`) = **60** archivos tocados. De los 57: 54 son aplicables; 3 no (`MANIFEST.sha256` e `INVENTARIO_PUBLICADO.sha256`, regenerados por script, y `12_` por autorreferencia). Hunks de diff (línea de cambio contigua) en los 54 aplicables: **81**.
| Archivo | Est. | Líneas +/− | Hunks | Registro de lectura original (`12_` §3) | Verificación de esta ronda |
|---|---|---|---|---|---|
| `00_DICTAMEN_Y_CIERRE_FASE0.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `00_INDICE_VIGENTES_E_HISTORICOS.md` | M | +18/−1 | 3 | leído completo; editado después de la lectura | diff vs `004a736^` re-leído con contexto; editado además tras su lectura |
| `01_INFORME_AUDITORIA.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `02_INVENTARIO_FUNCIONALIDADES.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `03_CONCILIACION_DOCUMENTAL.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `04_MATRIZ_REQUISITOS.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `08_RESPALDO_Y_RECUPERACION.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `09_ANALISIS_IA.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `10_REGISTRO_DECISIONES.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `11_ROADMAP_Y_CRITERIOS_FASES_1_A_5.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `12_ESTRATEGIA_DE_PRUEBAS.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `13_VERIFICACION_EJECUTADA.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `14_ESTADO_GIT_Y_OPERACIONES.md` | M | +3/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `INFORME_REVISION_COMPLEMENTARIA.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `INVENTARIO_PUBLICADO.sha256` | M | +53/−35 | 13 | n/a (lista de hashes o autorreferencia) | diff vs `004a736^` re-leído con contexto |
| `MANIFEST.sha256` | M | +52/−34 | 13 | n/a (lista de hashes o autorreferencia) | diff vs `004a736^` re-leído con contexto |
| `README_ENTREGA.md` | M | +14/−3 | 3 | leído completo; editado después de la lectura | diff vs `004a736^` re-leído con contexto; editado además tras su lectura |
| `auditoria_integral/01_INDICE_MAESTRO_FASE0.md` | A | +55/−0 | 1 | leído completo; editado después de la lectura | creado tras 004a736; cambios posteriores (diff) re-leídos con contexto |
| `auditoria_integral/02_MATRIZ_MAESTRA_DECISIONES.md` | A | +94/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |
| `auditoria_integral/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md` | A | +46/−0 | 1 | leído completo; editado después de la lectura | creado tras 004a736; cambios posteriores (diff) re-leídos con contexto |
| `auditoria_integral/04_MATRIZ_MAESTRA_DEPENDENCIAS.md` | A | +36/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |
| `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md` | A | +176/−0 | 1 | leído completo; editado después de la lectura | creado tras 004a736; cambios posteriores (diff) re-leídos con contexto |
| `auditoria_integral/06_REGISTRO_CONTRADICCIONES.md` | A | +262/−0 | 1 | leído completo; editado después de la lectura | creado tras 004a736; cambios posteriores (diff) re-leídos con contexto |
| `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | A | +112/−0 | 1 | leído completo; editado después de la lectura | creado tras 004a736; cambios posteriores (diff) re-leídos con contexto |
| `auditoria_integral/08_INFORME_INTEGRIDAD_ARCHIVOS.md` | A | +43/−0 | 1 | leído completo; editado después de la lectura | creado tras 004a736; cambios posteriores (diff) re-leídos con contexto |
| `auditoria_integral/09_PAQUETE_CONSOLIDADO_DECISIONES_PENDIENTES.md` | A | +74/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |
| `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md` | A | +40/−0 | 1 | leído completo; editado después de la lectura | creado tras 004a736; cambios posteriores (diff) re-leídos con contexto |
| `auditoria_integral/11_INDICE_CONCILIACION_DOCS_FASE0.md` | A | +79/−0 | 1 | leído completo; editado después de la lectura | creado tras 004a736; cambios posteriores (diff) re-leídos con contexto |
| `auditoria_integral/12_REGISTRO_LECTURA_Y_LIMITACIONES.md` | A | +244/−0 | 1 | n/a (lista de hashes o autorreferencia) | autorreferencia; solo diff de la ronda |
| `entregables_formales/13_REGISTRO_DECISIONES_PROPIETARIO.md` | M | +1/−1 | 1 | leído completo; editado después de la lectura | diff vs `004a736^` re-leído con contexto; editado además tras su lectura |
| `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md` | M | +23/−15 | 4 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/APROBACIONES_FASE0.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/CATALOGO_DEPENDENCIAS_D4_D8.md` | M | +10/−7 | 4 | leído completo; editado después de la lectura | diff vs `004a736^` re-leído con contexto; editado además tras su lectura |
| `entregables_formales/CONTROL_DE_CAMBIOS_CORRECCION_INTEGRAL_P4A_9_18_2026-11-22.md` | A | +30/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |
| `entregables_formales/CONTROL_DE_CAMBIOS_REGISTRO_D4_D6_D7_D8_2026-11-22.md` | A | +27/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |
| `entregables_formales/CONTROL_DE_CAMBIOS_REGULARIZACION_P4A_9_18_2026-11-22.md` | A | +27/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |
| `entregables_formales/CONVENCIONES_P4_5_CONDICIONES.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/D3_FAMILIAS_DE_REGLAS.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/D5_APROBACION.md` | M | +1/−0 | 1 | leído completo; editado después de la lectura | diff vs `004a736^` re-leído con contexto; editado además tras su lectura |
| `entregables_formales/DECISIONES_P4_PENDIENTES.md` | M | +20/−6 | 7 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/FICHA_P4.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/INFORME_CIERRE_2026-11-22_CORRECCION_DOCUMENTAL.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/INFORME_CIERRE_2026-11-22_REGISTRO_D4_D6_D7_D8.md` | A | +10/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |
| `entregables_formales/INFORME_CIERRE_2026-11-22_REGLA_PERMANENTE_12_43.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/LISTA_ORIGINAL_18_ENTIDADES.md` | M | +1/−1 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` | M | +1/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` | M | +12/−8 | 7 | leído completo; editado después de la lectura | diff vs `004a736^` re-leído con contexto; editado además tras su lectura |
| `entregables_formales/MATRIZ_DECISIONES_PROPIETARIO.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/PAQUETE_DECISION_D1_D8.md` | M | +1/−1 | 1 | leído completo; editado después de la lectura | diff vs `004a736^` re-leído con contexto; editado además tras su lectura |
| `entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md` | M | +3/−0 | 2 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/README_PROPUESTA_VIGENTE.md` | M | +2/−0 | 1 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` | M | +83/−2 | 2 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `entregables_formales/RONDA_UNICA_D4_D6_D7_D8_MATRIZ_CONSOLIDADA.md` | M | +8/−1 | 4 | leído completo en su estado actual | diff vs `004a736^` re-leído con contexto |
| `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt` | A | +113/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |
| `logs/scan_contradicciones.py` | A | +14/−0 | 1 | leído completo en su estado actual | creado tras 004a736; no editado desde su lectura completa |

## 4. Secciones modificadas re-leídas
- Se re-leyeron **los 81 hunks** de los 54 archivos aplicables con su contexto inmediato (párrafo o fila de tabla), comparando con el registro de lectura original (`12_` §3 y §7). Los archivos creados (A) ya se habían leído completos en la ronda de lectura; en los editados después de su lectura, `12_` §7 lista bytes leídos y bytes actuales.
- Comparación de los archivos restaurados (`00_INDICE_VIGENTES_E_HISTORICOS.md`, `README_ENTREGA.md`) con su versión original `1bb831a`: **0 líneas originales ausentes, mismo orden** (re-comprobado). La única reducción de tamaño >10 % en todo el historial de `evidence/cci-fase0` son los dos archivos truncados por `1cf96e3` (CR-21), ya restaurados en `580c51f` (`logs/…2026-11-22.txt`, V3).
- Se comprobó que ningún archivo histórico perdió contenido: las supresiones del diff son reescrituras con antecedente marcado (no borrados).

## 5. Hallazgos y 6. Correcciones
| Id | Archivo | Hallazgo | Corrección (el texto original se conserva y se marca) |
|---|---|---|---|
| F1 | `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` | Fila 13 había perdido el paréntesis literal; «delimitación pendiente en P4.B» contradecía D4.a=A; anotación de Perfil local imprecisa | Paréntesis restituido; «D4.a=A fijó el criterio de delimitación; relaciones y cardinalidades siguen sin aprobar (P4.B)»; Perfil local: existencia aprobada en P4.3 y D7.a=A solo fija el criterio de distinción |
| F2 | `auditoria_integral/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md` | «(ver CR-06)» era referencia errónea; fila Perfil local con alcance no declarado | «(ver CR-15)»; D7.a=A fija solo el criterio de distinción (no amplía el contenido) |
| F3 | `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | §4 no reflejaba que CR-15 y CR-16 ya estaban resueltos | Nota añadida (ver `06_` v3.0 y R5); sección R8 |
| F4 | `auditoria_integral/06_REGISTRO_CONTRADICCIONES.md` | Observación de la lectura apuntaba a secciones inexactas; «9 fases» (CR-22) debía decir «Fases 0–9»; el barrido de CR-21 citaba «167 archivos» | Corregidos; barrido referido al historial git de `evidence/cci-fase0` (todos los commits; no hay otra reducción >10 %). **Estados de CR intactos** |
| F5 | `entregables_formales/13_REGISTRO_DECISIONES_PROPIETARIO.md` | Frase «Ninguna se responde por el propietario» sin nota de estado posterior | Nota en línea: P1–P3 resueltas, P4 parcial, Q-7 resuelta |
| F6 | `entregables_formales/CATALOGO_DEPENDENCIAS_D4_D8.md` | Línea 95: «D-6, D-7 y D-8 permanecen pendientes» sin marca | «[superado: …]» |
| F7 | `entregables_formales/PAQUETE_DECISION_D1_D8.md` | Línea 62: D4.d «pendiente por D-5.2» sin marca | «[superado: …]» |
| F8 | `entregables_formales/D5_APROBACION.md` | Texto de análisis con D-4/D-6/D-7/D-8 «pendientes» sin nota de la ronda | Blockquote «Nota de la ronda de coherencia (el texto original no se altera)» |
**Correcciones de presentación propias (documentación de esta ronda):** cifras de 110 archivos/108–109 líneas de manifiesto/170 blobs en `05_`, `08_`, `10_`; la métrica «55/55 avisos de vigencia» de `05_`/`10_` no era reproducible tal como estaba redactada: ahora indica su base real (58 archivos en esas clases; 55 aplicables con marca; 3 «n/a») y que es **detección a nivel de archivo**; `12_` v2.1 añade la aclaración «líneas únicas ≠ bytes revisados individualmente» y amplía la lista de archivos editados tras su lectura (de 8 a 15); `01_` incorpora los límites de D4.d (M-1 y D-5.3) y de D6.c=A0 en su fila de decisiones y la fila 13.

**Observaciones sin corrección (registradas):** (a) archivos con referencias a documentos del repositorio de la aplicación que no existen en la rama (104 menciones; todas del tipo CR-12: externas, ya declaradas); (b) 39 menciones de hashes de commit inexistentes en este repositorio: `ffb47bc…` y otros cuatro commits del expediente local no publicado de la aplicación (documentados en `14_ESTADO_GIT_Y_OPERACIONES.md`) y los prefijos de los adjuntos A y B; (c) `README_ENTREGA.md` restaurado conserva su «Orden de lectura» redundante (viene de `1bb831a`); (d) las filas 1–8 de `MATRIZ_CONSOLIDADA_18_ENTIDADES.md` son resúmenes, no definiciones literales (la literal está en `03_` y en el registro); (e) 38 menciones de «Dx = valor» con valor distinto del decidido, todas dentro de opciones hipotéticas, tablas de compatibilidad o recomendaciones de paquetes ya respondidos (ninguna presenta otro valor como decisión).

## 7. Hallazgos todavía abiertos
- Ninguno de **coherencia documental corregible** queda abierto tras las correcciones F1–F8.
- Abiertos por requerir al propietario (no se resuelven por inferencia): P4.B, P4.C, P4.E (E1–E5), Q-1…Q-6, C-2, C-3 (CR-17), entidad 9 (suspendida), entidades 10–12 y 14–18, las preguntas A0 sin decidir (D6.c=A0), P5…P15, aprobaciones formales 0.1–0.7, contenido definitivo de las fases, aceptación de Fase 0 y autorización de Fase 1. CR-12 permanece «no resoluble por falta de evidencia» (archivos que no están en la rama).

## 8. Estado final CR-01…CR-22 (`06_` v3.0)
Distribución: 13 RESUELTA_DOCUMENTALMENTE · 5 HISTORICA_CON_ADVERTENCIA (CR-09, 10, 13, 14, 20) · 2 RESUELTA_POR_DECISION_PROPIETARIO (CR-07, CR-16) · 1 PENDIENTE_PROPIETARIO (CR-17) · 1 NO_RESOLUBLE_POR_FALTA_DE_EVIDENCIA (CR-12). Estados de CR-01…CR-18 **iguales** a los de `13b25ca` (comprobado por script, X2). Ningún estado se modificó en esta ronda.
| CR | Contradicción | Estado |
|---|---|---|
| CR-01 | Conteo de P4.A «8/18» presentado como vigente frente a 9/18 | RESUELTA_DOCUMENTALMENTE |
| CR-02 | Entidad 13 «No presentada» frente a aprobada (D4.c=A) | RESUELTA_DOCUMENTALMENTE |
| CR-03 | Entidad 9: «pendiente de decisión» frente a suspendida | RESUELTA_DOCUMENTALMENTE |
| CR-04 | Q-7/P4.D «pendiente» y P4.4 «aplazado» frente a resueltas/cerrada | RESUELTA_DOCUMENTALMENTE |
| CR-05 | D-1, D-2, D-3 y D-5 «pendiente de decisión» en el índice 16 | RESUELTA_DOCUMENTALMENTE |
| CR-06 | D4/D6/D7/D8 «pendientes» en documentos de apoyo | RESUELTA_DOCUMENTALMENTE |
| CR-07 | D4.d aprobada frente a «Adaptación pendiente de D-4» / «D4.d no aprobada» | RESUELTA_POR_DECISION_PROPIETARIO |
| CR-08 | Fichas P4.A 01–08 «pendiente» en el índice 16 | RESUELTA_DOCUMENTALMENTE |
| CR-09 | `docs/fase0/` declara «Fase 0 v3.3 COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL» y diseñ… | HISTORICA_CON_ADVERTENCIA |
| CR-10 | Referencias a Supabase/PostgreSQL/RLS/multiusuario dentro del expediente actual | HISTORICA_CON_ADVERTENCIA |
| CR-11 | Fórmulas de «Pre-condición: Fase 0 aceptada y Fase 1 autorizada» en roadmap y criterios | RESUELTA_DOCUMENTALMENTE |
| CR-12 | Referencias a archivos que no existen en la rama (documentos de la aplicación, adjuntos A y … | NO_RESOLUBLE_POR_FALTA_DE_EVIDENCIA |
| CR-13 | Copias previas de la raíz (00–14) frente a `entregables_formales/` (01–16) con numeración di… | HISTORICA_CON_ADVERTENCIA |
| CR-14 | `MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` con 7 hashes que ya no coinciden | HISTORICA_CON_ADVERTENCIA |
| CR-15 | Numeración «19» y Evento de actividad: D-1.a «no añade una entidad 19» frente a P4.3 (Evento… | RESUELTA_DOCUMENTALMENTE |
| CR-16 | «Tensión» D6.b=A frente a D6.c=A0 | RESUELTA_POR_DECISION_PROPIETARIO |
| CR-17 | C-2 (estado de la Fase 0 v3.3 anterior) y C-3 (D-04 «APROBADA», cinco roles) | PENDIENTE_PROPIETARIO |
| CR-18 | Conteos de clasificación: «93/93 archivos clasificados» frente a 104 archivos reales; 99 fil… | RESUELTA_DOCUMENTALMENTE |
| CR-19 | `README_PROPUESTA_VIGENTE.md`: fila «Pendiente: P1–P15, Q-1…Q-6» frente a decisiones ya emit… | RESUELTA_DOCUMENTALMENTE |
| CR-20 | Copias previas de la raíz sin aviso de vigencia (`03_CONCILIACION_DOCUMENTAL.md`, `10_REGIST… | HISTORICA_CON_ADVERTENCIA |
| CR-21 | Regresión propia: `00_INDICE_VIGENTES_E_HISTORICOS.md` y `README_ENTREGA.md` truncados en el… | RESUELTA_DOCUMENTALMENTE |
| CR-22 | Roadmap del anexo original (Fases 0–5 con Persistencia, Capacidades, IA y Endurecimiento) fr… | RESUELTA_DOCUMENTALMENTE |
- CR-07 y CR-16 se apoyan en decisiones realmente emitidas (D4.d=A, limitada por M-1 y D-5.3; D6.b=A con D6.c=A0). CR-22 sigue siendo registro de versiones de roadmap: `11_ROADMAP_FASES_0_A_5.md` es **propuesta no aprobada**, no una decisión del propietario. CR-21: restauración verificada (§4).

## 9. Coherencia de D4, D6, D7, D8 y Q-7
Valores vigentes en el registro: **D4.a=A, D4.b=A, D4.c=A, D4.d=A** (limitada por M-1 y D-5.3), **D6.a=A, D6.b=A, D6.c=A0**, **D7.a=A, D7.b=A, D7.c=C**, **D8=A**, **Q-7=(a)**.
- 332 menciones «Dx = valor» coinciden con el registro; 38 con otro valor son hipotéticas/condicionales (§6 e). Ninguna presenta D5.a–d como pendiente (23 menciones con marca de fuera de alcance; D5.a–d no se reabre).
- D6.c=A0 se mantiene como asignación conceptual (Métrica = definición; los valores pertenecen al Resultado de desempeño): **no** se convirtió en aprobación de la clasificación de origen (manual/importado/calculado), de L1/L2, de L3 ni de estructuras técnicas.
- D4.d=A (13 menciones sin M-1/D-5.3 a ±contexto: todas son listas de las 11 selecciones, notas o hipótesis; el bloque del registro declara los límites). Ninguna decisión conceptual se presenta como autorización de implementación (0 afirmaciones de Fase 1 autorizada).
- Fuente consultada: registro (sección D-4/D-6/D-7/D-8) y el resto del expediente por escaneo de ocurrencias (`logs/…`, V4/V6/V10).

## 10. Estado de las 18 entidades (P4.A)
| Estado | Entidades |
|---|---|
| Aprobadas, **solo definición mínima** (9/18) | 1 Campaña, 2 Brief, 3 Producto, 4 Oferta, 5 Copy, 6 Variante de copy, 7 Pieza creativa, 8 Auditoría creativa, 13 Adaptación de canal (literal = D4.c=A) |
| Suspendida, sin aprobar | 9 Hallazgo de auditoría |
| Sin aprobación vigente (8) | 10 Regla de marca, 11 Regla comercial, 12 Canal, 14 Versión de contenido, 15 Aprobación, 16 Resultado de desempeño (nombre fijado por D8=A, sin definición), 17 Métrica (ubicación conceptual por D6.c=A0), 18 Configuración de la aplicación |
- No se añadieron atributos, relaciones, cardinalidades, reglas ni fases; **no existe entidad 19** (Evento de actividad es una «entidad propuesta» fuera de la lista de 18, CR-15). D4.d (Adaptación aprobable) permanece limitada por M-1 y D-5.3. Perfil local: concepto propio (P4.3); D7.a=A solo fija el criterio de distinción frente a Configuración.

## 11. Arquitectura y vigencia
Vigente: navegador únicamente; un usuario por navegador; sin cuentas, login ni autenticación; sin backend/servidor; Supabase, PostgreSQL, SQL y RLS **no** son vigentes; IndexedDB como persistencia principal y Local Storage para preferencias ligeras; exportación/importación local; respaldo y recuperación **por diseñar**; sin sincronización multidispositivo, colaboración ni permisos multiusuario. Los 59 archivos de `docs/fase0/` (línea Supabase/RLS) permanecen como histórico con advertencia, no vinculantes (P3=b), idénticos a `main`. Comprobación: en los documentos vigentes y propuesta, las 10 líneas con términos de la arquitectura anterior sin negación inmediata se revisaron una a una (V7): describen lo que existe hoy en el código de la aplicación (p. ej. `UserIdentity`/`Membership` provisionales en `02_INVENTARIO_FUNCIONAL_CCI.md`), filas de «no incluido» o de lo que se sustituye (`08_RESPALDO_IMPORTACION_RECUPERACION.md`), preguntas históricas ya respondidas y títulos de decisiones resueltas (`13_REGISTRO_DECISIONES_PROPIETARIO.md`, registro), o descripciones de CR; ninguna es un requisito vigente; no se reescribió ninguna historia.
- Índices y referencias: 0 enlaces markdown rotos; las 104 rutas no resueltas son externas a la rama (CR-12); `05_` lista exactamente los 110 archivos del árbol (X8); `11_`: 59/59 archivos de `docs/fase0` con tamaño y SHA-256 correctos (X9).

## 12. Hashes, inventario y clon limpio
- Procedimiento (de `08_` v3.1): `MANIFEST.sha256` (**108** líneas, `sha256  ./ruta`; excluye ambos manifiestos), `INVENTARIO_PUBLICADO.sha256` (**109** líneas, `sha256  tamaño  ruta`; excluye a sí mismo), 110 archivos en `evidence/cci-fase0/`, 59 en `docs/fase0/` (fuera de los manifiestos; se contrastan con `main` y con `11_`), 170 blobs esperados en la rama (110 + 59 + 1 `README.md`).
- Los manifiestos se regeneran **al final**, sin ediciones posteriores. **El resultado de la verificación sobre el clon limpio del commit publicado y de la API se informa en la entrega**, porque no puede constar dentro de los archivos que se hashean.
- Local previo a la publicación (hechos de este informe): `docs/fase0` idéntico a `main`; 59/59 hashes y tamaños de `11_` correctos.

## 13. Limitaciones y verificaciones no realizadas
- **No se ejecutaron** pruebas, build, E2E ni CI de la aplicación; **no** se ejecutaron `modelo_estructural.py` ni `verificar_expediente.py`; los resultados de `logs/` previos son de ejecuciones anteriores.
- `CCI-Evidence` devuelve 403: no se usó ni se rodeó. No se leyeron los adjuntos A y B del propietario ni los documentos del repositorio de la aplicación.
- `docs/fase0/` se leyó por **líneas únicas** (2 216 734 B de 10 324 392 B totales, 21,5 %): no equivale a que cada byte se haya revisado individualmente.
- La detección de marcas de vigencia es a nivel de archivo; los escaneos son por patrón y dependen de sus expresiones regulares; no sustituyen la lectura.
- Toda la verificación es propia; no hay reproducción independiente. No se verificó la arquitectura por revisión de código.

## 14. Confirmación: sin código ni `main`
No se modificó ningún archivo de código ni de la aplicación; no se tocó `main`, `docs/fase0`, ni la visibilidad del repositorio; no se borraron ramas ni se cambiaron decisiones del propietario. Rutas modificadas: solo `evidence/cci-fase0/`.

## 15. Confirmación: sin merge, PR ni deploy
No se realizó merge, no se abrió PR y no se hizo deploy. No se usaron subagentes.

## 16. Porcentajes separados (con base de cálculo; sin porcentaje global de Fase 0)
| Indicador | Resultado | Base de cálculo |
|---|---|---|
| Verificación posterior a las ediciones — archivos | **54/54 = 100 %** | archivos aplicables modificados o creados desde `004a736^` (57 − 2 manifiestos − `12_`); verificados = diff re-leído por mí |
| Verificación posterior a las ediciones — secciones | **81/81 = 100 %** | hunks de diff de esos 54 archivos |
| Coherencia documental (controles) | **34/40 = 85,0 % a la primera ejecución; 40/40 = 100 % tras corregir** | 40 controles ejecutados (CR 10, decisiones 7, entidades 5, arquitectura 3, índices/referencias 8, registro de lectura 4, aceptación/aprobaciones 3); fallaron al inicio 6 (A10, B7, C1, C2, F2, F3) y se corrigieron; no hay controles fallidos ni abiertos |
| Integridad (archivos y hashes correctos / total verificados) | **Se informa en la entrega** (verificación sobre el commit publicado: esperado 110/110 archivos encontrados, 109/109 inventario hash+tamaño, 108/108 `sha256sum -c`, 59/59 `docs/fase0` vs `11_`) | Clon limpio + API |
| Decisiones conceptuales (resueltas / identificadas) | **12/30 = 40,0 %** | P1–P15 (15) + Q-1…Q-7 (7) + D-1…D-8 (8); resueltas: P1, P2, P3, Q-7, D-1…D-8. Las 11 subdecisiones D4/D6/D7/D8 están resueltas dentro de D-4, D-6, D-7, D-8. Indicador orientativo: decisiones de peso muy distinto |
| Entidades (definiciones aprobadas / 18) | **9/18 = 50,0 %** | Registro (definición mínima solamente) |
| Aprobaciones formales | **0/7 = 0 %** | 0.1–0.7 (`APROBACIONES_FASE0.md`: todas PENDIENTE; «Fase 0 aceptada» y «Fase 1 autorizada» también PENDIENTE) |
| Estado de aceptación de Fase 0 | **No aceptada** (pendiente del propietario) | `APROBACIONES_FASE0.md` |
| Estado de autorización de Fase 1 | **No autorizada** | `APROBACIONES_FASE0.md` |
| Fase 0 global | **No calculable** | No hay ponderación objetiva aprobada |
Lista de los 40 controles: CR: A1 22 CR y distribución 13/5/2/1/1; A2 CR-01…18 sin cambio vs `13b25ca`; A3 línea de evidencia en los 22; A4 los 5 históricos con advertencia; A5 CR-07/CR-16 apoyados en decisiones emitidas; A6 CR-17 pendiente y CR-12 abierto; A7 CR-19…22 reflejados en índices, `05_`, `07_`, `10_`; A8 restauración CR-21; A9 CR-22 no convertido en decisión; A10 sin contradicciones nuevas **(falló: F1–F8)**. Decisiones: B1 valores del registro; B2 ocurrencias coherentes; B3 D5.a–d no pendientes; B4 D6.c=A0 sin ampliar; B5 D4.d con límites; B6 sin autorización de implementación; B7 sin «pendiente» sin marca en decisiones respondidas **(falló: F6–F8)**. Entidades: C1 estados en la matriz 03 **(falló: F2)**; C2 fila 13 de la matriz consolidada **(falló: F1)**; C3 definiciones literales = registro; C4 sin atributos/relaciones/cardinalidades/entidad 19; C5 residuos «8/18» solo en notas de cambio. Arquitectura: D1 términos en documentos vigentes; D2 históricos conservados e identificados; D3 `docs/fase0` = `main`. Índices y referencias: E1 referencias a archivos de la rama; E2 enlaces markdown; E3 `05_` = árbol; E4 índices mencionan todos los archivos de texto; E5 restaurados conservan contenido; E6 commits citados (con nota §6 b); E7 `11_` 59/59; E8 versiones y fechas de cabeceras. Registro de lectura: F1 estados distinguidos; F2 «líneas únicas ≠ bytes» **(falló: faltaba la aclaración explícita)**; F3 lista de editados tras la lectura **(falló: 8 de 15)**; F4 sin ampliar cobertura sin verificación. Aceptación: H1 sin afirmación de Fase 0 aceptada/Fase 1 autorizada; H2 0/7; H3 sin porcentaje global.

## 17. Pendientes del propietario y lo que Claude no verificó
- **Por decidir/validar (propietario):** P4.B, P4.C, P4.E (E1–E5), Q-1…Q-6, C-2, C-3, entidad 9, entidades 10–12 y 14–18, las preguntas A0 de D6.c, P5…P15, aprobaciones 0.1–0.7, contenido definitivo de fases (y la propuesta de roadmap `11_`), aceptación de Fase 0, autorización de Fase 1.
- **No verificado por Claude:** lo listado en §13 (pruebas, build, E2E, CI, scripts del expediente, `CCI-Evidence`, adjuntos A/B, documentos de la aplicación, lectura byte a byte de `docs/fase0`, reproducción independiente).

## 18. Addendum — corrección puntual del control X4 (base `e049fcda41aad7e8b47f61b60c313c69164210cc`)
**Alcance:** solo el control X4 del script y sus efectos; no es una nueva auditoría y no se vuelve a verificar el resto del expediente. Lo anterior de este informe (§0–§17) no se altera: sus cifras de archivos, manifiestos y blobs corresponden al commit `e049fcd` (110 archivos, 108/109 líneas, 170 blobs); tras esta corrección son **111** archivos, **109** líneas de `MANIFEST.sha256`, **110** de `INVENTARIO_PUBLICADO.sha256` y **171** blobs.
- **Defecto original.** La comprobación X4 (que CR-19…CR-22 estén reflejados en seis documentos) marcaba un CR como ausente solo si su cadena **no** estaba en el texto **y además** no aparecía `19…`, `19…CR-22` ni `CR-19`. Por tanto, bastaba que un documento mencionara `CR-19` (o un fragmento `19…`) para dar por cubiertos CR-20, CR-21 y CR-22 (falso positivo); además un fragmento genérico sin ambos extremos se aceptaba como evidencia. El resultado se mostraba solo como cuatro listas vacías, sin distinguir qué evidencia había satisfecho cada CR.
- **Nueva lógica** (`cr_cubierto` y `evaluar_x4` en el script): cada CR se evalúa individualmente en cada documento; es evidencia una referencia explícita al propio CR (`CR-20`, sin confundir con `CR-2` ni `CR-200`) o un rango con **ambos extremos explícitos** (`CR-19…CR-22`, `CR-19…22`; separadores …, ..., –, —, -) que lo contenga y no esté invertido; no son evidencia `19…`, `19…CR-22`, `CR-19…` ni «CR-19 y siguientes». Si hay varios rangos válidos se informa el más específico. Si falta una referencia, el control falla (`X4_FALLO_referencia_ausente`) y lista cada par (CR, documento) ausente.
- **Pruebas de regresión controladas** (textos sintéticos, dentro del script): **26/26** aprobadas = 24 casos (CR-19 no satisface CR-20, CR-21 ni CR-22; referencia explícita válida satisface su propio CR; rango válido se interpreta correctamente; referencias ambiguas, incompletas, invertidas o confundibles se rechazan) + 1 prueba de que el control falla identificando exactamente documento y CR ausentes + 1 de evidencia más específica. Además el script reproduce el defecto: sobre un texto que solo dice CR-19, la lógica anterior daba «cubierto» para CR-20, CR-21 y CR-22 y la corregida «ausente».
- **Resultado de X4 sobre los documentos reales: 24/24 combinaciones (4 CR × 6 documentos) presentes; ausentes: ninguna.** No había omisión documental real que el defecto estuviera ocultando: no se modificó ningún documento para hacer pasar el control.
| CR | Documento | Resultado | Evidencia |
|---|---|---|---|
| CR-19 | `00_INDICE_VIGENTES_E_HISTORICOS.md` | PRESENTE | explícita: CR-19 |
| CR-19 | `README_ENTREGA.md` | PRESENTE | explícita: CR-19 |
| CR-19 | `auditoria_integral/01_INDICE_MAESTRO_FASE0.md` | PRESENTE | explícita: CR-19 |
| CR-19 | `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md` | PRESENTE | explícita: CR-19 |
| CR-19 | `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | PRESENTE | explícita: CR-19 |
| CR-19 | `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md` | PRESENTE | explícita: CR-19 |
| CR-20 | `00_INDICE_VIGENTES_E_HISTORICOS.md` | PRESENTE | explícita: CR-20 |
| CR-20 | `README_ENTREGA.md` | PRESENTE | explícita: CR-20 |
| CR-20 | `auditoria_integral/01_INDICE_MAESTRO_FASE0.md` | PRESENTE | rango: CR-19…CR-22 |
| CR-20 | `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md` | PRESENTE | rango: CR-19…CR-22 |
| CR-20 | `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | PRESENTE | explícita: CR-20 |
| CR-20 | `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md` | PRESENTE | rango: CR-19…CR-22 |
| CR-21 | `00_INDICE_VIGENTES_E_HISTORICOS.md` | PRESENTE | explícita: CR-21 |
| CR-21 | `README_ENTREGA.md` | PRESENTE | explícita: CR-21 |
| CR-21 | `auditoria_integral/01_INDICE_MAESTRO_FASE0.md` | PRESENTE | explícita: CR-21 |
| CR-21 | `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md` | PRESENTE | explícita: CR-21 |
| CR-21 | `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | PRESENTE | explícita: CR-21 |
| CR-21 | `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md` | PRESENTE | explícita: CR-21 |
| CR-22 | `00_INDICE_VIGENTES_E_HISTORICOS.md` | PRESENTE | explícita: CR-22 |
| CR-22 | `README_ENTREGA.md` | PRESENTE | explícita: CR-22 |
| CR-22 | `auditoria_integral/01_INDICE_MAESTRO_FASE0.md` | PRESENTE | explícita: CR-22 |
| CR-22 | `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md` | PRESENTE | explícita: CR-22 |
| CR-22 | `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | PRESENTE | explícita: CR-22 |
| CR-22 | `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md` | PRESENTE | explícita: CR-22 |
- **Efecto sobre §16:** el control A7 («CR-19…22 reflejados en índices, `05_`, `07_`, `10_`») se reevaluó con la lógica corregida y sigue aprobado (24/24); no cambian 34/40 ni 40/40. Los demás controles del script se reejecutaron: su salida coincide con la original en todas las categorías de fallo y observación (mismos 104 no resueltos externos, mismas 38 menciones condicionales, mismos 9 «sin marca», etc.); difieren solo X4 (corregido), X8 (111/111: `05_` ya lista el archivo de salida nuevo) y dos contadores de comprobaciones aprobadas (V1_ok 1158→1167 y V8_commit_existe 58→62), que suben porque los documentos actualizados añaden referencias y commits válidos. Los controles que no son del script (lectura de diffs y similares) **no** se repitieron.
- **Evidencia.** Salida original conservada sin cambios: `logs/verificacion_coherencia_posterior_2026-11-22.txt` (con el X4 defectuoso). Salida nueva: `logs/verificacion_coherencia_posterior_2026-11-22_x4_corregido.txt` (cabecera con el commit verificado `e049fcd…` y árbol de trabajo con los cambios de esta ronda, que se publican en el commit siguiente). La versión del script de `e049fcd` queda en el historial git.
- **Limitaciones.** Verificación propia; no hay reproducción independiente. Las pruebas de regresión cubren los casos enumerados, no todas las redacciones posibles. X4 comprueba presencia textual de la referencia, no que el texto que la acompaña sea correcto.

> **Nota fechada 2026-11-22 20:14 (respuesta del propietario; no es decisión nueva de este documento):** el propietario emitió las aprobaciones 0.1–0.7 (7/7; la 0.5 solo en cuanto a principios, con P8 sin resolver y sin ninguna integración aprobada) y respondió «sí» a R-1 (aplazamiento aceptado de las seis cuestiones residuales, no resolución). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «0/7», «PENDIENTES» o «R-1 pendiente» describen el estado previo y quedan superadas en ese punto; el resto del texto no se altera. **La aceptación formal de Fase 0 y la autorización independiente de Fase 1 siguen PENDIENTES.** Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.

> **Nota fechada 2026-11-22 20:26 (respuesta del propietario; no es decisión nueva de este documento):** el propietario aceptó formalmente la Fase 0 («Acepto formalmente la Fase 0, con las limitaciones expresas C-2 y C-3 abiertas y los 10 aplazamientos pendientes. No autoriza la Fase 1.»; redacción propuesta por Claude y adoptada literalmente). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «Fase 0 no aceptada» o a la aceptación formal como pendiente describen el estado previo y quedan superadas en ese punto. **C-2, C-3 y los 10 aplazamientos siguen abiertos y la autorización de la Fase 1 sigue PENDIENTE** (acto independiente). Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.

> **Nota fechada 2026-11-22 20:59 (respuesta del propietario; no es decisión nueva de este documento):** el propietario autorizó **únicamente la subfase S1.0** de la Fase 1 (auditoría técnica y definición del alcance ejecutable; rama `fase1/s1-0-auditoria` desde `7bcba74e05577761081d68ca14fdc19f2400248d`; solo lectura, pruebas existentes sin modificar y documentación/evidencia). Las subfases S1.1 y S1.2 quedan autorizadas solo tras su aprobación expresa de los resultados de S1.0 (no activas). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Autorización de la subfase S1.0». Las menciones anteriores de este documento a la autorización de la Fase 1 como pendiente o a «Fase 1 no autorizada» describen el estado previo y quedan superadas en ese punto; la Fase 1 en su conjunto NO está autorizada. **C-2, C-3 y los 10 aplazamientos siguen abiertos.**
