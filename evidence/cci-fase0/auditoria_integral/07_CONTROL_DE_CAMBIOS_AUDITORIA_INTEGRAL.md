# Control de cambios — Auditoría integral y regularización (2026-11-22)
**Versión:** 2.2 (secciones R1–R8 de rondas anteriores conservadas; R9 añade la corrección puntual de X4)
**Commit base:** `1bb831a32219898616e7a7ad8d12092aac16f253` (HEAD real verificado por API antes de editar; `main` = `6a1af24`). Rama `evidence/cci-fase0-review`. Solo documentación bajo `evidence/cci-fase0/`.
**Motivo:** mandato de auditoría integral de todo el expediente de Fase 0, regularización documental y preparación de decisiones pendientes.

## 1. Documentos creados (carpeta `auditoria_integral/`)
`01_INDICE_MAESTRO_FASE0.md`, `02_MATRIZ_MAESTRA_DECISIONES.md`, `03_MATRIZ_MAESTRA_ENTIDADES_P4A.md`, `04_MATRIZ_MAESTRA_DEPENDENCIAS.md`, `05_INFORME_AUDITORIA_INTEGRAL.md`, `06_REGISTRO_CONTRADICCIONES.md`, `07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` (este), `08_INFORME_INTEGRIDAD_ARCHIVOS.md`, `09_PAQUETE_CONSOLIDADO_DECISIONES_PENDIENTES.md`, `10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md`, `11_INDICE_CONCILIACION_DOCS_FASE0.md`.
## 2. Documentos modificados (solo adiciones/anotaciones; sin borrar antecedentes)
| Archivo | Cambio | Razón |
|---|---|---|
| `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md` | Entradas de fichas P4.A 01–08 y 09 con estado vigente; enlace a la auditoría | CR-08 |
| `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` | Nota fechada de lectura cronológica (P4.1 «PENDIENTE», P4.4 «APLAZADO», entidad 1 «pendiente» superados) | CR-04; no altera ninguna decisión |
| `00_INDICE_VIGENTES_E_HISTORICOS.md`, `README_ENTREGA.md` | Enlace al índice maestro y a los documentos de auditoría | Navegación |
| `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256` | Regenerados al terminar | Integridad |
## 3. Fundamento y verificaciones
Fundamento: registro autoritativo (P1–P4, Q-7, D-1…D-8, D4–D8). Verificaciones ejecutadas por mí: reconteo de 11 encabezados D4/D6/D7/D8 en el registro (uno cada uno); extracción literal de definiciones 1–8 y 13 desde el registro; búsquedas de patrón de estados incompatibles; comprobación de referencias a archivos; hashes y tamaños (ver `08_…`). No se usaron reemplazos globales.
## 4. Estados que permanecen abiertos
P4.B, P4.C, P4.E (E1–E5), Q-1, Q-2, C-2, C-3, entidad 9 (suspendida), entidades 10–12 y 14–18, A0-1/2/3, CR-15, CR-16 *[nota ronda de coherencia: CR-15 y CR-16 quedaron resueltas (ver `06_` v3.0 y R5); este §4 es el estado de la ronda original]*, P5…P15 y Q-3…Q-6, aprobaciones 0.1–0.7, aceptación de Fase 0, autorización de Fase 1. **D5.a–d: fuera de alcance, no reabiertas.**
## 5. Preservados sin cambios
Los 59 archivos de `docs/fase0/` (idénticos a `main`), todas las fichas, análisis D1/D2/D3/D5, paquetes, informes y controles anteriores, `MANIFIESTO_ENTREGA…txt`, anexos y logs.
## 6. Limitaciones
Ver `05_INFORME_AUDITORIA_INTEGRAL.md` §4. Se publicaron dos commits: (1) `1cf96e3` (contenido de la auditoría y manifiestos) y (2) ajuste de `16_INDICE`, números de integridad en `08_` y manifiestos regenerados. El SHA del segundo no puede escribirse dentro de los archivos que contiene; se informa en la entrega y se verifica por API.


---
# RONDA FINAL ÚNICA — control de cambios (2026-11-22)
**Versión:** 2.0 · **Base:** HEAD `8dc47b24bdd5b11df46a70f3c9d96930d0682235` (verificado por API al iniciar; idéntico a la referencia; `main` = `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`, sin commits posteriores en la rama). Rama `evidence/cci-fase0-review`. Solo documentación bajo `evidence/cci-fase0/`; sin cambios de código, `main`, PR, merge ni despliegue.

