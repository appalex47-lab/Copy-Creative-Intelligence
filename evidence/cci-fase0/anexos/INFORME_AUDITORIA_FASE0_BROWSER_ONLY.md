# CCI — Auditoría general para redefinir la Fase 0
Arquitectura browser-only · IndexedDB + Local Storage · 2026-11-22

Alcance: solo lectura y documentación. No se modificó código, documentos ni expedientes; no se instalaron dependencias; no se ejecutaron pruebas, build ni consultas a Supabase; no hay commits, ramas, remotos, push, PR, merge ni despliegue. Este informe vive fuera del repositorio.
Método: inspección estática de la rama `integration/cci-fase1-1-accepted` (HEAD `ffb47bc319db0806250bcecf91d390fa59fa0d70`) desde un clon independiente en `/tmp/clon_final_verif`. Las cifras de pruebas «ejecutadas» provienen de los expedientes del repositorio, no de ejecuciones de esta auditoría. Referencias de evidencia entre corchetes: `[ruta:línea]` o `[ruta]`.

---
## 1. Resumen ejecutivo
- CCI hoy es una **fundación técnica** (React 19 + TypeScript estricto + Vite) con 4 servicios de **solo lectura sobre datos ficticios en memoria**, política de entorno, manejo de errores y 2 pantallas. **No existe persistencia de ningún tipo** (cero usos de `indexedDB`, `localStorage`, `sessionStorage`, `fetch`, `XMLHttpRequest` ni `WebSocket` en `src/`). No hay funcionalidad de producto [`docs/product/README.md`].
- La arquitectura en capas (dominio → contratos → adaptadores → UI vía `useServices()`), el tipo `Result<T>`, la política de entorno, el manejo de errores, la accesibilidad y la infraestructura de pruebas **se conservan** y encajan con la nueva decisión.
- **No existe ninguna dependencia técnica de Supabase/PostgreSQL en el código ni en `package.json`** (verificado). La dependencia es **conceptual y documental**: comentarios, modo `supabase` rechazado, guardas ESLint/AST, y sobre todo documentos que declaran a PostgreSQL/Supabase como «fuente de verdad» (contradicen la nueva decisión).
- Lo que **hay que rediseñar** es el modelo: `Organization`, `Membership`, roles, `UserIdentity` y `DataOrigin 'backend'` presuponen multiusuario/servidor. Con un solo usuario por navegador y sin cuentas, su destino es una **decisión del propietario**.
- Hay **59 archivos de Fase 0** en `docs/fase0/` (52 de ellos históricos) centrados en 41 tablas, RLS, Edge Functions y 17 permisos de servidor; **Fase 0 no está aprobada**. Se conservan como histórico; su modelo de entidades de producto puede informar el dominio local, pero no su capa de seguridad de servidor.
- Se propone una Fase 0 redefinida **única** (sin subfases), un roadmap general y 15 decisiones del propietario. Dictamen: **LISTO CON LIMITACIONES DOCUMENTADAS** (§17). No equivale a aceptar Fase 0.

---
## 2. Estado real del repositorio
| Dato | Valor | Evidencia |
|---|---|---|
| Rama / HEAD | `integration/cci-fase1-1-accepted` / `ffb47bc319db0806250bcecf91d390fa59fa0d70` | `git rev-parse` |
| Estado | limpio, 0 entradas (incl. ignorados) | `git status --porcelain --ignored` |
| Historia | 26 commits; 5 sobre `7bcba74` (B1–B3, docs B5, corrección E2E, 2 expedientes) | `git log` |
| Publicación | la rama es **local**; `main` remoto = `6a1af2424ef3…`; no existe `integration/*` en GitHub | `git ls-remote` (lectura) |
| Versión declarada | `0.0.0-fase1.0-fundacion` | `package.json` |
| Remoto del clon | `origin` = clon local `/tmp/preserve_repo` (no GitHub) | `git remote -v` |

**Discrepancias documentales detectadas (no corregidas):**
1. `docs/roadmap/ROADMAP.md` dice que Fase 1.0 está «pendiente de aceptación formal» y que 1.1+ está «por definir»; la aceptación del propietario (1.0, 1.1-A, 1.1-B B0–B5, corrección E2E) consta en la conversación y en expedientes, no en el roadmap del repo.
2. `README.md` y `docs/decisions/DECISIONES.md` describen Supabase/PostgreSQL como destino; `README.md` indica «Fase 1.0 en construcción».
3. `docs/product/README.md`: sin funcionalidades de producto; no hay definición de dominio de producto en el código.

