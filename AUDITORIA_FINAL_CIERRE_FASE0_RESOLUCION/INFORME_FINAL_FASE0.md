# Informe final — Operación de Resolución Final Fase 0

## Veredicto
**FASE0_BLOCKED** (código de salida 2). Causa: dependencias externas pendientes: ID-13, EXT-03, EXT-01, EXT-02, EXT-04-L04, EXT-04-L05, EXT-04-L06, EXT-04-L07, EXT-04-L08. **No hay defecto técnico abierto detectado por las pruebas** (FAIL = 0); lo que impide `FASE0_READY_FOR_OWNER_ACCEPTANCE` son dependencias que solo el propietario puede aportar. **Fase 0 NO está aceptada.**

## Ejecución
- Ejecución `CCI-RUN-20261121T223416Z-67eb098f` · inicio 2026-11-21T22:34:16Z · duración 457.7 s · código evaluado `cd8689b55e2f7c06b2756596d0f449bb2c2ce5b6` · rama `audit/fase0-resolucion-final`.
- Pasos del orquestador: 77 · PASS 66 · FAIL 0 · BLOCKED 10 · NOT_TESTED 1 · etapas no iniciadas 0.
- Etapas: {'A': 'PASSED', 'B': 'PASSED', 'C': 'PASSED', 'D': 'PASSED', 'E': 'PASSED', 'F': 'PASSED', 'G': 'PASSED', 'H': 'PASSED', 'I': 'PASSED', 'J': 'PASSED', 'K': 'BLOCKED'}. Clústeres nuevos y vacíos, independientes (system_identifier, directorio y puerto distintos): {'dev': {'port': 34233, 'sysid': '7710756749892870120'}, 'prod': {'port': 48841, 'sysid': '7710756753390919690'}}.
- Matriz de la versión actual `MATRIZ_FINAL_DE_PRUEBAS.csv`: 548 filas → {'PASS': 527, 'BLOCKED': 10, 'NOT_TESTED': 1, 'PARTIAL': 9, 'NOT TESTED': 1}. Por suite: {'ORQ': 77, 'ADV': 142, 'IDENT-GUARDA-SQL': 14, 'SP': 30, 'AO': 22, 'AG18': 42, 'EXT01/E2E': 36, 'EXT03': 34, 'EXT02-SIM': 7, 'SEC05': 15, 'ORQ-META': 49, 'BAT': 22, 'RECON': 58}.
- Ataques contra la versión **anterior** (separados, no cuentan como resultado de la versión actual): `ATAQUES_CONTRA_VERSION_ANTERIOR.csv` → {'FAIL': 33, 'PASS': 27} (los 33 FAIL históricos: 18 casos adversariales de la rama publicada + 15 de search_path de ramas anteriores; son los ataques reproducidos, esperados).

## Causas raíz y correcciones
Ver `INFORME_HALLAZGOS.md` (estado previo, causa raíz, solución, archivos, prueba que reproduce, prueba posterior, resultado, instrucciones de desbloqueo, clasificación).

## Dependencias externas BLOQUEADAS (9)
| ID | Dependencia |
|---|---|
| ID-13 | validación real en Supabase (no autorizada ni disponible) |
| EXT-03 | listas de destinos DEV/PROD autorizados: RECHAZADO [L-DEV-VACIA] dev_allow vacía: el propietario debe aportar al menos un 'system_identifier\|base' de CCI-DEV |
| EXT-01 | custodio externo del hash aprobado no definido: falta la aprobación firmada (CCI_APROBACION_CUSTODIO) y la clave pública con su SHA-256 (CCI_CUSTODIO_PUBKEY, CCI_CUSTODIO_PUBKEY_SHA256). El mecanismo  |
| EXT-02 | compatibilidad con Supabase CCI-DEV (TEMP, pg_control_system(), PGOPTIONS por pooler, project ref, pooler): sólo verificable en CCI-DEV; la sonda existe y está probada en local (SIMULADO_LOCAL) |
| EXT-04-L04 | equivalencia del PostgreSQL temporal con el esquema físico aprobado (no existe esquema físico aprobado) |
| EXT-04-L05 | validación física en CCI-DEV |
| EXT-04-L06 | RLS, privilegios y concurrencia reales en CCI-DEV |
| EXT-04-L07 | trigger de elegibilidad R1–R9 en entorno físico |
| EXT-04-L08 | HV-02/PO-05: confirmación del propietario sobre la Adenda v9 (el documento no existe en el repositorio) |

Instrucciones exactas por ficha en `PLAN_DESBLOQUEO_EXTERNOS.md`.

## Estado del repositorio y confirmación de no acciones no autorizadas
- Rama local `audit/fase0-resolucion-final` (derivada de `c98ade0` / `audit/fase0-cierre-fail-fast`): **existe solo en este entorno temporal, no en GitHub**. Commits locales: a7c1d45, e1ce57d, eb0ac4a, c98ade0 (operación previa) y los de esta operación.
- **No se hizo push, merge, PR, despliegue ni release; no se tocó `main` ni V26; no se conectó CCI-PROD ni Supabase (ni CCI-DEV).** Las ramas remotas protegidas se verificaron intactas al inicio de la corrida (etapa A, `git ls-remote`).
- Las claves Ed25519 usadas en las pruebas son efímeras y de prueba; no hay custodio, autoridad ni credenciales reales. Ninguna aprobación se inventó.
- No se publica rama de cierre (la regla exige PASSED).

## Pendiente del propietario (decisiones y entregables)
- ID-13: validación real en Supabase (no autorizada ni disponible)
- EXT-03: listas de destinos DEV/PROD autorizados: RECHAZADO [L-DEV-VACIA] dev_allow vacía: el propietario debe aportar al menos un 'system_identifier|base' de CCI-DEV
- EXT-01: custodio externo del hash aprobado no definido: falta la aprobación firmada (CCI_APROBACION_CUSTODIO) y la clave pública con su SHA-256 (CCI_CUSTODIO_PUBKEY, CC
- EXT-02: compatibilidad con Supabase CCI-DEV (TEMP, pg_control_system(), PGOPTIONS por pooler, project ref, pooler): sólo verificable en CCI-DEV; la sonda existe y está 
- EXT-04-L04: equivalencia del PostgreSQL temporal con el esquema físico aprobado (no existe esquema físico aprobado)
- EXT-04-L05: validación física en CCI-DEV
- EXT-04-L06: RLS, privilegios y concurrencia reales en CCI-DEV
- EXT-04-L07: trigger de elegibilidad R1–R9 en entorno físico
- EXT-04-L08: HV-02/PO-05: confirmación del propietario sobre la Adenda v9 (el documento no existe en el repositorio)
- Decidir si la rama local se publica para revisión y si se fusiona (no se solicita decisión aquí).

## No verificado por mí
Todo lo que dependa de Supabase/CCI-DEV real (pooler, TEMP, PGOPTIONS, roles reales, RLS real), de un custodio o autoridad reales, del esquema físico aprobado, del trigger físico y de la Adenda v9 (el documento no está en el repositorio).
