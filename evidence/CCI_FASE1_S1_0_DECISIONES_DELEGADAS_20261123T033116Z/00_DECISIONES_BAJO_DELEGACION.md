# Decisiones S1-D01…D16 tomadas por Claude bajo delegación del propietario

**Fecha:** 2026-11-22 21:28 (hora de Ciudad de México). **Rama:** `fase1/s1-0-auditoria`. **Base:** `c74286b` (resultados de S1.0).

## 1. Naturaleza de este documento
- Estas decisiones **las toma Claude** por delegación expresa del propietario (mensaje del 2026-11-22 21:28: «Yo te doy toda la autoridad para que tú puedas aprobar lo que salga mejor para el desarrollo de esta aplicación, siempre y cuando tú actúes como el especialista…»). **No son decisiones personales del propietario sobre el fondo**; son revocables por él en cualquier momento.
- **Conflicto de interés declarado:** Claude redactó S1.0 y ahora aprueba sus propios resultados. Por eso (a) solo decide lo que la documentación sustenta, (b) deja sin resolver lo que no sustenta, y (c) la aceptación efectiva de S1.1/S1.2 depende de pruebas reproducibles, no de esta aprobación. Ninguna revisión independiente ha ocurrido.
- **Uso mínimo de la autoridad:** se decide lo que S1.1/S1.2 necesitan, más criterios de diseño no vinculantes para fases posteriores. No se amplía el perímetro de la autorización del 2026-11-22 20:59.

## 2. Lo que esta delegación NO se usó para hacer
- No se resuelven C-2, C-3 ni los 10 aplazamientos (P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6): ninguno es necesario para S1.1/S1.2.
- No se autorizan S1.3 en adelante ni la Fase 2; no se acepta la Fase 1; no hay merge ni deploy.
- No se aprueban atributos de entidades, relaciones, estados, flujos ni fórmulas (regla P4.C): la documentación no aporta la necesidad funcional ni la fuente.

