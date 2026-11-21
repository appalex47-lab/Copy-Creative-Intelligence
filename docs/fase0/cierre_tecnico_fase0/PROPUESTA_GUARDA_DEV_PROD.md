# GUARDA DE DESTINO DEV/PROD (LR-22 / H-03) — **IMPLEMENTADA Y PROBADA EN LOCAL; IDENTIFICADORES REALES PENDIENTES DEL PROPIETARIO**

## 1. Problema original (hallazgo H-03)
La guarda anterior solo comprobaba que **quien ejecuta declaró** `cci.validacion_autorizada=SI-CCI-DEV` y `cci.entorno=CCI-DEV`. Quien conectara por error a PROD y declarase DEV no era detenido (demostrado en local: la prueba GD-12 reproduce esa guarda y la ve aceptar un clúster que está en la denylist).

## 2. Mecanismo implementado (`scripts_validacion/cci_dev_NO_EJECUTADOS/00_guarda_destino.sql`, incluido con `\ir` por los seis scripts)
1. **Identidad efectiva leída del servidor**, no declarada: `system_identifier` del clúster (`pg_catalog.pg_control_system()`), nombre de la base y presencia de roles de plataforma `supabase_*`. Cada proyecto de Supabase es un clúster distinto con su propio `system_identifier`.
2. **Allowlist DEV** (`'system_identifier|base'`) y **denylist PROD** (`'system_identifier'`) **literales y versionadas** en el archivo; no se leen de variables de sesión ni de `PGOPTIONS` (probado: GD-07a/b). Cambiarlas exige un cambio revisable en git.
3. **PROD se rechaza aunque se declare DEV** y aunque también figure en la allowlist (GD-02, GD-04). Destino desconocido → rechazo (GD-03). Identidad no verificable (p. ej. sin permiso sobre `pg_control_system()`) → rechazo, falla cerrada (GD-05). Configuración incompleta o inválida → rechazo (GD-06).
4. **Anti-suplantación:** la guarda fija `search_path` a `pg_catalog` y califica sus funciones; una función `public.pg_control_system()` suplantada no la engaña (GD-07c; GD-11 demuestra que sin esa defensa sí se burlaría). Un rol de plataforma `supabase_admin` presente en modo local lo rechaza (GD-07d).
5. **Modo local temporal:** exige socket Unix, base `^cci_` y ausencia de roles de plataforma.
6. **Registro del motivo sin secretos:** `NO EJECUTADO [G-…]` con una huella md5 truncada (8 hex) del identificador, nunca el valor completo.
7. Si el archivo de guarda falta, los scripts abortan (`\set ON_ERROR_STOP on` va antes de `\ir`; GD-08).

Códigos: G-CONFIG-INCOMPLETA, G-CONFIG-INVALIDA, G-IDENTIDAD-NO-VERIFICABLE, G-PROD-RECHAZADO, G-DESTINO-DESCONOCIDO, G-LOCAL-NO-SOCKET, G-LOCAL-BASE, G-LOCAL-ROLES-PLATAFORMA.

## 3. Qué falta y por qué (no se inventa)
Las dos listas versionadas están **vacías**: el propietario no ha entregado los identificadores reales. Mientras tanto el modo CCI-DEV rechaza **todo** destino (G-DESTINO-DESCONOCIDO): falla segura, no se puede ejecutar en CCI-DEV por accidente. Para habilitarlo el propietario debe: (a) obtener `select system_identifier from pg_catalog.pg_control_system();` en CCI-DEV y en CCI-PROD (solo lectura, ejecutado por él), (b) aprobar el cambio de las listas (`'<id>|postgres'` en la allowlist, `'<id>'` de PROD en la denylist), (c) confirmar que el rol de ejecución en CCI-DEV puede ejecutar `pg_control_system()` (si no, la guarda falla cerrada y habría que decidir otra fuente de identidad).

## 4. Límites (declarados)
- No se probó contra Supabase: la lectura de `pg_control_system()` y los roles de plataforma con el rol real de CCI-DEV son supuestos hasta E0.
- Si el propietario registrase un identificador equivocado (p. ej. PROD en la allowlist y no en la denylist) la guarda lo aceptaría: por eso se exige la denylist y la confirmación humana del project ref (P1).
- Restaurar una copia de PROD sobre DEV (o viceversa) conservaría o cambiaría el `system_identifier` según el método; debe revisarse en el procedimiento operativo.

## 5. Estado
Implementada en los seis scripts y probada localmente (resultados en `scripts_validacion/resultados/guarda_destino.txt`, cifras en `INFORME_CIFRAS_DEFINITIVAS.md`). LR-22 queda PARCIALMENTE_RESUELTA: lo técnico está resuelto; falta información del propietario.

## Addendum de la auditoría final independiente (AUD-FINAL-01…05; vigente)
- **Marcador de ejecución completa (antes AUD-G1/AUD-G3):** la guarda crea al final de su bloque la tabla TEMPORAL `pg_temp.cci_guarda_ok`; cada uno de los seis scripts exige que exista justo después de `\ir` y, si no, aborta con `NO EJECUTADO [G-GUARDA-NO-EJECUTADA]`. Una tabla temporal **no puede preinstalarse** por PGOPTIONS ni por variables (la variante anterior, la variable `cci.guarda_ok`, sí podía: AUD-FINAL-02).
- **search_path (AUD-FINAL-01):** el `search_path` blindado de la guarda es **local a su bloque DO**; **no persiste** para las instrucciones posteriores (verificado, matriz SP-04 / GD-15). No se persiste a propósito: las políticas RLS y funciones que los scripts ponen a prueba se resuelven con el search_path de la sesión, y fijarlo a `pg_catalog, pg_temp` las rompe (probado). En su lugar, las funciones del catálogo que invocan los scripts van calificadas con `pg_catalog.` (144 llamadas; GD-19 demuestra que funciones homónimas en un esquema anterior del search_path no se invocan). Límite: operadores y tipos no se califican.
- **Integridad de la guarda (AUD-G2):** el marcador detecta guarda ausente/vacía/truncada/de otra versión; **no** detecta una guarda sustituida o editada que lo cree (límite estructural; matrices INT-06/10/12). Control técnico opcional: `ejecutar_script_verificado.sh <sha256_aprobado> <script.sql> …` verifica el SHA-256 de la guarda contra un valor aprobado **fuera del repositorio** y ejecuta sólo con `-f` y ruta absoluta; sólo protege a quien lo usa (invocar `psql` directamente lo omite). Un hash escrito en el repositorio no es protección independiente.
- **stdin:** `psql < script` resuelve `\ir` desde el directorio actual; una guarda homónima que forje el marcador pasaría (X-07). No se admite stdin.
