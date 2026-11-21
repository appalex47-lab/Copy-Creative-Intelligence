> **ACTUALIZACIÓN DE ESTA PUBLICACIÓN (2026-11-21).** El texto de abajo es la auditoría tal como se emitió. Posteriormente **AUD-G1 y AUD-G3 se corrigieron en el parche publicado**: la guarda deja el marcador `cci.guarda_ok` y cada uno de los seis scripts lo exige tras `\ir` (`[G-GUARDA-NO-EJECUTADA]`). Pruebas nuevas GD-13 (18) y GD-14 (6) → guarda 109/109; los 25 casos AG se repitieron tras la corrección: 25/25 conforme a lo esperado (`evidencia/huecos_AG_post_correccion.txt`; el estado previo está en `huecos_AG_pre_correccion_historico.json`). **AUD-G2 (hash de la guarda) y AUD-G4 (pooler) siguen abiertos.** SHA-256 vigente de `00_guarda_destino.sql`: `07c6673cc7f6cd4beebcb261eeea6e3ab1c4dbc99fe7dc8021b707607016e5a9`. El hash citado más abajo (598ad606…) corresponde a la versión anterior a la corrección y queda como histórico.

---

# Auditoría independiente de la guarda DEV/PROD (H-03) — CCI Fase 0
Fecha: 2026-11-21 · Base: HEAD 5b00848 + parche local H-01/H-02/H-03 (sin publicar) · SHA-256 de 00_guarda_destino.sql auditada: 598ad606071be717070cd4c3031bfd69184e09059406320c4edf25bc3dfe6f08
Restricciones respetadas: sin cambios de código en el parche, sin commits/push/PR, sin conexión a CCI-PROD ni CCI-DEV, sin Supabase real. Todas las pruebas fueron en clústeres PostgreSQL 16 locales (socket Unix).

## 1. Identidad (cómo se obtiene y valida)
| Elemento | Fuente | Evaluación |
|---|---|---|
| system_identifier | pg_catalog.pg_control_system() | Es identidad del **clúster físico**, no del proyecto Supabase. Fuerte si el rol puede ejecutarla; si no, la guarda rechaza (G-IDENTIDAD-NO-VERIFICABLE, probado AG-19). |
| Nombre de base | pg_catalog.current_database() | Sólo se usa **combinado** con sysid (`sysid|base`); nunca solo. Un nombre "development" no autoriza nada (AG-07o, AG-17). |
| Roles de plataforma | pg_roles (supabase_admin, etc.) | Sólo en modo local-temporal para impedir que un servidor tipo Supabase pase como local. No es parte de la allowlist DEV. |
| Variables cci.* (PGOPTIONS) | current_setting | Son **intención declarada**, nunca identidad. Con listas vacías, declarar DEV no abre nada (AG-01). |
| Allowlist / denylist | literales en el archivo | No se leen de variables de sesión (inyección por PGOPTIONS rechazada, GD-07a/b). Entregadas **vacías**: todo destino se rechaza. |
| Identificador de proyecto Supabase / rol de conexión | no se obtienen en servidor | **Brecha de diseño**: la guarda no ve el project ref ni el rol esperado. Se cubre con sysid+base y verificación E0 del propietario. |

Conclusión: la combinación sysid+base con denylist de PROD precedente es suficiente para distinguir CCI-DEV de CCI-PROD **si** sysid de ambos difieren. No lo es si DEV es clon físico/restauración de PROD (AG-18: mismo sysid y base ⇒ indistinguible; falla hacia cerrado sólo vía denylist con el sysid de PROD, lo que además bloquearía ese DEV). Requiere confirmar que CCI-DEV y CCI-PROD tienen sysid distintos.

## 2. Compatibilidad Supabase
Ver MATRIZ_COMPATIBILIDAD_SUPABASE.md. Sin verificación real: no se afirma nada sobre permisos de pg_control_system() en Supabase.

## 3. Pruebas
85 pruebas del parche + 25 casos de huecos añadidos por esta auditoría (ver MATRIZ_PRUEBAS_SEGURIDAD_GUARDA.md). Resultado: 1 hueco real, 1 límite de diseño, 0 bypass vía variables, search_path, base, privilegios, flags de psql.

## 4. Hallazgos
- **AUD-G1 (ALTO, hueco real): guarda vacía/truncada ⇒ scripts sin guarda.** `\ir` de un archivo vacío no falla y los scripts no verifican que la guarda se ejecutó. AG-02/03/04: los 6 scripts corren sin protección (incluye 03/04 con DML+ROLLBACK). Archivo ausente sí aborta (GD-08, AG-12). Mitigación validada en copia fuera del repo (evidencia/PROPUESTA_guarda_con_marcador.sql): la guarda pone cci.guarda_ok='' al inicio y '1' al final; cada script lo exige tras `\ir` (G-GUARDA-NO-EJECUTADA). Con guarda vacía los 3 scripts probados rechazan.
- **AUD-G2 (MEDIO): sin pin de integridad de la guarda.** Un archivo alterado con PROD en la allowlist pasa. Mitigación: fijar el SHA-256 de 00_guarda_destino.sql en la aprobación del propietario y verificarlo antes de ejecutar. El marcador no protege contra edición maliciosa de los propios scripts.
- **AUD-G3 (MEDIO): ejecución por stdin.** `psql < script` resuelve `\ir` desde el cwd: un 00_guarda_destino.sql homónimo (vacío) en el cwd anula la guarda en 01/02 (AG-11). Mitigación: ejecutar sólo con `-f` y ruta absoluta; la corrección AUD-G1 la cubre.
- **AUD-G4 (MEDIO, no verificado): PGOPTIONS a través de Supavisor/PgBouncer.** Si el pooler no reenvía opciones de arranque, las variables cci.* llegan vacías ⇒ G-CONFIG-INCOMPLETA (falla cerrado, sin riesgo, pero inoperable). Modo transacción (6543) pierde estado de sesión; usar conexión directa o modo sesión.
- **AUD-G5 (BAJO/informativo):** huella md5 de 8 hex del sysid en mensajes; riesgo bajo.
- Sin hallazgo: orden denylist→modo, comparación exacta (mayúsculas/espacios no coinciden), search_path por rol/base/PGOPTIONS/pg_temp, función falsa pg_control_system en esquema ajeno, -v ON_ERROR_STOP=0, --single-transaction, ON_ERROR_ROLLBACK.

## 5. Fail-safe
Toda condición ambigua rechaza, salvo AUD-G1/G3 (guarda neutralizada) que hoy **no** falla cerrado. Tras la mitigación AUD-G1 el contrato es completo para archivo vacío/truncado; edición dolosa se controla con el hash (AUD-G2).

## 6. No verificado
Permisos reales de pg_control_system() en Supabase para el rol de conexión; reenvío de opciones por el pooler; si CCI-DEV y CCI-PROD tienen sysid distintos; si CCI-DEV es clon de PROD.