## R1. Correcciones de contenido (hallazgos obligatorios)
| Hallazgo | Corrección | Archivos |
|---|---|---|
| 3.1 Texto 8/18 «Prevalece este aviso», «Adaptación pendiente de D-4», «(8/18) no se modifica» | Marcados como antecedente histórico superado con el estado vigente 9/18 (entidades 1–8 y 13 aprobadas con definición mínima; 9 suspendida; 10–12 y 14–18 sin aprobación vigente); entidad 13 solo con la definición literal de D4.c (sin atributos, relaciones, cardinalidades, mecanismos, estructura, persistencia, versionado ni fase); columnas históricas de las filas 13, 15, 17 y de Perfil local rotuladas | `MATRIZ_CONSOLIDADA_18_ENTIDADES.md`, `DECISIONES_P4_PENDIENTES.md`, `LISTA_ORIGINAL_18_ENTIDADES.md`, `REGISTRO_DECISIONES_RESUELTAS.md` (tres marcas inline que no alteran decisiones) |
| 3.2 D4.d presentada como pendiente | Barrido y marcas; aviso «PAQUETE RESPONDIDO» | `PAQUETE_DECISION_D4_D6_D7_D8.md`, MATRIZ_18, registro |
| 3.3 CR-16 mal interpretada | Resuelta por independencia (D6.b=A y D6.c=A0); PAQ-2/A0-1 reescrito; informe ejecutivo corregido | `06_`, `09_`, `10_` |
| 3.4 Estados «resuelta» sin reflejo en vigentes | Verificación contra los documentos vigentes; ver `06_` (campo «Evidencia») | `06_` |
| 3.5 93/93 frente a 104 | Clasificación de todos los archivos actuales; cifras corregidas | `05_`, `10_`, `08_` |
| Avisos de vigencia | Añadidos a 10 copias previas de la raíz y a `DIAGNOSTICO_INTEGRAL…` y `CONVENCIONES_P4_5…` | ver R2 |
| Matriz de pendientes | Sección B.2 con los campos adicionales por ítem | `02_` |
| Nuevo | `12_REGISTRO_LECTURA_Y_LIMITACIONES.md`; `logs/scan_contradicciones.py` y su salida | `auditoria_integral/`, `logs/` |

## R2. Archivos modificados respecto de `8dc47b2` (27; incluye este documento y `08_`, que se completaron después de listar)
- `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md`
- `auditoria_integral/08_INFORME_INTEGRIDAD_ARCHIVOS.md`
- `00_DICTAMEN_Y_CIERRE_FASE0.md`
- `00_INDICE_VIGENTES_E_HISTORICOS.md`
- `01_INFORME_AUDITORIA.md`
- `02_INVENTARIO_FUNCIONALIDADES.md`
- `04_MATRIZ_REQUISITOS.md`
- `08_RESPALDO_Y_RECUPERACION.md`
- `09_ANALISIS_IA.md`
- `11_ROADMAP_Y_CRITERIOS_FASES_1_A_5.md`
- `12_ESTRATEGIA_DE_PRUEBAS.md`
- `13_VERIFICACION_EJECUTADA.md`
- `14_ESTADO_GIT_Y_OPERACIONES.md`
- `README_ENTREGA.md`
- `auditoria_integral/01_INDICE_MAESTRO_FASE0.md`
- `auditoria_integral/02_MATRIZ_MAESTRA_DECISIONES.md`
- `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md`
- `auditoria_integral/06_REGISTRO_CONTRADICCIONES.md`
- `auditoria_integral/09_PAQUETE_CONSOLIDADO_DECISIONES_PENDIENTES.md`
- `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md`
- `entregables_formales/CONVENCIONES_P4_5_CONDICIONES.md`
- `entregables_formales/DECISIONES_P4_PENDIENTES.md`
- `entregables_formales/DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md`
- `entregables_formales/LISTA_ORIGINAL_18_ENTIDADES.md`
- `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md`
- `entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md`
- `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`

## R3. Archivos nuevos respecto de `8dc47b2` (3)
- `auditoria_integral/12_REGISTRO_LECTURA_Y_LIMITACIONES.md`
- `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt`
- `logs/scan_contradicciones.py`

## R4. Preservados sin cambios
Los 59 archivos de `docs/fase0/` (idénticos a `main`; `git ls-tree` coincide), el `README.md` de la raíz del repositorio, todas las fichas P4A y análisis (solo `FICHA_*` no tocadas), `anexos/` y los logs previos.

## R5. Estados que permanecen abiertos (no se resuelven aquí)
P4.B, P4.C, P4.E (E1–E5), Q-1…Q-6, C-2, C-3, entidad 9 (suspendida), entidades 10–12 y 14–18, A0-1/A0-2/A0-3, P5…P15, aprobaciones 0.1–0.7, aceptación formal de Fase 0 y autorización de Fase 1. **No se declara aceptada la Fase 0 ni se solicita autorizar la Fase 1.** D5.a–d: fuera del alcance, no reabiertas.

