# PLAN DE VALIDACIÓN POSTGRESQL / SUPABASE PARA CCI (V20)

**Versión:** V20 · **Fecha:** 2026-11-19 · **Fuente:** especificación (secciones G-1/G-5/G-10, IG5-48), `evidencia_v16/VALIDACION_SERVICIOS_EXTERNOS_V16.md` · **Estado de verificación:** plan documental; **no se ejecutó SQL, no se creó ni modificó ningún proyecto Supabase, no existen migraciones**. Nada de esto se ha validado.

## Niveles de validación (separados)
| Nivel | Qué es | Estado |
|---|---|---|
| 1. Documental | Coherencia de especificación, reglas, escenarios | Hecho (V16–V20) |
| 2. Modelo local en memoria | 22 funciones / 366 casos Python | Hecho, reejecutado V20 |
| 3. PostgreSQL real (local/contenedor) | SQL, FK, UNIQUE, CHECK, triggers, transacciones | **Parcial en V20:** fixture en clúster temporal PostgreSQL 16.15 (63 pruebas, 14 mutaciones); esquema físico real: no hecho |
| 4. Supabase CCI-DEV | RLS, roles, auth, políticas, concurrencia real | **No hecho; requiere autorización** |
| 5. CCI-PROD | Promoción | **No hecho; no autorizado** |

## Entornos
Objetivo: **CCI-DEV** y **CCI-PROD** (dos proyectos Supabase propios de CCI), documentados y **no implementados**. Prohibido reutilizar proyectos de otros productos (RevNavigator incluido).

## Plan reproducible en CCI-DEV (cuando el propietario lo autorice)
1. Escribir migraciones solo de las 41 tablas (27 base v3.3 + 14), en archivos versionados; revisión antes de aplicar.
2. Aplicar en PostgreSQL local limpio; PE-01..PE-05 ya se ejecutaron en V20 con un fixture (`PE_POSTGRESQL_V20/`); repetirlas contra el esquema real y ejecutar los escenarios marcados PARCIAL.
3. Pruebas de integridad: FK compuestas/diferidas FK01–FK41, UNIQUE, CHECK, inmutabilidad (triggers sin UPDATE/DELETE), guarda de publicación (nonce).
4. RLS: matriz organización × rol (5 roles) × operación; pruebas negativas entre organizaciones.
5. Concurrencia: dos transacciones simultáneas sobre asignación de revisor, resoluciones de descarte y publicación; idempotencia de reintentos.
6. Atomicidad: fallos inyectados a mitad de operaciones de procedencia (equivalentes a AT14/AT15 del modelo).
7. Registrar comando, versión de PostgreSQL, fecha, código de salida y hash de cada corrida.

## Criterios de promoción a CCI-PROD
Todos: (a) nivel 3 y 4 en verde con evidencia archivada; (b) G-1/G-5/G-10 aceptados por el propietario; (c) DG-19 y PK/columnas de `channel_formats` decididos; (d) migraciones revisadas y reversibles; (e) sin secretos en el repositorio; (f) autorización expresa del propietario.

## Pruebas que requieren infraestructura real
RLS, triggers sobre el esquema real, PE-01..PE-05 contra el esquema real, concurrencia, FK diferidas, privilegios, retención (DG-09), hash encadenado (DG-12).
