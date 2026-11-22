# Riesgos y limitaciones restantes
- Hallazgos 5–8 siguen abiertos (fuera de alcance): memberships DEMO inconsistentes, accesibilidad parcial, lint de .mjs/patrones/cwd (el cwd ya quedó resuelto de paso), guarda producción+DEMO, LICENSE, CI.
- El escáner de secretos es heurístico (patrones y asignaciones); puede tener falsos negativos/positivos. No inspecciona contenido de ZIP ni `docs/`.
- El análisis AST no ve especificadores totalmente dinámicos (se rechazan en la UI, pero un adaptador o `app` podrían usarlos); no es un análisis de grafo de dependencias transitivas.
- `console.error` registra solo el nombre del tipo de error; no hay telemetría.
- Riesgos de integración con `main` y de preservación (rama solo local) siguen vigentes; ver el informe de auditoría. Nuevo respaldo: `preservacion_cci_fase1_0/` (nuevo tar de Fase 1.0.1).
- Fase 0 sigue sin aprobarse ni cerrarse.
