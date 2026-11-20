# TRAZABILIDAD V15 → V16 (pendiente A)

| Concepto | Valor | Tipo de evidencia |
|---|---|---|
| Versión anterior (diseño vigente) | v15, commit `ad34f1a50c6b90f9fc880a2172141c7de6b8838a` | Observada (git) |
| V16 (corrección documental) | commit `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`, padre `ad34f1a5…`, 2026-11-19 | Observada (git log) |
| Mensaje | `docs(fase0): align active roadmap version references v16` | Observada |
| Archivos modificados por V16 | `docs/fase0/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md`, +1/−1 | Observada |
| Diferencia | línea 15: `(G-1, G-5, G-10, v5)` → `(G-1, G-5, G-10, v15)`; la referencia histórica a la v5 de la sección 4 se conserva | Observada |
| Verificación de V16 | Verificador en dos corridas sobre `git archive`: 59/59, 28/28, 300/300, salida idéntica | Ejecutada |
| Estado de aceptación | V15 y V16 sin aceptar por el propietario; G-1, G-5, G-10 sin cerrar; Fase 1 no iniciada | Declarado en los documentos |

## Entrada documental creada (local, sin commit)
| Archivo | Cambio | Motivo |
|---|---|---|
| `REGISTRO_HISTORICO_VERSIONES.md` | Sección nueva al final «Nota de trazabilidad: corrección documental V16» (identificador, commits, fecha, archivos, motivo, diferencias, verificación, limitaciones, estado) | Ningún documento activo mencionaba V16 |
| `INFORME_CIERRE_G1_G5_G10.md` | Una frase en el párrafo inicial que distingue V15 de V16 | Que el informe distinga las dos versiones |
| `AUDITORIA_FINAL_G1_G5_G10.md` | Un párrafo tras el título con la misma distinción | Idem para la auditoría |
| `ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md` | Un párrafo antes de la sección 0 (la sección 4 pasa de la línea 157 a la 159; su texto no cambió) | Idem para el roadmap |

No se tocó la especificación (identifica correctamente v15), el motor, el verificador ni los históricos. La historia de V15 no se reescribió: su entrada de registro permanece intacta.
Limitación: la nota describe V16 desde fuera; al publicarse en un commit posterior, ese commit sería otro cambio posterior a V16 (no se crea aquí). Pendiente de autorización: commit y push.

## Actualización V17
Todo cambio posterior a V16 es trabajo documental local, sin publicar: nota de trazabilidad V16 en el registro, una frase/párrafo en informe, auditoría y roadmap, la corrección S1 en la especificación (línea 3620) y esta carpeta. HEAD de referencia: 6a1af2424ef39e0960b8f7e09d4e19ec52e6f046 (sin commits nuevos). La historia de versiones no se alteró.

## Actualización V18
Cambios locales adicionales (no publicados, posteriores a V16): corrección S1b en ESPEC línea 38 (se añade attribution_discard_resolutions a la enumeración de las «catorce tablas»); nuevos archivos de evidencia `MATRIZ_SEMANTICA_REGLAS_V17.csv` (reescrito con las 13 columnas por regla), `INVENTARIO_22_FUNCIONES_V18.md`, `MATRIZ_CONSISTENCIA_S1_V18.md/.csv`, `instrumentar_22_funciones_v18.py` y sus salidas. HEAD publicado de referencia: 6a1af2424ef39e0960b8f7e09d4e19ec52e6f046; sin commits nuevos. Archivos modificados respecto del commit: ESPECIFICACION, INFORME, AUDITORIA, REGISTRO, ROADMAP (más la carpeta evidencia_v16, sin seguimiento).

## Actualización V19
Sin nuevas modificaciones de los cinco documentos activos respecto de V18 (ni de motor, verificador ni históricos). Nuevo en `evidencia_v16/`: `MATRIZ_ESCENARIOS_V19.csv`; reescrita `MATRIZ_SEMANTICA_REGLAS_V17.csv` (columnas V19). Referencia de HV-02: archivos ADDENDUM en `/home/claude/` fuera del repositorio (huellas verificadas contra el manifiesto). HEAD publicado: 6a1af2424ef39e0960b8f7e09d4e19ec52e6f046; sin commits nuevos.