---
## 3. Inventario técnico
**Pila:** React 19.3.1, react-dom 19.3.1 (únicas dependencias de ejecución); dev: TypeScript 6.0.3, Vite 8.3.8, Vitest 5.1.1, jsdom 31, Testing Library, Playwright 1.65.1 (+ axe-core), ESLint 10, Prettier. Lockfile v3 con 262 paquetes. Node ≥ 22.22.2. Sin librería de almacenamiento (`idb`, `dexie`…) ni de validación (`zod`…) [`package.json`].
**Configuración:** `tsconfig.app.json` con `strict`, `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`, target ES2023. `vite.config.ts` con plugin `cci-env-guard`. Scripts: `dev`, `build` (= `tsc -b && vite build --mode preview`), `build:production` (**falla a propósito**), `verify`, `test:run`, `test:e2e`, `check:secrets`. `playwright.config.ts` usa solo Chrome (`channel: 'chrome'`).
**Código (`src/`, ~30 archivos):**
| Módulo | Qué hace realmente | Evidencia |
|---|---|---|
| `domain/entities.ts` | `UserIdentity`, `Organization`, `Membership` (roles no vacíos), `AppState`, `DataOrigin 'demo'\|'backend'` | `[src/domain/entities.ts]` |
| `services/contracts/` | `Services` = identity, organizations, memberships, appState (todo **lectura**); `Result<T>`, 5 `AppErrorCode` | `[src/services/contracts/services.ts]`, `[result.ts]` |
| `services/adapters/demo/` | Datos ficticios en memoria + validación de integridad referencial y de roles al crearse | `[fixtures.ts]`, `[demoServices.ts]` |
| `services/index.ts` | `createServices(env)`: único caso `'demo'` | `[src/services/index.ts]` |
| `app/` | `envPolicy.ts` (pura), `env.ts`, `App.tsx`, navegación por estado | `[src/app/*]` |
| `hooks/` | `ServicesProvider`/`useServices`, `useAsyncResource` (loading/success/error, descarte de respuestas tardías) | `[src/hooks/*]` |
| `pages/` | `HomePage` (identidad, organizaciones, membresía propia), `ConnectionPage` (estado) | `[src/pages/*]` |
| `components/`, `layouts/`, `lib/` | `ErrorBoundary`, `StatusNotices`, `NavMenu`, `DemoBanner`, mensajes por código de error | `[src/components/*]`, `[src/lib/errorMessages.ts]` |
| `features/`, `types/` | vacíos (`.gitkeep`) | `[git ls-files]` |

**No hay** capa de casos de uso, repositorios, escritura/creación de datos, rutas, estado global ni persistencia. Las funciones «de producto» (copy, auditoría de piezas) **no existen**.
**Documentación vigente de la app:** `docs/architecture/` (10), `docs/decisions/` (2), `docs/roadmap`, `docs/product`. **Fase 0:** `docs/fase0/` (59 archivos; 52 históricos). **Expedientes:** `evidence/` (11 expedientes + `public/`), todos con manifiesto SHA-256 que verifica en checkout limpio.

