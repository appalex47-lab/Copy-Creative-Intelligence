# Hallazgo 6 — accesibilidad
Cambios: enlace «Saltar al contenido» (+`main` con `tabIndex=-1`); aviso DEMO como región con nombre; región de estado persistente `role="status"` (carga → «Contenido cargado.»); errores `role="alert"`; h2 por página con `aria-labelledby` y foco al navegar y tras reintentar; título del documento por página; foco visible 3px; botones de 44px; región JSON enfocable; sin `aria-label` en elementos genéricos; `aria-current` ya existía.
Herramientas: Playwright + @axe-core/playwright (WCAG 2.0/2.1/2.2 A/AA + best-practice) en Chrome real; no se añadió jest-axe ni eslint-plugin-jsx-a11y (redundantes). Pruebas semánticas en jsdom (6) como complemento.
Resultado axe: 0 violaciones en Inicio, Estado de conexión y estado de error (tras las correcciones). Defectos que axe/navegador encontraron y se corrigieron: `target-size` (botón Reintentar), enlace de salto sin destino enfocable.
NO resuelto/NO verificado (no se declara accesibilidad completa): lectores de pantalla reales, zoom 200–400 %, alto contraste, otros navegadores, evaluación manual WCAG. Ver `docs/architecture/ACCESIBILIDAD.md`.
Resultado: PASS (alcance automatizado) con limitaciones.
