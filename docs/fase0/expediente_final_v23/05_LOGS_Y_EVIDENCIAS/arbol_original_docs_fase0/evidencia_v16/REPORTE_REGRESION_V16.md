# REPORTE DE REGRESIÓN V16

> **Documento HISTÓRICO (V21, 2026-11-20):** evidencia de la etapa V16–V19 conservada tal como se produjo. Sus estados de publicación («local», «sin commit», «no publicado»), cifras (p. ej. 363 casos), clasificaciones de reglas (esquema V18/V19) y números de línea corresponden a la fecha de cada documento y **no** son el estado vigente. Estado vigente y fuente de verdad de cada dato: `../expediente_final_v21/INDICE_VIGENCIA_DOCUMENTAL_V21.md` y `../expediente_final_v21/MATRIZ_CONCILIACION_V21.md`.

Estado: local, sin commit. Base: HEAD `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` (padre `ad34f1a50c6b90f9fc880a2172141c7de6b8838a`) más las ediciones locales de trazabilidad (ver INVENTARIO_HALLAZGOS_Y_CORRECCIONES_V16.md).

## 1. Resultado ejecutado (dos corridas independientes)
| Dato | Corrida 1 | Corrida 2 |
|---|---|---|
| Inicio (UTC) | 2026-11-20T00:58:20Z | 2026-11-20T00:58:20Z |
| Fin (UTC) | 2026-11-20T01:14:00Z | 2026-11-20T01:13:52Z |
| Código de salida | 0 | 0 |
| Comprobaciones | 59 / 59 aprobadas, 0 fallan, 0 pendientes, 0 omitidas | idem |
| Controles | 28 / 28 OK | idem |
| Mutaciones | 300 / 300 detectadas, 0 NO DETECTADA | idem |
| Advertencias / Traceback | 0 | 0 |
| SHA-256 de la salida íntegra | `2c79bb683b9e171abe77f9f02e4e16a3b07e8da5b69a9b648ad2eca7d3160d08` | igual |

Comparación: `cmp` byte a byte → idénticas. Salidas íntegras: `salida_verificador_corrida1.txt` y `salida_verificador_corrida2.txt` (57 053 bytes cada una).

Comando exacto (cada corrida, en un directorio propio copiado del árbol local):
`env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -I herramientas/verificar_expediente.py --dir . --v33 /home/claude/fase0_v3_3_integral.md`
Entorno: Python 3.13.18, Linux, solo biblioteca estándar, ambas corridas en paralelo.

## 2. Observación sobre los totales
Sin el archivo original v3.3 (`--v33`) el verificador da 299 mutaciones y K48 pendiente, porque la mutación M-22 solo corre con el original. Con el original, 300/300. No se forzó ninguna cifra.
La salida es idéntica a la de las corridas sobre el commit V16 (mismo SHA-256): la nota de trazabilidad no cambia ningún resultado del verificador.

## 3. Pruebas individuales
`pruebas_guarda` (9) y `pruebas_atomicidad` (20): 29/29 PASS, dos corridas idénticas (`cc2825746646a760…`). Detalle en EVIDENCIA_PRUEBAS_INDIVIDUALES_V16.md. Las demás funciones de prueba del modelo se ejecutaron individualmente en la auditoría previa sobre el commit V16 (resultados 100 % aprobados; ver tabla ahí).

## 4. Integridad (observado)
| Archivo | SHA-256 (estado local) |
|---|---|
| ESPECIFICACION_TECNICA_G1_G5_G10.md | `910cc893a4591d3f4b937def76ea60fb600edadef0c86825c703cd0153a1c6a2` |
| INFORME_CIERRE_G1_G5_G10.md | `659de030c468e71688a841c104929707547e9a1be0f0e17931c289507aee1046` |
| AUDITORIA_FINAL_G1_G5_G10.md | `254e17bf3943105857a7b1a4c42f03e0de04a6cfdfa86aca6561b9dcba879b86` |
| ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md | `b44580847cf4da0ab749706b64aee6bbe0aff8f4656d8a7191755a4c72753461` |
| REGISTRO_HISTORICO_VERSIONES.md | `f722b648479f3b5a50b5e98129cd63779660b139132503284a6fbebc3d39c797` |
| herramientas/modelo_estructural.py | `cc87236a19b924617e13346f80eb642d0dc5f0090664908d1e96d8780f4fc52a` |
| herramientas/verificar_expediente.py | `1acec85dc5e76c9e004d8f2b7ed942c94826377ff240c346bee9f2792e7a035a` |
Históricos (SHA-256 del conjunto de `sha256sum historico/*`): `6f4468243a7b34a7c9be7e436f9816f272df05df9582b443f7f8794b6c9d4f1c`, igual que en V15 y V16.
V3.3: SHA-256 calculado del archivo original `b5dccdc73a8103966ab1e1b1e84b2e7ead68cd736fba666ec71d0e790d51c1da` = esperado.
Motor y verificador: mismo SHA-256 que en V15 (`cc87236a…`, `1acec85d…`).