---
## 4. Dependencias de backend encontradas
Clases: **1** necesario para la app local · **2** adaptable · **3** obsoleto para el alcance actual · **4** histórico a conservar · **5** requiere decisión.
Búsqueda: términos supabase, postgres, SQL, auth/sesión, RLS, edge function, service_role/anon, storage, organización/tenant, permisos/roles, fetch/XHR/WebSocket sobre `src`, `tests`, `e2e`, `scripts`, `docs`, `.github`, `database`, `supabase`, `.env.example`.
| # | Hallazgo | Evidencia | Clase |
|---|---|---|---|
| H1 | Ninguna dependencia, import ni llamada de red a Supabase/PostgreSQL en `src/` ni `package.json` | `grep` sin resultados; `[tests/architecture.test.ts:40-46]` | — (hecho) |
| H2 | `fetch/XHR/WebSocket/localStorage/indexedDB`: 0 usos en `src/` | `git grep` | — (hecho) |
| H3 | `DataOrigin = 'demo' \| 'backend'` y `AppState.dataMode: 'demo' \| 'backend'` | `[entities.ts:6,42]` | 2 |
| H4 | `Organization`, `Membership`, `roles` (5 claves), `active`; comentario «la autorización real será del backend (RLS)» | `[entities.ts:14-38]` | 5 |
| H5 | `UserIdentity` / `IdentityService.getCurrentIdentity` («se consulta, no se autentica») | `[services.ts:13-15]` | 5 |
| H6 | `Result<T>`, `AppErrorCode`, `describeError`, `useAsyncResource` | `[result.ts]`, `[errorMessages.ts]` | 1 |
| H7 | `VITE_DATA_MODE=demo\|supabase`; `supabase` → `not_implemented`; producción **rechaza DEMO**; `build:production` falla a propósito | `[envPolicy.ts:71-94]`, `[package.json]` | 2 / 5 |
| H8 | `createServices` con un único modo `demo` y comentario «el modo backend (Supabase) se añadirá» | `[services/index.ts:5]` | 2 |
| H9 | Guardas anti-Supabase: ESLint `no-restricted-imports`, prueba AST, `buildGuard`, patrones de `check-secrets` | `[eslint.config.js:40-65]`, `[tests/moduleReferences.test.ts]`, `[scripts/check-secrets.mjs:23-38]` | 2 (decidir si se conservan como control genérico de dependencias de backend) |
| H10 | `.env.example`: `VITE_SUPABASE_URL/ANON_KEY` comentadas | `[.env.example]` | 3 |
| H11 | `supabase/README.md` (Auth, PostgreSQL, RLS, Edge Functions, Storage; CCI-DEV/PROD) y `database/README.md` | ambos | 3 + 4 |
| H12 | `docs/architecture/INTEGRACION_SUPABASE_ESTADO.md` | | 4 (con aviso de obsolescencia: decisión) |
| H13 | `ARQUITECTURA.md` §«Fuente de verdad»: «PostgreSQL/Supabase será la fuente central; IndexedDB/localStorage solo caché futura» | `[docs/architecture/ARQUITECTURA.md]` | 3 (**contradice** la decisión) |
| H14 | `DECISIONES.md` D2–D4 (Supabase futuro, **D3 PostgreSQL fuente de verdad**, CCI-DEV/PROD) y pendiente «Auth/multi-organización» | `[docs/decisions/DECISIONES.md]` | 3 / 4 / 5 |
| H15 | `ENTORNOS_Y_MODO_DEMO.md`, `README.md` (stack «backend futuro»), `CI.md`/`ci.yml` (negaciones de Supabase) | | 2 / 4 |
| H16 | `docs/fase0/` (59 archivos): 41 tablas, 231 reglas, 780 escenarios, 17 permisos, RLS, Edge Functions, `transition_piece_status` («el backend es la autoridad», P5); **no aprobada** | `[docs/fase0/ESPECIFICACION_TECNICA_G1_G5_G10.md:50,104]` | 4 / 5 |
| H17 | Expedientes `evidence/` (D1–D9, R1–R9, T-xx, RJ001–RJ010, SQLSTATE propuestos) | `[evidence/CCI_FASE1_1_*]` | 4 |
| H18 | Filtro de membresía en `HomePage` (solo presentación; no es autorización) | `[HomePage.tsx:48-49]`, `[ARQUITECTURA.md]` | 2 |
| H19 | Conceptos «sesiones», «RLS», «Auth» en comentarios de `envPolicy.ts`, `vite.config.ts`, `entities.ts` | | 2 |
No se eliminó ni se propone eliminar contrato ni documento histórico.
**¿Se conservan los modelos y servicios mediante adaptadores locales?** Los **contratos de lectura** pueden implementarse con un adaptador local (IndexedDB) sin tocar la UI. Pero **no bastan**: son de solo lectura, carecen de escritura/casos de uso, y su entidad central (`Organization`/`Membership`) pierde sentido con un solo usuario sin cuentas. Se recomienda **rediseñar el modelo de dominio** (decisión P1/P4) y **reutilizar** el patrón (contratos + `Result` + inyección).

