# S1.2 — Sistema visual, navegación y accesibilidad: informe de ejecución (parcial)

**Base:** `6b78fe5`. **Perímetro:** autorización del 2026-11-22 20:59; S1.2 activada por la aprobación delegada (decisiones de Claude bajo delegación del propietario; registro en `../CCI_FASE1_S1_0_DECISIONES_DELEGADAS_20261123T033116Z/`).

## 1. Prueba E2E intermitente (F-09 / S1-D06): causa verificada y corregida
- **Reproducción:** la prueba «foco visible…» falló 1 de 30 corridas (`--repeat-each=30`) en el estado base.
- **Sondeo (spec temporal, ya retirado; su salida no se conservó en archivo):** 60 corridas **sin** esperar el montaje de la interfaz → 4 anomalías (3 con el foco en el enlace «Saltar al contenido» y 1 con el foco en `<body>`, `outlineStyle: none`); 60 corridas **esperando** a que la interfaz esté montada → 0 anomalías. Causa: Tab se pulsa antes de que React monte la interfaz (`readyState` ya es `complete`); el Tab se pierde.
- **Corrección:** la prueba espera `status = «Contenido cargado.»` antes de pulsar Tab (la prueba «teclado» ya lo hacía). **Sin reintentos** que enmascaren. Tras el cambio: 60/60 corridas de esa prueba.

## 2. Componentes reutilizables (AC1-04)
- Nuevos: `Button`, `Card`, `EmptyState` (estado vacío explícito, exigido por AC1-11 para el Command Center futuro) con 8 pruebas unitarias y estilos con tokens existentes. **No se conectaron a ninguna vista**: no hay vistas nuevas (S1-D07).
- Galería de pruebas fuera del build (`e2e/gallery.html`, `gallery.tsx`) y `e2e/components.spec.ts`: axe real a 320, 768 y 1440 px sin violaciones, sin desbordamiento horizontal, foco visible ≥ 3 px en cada botón habilitado. **Prueba de mutación:** un botón sin nombre accesible hace fallar axe (`button-name`); retirado después.

## 3. Anchos (S1-D14 / AC1-13)
- `e2e/responsive.spec.ts` incluye ahora 320 px (reflujo WCAG 1.4.10) junto a 360, 375, 390, 768, 1024 y 1440.

## 4. Resultados finales (logs en `logs/`)
- `tsc -b`, ESLint, Prettier, `check:secrets`, build en modo preview: rc 0.
- Vitest: 149 pruebas pasan (base: 130; tras S1.1: 141).
- Playwright: 35 pruebas (base: 29), **3 corridas consecutivas 35/35**, en Chrome for Testing 153.

## 5. Estado frente a los criterios (propuesta de Claude; no aceptación)
| Criterio | Estado observado |
|---|---|
| AC1-01 | Cumple en S1.1 (detector AST + mutación) |
| AC1-02 | Cumple (rc 0 en los tres) |
| AC1-03 | Cumple en lo existente: navegación, foco, enlace de salto; 3 corridas E2E consecutivas sin fallo |
| AC1-04 | Cumple para los 3 componentes nuevos y para las vistas actuales (axe E2E); `NavMenu`, `StatusNotices`, `ErrorBoundary` ya tenían pruebas |
| AC1-13 | **Parcial:** anchos fijados y probados con axe, solo en Chrome for Testing 153; Edge, Firefox y Safari sin probar |

## 6. Qué NO se hizo / límites
- No se crearon vistas nuevas ni se cambió la navegación (S1-D07); la identidad visual sigue marcada «provisional» y no se rediseñó.
- No se tocaron dominio, contratos, adaptadores, `AppErrorCode`, documentación, dependencias ni configuración de herramientas.
- Pruebas diseñadas y ejecutadas por la misma sesión; sin revisión independiente. CI no ejecutado. Solo un navegador. La Fase 1 en su conjunto no está aceptada ni autorizada.
