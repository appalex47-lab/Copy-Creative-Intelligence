# MATRIZ DE CONCILIACIÓN V21 — CIFRAS, CLASIFICACIONES Y EVIDENCIAS

**Versión:** V21 · **Fecha:** 2026-11-20 · **Fuente:** evidencia primaria de `../expediente_final_v16_v19/`, `../evidencia_v16/` y `salidas/`; recomputada por `scripts/v21_bateria_cierre.py` · **Estado de verificación:** cada fila está respaldada por una prueba de la batería V21 que la recalcula desde el archivo de origen (no se copiaron conteos de informes anteriores). El resultado de cada prueba está en `salidas/RESULTADOS_BATERIA_V21.tsv`.

Las cifras declaradas en V20 se **comprobaron**, no se impusieron: todas coinciden con la evidencia. Las diferencias encontradas por V21 estaban en otros lugares (clasificación en un documento, números de línea, estado de publicación) y se listan en `REGISTRO_CAMBIOS_V20_V21.md`.

## 1. Cifras centrales
| Elemento | Declarado V20 | Recomputado V21 | Archivo de origen | Script / procedimiento que lo produce | Salida de ejecución | Prueba V21 | Estado |
|---|---|---|---|---|---|---|---|
| Reglas | 231 | **231** (231 únicas; igual al conjunto de filas de definición de la especificación; familias IG1 33, IG5 116, IG10 37, IS 16, IM 12, IE 12, IP 5) | `MATRIZ_FINAL_231_REGLAS_V16_V19.csv` y especificación | `v21_bateria_cierre.py` | `salidas/salida_bateria_V21_corrida1.txt` | V21-A01 | PASS |
| Escenarios | 780 | **780** (780 únicos; igual a las filas `T-n` de la especificación): 258 demostrados por ejecución en el modelo, 510 por lectura (6 con observación), 12 parciales | `MATRIZ_FINAL_780_ESCENARIOS_V16_V19.csv` | ídem | ídem | V21-A05, A06 | PASS |
| Pares regla↔escenario | 1592 | **1592** únicos, bidireccionales, 0 huérfanos, 0 omitidos | `MATRIZ_TRAZABILIDAD_REGLAS_ESCENARIOS_V16_V19.csv` | ídem | ídem | V21-A07 | PASS |
| Referencias (tablas) | 41 | **41** = 27 base de v3.3 + 14 nuevas (10 nombradas en la línea 38 de la especificación + 4 de cambio/atribución por campo material), todas con definición | Especificación (línea 38, definiciones `####`) y v3.3 original | ídem | ídem | V21-A09 | PASS |
| Referencias de versión (H/A/I/U) | 1148 + 32 | **1148** (A 125, H 1022, U 1) + **32** (A 32), valores válidos | `../evidencia_v16/MATRIZ_REFERENCIAS_V16.csv`, `MATRIZ_REFERENCIAS_V20_SUPLEMENTO.csv` | ídem | ídem | V21-A10 | PASS |
| Funciones | 22 | **22** (instrumentadas una vez cada una) | `../herramientas/modelo_estructural.py` (SHA-256 `cc87236a…c52a`, sin modificar) | `../evidencia_v16/instrumentar_22_funciones_v20.py` | `../expediente_final_v16_v19/salida_22_funciones_V20_corrida1.txt`, `salida_22_funciones_V20_corrida2.txt`; V21: `salidas/salida_22_funciones_V21_corrida3.txt` | V21-B01, B03, B04 | PASS |
| Casos individuales | 366 | **366** claves únicas, 366 PASS, 0 FAIL, 0 SKIP; por función igual al registro y a la salida cruda | `../expediente_final_v16_v19/REGISTRO_CASOS_22_FUNCIONES_V20.csv` | ídem | 3 salidas idénticas (2 de V20 + 1 ejecutada en V21) | V21-B01..B06 | PASS |
| Pruebas PostgreSQL | 63 | **63** declaradas = 63 ejecutadas = 63 PASS, en 3 corridas idénticas | `../expediente_final_v16_v19/PE_POSTGRESQL_V20/02_pruebas.sql` | `PE_POSTGRESQL_V20/ejecutar.sh` | `salida_PE_V20_corrida1.txt` y `salida_PE_V20_corrida2.txt`; V21: `salidas/salida_PE_V21_corrida3.txt` | V21-C01, C03 | PASS |
| Mutaciones PostgreSQL | 14 | **14** declaradas, 14 detectadas en 2 corridas, 0 no aplicadas | `PE_POSTGRESQL_V20/mutaciones.sh` | `mutaciones.sh` | `salida_PE_V20_mutaciones.txt`; V21: `salidas/salida_PE_V21_mutaciones_corrida2.txt` | V21-C02 | PASS |
| Verificador (comprobaciones K) | 59 | **59** aprueban, 0 fallan | `../herramientas/verificar_expediente.py` (SHA-256 `1acec85d…035a`, sin modificar) | comando de `REPORTE_REGRESION_FINAL.md` | V20: `salida_verificador_V20_final_corrida1.txt` y `salida_verificador_V20_final_corrida2.txt`; V21: `salidas/salida_verificador_V21_corrida1.txt` y `salidas/salida_verificador_V21_corrida2.txt` | V21-D01, D02 | PASS |
| Controles del verificador | 28 | **28** OK | ídem | ídem | ídem | V21-D01 | PASS |
| Controles negativos (mutaciones del verificador) | 300 | **300** detectadas de 300 | ídem | ídem | ídem | V21-D01 | PASS |

