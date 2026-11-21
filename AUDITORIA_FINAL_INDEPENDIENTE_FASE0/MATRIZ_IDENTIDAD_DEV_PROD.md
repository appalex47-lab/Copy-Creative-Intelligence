# Matriz de identidad DEV/PROD
Dos clústeres PostgreSQL reales y distintos (C1 = DEV registrado, C2 = PROD en denylist), mismo archivo de guarda.
| Caso | Descripción | Scripts | Estados (corregido) | Estados (publicada) | Esperado | Observado |
|---|---|---|---|---|---|---|
| ID-01 | DEV real (clúster 1 en allowlist) con variables DEV: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | PASA | [('PASA', 6)] |
| ID-02 | identidad DEV DECLARADA contra el servidor PROD (clúster 2 en denylist): 01_inventario_esquema_ | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-PROD-RECHAZADO | [('RECHAZA:G-PROD-RECHAZADO', 6)] |
| ID-03 | servidor NO registrado (ni allow ni deny) con variables DEV: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| ID-040 | allowlist con entrada vacía '': 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| ID-041 | allowlist con entrada '\|': 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| ID-042 | allowlist con sólo sysid sin base: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| ID-043 | allowlist con mayúsculas en la base: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| ID-044 | allowlist con espacio sobrante: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| ID-045 | allowlist con otra base: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| ID-046 | allowlist con sysid con ceros a la izquierda: 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-DESTINO-DESCONOCIDO | [('RECHAZA:G-DESTINO-DESCONOCIDO', 6)] |
| ID-05 | rol sin EXECUTE en pg_control_system(): 01_inventario_esquema_SOLO_LECTURA | 6 | {'PASS': 6} | {'PASS': 6} | RECHAZA:G-IDENTIDAD-NO-VERIFICABLE | [('RECHAZA:G-IDENTIDAD-NO-VERIFICABLE', 6)] |
| ID-06 | AG-18 clon/restauración física: servidor con el MISMO system_identifier y base que el DEV regis | 6 | {'PARTIAL': 6} | {'PARTIAL': 6} | NO distinguible: la guarda PASA (limitación estructural; sól | [('PASA', 6)] |

- **Identidad DEV declarada contra servidor PROD (ID-02):** rechazada con `G-PROD-RECHAZADO` en los 6 scripts. **Servidor no registrado (ID-03):** `G-DESTINO-DESCONOCIDO`.
- **Entradas degeneradas de la allowlist (ID-04x):** vacía, `|`, sólo sysid, mayúsculas, espacio, otra base, ceros a la izquierda ⇒ rechazo (comparación exacta; no hay normalización).
- **Rol sin EXECUTE en `pg_control_system()` (ID-05):** `G-IDENTIDAD-NO-VERIFICABLE`.
- **AG-18 / ID-06 clon o restauración física de PROD como DEV: la guarda NO puede distinguirlos** (mismo `system_identifier` y, normalmente, misma base). Clasificado **limitación estructural (PARTIAL), no prueba aprobada**. Si PROD se registra en la denylist, el clon también se bloquea (falla cerrado a costa de bloquear ese DEV); si no, pasa.
- `system_identifier` identifica el **clúster físico**, no el proyecto Supabase; el project ref no se obtiene en el servidor. Valores nulos/vacíos ⇒ rechazo; variables manipuladas ⇒ rechazo (GD-06/07).