## 3. Decisiones
| Id | Decisión de Claude | Estado | Motivo (especialista) |
|---|---|---|---|
| S1-D15 | **Aprobar con cambios** los resultados de S1.0 como diagnóstico factual (F-01…F-12; las interpretaciones etiquetadas siguen siendo hipótesis). **Activar S1.1 y S1.2** dentro del perímetro del 20:59. | APROBADA (delegada) | Los hallazgos están respaldados por logs; el riesgo de arrancar es bajo porque ambas subfases excluyen dominio y persistencia. |
| S1-D01 | Opción (a): dominio y contratos provisionales **intactos y compilando**; no se tocan en S1.1/S1.2. Reemplazo en S1.3 (no autorizada). | APROBADA (delegada) | La autorización excluye el dominio; tocarlo sería ampliar el perímetro. |
| S1-D02 | Dirección: introducir un modo operativo `local` cuando haya persistencia real. **Sin cambios de política de entorno ahora.** AC1-11 sigue bloqueado hasta S1.9. | DIRECCIÓN APROBADA; sin implementación | Un modo `local` sin persistencia sería vacío y no verificable. |
| S1-D03 | Conservar DEMO solo para pruebas y demostraciones identificadas. Sin cambios ahora. | DIRECCIÓN APROBADA; sin implementación | Coherente con P9; sin modo local no hay caso que probar. |
| S1-D04 | Sin limpieza de Supabase en S1.1/S1.2, salvo lo que un cambio autorizado exija tocar. `docs/`, `supabase/`, `database/`, `.env.example` y `ci.yml` no se tocan (la autorización de S1.1/S1.2 cubre código, pruebas y configuración de herramientas, no documentación). | APROBADA (delegada) | Evita ampliar el perímetro. |
| S1-D05 | Extender la prueba de arquitectura por AST a `fetch`, `XMLHttpRequest`, `WebSocket`, `EventSource` y `navigator.sendBeacon` en `src/` (AC1-01). | APROBADA; se ejecuta en S1.1 | Es la parte de AC1-01 hoy sin imponer. |
| S1-D06 | Diagnosticar la causa de la prueba E2E intermitente en S1.2, con evidencia, antes de contar 3 corridas consecutivas. **Prohibido enmascararla con reintentos.** | APROBADA | La causa está sin verificar. |
| S1-D07 | Criterio: «Estado» y «Pendientes» se limitan a condiciones operativas verificables, con estado vacío explícito. En S1.2 la navegación se construye sobre las **dos vistas existentes**; no se crean vistas nuevas ni se pide persistencia al navegador. | CRITERIO APROBADO; vistas nuevas no | Sin datos reales, una vista nueva sería decorativa. |
| S1-D08 | **No aprobada.** Criterio de diseño: solo acciones significativas y sin contenido del usuario. El catálogo y los datos mínimos del Evento de actividad requieren una especificación con necesidad funcional y fuente antes de S1.3. | NO APROBADA (queda abierta) | Regla P4.C y «no implementar hasta especificar». |
| S1-D09 | **No cerrada.** Criterio: lista permitida cerrada, validada al leer y al escribir. Valores y defaults se cierran antes de S1.6. | ABIERTA (criterio) | La documentación no trae valores. |
| S1-D10 | **No cerrada.** Se decide junto con el esquema mínimo (S1-D13). | ABIERTA | Depende de S1-D13. |
| S1-D11 | Dirección: **incluir respaldo básico (exportar/importar) en la Fase 1** como último paso de persistencia, por el riesgo RK-01 (pérdida de datos al limpiar el navegador). Punto de partida de importación: **reemplazo completo con confirmación explícita**; la combinación queda excluida mientras no existan reglas de conflicto. Contrato de archivo por especificar; requiere autorización de la subfase. | DIRECCIÓN APROBADA (condicionada); sin implementación | B7 permitía incluirlo con aprobación; el riesgo de no hacerlo es mayor. |
| S1-D12 | Solo códigos de error reales y observables; no añadir `conflict` por anticipado. **Sin cambios al catálogo `AppErrorCode` en S1.1/S1.2.** | CRITERIO APROBADO | La autorización lo prohíbe en estas subfases. |
| S1-D13 | **No aprobada.** La documentación no basta para definir v0, v1 y v2 (ver `05_`). Antes de S1.3 se necesita una especificación del esquema mínimo con necesidad funcional por cada atributo. | NO APROBADA (queda abierta) | Inventar un esquema violaría P4.C. |
| S1-D14 | Anchos para AC1-13: **320, 360, 375, 390, 768, 1024 y 1440 px** (se añade 320 por el criterio de reflujo WCAG 1.4.10; los demás ya existen). Navegadores: Chrome estable obligatorio; Edge cuando el entorno lo permita; Firefox y Safari como mejor esfuerzo, sin bloquear (P11). CI en GitHub Actions: se decide en S1.11. | APROBADA (delegada) | Concreta P11 sin ampliar el perímetro. |
| S1-D16 | Aclarar el nombre «Fase 1.0–1.1-A1» frente a «Fase 1» cuando se autorice tocar documentación del repositorio. | APLAZADA con motivo | No hay autorización para editar documentación existente. |

## 4. Estado resultante
- S1.0: resultados aprobados con cambios (delegado). S1.1 y S1.2: **activas** en el perímetro del 20:59 (código fuente, pruebas y configuración de herramientas de esta rama; sin ampliar `AppErrorCode`; pruebas AC1-01, AC1-02, AC1-03, AC1-04 y la parte aplicable de AC1-13).
- Sigue sin autorizar: persistencia, dominio, migraciones, preferencias, perfil local, respaldo, datos del Command Center, S1.3 en adelante, Fase 2. Fase 1 completa: **no autorizada ni aceptada**.
- Abiertas: S1-D08, S1-D09, S1-D10, S1-D13, S1-D16; C-2, C-3 y los 10 aplazamientos.
