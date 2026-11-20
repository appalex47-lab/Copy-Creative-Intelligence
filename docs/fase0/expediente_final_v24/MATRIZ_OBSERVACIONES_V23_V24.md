# MATRIZ DE OBSERVACIONES V23 → V24

| ID | Observación (V23) | Archivo y sección | Corrección V24 | Evidencia de verificación | Estado |
|---|---|---|---|---|---|
| OBS-01 | Indicaba «Versión: V21 (empaquetado V22)», sin distinguir expediente, corrección del paquete y revisión actual | `00_LEEME/LEEME_EXPEDIENTE_V21.md` §1 (y §2) | Tres versiones diferenciadas: expediente V21; corrección documental del paquete V23; revisión actual V24. El expediente V21 no se renombra ni se altera retroactivamente | Control «OBS-01» de `REPORTE_VALIDACION_V24.md` | PASS |
| OBS-02 | §3 y §15 afirmaban ausencia de commit/push/publicación, que parecía el estado actual | LEEME §3 y §15 | Se conserva el texto histórico y se añade nota: describe el estado al generar V21/V23; V23 se publicó después en `audit/fase0-v23-review`; no es aceptación formal; sin merge ni cambios en `main` | Controles «OBS-02 §3» y «OBS-02 §15» | PASS |
| OBS-03 | Diferenciar pruebas sobre fixture temporal de validación física en CCI-DEV y conservar 7 limitaciones | LEEME §13; `07_…/00_ESTADOS_DE_VERIFICACION_Y_LIMITACIONES.md`; `INFORME_FINAL_V21.md` | Los documentos de limitaciones ya lo cumplían (sin modificar). LEEME §13 ampliado con las 7 limitaciones explícitas, sin convertirlas en PASS | Controles «OBS-03» (LEEME y documentos de limitaciones) | PASS |

Resultado: 3/3 observaciones resueltas. La publicación no equivale a aceptación formal de Fase 0 ni a autorización de Fase 1.