## 5. Distinción de evidencia
- Resultado ejecutado: verificador (documental y estructural), baterías del modelo en memoria, instrumentación individual.
- Limitación: nada se ejecutó en PostgreSQL, Supabase, RLS, concurrencia ni integración externa (ver VALIDACION_SERVICIOS_EXTERNOS_V16.md).
- Resultado inferido: ninguno se presenta como aprobado.

## Actualización V17 (tras la corrección S1)
Verificador (`--v33` con el original v3.3) sobre el árbol local, dos corridas completas: 59/59 comprobaciones, 28/28 controles, 300/300 mutaciones, 0 fallas, 0 advertencias. SHA-256 de la salida de ambas: 2c79bb683b9e171abe77f9f02e4e16a3b07e8da5b69a9b648ad2eca7d3160d08 (igual que en V16). SHA-256 de la especificación local: 334cedb7e17cb719… (prefijo). No se repitieron las pruebas individuales del modelo: el modelo y el verificador no cambiaron. Sin `__pycache__` en el repositorio. Sin commit, merge ni push.

## Actualización V18 (tras S1b, ESPEC línea 38)
- Cambio estructural de texto: una frase en la especificación (S1b); SHA-256 de la especificación local: 0e0beb78bb2923c1… (prefijo). Por tratarse de un cambio en la especificación se repitieron **las dos corridas completas** del verificador (`--v33` con el original v3.3): 59/59 comprobaciones, 28/28 controles, 300/300 mutaciones, 0 fallas, 0 pendientes; SHA-256 de la salida en ambas: 2c79bb683b9e171abe77f9f02e4e16a3b07e8da5b69a9b648ad2eca7d3160d08 (igual que V16 y V17). Salidas: `salida_verificador_V18_corrida1.txt` y `_corrida2.txt`.
- Pruebas afectadas por el cambio: ninguna del modelo (el modelo y el verificador no cambiaron). Se ejecutaron, además, las 22 funciones con resultado individual (366 casos, 0 fallos, dos salidas idénticas, SHA-256 2b856198…f2f4).
- No se repitieron pruebas con evidencia válida cuyo alcance no cambió. No hay `__pycache__` en el repositorio. Sin commit, merge ni push; sin Supabase ni despliegues.

## Actualización V19
- Elementos protegidos modificados en V19: ninguno (la especificación mantiene el SHA-256 0e0beb78bb2923c1… de V18; motor, verificador e históricos intactos). Por eso bastó **una** corrida completa del verificador integral (`--v33` con el original v3.3): 59/59 comprobaciones, 28/28 controles, 300/300 mutaciones, 0 fallas, 0 pendientes; SHA-256 de la salida 2c79bb683b9e171abe77f9f02e4e16a3b07e8da5b69a9b648ad2eca7d3160d08, idéntico a V16, V17 y V18. Salida: `salida_verificador_V19_corrida1.txt`.
- Pruebas afectadas: ninguna; no se repitieron las 22 funciones (366 casos, V18).
- Pruebas nuevas ejecutadas: ninguna (PE-01..PE-05 solo diseñadas; requieren PostgreSQL).
- No se redujeron controles ni se alteraron pruebas. Sin `__pycache__`. Sin commit, merge ni push.

## Nota V20 (2026-11-19) sobre el estado de publicación

Las expresiones «local», «no publicado» y «sin commit» de las secciones anteriores describen el estado en la fecha de cada sección (histórico, no se borra). Desde entonces V16–V19 se publicó en la rama `audit/fase0-v19-review` (commit `c6ef74be4db185ac3e4fd36810f24619e6f51fcf`); `main` sigue en V16. El trabajo V20 está en el árbol local sin commit. Estado vigente y cierre: `../expediente_final_v16_v19/`.
