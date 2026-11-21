# Matriz de los seis scripts
Todos incluyen `00_preflight_guarda.sql` y `00_verificar_marcador.sql` con doble `\set cci_script`. Casos A–O aplicados a cada script.

| Script | Árbol final (casos adversariales) | Rama publicada e0b1d81 (A, D, E1, H) | SHA-256 (16) |
|---|---|---|---|
| 01 | 20 PASS / 1 PARTIAL / 0 FAIL | 3 FAIL (defecto) / 1 PASS | 2c04e5eba28de65c |
| 02 | 16 PASS / 1 PARTIAL / 0 FAIL | 3 FAIL (defecto) / 1 PASS | d3ff9dfeb5036c1d |
| 03 | 16 PASS / 1 PARTIAL / 0 FAIL | 3 FAIL (defecto) / 1 PASS | 065e698ce5fcacc8 |
| 04 | 16 PASS / 1 PARTIAL / 0 FAIL | 3 FAIL (defecto) / 1 PASS | 955efe7f05dbe946 |
| 05A | 20 PASS / 1 PARTIAL / 0 FAIL | 3 FAIL (defecto) / 1 PASS | a18fcd80d5ac9d21 |
| 05B | 16 PASS / 1 PARTIAL / 0 FAIL | 3 FAIL (defecto) / 1 PASS | 10f7a93f359a340c |

Mapa de casos: A marcador pre-creado · B tabla homónima · C marcador de corrida previa (C2 otra sesión) · D guarda vacía+marcador · E1 guarda alterada que crea marcador · E2 guarda falsa con protocolo (PARTIAL si controla también el hash) · F fallo tras iniciar · G guarda sustituida · H psql directo sin ejecutor · I seis scripts consecutivos · J pooler simulado · K marcador alterado en ejecución · L marcador de otro script · M reuso tras rollback/error · N otra sesión · O guarda borrada/modificada (WRAP-*).
