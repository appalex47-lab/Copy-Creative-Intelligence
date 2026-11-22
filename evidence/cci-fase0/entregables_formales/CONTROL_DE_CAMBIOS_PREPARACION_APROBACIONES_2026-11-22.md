# Control de cambios — regularización posterior a la ratificación y preparación de aprobaciones (2026-11-22)
> Documento de control; **no es una decisión del propietario**. Commit de partida: `f7bb7acdc9480936bf001d1e2c895093d2574844` (rama `evidence/cci-fase0-review`). Commit final: el que contiene este documento (un hash no puede constar dentro de los archivos que contiene; se informa en la entrega y se verifica por API). Un solo commit documental, solo en la rama autorizada; sin PR, sin fusión.

## 1. Interpretación del encargo
El propietario pidió, en una sola corrida, concluir lo documental posible sin nueva decisión, conciliar decisiones y entidades, rehacer las fichas 0.1–0.7, reforzar los verificadores y dejar el expediente listo para la aprobación, **sin** declarar cerrada la Fase 0, sin emitir aprobaciones y sin autorizar Fase 1. No se reabrió ninguna decisión ratificada (B1–B10) ni se atribuyó una decisión que el propietario no emitió.

## 2. Archivos creados (11)
- `auditoria_integral/14_INFORME_FINAL_REGULARIZACION_Y_PREPARACION_APROBACIONES.md`
- `entregables_formales/CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md`
- `entregables_formales/CONTROL_DE_CAMBIOS_PREPARACION_APROBACIONES_2026-11-22.md`
- `entregables_formales/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md`
- `logs/escaneo_contradicciones_2026-11-22_regularizacion.txt`
- `logs/modelo_estructural_historico_2026-11-22.txt`
- `logs/verificacion_coherencia_posterior_2026-11-22_regularizacion.txt`
- `logs/verificacion_semantica_fase0.py`
- `logs/verificacion_semantica_fase0_2026-11-22.txt`
- `logs/verificacion_semantica_fase0_prueba_mutacion_2026-11-22.txt`
- `logs/verificar_expediente_historico_2026-11-22.txt`

## 3. Archivos modificados (33), por grupo y justificación

### Índices (4)
*Justificación:* Nota fechada de estado vigente con el texto anterior conservado.
- `00_INDICE_VIGENTES_E_HISTORICOS.md`
- `README_ENTREGA.md`
- `auditoria_integral/01_INDICE_MAESTRO_FASE0.md`
- `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md`

### Informes y matrices de auditoría (6)
*Justificación:* Cifras, filas y notas; el informe ejecutivo (§2 y §4) y los registros 05, 07, 08 y 12 se actualizaron; el estado de CR no cambia.
- `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md`
- `auditoria_integral/06_REGISTRO_CONTRADICCIONES.md`
- `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md`
- `auditoria_integral/08_INFORME_INTEGRIDAD_ARCHIVOS.md`
- `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md`
- `auditoria_integral/12_REGISTRO_LECTURA_Y_LIMITACIONES.md`

### Entregables formales vigentes o subordinados (12)
*Justificación:* Alineación al alcance ratificado (B1–B10); reescritura de `APROBACIONES_FASE0.md`; el texto anterior se conserva marcado como antecedente.
- `entregables_formales/04_ARQUITECTURA_BROWSER_ONLY.md`
- `entregables_formales/05_MODELO_DOMINIO_CCI.md`
- `entregables_formales/06_MODELO_DATOS_CCI.md`
- `entregables_formales/07_DISENO_PERSISTENCIA_INDEXEDDB.md`
- `entregables_formales/08_RESPALDO_IMPORTACION_RECUPERACION.md`
- `entregables_formales/10_DEFINICION_MVP_CCI.md`
- `entregables_formales/11_ROADMAP_FASES_0_A_5.md`
- `entregables_formales/12_CRITERIOS_ACEPTACION_FASES.md`
- `entregables_formales/14_MATRIZ_RIESGOS_CCI.md`
- `entregables_formales/APROBACIONES_FASE0.md`
- `entregables_formales/CONVENCIONES_P4_5_CONDICIONES.md`
- `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md`

