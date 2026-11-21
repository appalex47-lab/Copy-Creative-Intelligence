# Auditoría técnica de la guarda H-03
HEAD auditado: `d365a162e54809f3b8de9c77f5902a8ea131a97f` (rama `audit/fase0-remediaciones-h01-h02-h03`); guarda publicada SHA-256 `07c6673cc7f6cd4beebcb261eeea6e3ab1c4dbc99fe7dc8021b707607016e5a9`; guarda corregida localmente `b30a39d9d6dac4974913bf7140a619d1991b599a0c0d12af504f9af0906eb1ec`.
## Diseño (revisado en el código real)
`00_guarda_destino.sql` se incluye con `\ir` tras `\set ON_ERROR_STOP on` (única instrucción previa) en los 6 scripts. Un bloque `DO` (1) fija `search_path` local a `pg_catalog, pg_temp`, (2) valida variables, (3) lee `system_identifier` con `pg_catalog.pg_control_system()` y falla cerrado si no puede, (4) aplica denylist antes que el modo, allowlist `sysid|base` en modo DEV o reglas locales (socket, base `^cci_`, sin roles de plataforma), (5) crea el marcador. Listas literales y vacías ⇒ todo destino se rechaza.
## Hallazgos de esta auditoría (ver REGISTRO_HALLAZGOS.md)
- **4.1 search_path:** local al bloque DO; no persiste (probado). Defecto F-01 y su corrección (calificación `pg_catalog.`). Ver MATRIZ_PERSISTENCIA_SEARCH_PATH.md.
- **4.2 integridad:** marcador GUC preinstalable (F-02, corregido con tabla temporal). Una guarda sustituida/forjada o editada sigue pasando (límite estructural): sólo el hash externo la detecta; el pin documental no es protección independiente (AUD-G2). Ver MATRIZ_INTEGRIDAD_GUARDA.md.
- **4.3 identidad:** `system_identifier` identifica el clúster físico; AG-18 (clon) es indistinguible ⇒ limitación estructural, no aprobación. Declarar DEV contra el servidor PROD (denylist) rechaza en los 6 scripts. Ver MATRIZ_IDENTIDAD_DEV_PROD.md.
- **4.4 seis scripts:** cada uno invoca la guarda en una línea fija, sin DDL/DML previo, aborta con rc=3, y un rechazo no deja cambios persistentes (persist.py). Ver MATRIZ_SEIS_SCRIPTS.md.
## Veredicto técnico
Con las correcciones locales: guarda **correcta en PostgreSQL local, fail-closed** ante ambigüedad; **no demostrada en Supabase**; con límites estructurales. Sin las correcciones (estado publicado): dos defectos altos reproducidos.
