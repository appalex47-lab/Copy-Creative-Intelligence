# EVIDENCIA DE PRUEBAS INDIVIDUALES V16 (pendiente C)

## Observación
`pruebas_guarda()` (modelo_estructural.py:1810) y `pruebas_atomicidad()` (:2104) ya devuelven una lista de pares `(nombre, bool)`: cada caso es individualizable sin cambiar su lógica. El resultado agregado que daba el verificador (K47) ocultaba esos pares.

## Instrumentación (sin tocar el motor, el verificador ni las pruebas)
Script externo nuevo: `instrumentar_pruebas_individuales.py` (esta carpeta). Importa el módulo tal cual, llama a las dos funciones y escribe por caso: identificador, esperado (True), obtenido, PASS/FAIL y mensaje si falla. Los casos de `pruebas_atomicidad` 9–20 son las 12 mutaciones de `correr_mutaciones_rechazo` (A54–A65), que la función incorpora (`rechaza` y `atomico`).

Comando: `env -i PATH=/usr/bin:/bin LC_ALL=C.UTF-8 PYTHONHASHSEED=0 PYTHONDONTWRITEBYTECODE=1 python3 -I instrumentar_pruebas_individuales.py <ruta>/herramientas`

## Resultado ejecutado (2026-11-20, dos corridas, salida idéntica, SHA-256 prefijo `cc2825746646a760`)
| Función | Casos | PASS | FAIL |
|---|---|---|---|
| pruebas_guarda | 9 | 9 | 0 |
| pruebas_atomicidad | 20 | 20 | 0 |
Salidas: `salida_pruebas_individuales_corrida1.txt`, `..._corrida2.txt`. El resultado esperado es siempre True: la guarda debe bloquear el intento y la reutilización inválida debe rechazarse sin escribir nada y con el estado completo intacto.

## Comparación con el agregado
K47 aprueba en el verificador y los 29 casos individuales aprueban: sin discrepancia. 

## Otras funciones (ejecutadas individualmente sobre el commit V16; cada elemento trae su indicador de detección)
mutaciones_rechazo 12/12; adversariales 16/16; escenarios 17/17; mutaciones_k47 36/36; mutaciones_resoluciones 12/12; mutaciones_assets 53/53; positivos_arte 26/26; mutaciones_cadena 24/24; adversariales_cadena 24/24; mutaciones_atribucion 12/12; atomicidad14 11/11; E14 6/6; av 8/8; cf 8/8; ac 6/6; positivos15 8/8; adversariales15 8/8; atomicidad15 8/8; modelo14 12/12. Esta tabla viene de la ejecución de la auditoría previa (2026-11-19) y no se repitió hoy individualmente; hoy se repitió el verificador completo, que las ejecuta.

## Actualización V17: inventario de funciones de prueba
`modelo_estructural.py` expone 22 funciones de ejecución públicas (más 2 auxiliares `_correr_lista`, `_correr15`). Individualizadas con resultado propio: `pruebas_guarda` (9/9) y `pruebas_atomicidad` (20/20). Las otras 20 (mutaciones, adversariales, positivos y `escenarios`; además `pruebas_atomicidad14`, `pruebas_E14` y `pruebas_atomicidad15`) las ejecuta y cuenta el verificador (K45–K59, 300 mutaciones, cada una reportada como DETECTADA en su salida). No se repitieron: la evidencia vigente cubre el estado actual, porque el cambio S1 no toca el modelo. Posibles candidatas a individualizar si se desea mayor detalle: `pruebas_atomicidad14`, `pruebas_E14`, `pruebas_atomicidad15` (no ejecutadas por separado). Nota: mi cuenta es 20 restantes; un resumen previo hablaba de 19.

## Actualización V18
Sustituye al inventario de V17 (que hablaba de 20 funciones pendientes): son 22 funciones de ejecución y 363 casos, todos con resultado individual PASS en el modelo en memoria (script externo `instrumentar_22_funciones_v18.py`; salidas `salida_22_funciones_corrida1/2.txt`, idénticas). Detalle por función, invocación del verificador y cobertura: `INVENTARIO_22_FUNCIONES_V18.md`. `pruebas_atomicidad14` (11), `pruebas_E14` (6) y `pruebas_atomicidad15` (8) devolvían ya un `ok` por caso; el verificador solo imprimía el agregado. Sin modificar la lógica de las pruebas. Es evidencia de modelo en memoria, no de PostgreSQL.

## Actualización V19
Las 22 funciones y sus 363 casos no se repitieron: ni el modelo ni el verificador cambiaron. Las cinco pruebas PE-01..PE-05 (reglas E de C08) están diseñadas pero **no ejecutadas** (requieren PostgreSQL); no cuentan como evidencia. Vínculo escenario→prueba ejecutada: 258 escenarios «Diseño» citan un identificador de prueba que figura PASS en la salida de las 22 funciones (MATRIZ_ESCENARIOS_V19.csv); es un vínculo por identificador, no una lectura de la equivalencia.
