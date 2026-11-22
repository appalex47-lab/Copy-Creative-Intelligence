# Informe de auditoría técnica (Fase 0)

> **AVISO DE VIGENCIA (ronda final 2026-11-22; el contenido original no se altera).** Copia previa del expediente (raíz): **histórica / propuesta anterior**. No constituye estado vigente ni acepta Fase 0 ni autoriza Fase 1. Estado vigente y jerarquía de fuentes: `00_INDICE_VIGENTES_E_HISTORICOS.md`, `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` y `auditoria_integral/01_INDICE_MAESTRO_FASE0.md`.

El informe de auditoría browser-only completo (17 secciones, con evidencia de archivo y línea) se conserva **sin modificar** en `anexos/INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md` (SHA-256 `564062605d4a4ec30b7c8af608158b75263b51d8394606b132c2ca40686c1f84`; verificado igual al publicado en la rama pública y al entregado). Este documento lo complementa con lo pedido en la instrucción maestra §3.A y con verificaciones nuevas.

## 1. Partida
Rama `integration/cci-fase1-1-accepted` (local), commit `ffb47bc319db0806250bcecf91d390fa59fa0d70`, árbol limpio. `main` remoto `6a1af24…` sin cambios. Detalle en `14_ESTADO_GIT_Y_OPERACIONES.md`.
## 2. Estructura y componentes
389 archivos versionados; `src/` ~30 archivos (domain 1, services 8 + pruebas, app 5, hooks 3, pages 3, components 5, layouts 1, lib 2, styles 2); `tests/` 5; `e2e/` 6; `docs/` 73 archivos (21 vigentes o de Fase 0 raíz y herramientas + 52 en `docs/fase0/historico`); `evidence/` 11 expedientes + `public/`. Detalle del inventario por módulo: informe anexo §3.
## 3. Servicios, tipos, modelos
4 servicios de **lectura** (`identity`, `organizations`, `memberships`, `appState`) con adaptador DEMO en memoria; tipos `UserIdentity`, `Organization`, `Membership`, `AppState`, `Result<T>`, `AppErrorCode` (5). Sin escritura, sin repositorios, sin casos de uso.
## 4. Dependencias
Ejecución: `react`, `react-dom` 19.3.1. Desarrollo: TypeScript 6.0.3, Vite 8.3.8, Vitest 5.1.1, Playwright 1.65.1, axe-core, ESLint 10, Prettier 3.10.1, jsdom 31 (lockfile v3, 262 paquetes). Sin Supabase ni librerías de almacenamiento/validación.
## 5. Pruebas
**Ejecutadas hoy** (ver `13`): 162/162 unitarias y de arquitectura; 29/29 E2E en 3 corridas; typecheck, lint, formato, secretos, build aprobados; `build:production` falla como se espera. Esto **sustituye** la reserva del informe anexo («no se ejecutaron pruebas»), que se refería a esa auditoría; las cifras antes citadas de expedientes quedan confirmadas.
## 6. Documentación y evidencia histórica
Conciliación completa en `03`. Los expedientes `evidence/` son evidencia válida de la **infraestructura**; no prueban funcionalidad de producto.
## 7. Funcionalidades reales / parciales / prototipos / inexistentes
Ver `02_INVENTARIO_FUNCIONALIDADES.md`: la fundación está comprobada; el producto (9 módulos y persistencia) **no existe**.
## 8. Observaciones nuevas respecto del informe anexo
1. La instrucción maestra incorpora la entidad **Campaña**, que la decisión F11-D5 del trabajo aceptado había **retirado** (`Project`): se registra como contradicción histórica (ver `entregables_formales/CONCILIACION_D1_D9_VERIFICADA.md` y Q-7).
2. Para el «Command Center con actividad real» falta una entidad de **evento de actividad** que no está en la lista del propietario (propuesta en `06`).
3. La corrección ortográfica determinista y la auditoría visual de jerarquía/congruencia plantean límites técnicos (diccionario; IA/visión) documentados en `09`.
4. El valor «versión» del `package.json` y el `ROADMAP.md` usan la numeración antigua (K19, K20).
## 9. Límites de esta auditoría
Sin `npm audit`; sin CI real; comportamientos de navegador (cuotas, Web Locks, expulsión) no verificados; una sola máquina/Chrome.