---
## 5. Elementos reutilizables
Estructura en capas y su prueba AST (`tests/architecture.test.ts`) · `Result<T>`/`AppErrorCode` con prueba exhaustiva · `useAsyncResource` · `ErrorBoundary` · política de entorno pura compartida por build y ejecución · inyección `useServices()` · `check-secrets` · tests de accesibilidad (axe) y resiliencia E2E · infraestructura de expedientes con SHA-256 · tsconfig estricto · patrón «adaptador DEMO se niega a crearse si sus datos son inconsistentes» (aplicable a validar datos importados).
## 6. Elementos que necesitan adaptación
`entities.ts` (H3–H5) · `createServices` y `VITE_DATA_MODE` (nuevo modo local) · regla «producción rechaza DEMO» y `build:production` fallido (H7) · contratos (añadir escritura y casos de uso) · `AppState` y `ConnectionPage` (hoy dice «sin persistencia») · documentos H13–H15 · `ROADMAP`/`README`.
## 7. Elementos fuera de alcance (conservados, no tocados)
Backend, Supabase/PostgreSQL/SQL/RLS/Edge Functions/Storage, CCI-DEV/CCI-PROD, multiusuario, sincronización, `docs/fase0/` y expedientes históricos.

---
## 8. Arquitectura propuesta
```
UI (React: pages / components)            -- no conoce IndexedDB
   ↓ useServices()
Casos de uso (application)                 -- orquestan reglas; devuelven Result<T>
   ↓
Dominio (entidades, invariantes, validadores)  -- sin dependencias de navegador
   ↓ puertos
Repositorios (interfaces)                  -- p. ej. PieceRepository, BackupService
   ↓
Adaptadores: indexeddb/ · memory/ (pruebas) · demo/ (existente)
Preferencias: PreferencesStore → adaptador localStorage
Exportación/Importación: módulo propio (formato versionado, validación, integridad)
Integraciones externas: puerto AiProvider (sin implementación en Fase 0)
```
- **Justificación de la abstracción:** no es por un backend hipotético, sino por (a) probar casos de uso sin navegador con un adaptador en memoria, (b) aislar el esquema de IndexedDB y sus migraciones, (c) mantener la regla ya probada «la UI no importa adaptadores». Es una evolución del patrón existente, no complejidad nueva.
- **No incluir** capa de sincronización, colas de red, DTOs de servidor ni «modo backend».
- **Reglas verificables:** ampliar `tests/architecture.test.ts` para que solo `services/adapters/indexeddb/` use `indexedDB` y solo el adaptador de preferencias use `localStorage` (propuesta; no existe hoy).
- **Brecha actual:** no existe la capa de casos de uso ni `src/application/`; la UI llama a servicios directamente (aceptable mientras sean lecturas).

