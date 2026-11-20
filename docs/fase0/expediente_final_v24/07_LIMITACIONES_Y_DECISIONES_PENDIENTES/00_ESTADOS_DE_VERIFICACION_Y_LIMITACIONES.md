# Estados de verificación, limitaciones y decisiones pendientes (guía de lectura del paquete)

Documento de orientación generado al empaquetar (V22). **No crea ni cambia ninguna decisión ni resultado.** La fuente de verdad son los documentos originales de este mismo directorio y de `01_DOCUMENTOS_PRINCIPALES/` (`REGISTRO_DECISIONES_ABIERTAS_V21.md`, `INFORME_FINAL_V21.md`).

## 1. Verificado (con evidencia archivada y reproducible en el entorno de origen)
- Batería de cierre V21: 46 pruebas, 46 PASS, dos corridas con TSV idénticos (`04_RESULTADOS_DE_PRUEBAS/V21/`).
- Controles negativos de la batería: 26/26 (línea base limpia + 25 defectos inyectados detectados).
- Verificador del expediente: 59/59 comprobaciones, 28/28 controles, 300/300 mutaciones, dos corridas (V21) y las de V20.
- 22 funciones del modelo en memoria: 366 casos (363 + 3 positivos K45 no contados por el script V18), tres corridas.
- PostgreSQL 16.15 **temporal**: 63/63 pruebas y 14/14 mutaciones detectadas, sobre un fixture derivado del diseño.
- Integridad SHA-256 del expediente V21 (manifiesto V21, dos métodos).

## 2. Verificado parcialmente
- **12 escenarios PARCIAL** (T-03, T-06, T-10, T-47, T-78, T-80, T-124, T-137, T-138, T-139, T-140, T-166): no demuestran toda su obligación sin esquema físico (veredicto «PARCIAL / NO DEMUESTRA TODO» en `MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv`).
- **T-409 a T-422**: sin ejecución individual propia; cubiertos por lectura.
- **Las 22 funciones**: validación indirecta (sensibilidad a mutaciones e independencia del auditor); no se afirma lectura línea a línea de su código.
- **PostgreSQL temporal**: no es el esquema físico aprobado ni Supabase.

## 3. No verificado
- Esquema físico aprobado, RLS, privilegios y concurrencia real; Supabase/Storage; PE-01..PE-05 contra el esquema real.
- Trigger de elegibilidad R1–R9 (requiere 12 tablas que el fixture no incluye): no ejecutado.
- **HV-02 / PO-05: NO VERIFICABLE** sin confirmación del propietario de que se refiere a la Adenda v9.

## 4. Pendiente de decisión del propietario
PO-05, aceptación de G-1, G-5 y G-10, DG-19 (y la PK de `channel_formats`), DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10 y OD-13. Detalle y estado en `REGISTRO_DECISIONES_ABIERTAS_V21.md` e `INVENTARIO_DECISIONES_ABIERTAS_FASE0.md`. Ninguna se marcó como aprobada.

## 5. No autorizado
Fase 1 (NO INICIADA); validación física en CCI-DEV; promoción a CCI-PROD; publicación (commit/push/merge/PR) de V21; reutilizar proyectos de RevNavigator.
