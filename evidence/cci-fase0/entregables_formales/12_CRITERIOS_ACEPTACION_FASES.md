# Criterios de aceptación por fase

> **Estado (2026-11-22):** criterios **propuestos**, no aprobados individualmente; se someten a la ficha 0.7. Las menciones a campos concretos (p. ej. «13 campos» del Brief en AC2-01, «9 campos» del Hallazgo en AC3-03) proceden de la instrucción original y de la matriz de requisitos como **requisitos propuestos**; **no son atributos aprobados** (P4.C: los atributos se definen en la especificación de cada módulo). Las pre-condiciones de cada fase indican lo que debe estar resuelto *antes* de esa fase; no las resuelven.
> Fuente: `../11_ROADMAP_Y_CRITERIOS_FASES_1_A_5.md` (AC1-01…AC5-08), trazados en `03_MATRIZ_REQUISITOS_CCI.md`. Todos: definidos, no ejecutados.

## Fase 1 — Fundamentos y Command Center
Pre-condición: Fase 0 aceptada y Fase 1 autorizada; decisiones P1, P2 y P3 (resueltas 2026-11-22), P4, P5, P9, P11, P12, P13, Q-4 resueltas (ratificación 2026-11-22 15:56: **cumplidas las decisiones**; siguen pendientes la aceptación de Fase 0 y la autorización de Fase 1).
| ID | Criterio verificable |
|---|---|
| AC1-01 | Ningún módulo de `src/` usa `fetch`/XHR/WebSocket ni SDK de servidor; verificado por prueba de arquitectura (AST) |
| AC1-02 | `tsc -b`, ESLint y Prettier con 0 errores/0 advertencias; `strict` y `noUncheckedIndexedAccess` activos |
| AC1-03 | Navegación entre las vistas aprobadas con rutas/estado, foco gestionado y salto de contenido; E2E aprobadas |
| AC1-04 | Componentes reutilizables con pruebas y sin violaciones axe |
| AC1-05 | Dominio inicial implementado con validadores y pruebas unitarias (positivas y negativas) por invariante |
| AC1-06 | IndexedDB solo accedida desde el adaptador; repositorios con contrato y pruebas contra el adaptador en memoria **y** en navegador real |
| AC1-07 | Migración v0→v1 y v1→v2 de prueba con datos semilla; BD de versión mayor se rechaza sin escribir |
| AC1-08 | Cada `AppErrorCode` de persistencia tiene mensaje, prueba y comportamiento de UI definido |
| AC1-09 | Preferencias en Local Storage validadas (valor corrupto → defecto); prueba de que no se guarda nada fuera de la lista permitida |
| AC1-10 | La pantalla de almacenamiento muestra uso/cuota/persistencia leídos del navegador; E2E con datos reales |
| AC1-11 | Command Center muestra solo datos de IndexedDB (vacío = estado vacío explícito); pendientes y actividad provienen de entidades reales; ningún dato DEMO en build de producción |
| AC1-12 | Tras recargar y reiniciar el navegador los datos persisten; tras abortar una transacción no hay estado parcial |
| AC1-14 *(propuesto a partir de P1)* | Perfil local opcional: sin nombre la aplicación funciona igual; el nombre solo se muestra como texto escapado; no existen organización, membresía ni roles en dominio, contratos ni interfaz (prueba de arquitectura/AST + E2E) |
| AC1-13 | Responsive en los anchos definidos y axe sin violaciones |
| Evidencia | regresión completa (unitarias, E2E ≥3 corridas consecutivas), logs, capturas, manifiesto SHA-256, expediente en el formato de cierre |

## Fase 2 — Copy Studio
Pre-condición: P6, P8, Q-6 resueltas.
| ID | Criterio |
|---|---|
| AC2-01 | Brief con los 13 campos; validación por campo |
| AC2-02 | Briefs incompletos se señalan con el motivo; no se generan copys silenciosamente |
| AC2-03 | Generación según la alternativa aprobada; sin IA remota el flujo manual funciona de extremo a extremo |
| AC2-04 | Crear, editar, duplicar, comparar, guardar, recuperar, etiquetar, buscar, exportar e historial operan sobre datos persistentes |
| AC2-05 | Reglas de copy deterministas con casos positivos/negativos/frontera; mismos datos → mismo resultado |
| AC2-06 | Fallo o ausencia de IA no impide editar, guardar ni validar |
| AC2-07 | Copys/variantes con versiones inmutables y recuperables |
| AC2-08 | Exportación de copys verificable (round-trip) |

## Fase 3 — Creative Auditor
Pre-condición: P5, Q-5 resueltas.
| ID | Criterio |
|---|---|
| AC3-01 | Cada dimensión de auditoría de copy tiene regla, severidad y pruebas (incl. falsos positivos/negativos) |
| AC3-02 | Contraste y legibilidad se calculan de forma determinista; lo no determinista se marca como revisión manual o sugerencia |
| AC3-03 | Hallazgos con los 9 campos obligatorios; sin evidencia no hay hallazgo |
| AC3-04 | Puntuación reproducible con ponderaciones documentadas; pruebas de casos y bordes |
| AC3-05 | Sugerencias de IA nunca alteran puntuaciones ni reglas |
| AC3-06 | Corregir→reauditar→comparar conserva el historial |
| AC3-07 | Imágenes inválidas y archivos no compatibles se rechazan con mensaje y sin corrupción |

## Fase 4 — Promotion Validator y Channel Adaptation
Pre-condición: Q-1, Q-2 resueltas.
| ID | Criterio |
|---|---|
| AC4-01 | Cada validación (precios, vigencia, restricciones, productos, exclusiones, condiciones, texto legal, coherencia) tiene casos de prueba |
| AC4-02 | Descuento = ((original − promocional)/original) × 100 con redondeo y tolerancia aprobados; pruebas de borde (original = 0, promocional > original, valores negativos, decimales) |
| AC4-03 | Los 6 tipos de resultado se distinguen y se explican |
| AC4-04 | Datos faltantes se reportan como faltantes; ningún valor se infiere |
| AC4-05 | Cada canal aprobado tiene reglas y pruebas de límites de caracteres |
| AC4-06 | Cada adaptación conserva fuente, canal, versión, reglas aplicadas y diferencias |

## Fase 5 — Integración, biblioteca, aprobaciones y Performance Intelligence
Pre-condición: P7, P10, P15, Q-3 resueltas.
| ID | Criterio |
|---|---|
| AC5-01 | Biblioteca con búsqueda, filtros, etiquetas y reutilización sobre datos reales |
| AC5-02 | Estados del flujo aprobados; sin identidades ni permisos simulados |
| AC5-03 | Ninguna aprobación ocurre sin acción humana explícita |
| AC5-04 | Contenido aprobado no se sobrescribe; todo cambio crea versión con motivo |
| AC5-05 | Cada indicador tiene fórmula documentada y se oculta si faltan datos; origen manual/importado/calculado visible |
| AC5-06 | Importación todo-o-nada con validación, integridad, compatibilidad y confirmación; sin restauración parcial en pruebas de interrupción |
| AC5-07 | Flujo completo de extremo a extremo en E2E |
| AC5-08 | Regresión, accesibilidad, responsive, rendimiento, persistencia, recuperación, seguridad local, compatibilidad (según P11), manual de usuario y manual técnico entregados |

## Condiciones de cierre comunes
Pruebas con estado exacto; defectos y limitaciones explícitos; evidencia completa con SHA-256; informe en el formato de cierre; declaración de operaciones Git; recomendación (nunca «aceptada»). Entrega a ChatGPT solo tras autorización específica.
