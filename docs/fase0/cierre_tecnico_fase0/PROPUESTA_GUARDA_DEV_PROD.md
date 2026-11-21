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

## Addendum AUD-G1 / AUD-G3 (auditoría independiente de la guarda, 2026-11-21)
- **Hallazgo:** si `00_guarda_destino.sql` quedaba vacío o truncado, `\ir` no fallaba y los seis scripts corrían sin guarda (un archivo ausente sí abortaba). Lo mismo con ejecución por stdin y un archivo homónimo vacío en el directorio actual.
- **Corrección incorporada:** la guarda pone `cci.guarda_ok=''` al inicio y `'1'` sólo si todas las reglas pasan; cada uno de los seis scripts exige `cci.guarda_ok='1'` justo después de `\ir` y, si no, aborta con `NO EJECUTADO [G-GUARDA-NO-EJECUTADA]`. Pruebas GD-13 (18) y GD-14 (6) sobre los seis scripts.
- **Límite residual:** el marcador protege contra guarda vacía/truncada/ausente, no contra la edición dolosa de los propios scripts ni contra un operador que fije `cci.guarda_ok=1` por PGOPTIONS con una guarda ya neutralizada. Control compensatorio: fijar en la aprobación del propietario el SHA-256 de `00_guarda_destino.sql` y ejecutar sólo con `-f` y ruta absoluta.
