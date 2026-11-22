# 01 — Inventario de fuentes de diseño y jerarquía aplicada

**Toda conclusión de este expediente está VALIDADA CONTRA UN DISEÑO TODAVÍA NO APROBADO (Fase 0 NO ACEPTADA).**
Solo lectura. No se modificó `docs/fase0`.

## Jerarquía documental (decisión del propietario, 2026-11-21)
1. Decisiones expresas aprobadas por el propietario.
2. Especificación técnica vigente: reglas y comportamiento.
3. Matriz del modelo: estructura, entidades, campos, relaciones.
4. Registro de decisiones: asuntos pendientes / aprobados / rechazados.
Contradicción entre fuentes vigentes → se registra y se pide decisión; no se resuelve por criterio propio.

## Fuentes leídas
| # | Fuente (ruta bajo `docs/fase0/`) | Rol en la jerarquía | Estado declarado en el propio documento |
|---|---|---|---|
| F1 | `ESTADO_DOCUMENTAL_VIGENTE.md` | Estado | Fase 0 **NO ACEPTADA**; `cierre_tecnico_fase0/` VIGENTE; V26 = línea base histórica |
| F2 | `expediente_final_v26/V25_copia_integra/05_LOGS_Y_EVIDENCIAS/original_externo_v3_3/fase0_v3_3_integral.md` (SHA-256 `b5dccdc7…1c1da`, idéntico en v23, v24, v25 y v26) | Fase 0 v3.3: línea base documental (D-01…D-08, 27 tablas, 17 permisos propuestos, 5 roles) | «Aceptada como línea base documental con limitaciones» según F3; **T-01 (17 permisos) y T-02 figuran como NO APROBADA dentro de F2** |
| F3 | `ESPECIFICACION_TECNICA_G1_G5_G10.md` (v15, 5064 líneas) | Especificación técnica (reglas, R1–R9, impacto en 27 tablas) | «No aceptada ni validada técnicamente» |
| F4 | `cierre_tecnico_fase0/MATRIZ_MODELO_LOGICO_FISICO.md` | Matriz del modelo (41 tablas) | Vigente; sin equivalencia con Supabase real |
| F5 | `cierre_tecnico_fase0/REGISTRO_DECISIONES_RECOMENDADAS.csv` (21 filas) | Registro de decisiones | **0 aprobadas**; 12 RECOMENDADO_REQUIERE_APROBACION, 8 PENDIENTE_DE_INFORMACION_EXTERNA, 1 NO_RESOLUBLE_EN_FASE_0 |
| F6 | `cierre_tecnico_fase0/PROPUESTA_CONTRATO_ERRORES_R1_R9.md` | Contrato de errores R1–R9 | **NO APROBADA** (propuesta técnica) |
| F7 | `cierre_tecnico_fase0/PROPUESTA_GUARDA_DEV_PROD.md` | Entornos DEV/PROD (base de datos) | Implementada solo en local; listas de identificadores vacías |

## Observaciones del inventario
- **No existe un documento con decisiones del propietario «expresamente aprobadas»** que sea localizable como tal: el registro F5 declara 0 aprobadas. Las únicas «aprobaciones» citadas están en F2/F3 (D-01…D-08 aprobadas; «27 tablas, 17 claves físicas, 13 transiciones» como «APROBADOS / vigentes» en F3 l.34). Sin acceso a la fuente primaria de esas aprobaciones, se tratan como declaradas, no verificadas.
- Existen versiones históricas de la especificación (v2…v14) en `historico/`; **no** se usaron.
- `fase0_v3_3_integral.md` existe en 4 copias idénticas (hash igual); se leyó una.
- Alcance de lectura: F2 (secciones 4, 5, permisos, matriz de 27 tablas, roles, T-01…T-05, D-01…D-08), F3 (l.1–60, 125, 3634–3660, 1583–1596, referencias a membresía/actividad), F4 completo, F5 (columnas ID/Nombre/Estado), F6 completo, F7 (secciones 1–5). **No** se leyó íntegra F3 (937 KB) ni el resto de matrices.
