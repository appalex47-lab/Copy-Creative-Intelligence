# Control de cambios — registro de la delegación del propietario y de las decisiones S1-D01…D16 (2026-11-22)
> **Documento fechado, no es decisión nueva.** Base: commit local `e773b0d727bf12efa4b356ddc154de6d791b1f2d`. Registra qué se cambió en el expediente para reflejar el mensaje del propietario del 2026-11-22 21:28. Solo documental: no se modificó código de la aplicación, `docs/fase0`, `main` ni la vista previa privada.

## 1. Hecho registrado (texto literal en `REGISTRO_DECISIONES_RESUELTAS.md`)
- El propietario **delegó** en Claude la aprobación de los puntos pendientes de la Fase 1. Las decisiones S1-D01…D16 las tomó Claude bajo esa delegación; **no son decisiones personales del propietario**; son revocables.
- Efecto: S1.1 y S1.2 quedan **activas** dentro del perímetro del 20:59, sin ampliarlo.

## 2. Lo que NO se registró
- No se resolvieron C-2, C-3 ni los 10 aplazamientos; no se reabrió D5.a–d.
- No se autorizó S1.3 en adelante, ni la Fase 2; no se aceptó la Fase 1; la Fase 1 en su conjunto **no está autorizada**.
- No se aprobó ningún atributo, esquema, catálogo ni formato (S1-D08, S1-D09, S1-D10 y S1-D13 siguen abiertas).
- Decisión de método: **no se añadió una nota fechada a los 29 documentos derivados** como en la ronda de las 20:59; el registro autoritativo contiene una nota cronológica que supera el estado «no activas» en ese punto. Las notas de las 20:59 se conservan como describen su momento.
- Los commits del expediente siguen siendo **locales** (la rama del expediente no se publicó).

## 3. Archivos modificados
- `REGISTRO_DECISIONES_RESUELTAS.md`: sección autoritativa nueva.
- `APROBACIONES_FASE0.md`: fila «Aparte» actualizada y nota fechada.
- `logs/verificacion_semantica_fase0.py` (S5c reorientado a S1.3 en adelante y Fase 1 completa; nuevo A6; 84 pruebas), `logs/prueba_mutacion_semantica.py` (M22 reapuntada; nueva M24; 24 mutaciones), `logs/verificacion_coherencia_posterior.py` (tupla de autoexclusión).
- `auditoria_integral/05`, `07` (R17), `08` y `12` (filas, cifras y §15); `MANIFEST.sha256` e `INVENTARIO_PUBLICADO.sha256` (regenerados).
Cifras tras la ronda: 170 archivos; manifiestos de 168 y 169 líneas; 230 blobs.
