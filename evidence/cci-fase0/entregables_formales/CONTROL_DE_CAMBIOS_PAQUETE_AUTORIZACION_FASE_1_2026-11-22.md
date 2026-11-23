# Control de cambios — paquete de decisión para la autorización de la Fase 1 (2026-11-22)
> **Documento fechado, no es decisión nueva.** Base: commit local `e16777855b98b96a9912ab89532a1698c62d5ce2`. Registra la incorporación al expediente de `PAQUETE_DECISION_AUTORIZACION_FASE_1.md`. Solo documental: no se modificó código de la aplicación, `docs/fase0/`, `main` ni la vista previa privada.

## 1. Qué se añadió
- `entregables_formales/PAQUETE_DECISION_AUTORIZACION_FASE_1.md`: paquete de apoyo con los seis elementos que exige la propuesta maestra §19 (subfases, repositorio y rama, áreas modificables, pruebas, prohibiciones de commit/merge/push/deploy, criterios y evidencia), las decisiones que condicionan el alcance (respaldo básico B7; perfil local P1/AC1-14), las limitaciones heredadas y un texto de decisión propuesto por Claude con campos vacíos para el propietario.
- Este control de cambios y 6 salidas en `logs/` (sufijo `_2026-11-22_paquete_autorizacion_fase_1`).

## 2. Lo que NO se registró ni se hizo
- **No se autorizó la Fase 1:** la autorización sigue PENDIENTE (acto independiente, a emitir por el propietario con su propio texto).
- No se resolvieron C-2, C-3 ni ninguno de los 10 aplazamientos; no se reabrió D5.a–d; no se aprobaron atributos de entidades; no se eligieron repositorio, rama, áreas ni pruebas (son propuestas marcadas [Rec. Claude]).
- No se inspeccionó la estructura real del repositorio de la aplicación; no se ejecutaron pruebas, build, E2E ni CI.

## 3. Archivos modificados
`05`, `07` (R15), `08` y `12` de `auditoria_integral/` (filas, cifras y notas); `logs/verificacion_coherencia_posterior.py` (solo la tupla de autoexclusión); `MANIFEST.sha256` e `INVENTARIO_PUBLICADO.sha256` (regenerados). Cifras tras la ronda: 156 archivos; manifiestos de 154 y 155 líneas; 216 blobs.

> **Nota fechada 2026-11-22 20:59 (respuesta del propietario; no es decisión nueva de este documento):** el propietario autorizó **únicamente la subfase S1.0** de la Fase 1 (auditoría técnica y definición del alcance ejecutable; rama `fase1/s1-0-auditoria` desde `7bcba74e05577761081d68ca14fdc19f2400248d`; solo lectura, pruebas existentes sin modificar y documentación/evidencia). Las subfases S1.1 y S1.2 quedan autorizadas solo tras su aprobación expresa de los resultados de S1.0 (no activas). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Autorización de la subfase S1.0». Las menciones anteriores de este documento a la autorización de la Fase 1 como pendiente o a «Fase 1 no autorizada» describen el estado previo y quedan superadas en ese punto; la Fase 1 en su conjunto NO está autorizada. **C-2, C-3 y los 10 aplazamientos siguen abiertos.**
