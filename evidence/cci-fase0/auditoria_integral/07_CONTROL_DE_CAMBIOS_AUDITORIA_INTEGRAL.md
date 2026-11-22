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
Ver `05_INFORME_AUDITORIA_INTEGRAL.md` §4. El SHA de los commits no puede escribirse dentro de los archivos que contienen; se informa en la entrega y se verifica por API.
