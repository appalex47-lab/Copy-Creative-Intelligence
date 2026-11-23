# 03 — Alcance de pantallas de la Fase 1 (S1.0)
> **PROPUESTA, no aprobada.** Fuentes: roadmap y criterios del expediente (Fase 1, AC1-01…AC1-14), arquitectura y diseño de persistencia del expediente, y la especificación funcional propuesta que el propietario aportó (elaborada por ChatGPT; no aprobada). «Definible» = los documentos aprobados bastan; «Bloqueada» = requiere una decisión del propietario (ver `06_`). No se propone ningún atributo.

| Vista / función | Qué haría (según las fuentes) | Datos y origen | Estado | Criterio | Decisión que la desbloquea |
|---|---|---|---|---|---|
| Estructura de navegación, enlace de salto, gestión de foco, teclado | Cambiar entre las vistas aprobadas con foco gestionado | Estado de navegación de la aplicación | **Definible** (ya existe una base: F-06) | AC1-03 | catálogo de vistas (S1-D07) |
| Sistema visual y componentes | Botones, campos, tarjetas, estados vacíos, avisos, errores, listas | Datos recibidos de casos de uso; sin acceso directo a almacenamiento | **Definible** | AC1-04, AC1-13 | — |
| Accesibilidad y responsive | Foco, nombres accesibles, contraste, adaptación a anchos | Estructura de vistas | **Parcial** | AC1-03, 04, 13 | anchos concretos (S1-D14) |
| Command Center — Estado | Estado de la aplicación y de su persistencia | Conexión a IndexedDB, versión de esquema, coordinación de pestañas | **Bloqueada** | AC1-06, 11, 12 | qué representa «Estado» (S1-D07) |
| Command Center — Actividad reciente | Lista cronológica de acciones locales, con estado vacío explícito | Registros reales de **Evento de actividad** (entidad aprobada; estructura y eventos sin especificar) | **Bloqueada** | AC1-05, 06, 11 | estructura y catálogo (S1-D08) |
| Command Center — Pendientes | Avisos operativos comprobables; sin tareas ficticias | No existe entidad «Pendiente» ni catálogo; las entidades de negocio que producirían pendientes llegan en fases posteriores | **Bloqueada** | AC1-11 | condiciones de pendiente (S1-D07) |
| Pantalla de almacenamiento | Uso, cuota y estado de persistencia del navegador; «No disponible» si no se expone | API de almacenamiento del navegador | **Definible** en lo observable; acción de solicitar persistencia sin decidir | AC1-10 | solicitar persistencia (S1-D07) |
| Preferencias | Consultar y modificar preferencias ligeras permitidas | Local Storage `cci.prefs.v1`; cinco categorías documentadas (tema, idioma, última vista, avisos vistos, copia de la fecha del último respaldo) sin valores ni defaults | **Bloqueada** | AC1-09 | lista permitida (S1-D09) |
| Perfil local opcional | Introducir, editar o borrar un nombre visible (`displayName` opcional) | Ubicación de almacenamiento, longitud máxima y borrado sin definir | **Bloqueada** | AC1-14 | ubicación y límites (S1-D10) |
| Respaldo (exportar / importar) | Solo si el propietario lo aprueba dentro de la Fase 1 | Formato, alcance de datos y semántica de importación sin definir | **Bloqueada** | AC1-06, 08, 12 | aprobación y contrato (S1-D11) |
| Errores de persistencia | Mensajes y comportamiento por código | Códigos candidatos del diseño; ninguno aprobado | **Bloqueada** | AC1-08 | catálogo (S1-D12) |

## Qué puede avanzar sin decisiones nuevas (si el propietario activa S1.1 y S1.2)
Estructura de capas, navegación con foco gestionado, sistema visual y componentes, accesibilidad, ampliación de la prueba de arquitectura (AC1-01) y el triage de la prueba E2E intermitente. **No** puede avanzar sin decisión ni está en la autorización de S1.1/S1.2: ninguna vista que muestre datos, dominio, persistencia, preferencias, perfil o respaldo.

## Consecuencia observada
Sin entidades de negocio en la Fase 1, «Estado» y «Pendientes» del Command Center no tienen fuente más allá de condiciones operativas del navegador; probablemente la pantalla muestre sobre todo estados vacíos explícitos (AC1-11). Decidir si eso basta es del propietario.
