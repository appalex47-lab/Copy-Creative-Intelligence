# Diseño de persistencia local (propuesta; nada implementado)
## 1. Reparto de almacenamiento
| Dato | Almacén | Justificación |
|---|---|---|
| Todas las entidades de §06, versiones, eventos, metadatos | IndexedDB | volumen, relaciones, índices, transacciones |
| Esquema, instancia, fecha del último respaldo (fuente) | IndexedDB `meta` | atómico con los datos |
| Preferencias ligeras (tema, idioma, última vista, avisos vistos, copia de la fecha de último respaldo) | Local Storage `cci.prefs.v1` | sincrónico, pequeño, descartable |
| Secretos, claves de IA, contenido, borradores, exportaciones | **ninguno** | no se persisten |
Local Storage **no** se convierte en una base paralela: solo valores escalares y objetos pequeños de interfaz, validados al leer (valor corrupto → valor por defecto).

## 2. Base de datos
BD única `cci`, versión entera (`schemaVersion`). Un único módulo propietario del esquema. Almacenes (object stores) y claves:
| Store | keyPath | Índices |
|---|---|---|
| `meta` | `key` | — |
| `settings` | `key` | — |
| `campaigns` | `id` | `status`, `updatedAt`, `archivedAt` |
| `products` | `id` | `name` |
| `offers` | `id` | `campaignId`, `validTo` |
| `briefs` | `id` | `campaignId`, `status` |
| `copies` | `id` | `briefId`, `campaignId`, `status`, `updatedAt` |
| `variants` | `id` | `copyId` |
| `versions` | `id` | `[entityType+entityId]`, `[entityType+entityId+number]` (único) |
| `rules` | `id` | `scope`, `enabled` |
| `activity` | `id` | `createdAt`, `entityId` |
| (F3) `pieces`, `audits`, `findings`; (F4) `channels`, `adaptations`; (F5) `approvals`, `results`, `tags` | `id` | según entidad |
| (si P5=sí) `blobs` | `id` | `ownerId` |
Los stores de F3–F5 se añaden por **migraciones**, no desde el inicio (evita esquema especulativo).

## 3. Transacciones e integridad
- Operación de negocio = una transacción `readwrite` sobre todos los stores afectados; commit atómico; nunca `await` externo dentro de la transacción.
- IndexedDB no impone claves foráneas: los repositorios verifican existencia de referencias dentro de la misma transacción; borrar = archivar (`archivedAt`) salvo purga explícita con confirmación.
- `revision` entero para control optimista; escritura con revisión obsoleta → `conflict`.
- `versions` es append-only; el contenido aprobado no se sobrescribe: se crea una versión nueva y se registra motivo.
- Utilidad de verificación de consistencia (referencias huérfanas, versiones faltantes, duplicados) ejecutable por el usuario y tras importar/migrar.

## 4. Versionado de esquema y migraciones
- `onupgradeneeded` ejecuta migraciones **secuenciales** vN→vN+1 registradas en una lista ordenada; cada una es idempotente, determinista y tiene pruebas con datos semilla de la versión anterior.
- Antes de migrar: se ofrece exportar; si la BD tiene versión **mayor** que la app, no se abre en escritura (modo bloqueado con aviso).
- Cada registro importable lleva el `schemaVersion` del archivo, no del registro.

## 5. Errores y recuperación
Distinguir `QuotaExceededError`, `AbortError`, `VersionError`, `InvalidStateError`, bloqueo (`onblocked`/`onversionchange`), almacenamiento no disponible (modo privado, política del navegador). Mapeo a `AppErrorCode` (§05). Ante aborto la UI conserva el borrador en memoria y muestra el error; **no** declara éxito.
Cierre inesperado: transacciones incompletas se revierten; lo no persistido en memoria se pierde → autoguardado de borradores como `Copy` en estado Borrador cada N segundos de inactividad (decisión de diseño a confirmar en Fase 2).

## 6. Concurrencia (P12)
Pestañas múltiples: `onversionchange` cierra la conexión y recarga; escritura protegida por `revision`; propuesta: bloqueo exclusivo por Web Locks (si está disponible) o aviso «abierta en otra pestaña» y modo solo lectura. Sin garantía de orden entre pestañas sin coordinación.

## 7. Volumen y límites
Texto y metadatos: muy por debajo de límites prácticos. Binarios (Piezas creativas, F3) son el riesgo: cuota por origen variable según navegador y disco (**no verificada aquí**). Estado real del almacenamiento (Fase 1 lo muestra) mediante `navigator.storage.estimate()`; solicitud `navigator.storage.persist()` (petición, no garantía).

## 8. Seguridad del almacenamiento
Sin cifrado por la aplicación; accesible a cualquier script del mismo origen y a quien tenga el perfil del navegador. El almacenamiento es por **origen**, no por ruta: requiere origen propio (P10). Cifrado opcional con frase de paso (P7) no mitiga XSS ni extensiones.

## 9. Pruebas de persistencia requeridas (definidas, no ejecutadas)
Repositorios contra adaptador en memoria; persistencia real en navegador (Playwright); migraciones con datos semilla; aborto de transacción; cuota llena (simulada); recarga y reinicio; multi-pestaña; consistencia tras importar/migrar.
