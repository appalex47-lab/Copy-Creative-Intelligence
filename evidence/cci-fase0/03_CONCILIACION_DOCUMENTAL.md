# Conciliación documental: arquitectura anterior vs. decisión browser-only
Regla: ningún documento se elimina ni reescribe en Fase 0. Se registra su **condición**: `VIGENTE`, `HISTÓRICO` (antecedente, no aceptado para la nueva arquitectura), `A REVISAR` (contradice la decisión vigente; la corrección requiere autorización posterior), o `ADAPTABLE`.

## 1. Contradicciones detectadas (con evidencia)
| # | Archivo / ubicación | Contradicción | Condición propuesta | Acción futura (requiere autorización) |
|---|---|---|---|---|
| K1 | `README.md` (stack, líneas 3, 7, 17, 41) | «Backend futuro: Supabase/PostgreSQL/Auth/RLS/Edge Functions/Storage»; Fase 0 «diseño de datos y seguridad… PostgreSQL 17» | A REVISAR | Reescribir README vigente (§5) |
| K2 | `docs/architecture/ARQUITECTURA.md` §«Fuente de verdad» | «PostgreSQL/Supabase será la fuente central; IndexedDB/localStorage solo caché futura» | A REVISAR | Sustituir sección por ADR browser-only |
| K3 | `docs/architecture/ARQUITECTURA.md` (tabla `domain`, «Seguridad por diseño») | roles/autoridad del backend (RLS), «aislamiento por organización» | A REVISAR | Reformular al modelo local |
| K4 | `docs/decisions/DECISIONES.md` D2, D3, D4 y pendiente «Auth/multi-organización» | D3 «PostgreSQL/Supabase fuente de verdad»; D4 «CCI-DEV y CCI-PROD» | HISTÓRICO (D2–D4) + ADR nuevo | Marcar «reemplazada por decisión del propietario» (sin borrar) |
| K5 | `docs/architecture/INTEGRACION_SUPABASE_ESTADO.md` | todo el documento | HISTÓRICO | Banner de condición |
| K6 | `docs/architecture/ENTORNOS_Y_MODO_DEMO.md` | «La seguridad real dependerá de Auth, RLS y backend»; producción rechaza DEMO «aún no existe backend» | A REVISAR | Redefinir «producción» (decisión P9) |
| K7 | `docs/architecture/SEMANTICA_DE_SERVICIOS.md` | `memberships.listForOrganization`; semántica por organización | ADAPTABLE | Conservar la semántica (`not_found`/lista vacía/`validation_error`) para repositorios |
| K8 | `docs/architecture/CONTROL_DE_SECRETOS.md`, `CI.md`, `GUIA_*` | menciones de Supabase solo como negación o ejemplo | VIGENTE (sin conflicto) | revisión menor |
| K9 | `docs/roadmap/ROADMAP.md` | «Fase 1.0 pendiente de aceptación formal»; «Fase 1.1+ por definir»; Fase 0 = PG17/CCI-DEV | A REVISAR | Roadmap vigente (§11) |
| K10 | `docs/product/README.md` | «sin funcionalidades de producto» | VIGENTE (hasta Fase 1) | reemplazo por requisitos |
| K11 | `supabase/README.md`, `database/README.md` | «reservado para Auth, PostgreSQL, RLS…; CCI-DEV/PROD» | HISTÓRICO | Mantener; marcar condición |
| K12 | `.env.example` | `VITE_SUPABASE_URL`, `VITE_SUPABASE_ANON_KEY` (comentadas) | A REVISAR | Retirar referencias cuando se autorice |
| K13 | `src/domain/entities.ts` | `DataOrigin 'backend'`, «autorización real será del backend (RLS)»; modelo `Organization/Membership` | A REVISAR (código) | Reemplazo en Fase 1 |
| K14 | `src/app/envPolicy.ts`, `vite.config.ts` | `VITE_DATA_MODE=supabase`; «seguridad real dependerá de Auth, RLS y backend» | A REVISAR (código) | Rediseño en Fase 1 (P9) |
| K15 | `src/services/index.ts` y contratos | comentarios «modo backend (Supabase) se añadirá» | A REVISAR (comentarios) | Fase 1 |
| K16 | ESLint/AST/`buildGuard`/`check-secrets` (reglas anti-Supabase) | no contradicen; son controles | ADAPTABLE | Decidir si se conservan como control genérico (P13) |
| K17 | `docs/fase0/` (59 archivos): 41 tablas, 231 reglas, 780 escenarios, 17 permisos, RLS, Edge Functions | diseño de servidor, **no aprobado** | HISTÓRICO | No presentar como aceptado; fuente parcial para el dominio (P3) |
| K18 | `evidence/*` (D1–D9, R1–R9, T-xx, RJ001–RJ010) | decisiones de la arquitectura anterior | HISTÓRICO | Conservar; marcar en el índice |
| K19 | `package.json` `version` `0.0.0-fase1.0-fundacion` y `description` | nombra «Fase 1.0 fundación» con la numeración anterior | A REVISAR | Alinear con la nueva numeración de fases |
| K20 | **Numeración de fases**: histórico «Fase 1.0/1.1/1.1-B» vs. instrucción maestra «Fase 0–5» | el trabajo aceptado usa la numeración antigua | — | Mapeo propuesto en §11 del roadmap: lo aceptado como 1.0/1.1 corresponde a infraestructura previa a la nueva Fase 1; **no** equivale a la nueva Fase 1 |

## 2. Estado de las decisiones históricas D1–D9
Corregido en la revisión del 2026-11-22: existen **dos series** con los mismos identificadores (DECISIONES.md D1–D7 y Fase 1.1 D1–D9). El análisis verificado contra los registros originales está en `entregables_formales/CONCILIACION_D1_D9_VERIFICADA.md`. Ninguna decisión histórica se reabre; las que quedan en tensión con la arquitectura browser-only se remiten a P1, P2, P13, P15 y a la nueva Q-7.

## 3. Condición de cada familia documental
| Familia | Condición | Nota |
|---|---|---|
| `docs/fase0/**` | HISTÓRICO | no aceptado para la nueva arquitectura |
| `evidence/CCI_FASE1_0*`, `1_1*`, `B4_B5`, `E2E` | HISTÓRICO válido para la infraestructura | su alcance era la fundación con DEMO |
| `evidence/public/**` | copias de consulta derivadas | no son evidencia original |
| `docs/architecture/*` | mezcla (ver K2–K8) | |

## 4. Documentación vigente única propuesta (no creada)
Un conjunto de **9 documentos vigentes** que reemplazan a los actuales como referencia, sin borrarlos: `README`, `ARQUITECTURA`, `DECISIONES` (ADR), `MODELO_DE_DOMINIO`, `REQUISITOS`, `ROADMAP`, `ESTRATEGIA_DE_PRUEBAS`, `PERSISTENCIA`, `EXPORTACION_Y_RECUPERACION`. Borradores sustanciales de los contenidos están en los archivos 04–12 de este expediente; su incorporación al repositorio requiere autorización posterior.
Procedimiento sugerido: (1) añadir un encabezado de condición a cada documento histórico (sin cambiar su cuerpo); (2) crear los 9 vigentes; (3) un índice único `docs/INDICE.md` que declare qué es vigente y qué histórico; (4) prueba automática que verifique que ningún documento **vigente** declare PostgreSQL/Supabase como fuente de verdad o dependencia.