### Documentos históricos o subordinados (nota de vigencia) (9)
*Justificación:* Sustitución puntual de «P4.A vigente 9/18» por una frase fechada que remite al estado vigente 18/18.
- `entregables_formales/D3_FAMILIAS_DE_REGLAS.md`
- `entregables_formales/DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md`
- `entregables_formales/FICHA_P4.md`
- `entregables_formales/INFORME_CIERRE_2026-11-22_CORRECCION_DOCUMENTAL.md`
- `entregables_formales/INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md`
- `entregables_formales/INFORME_CIERRE_2026-11-22_REGLA_PERMANENTE_12_43.md`
- `entregables_formales/LISTA_ORIGINAL_18_ENTIDADES.md`
- `entregables_formales/MATRIZ_DECISIONES_PROPIETARIO.md`
- `entregables_formales/README_PROPUESTA_VIGENTE.md`

### Verificadores (2)
*Justificación:* Control semántico nuevo, escáner de contradicciones por párrafo y lista de exclusión de la salida propia; sin ocultar controles.
- `logs/scan_contradicciones.py`
- `logs/verificacion_coherencia_posterior.py`

## 4. No modificados (conservados)
`docs/fase0/` (59 archivos, idénticos a `main`), `anexos/`, las salidas anteriores de los scripts, `13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md`, el código de la aplicación, `main` y cualquier otra rama. El estado de CR-01…CR-22 no cambió.

## 5. Decisiones del propietario documentadas y recomendaciones
Las únicas decisiones documentadas son las ya registradas (B1–B10 y anteriores). Las recomendaciones del paquete (`PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md`) son **[Rec. Claude], no vinculantes**; no se convirtieron en decisiones. Limitaciones mantenidas: C-2 y C-3 abiertas; diez aplazamientos sin resolver; R-1 pendiente de respuesta (única pregunta residual).

## 6. Defectos documentales encontrados y corregidos en esta ronda
1. `APROBACIONES_FASE0.md` con prerrequisitos y un cierre desactualizados («P4 parcial», «P4.A vigente 9/18»). 2. `10_INFORME_EJECUTIVO` §2 y §4 con cifras anteriores a la ratificación. 3. `MATRIZ_CONSOLIDADA` con el rótulo «Diagnóstico y propuesta. No aprueba nada» sin marca de antecedente. 4. Descripciones más amplias que lo ratificado en `05`, `06`, `07`, `14`, `CONVENCIONES_P4_5_CONDICIONES` y `10_DEFINICION_MVP` (p. ej. cardinalidades y atributos presentados como definidos, `revision` y «si P5=sí» como abiertos, Q-4 como abierta). 5. Once notas de vigencia con «P4.A vigente 9/18». 6. Nota de vigencia en `01_INDICE_MAESTRO` con 9/18. Cada corrección conserva el texto anterior o lo marca como antecedente.

## 7. Verificaciones ejecutadas y no ejecutadas
- **Ejecutadas (sobre el árbol de trabajo):** `verificacion_semantica_fase0.py` (32/32 pruebas; 0 errores reales; prueba de mutación: 7 defectos inducidos detectados); `verificacion_coherencia_posterior.py` (0 fallos; X4 regresión 26/26; X8 125/125 filas frente al árbol); `scan_contradicciones.py` v2; herramientas históricas sobre una copia de `docs/fase0` (58/59 comprobaciones aprueban, 1 pendiente; ejecutadas sin mutaciones). Salidas en `logs/`.
- **Pendientes de ejecución tras publicar:** verificación por API, comparación con `main`, clon limpio, recálculo de manifiestos y repetición de ambos scripts (resultado en el informe de entrega).
- **No ejecutadas:** pruebas, build, E2E y CI de la aplicación; verificación técnica de Web Locks, cuotas de IndexedDB y navegadores; lectura de los anexos A/B y de los documentos del repositorio de la aplicación; `CCI-Evidence` (403).
- Limitaciones: verificación propia de la sesión, sin reproducción independiente; los archivos modificados no se releyeron completos tras la edición (se comprobaron por búsqueda y por scripts).

## 8. Comparación con `main`
`main` permanece en `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`; `docs/fase0/` es idéntico a `main`; la rama solo añade o modifica archivos bajo `evidence/cci-fase0/`.
