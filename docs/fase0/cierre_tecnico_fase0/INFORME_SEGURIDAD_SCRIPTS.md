# INFORME DE SEGURIDAD DE LOS SCRIPTS SQL (CCI-DEV, v2)

**Alcance:** `01`, `02`, `03`, `04` (+ `04_lib_clasificador.sql`), `05_A`, `05_B`. **Todos NO EJECUTADOS contra CCI-DEV/CCI-PROD.** Revisión estática + smoke en PostgreSQL local temporal. No demuestra nada sobre Supabase.

## Hallazgos corregidos (v1 → v2)
| Script | Defecto v1 | Corrección v2 |
|---|---|---|
| 04 | `intenta()` capturaba cualquier excepción; negativos = PASS (11 falsos PASS reproducidos) | clasificador; PASS solo con función existente + contrato SQLSTATE/prefijo; errores técnicos = BLOCKED; inesperado = FAIL; sin contrato = PARTIAL |
| 03 | columna inexistente `approver`; DELETE/TRUNCATE ejecutables; pruebas posiblemente vacuas | precondiciones, resultado por tabla, sondas sin efecto, comprobación de no vacuidad |
| 05 | sin comprobar tabla; sin timeouts | precondición (BLOCKED), `lock_timeout`/`statement_timeout`, PASS solo con espera medida |
| 01/02 | sin guarda explícita | guarda + `begin read only`; solo inventario |

## Comprobaciones (escáner `ct_escaner_seguridad_sql.py`, v3: `sql` sobre los seis scripts, la biblioteca y `00_guarda_destino.sql`; `texto` sobre todo el dossier; `autoprueba`; totales en `INFORME_CIFRAS_DEFINITIVAS.md`)
Guarda de destino compartida incluida (`\\ir 00_guarda_destino.sql`) tras `ON_ERROR_STOP` y antes de cualquier SQL de datos, y el propio archivo de guarda con identidad efectiva, allowlist/denylist literales, rechazo de PROD, fallo cerrado y anti-suplantación; sin COMMIT; sin DDL/DCL peligroso fuera de literales (DROP/TRUNCATE/ALTER/GRANT/REVOKE/CREATE ROLE|EXTENSION|DATABASE|SCHEMA); escrituras solo en scripts con ROLLBACK; sin metacomandos de conexión (`\c`, `\!`, `\copy`); sin referencias de proyecto, URL, secretos ni JWT; sin objetos permanentes. v2 añade: SQL dinámico (`%s`, concatenación), `WHEN OTHERS`, `SET ROLE`, `LOCK`/`FOR UPDATE`, `pg_sleep`, `ON_ERROR_STOP`, secretos/credenciales/correos/teléfonos/refs de proyecto en **todo** el dossier y enlaces simbólicos. **Controles negativos:** `autoprueba` (muestras aisladas, cada una dispara su comprobación; el control limpio no dispara ninguna; incluye mutaciones del archivo de guarda). El escáner v1 no examinaba el interior de los bloques `$$…$$`; corregido.

## Smoke local (modo LOCAL-TEMPORAL)
Guardas: los seis abortan sin autorización (6/6) y el 01 aborta en una base sin prefijo `cci_` (7/7). 03: shim defectuoso → RLS-01/02/03 FAIL; corregido → PASS; RLS-06 NOT VERIFIED. 04: NO VERIFICABLE EN ENTORNO FÍSICO. 05: B espera 3,50 s → PASS; sin tabla → BLOCKED.

## Límites (declarados)
1. La guarda verifica la identidad efectiva contra listas literales, pero esas listas están vacías hasta que el propietario entregue los identificadores reales de CCI-DEV/CCI-PROD (LR-22; P1). Pruebas: `resultados/guarda_destino.txt`.
2. El escáner es heurístico (expresiones regulares); no sustituye una revisión humana.
3. Los scripts se ejecutaron solo localmente; permisos reales, `auth.uid()` y RLS de Supabase no se probaron.
4. Los scripts son **plantillas** hasta que exista el esquema físico (la lógica de R1–R9 no se simula).
