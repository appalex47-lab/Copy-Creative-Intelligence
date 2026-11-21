# Informe de auditoría adversarial de operadores PostgreSQL — Fase 0 CCI

Rama local `audit/fase0-operadores-cierre` · código evaluado `2c516414ebc3271b166a2ebc1d1079618002883e` · ejecución `CCI-RUN-20261121T232214Z-422150a8` · base de partida `120c89fc020e63b8f63c7d6dbe0bcca588bd8d59` (último commit de código previo: `404f5adc69d6db4b30ceae79912fd3a9ef533cce`).

## 1. Conclusión
**El riesgo existía y se demostró con ejecución real.** El blindaje `search_path = pg_catalog, public, pg_temp` NO impedía que un operador con firma más específica definido en `public` sustituyera al de `pg_catalog`: con la guarda del commit 404f5adc, operadores de firma más específica en `public` (p. ej. `= (oid, regnamespace)`) fueron invocados por los scripts 01, 02, 03, 04 (ejecución real, `HIJACK-OP` emitido por el servidor), y la variante silenciosa (E-01) ejecutó una función auxiliar con efecto lateral y devolvió el valor correcto sin que el script fallara. Además se demostró de extremo a extremo (P-11) que un operador **autorizado** con un CREATE residual en `public` puede plantar el operador y secuestrar la siguiente ejecución, y que la guarda anterior no comprobaba privilegios efectivos (CREATE heredado/por PUBLIC/por propiedad, membresías NOINHERIT de roles privilegiados, otros roles con CREATE).

La premisa «SPD7 = 0 secuestros» era cierta pero no concluyente: SPD7 sólo probaba homónimos con la firma exacta de pg_catalog, que pierden por el orden del `search_path`.

## 2. Correspondencia de scripts
| Archivo | Papel | Sujeto al control de operadores |
|---|---|---|
| `00_guarda_destino.sql` | guarda (DO block; `search_path` local `pg_catalog, pg_temp`) | contiene los controles; sus operadores se resuelven con el `search_path` del bloque (sin `public`) |
| `00_preflight_guarda.sql` | verifica el SHA-256 externo y ejecuta la guarda | vía guarda |
| `00_verificar_marcador.sql` | marcador por ejecución | `search_path` local `pg_catalog, pg_temp` |
| `04_lib_clasificador.sql` | biblioteca incluida por 04 | vía 04 |
| **01_inventario_esquema_SOLO_LECTURA.sql** | script 1 de 6 | sí (secuestrado en VULN) |
| **02_rls_privilegios_SOLO_LECTURA.sql** | script 2 de 6 | sí (secuestrado en VULN) |
| **03_pruebas_rls_ROLLBACK.sql** | script 3 de 6 | sí (secuestrado en el barrido B-02) |
| **04_trigger_r1_r9_ROLLBACK.sql** | script 4 de 6 | sí (secuestrado en B-01/C-01) |
| **05_concurrencia_sesion_A.sql / _B.sql** | scripts 5 y 6 de 6 | ejecutados en cada barrido; sin secuestro observado con las firmas probadas (no se afirma que no existan otras) |

Los «seis scripts» son 01, 02, 03, 04, 05A y 05B; los archivos `00_*` y `04_lib_*` son la cadena de guarda/biblioteca incluida por ellos.

