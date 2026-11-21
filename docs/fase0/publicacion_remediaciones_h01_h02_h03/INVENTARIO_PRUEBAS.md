# Inventario de pruebas — VIGENTE (ejecución del 2026-11-21, árbol corregido; cifras de la rama publicada d365a16 = histórico)
| Área | Prueba | Resultado |
|---|---|---|
| H-01 | Batería de 22 pasos (clústeres 1 y 2) | 22/22 OK en cada uno |
| H-01 | Aserciones del smoke | 12/12 |
| H-02 | Reconciliación / consistencia | 58/58 / 58/58 |
| H-03 | Guarda DEV/PROD (GD-00…GD-19) | 139/139 PASS |
| H-03 | Matrices de la auditoría final (228 casos × árbol) | corregido: {'PASS': 202, 'PARTIAL': 26}; rama publicada: {'PASS': 196, 'PARTIAL': 26, 'FAIL': 6} |
| Integración | Comparación entre clústeres | 30/30 |
Histórico: 109/109 y 22/22 de la rama publicada se reprodujeron en un tercer clúster (confirmación, no vigente).
