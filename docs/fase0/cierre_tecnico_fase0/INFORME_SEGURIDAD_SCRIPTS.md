# INFORME DE SEGURIDAD DE LOS SCRIPTS SQL (CCI-DEV, v2)

**Alcance:** `01`, `02`, `03`, `04` (+ `04_lib_clasificador.sql`), `05_A`, `05_B`. **Todos NO EJECUTADOS contra CCI-DEV/CCI-PROD.** Revisión estática + smoke en PostgreSQL local temporal. No demuestra nada sobre Supabase.

## Hallazgos corregidos (v1 → v2)
| Script | Defecto v1 | Corrección v2 |
|---|---|---|
| 04 | `intenta()` capturaba cualquier excepción; negativos = PASS (11 falsos PASS reproducidos) | clasificador; PASS solo con función existente + contrato SQLSTATE/prefijo; errores técnicos = BLOCKED; inesperado = FAIL; sin contrato = PARTIAL |
| 03 | columna inexistente `approver`; DELETE/TRUNCATE ejecutables; pruebas posiblemente vacuas | precondiciones, resultado por tabla, sondas sin efecto, comprobación de no vacuidad |
| 05 | sin comprobar tabla; sin timeouts | precondición (BLOCKED), `lock_timeout`/`statement_timeout`, PASS solo con espera medida |
| 01/02 | sin guarda explícita | guarda + `begin read only`; solo inventario |

## Comprobaciones (escáner `ct_escaner_seguridad_sql.py`: 64, 0 FAIL)
Guarda presente (CCI-DEV y local-temporal) y antes de cualquier SQL de datos; sin COMMIT; sin DDL/DCL peligroso fuera de literales (DROP/TRUNCATE/ALTER/GRANT/REVOKE/CREATE ROLE|EXTENSION|DATABASE|SCHEMA); escrituras solo en scripts con ROLLBACK; sin metacomandos de conexión (`\c`, `\!`, `\copy`); sin referencias de proyecto, URL, secretos ni JWT; sin objetos permanentes. **Control negativo:** un script deliberadamente malo produce 8 FAIL (el escáner detecta).

## Smoke local (modo LOCAL-TEMPORAL)
Guardas: los seis abortan sin autorización (6/6) y el 01 aborta en una base sin prefijo `cci_` (7/7). 03: shim defectuoso → RLS-01/02/03 FAIL; corregido → PASS; RLS-06 NOT VERIFIED. 04: NO VERIFICABLE EN ENTORNO FÍSICO. 05: B espera 3,50 s → PASS; sin tabla → BLOCKED.

## Límites (declarados)
1. La guarda no prueba que la base sea CCI-DEV (LR-22): depende del operador y del propietario (P1).
2. El escáner es heurístico (expresiones regulares); no sustituye una revisión humana.
3. Los scripts se ejecutaron solo localmente; permisos reales, `auth.uid()` y RLS de Supabase no se probaron.
4. Los scripts son **plantillas** hasta que exista el esquema físico (la lógica de R1–R9 no se simula).
