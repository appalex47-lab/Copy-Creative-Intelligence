# Auditoría del marcador de guarda (H-03)
## Defecto en la rama publicada (e0b1d81 / d365a16)
El marcador `pg_temp.cci_guarda_ok` es una tabla temporal que cualquier usuario puede crear. Ataques reproducidos contra e0b1d81 (6 scripts cada uno): **A** (marcador pre-creado), **D** (guarda vacía + marcador), **E1** (guarda alterada que crea el marcador) → el cuerpo del script se ejecutó (canario impreso) = **FAIL, defecto reproducido** (18 casos). **H** (psql directo) fue rechazado.
## Diseño corregido
1. Cada script: `\set cci_script '<id>'`, `\ir 00_preflight_guarda.sql`, de nuevo `\set cci_script`, `\ir 00_verificar_marcador.sql`.
2. El preflight exige `CCI_DIR` y `CCI_GUARDA_SHA256_APROBADO` (hash aprobado externamente), copia la guarda a un directorio privado, hashea **la copia** y ejecuta esa misma copia (sin ventana check→use). Hash distinto → `NO EJECUTADO [G-GUARDA-INTEGRIDAD]`.
3. La guarda, al terminar, genera un id aleatorio (`gen_random_uuid`) en una variable de psql (`cci_run`, no forjable desde SQL), crea `pg_temp.cci_g_<id>` (script, pid, usado) y registra la fila.
4. El verificador exige `cci_run`, la tabla de esa corrida, script = el declarado, pid = `pg_backend_pid()`, `usado=false`, y la **consume** (update …usado=true; exactamente 1 fila). Un marcador reusado, de otro script/sesión, alterado o pre-creado no coincide.
## Resultados (árbol final)
Casos A, B, C, C2, D, E1 (modos M y H), F, G, H, I, J, K (4 variantes), L, M, N: **todos rechazados**, sin efectos persistentes (136 PASS + 6 PARTIAL en el árbol corregido; 0 FAIL).
## Límite estructural (PARTIAL, E2/M)
Una guarda falsificada que implemente el protocolo completo pasa **si el atacante controla además el hash aprobado**. Con el hash externo real se rechaza (E2/H). La protección depende de que el hash viva fuera del alcance del atacante; **el custodio externo no existe aún** → configuración pendiente, no protección operativa.
## Pooler (J)
Simulado (no hay pgbouncer): en modo transacción la tabla temporal no sobrevive y los scripts rechazan. No validado con Supavisor real.
