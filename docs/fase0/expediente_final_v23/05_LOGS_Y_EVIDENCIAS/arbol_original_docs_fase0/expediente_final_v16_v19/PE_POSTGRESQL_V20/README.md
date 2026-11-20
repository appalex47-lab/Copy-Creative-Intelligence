# PE_POSTGRESQL_V20 — pruebas en PostgreSQL temporal (fixture)

**Versión:** V20 · **Fecha:** 2026-11-20 · **Fuente:** reglas IG1-05, IG1-06, IG1-10, IG1-21, IG5-36 (PE-01..PE-05), definición de `channel_formats` (spec sección 3.14 y bloque V20) y de `attribution_discard_resolutions` (spec línea 1118 y siguientes) · **Estado de verificación:** ejecutado.

## Qué es y qué no es
- Un clúster **temporal y aislado** de PostgreSQL 16.15 (binarios ya instalados en el equipo; `initdb` en `/tmp`, socket Unix, sin red, eliminado al terminar). No se usó ningún servicio real, ni Supabase, ni RevNavigator.
- `01_fixture.sql` es un **subconjunto mínimo derivado de la especificación**, escrito para probar las reglas. **No es una migración ni el esquema físico aprobado**; no define RLS ni roles; la clave primaria de `channel_formats` sigue NO DETERMINADA (el fixture usa solo la clave única compuesta).
- No se simuló PostgreSQL con Python ni SQLite.

## Resultados
- `salida_PE_V20_corrida1.txt` y `salida_PE_V20_corrida2.txt`: 63 pruebas, 63 PASS, 0 FAIL; las dos salidas tienen el mismo SHA-256 (1e56d066…509e).
- PE-01 (IG1-05) 5 pruebas; PE-02 (IG1-06) 5; PE-03 (IG1-10) 4; PE-04 (IG1-21) 5; PE-05 (IG5-36, las nueve columnas) 9; `PG-CF-01..15` (channel_formats); `PG-AD-01..20` (attribution_discard_resolutions). Cada prueba parte de un estado válido, se ejecuta en subtransacción y compara el SQLSTATE y el mensaje esperados.
- `salida_PE_V20_mutaciones.txt`: control de sensibilidad, 14 mecanismos del fixture eliminados uno a uno; en las 14 la prueba asociada pasó a FAIL (14/14 detectadas). Las dos primeras ejecuciones del script de mutaciones tuvieron nombres de constraint mal escritos (3 «no detectadas» por error del arnés, no de las pruebas); se corrigieron los nombres y se añadió el aviso «MUTACIÓN NO APLICADA».
- `salida_corrida0_arnes_con_2_FAIL_historica.txt`: primera ejecución, con 2 FAIL por errores del **arnés** (no de las reglas): PE-02d usó una pieza con maestra ya asignada (disparaba antes el trigger de inmutabilidad) y AD-20 esperaba CHECK cuando el trigger de resolución previa se evalúa primero. Se corrigió el caso de prueba (PE-02d con una pieza sin maestra) y la expectativa del mecanismo de AD-20 (la autorreferencia se rechaza igual); no se relajó ninguna otra expectativa. Los identificadores `CF-xx`/`AD-xx` de esa corrida se renombraron después a `PG-CF-xx`/`PG-AD-xx` para no chocar con los casos CF-01..08 del modelo en memoria.

## Límites declarados
- No se implementó el trigger de elegibilidad completa R1–R9 (IG5-95) ni las 12 tablas nuevas restantes; la elegibilidad se cubre en el modelo en memoria (K46/K47).
- Valida que las restricciones **tal como el diseño las declara** son expresables y efectivas en PostgreSQL; **no** valida el esquema físico futuro, RLS, privilegios, concurrencia ni Supabase.
- Para repetirlo contra CCI-DEV: `./ejecutar.sh <socket> <puerto>` solo sobre un clúster temporal; contra CCI-DEV haría falta autorización expresa y un esquema real.
