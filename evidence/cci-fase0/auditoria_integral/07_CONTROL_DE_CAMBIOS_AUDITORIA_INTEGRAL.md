# Control de cambios — Auditoría integral y regularización (2026-11-22)
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
P4.B, P4.C, P4.E (E1–E5), Q-1, Q-2, C-2, C-3, entidad 9 (suspendida), entidades 10–12 y 14–18, A0-1/2/3, CR-15, CR-16, P5…P15 y Q-3…Q-6, aprobaciones 0.1–0.7, aceptación de Fase 0, autorización de Fase 1. **D5.a–d: fuera de alcance, no reabiertas.**
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
Ver `12_REGISTRO_LECTURA_Y_LIMITACIONES.md`: **no se logró la lectura íntegra** del expediente ni de `docs/fase0/`; la ronda no se declara completamente terminada en ese criterio. El SHA del commit de esta ronda no puede escribirse dentro de los archivos que contiene; se informa en la entrega y se verifica por API.
