# PROPUESTA SEGURA PARA DISTINGUIR CCI-DEV DE CCI-PROD (LR-22) — **NO IMPLEMENTADA NI APROBADA**

## 1. Limitación (vigente)
La guarda actual de los scripts (`cci.validacion_autorizada='SI-CCI-DEV'` y `cci.entorno='CCI-DEV'`, pasadas por `PGOPTIONS`) solo prueba que **quien ejecuta declaró** que es DEV. Un operador que conecte por error a PROD y declare DEV no es detenido. En modo local exige socket Unix y base `^cci_`, lo que **no** aplica a Supabase. Detectar «un entorno» no es distinguir DEV de PROD. No se conectó a ningún proyecto para esta propuesta.

## 2. Propuesta (defensa en capas; cada capa la ejecuta el propietario)
1. **Marcador en la base (identidad demostrable):** el propietario crea **solo en DEV** un marcador inmutable, p. ej. `ALTER DATABASE postgres SET cci.entorno_id = '<UUID-DEV>'` (o una tabla `public._cci_entorno(id uuid primary key, nombre text)` con una fila) y registra el UUID por canal seguro. **En PROD no existe ese marcador** (o existe con otro UUID y nombre `PROD`).
2. **El script exige el UUID esperado:** `-v entorno_id_esperado=<UUID-DEV>`; el bloque de guarda compara `current_setting('cci.entorno_id', true)` con la variable y aborta si falta o difiere. Un PROD sin marcador aborta por defecto (*fail-closed*).
3. **Marcador negativo de PROD:** el propietario puede además marcar PROD con `cci.entorno_id='PROD'`; el script aborta explícitamente si lo ve.
4. **Rol sin escritura permanente:** ejecutar con un rol de prueba sin privilegios sobre tablas de negocio salvo los necesarios; los scripts de escritura ya terminan en ROLLBACK.
5. **Confirmación humana del `project ref`:** el propietario registra el `project ref` de DEV en el acta de autorización (P1) y verifica en el panel que la cadena de conexión corresponde.
6. **Credenciales separadas:** ninguna credencial de PROD en el equipo que ejecuta; cadenas de DEV entregadas por canal seguro (P4).
7. **Prueba de la guarda sin tocar proyectos:** en PostgreSQL local con `ALTER DATABASE … SET cci.entorno_id` se puede probar que (a) UUID correcto → pasa, (b) UUID distinto → aborta, (c) sin marcador → aborta. Esta prueba local se puede añadir al smoke cuando el propietario apruebe el mecanismo.

## 3. Límites
Sigue dependiendo de que el propietario cree y registre correctamente el marcador y de que **nunca** exista el UUID de DEV en PROD (p. ej. por restaurar una copia de DEV sobre PROD). Ninguna guarda elimina el riesgo humano; solo lo reduce y lo vuelve auditable.

## 4. Estado
No hay cambios en los scripts (el mecanismo requiere decisión del propietario y objetos en el entorno real). LR-22 sigue VIGENTE; la propuesta es la acción concreta.
