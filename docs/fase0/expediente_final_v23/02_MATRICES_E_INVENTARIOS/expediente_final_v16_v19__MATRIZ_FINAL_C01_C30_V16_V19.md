# MATRIZ FINAL C01–C30 (V16–V19, cierre V20)

> **Superseded (V20, 2026-11-20):** esta matriz de 30 criterios corresponde a la pasada anterior. Su sucesora V20 `MATRIZ_ACEPTACION_V20_C01_C32.md` también es histórica; los criterios vigentes son los de V21 (`../expediente_final_v21/REPORTE_VALIDACION_INTEGRAL_V21.md`). Se conserva como histórico.

**Versión:** V20 · **Fecha:** 2026-11-19 · **Fuente:** `evidencia_v16/MATRIZ_C01_C30_V16.md` (definiciones sin modificar), `git ls-remote`, hashes, reejecuciones V20 · **Estado de verificación:** cada fila cita su evidencia; ninguna implica aceptación del propietario.

Estados permitidos: APROBADO, APROBADO CON SALVEDAD, NO APROBADO, NO VERIFICABLE, PENDIENTE DE DECISIÓN DEL PROPIETARIO, NO APLICA.

| Criterio | Estado final V20 | Evidencia y justificación |
|---|---|---|
| C01 HEAD remoto = V16 | APROBADO | `git ls-remote`: `main` y `HEAD` = 6a1af24 (V16). La rama de auditoría `audit/fase0-v19-review` = c6ef74b, independiente. |
| C02 V16 tiene como padre V15 | APROBADO | 6a1af24 → padre ad34f1a (V15). c6ef74b tiene padre 6a1af24. |
| C03 Sin divergencia inesperada | APROBADO | `main` sin commits nuevos; c6ef74b es descendiente directo de V16. |
| C04 Diff V15→V16 un solo archivo | APROBADO | Sin cambios respecto de la auditoría previa (ROADMAP, +1/−1). |
| C05 Único cambio = corrección autorizada | APROBADO | v5→v15 en la línea 15 del roadmap. |
| C06 Línea 15 identifica V15 | APROBADO | Texto intacto. |
| C07 Línea 157 conserva referencia a V5 | APROBADO | Texto histórico intacto (hoy en línea desplazada por notas añadidas). |
| C08 Inspección íntegra de documentos activos | APROBADO CON SALVEDAD | Las 231 reglas y los 780 escenarios se leyeron y clasificaron una a una (matrices V20, 780/780 con regla existente y cobertura bidireccional; 1.592 pares sin inconsistencia). Salvedades: 12 escenarios PARCIAL; 5 reglas E; equivalencia aserción↔cláusula demostrada solo en familias ADV; el resto de la prosa de la especificación se revisó por patrones y lectura dirigida, no con una lectura humana independiente. |
| C09 Auditoría de referencias de versión | APROBADO CON SALVEDAD | 1.148 referencias clasificadas (MATRIZ_REFERENCIAS_V16.csv); la detección es por patrón. |
| C10 Matriz de clasificación de referencias | APROBADO | MATRIZ_REFERENCIAS_V16.csv (normalizada a LF; contenido lógico igual). |
| C11 Sin inconsistencias activas sin resolver | PENDIENTE DE DECISIÓN DEL PROPIETARIO | HV-01, S1, S1b, fila 1270 corregidas. HV-02 queda **NO VERIFICABLE** sin confirmación expresa del propietario (ver MATRIZ_HV02_PO05_EVIDENCIA.md). |
| C12 Coherencia entre los cinco documentos | APROBADO CON SALVEDAD | Bloque de estado V20 uniforme en los cinco; cifras 231/780/41/22/366 iguales. Salvedad: coherencia verificada por verificador y lectura, sujeta a la revisión del propietario. |
| C13 Registro histórico preservado | APROBADO | Entradas anteriores intactas; solo se añadió el bloque V20. `historico/` sin cambios. |
| C14 Motor intacto | APROBADO | SHA-256 cc87236a…c52a, sin diferencia con c6ef74b. |
| C15 Verificador intacto | APROBADO | SHA-256 1acec85d…035a, sin diferencia con c6ef74b. |
| C16 Pruebas intactas | APROBADO | Viven en motor y verificador; sin cambios. |
| C17 Verificador integral ejecutado | APROBADO | Ver REPORTE_REGRESION_FINAL.md: base c6ef74b y árbol V20. |
| C18 Regresión completa o limitaciones | APROBADO CON SALVEDAD | Verificador + 22 funciones/366 casos reejecutados; sin PostgreSQL/Supabase (identificado). |
| C19 Primera ejecución independiente | APROBADO | Corrida A en copia limpia. |
| C20 Segunda ejecución independiente | APROBADO | Corrida B en copia limpia. |
| C21 Reproducibilidad | APROBADO | Salidas comparadas por SHA-256 (ver reporte). |
| C22 Pruebas no ejecutadas no contadas | APROBADO | Las pruebas externas figuran como no ejecutadas; PE-01..PE-05 solo cuentan como ejecutadas en el fixture. |
| C23 Integridad v3.3 | APROBADO | b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da. |
| C24 Decisiones y pendientes preservados | APROBADO | PO-05 y reservadas presentes (INVENTARIO_DECISIONES_ABIERTAS_FASE0.md); línea 126 del registro intacta. |
| C25 No se modificó ningún archivo en la auditoría | NO APLICA | La misión V20 autoriza ediciones documentales locales; el criterio no se redefine. |
| C26 No se creó V17 ni otro commit | NO APLICA | Existe el commit c6ef74b, creado con autorización expresa del propietario (publicación acumulada V16–V19). En V20 no se creó ningún commit. |
| C27 Sin push ni alteración de main | APROBADO CON SALVEDAD | `main` intacto (6a1af24). Existió un push autorizado de la rama de auditoría; en V20 no hubo push. |
| C28 No se integró la vista previa privada | APROBADO | No se tocó. |
| C29 No se cerraron G-1, G-5, G-10 | APROBADO | Siguen abiertos; 153 reglas D condicionadas. |
| C30 Fase 1 no iniciada ni autorizada | APROBADO | Sin cambios. |

**Resumen (conteo computado):** 22 APROBADO, 5 APROBADO CON SALVEDAD (C08, C09, C12, C18, C27), 1 PENDIENTE DE DECISIÓN DEL PROPIETARIO (C11), 2 NO APLICA (C25, C26), 0 NO APROBADO, 0 NO VERIFICABLE. C17–C21 dependen del resultado de REPORTE_REGRESION_FINAL.md.
