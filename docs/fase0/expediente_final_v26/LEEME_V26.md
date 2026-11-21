# LEEME V26 — Auditoría integral, correcciones y cierre de trazabilidad

**Fecha:** 2026-11-20 (fecha local, America/Mexico_City; las salidas remotas llevan su sello en UTC) · **Rama:** `audit/fase0-v26-review` · **Base:** `audit/fase0-v25-review`, HEAD de publicación `c3adaf97588ce3b8fef075a44aff6336f4e8c266` (commit del expediente V25 `f235768135175ce3fcd9405a3a4d3a3a68311d3e`).

**V26 no constituye aceptación formal de Fase 0** (corresponde exclusivamente al propietario), no autoriza Fase 1 (NO INICIADA) y no toca Supabase, CCI-DEV ni CCI-PROD.

## 1. Relación entre versiones (estado histórico de cada una)
- **V21:** expediente técnico de origen (contenido técnico y documental generado en V21: 231 reglas, 780 escenarios, 22 funciones, verificador, batería, PostgreSQL temporal).
- **V22/V23:** empaquetado en ZIP y corrección documental del paquete (V23 corrigió el comando de verificación del LEEME y regeneró el manifiesto).
- **V24:** corrigió observaciones documentales (identificación de versión, contexto histórico de las afirmaciones, limitaciones en el LEEME).
- **V25:** concilió los controles de V24 (16 vs 18): 18 controles distintos en dos pasadas, más 8 verificaciones remotas aparte.
- **V26:** auditoría integral de V25, resolución de RV07, matriz única de controles, correcciones documentales (por errata y mapas, sin alterar copias históricas) y cierre de trazabilidad.

## 2. Estado histórico frente al estado actual de publicación
Los documentos de V21 a V25 conservados en `V25_copia_integra/` describen **el estado en su fecha** (por ejemplo, «sin commit» en el LEEME V21 es histórico). El **estado actual de publicación** es el de la rama `audit/fase0-v26-review` en GitHub; su verificación remota posterior al push se registra en `REPORTE_PUBLICACION_V26_GITHUB.md`, fuera de este expediente. `V25_copia_integra/` y `V25_publicacion/` son **copias** de los archivos de la rama V25 (no son los originales de esa rama).

## 3. Qué contiene
- `V25_copia_integra/`: copia byte a byte de los 275 archivos de `expediente_final_v25` (rutas `00_…` a `08_…` y documentos V24/V25). Se conserva sin cambios para que sus manifiestos sigan verificando.
- `V25_publicacion/REPORTE_PUBLICACION_V25_GITHUB.md`: copia del reporte de publicación V25 (estaba fuera del expediente V25).
- Documentos V26: `INFORME_AUDITORIA_FINAL_V26.md`, `INFORME_CONCILIACION_CONTROLES_V26.md`, `MATRIZ_CONTROLES_V26.csv`, `EJECUCIONES_CONTROLES_V26.csv`, `MATRIZ_CAMBIOS_V25_V26.md`, `REPORTE_VALIDACION_V26.md`, `REPORTE_VERIFICACION_REMOTA_V26.md`, `MAPA_REFERENCIAS_V26.csv`, `MANIFIESTO_SHA256_V26.txt`.
- `evidencia_reconstruccion_V26/`: scripts, salidas crudas, restos recuperados de V25 y comparaciones para reproducir todo.

## 4. Cifras de conciliación (únicas para todos los documentos V26)
<!-- CONCILIACION:INICIO -->
| Concepto | Valor |
|---|---|
| Total de controles únicos | 94 |
| Total de ejecuciones | 238 |
| Controles PASS | 85 |
| Controles FAIL | 0 |
| Controles BLOCKED | 0 |
| Controles NOT VERIFIED | 5 |
| Controles PARTIAL | 4 |
| Ejecuciones PASS | 236 |
| Ejecuciones FAIL | 1 |
| Ejecuciones BLOCKED | 0 |
| Ejecuciones NOT VERIFIED | 0 |
| Ejecuciones PARTIAL | 1 |
<!-- CONCILIACION:FIN -->

Controles únicos = filas de la matriz. Ejecuciones = corridas con salida cruda archivada (una repetición de un control es una ejecución, no otro control). Las 4 declaraciones sin evidencia (D10, D11 y RV07 de V25) no se cuentan. El detalle por categoría está en el informe de conciliación.

## 5. Integridad
`MANIFIESTO_SHA256_V26.txt` cubre todos los archivos de este directorio **salvo él mismo** (un archivo no puede contener su propio hash). Verificación desde esta carpeta: `sha256sum -c MANIFIESTO_SHA256_V26.txt`. Los manifiestos históricos dentro de `V25_copia_integra/` se conservan: el de V25 verifica 274/274 desde esa carpeta, `08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt` verifica 252/252 y el de V24 falla exactamente en los 3 archivos que V25 anotó (esperado).

## 6. Limitaciones técnicas que permanecen
- **12 escenarios PARCIAL:** T-03, T-06, T-10, T-47, T-78, T-80, T-124, T-137, T-138, T-139, T-140, T-166 (controles L01).
- **T-409 a T-422** sin ejecución individual propia (L02).
- **22 funciones** validadas indirectamente (sensibilidad a mutaciones e independencia del auditor), no por lectura línea a línea (L03).
- **PostgreSQL temporal:** 63/63 pruebas y 14/14 mutaciones según la evidencia existente (HT05, HT06), sin equivalencia con el esquema físico aprobado (L04).
- **Sin validación física en CCI-DEV** (L05); sin validación real de **RLS, privilegios ni concurrencia** (L06).
- **R1–R9** (trigger de elegibilidad) no ejecutado (L07).
- **HV-02 / PO-05** sin verificación (L08).

## 7. Decisiones pendientes del propietario
PO-05, G-1, G-5, G-10, DG-19, DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10 y OD-13 (detalle en `V25_copia_integra/07_LIMITACIONES_Y_DECISIONES_PENDIENTES/INVENTARIO_DECISIONES_ABIERTAS_FASE0.md`). V26 no convierte ninguna en decisión aprobada.

## 8. Qué no hace V26
No modifica `main`, V20, V23, V24 ni V25; no hay PR, merge ni force push; no cambia código funcional, resultados, clasificaciones ni decisiones; no toca Supabase; no inicia Fase 1.
