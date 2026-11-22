# Control de cambios — registro de la ratificación de la propuesta maestra de cierre de Fase 0 (2026-11-22)
**Naturaleza:** control de cambios de hechos. **No es una decisión del propietario** ni una aprobación. Base: HEAD `bb2030a9bc88d0ac5f2603ade57f674033c7ab0c` de la rama `evidence/cci-fase0-review`.

## 1. Origen y alcance
El propietario recibió `PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md` (copia literal en este directorio; SHA-256 `8eb73476310cd98a01d8ec049ca1fd4c165758fc344fa8870b1ed532b7aa3999`; 25057 B) y respondió **«Confirmo todo»** (2026-11-22 15:56, hora de Ciudad de México). Esta ronda registra esa respuesta en el expediente y actualiza la evidencia derivada. **No** se modificó código de la aplicación, `docs/fase0/`, `main` ni la visibilidad del repositorio; no se hizo merge, PR ni deploy; no se cambió el estado de ningún CR; no se emitió ninguna aprobación.

## 2. Interpretaciones adoptadas (a validar por el propietario si no coinciden con su intención)
1. «Confirmo todo» se tomó como ratificación expresa de los bloques **B1–B10**, tal como la propuesta declara que requiere («ratificación expresa del propietario» antes de modificar el registro).
2. **B1–B9** se registraron como decisiones del propietario por su **contenido**.
3. **B10** se registró solo como ratificación del contenido propuesto para **revisar** las aprobaciones 0.1–0.7: la propia propuesta indica que ninguna aprobación formal se considera emitida por ella. Por tanto **0.1–0.7 siguen PENDIENTES (0/7)**, Fase 0 **no está aceptada** y Fase 1 **no está autorizada**.
4. Las opciones de A0-1 («(b)»), Q-4 («(a)») y P11 no coinciden de forma exacta con las letras del registro anterior o del expediente; se registraron por el contenido de la propuesta (no por letra).
5. Las «Recomendaciones iniciales» de la propuesta para P6, P8, Q-1, Q-2, Q-3, Q-5 y Q-6 **no** se registraron como decisiones; solo se registró el aplazamiento (B8).
6. C-2 y C-3 se mantienen abiertas como limitaciones expresas (B9); CR-17 conserva su estado PENDIENTE_PROPIETARIO.

## 3. Cambios por archivo
**Nuevos (3):** `entregables_formales/PROPUESTA_MAESTRA_CIERRE_FASE0_v1.0.md` (copia literal); este documento; `logs/verificacion_coherencia_posterior_2026-11-22_tras_ratificacion.txt` (salida del script, con el control V13 añadido).
**Modificados (27):**
- `README_ENTREGA.md`
- `auditoria_integral/01_INDICE_MAESTRO_FASE0.md`
- `auditoria_integral/02_MATRIZ_MAESTRA_DECISIONES.md`
- `auditoria_integral/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md`
- `auditoria_integral/04_MATRIZ_MAESTRA_DEPENDENCIAS.md`
- `auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md`
- `auditoria_integral/06_REGISTRO_CONTRADICCIONES.md`
- `auditoria_integral/07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md`
- `auditoria_integral/08_INFORME_INTEGRIDAD_ARCHIVOS.md`
- `auditoria_integral/09_PAQUETE_CONSOLIDADO_DECISIONES_PENDIENTES.md`
- `auditoria_integral/10_INFORME_EJECUTIVO_PREPARACION_CIERRE.md`
- `auditoria_integral/12_REGISTRO_LECTURA_Y_LIMITACIONES.md`
- `entregables_formales/10_DEFINICION_MVP_CCI.md`
- `entregables_formales/13_REGISTRO_DECISIONES_PROPIETARIO.md`
- `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md`
- `entregables_formales/APROBACIONES_FASE0.md`
- `entregables_formales/D3_FAMILIAS_DE_REGLAS.md`
- `entregables_formales/DECISIONES_P4_PENDIENTES.md`
- `entregables_formales/DIAGNOSTICO_INTEGRAL_18_ENTIDADES.md`
- `entregables_formales/FICHA_P4.md`
- `entregables_formales/FICHA_P4A_09_HALLAZGO.md`
- `entregables_formales/LISTA_ORIGINAL_18_ENTIDADES.md`
- `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md`
- `entregables_formales/MATRIZ_DECISIONES_PROPIETARIO.md`
- `entregables_formales/README_PROPUESTA_VIGENTE.md`
- `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`
- `logs/verificacion_coherencia_posterior.py`
Detalle: `REGISTRO_DECISIONES_RESUELTAS.md` recibió la sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)» (definiciones literales extraídas programáticamente del archivo de la propuesta) y una nota cronológica; las matrices 02/03 y la matriz consolidada se actualizaron con el estado vigente (el estado anterior se conserva marcado como antecedente superado); el informe ejecutivo (10) actualizó cifras (decisiones 20/30; entidades 18/18; aprobaciones 0/7); el resto recibió notas fechadas sin reescribir su contenido original. `MANIFEST.sha256` e `INVENTARIO_PUBLICADO.sha256` se regeneraron.

