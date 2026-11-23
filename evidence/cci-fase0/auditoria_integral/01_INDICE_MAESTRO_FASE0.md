# Índice maestro de Fase 0 — CCI (2026-11-22)
**Naturaleza:** documento vigente de orientación, subordinado a `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. No es una aprobación del propietario ni un informe de aceptación.
**Base:** HEAD de partida `1bb831a32219898616e7a7ad8d12092aac16f253`; rama `evidence/cci-fase0-review`; repositorio `appalex47-lab/Copy-Creative-Intelligence`.

## 1. Jerarquía de fuentes (de mayor a menor autoridad)
1. **Decisiones expresas del propietario** emitidas en la conversación o en registros verificables.
2. `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` — **fuente autoritativa documental** (cuando refleja fielmente las decisiones). Si difiere de una decisión original verificable, se corrige el registro; no se puede verificar aquí ninguna decisión que no esté transcrita en la conversación o en el registro.
3. **Documentos vigentes subordinados:** `entregables_formales/04_ARQUITECTURA_BROWSER_ONLY.md` (propuesta de arquitectura vigente por decisión del propietario; la aprobación 0.2 sigue pendiente), `MATRIZ_CONSOLIDADA_18_ENTIDADES.md`, `DECISIONES_P4_PENDIENTES.md`, `CATALOGO_DEPENDENCIAS_D4_D8.md`, `APROBACIONES_FASE0.md`.
4. **Índices, matrices, informes y controles de cambios** (reflejan los niveles 1–3; son fechados).
5. **Análisis, paquetes, fichas y documentos históricos** (valor probatorio; no prevalecen sobre decisiones posteriores): incluidos los 59 archivos de `docs/fase0/` (ver `11_INDICE_CONCILIACION_DOCS_FASE0.md`).
Una **nota de ChatGPT**, un **informe de cierre** o una **recomendación de Claude** no son aprobaciones del propietario.

## 2. Estado vigente (resumen)
| Tema | Estado vigente | Fuente |
|---|---|---|
| Arquitectura | **browser-only, un usuario por navegador**: sin cuentas/login, autenticación, backend, Supabase, PostgreSQL, SQL, servidor ni sincronización; IndexedDB principal; Local Storage solo preferencias ligeras; exportación/importación local, respaldo y recuperación por diseñar | P1, P2, P3 y `04_ARQUITECTURA_BROWSER_ONLY.md` |
| P1, P2 (incl. «Seguridad por diseño»), P3 | Resueltas | Registro |
| P4.1 | Resuelta parcialmente (solo nombres de la lista de 18) | Registro |
| P4.2, P4.3, Colección | Resueltas / mantenida | Registro |
| P4.4 / P4.D / Q-7 | **Resueltas → (a); P4.4 cerrada** | Registro |
| P4.5 | Aprobación preliminar conservada (no definitiva) | Registro |
| P4.A | **18/18 aprobadas (100 %) con definición mínima** (ratificación 15:56; antes: 9/18 — entidades 1–8 y 13 — con 9 suspendida) | Registro (P4.A, D4.c, B1) |
| D-1, D-2, D-3, D-5 | Resueltas (D5.a–d fuera del alcance vigente; no se reabren) | Registro |
| D-4 (D4.a–d), D-6 (D6.a–c), D-7 (D7.a–c), D-8 | Resueltas: D4.a=A, D4.b=A, D4.c=A, D4.d=A (limitada por M-1 y D-5.3), D6.a=A, D6.b=A, D6.c=A0 (deja sin decidir origen de valores, L1/L2 y L3), D7.a=A, D7.b=A, D7.c=C, D8=A | Registro, sección «D-4, D-6, D-7 y D-8» |
| P4.B, P4.C, P4.E (E1–E5) | **Pendientes** | `DECISIONES_P4_PENDIENTES.md` |
| Q-1, Q-2, C-2, C-3 | **Abiertas** | Registro, `INDICE_ANTECEDENTES_HISTORICOS.md` |
| Resto de decisiones P5–P15, Q-3–Q-6 | Pendientes (ver matriz maestra) | `13_REGISTRO_DECISIONES_PROPIETARIO.md` |
| Aprobaciones 0.1–0.7 | **Pendientes** | `APROBACIONES_FASE0.md` |
| Aceptación formal de Fase 0 | **No aceptada** | — |
| Fase 1 | **No autorizada**; no hay autorización para implementar código | — |

**Actualización ronda final (2026-11-22):** esta auditoría se completó en una ronda final; los documentos 05, 06, 08, 09, 10 y 12 se rehicieron o actualizaron. Versión de la carpeta: `auditoria_integral` v2 (ronda final, base HEAD `8dc47b2`). P4.A vigente: **9/18**; D4.d=A; CR-16 resuelta por independencia de D6.b y D6.c=A0.
*[Alineación 2026-11-22, regularización posterior a la ratificación B1–B10; no es decisión nueva; el texto anterior se conserva]* El conteo «P4.A vigente: 9/18» corresponde a la ronda final previa. **Estado vigente: P4.A 18/18 (existencia y definición mínima únicamente)** conforme a `REGISTRO_DECISIONES_RESUELTAS.md`, sección B1.

## 3. Documentos de la auditoría integral (esta carpeta)
| # | Documento | Contenido |
|---|---|---|
| 01 | `01_INDICE_MAESTRO_FASE0.md` | Este índice |
| 02 | `02_MATRIZ_MAESTRA_DECISIONES.md` | Decisiones resueltas y pendientes |
| 03 | `03_MATRIZ_MAESTRA_ENTIDADES_P4A.md` | 18 entidades |
| 04 | `04_MATRIZ_MAESTRA_DEPENDENCIAS.md` | P4.B/P4.C/P4.E/Q/C y dependencias |
| 05 | `05_INFORME_AUDITORIA_INTEGRAL.md` | Alcance, clasificación de todos los archivos del expediente (vigencia), método, limitaciones |
| 06 | `06_REGISTRO_CONTRADICCIONES.md` | Contradicciones y su resolución (v3.0: CR-01…CR-22) |
| 07 | `07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md` | Cambios de esta auditoría |
| 08 | `08_INFORME_INTEGRIDAD_ARCHIVOS.md` | Hashes, tamaños, clon limpio |
| 09 | `09_PAQUETE_CONSOLIDADO_DECISIONES_PENDIENTES.md` | Paquetes para el propietario |
| 10 | `10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md` | Preparación para el cierre |
| 11 | `11_INDICE_CONCILIACION_DOCS_FASE0.md` | Conciliación de los 59 archivos de `docs/fase0/` |
| 12 | `12_REGISTRO_LECTURA_Y_LIMITACIONES.md` | Registro de lectura real v2.1 (v2.0 + §7 de la ronda de coherencia; lectura completa; `docs/fase0` por líneas únicas; estados LEÍDO_COMPLETO / LEÍDO_PARCIALMENTE / NO_ACCESIBLE / NO_APLICABLE) y ficha de los 52 históricos |
| 13 | `13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md` | Verificación final de coherencia posterior a la regularización (hallazgos, correcciones, estados, porcentajes con base; no acepta Fase 0 ni autoriza Fase 1) |

## 4. Orden de lectura recomendado
Registro → este índice → 02, 03, 04 → 09 (lo que el propietario debe decidir) → 10 → 05, 06, 08, 12, 13 (evidencia de la auditoría).
Guía de entrega y estado de archivos: `README_ENTREGA.md`, `00_INDICE_VIGENTES_E_HISTORICOS.md`, `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md`.

**Actualización ronda de lectura completa (2026-11-22; base HEAD `13b25ca`):** lectura íntegra de todos los archivos legibles (`12_` v2.0); nuevas CR-19…CR-22 en `06_` v3.0 (CR-21: regresión propia restaurada); docs 05, 07 (R7), 08, 10, 11 actualizados. **Roadmaps:** vigente como propuesta no aprobada es `entregables_formales/11_ROADMAP_FASES_0_A_5.md`; el §15 del anexo original y los roadmaps de `docs/fase0` son antecedentes (CR-22). La jerarquía de fuentes no cambia. No se acepta Fase 0 ni se autoriza Fase 1.

> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; el texto original no se altera):** la fila P4.A de la tabla de estado («9/18 … entidad 9 suspendida») es antecedente: **P4.A vigente = 18/18** con definición mínima aprobada. Estado vigente por ítem: `02_MATRIZ_MAESTRA_DECISIONES.md` §A.2 y B; entidades: `03_MATRIZ_MAESTRA_ENTIDADES_P4A.md`. Nuevos archivos: `../entregables_formales/PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md`, `../entregables_formales/CONTROL_DE_CAMBIOS_RATIFICACION_PROPUESTA_MAESTRA_2026-11-22.md`, `../logs/verificacion_coherencia_posterior_2026-11-22_tras_ratificacion.txt`. Fuente y texto literal: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)». Aprobaciones 0.1–0.7, aceptación de Fase 0 y autorización de Fase 1 siguen pendientes.

> **Nota fechada 2026-11-22 (regularización posterior a la ratificación y preparación de aprobaciones; no es decisión nueva):** el expediente incorpora `entregables_formales/CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md`, `entregables_formales/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md`, `entregables_formales/CONTROL_DE_CAMBIOS_PREPARACION_APROBACIONES_2026-11-22.md` y `auditoria_integral/14_INFORME_FINAL_REGULARIZACION_Y_PREPARACION_APROBACIONES.md`. Estado vigente: aprobaciones 0.1–0.7 = 0/7 emitidas (pendientes); Fase 0 no aceptada; Fase 1 no autorizada; 20/30 decisiones resueltas y 10/30 aplazadas; P4.A 18/18 (solo existencia y definición mínima).

> **Nota fechada 2026-11-22 (segunda regularización; no es decisión nueva):** R-1 corregida: incluye **seis** cuestiones residuales (la ubicación conceptual de la familia de reglas de copy, de D-3, y las cinco de D-5: auditoría o validaciones previas; modificación de un contenido aprobado; relación con las versiones; identidad exacta del contenido aprobado; relación con los estados del flujo); una respuesta afirmativa se registra como aplazamiento, nunca como resolución. D5.a–d siguen fuera del alcance vigente y no se reabren. `06_MODELO_DATOS_CCI.md` es una propuesta histórica, no un esquema de datos aprobado. Estado: aprobaciones 0.1–0.7 = 0/7 emitidas; Fase 0 no aceptada; Fase 1 no autorizada. La tabla de §3 lista los documentos 01–13 (fotografía anterior); la carpeta contiene además `14_INFORME_FINAL_REGULARIZACION_Y_PREPARACION_APROBACIONES.md` y `15_INFORME_FINAL_SEGUNDA_REGULARIZACION.md` (15 documentos en total).
