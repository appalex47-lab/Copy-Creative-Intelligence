# 06 — Registro de decisiones pendientes (S1.0)
> Todas están **pendientes del propietario**. Las recomendaciones son **[Rec. Claude], no vinculantes**. La numeración S1-Dxx es de este registro. Las preguntas D-F1-01…D-F1-14 de la especificación funcional aportada por el propietario (elaborada por ChatGPT, no aprobada) se citan como referencia cuando coinciden.

| Id | Decisión | Opciones | [Rec. Claude] | Referencia |
|---|---|---|---|---|
| S1-D01 | Qué hacer con el dominio y los contratos provisionales de la era Supabase (identidad, organización, membresía, proyecto) durante S1.1/S1.2, cuya autorización excluye dominio | (a) dejarlos intactos y compilando hasta autorizar S1.3; (b) aislarlos tras un adaptador marcado provisional; (c) ampliar la autorización para reemplazarlos | (a): no tocar lo que la autorización excluye; reemplazar en S1.3 | F-01 |
| S1-D02 | Modo de datos operativo local y política de producción (hoy `production` se rechaza) | introducir `local` como modo operativo / mantener la política actual hasta S1.9 | Decidir antes de S1.9; no es necesario para S1.1/S1.2 | F-03; P9 |
| S1-D03 | Destino del modo DEMO, `DemoBanner` y el «(DEMO)» fijo del título | conservar solo para pruebas y demostraciones identificadas / retirar | Conservar solo para demostraciones identificadas (coherente con P9) | F-07 |
| S1-D04 | Alcance de la limpieza de referencias a Supabase (`supabase/`, `database/`, docs de arquitectura, `envPolicy`, `.env.example`, `ci.yml`, scripts y pruebas) | ninguna / solo código y pruebas / todo | Actualizar primero la documentación de arquitectura; el resto, por subfase | F-10; P2, P3 |
| S1-D05 | Ampliar la prueba de arquitectura por AST a `fetch`/XHR/WebSocket (AC1-01) | sí / no | Sí; está dentro de S1.1 (pruebas) | F-05 |
| S1-D06 | Tratamiento de la prueba E2E intermitente | diagnosticar y corregir en S1.2 / aceptar y reintentar | Diagnosticar en S1.2 antes de contar las 3 corridas consecutivas | F-09 |
| S1-D07 | Qué representan «Estado» y «Pendientes» del Command Center, catálogo de vistas y si se ofrece solicitar persistencia al navegador | limitar a estado de persistencia y avisos operativos verificables / otro | Limitar a lo operativo verificable; estado vacío explícito si no hay condiciones | D-F1-01, 04; AC1-11 |
| S1-D08 | Acciones que registra el Evento de actividad y datos mínimos | catálogo propuesto en la especificación aportada (p. ej. apertura, cambio de perfil, de preferencia, respaldo, error de persistencia) / otro | Aprobar solo acciones significativas, sin contenido del usuario; decisión tuya | D-F1-02, 03 |
| S1-D09 | Lista permitida de preferencias, valores y defaults (cinco categorías documentadas, sin valores) | cerrarla / reducirla | Cerrar valores y defaults antes de S1.6 | D-F1-05; AC1-09 |
| S1-D10 | Ubicación de almacenamiento del perfil local, longitud máxima y borrado | propuestas del diseño / otra | Decidir con el esquema mínimo (S1-D13) | D-F1-06; AC1-14 |
| S1-D11 | Respaldo básico dentro de la Fase 1 y semántica de importación (reemplazo o combinación) | incluir / diferir a la Fase 5 (riesgo RK-01) | Incluir, con contrato de archivo y pruebas de integridad | D-F1-07, 08 |
| S1-D12 | Catálogo final de códigos de error de persistencia y su UI | los siete candidatos del diseño / subconjunto | Solo códigos reales observables; no añadir `conflict` por anticipado | D-F1-09; AC1-08 |
| S1-D13 | Esquema mínimo de la Fase 1 y definición de v0, v1 y v2 con semillas | ver `05_` | Primero el esquema mínimo; después los tres fixtures | D-F1-10; AC1-07 |
| S1-D14 | Matriz de navegadores (P11 resuelta por niveles; falta concretar versiones), anchos de viewport para AC1-13 y ejecución de CI | fijarlos / dejarlos para S1.11 | Fijar anchos antes de implementar S1.2 | D-F1-13; F-11, F-12 |
| S1-D15 | **Aprobar (o no) estos resultados de S1.0 y activar S1.1 y S1.2** | aprobar todo / aprobar con cambios / no aprobar | Revisar primero F-01, F-03 y S1-D01 | autorización del 2026-11-22 20:59 |
| S1-D16 | Nombres: el código base se llama «Fase 1.0–1.1-A1»; el expediente usa «Fase 1» con otro alcance | aclarar en la documentación / renombrar | Aclararlo en `docs/roadmap` cuando se autorice tocar documentación existente | §1 de `01_` |

**Heredado, sin cambios:** C-2 y C-3 abiertas; los 10 aplazamientos (P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6) siguen pendientes; ninguno vence antes de la Fase 1, y P10 (hosting) condiciona cualquier despliegue.
