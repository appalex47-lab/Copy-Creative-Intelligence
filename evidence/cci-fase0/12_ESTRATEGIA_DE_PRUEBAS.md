# Estrategia de pruebas (vigente propuesta)
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
