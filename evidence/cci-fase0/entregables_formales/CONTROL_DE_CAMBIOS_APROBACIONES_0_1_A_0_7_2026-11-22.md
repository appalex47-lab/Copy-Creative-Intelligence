# Control de cambios — registro de las aprobaciones 0.1–0.7 y de la respuesta a R-1 (2026-11-22)
> **Documento fechado, no es decisión nueva.** Base: commit local `cad808a2da6659d68b41578625ed409a4f8ee3d8`. Registra qué se cambió en el expediente para reflejar la respuesta del propietario del 2026-11-22 20:14. Solo documental: no se modificó código de la aplicación, `docs/fase0/`, `main`, anexos ni la vista previa privada; no se publicó (el destino autorizado `CCI-Evidence` devolvió 403; commit solo local).

## 1. Decisión registrada (texto literal del propietario)
«Apruebo 0.1 a 0.7 según las recomendaciones del paquete (0.5 solo en cuanto a principios; P8 sigue sin resolver y ninguna integración queda aprobada). R-1 sí.»

Registro autoritativo: `REGISTRO_DECISIONES_RESUELTAS.md`, sección «Aprobaciones formales 0.1–0.7 y respuesta a R-1». Efectos:
- Aprobaciones 0.1–0.7 **emitidas por el propietario: 7/7** (la 0.5 solo en cuanto a principios; P8 sigue sin resolver y ninguna integración, proveedor, clave ni llamada remota queda aprobada).
- R-1 = «sí»: **aplazamiento aceptado**, nunca resolución, de las seis cuestiones residuales (ubicación conceptual de la familia de reglas de copy, de D-3; y las cinco de D-5). No modifica D-3 ni D-5, no reabre D-5.1/5.2/5.3, M-1 ni D5.a–d. No se suma a 20/30 ni a 10/30.
- Decisiones conceptuales sin cambio: 20/30 resueltas; 10/30 con aplazamiento aceptado (P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6); 0 abiertas. P4.A 18/18. Estados de CR sin cambio.

## 2. Lo que NO se registró
- **No** se aceptó la Fase 0 (acto distinto, PENDIENTE: requiere respuesta expresa).
- **No** se autorizó la Fase 1 (autorización independiente, PENDIENTE; con subfases, respaldo B7, pruebas y prohibiciones indicadas en la propuesta, §19).
- No se resolvió P8 ni ningún otro aplazamiento; no se cerraron C-2 ni C-3; no se reabrió D5.a–d.
- No se interpretó ninguna recomendación como decisión fuera del alcance de la respuesta; el propietario las adoptó por esa respuesta, con el alcance de cada ficha.

## 3. Cambios
| Grupo | Archivos | Cambio |
|---|---|---|
| Registro autoritativo | `REGISTRO_DECISIONES_RESUELTAS.md` | Sección nueva con el texto literal, tabla 0.1–0.7, R-1, conteos, límites y nota cronológica; la nota de R-1 anterior queda con una remisión (el texto previo se conserva) |
| Fichas | `APROBACIONES_FASE0.md` | Estado de 0.1–0.7: APROBADA (0.5 solo principios); «Final» y «Aparte» PENDIENTES; nota fechada al inicio y en el antecedente |
| Paquete | `PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md` | Nota fechada y estado por ficha; R-1 respondida (aplazamiento aceptado) |
| Índices vivos | `00_INDICE_VIGENTES_E_HISTORICOS.md`, `01_INDICE_MAESTRO_FASE0.md`, `05_INFORME_AUDITORIA_INTEGRAL.md` | Estado de las aprobaciones actualizado con fecha |
| Notas fechadas (texto anterior conservado) | `README_ENTREGA.md`, `02`, `05`, `06`, `09`, `10`, `13`, `14`, `15`, `16_INDICE…`, `CONCILIACION…`, `INFORME_REVISION_COMPLEMENTARIA.md`, `INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md`, `PROPUESTA_MAESTRA…`, controles de cambios de rondas anteriores (4) | Nota de las 20:14: lo anterior sobre «0/7», «PENDIENTES» o «R-1 pendiente» describe el estado previo |
| Verificadores | `logs/verificacion_semantica_fase0.py` | S4 pasa a detectar la extensión de 0.1–0.7 a lo no decidido (aceptación de Fase 0, autorización de Fase 1, integración de IA, P8 resuelta); nuevos S4b (0.5 sin «solo principios»), S15 (estado previo «0/7» sin nota de las 20:14), A1 reescrito (7 fichas APROBADAS, «Final» y «Aparte» PENDIENTES), A3 (el registro contiene el texto literal y sus límites); 70 pruebas |
| | `logs/prueba_mutacion_semantica.py` | 13 defectos sintéticos (M5 reescrito; M9–M13 nuevos) |
| | `logs/verificacion_coherencia_posterior.py` | X5b/X5c/X5d: 7 aprobaciones APROBADAS; «Final» y «Aparte» PENDIENTES; ninguna fase aceptada ni autorizada |
| Archivos nuevos (7) | este control de cambios y 6 salidas en `logs/` (`*_aprobaciones_0_1_a_0_7.txt`) | Evidencia |
| Integridad | `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256`, docs `05`, `07` (sección R13), `08`, `12` | Cifras (141 archivos; manifiestos de 139 y 140 líneas; 201 blobs esperados), filas y notas |

**Preservados sin cambios:** `docs/fase0/` (59), `anexos/`, las salidas anteriores de los scripts, los estados de CR-01…CR-22 y el texto de las decisiones anteriores.

## 4. Límites de la verificación
Se verificó la coherencia **documental** con scripts propios (semántico, mutación, coherencia, escaneo, integridad en clon limpio local) y relectura de los cambios. **No** se ejecutaron pruebas, build, E2E ni CI de la aplicación; no se verificaron Web Locks, cuotas de IndexedDB ni compatibilidad de navegadores; los anexos A/B y los documentos del repositorio de la aplicación no se leyeron; no hubo acceso a `CCI-Evidence`; no hubo reproducción independiente por un tercero.
