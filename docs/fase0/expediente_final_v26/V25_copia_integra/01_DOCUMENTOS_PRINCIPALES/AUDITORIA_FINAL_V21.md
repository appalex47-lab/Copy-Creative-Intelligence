# AUDITORÍA FINAL V21 — DOCUMENTOS ACTIVOS, FUENTES DE VERDAD Y CONSISTENCIA

**Versión:** V21 · **Fecha:** 2026-11-20 · **Fuente:** lectura y verificación automática de todo `docs/fase0/` (rama `audit/fase0-v19-review`, base V20 `ac84133b776cc73c0cb3416e51e2767039bb5132`) · **Estado de verificación:** los 15 puntos de revisión del apartado 1 se comprueban con pruebas de la batería V21 (resultado en `REPORTE_VALIDACION_INTEGRAL_V21.md`); lo que no admite prueba automática se indica.

## 1. Alcance y puntos revisados
Se revisaron los cinco documentos activos, los 39 archivos de `expediente_final_v16_v19/` (incluidos `PE_POSTGRESQL_V20/` y todas las salidas), los 28 de `evidencia_v16/`, `historico/` (52 archivos; identidad) y `herramientas/` (identidad). Puntos del encargo y cómo se comprobaron:

| # | Punto | Cómo se comprobó | Resultado |
|---|---|---|---|
| 1 | Fechas y versiones | V21-F06 (entregables); bloques de estado | Corregido el bloque de estado (D-07) |
| 2 | Nombres de archivos | V21-F05 (todo `archivo.ext` citado existe) | Corregido 1 (D-10) |
| 3 | Rutas relativas | V21-F05 | Sin rotas |
| 4 | Referencias internas | V21-F01..F04 | Corregidas líneas de 231 reglas, 780 escenarios, 90 citas y 4 documentos (D-03..D-06) |
| 5 | Enlaces a evidencias | V21-B02, B03, C01..C03 | Sin discrepancias |
| 6 | Conteos | V21-A01, A05..A10, B01, B04, B06, C01, C02, D01 | Sin discrepancias |
| 7 | Clasificaciones | V21-A02..A04, E01, E02 | Corregido el inventario (D-01) |
| 8 | Decisiones abiertas | V21-E06, E07; registro V21 | Corregida DG-20 (D-02); ninguna inventada ni cerrada |
| 9 | Declaraciones de aprobación | V21-E05 | Ninguna declaración falsa de aceptación |
| 10 | Estados de implementación | V21-A03 | Ninguna regla afirma implementación en el producto |
| 11 | Dependencias | Registro V21 §A–C; plan de validación | Documentadas |
| 12 | Terminología | Lectura | Se unificó «Referencias»: tablas (41) y referencias de versión H/A/I/U (1148 + 32) se distinguen en la matriz de conciliación |
| 13 | Consistencia CSV ↔ Markdown | V21-B06, A07, A08 | Sin discrepancias |
| 14 | Codificación y formato | V21-G10 (BOM, CR, salto final); `REPORTE_FORMATO_Y_INTEGRIDAD.md` | Sin hallazgos |
| 15 | Integridad de archivos | Manifiesto V21 (hashlib y `sha256sum -c`) | Ver reporte |

## 2. Fuente de verdad de cada dato
| Dato | Fuente de verdad (evidencia primaria) | Documentos derivados |
|---|---|---|
| Universo de 231 reglas | Filas de definición de la especificación | Matriz de reglas |
| Clase de cada regla | `MATRIZ_FINAL_231_REGLAS_V16_V19.csv` (derivada de subclase, estado y PASS de PE-01..05; recomputada por V21-A02) | Informes, inventario |
| 780 escenarios y su veredicto | Filas `T-n` de la especificación y `MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv` | Informes |
| 366 casos | Salida cruda de `instrumentar_22_funciones_v20.py` (3 corridas) | `REGISTRO_CASOS_22_FUNCIONES_V20.csv`, matriz de pruebas |
| 63 pruebas / 14 mutaciones de PostgreSQL | `02_pruebas.sql` / `mutaciones.sh` y sus salidas (3 y 2 corridas) | Informes |
| 59 / 28 / 300 del verificador | Salida cruda del verificador (V20 ×2, V21 ×2) | Informes |
| 41 tablas | Especificación línea 38 + v3.3 original (27) | `MATRIZ_MODELO_DATOS_FINAL.md` |
| Decisiones abiertas | Especificación, registro histórico, Adenda v9 | `REGISTRO_DECISIONES_ABIERTAS_V21.md` (vigente), inventario |
| Estado de aceptación | Ninguna aceptación existe; PO-05 sin confirmar | Bloque de estado V21 |

## 3. Hallazgos de la auditoría y resolución
Ver `REGISTRO_CAMBIOS_V20_V21.md` (D-01 a D-11): 11 defectos documentales corregidos; ninguno altera una cifra de V20 (las cifras de V20 se confirmaron), sino la distribución de clases de **un** documento, números de línea, descripción de DG-20, estados de publicación y avisos de vigencia. **Defectos del motor: ninguno detectado.**

## 4. Lo que la auditoría no puede afirmar
- La lectura de las 22 funciones es indirecta (sensibilidad a mutaciones, independencia del auditor 6/6, tres corridas idénticas); no se afirma una revisión línea a línea del código.
- Clase B/A significa «ejecutada en el modelo o en el fixture», no «implementada en el producto» ni «aceptada».
- Las 153 reglas de clase D dependen de que el propietario acepte G-1, G-5 y G-10.
- No hay validación contra un esquema físico real ni contra Supabase (limitación externa, no defecto documental).