## R6. Limitaciones
Ver `12_REGISTRO_LECTURA_Y_LIMITACIONES.md` v2.0: la brecha de lectura declarada en la ronda final quedó cerrada en la ronda de lectura (ver R7), con la limitación del método de líneas únicas. El SHA del commit de esta ronda no puede escribirse dentro de los archivos que contiene; se informa en la entrega y se verifica por API.

## R7. Ronda de lectura completa (base `13b25ca447c0ab17f46b3143615b4c2156661b79`)
**Alcance:** leer íntegramente los archivos parciales o sin lectura (expediente y los 59 de `docs/fase0/`, incluidos los 52 históricos) y documentar el resultado. No se modificó código, `main`, `docs/fase0` ni se hizo merge, PR o deploy.
**Archivos modificados (solo adiciones/restauración; contenido original no alterado):**
| Archivo | Cambio | Razón |
|---|---|---|
| `00_INDICE_VIGENTES_E_HISTORICOS.md`, `README_ENTREGA.md` | Restaurados desde `1bb831a` (habían sido truncados en `1cf96e3`) + nota de restauración + referencias a CR-19…22 | CR-21 (defecto propio) |
| `03_CONCILIACION_DOCUMENTAL.md`, `10_REGISTRO_DECISIONES.md`, `INFORME_REVISION_COMPLEMENTARIA.md` | Aviso de vigencia antepuesto | CR-20 |
| `entregables_formales/MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` | Línea `# NOTA` de cabecera | CR-20 / CR-14 |
| `entregables_formales/README_PROPUESTA_VIGENTE.md` | Nota de actualización posterior | CR-19 |
| `auditoria_integral/01`, `05`, `06` (v3.0), `08`, `10`, `11`, `12` (v2.0) | Cifras, método y limitaciones actualizados; CR-19…CR-22 | Lectura completa |
| `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256` | Regenerados por script | Integridad |
**Preservados sin cambios:** `docs/fase0/` (59 archivos), `anexos/`, `logs/` previos, fichas P4A y análisis.

