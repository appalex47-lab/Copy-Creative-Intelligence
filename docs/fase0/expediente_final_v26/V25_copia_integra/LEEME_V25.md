# LEEME V25 — Conciliación de controles y trazabilidad

## Relación entre versiones
- **V21:** versión del expediente técnico de origen (el contenido técnico y documental es el generado en V21).
- **V22/V23:** empaquetado en ZIP y **corrección documental del paquete** (V23 corrigió el comando de verificación del LEEME y regeneró el manifiesto).
- **V24:** corrigió observaciones documentales (identificación de versión, contexto histórico, limitaciones en el LEEME).
- **V25:** **concilia la trazabilidad de los controles de V24** (16 vs 18): cifra consolidada = 18 controles distintos, todos PASS, ejecutados en dos pasadas; más 8 verificaciones remotas aparte.

## Qué contiene
Copia autónoma del expediente V24 (con las rutas originales `00_…` a `08_…`), con una nota de conciliación añadida a 4 documentos; los 4 documentos V24 de informe/validación/matriz/publicación; la evidencia de la reconstrucción en `evidencia_reconstruccion_V25/`; y los documentos V25: `INFORME_CONCILIACION_CONTROLES_V25.md`, `MATRIZ_CONTROLES_V25.csv`, `MATRIZ_CAMBIOS_V24_V25.md`, `REPORTE_VALIDACION_V25.md` y `MANIFIESTO_SHA256_V25.txt`.

## Integridad
`MANIFIESTO_SHA256_V25.txt` cubre todos los archivos de este directorio **salvo él mismo** (un archivo no puede contener su propio hash). Verificación, desde esta carpeta: `sha256sum -c MANIFIESTO_SHA256_V25.txt`. `MANIFIESTO_SHA256_V24.txt` y `08_…/SHA256SUMS.txt` se conservan como registro histórico de V24 y ya no verifican en 3 archivos con nota V25 (esperado, ver `MATRIZ_CAMBIOS_V24_V25.md`).

## Avisos
- **V25 no constituye aceptación formal de Fase 0.** Esa decisión corresponde exclusivamente al propietario.
- **No autoriza Fase 1 ni validaciones en Supabase** (CCI-DEV/CCI-PROD no se tocaron).
- Las limitaciones técnicas se conservan: sin validación física en CCI-DEV; PostgreSQL temporal ≠ esquema aprobado (63/63 y 14/14 según la evidencia existente); 12 escenarios PARCIAL; T-409 a T-422 sin ejecución individual propia; 22 funciones validadas indirectamente; sin validación de RLS, privilegios, concurrencia real ni esquema físico aprobado; R1–R9 no ejecutado; HV-02 / PO-05 sin verificación; decisiones del propietario pendientes.
- Los textos de «no hay commit/publicación» del LEEME original son históricos (ver notas V24 en `00_LEEME/LEEME_EXPEDIENTE_V21.md`).
