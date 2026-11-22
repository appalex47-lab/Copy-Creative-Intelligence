# Estrategia de pruebas (vigente propuesta)

> **AVISO DE VIGENCIA (ronda final 2026-11-22; el contenido original no se altera).** Copia previa del expediente (raíz): **histórica / propuesta anterior**. No constituye estado vigente ni acepta Fase 0 ni autoriza Fase 1. Estado vigente y jerarquía de fuentes: `00_INDICE_VIGENTES_E_HISTORICOS.md`, `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` y `auditoria_integral/01_INDICE_MAESTRO_FASE0.md`.

Estados: **definida · ejecutada · aprobada · fallida · bloqueada · no ejecutada**. Una prueba solo es «aprobada» con ejecución registrada.
| Capa | Herramienta existente | Falta |
|---|---|---|
| Dominio y casos de uso | Vitest | casos por invariante y regla (positivos/negativos/frontera) |
| Repositorios | Vitest + adaptador en memoria | contratos compartidos que corran contra ambos adaptadores |
| Persistencia real | — | Playwright con IndexedDB real (y doble de IndexedDB solo si P13 lo aprueba) |
| Migraciones | — | semillas por versión; BD de versión mayor |
| Exportación/importación | — | round-trip, archivos corruptos, interrupción |
| Integridad y recuperación | — | aborto de transacción, cuota llena, recarga |
| E2E, accesibilidad, responsive | Playwright + axe (Chrome) | nuevas pantallas; Firefox/WebKit según P11 |
| Rendimiento | — | volumen de datos y tiempos de apertura/exportación |
| Arquitectura | AST + ESLint | reglas de §05 |
| Seguridad local | `check-secrets` | validación de importación, XSS en contenido de usuario |
Reglas: no reducir alcance para mejorar porcentajes; regresión completa al cerrar cada fase; E2E con ≥3 corridas consecutivas y reporte de intermitencias; evidencia con logs y hashes.
