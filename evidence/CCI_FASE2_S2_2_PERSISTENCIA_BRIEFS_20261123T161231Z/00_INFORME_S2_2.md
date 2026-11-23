# Fase 2, S2.2 — Persistencia de briefs (AC2-04, base de AC2-08)

Fecha: 2026-11-23. Ejecutado por Claude por orden del propietario ("Apruebo todo").

## Entregado
- `src/domain/briefRecord.ts`: brief guardado (id `brf_…`, fechas, campos). Un borrador incompleto se guarda; un campo inválido o una clave desconocida se rechazan. El estado completo/incompleto se deriva al leer con las reglas vigentes.
- Repositorio `briefs` (put/get/list/remove/count) en memoria e IndexedDB; migración v2→v3 (almacén `briefs`, índice `updatedAt`) sin tocar datos existentes.
- Respaldo v2: incluye `briefs`; los respaldos v1 siguen importándose (suma calculada con la forma v1). Importar sigue reemplazando todo, atómico (también los briefs). Límite 2 000 briefs; el límite de 5 MB sigue vigente.
- Contrato compartido: 4 casos nuevos ejecutados en memoria Y en IndexedDB real (Chrome).

## Verificación
- 213 pruebas unitarias, typecheck, lint, formato, secretos y build (verify = 0).
- E2E en Chrome 153: 76/76 en 3 corridas consecutivas, incluido un E2E que importa un respaldo v1.
- E2E actualizados por el cambio de versión (base v3; respaldo "más reciente" ahora v3).

## Supuestos de Claude (reversibles)
Formato de id, límite de 2 000 briefs, versión de respaldo 2, índice `updatedAt`.

## Pendiente (siguiente corte S2.3)
Servicio de briefs y pantalla (crear/editar/listar con validación por campo y briefs incompletos señalados), sin lo cual el usuario aún no ve esta persistencia. Sin cambios de pantalla en este corte salvo el texto de importación ("N briefs").

## No verificado
Rendimiento con miles de briefs; Web Locks/multi-pestaña para escritura de briefs (se hará con el servicio, que usará `writable()`); navegadores distintos de Chrome 153.
