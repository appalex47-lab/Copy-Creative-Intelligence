# Estrategia de respaldo y recuperación (propuesta)
Principio: «Los datos locales deben poder exportarse y recuperarse». La aplicación **no promete recuperación automática**: el navegador puede borrar o expulsar el almacenamiento.

## 1. Formato de exportación (lógico, independiente del contenedor; P6)
Sobre: `{ format: "cci-backup", formatVersion, appVersion, schemaVersion, exportedAt, instanceId, scope: "full"|"selective", counts: {store: n}, payload: {store: [registros]}, integrity: {algorithm: "SHA-256", payloadHash} }`.
- `payloadHash`: SHA-256 (Web Crypto) del `payload` en forma canónica. Detecta corrupción accidental; **no** prueba autoría ni evita manipulación deliberada (quien edite el archivo puede recalcular el hash).
- Binarios (si P5=sí): JSON con base64 (simple, grande) o contenedor ZIP (requiere dependencia, P13). El formato lógico no cambia.
- Exportación selectiva: por campaña o por conjunto de entidades, con cierre referencial (incluye lo necesario o marca referencias externas).

## 2. Importación (todo o nada)
1. Limitar tamaño y leer sin ejecutar contenido.
2. Parsear y validar con validadores propios (tipos, obligatorios, rangos, claves desconocidas ignoradas/rechazadas según política, defensa contra `__proto__`/`constructor`).
3. Comprobar `format`, `formatVersion`, `schemaVersion`: archivo con versión **mayor** → rechazar; menor → migrar **en memoria**.
4. Verificar `payloadHash` y `counts`.
5. **Simulacro** en memoria: integridad referencial, unicidad de versiones.
6. Mostrar resumen (qué se reemplaza/añade) y exigir confirmación explícita; ofrecer exportar el estado actual primero.
7. Escribir en **una sola transacción** (reemplazo total) o en una BD temporal que se conmuta al final; si algo falla, se aborta y no queda estado parcial.
8. Ejecutar la verificación de consistencia y mostrar el resultado.

## 3. Respaldo y restauración
- Respaldo manual en cualquier momento; recordatorio por antigüedad (sin automatismos que escriban en el sistema de archivos sin consentimiento).
- Restaurar copia anterior = importar un respaldo con la misma guarda (pasos 1–8). Siempre hay un respaldo previo ofrecido antes de reemplazar.
- File System Access API (solo algunos navegadores) es opcional y no se asume.

## 4. Escenarios
| Escenario | La app puede | La app no puede |
|---|---|---|
| Cierre inesperado del navegador | revertir transacciones incompletas; recuperar borradores autoguardados | recuperar lo no persistido |
| Borrado de datos del sitio | mostrar la ausencia de datos y ofrecer importar un respaldo | recuperar sin respaldo |
| Cambio de navegador o dispositivo | exportar/importar manualmente | sincronizar |
| Actualización de la app | migrar con respaldo previo ofrecido | revertir una migración confirmada sin respaldo |
| Datos de versión incompatible | rechazar, no escribir, ofrecer exportar lo legible | «arreglar» automáticamente |
| Expulsión de almacenamiento por el navegador | advertir y solicitar `persist()` | garantizar la permanencia |

## 5. Avisos al usuario
Banner persistente «Tus datos solo están en este navegador», fecha del último respaldo, alerta si nunca se exportó o si pasaron N días (valor configurable), confirmación al reemplazar, y estado real del almacenamiento (uso estimado y si es persistente).

## 6. Pruebas definidas (no ejecutadas)
Round-trip exportar→importar; archivo truncado/corrupto/hash alterado/versión mayor/versión menor; claves maliciosas; importación interrumpida (sin estado parcial); restauración sobre datos existentes con confirmación; selectiva con referencias; tamaño límite.