## 3. Ataques probados (VULN = guarda del commit 404f5adc, **idéntica byte a byte**: True, SHA-256 `007279eeda3956ba522a9827bc8b78eac1c5abb26a1da80407eff27516a68d86`; NEW = guarda actual)
| Caso | Categoría | Descripción | VULN (guarda 404f5adc): scripts secuestrados | NEW: ataques ejecutados | NEW: rechazo | Estado |
|---|---|---|---|---|---|---|
| A-01 | A homónimos exactos en public | operadores con la MISMA firma que los de pg_catalog creados en public | ninguno | 0 | G-OPERADOR-AJENO-EN-SEARCH-PATH | PASS |
| B-01 | B firma más específica | = (oid, regnamespace) y variantes con tipos reg* en public | 01, 02, 04 | 0 | G-OPERADOR-AJENO-EN-SEARCH-PATH | PASS |
| B-02 | B firma más específica | BARRIDO: 8 operadores × 16×16 tipos en public (2048 firmas por base) | 01, 02, 03 | 0 | G-OPERADOR-AJENO-EN-SEARCH-PATH | PASS |
| C-01 | C conversión implícita | operadores cuyas firmas sólo coinciden tras conversiones implícitas de los operandos de los scripts | 04 | 0 | G-OPERADOR-AJENO-EN-SEARCH-PATH | PASS |
| D-01 | D tipos personalizados | tipo compuesto y dominio en public con operadores propios + casts implícitos de usuario | ninguno | 0 | G-OPERADOR-AJENO-EN-SEARCH-PATH | PASS |
| E-01 | E función auxiliar | = (oid, regnamespace) que ejecuta una función auxiliar con efecto lateral y devuelve el resultado CORRECTO (el script no falla: ataque silencioso) | 01, 02 | 0 | G-OPERADOR-AJENO-EN-SEARCH-PATH | PASS |
| K-01 | K operador empaquetado como extensión | extensión HOSTIL cci_evilext instalada en public con = (oid,regnamespace): el origen 'extensión' no lo hace confiable cuando el símbolo es estándar | 01, 02 | 0 | G-OPERADOR-AJENO-EN-SEARCH-PATH | PASS |
| K-02 | K extensión legítima | btree_gist (necesaria para las exclusiones de CCI) instalada en public: la guarda la acepta y los 6 scripts conservan su comportamiento | ninguno | 0 | - | PASS |

Firmas que se ejecutaron realmente contra VULN: 01: ['HIJACK-OP = oid regnamespace public', 'HIJACK-OP ext = oid regnamespace', 'HIJACK-OP-AUX efecto lateral ejecutado'], 02: ['HIJACK-OP = oid regnamespace public', 'HIJACK-OP ext = oid regnamespace', 'HIJACK-OP-AUX efecto lateral ejecutado'], 03: ['HIJACK-OP || name name public'], 04: ['HIJACK-OP = oid regclass public', 'HIJACK-OP || text int4 public'].

Resolución real del operador (sondas tras la guarda; el servidor registra el operador del que depende la vista, no una inspección textual):
| Caso/árbol | Categoría | Operador realmente resuelto | search_path efectivo | Rechazo | Estado |
|---|---|---|---|---|---|
| J-01/NEW | J resolución real | pg_catalog(objeto fijado: sin pg_depend) | pg_catalog, public, pg_temp | - | PASS |
| J-02/VULN | J resolución real | public.=(oid,regnamespace) | pg_catalog, public, pg_temp | - | PASS |
| J-02/NEW | J resolución real | (sin resolución: el script no llegó a ejecutarse) | n/d | G-OPERADOR-AJENO-EN-SEARCH-PATH | PASS |
| F-01/VULN | F creado tras fijar search_path | public.=(oid,regnamespace) | pg_catalog, public, pg_temp | - | PASS |
| F-01/NEW | F creado tras fijar search_path | public.=(oid,regnamespace) | pg_catalog, public, pg_temp | - | PASS |
| G-01/VULN | G objetos temporales | pg_catalog(objeto fijado: sin pg_depend) | pg_catalog, public, pg_temp | - | PASS |
| G-01/NEW | G objetos temporales | pg_catalog(objeto fijado: sin pg_depend) | pg_catalog, public, pg_temp | - | PASS |
| H-01/NOPIN | H PGOPTIONS | evil.=(oid,regnamespace) | evil,pg_catalog,public | - | PASS |
| H-01/VULN | H PGOPTIONS | (sin resolución: el script no llegó a ejecutarse) | n/d | G-SEARCH-PATH-NO-SEGURO | PASS |
| H-01/NEW | H PGOPTIONS | (sin resolución: el script no llegó a ejecutarse) | n/d | G-SEARCH-PATH-NO-SEGURO | PASS |
| H-02/NOPIN | H configuración heredada | evil.=(oid,regnamespace) | evil, pg_catalog, public | - | PASS |
| H-02/NEW | H configuración heredada | (sin resolución: el script no llegó a ejecutarse) | n/d | G-SEARCH-PATH-NO-SEGURO | PASS |
| H-03/NOPIN | H configuración heredada | evil.=(oid,regnamespace) | evil, pg_catalog, public | - | PASS |
| H-03/NEW | H configuración heredada | (sin resolución: el script no llegó a ejecutarse) | n/d | G-SEARCH-PATH-NO-SEGURO | PASS |
| H-04/NEW | H SET posterior | evil.=(oid,regnamespace) | evil, public | - | PASS |
| H-04b/NEW | H SET LOCAL | evil.=(oid,regnamespace) | evil, public | - | PASS |

