# Arquitectura browser-only

> Documento formal del §14. Fuente de contenido: `../05_ARQUITECTURA_BROWSER_ONLY.md` (sin cambios de fondo). Estado: propuesta para revisión; nada aprobado ni implementado.

Decisión vigente (instrucción maestra §1.1): aplicación web local, un usuario por navegador, sin cuentas/login/autenticación/backend/Supabase/PostgreSQL/SQL/servidor/sincronización; IndexedDB como persistencia principal; Local Storage solo para preferencias ligeras. El backend es evolución futura, **no dependencia**.

## 1. Capas y dirección de dependencias
```
Presentación (React: páginas, componentes, hooks de UI)
   │  solo conoce casos de uso vía useServices()/hooks
Aplicación (casos de uso: orquestan, devuelven Result<T>, ejecutan reglas deterministas)
   │
Dominio (entidades, invariantes, reglas, cálculos puros: descuento, puntuación, longitud)
   │  sin APIs del navegador
Contratos (interfaces de repositorio y de puertos: Clock, Ids, AiProvider, FileSystem)
   │
Repositorios (implementaciones de contratos por entidad)
   │
Adaptadores: persistencia/indexeddb · persistencia/memory (pruebas) · preferencias/localstorage · exportación/importación · integraciones externas (IA: solo puerto)
```
Reglas verificables (ampliación de `tests/architecture.test.ts`, análisis por AST ya existente):
1. La presentación no importa adaptadores, repositorios concretos ni usa `indexedDB`/`localStorage`.
2. Solo `adapters/persistence/indexeddb/` usa `indexedDB`; solo `adapters/preferences/` usa `localStorage`.
3. Dominio y aplicación no importan React ni APIs del DOM/navegador.
4. Ningún módulo usa `fetch`/XHR/WebSocket salvo el adaptador de integraciones externas (y solo si el propietario decide una alternativa de IA con red, P8).
5. Los cálculos de negocio (descuento, puntuación, reglas) viven en dominio como funciones puras; la IA nunca los sustituye.

## 2. Estructura de directorios propuesta (Fase 1; no creada)
`src/domain/`, `src/application/`, `src/contracts/`, `src/repositories/`, `src/adapters/{persistence/indexeddb,persistence/memory,preferences,export,ai}`, `src/ui/` (o `components/`, `pages/`, `layouts/` actuales), `src/app/` (composición), `src/modules/<módulo>/` para agrupar casos de uso y pantallas de cada uno de los 9 módulos. Se reutilizan `hooks/`, `lib/`, `styles/` actuales.

## 3. Qué se conserva del código actual
`Result<T>`/`AppErrorCode` (ampliable), `useAsyncResource`, `ErrorBoundary`, `ServicesProvider`, política de entorno (rediseñada, P9), pruebas de arquitectura, accesibilidad, E2E. El adaptador DEMO queda **solo para pruebas** o detrás de un modo explícito etiquetado, nunca como información operativa del Command Center.

## 4. Flujo de datos (ejemplo: guardar un copy)
UI → caso de uso `SaveCopyVersion` (valida con dominio, ejecuta reglas deterministas) → `CopyRepository`/`VersionRepository` (contratos) → adaptador IndexedDB (transacción única sobre `copies` y `versions`) → `Result<…>` → UI muestra estado real (guardado/error), nunca éxito optimista.

## 5. Errores
`AppErrorCode` actuales + propuestos para persistencia: `storage_unavailable`, `quota_exceeded`, `storage_blocked`, `schema_incompatible`, `integrity_violation`, `import_invalid`, `conflict` (revisión). Ampliación sujeta a P13. Mensajes por código; el detalle interno no se muestra ni se registra con contenido del usuario.

## 6. Evolución futura sin sobrecarga
Los contratos de repositorio permiten otra implementación en el futuro. **No se construye** capa de sincronización, DTOs de red ni «modo backend». La justificación de las abstracciones es probar casos de uso con un adaptador en memoria y aislar el esquema/migraciones de IndexedDB.

## 7. Límites declarados
IndexedDB no es cifrado ni frontera de seguridad; extensiones, malware, acceso físico y borrado por el navegador están fuera del control de la aplicación. No hay multiusuario real ni autorización.
