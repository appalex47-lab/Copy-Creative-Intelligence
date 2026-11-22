# Decisiones arquitectónicas (fundación)

- D1 React + TypeScript estricto + Vite (mandato).
- D2 Contratos tipados + adaptadores intercambiables; DEMO ahora, Supabase futuro no conectado.
- D3 PostgreSQL/Supabase como fuente de verdad; caché local solo después.
- D4 Entornos CCI-DEV y CCI-PROD independientes; no reutilizar RevNavigator.
- D5 TypeScript 6.0.3: 7.x es incompatible con el peer de typescript-eslint (`<6.1.0`).
- D6 Herramientas acotadas a rutas de la app para preservar documentación de Fase 0.
- D7 Navegación por estado (sin router) hasta que existan rutas de producto.

## Pendientes (requieren decisión del usuario)

Modelo definitivo de datos (Fase 0), estrategia de Auth/multi-organización, router, sistema de diseño definitivo, CI.
