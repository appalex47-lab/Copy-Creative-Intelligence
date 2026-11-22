# Riesgos y limitaciones restantes
- Accesibilidad: no completa; faltan lectores de pantalla, zoom, alto contraste, otros navegadores y evaluación manual.
- CI no ejecutado en GitHub; acciones sin anclar por SHA; supuesto de Chrome en el runner.
- Las pruebas e2e dependen de Chrome instalado (o `CCI_CHROME_PATH`); `--no-sandbox` en el entorno de pruebas.
- La protección DEMO evita errores de configuración, no es seguridad; cualquiera puede construir otro modo localmente; la seguridad real dependerá de Auth/RLS/backend (no implementados).
- Mientras no exista backend, un build de producción es imposible por diseño (`build:production` falla).
- Escáner de secretos heurístico; ZIP no inspeccionados (2 en la raíz, más ZIP en `docs/fase0` y `ARTEFACTOS_REVISION_PUBLICACION` fuera de alcance); sin análisis del historial de Git.
- Cambios de contrato aditivos (`validation_error`, `environment: 'preview'`); deben validarse contra el diseño de datos definitivo de Fase 0 (no aprobado).
- Integración con `main` (62 commits de Fase 0 heredados) y rama solo local: riesgos de la auditoría independiente siguen vigentes. LICENCIA pendiente. Fase 0 sin aprobar ni cerrar.
- Capturas: solo 2 de 13 inspeccionadas visualmente una a una.