---
## 9. Diseño de persistencia local (propuesta; nada implementado)
### 9.1 IndexedDB (almacenamiento principal)
- **Base:** una única BD `cci` con versión entera creciente; un solo propietario del esquema.
- **Object stores candidatos** (sujetos a P4; basados en el diseño documental de Fase 0, que menciona `brand_guidelines`, piezas, `copy_versions`, `assets`/`asset_versions`, revisiones, `publication_attempts`): `meta` (clave: `schemaVersion`, `instanceId`, `lastExportAt`), `workspace` (registro único; sustituye a usuario/organización si P1 lo decide), `brand_guidelines`, `pieces`, `copy_versions`, `assets`, `asset_versions`, `reviews`, `event_log`. Las entidades definitivas **no están aprobadas**.
- **Claves e índices:** `id` UUID generado en cliente (`crypto.randomUUID`); índices por `pieceId`, `status`, `updatedAt`, `createdAt`; relaciones por id (sin integridad referencial nativa en IndexedDB → la imponen los casos de uso/repositorios).
- **Transacciones:** `readwrite` sobre todos los stores implicados en una operación de negocio; el commit es atómico (si falla o el navegador cierra, se aborta). Operaciones multi-entidad en una sola transacción; no esperar `await` externos dentro de una transacción (se auto-confirma).
- **Integridad:** validación en el repositorio antes de escribir; campo `revision` entero para control optimista; comprobación de referencias en transacción; verificador de consistencia invocable (utilidad de «reparar/diagnosticar»).
- **Versionado y migraciones:** `onupgradeneeded` con migraciones secuenciales vN→vN+1, cada una idempotente y probada; antes de migrar, **ofrecer exportación**; si la BD tiene versión **mayor** que la app, **no abrir en escritura** y avisar.
- **Errores:** distinguir `QuotaExceededError`, `AbortError`, `VersionError`, `UnknownError`, BD bloqueada (`onblocked`) y modo privado/almacenamiento no disponible; mapear a `AppErrorCode` existentes o ampliarlos (decisión P13).
- **Interrupciones:** una transacción incompleta se revierte; los datos **en memoria no guardados** (borradores) se pierden → definir autoguardado de borradores como entidad persistida (decisión).
- **Concurrencia entre pestañas:** `onversionchange` (cerrar y recargar), `revision` optimista, y bloqueo de escritura exclusivo mediante Web Locks API o aviso «ya abierta en otra pestaña» (decisión P12). Sin garantía de orden entre pestañas sin coordinación.
- **Volumen:** texto y metadatos → muy por debajo de los límites; **binarios (imágenes de piezas) son el riesgo** (cuota por origen variable según navegador y disco; **no verificada aquí**). Usar `navigator.storage.estimate()` y solicitar `navigator.storage.persist()` (es una petición, **no garantía**). Decidir en P5 si se guardan binarios o solo referencias.
### 9.2 Local Storage (solo configuración ligera)
- **Sí:** tema, idioma, última pantalla, preferencias de interfaz, banderas «ya vio el aviso», fecha del último respaldo (cache de la de `meta`), clave de versión de preferencias (`cci.prefs.v1`).
- **No:** contenido, borradores, entidades, exportaciones, claves de API, tokens, datos personales. Motivos: API síncrona (bloquea el hilo), solo cadenas, tope típico de pocos MB, sin transacciones, legible por cualquier script del mismo origen.
- Validar al leer (valores corruptos → valores por defecto, nunca excepción).
### 9.3 Qué vive dónde
| Dato | Almacén | Motivo |
|---|---|---|
| Piezas, versiones, activos, revisiones, registro de eventos | IndexedDB | volumen, relaciones, transacciones |
| Versión de esquema, instancia, fecha de último respaldo (fuente) | IndexedDB `meta` | atómico con los datos |
| Preferencias y estado de interfaz | Local Storage | ligero, sincrónico, descartable |
| Secretos/claves | **ninguno** | no se persisten (ver §11) |

---
## 10. Estrategia de respaldo y recuperación
- **Exportar todo:** archivo único con sobre `{ format: 'cci-backup', formatVersion, appVersion, schemaVersion, exportedAt, counts, payload, sha256 }` (hash del `payload` canónico con Web Crypto; **detecta corrupción, no autoría**). Si hay binarios, formato contenedor (decisión P6).
- **Importar:** (1) leer y limitar tamaño; (2) parsear sin evaluar código; (3) validar contra el esquema con validadores propios; (4) comprobar `formatVersion`/`schemaVersion` (rechazar mayores; migrar menores en memoria); (5) verificar `sha256` y conteos; (6) simulacro (dry-run) en memoria; (7) escribir en **una sola transacción** `clear+put` o crear BD temporal y conmutarla → **todo o nada**, nunca importación parcial; (8) tras éxito, verificación de consistencia.
- **Respaldo previo automático:** antes de importar o migrar, exigir/ofrecer una exportación de la copia actual (red de seguridad para «restaurar copia anterior»).
- **Avisos al usuario:** banner permanente con fecha del último respaldo; advertencia si nunca se exportó; texto claro «los datos solo están en este navegador».
- **Escenarios:**
| Escenario | Qué puede garantizar la app | Qué no |
|---|---|---|
| Cierre inesperado | transacciones atómicas | recuperar borradores en memoria no guardados |
| Borrado de datos del sitio | nada (pérdida total) | recuperar sin respaldo manual |
| Cambio de navegador / dispositivo | solo exportar/importar manual | transferir automáticamente |
| Actualización de la app | migración versionada + exportación previa | revertir una migración ya confirmada sin respaldo |
| Datos de versión incompatible | rechazar, no escribir, ofrecer exportar | «arreglar» automáticamente |
- No se promete recuperación automática: el navegador puede **expulsar** el almacenamiento (presión de disco, políticas de rastreo de algunos navegadores; **no verificado aquí**), y `persist()` no es garantía.

