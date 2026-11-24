# CCI Fase 2 · S2.7 — Rediseño de variantes

Decisión de Claude bajo delegación (aprobada por el propietario el 2026-11-23: «Decide tú, ya sabes, tienes mi aprobación»). Revocable.

## Motivo
El documento de funciones de Fase 2 dice: Variant y Version son conceptos distintos; las variantes NO tienen versiones propias. S2.4 había modelado una variante como otro Copy con su propio historial: era un desvío.

## Cambio
- Una variante es una alternativa de texto DENTRO de un copy (`variants`), con nombre y contenido; se edita en su lugar, sin historial. El copy conserva sus versiones inmutables (agregar/editar/eliminar variantes no crea versiones).
- Se retiró «Duplicar como variante» (creaba un copy nuevo). Servicio: `addVariant`, `updateVariant`, `removeVariant`.
- Supuestos de Claude (reversibles): máximo 10 variantes por copy; nombre único por copy (sin distinguir mayúsculas); «Revisar reglas» también aplica a cada variante.
- Compatibilidad: un copy sin variantes no lleva la clave `variants`, así los datos guardados antes siguen válidos sin migración. Respaldo `cci-backup` v5 (variantes dentro del copy; se aceptan v1–v4; un archivo anterior a v5 con variantes se rechaza).
- Los copys que el propietario ya creó como «variante» con la función anterior (otro copy del mismo brief) siguen siendo copys independientes; no se convierten solos.

## Verificación
- `npm run verify` exit 0 (269 pruebas unitarias). Playwright completo ×3: 82/82.
## No verificado
- Edge/Firefox/Safari/móvil/lector de pantalla.
