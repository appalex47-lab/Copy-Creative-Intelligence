# Matriz de riesgos de CCI
Probabilidad/impacto: A alta · M media · B baja (estimaciones **mías**, no medidas). Origen: auditoría y diseño.
| ID | Riesgo | P | I | Mitigación propuesta | Decisión/Fase |
|---|---|---|---|---|---|
| RK-01 | Pérdida de datos por borrado/expulsión del navegador | M | A | `persist()`, aviso de respaldo, exportación periódica; no se promete recuperación automática | P9, F1/F5 |
| RK-02 | Cuota agotada con binarios | M | M | límites de tamaño, estimación de cuota, política P5 | P5, F3 |
| RK-03 | Origen compartido expone datos a otras apps del mismo origen | M | A | hosting por origen propio; documentarlo | P10, F5 |
| RK-04 | Edición concurrente en varias pestañas | M | M | `revision` optimista + política P12 | P12, F1 |
| RK-05 | Importación parcial/corrupta | B | A | todo-o-nada, hash, validación, respaldo previo | F5 |
| RK-06 | Claves de IA expuestas en el cliente | A | A | sin claves en código/almacenamiento; alternativa IA aprobada | P8, F2 |
| RK-07 | Modelo de dominio mal definido → migraciones costosas | M | A | decidir P4/Q-4 antes de F1; migraciones secuenciales con pruebas | P4, F1 |
| RK-08 | Documentación contradictoria (K1–K20) | A | M | documentación vigente propuesta; no reescribir histórico | P2, P3 |
| RK-09 | Dependencias nuevas sin auditar | M | M | política P13; `npm audit` no ejecutado aún | P13 |
| RK-10 | Diferencias entre navegadores | M | M | matriz soportada P11; solo Chrome verificado | P11 |
| RK-11 | XSS con contenido de usuario/archivos | M | A | no `dangerouslySetInnerHTML`, sanitización, validación de importación | F1+ |
| RK-12 | IA tratada como fuente de verdad comercial | B | A | reglas/cálculos en código; IA solo sugiere | F2–F4 |
| RK-13 | Alcance ampliado por iniciativa propia | M | M | control por fases del propietario | todas |
| RK-14 | CI nunca ejecutado en runner real | M | M | ejecutar CI antes de aceptar Fase 1 | F1 |
| RK-15 | El código aceptado (B1–B3) conserva `Organization/Membership/roles` mientras P1=(b) los excluye del dominio vigente: divergencia entre código y documentación hasta que se autorice su retiro en Fase 1 | A | B | documentarla (hecho); retirar solo con autorización de Fase 1; no reescribir la historia | P1, F1 |
| RK-16 | Flujo de un único usuario: quien crea un copy también lo aprueba; no hay separación de funciones | A | M | documentarlo como limitación aceptada de la arquitectura; no simular aprobadores | P1, F5 |

IndexedDB no es cifrado ni frontera de seguridad; el usuario es responsable de proteger el equipo y sus respaldos.
