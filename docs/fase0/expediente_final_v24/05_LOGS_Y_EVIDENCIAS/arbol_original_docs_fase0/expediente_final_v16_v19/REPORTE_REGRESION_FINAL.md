# REPORTE DE REGRESIÓN FINAL (V20)

**Versión:** V20 · **Fecha:** 2026-11-20 (inicio de las corridas finales 2026-11-20T06:24:49Z) · **Fuente:** salidas archivadas en este directorio · **Estado de verificación:** ejecutado; salidas comparadas por SHA-256 sobre los archivos reales. Todo en memoria/documental, más el fixture PostgreSQL temporal; sin esquema físico real ni Supabase.

Entorno: Linux, Python 3.13.18, PostgreSQL 16.15 (clúster temporal), `env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -I …`; copias limpias del mismo árbol en directorios independientes, corridas en paralelo.

| Prueba | Comando (resumen) | Casos / PASS / FAIL / SKIP | Exit | Duración | SHA-256 de la salida |
|---|---|---|---|---|---|
| Verificador completo, base c6ef74b | `verificar_expediente.py --dir . --v33 fase0_v3_3_integral.md` | 59 / 59 / 0 / 0; 28 controles OK; 300 mutaciones detectadas | 0 | ~15 min | 2c79bb683b9e171abe77f9f02e4e16a3b07e8da5b69a9b648ad2eca7d3160d08 (= histórico V19) |
| Verificador completo, corrida final A (árbol V20) | ídem | 59/59, 28/28, 300/300; 0 fallas, 0 omitidas | 0 | 1.028 s | f71e2c3e3bb0fdcbb3157ada0bf1589114183f22e8c29cd02e7ba642b1a51c59 |
| Verificador completo, corrida final B | ídem | ídem | 0 | 1.024 s | f71e2c3e3bb0fdcbb3157ada0bf1589114183f22e8c29cd02e7ba642b1a51c59 |
| 22 funciones, corrida 1 y 2 | `instrumentar_22_funciones_v20.py herramientas <spec>` | 366 / 366 / 0 / 0 | 0 | <1 min | f683969f6b8ecd3d38ccbb2a1397abaf7cb9cfd4948ccecfa18aedfcd8316d9d |
| Independencia motor/auditor | `independencia_auditor_v20.py herramientas` | 6 / 6 / 0 / 0 | 0 | <1 min | ver `salida_independencia_auditor_V20.txt` |
| Estructural de FK | `pruebas_estructurales_v20.py <spec>` | 4 / 4 / 0 / 0; contra la spec de c6ef74b: 0/4 (**debe fallar**; detecta las 7 columnas) | 0 / 1 | <1 s | ver archivos `salida_pruebas_estructurales_V20*.txt` |
| PostgreSQL temporal (PE, canales, resoluciones) | `PE_POSTGRESQL_V20/ejecutar.sh` ×2 | 63 / 63 / 0 / 0 | 0 | segundos | 1e56d06637ab1ad18cd07e8e357f909390793a593f3c8bb55862dece3e83509e (ambas corridas idénticas) |
| PostgreSQL: sensibilidad | `mutaciones.sh` | 14 mutaciones, 14 detectadas | 0 | segundos | `salida_PE_V20_mutaciones.txt` |

## Comparaciones
- Corridas A y B del verificador: **diferencia = 0 líneas** (hash idéntico).
- Frente a la evidencia histórica V19 (`salida_verificador_V19_corrida1.txt`): difieren **solo 3 líneas**, todas esperadas por las relaciones añadidas en V20: K14 (65→67 relaciones), K26 (34→36 aristas), K44 (117→126 relaciones). Ninguna otra línea cambia; el resultado global es el mismo (59/59, 28/28, 300/300).
- 22 funciones: los 366 resultados individuales son idénticos byte a byte a los de V18 (la única diferencia es la línea TOTAL, 363 → 366, por la corrección del conteo).
- La salida con el script V18 (363) se conserva como `salida_22_funciones_script_v18_conteo_363_corrida*.txt`.

## Suites históricas (descubiertas en la salida real, no supuestas)
K01–K59 (58 identificadores distintos en la salida), A01–A65, FK01–FK41, CHAIN-01–24, ATTR-01–12, K56-M01–12, M01–M27 (mutaciones de motor), y dentro de las 22 funciones: K47-M/R/A, K45-M01–27 + POS-01–03, ADV1–ADV16, P01–P26, ADVC-01–24, AT14-01–11, E14-01–06, AV/CF/AC, AP-01–08, ADV15-01–08, AT15-01–08 y pruebas de guarda/atomicidad. Todas aprueban; ninguna se eliminó. Identificadores repetidos entre familias (p. ej. 01–09 de guarda y atomicidad; CF-01..08 del modelo frente a PG-CF-01..15 de PostgreSQL) son casos distintos con función distinta, no duplicados.

## Integridad tras las pruebas
Motor, verificador y `historico/` sin cambios (`git diff` vacío frente a c6ef74b); sin `__pycache__`; v3.3 recalculada.

## No ejecutado
RLS, concurrencia, Supabase, despliegue y SQL contra un esquema físico real (solo existe el fixture de `PE_POSTGRESQL_V20`).
