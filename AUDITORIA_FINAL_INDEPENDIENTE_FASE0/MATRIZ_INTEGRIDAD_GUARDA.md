# Matriz de integridad de la guarda (cada fila × los 6 scripts; árbol corregido vs rama publicada)
| Caso | Descripción | Scripts | Estados (corregido) | Estados (publicada) | Esperado | Observado (corregido) |
|---|---|---|---|---|---|---|
| INT-01 | guarda ausente | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA\|ABORTA | [('ABORTA:archivo', 6)] |
| INT-02 | guarda vacía (0 bytes) | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-GUARDA-NO-EJECUTADA | [('RECHAZA:G-GUARDA-NO-EJECUTADA', 6)] |
| INT-03 | guarda sólo comentario | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-GUARDA-NO-EJECUTADA | [('RECHAZA:G-GUARDA-NO-EJECUTADA', 6)] |
| INT-04 | guarda truncada antes del bloque DO | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-GUARDA-NO-EJECUTADA | [('RECHAZA:G-GUARDA-NO-EJECUTADA', 6)] |
| INT-05 | guarda truncada a mitad del bloque DO (sintaxis rota) | 6 | {'PASS': 6} | {'PASS': 6} | ABORTA | [('ABORTA:rc=3', 6)] |
| INT-06 | guarda con SÓLO el marcador final (guarda sustituida que forja el marcador) | 6 | {'PARTIAL': 6} | {'PARTIAL': 6} | (?!RECHAZA\|ABORTA:archivo) (límite estructural: sin hash ext | [('SIN_GUARDA_EJECUTO', 5), ('ABORTA:rc=3', 1)] |
| INT-07 | guarda con SÓLO la primera línea del bloque (marcador inicial) | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-GUARDA-NO-EJECUTADA | [('RECHAZA:G-GUARDA-NO-EJECUTADA', 6)] |
| INT-08 | guarda sustituida por otro SQL inocuo (select 1;) | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-GUARDA-NO-EJECUTADA | [('RECHAZA:G-GUARDA-NO-EJECUTADA', 6)] |
| INT-09 | guarda con orden alterado: marcador creado ANTES de las comprobaciones y destino desconocido | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| INT-10 | allowlist modificada (añade el destino): 01_inventario_esquema_SOLO_LECTURA | 6 | {'PARTIAL': 6} | {'PARTIAL': 6} | PASA (tamper no detectable sin hash externo) | [('PASA', 6)] |
| INT-11 | denylist con el destino + allowlist: PROD gana: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-PROD-RECHAZADO | [('RECHAZA:G-PROD-RECHAZADO', 6)] |
| INT-12 | denylist VACIADA (tamper) sobre un destino que era PROD: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PARTIAL': 6} | {'PARTIAL': 6} | PASA (tamper no detectable sin hash externo) | [('PASA', 6)] |
| X-01 | -f ruta absoluta desde otro cwd | 6 | {'PASS': 6} | {'PASS': 6} | PASA\|RECHAZA | [('PASA', 6)] |
| X-02 | -f ruta relativa desde el directorio del script | 6 | {'PASS': 6} | {'PASS': 6} | PASA\|RECHAZA | [('PASA', 6)] |
| X-03 | -f ruta relativa desde otro directorio | 6 | {'PASS': 6} | {'PASS': 6} | PASA\|RECHAZA | [('PASA', 6)] |
| X-04 | stdin desde el directorio de los scripts (guarda real junto) | 6 | {'PASS': 6} | {'PASS': 6} | PASA\|RECHAZA | [('PASA', 6)] |
| X-05 | stdin desde un directorio SIN guarda | 6 | {'PASS': 6} | {'PASS': 6} | ABORTA | [('ABORTA:archivo', 6)] |
| X-06 | stdin con guarda homónima VACÍA en el cwd | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-GUARDA-NO-EJECUTADA\|ABORTA | [('RECHAZA:G-GUARDA-NO-EJECUTADA', 6)] |
| X-07 | stdin con guarda homónima FORJADORA en el cwd (stdin no soportado) | 6 | {'PARTIAL': 2, 'PASS': 4} | {'PARTIAL': 2, 'PASS': 4} | (?!RECHAZA) (límite: no usar stdin) | [('ABORTA:archivo', 4), ('SIN_GUARDA_EJECUTO', 2)] |
| X-08 | --single-transaction: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | PASA\|RECHAZA\|ABORTA | [('PASA', 6)] |
| X-09 | -v ON_ERROR_STOP=0 con DEV y listas vacías: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| X-10 | guarda vacía + marcador PREINSTALADO por PGOPTIONS cci.guarda_ok=1: 01_inventario_esquema_SOLO_ | 6 | {'PASS': 6} | {'FAIL': 6} | RECHAZA:G-GUARDA-NO-EJECUTADA | [('RECHAZA:G-GUARDA-NO-EJECUTADA', 6)] |

**Qué garantiza el marcador `pg_temp.cci_guarda_ok`:** que el bloque `DO` de *esta* guarda llegó a su última línea (ausente/vacía/truncada/de otra versión ⇒ rechazo; X-10: no preinstalable por PGOPTIONS). **Qué NO garantiza:** autenticidad. Una guarda sustituida que cree la tabla (INT-06), o con allowlist editada (INT-10) o denylist vaciada (INT-12), pasa; también stdin con guarda homónima forjadora (X-07). Esos casos son **PARTIAL = limitación estructural**, no aprobaciones.
**AUD-G2 (pin de hash):** el pin vive hoy en documentos del propio repositorio ⇒ **no es independiente**. El mecanismo de ejecución (`psql`) no lo verifica. Se añadió `ejecutar_script_verificado.sh <sha256_aprobado> <script> …` (GD-18a-f: hash distinto, guarda manipulada o sustituida o ausente ⇒ no ejecuta) que verifica contra un hash aprobado **externo** y fuerza `-f` con ruta absoluta; protege sólo a quien lo usa. Quién puede modificar el hash externo: quien custodie el registro de aprobación del propietario (fuera del repo, no definido aún ⇒ decisión pendiente). Mitigación documental ≠ garantía técnica.
**Contextos de ejecución:** `-f` absoluta/relativa/otro directorio (X-01..03) usan siempre la guarda junto al script; stdin usa el cwd (X-04..07); `--single-transaction`, `ON_ERROR_STOP=0` (X-08/09) no eluden. Versión anterior de la guarda (marcador GUC) con scripts nuevos o al revés ⇒ no pasan (marcador distinto); el orden alterado (marcador antes de las comprobaciones, INT-09) no deja marcador porque el DDL del bloque se revierte al fallar.