---
## 11. Inteligencia artificial y privacidad (alternativas; nada implementado)
| Alternativa | Qué es | Riesgos / límites | Conexión |
|---|---|---|---|
| A. Sin IA remota (reglas locales, plantillas, listas de verificación) | todo offline | capacidad limitada | no |
| B. Llamada directa del navegador al proveedor con clave del propio usuario (BYOK) | la clave se pega en la sesión | **la clave queda expuesta a XSS, extensiones y herramientas de desarrollo**; coste e límites los asume el usuario; el contenido del copy sale del dispositivo; CORS/política del proveedor **no verificados**; no apta para claves de la organización | sí |
| C. Modelo local en el navegador (WASM/WebGPU) | inferencia local | descarga pesada, calidad y rendimiento variables, soporte de navegador **no verificado** | solo para descargar el modelo |
| D. Flujo manual (copiar/pegar prompts y resultados) | el usuario usa el proveedor fuera de la app | fricción; sin riesgo de claves en la app | no |
| E. Integración segura futura (intermediario del lado servidor) | backend futuro | **fuera del alcance actual**; solo evolución potencial | sí |
- **Reglas propuestas (a decidir):** nunca persistir claves en Local Storage ni IndexedDB; si se admite B, mantenerla solo en memoria de la sesión y advertir; informar al usuario qué datos se envían; sin telemetría; la funcionalidad local esencial **no depende** de Internet.
- Costos y límites: dependen de cada proveedor y plan; **no se evaluaron**.

---
## 12. Seguridad y privacidad (aplicación de un usuario por navegador)
| Tema | Estado en el repositorio | Riesgo / recomendación |
|---|---|---|
| XSS | 0 usos de `dangerouslySetInnerHTML`, `innerHTML`, `eval`, `new Function`, `document.write` en `src/` y `index.html` | Hoy no hay contenido de usuario; al renderizar copy del usuario o importado mantener escape de React, prohibir HTML crudo por lint, considerar CSP. Sin CSP declarada hoy |
| Importaciones | no existe | Validar tamaño, esquema y tipos; ignorar claves inesperadas; evitar `__proto__`/`constructor` en objetos; no ejecutar contenido importado |
| Dependencias | 262 paquetes en lockfile; runtime solo React/React-DOM | **`npm audit` no ejecutado** (requiere red/instalación); revisar antes de aceptar |
| Logs | `useAsyncResource` registra solo el tipo de error [`useAsyncResource.ts:44`] | Mantener la regla: nunca registrar contenido del usuario |
| Escáner de secretos | `check-secrets.mjs` heurístico | No sustituye revisión; útil contra fugas accidentales |
| Extensiones del navegador | fuera del control de la app | Pueden leer/alterar la página y, según permisos, los datos del origen |
| Almacenamiento | — | IndexedDB/Local Storage **no están cifrados por la aplicación ni son frontera de seguridad**: accesibles a cualquier script del mismo origen, al usuario del dispositivo y a quien tenga el perfil del navegador |
| **Aislamiento por origen** | hosting no definido | El almacenamiento es **por origen (esquema+host+puerto), no por ruta**. Si CCI se sirviera bajo un origen compartido con otras aplicaciones (p. ej. varias páginas del mismo dominio), podrían ver los datos de CCI. Requiere un origen propio (decisión P10; **no verificado** dónde se alojará) |
- **Amenazas que se pueden reducir:** corrupción accidental (validación + transacciones + hash), importaciones maliciosas (validación estricta), fuga por logs, XSS por HTML crudo, claves persistidas.
- **Fuera del control de la app:** acceso físico, malware en el equipo, extensiones con permisos amplios, borrado por el usuario o el navegador, robo del perfil.
- Cifrado local con frase de paso (Web Crypto) es opcional y no resuelve XSS ni extensiones (P7).
- No se afirma seguridad multiusuario: el filtro de `HomePage` es presentación.

