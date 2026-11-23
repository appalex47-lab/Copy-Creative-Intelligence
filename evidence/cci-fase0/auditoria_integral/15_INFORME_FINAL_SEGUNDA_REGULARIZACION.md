# Informe final — última regularización documental antes de las aprobaciones 0.1–0.7 (2026-11-22)
> Informe derivado; **no es una decisión del propietario** y no emite aprobaciones. Referencia: `bf437e4617b253929e1fb7c77bb5f70907471495`, rama `evidence/cci-fase0-review`. Detalle de cambios: `entregables_formales/CONTROL_DE_CAMBIOS_SEGUNDA_REGULARIZACION_2026-11-22.md`.

## A. Resultado ejecutivo
**Expediente listo con limitaciones expresas** para la ronda de aprobaciones 0.1–0.7. Las limitaciones son: (i) la publicación en el repositorio privado autorizado `appalex47-lab/CCI-Evidence` no fue posible (el acceso devolvió 403 y la incorporación del repositorio fue denegada; no se usó ninguna vía alternativa); (ii) no se ejecutaron pruebas, build, E2E ni CI de la aplicación; (iii) toda la verificación es de esta misma sesión, sin reproducción independiente. No se declara cerrada la Fase 0.

## B. Correcciones
Ver la tabla de `CONTROL_DE_CAMBIOS_SEGUNDA_REGULARIZACION_2026-11-22.md` §1 y §3. En síntesis: R-1 corregida y sincronizada (seis cuestiones), D5.a–d mantenidas fuera del alcance (no incluidas en R-1), `06_MODELO_DATOS_CCI.md` y los índices reclasificados, verificadores reforzados con pruebas positivas y negativas. La evidencia de relectura completa por archivo está en `logs/relectura_completa_2026-11-22_segunda_regularizacion.txt`.

## C. Pregunta R-1 (única; no bloquea 0.1–0.7)
**Redacción final:** «R-1. Confirmo que se aplazan hasta la especificación del módulo correspondiente, sin modificar D-3 ni D-5, las seis cuestiones residuales listadas: la ubicación conceptual de la familia de reglas de copy (D-3) y las cinco cuestiones residuales de D-5 (auditoría o validaciones previas; modificación de un contenido aprobado; relación con las versiones; identidad exacta del contenido aprobado; relación con los estados del flujo).»
**Cuestiones incluidas (numeración de la tabla de R-1; entre paréntesis, la numeración propia de D-5):** N.º 1 (D-3): ubicación conceptual de la familia de reglas de copy; N.º 2 (D-5 (1)): si la aprobación requiere auditoría o validaciones previas; N.º 3 (D-5 (2)): qué sucede cuando se modifica un contenido aprobado; N.º 4 (D-5 (3)): cómo se relaciona la aprobación con las versiones; N.º 5 (D-5 (4)): identidad exacta del contenido al que se aplica cada aprobación; N.º 6 (D-5 (5)): relación entre aprobación y estados del flujo.
**No reabre D-5:** no toca D-5.1 (R3), D-5.2 (conjunto (b)), D-5.3 (M-1) ni D5.a–d; una respuesta afirmativa se registra como aplazamiento aceptado, no como resolución, y no se suma a las 20 resueltas ni a las 10 aplazadas. Control automático: R2 (cada fila de la tabla contiene su cuestión; redacción final completa; ninguna frase vincula R-1 con D5.a–d sin exclusión), R3 (todo documento vigente que menciona R-1 declara las seis), R4 (el registro contiene la nota), S14 en todo el árbol no histórico.