**No se suman resultados que se solapan.** Cuatro universos distintos, sin ningún total combinado: (a) 366 casos individuales del modelo en memoria (incluye mutaciones del modelo y 3 positivos); (b) 63 pruebas de PostgreSQL, de las cuales 14 son además el objetivo de las 14 mutaciones de sensibilidad del fixture (las mutaciones no son pruebas adicionales: provocan que una de las 63 falle); (c) 59 comprobaciones K + 28 controles + 300 mutaciones del verificador documental (las 300 mutaciones son controles negativos del verificador; el verificador invoca internamente algunas de las 22 funciones, pero esas invocaciones **no** aportan casos adicionales a los 366); (d) 6 pruebas de independencia y 4 estructurales de FK de V20, no sumadas.

## 2. Reconciliación 363 / 366
Causa raíz (heredada de V20, reverificada): el script `instrumentar_22_funciones_v18.py` imprimía los 3 positivos de `correr_mutaciones_k45` (POS-01..03) pero no los contaba (total impreso 363). El total real es **366 = 363 + 3**. V21-B01 (registro), B02 (cada caso apunta a su línea real de la salida original), B03 (3 corridas idénticas) y B04 (recuento independiente de la salida cruda, por función) lo comprueban. El valor 363 solo se conserva como subtotal histórico en las salidas del script V18 (`salida_22_funciones_script_v18_conteo_363_corrida1.txt` y `…_corrida2.txt`).

## 3. Clasificación de las 231 reglas (distribución vigente)
| Clase | Significado | Cantidad |
|---|---|---|
| A | Implementada y probada en el modelo en memoria (todos los escenarios de la regla ejecutados) | **1** (IG5-105) |
| B | Parcial: probada solo en parte (modelo) o ejecutada en el fixture de PostgreSQL temporal | **8** (IG5-72, IG5-92, IG5-99 y las 5 reclasificadas) |
| C | Diseño documentado sin implementación demostrable | **69** |
| D | Condicionada por un diseño no aceptado (G-1, G-5, G-10 sin aceptación del propietario) | **153** |
| E | Evidencia insuficiente | **0** |
| | **Total** | **231** |

Derivación independiente: V21-A02 recalcula la clase de cada regla desde `Subclase_V19`, `Estado_implementacion` y los resultados PASS de PE-01..PE-05 (no desde la columna final) y coincide en las 231. **Estas clases no afirman implementación en el producto ni aceptación**: B/A significan «ejecutada en modelo/fixture». V21-A03 comprueba que ninguna fila afirma implementación.

### Trazabilidad de la clasificación V19 → V20 → V21
| Versión | A | B | C | D | E | Nota |
|---|---|---|---|---|---|---|
| V18 (columna `Clase_V18`) | 39 | 14 | 173 | — | 5 | Esquema anterior sin clase D: A incluía reglas derivadas de decisiones; las 5 E eran IG1-05, IG1-06, IG1-10, IG1-21, IG5-36 |
| V19 (distribución previa a ejecutar PE-01..PE-05, la que el inventario conservaba por error) | 1 | 3 | 69 | 153 | 5 | Introduce D (condicionada por diseño no aceptado); se reconstruye como la distribución final V20 sin las 5 reglas pasadas de E a B (B 8 − 5 = 3); el inventario la declaraba textualmente |
| V20 (columna `Clase_final_V20`) | 1 | 8 | 69 | 153 | 0 | Las 5 E pasaron a B tras ejecutarse en PostgreSQL temporal |
| V21 | 1 | 8 | 69 | 153 | 0 | **Sin cambio de clase respecto de V20.** V21 corrigió el documento que conservaba la distribución V19 (B 3, E 5) |

Las cinco reglas reclasificadas conservan definición, escenarios, evidencia (PE-01 5 pruebas, PE-02 5, PE-03 4, PE-04 5, PE-05 9; todas PASS), base e intervención requerida («ejecutar el mismo fixture contra el esquema físico en CCI-DEV cuando exista y esté autorizado»); la matriz de reglas lo conserva fila a fila y V21-A04 comprueba que no hay campos vacíos.

## 4. Documentos que reproducen clasificaciones o cifras
| Documento | Estado | Cifra de clases que contiene |
|---|---|---|
| `../expediente_final_v16_v19/INVENTARIO_DECISIONES_ABIERTAS_FASE0.md` | VIGENTE (corregido en V21) | A 1, B 8, C 69, D 153, E 0 |
| `../expediente_final_v16_v19/AUDITORIA_FINAL_FASE0_V16_V19.md` | SUSTITUIDO (aviso en el archivo) | A 1, B 8, C 69, D 153, E 0 (cifra V20, coincide) |
| `../expediente_final_v16_v19/INFORME_FINAL_V20.md` | SUSTITUIDO (aviso en el archivo) | ídem |
| `../evidencia_v16/INVENTARIO_HALLAZGOS_Y_CORRECCIONES_V16.md` y matrices CSV V17–V19 | HISTÓRICO (aviso en los `.md`) | esquema V18/V19 (A/B/C/E); no es la cifra vigente |
| `INFORME_FINAL_V21.md`, `AUDITORIA_FINAL_V21.md`, este documento | VIGENTES | A 1, B 8, C 69, D 153, E 0 |