---
## 13. Pruebas existentes y faltantes
**Existentes (declaraciones contadas por `grep`; ejecución reportada por expedientes: 162 pruebas unitarias/de componentes y 29 E2E consecutivas en B4–B5/E2E, no re-ejecutadas aquí):**
| Tipo | Archivos | Declaradas |
|---|---|---|
| Unitarias/componentes (`src/`) | 9 | 73 |
| Arquitectura, secretos, build guard, referencias de módulos (`tests/`) | 4 | 32 |
| E2E (Playwright + axe, resiliencia, responsive) | 3 | 17 |
**Faltantes para la arquitectura local (propuestas; ninguna existe ni se ha ejecutado):**
| Prueba | Observación |
|---|---|
| Unitarias de dominio y validadores | nuevas |
| Contratos/repositorios con adaptador en memoria | nuevas |
| Persistencia real en IndexedDB | jsdom no la incluye; requiere navegador real o un doble (p. ej. `fake-indexeddb`, **dependencia no instalada, requiere decisión**) |
| Migraciones entre versiones | datos semilla por versión |
| Exportación/importación, round-trip, archivos corruptos/incompatibles/truncados | nuevas |
| Integridad y recuperación (aborto de transacción, cuota llena) | nuevas |
| Recarga/reinicio del navegador con datos | E2E nuevas |
| Multi-pestaña (`onversionchange`, bloqueo) | E2E nuevas |
| Rendimiento (volumen, tiempo de apertura/exportación) | nuevas |
| Accesibilidad de nuevas pantallas | ampliar axe existente |
| Compatibilidad entre navegadores | hoy solo Chrome; Firefox/WebKit no configurados |
| Arquitectura: solo el adaptador IndexedDB usa `indexedDB` | ampliar prueba AST |

---
## 14. Propuesta de Fase 0 general (redefinida; una sola fase)
**Objetivo.** Definir y dejar aprobable la arquitectura de CCI como aplicación de un solo usuario, ejecutada íntegramente en el navegador, con persistencia local (IndexedDB + Local Storage), protección de datos por exportación/importación y política de IA/privacidad, conservando lo ya aceptado y sin backend.
**Alcance.** Especificación y decisión; sin desarrollo de producto. Incluye reconciliación documental, modelo de dominio local, esquema físico, formato de respaldo, políticas de seguridad/IA y plan de pruebas. Excluye backend, cuentas, sincronización e implementación.
**Arquitectura objetivo.** §8–§10.
**Decisiones ya confirmadas por el propietario:** un usuario por navegador; sin cuentas, login, autenticación, backend, Supabase, PostgreSQL, SQL, servidor ni sincronización; React + TypeScript + Vite; IndexedDB principal; Local Storage ligero; funciones locales sin depender de servidor; aceptación de Fase 1.0 y 1.1 (con limitaciones documentadas).
**Decisiones pendientes:** §16.
**Entregables (organizados por tema):**
1. Decisión arquitectónica (ADR) que sustituye formalmente las decisiones de fuente de verdad PostgreSQL/Supabase, con histórico conservado.
2. Modelo de dominio local y destino de `Organization`/`Membership`/roles/identidad.
3. Esquema físico IndexedDB (stores, claves, índices, invariantes) y política de migraciones.
4. Especificación de Local Storage (claves, validación, límites).
5. Especificación del formato de exportación/importación, flujo todo-o-nada y manejo de incompatibilidad.
6. Matriz de escenarios de pérdida/recuperación y textos de advertencia.
7. Política de seguridad y privacidad (XSS, importaciones, logs, origen, extensiones).
8. Análisis y decisión de IA (alternativa elegida y reglas).
9. Política de entorno/compilación (qué significa «producción» en modo local) y de dependencias permitidas.
10. Plan de pruebas por tipo, con criterios de aprobación.
11. Matriz de trazabilidad: contratos y documentos vigentes ↔ nueva arquitectura (qué se conserva, adapta, retira como vigente).
12. Roadmap general aprobado.
**Dependencias:** decisiones del propietario; acceso a los documentos de Fase 0 y expedientes (disponibles); definición del dominio de producto (hoy inexistente).
**Riesgos:** dominio de producto indefinido; pérdida de datos por borrado del usuario; binarios y cuota; origen compartido; claves de IA; documentos contradictorios que confundan a revisores; reescritura prematura del modelo.
**Criterios verificables de aceptación:** (a) cada entregable existe, versionado y con SHA-256; (b) ningún documento **vigente** declara PostgreSQL/Supabase como fuente de verdad o dependencia (verificación por búsqueda); (c) cada entidad y store tiene definición completa y trazabilidad a decisión del propietario; (d) el formato de exportación tiene esquema y casos válidos/ inválidos documentados; (e) cada escenario de §10 tiene comportamiento definido; (f) el plan de pruebas enumera cada prueba con tipo, entrada, resultado esperado y estado «no ejecutada»; (g) las decisiones de §16 marcadas obligatorias están resueltas por escrito; (h) expedientes históricos intactos (manifiestos verifican).
**Pruebas requeridas para declarar la fase:** verificaciones documentales y de consistencia (búsquedas, manifiestos, matriz de trazabilidad). Las pruebas técnicas de §13 se **planifican** en esta fase y se ejecutan cuando exista implementación (salvo que el propietario decida incluir una prueba de concepto, P14).
**Condiciones para declarar terminada la fase:** criterios (a)–(h) cumplidos y **aprobación expresa del propietario**. Esta auditoría no la otorga.