Aserción estática H-05: PASS — ningún script ejecutable cambia `search_path`/rol ni crea operadores/casts/tipos salvo los usos documentados: ["00_verificar_marcador.sql: perform pg_catalog.set_config('search_path','pg_catalog, pg_temp',true);", "04_lib_clasificador.sql: if p_rol is not null then execute pg_catalog.format('set local role %I', p_rol); end if;", '04_lib_clasificador.sql: begin reset role; exception when others then null; end;', '04_lib_clasificador.sql: begin reset role; exception when others then null; end;'].

## 4. Corrección aplicada (guarda; archivos aprobados regenerados en `SHA256SUMS_CCI.txt`)
Se evaluó en el orden pedido:
1. **Revocar CREATE innecesario sobre public** → exigido y comprobado en la guarda (modo DEV): `G-OPERADOR-CREATE-EN-PUBLIC`, `G-PUBLIC-CREATE-AJENO`; la plantilla `PROCEDIMIENTO_ROLES_CCI_DEV.sql` (no ejecutada) incluye la revocación.
2. **Que ningún rol operativo herede privilegios peligrosos** → `has_schema_privilege`/`has_database_privilege` efectivos (incluyen herencia, PUBLIC y propiedad) y `G-OPERADOR-MEMBRESIA-PRIVILEGIADA`.
3. **Eliminar membresías indirectas** → `pg_has_role(...,'member')` independiente de INHERIT (P-05, P-06).
4. **Proteger esquemas auxiliares/temporales** → `G-OPERADOR-CREATE-EN-BASE` (evita esquemas auxiliares) y rechazo de operadores en `pg_temp_*`; G-01 demuestra que PostgreSQL ignora `pg_temp` para operadores.
5. **Calificar explícitamente operadores críticos** → **inviable de forma completa**: `IN (…)`, `= ANY`, `JOIN … ON a = b`, `ORDER BY`, `LIKE`, comparaciones de columnas y los operandos de las políticas RLS evaluadas por el servidor no admiten `OPERATOR(pg_catalog.=)` en todos los sitios. Alternativa verificable: la guarda rechaza cualquier operador ajeno en los esquemas del `search_path` y fija el `search_path` de sesión (pg_catalog primero); G-01/J-01/J-02 verifican el operador realmente resuelto.
6. **Calificar funciones y referencias sensibles** → ya calificadas con `pg_catalog.` (SPD1/SPD2: 73 funciones, todas las sobrecargas; sin regresión).
7. **Controles del lado del servidor** → necesarios para el límite estructural (control total de la máquina del operador); documentados como BLOQUEADO (EXT-02/L05, ficha ampliada en `PLAN_DESBLOQUEO_EXTERNOS.md`). Dentro de una base ya comprobada, un rol con CREATE en `public` podría plantar un operador después de la guarda: por eso la guarda exige que NINGÚN rol no superusuario lo tenga (P-09) y el límite restante es el superusuario/propietario de la base.

Regresión corregida durante el trabajo: (a) la comprobación inicial rechazaba la extensión legítima `btree_gist` (usada por las exclusiones de CCI; 12 operadores `<->` en `public`) → se toleran sólo operadores de extensión con símbolos no estándar (K-01 demuestra que una extensión hostil con `=` sigue rechazada; K-02 que btree_gist se acepta y los 6 scripts funcionan); (b) bug latente del script 04: `'…'||:post_count||'…'` con valor −1 se leía como operador `||-` (corregido con casts y espacios; ya en la ejecución anterior); (c) GD-15 afirmaba el `search_path` previo; (d) la reconciliación de alcance no admitía `ARTEFACTOS_REVISION_PUBLICACION/` (artefactos de publicación autorizados por el propietario).

## 5. Resultado de la suite adversarial
39/39 PASS (8/8 escenarios de barrido, 16/16 sondas de resolución real, 14/14 de privilegios, 1 estática). Contra VULN se ejecutaron 11 combinaciones caso×script (control positivo); contra NEW, 0.