## 4. Cifras tras la ratificación (con su base)
| Indicador | Valor | Nota |
|---|---|---|
| P4.A: entidades con definición mínima aprobada | 18/18 (100 %) | antes 9/18 (antecedente superado); solo existencia y definición mínima |
| Decisiones conceptuales resueltas | 20/30 (66,7 %) | P1–P5, P9, P11–P14, Q-4, Q-7, D-1…D-8; base mixta, indicador orientativo |
| Aplazamiento aceptado (no resueltas) | 10/30 | P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6 |
| Aprobaciones 0.1–0.7 emitidas | 0/7 | |
| Aceptación de Fase 0 / autorización de Fase 1 | No aceptada / No autorizada | sin porcentaje global de Fase 0 |

## 5. Estado documental de los criterios del §18 de la propuesta (comprobación documental; no es una decisión ni una aceptación)
| Criterio | Estado |
|---|---|
| 1. P4, P5, P9, P11–P14 y Q-4 resueltas | Cumplido (por el registro) |
| 2. Entidades definidas o aplazadas/excluidas | Cumplido (18/18) |
| 3. P4.B, P4.C y P4.E con resolución explícita | Cumplido |
| 4. A0 con resolución o aplazamiento justificado | Cumplido (A0-1 y A0-3 resueltas; A0-2 diferida con justificación en B5) |
| 5. C-2 y C-3 reconocidas como limitaciones abiertas | Cumplido (B9) |
| 6. Roadmap con alcance, dependencias y criterios claros | **No verificado / pendiente:** depende de la revisión del propietario (aprobación 0.7) |
| 7. Aprobaciones 0.1–0.7 revisadas y emitidas | **Pendiente** (0/7) |
| 8. Reserva técnica X4 corregida y documentada | Cumplido (commit `bb2030a`) |
| 9. Expediente sin contradicciones conocidas no declaradas | Ver el resultado del script en `logs/verificacion_coherencia_posterior_2026-11-22_tras_ratificacion.txt` (verificación propia; sin reproducción independiente) |
Que los criterios 1–5 y 8 consten cumplidos **no** significa que Fase 0 esté aceptada: los criterios 6 y 7 siguen pendientes y la aceptación es decisión exclusiva del propietario.

## 6. Límites de la verificación
Verificación propia, sin reproducción independiente. No se ejecutaron pruebas, build, E2E ni CI de la aplicación, ni `modelo_estructural.py` ni `verificar_expediente.py`. `CCI-Evidence` sigue devolviendo 403 (no se usó ni se rodeó). El contenido técnico de las propuestas (p. ej. Web Locks, cuotas de IndexedDB) no se verificó contra el comportamiento real de los navegadores. Los adjuntos A y B y los documentos del repositorio de la aplicación no se leyeron.

## 7. Observaciones sobre la copia literal de la propuesta y sobre el script
- **§20 de la propuesta («Estado de avance: base verificable»)** describe el estado **anterior** a la ratificación (p. ej. «9/18» entidades con definición mínima aprobada, y la reserva X4 pendiente): está **superado** por el registro (18/18; X4 corregida en `bb2030a`). La copia se conserva literal (su hash consta arriba) y no se edita.
- **Control V13 (nuevo en el script):** busca «9/18», «9 de 18» o «9 aprobadas» sin marca de antecedente. Se excluyó del patrón la expresión ordinal «Entidad 9 de 18» (la entidad número 9 de las 18), que no es un conteo.
- **Falsos positivos revisados a mano en la salida del script:** (a) V6, `REGISTRO_DECISIONES_RESUELTAS.md`: el patrón «D7.c … pendiente» coincide con la palabra «independientes» del límite de la entidad 12; (b) V6, copia de la propuesta, encabezado «D6.c=A0 — Subdecisiones pendientes»: texto previo a la ratificación; (c) V7, copia de la propuesta: «guardas contra Supabase y servicios de backend», «Integraciones de backend» y «Colaboración multiusuario» figuran como **exclusiones** (guardas y elementos fuera del MVP), no como arquitectura vigente. No se modificó la copia literal por estos avisos.
- **Marcas en dos controles de cambios anteriores:** se añadió una marca inline de antecedente superado a una línea de `CONTROL_DE_CAMBIOS_REGULARIZACION_P4A_9_18_2026-11-22.md` y a una de `CONTROL_DE_CAMBIOS_CORRECCION_INTEGRAL_P4A_9_18_2026-11-22.md` (además de la nota final); el aviso V13 que persiste en la salida corresponde únicamente a la línea 547 de la copia literal de la propuesta (§20), ya explicada arriba.
- **V1 y X8:** las referencias a la nueva salida del script solo resuelven una vez creada; el archivo guardado se generó con una ejecución en la que ya existía.

