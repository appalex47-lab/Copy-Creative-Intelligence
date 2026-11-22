# Hallazgos originales autorizados (auditoría independiente de Fase 1.0)
1. MEDIO — `check:secrets` no detectaba `.env`/`.env.local` en la raíz (APP_PATHS no incluía la raíz); la prueba "sin .env" daba falsa seguridad; patrones limitados (sin Cohere).
2. MEDIO — la prueba de arquitectura solo veía `from '...'`; un `import('@supabase/…')` dinámico pasaba.
3. MEDIO — `HomePage` sin try/catch (carga permanente ante excepción), `ConnectionPage` ignoraba `Result` fallidos, sin Error Boundary.
4. BAJO — `src/types/` no existía tras clonar aunque la documentación decía lo contrario.
Fuera de alcance (no tocados): 5 (inconsistencia memberships DEMO), 6 (accesibilidad más allá de lo necesario para estados), 7 (lint de .mjs, cobertura de patrones, cwd), 8 (guarda producción+DEMO, LICENSE, CI).