## R8. Ronda de verificación de coherencia posterior (base `580c51f3d0e2e54695a431352957f34f9418b067`)
**Alcance:** verificación acotada de coherencia de todo lo modificado desde el inicio de la regularización de Fase 0 (no una re-auditoría de los 166 documentos). Informe: `13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md`. No se modificó código, `main`, `docs/fase0`; no hubo merge, PR ni deploy. No se cambió el estado de ningún CR ni ninguna decisión del propietario.
**Archivos modificados (correcciones editoriales de anotaciones; el texto original se conserva y las notas lo indican):**
| Archivo | Cambio | Hallazgo |
|---|---|---|
| `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` | Restituido el paréntesis literal de la fila 13; «delimitación pendiente en P4.B» → D4.a=A fijó el criterio (relaciones/cardinalidades siguen sin aprobar); anotación de Perfil local | F1 |
| `auditoria_integral/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md` | Referencia «CR-06» → «CR-15»; fila Perfil local (D7.a=A solo fija el criterio de distinción) | F2 |
| `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | Nota en §4 (CR-15 y CR-16 resueltos) y esta sección | F3 |
| `auditoria_integral/06_REGISTRO_CONTRADICCIONES.md` | Observación de la lectura corregida; «9 fases» → «Fases 0–9» (CR-22); barrido de CR-21 referido al historial git | F4 |
| `entregables_formales/13_REGISTRO_DECISIONES_PROPIETARIO.md` | Nota en línea de estado (P1–P3 resueltas, P4 parcial, Q-7 resuelta) | F5 |
| `entregables_formales/CATALOGO_DEPENDENCIAS_D4_D8.md`, `entregables_formales/PAQUETE_DECISION_D1_D8.md` | Marcas «[superado: …]» en líneas que decían «pendiente» | F6, F7 |
| `entregables_formales/D5_APROBACION.md` | Nota de la ronda de coherencia tras el encabezado de actualización posterior | F8 |
| `auditoria_integral/01`, `05` (v3.1), `08` (v3.1), `10`, `12` (v2.1) | Cifras (110 archivos; 108/109 líneas de manifiesto; 170 blobs), métrica de avisos de vigencia con su alcance real, aclaración «líneas únicas ≠ bytes revisados individualmente» | Integridad / presentación |
| `00_INDICE_VIGENTES_E_HISTORICOS.md`, `README_ENTREGA.md` | Nota de la ronda (solo adición al final) | Índices |
| `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256` | Regenerados por script al final, sin ediciones posteriores | Integridad |
**Archivos nuevos (3):** `auditoria_integral/13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md`, `logs/verificacion_coherencia_posterior.py`, `logs/verificacion_coherencia_posterior_2026-11-22.txt`.
**Preservados sin cambios:** `docs/fase0/` (59), `anexos/`, logs previos, fichas P4A y análisis, `REGISTRO_DECISIONES_RESUELTAS.md` y todos los demás archivos no listados.

## R9. Corrección puntual del control X4 (base `e049fcda41aad7e8b47f61b60c313c69164210cc`)
**Alcance:** corregir el control X4 de `logs/verificacion_coherencia_posterior.py`, reejecutar el script y actualizar la evidencia directamente afectada. No es una nueva auditoría. No se modificó código de la aplicación, decisiones, definiciones de entidades, estados de CR ni documentos históricos; no hubo omisión documental real (X4: 24/24).
| Archivo | Cambio | Motivo |
|---|---|---|
| `logs/verificacion_coherencia_posterior.py` | X4 reescrito (comprobación individual por CR y documento; rangos con ambos extremos explícitos; pruebas de regresión; reproducción del defecto) | Defecto de X4 (ver `13_` §18) |
| `logs/verificacion_coherencia_posterior_2026-11-22_x4_corregido.txt` (nuevo) | Salida fechada del script corregido, con el commit verificado en su cabecera | Evidencia; la salida original se conserva sin cambios |
| `auditoria_integral/13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md` | Addendum §18 (el contenido anterior no se altera) | Registrar defecto, corrección, pruebas y resultado |
| `auditoria_integral/05`, `08`, `10`, `12` | Cifras: 111 archivos; 109/110 líneas de manifiesto; 171 blobs; una fila NO_APLICABLE | Archivo nuevo |
| `auditoria_integral/07` (este archivo) | R9 | Control de cambios |
| `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256` | Regenerados | Integridad |

## R10. Registro de la ratificación de la propuesta maestra de cierre de Fase 0 (base `bb2030a9bc88d0ac5f2603ade57f674033c7ab0c`)
**Alcance:** registrar la respuesta «Confirmo todo» del propietario (2026-11-22 15:56) como ratificación de B1–B10 y actualizar la evidencia derivada. No es una nueva auditoría. No se modificó código de la aplicación, `docs/fase0/`, `main` ni estados de CR; no se emitió ninguna aprobación (0/7); no se aceptó Fase 0 ni se autorizó Fase 1.
| Archivo | Cambio | Motivo |
|---|---|---|
| `entregables_formales/PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md` (nuevo) | Copia literal de la propuesta ratificada | Fuente literal de las definiciones |
| `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` | Sección de ratificación B1–B10 y nota cronológica | Registro autoritativo |
| `entregables_formales/CONTROL_DE_CAMBIOS_RATIFICACION_PROPUESTA_MAESTRA_2026-11-22.md` (nuevo) | Interpretaciones, archivos, cifras y estado de los criterios del §18 | Control de cambios |
| Matrices y fichas (`02`, `03`, `04`, `09`, matriz consolidada, `13_REGISTRO…`, `DECISIONES_P4_PENDIENTES`, `FICHA_P4*`, `MATRIZ_DECISIONES_PROPIETARIO`, `D3`, `10_DEFINICION_MVP`, `DIAGNOSTICO…`, `LISTA_ORIGINAL…`) | Estado vigente actualizado o nota fechada; el estado anterior se conserva como antecedente superado | Coherencia sin reescribir historia |
| Índices y informes (`00_INDICE`, `README_ENTREGA`, `README_PROPUESTA_VIGENTE`, `16_INDICE`, `01`, `05` v3.3, `06` (solo nota), `08` v3.3, `10` v3.3, `12` v2.3, `APROBACIONES_FASE0`) | Cifras (114 archivos; manifiestos de 112 y 113 líneas; 174 blobs), notas y filas | Coherencia |
| `logs/verificacion_coherencia_posterior.py` | Añadido control V13 (conteo «9/18» sin marca de antecedente) y nombre de la nueva salida en la lista de exclusión | Verificar la coherencia tras la ratificación |
| `logs/verificacion_coherencia_posterior_2026-11-22_tras_ratificacion.txt` (nuevo) | Salida del script | Evidencia |
| `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256` | Regenerados | Integridad |
**Preservados sin cambios:** `docs/fase0/` (59), `anexos/`, la salida original y la corregida del script, `13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md`, fichas P4A históricas (salvo la nota en la ficha 09), y los estados de CR-01…CR-22.

