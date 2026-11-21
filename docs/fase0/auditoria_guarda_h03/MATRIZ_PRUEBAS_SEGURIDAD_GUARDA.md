# Matriz de pruebas de seguridad de la guarda
Cobertura de las 85 pruebas del parche (GD-00..GD-12) frente a lo pedido, más 25 casos nuevos (AG-xx) en evidencia/aud_huecos_guarda.py (clúster local nuevo, 6 scripts por caso).
| Escenario | Pruebas existentes | Casos añadidos | Resultado |
|---|---|---|---|
| DEV autorizado | GD-01 | AG-05 | pasa |
| PROD rechazado | GD-02/02b | AG-06 (allow+deny: gana PROD), AG-17 | rechaza |
| Proyecto desconocido | GD-03a/b/c | AG-01, AG-07m/e/s/o (variantes exactas) | rechaza |
| Identidad no verificable | GD-05/05b | AG-19 (rol sin EXECUTE) | rechaza |
| Variables manipuladas | GD-06a-e, GD-07a/b | AG-16m/e/c/v | rechaza |
| search_path manipulado | GD-07c | AG-08 (ALTER DATABASE), AG-09 (ALTER ROLE), AG-10 (pg_temp) | rechaza |
| Configuración incompleta | GD-06 | AG-16v | rechaza |
| Suplantación (DEV declarado contra PROD) | GD-04 | AG-17 (base cci_dev, sysid en denylist) | rechaza |
| Clon con mismo sysid y base | — | AG-18 | **pasa: límite conocido** |
| Ejecución desde los 6 scripts | GD-all | todos los AG, 6 scripts | ver hallazgos |
| Flags psql | — | AG-13/14/15 | rechaza |
| Guarda vacía/truncada | GD-08 (sólo ausente) | AG-02/03/04 | **HUECO AUD-G1** (SIN_GUARDA en 6/6) |
| stdin con cwd rogue | — | AG-11 | **HUECO AUD-G3** (01/02 sin guarda; 03-05 abortan) |
Resumen de AG: 25 casos, 20 OK, 4 hallazgos (AG-02/03/04/11), 1 límite (AG-18, esperado). AG-16e dio inicialmente falso positivo por mi comillado (la conexión fallaba); repetido con escape correcto: rechaza (G-CONFIG-INVALIDA).
Mitigación AUD-G1 validada en copia (guarda vacía ⇒ G-GUARDA-NO-EJECUTADA en 01/03/05A). Pruebas nuevas a incorporar al parche tras corregirlo: AG-02/03/04/11.