---
## 15. Roadmap general actualizado (fases generales; ninguna se marca terminada sin evidencia)
| Fase | Contenido | Estado |
|---|---|---|
| **0 — Redefinición de arquitectura local** | §14 | Propuesta; la fase anterior (diseño de datos y seguridad con PostgreSQL) **no está aprobada** y queda como histórico |
| **1 — Fundación técnica** | Estructura, contratos, DEMO, entorno, pruebas, CI documentado | 1.0 y 1.1 (A, B) **aceptadas por el propietario con limitaciones documentadas** (expedientes en `evidence/`); el `ROADMAP.md` del repo está desactualizado |
| **2 — Persistencia local y protección de datos** | Adaptador IndexedDB, preferencias, migraciones, exportación/importación, recuperación | No iniciada |
| **3 — Capacidades de producto** | Copy y auditoría de piezas, según el dominio que el propietario defina | No iniciada; dominio no definido |
| **4 — Inteligencia artificial** | Según la alternativa decidida | No iniciada; opcional |
| **5 — Endurecimiento y publicación** | Compatibilidad entre navegadores, rendimiento, accesibilidad, seguridad, hosting con origen propio, licencia | No iniciada |
| *Evolución potencial* | Backend/sincronización | **No es dependencia**; solo posibilidad futura |
Estas fases son propuestas generales, no autorizaciones ni subfases de Fase 0.

---
## 16. Decisiones que requieren aprobación del propietario
| # | Decisión | Opciones / nota |
|---|---|---|
| P1 | Destino de `UserIdentity`, `Organization`, `Membership`, roles y `active` | eliminar · reducir a «perfil/espacio local» · conservar roles como etiquetas |
| P2 | Sustituir formalmente D2–D4 de `DECISIONES.md` y la sección «Fuente de verdad» | marcar como históricas |
| P3 | Tratamiento de `docs/fase0/` (41 tablas, RLS, permisos) | archivo histórico · fuente parcial para el dominio |
| P4 | Dominio de producto local y entidades mínimas | hoy no definido |
| P5 | Binarios (imágenes/archivos) dentro de IndexedDB | sí con límites · solo metadatos/referencias |
| P6 | Formato de exportación | JSON · contenedor con binarios · cifrado opcional |
| P7 | Cifrado local con frase de paso | sí/no (no sustituye XSS) |
| P8 | Alternativa de IA (A–E) y política de claves | §11 |
| P9 | Qué es «producción» en modo local; destino de `build:production` y de la regla «producción rechaza DEMO» | redefinir |
| P10 | Hosting y origen (aislamiento del almacenamiento; `file://` vs dominio propio) | decidir antes de implementar |
| P11 | Matriz de navegadores soportados | hoy solo Chrome probado |
| P12 | Política multi-pestaña | bloqueo exclusivo · avisar · permitir con revisión |
| P13 | Política de dependencias (envoltorio de IndexedDB, validación, `fake-indexeddb`) y ampliación de `AppErrorCode` | sin instalar nada hasta decidir |
| P14 | ¿La Fase 0 incluye una prueba de concepto ejecutable? | sí/no |
| P15 | Pendientes previos: licencia, enlace de sesión en el historial, publicación de la rama local, D4 (T-01/T-02), F5/G-1, F6, aprobación de Fase 0 anterior | siguen abiertos |

---
## 17. Dictamen final
**LISTO CON LIMITACIONES DOCUMENTADAS.** (No es aceptación de Fase 0.)
Fundamento: el inventario es completo para el repositorio actual y las conclusiones tienen evidencia de archivo. No se declara persistencia local: **no está implementada ni probada**.
**Limitaciones:** (1) no se ejecutaron pruebas, build ni `npm audit`; las cifras de ejecución vienen de expedientes; (2) comportamientos de navegadores (cuotas, expulsión, Web Locks, soporte de IA local, CORS de proveedores) son conocimiento general **no verificado** aquí; (3) hosting y origen futuros desconocidos; (4) el dominio de producto no está definido, por lo que los stores de §9 son candidatos; (5) la rama auditada es local y no está publicada.
