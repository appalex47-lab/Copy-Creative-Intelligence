# Limitaciones pendientes
**Resuelto (código corregido y probado localmente, sin Supabase):** F-01, F-02, F-05..F-08, F-10; H-01 y H-02 con las correcciones locales.
**Parcialmente resuelto:** F-03 (hash externo: sólo con envoltorio y registro fuera del repo), F-04 (stdin no soportado).
**Código corregido pero NO probado en Supabase:** toda la guarda (marcador por tabla temporal requiere privilegio TEMP y sesión estable).
**Pruebas que requieren CCI-DEV (sin autorización, no ejecutadas):** `pg_control_system()` y su permiso, TEMP, PGOPTIONS por el pooler, project ref, system_identifier de CCI-DEV y CCI-PROD (no inventados; las listas siguen vacías ⇒ fail-closed), comportamiento de los seis scripts en Supabase.
**Limitaciones estructurales:** guarda sustituida/forjada o listas editadas indetectables sin hash externo; clon/restauración de PROD indistinguible (AG-18); operadores/tipos sin calificar; arnés no paralelizable; independencia de orden no demostrada.
**Decisiones pendientes del propietario (conservan su estado real, sin evidencia de resolución):** las 21 decisiones (todas REQUIERE_APROBACION_DEL_PROPIETARIO; DG-20 recomendada pero no aprobada), Adenda v9 y OD-13 (texto no aportado; no se infiere), custodia del hash externo, si CCI-DEV es clon de PROD, autorización de CCI-DEV, aceptación de Fase 0, inicio de Fase 1. Heredados de V26: 5 controles NO VERIFICADO y 4 PARCIAL.
**Las correcciones locales no están publicadas:** el estado publicado en GitHub (d365a16) conserva F-01/F-02/F-05/F-06.
