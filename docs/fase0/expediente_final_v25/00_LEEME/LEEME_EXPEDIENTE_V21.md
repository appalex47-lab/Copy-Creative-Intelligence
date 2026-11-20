# LEEME — Expediente V21 de Fase 0 · Copy & Creative Intelligence (CCI)

## 1. Identificación
Proyecto: Copy & Creative Intelligence (CCI), Fase 0 (G-1, G-5, G-10). Solo documentación; no contiene código funcional del producto.

**Versiones (OBS-01, aclaración V24):**
- **Versión del expediente: V21.** El contenido técnico y documental del expediente es el generado en V21; no se cambia retrospectivamente.
- **Corrección documental del paquete: V23.** El paquete se armó por primera vez en V22 (ZIP con SHA-256 `25ac41b0…d68`); V23 corrigió únicamente la instrucción de verificación del manifiesto en este LEEME y regeneró `SHA256SUMS.txt` (ZIP `CCI_FASE0_EXPEDIENTE_V21_V23.zip`, SHA-256 `7dd5e3b8…d93f`).
- **Revisión documental actual: V24.** Corrige la identificación de versión (este apartado), contextualiza como históricas las declaraciones de los apartados 3 y 15 y precisa la presentación de limitaciones en el apartado 13. No modifica pruebas, resultados, reglas, clasificaciones, decisiones ni evidencias. Detalle en `../INFORME_CORRECCIONES_V24.md`.

## 2. Fecha y hora de generación del ZIP
2026-11-20 15:33:37 UTC (empaquetado V22; el ZIP V23 se regeneró después con la corrección del LEEME y su hash está en el apartado 1).

## 3. Origen exacto
- Repositorio: `appalex47-lab/Copy-Creative-Intelligence`, rama `audit/fase0-v19-review`.
- HEAD local al empaquetar: `ac84133b776cc73c0cb3416e51e2767039bb5132` (= commit V20 `ac84133b776cc73c0cb3416e51e2767039bb5132`).
- **El expediente V21 NO está comprometido ni publicado**: son 26 archivos modificados y 26 nuevos (carpeta `expediente_final_v21/`) en el árbol de trabajo sobre ese HEAD. Por eso no existe un SHA de commit de V21; su identidad se fija con `MANIFIESTO_EVIDENCIAS_SHA256_V21.txt` (01_) y `SHA256SUMS.txt` (08_). La rama remota está en `ac84133` (V20): **GitHub no contiene V21**.

> **Nota V24 (registro histórico):** las afirmaciones de este apartado describen el estado del expediente **en el momento de generar V21/V23** (2026-11-20, antes de cualquier publicación). Se conservan como trazabilidad y **no describen el estado actual**. Posteriormente el expediente V23 fue publicado en GitHub, rama `audit/fase0-v23-review` (commits `8be8acecffce64e2a4660383bc8d5306a303c9c1` y `8674114c69881ff1ebda3c5db1f89f2a4d6d31c6`). Esa publicación no representa aceptación formal de Fase 0. No hubo merge ni modificación de `main` (`6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`) ni de la rama V20.

## 4. `main` comprobada
`6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` (local y `git ls-remote origin`; esperado `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`). Sin cambios.

## 5. Alcance
Auditoría documental, conciliación (231 reglas, 780 escenarios, 41 tablas, 22 funciones, 366 casos, 63 pruebas PG), validación y evidencias de V16–V21. No incluye validación del esquema físico, Supabase ni Fase 1.

## 6. Estructura
- `00_LEEME/` este documento.
- `01_DOCUMENTOS_PRINCIPALES/` los 9 entregables V21 (informe, auditoría, conciliación, índice de vigencia, decisiones abiertas, reporte de validación, cambios V20→V21, anclas de línea, manifiesto V21).
- `02_MATRICES_E_INVENTARIOS/` matrices e inventarios (rutas originales con `/` sustituido por `__`).
- `03_SCRIPTS/` scripts V21 (`v21/`), herramientas protegidas sin modificar, scripts de instrumentación V16–V20 y scripts SQL/sh de PostgreSQL.
- `04_RESULTADOS_DE_PRUEBAS/` salidas crudas: V21, V20, V20 PostgreSQL y V16–V19 históricas.
- `05_LOGS_Y_EVIDENCIAS/` `arbol_original_docs_fase0/` (copia íntegra de `docs/fase0/` con sus rutas originales, incluidos los 5 documentos activos y `historico/`) y `original_externo_v3_3/`.
- `06_DIFF_Y_CONTROL_DE_CAMBIOS/` diffs V20→V21, listas de archivos, evidencia de alcance, estado de git antes y estado de ramas.
- `07_LIMITACIONES_Y_DECISIONES_PENDIENTES/` limitaciones y decisiones, con una guía de cinco estados.
- `08_INTEGRIDAD_Y_MANIFIESTOS/` `SHA256SUMS.txt`, `CORRESPONDENCIA_RUTAS_ORIGEN.csv` (ruta en el paquete → ruta original → SHA-256) e `INFORME_VERIFICACION_REPRODUCCION.md` (reproducciones hechas desde una copia del paquete). El informe de validación posterior al empaquetado se entrega **junto al ZIP, fuera de él** (un ZIP no puede contener la validación de su propio hash).

