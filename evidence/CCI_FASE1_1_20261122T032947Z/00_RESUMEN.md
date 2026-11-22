# CCI Fase 1.1-A — Resumen (solo análisis y documentación)

**Todo validado contra un diseño todavía NO aprobado (Fase 0 no aceptada).** Sin cambios de código, tipos, fixtures ni pruebas; sin Supabase/PostgreSQL; sin commits, push, PR, merge, deploy ni vista previa.

| Resultado | Cifra |
|---|---|
| Filas de trazabilidad | 25: 7 COINCIDE · 4 DISCREPANCIA · 5 SIN_DISEÑO · 2 SIN_REPRESENTACIÓN · 2 PENDIENTE_DE_DECISIÓN · 5 NO_APLICA |
| 27 tablas base ↔ 41 de la matriz | Coinciden en nombres y cifras (27 + 14 = 41) — columnas no verificables |
| 17 permisos | 17 distintas en la fuente; **contradicción** sobre su aprobación (T-01 «NO APROBADA» en v3.3 vs «aprobados» en la especificación) |
| 5 roles | Cifra coincide; 2 de 5 claves difieren del código (`diseno`, `revisor_aprobador`) |
| R1–R9 | Reglas de base de datos (SQLSTATE propuesto `RJ001…RJ010`, no aprobado); capa distinta de `AppErrorCode` |
| Project | PENDIENTE_DE_DECISIÓN (no se asume `campaigns`) |

Estado verificado al terminar: HEAD `9950e709…` y 62 commits sobre `origin/main` sin cambio; `docs/fase0`, `evidencia/` y los tres expedientes previos intactos (hashes base); árbol idéntico al respaldo previo salvo este expediente.

Archivos: 01 inventario · 02 matriz · 03 consistencia · 04 errores R1–R9 · 05 Project · 06 brechas y decisiones · 07 limitaciones · 08 verificación final · MANIFEST.sha256.
