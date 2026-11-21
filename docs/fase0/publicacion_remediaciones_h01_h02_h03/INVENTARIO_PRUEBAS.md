# Inventario de pruebas (ejecución de esta publicación, 2026-11-21; histórico = no revalidado aquí)
| Área | Prueba / paso | Resultado (clúster 1 y clúster 2 idénticos) |
|---|---|---|
| H-01 | Batería final, 22 pasos (`INDICE_BATERIA_*.csv`) | 22/22 OK en cada clúster limpio |
| H-01 | Aserciones de contenido del smoke de los 6 scripts | 12/12 PASS |
| H-01 | Precondición de roles explícita (`bateria_final/precondicion_roles.txt`) | incluida en la batería |
| H-02 | Reconciliación integral | 58/58 PASS |
| H-02 | Verificador de consistencia (+ controles negativos) | 58/58; controles 7/7 |
| H-02 | Controles negativos del manifiesto | 36/36 |
| H-02 | Manifiesto SHA-256 (verificación independiente) | 137 entradas, 0 hashes incorrectos |
| H-03 | Guarda DEV/PROD sobre los 6 scripts (GD-00…GD-14) | 109/109 PASS (20 rechazos con `G-PROD-RECHAZADO`; 18 de guarda vacía/truncada; 6 por stdin) |
| H-03 | Casos de hueco AG (auditoría independiente) | 25/25 conforme a lo esperado tras la corrección (AG-18 = límite conocido) |
| Integración | Comparación entre clústeres | 30/30 idénticos |
| Controles negativos | Autoprueba del escáner / escáner SQL / escáner de texto | 37 / 137 / 771, 0 FAIL |
Cifras históricas **no** reutilizadas: la cifra "85/85" y "33/33 rechazos contra PROD simulado" de la entrega anterior son históricas; esta publicación reporta 109/109 y 20 rechazos `G-PROD-RECHAZADO` (la definición de "33" no pudo reproducirse con el mismo criterio de conteo, por lo que no se reitera).
