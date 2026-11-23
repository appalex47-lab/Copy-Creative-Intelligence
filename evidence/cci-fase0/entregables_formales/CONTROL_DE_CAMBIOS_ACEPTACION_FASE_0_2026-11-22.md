# Control de cambios — registro de la aceptación formal de la Fase 0 (2026-11-22)
> **Documento fechado, no es decisión nueva.** Base: commit local `301e20c8486ac7073eb5d8e91c71f9cd99ab732b`. Registra qué se cambió en el expediente para reflejar la respuesta del propietario del 2026-11-22 20:26. Solo documental: no se modificó código de la aplicación, `docs/fase0/`, `main`, anexos ni la vista previa privada; no se publicó (el destino autorizado `CCI-Evidence` devolvió 403; commit solo local).

## 1. Decisión registrada (texto literal del propietario)
«Acepto formalmente la Fase 0, con las limitaciones expresas C-2 y C-3 abiertas y los 10 aplazamientos pendientes. No autoriza la Fase 1.»

Procedencia: la redacción fue propuesta por Claude como texto sugerido, no vinculante, y el propietario la adoptó literalmente. Registro autoritativo: `REGISTRO_DECISIONES_RESUELTAS.md`, sección «Aceptación formal de la Fase 0». Efectos:
- La **Fase 0 queda aceptada formalmente** por el propietario (fila «Final» de `APROBACIONES_FASE0.md`), con las aprobaciones 0.1–0.7 ya emitidas a las 20:14.
- Se acepta **con** C-2 y C-3 abiertas (limitaciones expresas) y **con** los 10 aplazamientos pendientes (P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6). Ninguno se resuelve por esta aceptación.
- Decisiones conceptuales sin cambio: 20/30 resueltas; 10/30 con aplazamiento aceptado; 0 abiertas. Estados de CR sin cambio.

## 2. Lo que NO se registró
- **No** se autorizó la Fase 1 (lo dice el propio texto): sigue **PENDIENTE**, como acto independiente, con subfases, respaldo B7, pruebas y prohibiciones indicadas en la propuesta (§19).
- No se cerraron C-2 ni C-3; no se resolvió P8 ni ningún otro aplazamiento; no se reabrió D5.a–d.
- No se aprobó implementar, instalar dependencias, modificar código, publicar ni fusionar con la vista previa privada.
- La aceptación es del expediente **documental**: no acredita pruebas, build, E2E ni CI de la aplicación, ni la verificación técnica de Web Locks, cuotas de IndexedDB o compatibilidad de navegadores.

## 3. Cambios
| Grupo | Archivos | Cambio |
|---|---|---|
| Registro autoritativo | `REGISTRO_DECISIONES_RESUELTAS.md` | Sección nueva con el texto literal, procedencia, efectos, límites y nota cronológica |
| Fichas y paquete | `APROBACIONES_FASE0.md`, `PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md` | Fila «Final» = ACEPTADA (20:26); «Aparte» sigue PENDIENTE; notas fechadas |
| Índices vivos | `00_INDICE_VIGENTES_E_HISTORICOS.md`, `01_INDICE_MAESTRO_FASE0.md`, `05_INFORME_AUDITORIA_INTEGRAL.md` | Estado actualizado con fecha |
| Notas fechadas (texto anterior conservado) | 26 documentos (índices, informes, controles de cambios y propuestas; más las dos fichas ya citadas) que describían la Fase 0 como no aceptada o la aceptación como pendiente | Nota de las 20:26 (texto anterior conservado) |
| Verificadores | `logs/verificacion_semantica_fase0.py` | S5 solo detecta la Fase 1 presentada como autorizada; nuevos S5b (aceptación con alcance no decidido), S16 (estado previo «no aceptada» sin nota de las 20:26), A1 (fila «Final» ACEPTADA; «Aparte» PENDIENTE), A4 (el registro contiene el texto literal y sus límites); 79 pruebas |
| | `logs/prueba_mutacion_semantica.py` | 19 defectos sintéticos (M14–M19 nuevos) |
| | `logs/verificacion_coherencia_posterior.py` | X5c/X5d: «Final» ACEPTADA, «Aparte» PENDIENTE, Fase 1 no autorizada |
| Archivos nuevos (7) | este control de cambios y 6 salidas en `logs/` (`*_aceptacion_fase_0.txt`) | Evidencia |
| Integridad | `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256`, docs `05`, `07` (sección R14), `08`, `12` | Cifras (148 archivos; manifiestos de 146 y 147 líneas; 208 blobs esperados), filas y notas |

**Preservados sin cambios:** `docs/fase0/` (59), `anexos/`, las salidas anteriores de los scripts, los estados de CR-01…CR-22 y el texto de las decisiones anteriores.

## 4. Límites de la verificación
Se verificó la coherencia **documental** con scripts propios (semántico, mutación, coherencia, escaneo, integridad en clon limpio local) y relectura de los cambios. **No** se ejecutaron pruebas, build, E2E ni CI de la aplicación; no se verificaron Web Locks, cuotas de IndexedDB ni compatibilidad de navegadores; los anexos A/B y los documentos del repositorio de la aplicación no se leyeron; no hubo acceso a `CCI-Evidence`; no hubo reproducción independiente por un tercero.