## 7. Inventario y rutas originales
`08_INTEGRIDAD_Y_MANIFIESTOS/CORRESPONDENCIA_RUTAS_ORIGEN.csv`. Varios archivos aparecen en más de una carpeta (copias organizadas y árbol original); ninguna copia fue editada.

## 8. Cómo revisar
Orden sugerido: `07_.../00_ESTADOS_DE_VERIFICACION_Y_LIMITACIONES.md` → `INFORME_FINAL_V21.md` → `MATRIZ_CONCILIACION_V21.md` → `REGISTRO_DECISIONES_ABIERTAS_V21.md` → `AUDITORIA_FINAL_V21.md` → `INDICE_VIGENCIA_DOCUMENTAL_V21.md` (qué documento es vigente, histórico o sustituido) → `REPORTE_VALIDACION_INTEGRAL_V21.md`.

## 9. Reproducción de pruebas
Comprobación de integridad del paquete (sin dependencias), desde la carpeta donde se extrajo el ZIP:

```
cd CCI_FASE0_EXPEDIENTE_V21
sha256sum -c 08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt
```

- El comando debe ejecutarse desde la raíz del expediente extraído (`CCI_FASE0_EXPEDIENTE_V21/`).
- Las rutas del manifiesto son relativas a esa raíz.
- El manifiesto no incluye su propio hash.
- El hash del ZIP final se proporciona por separado, en el reporte de entrega (la comprobación completa del ZIP se entrega aparte, junto al ZIP).

Verificador completo (≈20 min), desde `05_LOGS_Y_EVIDENCIAS/arbol_original_docs_fase0/`:
`env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -I herramientas/verificar_expediente.py --dir . --v33 ../original_externo_v3_3/fase0_v3_3_integral.md`
Las demás pruebas están descritas en `REPORTE_REGRESION_FINAL.md` (V20) y en `03_SCRIPTS/`.

## 10. Dependencias
Python 3 (stdlib), `sha256sum`; para PostgreSQL: binarios de PostgreSQL 16 y un clúster temporal (nunca CCI-DEV/CCI-PROD); la batería V21, el generador del manifiesto V21 y los controles negativos requieren además el repositorio Git original (consultan el commit V20).

## 11. Resultados reproducibles
Los que figuran en `INFORME_VERIFICACION_REPRODUCCION.md` (08_), generado al validar este ZIP. Los resultados no listados allí no se re-ejecutaron desde el ZIP.

## 12. Resultados no reproducibles desde el ZIP solo
Todo lo que requiere el repositorio Git (batería V21, controles negativos, verificación de manifiesto V21 contra `historico/` del commit V20) y PostgreSQL (63 pruebas y 14 mutaciones). Se conservan sus salidas originales en `04_`.

## 13. Limitaciones
**Pruebas sobre un fixture temporal ≠ validación física en CCI-DEV.** Lo ejecutado (PostgreSQL 16 temporal, modelo en memoria, verificador) no equivale a una validación del esquema físico real. Se conservan, sin convertirlas en PASS:
- PostgreSQL temporal: 63/63 pruebas y 14/14 mutaciones, según la evidencia existente, sobre un fixture derivado del diseño (no es el esquema aprobado).
- 12 escenarios permanecen PARCIAL.
- T-409 a T-422 no tienen ejecución individual propia.
- Las 22 funciones fueron validadas indirectamente por ejecución (sensibilidad a mutaciones e independencia del auditor), no mediante lectura línea por línea.
- No se ha demostrado validación física en CCI-DEV.
- No se han validado RLS, privilegios, concurrencia real ni el esquema físico aprobado; el trigger R1–R9 no se ejecutó.
- HV-02 / PO-05 continúa sin verificación (NO VERIFICABLE).

Resumen original (V22):
Ver `07_LIMITACIONES_Y_DECISIONES_PENDIENTES/`: sin esquema físico ni CCI-DEV; PostgreSQL temporal ≠ esquema aprobado ≠ Supabase; sin RLS, privilegios ni concurrencia; trigger R1–R9 no ejecutado; 12 escenarios PARCIAL; T-409..T-422 sin ejecución individual; 22 funciones validadas indirectamente; HV-02 NO VERIFICABLE.

## 14. Decisiones pendientes del propietario
PO-05, G-1, G-5, G-10, DG-19, DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10, OD-13 (todas abiertas).

## 15. Declaración
**Este ZIP no implica aceptación formal de Fase 0 ni autorización de Fase 1.** *Registro histórico del empaquetado V21/V23:* en ese momento no se hizo commit, push, merge ni PR; no se tocó CCI-DEV ni CCI-PROD.

> **Nota V24:** la frase anterior describe el estado al generar V21/V23, no el actual. El expediente V23 fue publicado después en GitHub (rama `audit/fase0-v23-review`), sin merge, sin PR y sin cambios en `main`. La publicación no es aceptación formal de Fase 0; esa aceptación corresponde exclusivamente al propietario. No se tocó CCI-DEV ni CCI-PROD y Fase 1 no está iniciada.
