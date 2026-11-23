# P4.5 — Condiciones y justificaciones (propuestas mías, sin aprobar)

> **ESTADO VIGENTE (ratificación 2026-11-22 15:56; sustituye al estado de la ronda final):** P4.E (E1–E5) quedó **resuelta** por la ratificación B4 (convenciones definitivas con las delimitaciones registradas en `REGISTRO_DECISIONES_RESUELTAS.md`; P12 = (b)). Las tablas de este documento son las **propuestas de Claude que fundamentaron** esa ratificación: donde difieran del registro, prevalece el registro. Este documento no contiene decisiones del propietario. *[Estado anterior, superado: «propuestas de Claude sin aprobar; P4.5 permanece preliminar; P4.E (E1–E5) sigue pendiente».]*
Posiciones del propietario en `REGISTRO_DECISIONES_RESUELTAS.md`. Este documento desarrolla lo que él condicionó. Nada es decisión hasta que lo valide.
## 1. Fechas: almacenamiento UTC sin perder la semántica comercial
- **Instantes** (creado, modificado, auditado, aprobado): ISO-8601 UTC con `Z`. Es lo aprobado.
- **Fechas comerciales** (vigencia de una oferta, inicio/fin de promoción): **no** son instantes. Una vigencia «hasta el 30 de noviembre» es una **fecha de calendario** `YYYY-MM-DD` que **no se convierte a UTC** (al convertir, la fecha puede cambiar de día).
- Si la vigencia incluye **hora** (p. ej. «hasta las 23:59»), se guarda la hora local **más la zona horaria IANA** (p. ej. `America/Mexico_City`), no un desplazamiento fijo; el instante UTC se **calcula** al validar, no se guarda como única verdad.
- La zona horaria de referencia es un dato de Configuración **a decidir por ti**; no la asumo.
- Pruebas de frontera: cambio de horario de verano, fin de mes/año, comparación vigencia-vs-fecha-actual. Estado: **propuesta**.
## 2. `revision` (control optimista): ¿hay necesidad real?
| Escenario | ¿Requiere `revision`? |
|---|---|
| Una sola pestaña, un usuario | No: una cola de escritura serializada evita carreras entre guardado automático y manual |
| Varias pestañas (P12 pendiente) con **solo lectura** en las secundarias (recomendación (b)) o bloqueo exclusivo (a) | No |
| Varias pestañas con escritura concurrente (P12 = c) | **Sí**, en las entidades editables (Brief, Copy, Variante), para detectar pisado de cambios |
| Importar/restaurar | No: es todo-o-nada con reemplazo confirmado |
| Historial/versiones | No: las versiones son inmutables y separadas |
**Conclusión:** **no hay necesidad general**; solo existiría si se elige P12 = (c). Propongo **no incluir `revision` como convención global**; si P12 = (c), aplicarla solo a las entidades editables. `updatedAt` se conserva como información, no como control. Decisión definitiva: ligada a P12.
## 3. Archivar frente a eliminar (condición de `archivedAt`)
| Operación | Qué hace | Reversible | Efecto en versiones y referencias |
|---|---|---|---|
| **Archivar** | marca `archivedAt`; sale de listas por defecto | Sí (restaurar) | conserva todo, incluidas versiones, auditorías y referencias |
| **Restaurar** | limpia `archivedAt` | — | sin pérdida |
| **Eliminar (purga)** | borrado físico tras confirmación explícita | **No** | **propuesta:** bloquear si hay versiones aprobadas vinculadas o exigir eliminar también sus dependientes con aviso; el respaldo previo se ofrece antes |
Documentar en la interfaz y en `07`: «archivar no es eliminar». Estado: **propuesta**, pendiente de tu validación del tratamiento de versiones aprobadas.
## 4. Desconocido, cero, vacío y no aplicable
| Estado | Significado | Ejemplo | Representación propuesta |
|---|---|---|---|
| Desconocido | no se sabe | precio no informado | `null`/ausente |
| Cero | valor conocido 0 | descuento 0 % | `0` |
| Vacío | conocido y vacío | lista de exclusiones sin elementos | `""` / `[]` |
| No aplicable | el campo no corresponde | «vigencia» en una oferta permanente | marca explícita (`notApplicable`), no `null` |
Los cálculos y validaciones **no tratan** `null` como cero; un dato desconocido produce «información faltante» (instrucción maestra l.529). Representación exacta: **propuesta**, a validar.
## 5. Versiones inmutables con hash: alcance honesto
Aprobado como **principio de integridad y trazabilidad**. El hash (SHA-256 del contenido canónico) detecta **cambios accidentales o corrupción**. **No** garantiza autoría ni impide que alguien con acceso local reescriba contenido y recalcule el hash (IndexedDB no es una frontera de seguridad; ver ADR propuesto §2 bis). No se presenta como garantía de seguridad.
