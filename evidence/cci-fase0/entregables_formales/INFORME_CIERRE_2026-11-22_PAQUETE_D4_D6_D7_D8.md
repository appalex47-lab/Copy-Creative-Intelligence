# Informe de cierre — Paquete D-4, D-6, D-7 y D-8 (2026-11-22, 12:40)
> **Actualización posterior (2026-11-22, tras la revisión de ChatGPT) — el texto original se conserva como registro de ese momento.** Donde este informe menciona D5.a–d como pendientes, rige la decisión posterior del propietario: **D-5 resuelta; D5.a–d fuera del alcance del paquete vigente; no son pendientes ni abiertas ni se vuelven a preguntar.** Sin otras modificaciones.
Aplicado conforme al protocolo permanente recibido a las 12:39. Ninguna recomendación se presenta como decisión aprobada; ninguna dependencia se declara aceptada.

## A. Resultado
- **Se solicitó:** un paquete único de decisión para D-4, D-6, D-7 y D-8 (12:35).
- **Completado:** `PAQUETE_DECISION_D4_D6_D7_D8.md` (11 decisiones: D4.a–d, D6.a–c, D7.a–c, D8; alternativas, consecuencias, evidencia, recomendación, límites, revisión cruzada, matriz, respuestas agrupadas, asuntos excluidos). Sustituye a `PAQUETE_DECISION_D1_D8.md` (conservado como histórico).
- **Pendiente:** tu respuesta a las 11 decisiones; D5.a–d; resto de pendientes de Fase 0. *[superado por decisión posterior: D5.a–d fuera del alcance vigente; ver nota superior]*
- **No ejecutado:** subida a CCI-Evidence (ver C); código, commits, push, PR, merge, despliegues; fusión con vista previa privada.

## B. Decisiones
- **Aprobadas expresamente por el propietario (sin cambios):** D-1, D-2, D-3, D-5 (R3, conjunto (b), M-1); entidades 1–8 de P4.A; P4.1–P4.3, Q-7 = (a).
- **Recomendaciones mías pendientes (no aprobadas):** D4.a–d = A; D6.a–c = A; D7.a = A, D7.b = A, D7.c = C; D8 = A.
- **Requieren tu intervención:** esas 11; D5.a–d; entidad 9 Hallazgo; entidades 10–18; P4.B, P4.C, E1–E5; Q-1, Q-2 y demás pendientes; aprobaciones 0.1–0.7; aceptación de Fase 0; autorización de Fase 1. *[superado por decisión posterior: D5.a–d fuera del alcance vigente; ver nota superior]*

## C. Evidencias
- **Creados:** `PAQUETE_DECISION_D4_D6_D7_D8.md`, este informe, `MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt`.
- **Modificados (solo añadidos o aviso de sustitución, sin borrar historia):** `PAQUETE_DECISION_D1_D8.md`, `REGISTRO_DECISIONES_RESUELTAS.md`, `DECISIONES_P4_PENDIENTES.md`, `16_INDICE_EVIDENCIAS_FASE0.md`, `../README_ENTREGA.md`, `../MANIFEST.sha256`.
- **Manifiesto y SHA-256:** ver `MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` (ruta, nombre, tamaño, SHA-256) y `MANIFEST.sha256` del expediente completo; verificación `sha256sum -c` en el expediente: 0 fallos.
- **Repositorio de evidencias (CCI-Evidence):** **NO verificado y NO subido.** No pude confirmar por API que exista ni que sea «private»: el repositorio no está accesible en esta sesión (la API respondió 403 «no habilitado») y la solicitud de adjuntarlo con permiso de escritura fue **denegada** por el control de permisos de la sesión. Por tu regla («si no puedes confirmar que es privado, no subas»), no se subió nada, no se creó otro repositorio y no se usó el repositorio público. **Rama y commit: ninguno.**
- **Repositorio de desarrollo** (lectura, sin modificar): rama `integration/cci-fase1-1-accepted`, HEAD `ffb47bc`, árbol limpio.
- **Entrega directa:** todos los archivos van como adjuntos en el chat (paquete, informe, manifiesto, expediente completo en `.tar.gz`). Faltan: ninguno.

## D. Estado técnico
- Cambios en código: ninguno (no autorizados).
- Pruebas ejecutadas en esta entrega: ninguna. Resultados previos (162/162 unitarias, 29/29 E2E) proceden de ejecuciones anteriores y no se reverificaron.
- Limitaciones del entorno: sin acceso a CCI-Evidence; sin re-ejecución de build, CI ni `npm audit`; solo Chrome 153 verificado en el pasado.

## E. Porcentajes de avance (separados; sin global)
| Rubro | Num/Den | % | Base |
|---|---|---|---|
| Decisiones conceptuales (dependencias D-1…D-8) | 4/8 | 50 % | resueltas: D-1, D-2, D-3, D-5 |
| Entidades aprobadas (P4.A, lista A) | 8/18 | 44,4 % | definiciones mínimas aprobadas |
| Documentación | — | no calculado | no hay base verificable de ponderación de los 17 entregables |
| Pruebas | — | no calculado en esta entrega | sin ejecución nueva |
| Estado del repositorio | 0 commits, 0 cambios | — | desarrollo limpio en `ffb47bc`; evidencia no subida |

## F. Punto de detención
Me detengo. No continúo con otra dependencia, subfase ni fase. Espero tu revisión y autorización expresa. Ya indicaste que no fusionamos con la vista previa privada; lo dejo solo como registro.

> **Nota fechada 2026-11-22 (auditoría cruzada):** Refleja el estado al 12:35 (D-4/D-6/D-7/D-8 pendientes; P4.A 8/18); superado. Estado vigente y fuente: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`; P4.A vigente 9/18; D-1…D-8 resueltas en su alcance. Este documento se conserva como evidencia histórica.
