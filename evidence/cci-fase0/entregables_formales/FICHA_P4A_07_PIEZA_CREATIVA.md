# P4.A — Entidad 7 de 18: Pieza creativa (CreativeAsset) — RESUELTA
Estado: **RESUELTA 2026-11-22 11:52 → (b)** con la definición mínima del propietario y el alcance exacto de `REGISTRO_DECISIONES_RESUELTAS.md`. La ficha conserva el planteamiento original.

**Nombre canónico:** `Pieza creativa` (lista A: `CreativeAsset`, l.354; B l.203 «Piezas creativas»).

**Definición propuesta (mínima):** Pieza visual que el usuario incorpora a CCI, que puede ser auditada visualmente y conservarse en la Creative Library.

**Fuentes exactas:**
- A l.354 «CreativeAsset»; B l.203 «Piezas creativas» (lista de entidades).
- B l.421–422 (Fase 3, Creative Auditor): «Auditar copys y piezas visuales».
- B l.439–447: «Auditoría visual» (legibilidad, contraste, jerarquía, distribución, consistencia de marca, elementos obligatorios, congruencia copy-pieza, formato).
- B l.599: «Piezas» en la Creative Library, junto a búsqueda, filtros, etiquetas, versiones y auditorías.
- B l.487–488 (Pruebas): «Imágenes inválidas», «Archivos no compatibles».
- A l.425–436 (§8.3 «Archivos e imágenes»): tema de análisis de almacenamiento (Blob, IndexedDB, límites, formatos, previsualización, eliminación, exportación, cuota); no define la entidad.

**Clasificación:**
- Nombre y existencia: solicitado.
- «Hay piezas visuales», «se auditan visualmente», «se guardan en la Library», «pueden ser imágenes/archivos inválidos o no compatibles»: derivado de las citas.
- «Incorpora el usuario» (se supone carga manual), «binario o referencia», dimensiones, versión, que pertenezca a Campaña y que se vincule a Copy: **propuesta mía**, sin cita.

**Ambigüedades:**
1. Tus instrucciones no definen qué es una pieza: imagen, documento, diseño, enlace. «Imágenes inválidas» y «archivos no compatibles» sugieren archivos cargados, pero no se afirma.
2. No se dice si CCI guarda el archivo (Blob) o solo una referencia; A §8.3 lo deja como análisis pendiente (P9/P11 según el expediente).
3. «Congruencia copy-pieza» (B l.447) implica relación con Copy; no se define cómo.
4. «Piezas» en la Library con «Versiones» sugiere versionado, pero la relación con ContentVersion (entidad 14) no está definida.
5. Relación con Campaña: no citada como obligatoria; Campaña–Pieza es propuesta mía pendiente (P4.B).
6. Fase: Fase 3 (B l.421) y Library; asignación formal → Q-4.

**Consecuencias si se aprueba la definición mínima:**
- Pieza creativa existe como entidad propia; formato, almacenamiento (archivo o referencia), límites y relaciones quedan sin aprobar.
- La decisión sobre almacenar archivos (cuota, exportación) se tomará aparte; esta aprobación no la anticipa.
- Entra en persistencia y exportación como entidad propia (diseño sin aprobar).
- No se aprueban criterios de auditoría visual.

**Recomendación mía:** aprobar la definición mínima sin precisar tipo de archivo ni forma de almacenamiento.

**Opciones:** (a) aprobar la definición mínima · (b) aprobar con cambios (indícalos) · (c) diferir o rechazar.
