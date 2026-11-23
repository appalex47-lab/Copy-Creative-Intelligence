# Control de cambios — última regularización documental antes de las aprobaciones 0.1–0.7 (2026-11-22)
> Documento de control; **no es una decisión del propietario**. Commit de referencia: `bf437e4617b253929e1fb7c77bb5f70907471495` (rama `evidence/cci-fase0-review`). Alcance: **solo documental**; sin código de la aplicación, sin `docs/fase0/`, sin `main`, sin PR, sin fusión, sin despliegue, sin tocar la vista previa privada, sin cambiar la arquitectura. El commit final es el que contiene este documento (un hash no puede constar dentro de los archivos que contiene; se informa en la entrega).

## 1. Qué se corrigió y por qué
La revisión externa del commit `bf437e4` halló inconsistencias. Se resolvieron así (los documentos se corrigieron para reflejar las decisiones; ninguna decisión se cambió para ajustarse a un documento):
| N.º | Problema | Corrección |
|---|---|---|
| 1 | La pregunta **R-1** describía solo cinco subcuestiones y omitía la cuestión (4) de D-5 («puntos 1, 2, 3 y 5») | R-1 enumera ahora **seis** cuestiones: la ubicación conceptual de la familia de reglas de copy (D-3) y las **cinco** residuales de D-5: (1) si la aprobación requiere auditoría o validaciones previas; (2) qué sucede cuando se modifica un contenido aprobado; (3) cómo se relaciona la aprobación con las versiones; (4) la identidad exacta del contenido al que se aplica cada aprobación; (5) la relación entre aprobación y los estados del flujo. Se pide una sola confirmación de **aplazamiento** (no resolución), sin alterar D-3 ni D-5 |
| 2 | La cuestión de D-3 podía confundirse con la existencia de la familia de reglas, la separación ReglaDeMarca/ReglaComercial, las reglas por canal o una ubicación técnica | Se distingue expresamente (paquete, conciliación §2b, registro) |
| 3 | D5.a–d podían leerse como pendientes o como dependencia de D-4 / 0.1–0.7 | Se declaran **fuera del alcance vigente**, no pendientes, no contadas como abiertas, no incluidas en R-1; los registros históricos se conservan como antecedentes superados |
| 4 | `06_MODELO_DATOS_CCI.md` podía leerse como contrato de datos vigente | Bloque de clasificación (propuesta histórica, no aprobada, anterior a D-1…D-8, P4 y B1–B10), marcas sobre la tabla de campos y el resumen ER, referencia a las decisiones limitantes (B3, B2, D-1…D-8), distinción entre definición mínima y atributos/relaciones no aprobados; contenido original íntegro; índices 00 y 16 y matrices alineados |
| 5 | Los verificadores no distinguían estos conceptos o dependían de coincidencias de texto | `verificacion_semantica_fase0.py` ampliado (59 pruebas; controles S10–S14, R2–R4, D4; R-1 comprobada **fila por fila** y en su redacción final); prueba de mutación reproducible `prueba_mutacion_semantica.py` (8 defectos sembrados) |

## 2. Archivos creados (9)
- `entregables_formales/CONTROL_DE_CAMBIOS_SEGUNDA_REGULARIZACION_2026-11-22.md` (este documento)
- `auditoria_integral/15_INFORME_FINAL_SEGUNDA_REGULARIZACION.md`
- `logs/prueba_mutacion_semantica.py`
- `logs/prueba_mutacion_semantica_2026-11-22_segunda_regularizacion.txt`
- `logs/verificacion_semantica_fase0_2026-11-22_segunda_regularizacion.txt`
- `logs/verificacion_coherencia_posterior_2026-11-22_segunda_regularizacion.txt`
- `logs/escaneo_contradicciones_2026-11-22_segunda_regularizacion.txt`
- `logs/relectura_completa_2026-11-22_segunda_regularizacion.txt`
- `logs/integridad_y_clon_limpio_2026-11-22_segunda_regularizacion.txt`

## 3. Archivos modificados (27)
| Grupo | Archivos | Cambio |
|---|---|---|
| Decisión y fichas | `entregables_formales/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md`, `APROBACIONES_FASE0.md`, `CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md` | R-1 corregida (seis cuestiones); limitación de 0.3 con las seis; conciliación §2b; fichas siguen PENDIENTES (0/7) |
| Registro autoritativo | `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` | Nota fechada al final (no es decisión nueva): cuestiones residuales de D-3 y D-5, protección de D5.a–d, R-1 pendiente. Ninguna decisión ni límite de D1–D8 se altera |
| Informes y matrices | `auditoria_integral/02`, `04`, `09`, `10`, `14`, `05`, `07`, `08`, `12` | Notas fechadas de alineación; en 14 y 10 se corrige la descripción de R-1; en 05/07/08/12 cifras, filas y registro |
| Documentos subordinados | `entregables_formales/05_MODELO_DOMINIO_CCI.md`, `11_ROADMAP_FASES_0_A_5.md`, `D3_FAMILIAS_DE_REGLAS.md`, `DECISIONES_P4_PENDIENTES.md`, `FICHA_P4.md`, `MATRIZ_DECISIONES_PROPIETARIO.md` | Notas fechadas: la ubicación de la familia de reglas de copy sigue sin fijarse (cuestión residual de R-1) |
| Modelo de datos | `entregables_formales/06_MODELO_DATOS_CCI.md` | Clasificación como propuesta histórica no aprobada (contenido original conservado) |
| Índices | `00_INDICE_VIGENTES_E_HISTORICOS.md`, `README_ENTREGA.md`, `auditoria_integral/01_INDICE_MAESTRO_FASE0.md`, `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md` | Tabla «Clasificación de documentos con riesgo de confusión»; notas de la segunda regularización |
| Control previo | `entregables_formales/CONTROL_DE_CAMBIOS_PREPARACION_APROBACIONES_2026-11-22.md` | Nota fechada que corrige la descripción de R-1 de esa ronda (texto original conservado) |
| Verificadores | `logs/verificacion_semantica_fase0.py`, `logs/verificacion_coherencia_posterior.py` | Controles nuevos; nombres de las nuevas salidas en la lista de exclusión |
| Integridad | `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256` | Regenerados |

## 4. Preservado sin cambios
`docs/fase0/` (59 archivos), `anexos/`, `main`, el código de la aplicación, el estado de CR-01…CR-22, el texto de las decisiones D1–D8 y B1–B10, las salidas anteriores de los scripts, `13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md` y los documentos históricos (solo notas fechadas en los listados arriba).

## 5. Lo que no se hizo
No se emitió ninguna aprobación (0.1–0.7 = 0/7); no se aceptó Fase 0; no se autorizó Fase 1; no se reabrió D5.a–d ni ninguna decisión ratificada; no se decidieron C-2 ni C-3; no se publicó en `CCI-Evidence` (el acceso devolvió 403 y la incorporación del repositorio fue denegada; no se usó ninguna vía alternativa ni la rama de desarrollo como sustituto).

> **Nota fechada 2026-11-22 20:14 (respuesta del propietario; no es decisión nueva de este documento):** el propietario emitió las aprobaciones 0.1–0.7 (7/7; la 0.5 solo en cuanto a principios, con P8 sin resolver y sin ninguna integración aprobada) y respondió «sí» a R-1 (aplazamiento aceptado de las seis cuestiones residuales, no resolución). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «0/7», «PENDIENTES» o «R-1 pendiente» describen el estado previo y quedan superadas en ese punto; el resto del texto no se altera. **La aceptación formal de Fase 0 y la autorización independiente de Fase 1 siguen PENDIENTES.** Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.
