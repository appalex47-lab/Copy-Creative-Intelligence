# Matriz de persistencia del search_path
**Conclusión técnica:** `set_config('search_path', …, true)` es *local a la transacción*; la guarda lo ejecuta dentro de un bloque `DO` que, en `psql` sin `BEGIN`, es su propia transacción. Al terminar el bloque el valor **se restablece** (SP-04: la primera instrucción posterior ve el `search_path` del llamador, `evil,public,pg_temp`). Por tanto el search_path blindado protege **únicamente la evaluación de la guarda** (sus llamadas ya van calificadas), **no** las instrucciones posteriores del script. La afirmación "search_path blindado" de la entrega publicada era cierta sólo en ese alcance.
**Por qué no se persiste a nivel de sesión:** se probó fijar `pg_catalog, pg_temp` en sesión: rompió el smoke del script 03 (las políticas RLS del shim resuelven `memberships` con el search_path de la sesión; BLOCKED 42P01). Un parámetro de sesión así distorsionaría las pruebas RLS contra CCI-DEV.
**Defecto real encontrado (AUD-FINAL-01):** en la rama publicada, funciones homónimas en un esquema anterior a pg_catalog se invocaban desde 05A y 05B (`hijack_PRE_rama_publicada.txt`). **Corrección:** 144 llamadas a funciones del catálogo calificadas con `pg_catalog.` en los 6 scripts y la biblioteca; `hijack_POST_correccion.txt`: 0 invocaciones; GD-19 lo fija como prueba permanente. Límite: operadores y tipos no se califican.
| Escenario | Esperado | Rama publicada | Árbol corregido |
|---|---|---|---|
| Guarda: alteración a nivel de ROL (`ALTER ROLE SET search_path=evil`) con `pg_control_system` falsa | Rechaza (identidad real) | PASS (SP-02, ambos) | PASS |
| Guarda: alteración a nivel de BASE (`ALTER DATABASE SET search_path=evil`) | Rechaza | PASS (SP-01) | PASS |
| Guarda: `pg_temp`/`evil` primeros (PGOPTIONS) | Rechaza | PASS (SP-03) | PASS |
| Persistencia tras el bloque DO | NO persiste (documentado) | confirmado (SP-04) | confirmado (SP-04, GD-15) |
| Funciones homónimas tras la guarda (hijack) | No se invocan | **FAIL**: 05A y 05B invocaron la función falsa | PASS (6/6) |

Resumen de filas SP/X-10 en la matriz: corregido {'PASS': 30}; publicada {'FAIL': 6, 'PASS': 24}.
