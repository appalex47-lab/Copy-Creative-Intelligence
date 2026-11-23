# 05 — Esquemas v0, v1 y v2 para AC1-07: insuficiencia documental (S1.0)
> S1.0 debía «definir los esquemas v0, v1 y v2 necesarios para AC1-07, o registrar la insuficiencia documental». **Se registra la insuficiencia.** No se propone ningún esquema, atributo, almacén ni semilla: hacerlo sería inventarlos, y ninguno está aprobado (la regla P4.C vigente solo permite aprobar los atributos indispensables para el alcance autorizado, con su justificación).

## 1. Qué exige AC1-07
«Migración v0→v1 y v1→v2 de prueba con datos semilla; BD de versión mayor se rechaza sin escribir» (`12_CRITERIOS_ACEPTACION_FASES.md` del expediente).

## 2. Qué respaldan los documentos
- El diseño de persistencia del expediente solo exige migraciones secuenciales, deterministas e idempotentes, probadas con semillas de la versión anterior.
- La tabla de almacenes de ese diseño es una propuesta histórica, no un esquema aprobado. Incluye entidades de negocio de fases posteriores que no deben crearse en la Fase 1.
- Entidades aprobadas fuera de las 18 y relevantes para la Fase 1: Evento de actividad («estructura y eventos por especificar; no implementar hasta especificar») y Perfil local (`displayName` opcional; longitud máxima por definir).

## 3. Qué muestra el repositorio base (hecho)
- **La aplicación base nunca crea una base de datos IndexedDB ni escribe en Local Storage** (sin coincidencias en `src`, `tests`, `e2e`). Por tanto **no existe ninguna instalación previa con datos que migrar**: v0 no puede derivarse de una versión desplegada.
- No existe esquema físico, almacén, índice ni semilla en el repositorio.

## 4. Qué no puede fijarse sin decisión del propietario
| Versión | No definible con la documentación |
|---|---|
| v0 | Si es base vacía, base sin `schemaVersion`, instalación previa u otra estructura; almacenes, claves, índices y registros semilla |
| v1 | Almacenes permitidos, estructura de metadatos, estructura de Evento de actividad y de Perfil local, índices y semillas |
| v2 | Cambios respecto a v1 y su justificación, almacenes, índices y semillas |

## 5. Lo que sí puede prepararse sin inventar (si el propietario lo aprueba y se autoriza S1.4/S1.5)
Arnés de pruebas de migración y mecanismo genérico de migración secuencial; prueba de apertura de base de versión mayor (rechazo sin escritura); fixtures sintéticos independientes de datos reales **una vez aprobados los esquemas**.

## 6. Orden de decisión [PROPUESTA, no aprobada]
Primero el esquema mínimo de la Fase 1 (metadatos de esquema, Evento de actividad, Perfil local si se persiste allí); después qué representa cada versión de prueba. Registro en `06_` (S1-D13).