## D. Decisiones y entidades (métricas separadas; sin porcentaje global de Fase 0)
| Concepto | Cifra |
|---|---|
| Decisiones de nivel superior resueltas | 20/30 (66,7 %) |
| Decisiones aplazadas con fase límite (P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6) | 10/30 (33,3 %) |
| Decisiones abiertas de nivel superior | 0/30 |
| Entidades con existencia y definición mínima (P4.A) | 18/18 (100 %) |
| Aprobaciones formales 0.1–0.7 emitidas | 0/7 (0 %) |
| C-2 y C-3 | abiertas como limitaciones expresas |
| D5.a–d | fuera del alcance vigente; no pendientes; no contadas como abiertas |
| R-1 | pendiente de respuesta del propietario (aplazamiento de seis subcuestiones; no suma a ninguna cifra anterior) |
Se distinguen siempre: ratificación B1–B10 (hecha), aprobaciones 0.1–0.7 (pendientes), aceptación final de Fase 0 (pendiente) y autorización de Fase 1 (pendiente, independiente).

## E. Documentación y verificaciones
- **Controles semánticos:** 59/59 pruebas positivas y negativas; sobre el árbol real, 0 errores reales (salida: `logs/verificacion_semantica_fase0_2026-11-22_segunda_regularizacion.txt`). Son pruebas sintéticas de **documentos**, no pruebas de la aplicación.
- **Prueba de mutación:** 8/8 defectos sembrados detectados (R-1 sin la cuestión (4) de D-5; R-1 sin la ubicación de reglas de copy; D5.a–d como pendientes; R-1 como resuelta; aprobaciones presentadas como emitidas; recomendación presentada como decisión del propietario; R-1 que reabre D5.c; doc 06 sin marca histórica) y control sin mutación = 0 errores (`logs/prueba_mutacion_semantica.py` y su salida). Una primera ejecución detectó 5/8; se reforzaron los controles hasta 8/8 (la primera ejecución consta en el encabezado de la salida guardada de la prueba de mutación).
- **Coherencia posterior y barrido de contradicciones:** sin fallos; `scan_contradicciones.py` v2 es un barrido de patrones (clasificación por párrafo); su única clase de alerta fuerte recae en documentos históricos protegidos de `docs/fase0/` (no modificados). Las salidas están en `logs/`.
- **Herramientas históricas** (`verificar_expediente.py`, `modelo_estructural.py`): aplican solo a `docs/fase0/` y no se reejecutaron en esta ronda; sus salidas previas se conservan.
- **Integridad y clon limpio:** ver `logs/integridad_y_clon_limpio_2026-11-22_segunda_regularizacion.txt` (hashes, tamaños, enlaces, denominadores explícitos, reproducción de verificadores desde un clon limpio local y comparación con las salidas guardadas). La reproducción desde un clon limpio con el mismo procedimiento y la misma sesión **no** es verificación independiente.
- **Relectura completa:** `logs/relectura_completa_2026-11-22_segunda_regularizacion.txt` (archivo, líneas/bytes, resultado).

## F. Repositorios
Rama `evidence/cci-fase0-review` (referencia `bf437e4`; el commit final se informa en la entrega y se verifica por API). `main` intacta; sin PR ni fusión. Destino privado `appalex47-lab/CCI-Evidence`: **no verificado** (403 y `add_repo` denegado; no se verificó visibilidad ni permiso de escritura); **no se publicó** allí y la rama de desarrollo no sustituye ese destino. La decisión sobre la vista previa privada ya la tomó el propietario: no se fusiona; se deja solo como registro.

## G. Pendientes del propietario (sin convertir recomendaciones en aprobaciones)
Aprobaciones 0.1–0.7 (0/7); respuesta a R-1; aceptación final de Fase 0; autorización independiente de Fase 1; C-2 y C-3 (abiertas como limitaciones); aplazamientos P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6 (con fase límite); alcance del respaldo en Fase 1 (B7, condicional); conceder acceso a `CCI-Evidence` si desea publicar allí.

## H. Siguiente paso
Responder en una sola intervención: «0.1 … 0.7 aprobada/rechazada/con cambios: …» y «R-1 sí/no». Las siete fichas compactas y la redacción de R-1 están en `entregables_formales/PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md`.

## No verificado
Pruebas, build, E2E y CI de la aplicación; Web Locks, cuotas de IndexedDB y compatibilidad de navegadores; anexos A/B y documentos del repositorio de la aplicación; `CCI-Evidence` (inaccesible); reproducción independiente de las verificaciones.
