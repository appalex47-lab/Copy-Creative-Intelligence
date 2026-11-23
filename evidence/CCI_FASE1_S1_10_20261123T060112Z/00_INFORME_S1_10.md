# S1.10 — Respaldo: exportar/importar (decisiones de Claude bajo delegación)

## Qué se hizo
- Vista "Respaldo". Exportar descarga `cci-respaldo-AAAAMMDD-HHMMSS.json` (Blob local; sin red).
- Formato (supuesto mío, reversible): `{format:'cci-backup', version:1, exportedAt, data:{profile, settings, activity}, integrity:{SHA-256}}`. La suma se calcula sobre una forma canónica de los datos.
- Importar = REEMPLAZAR todo (perfil, preferencias, actividad) con vista previa y confirmación explícita ("Reemplazar todos los datos locales" / "Cancelar"). Antes de confirmar no cambia nada.
- Validación estricta (dato no confiable): tamaño ≤ 5 MB, ≤ 10 000 eventos, claves desconocidas rechazadas, eventos repetidos/inválidos rechazados, versión mayor rechazada, suma de integridad verificada. Los mensajes de rechazo son textos propios y no reproducen contenido del archivo.
- Atomicidad: IndexedDB reemplaza actividad y perfil en UNA transacción (si algo falla, se aborta todo). Las preferencias (Local Storage, no transaccional) se escriben antes y se restauran si la base falla.
- Se anotan `backup_exported`/`backup_imported` y se actualiza `lastBackupAt`. DEMO: no admite respaldos.

## Verificación (logs en esta carpeta)
- typecheck, lint, format, secretos, build OK; 189 pruebas unitarias OK (dominio, servicio, contrato compartido memoria+IndexedDB con 3 casos nuevos).
- Chrome real: 62/62 en 3 corridas consecutivas. Nuevas: exportación real con descarga; ida y vuelta con persistencia tras recargar; archivo alterado rechazado; no JSON/otro formato/versión nueva; cancelar; y en IndexedDB real una escritura que falla a mitad del reemplazo deja los datos anteriores intactos (AC1-12).
- Mutaciones: omitir la comprobación de la suma hace fallar la prueba del servicio; quitar `tx.abort()` hace fallar la prueba de atomicidad.

## Supuestos míos (reversibles)
Formato y versión del archivo; límites 5 MB / 10 000 eventos; nombre del archivo; que la importación siempre reemplace (dirección dada, no fusiona); lastBackupAt se actualiza al generar el archivo (no se sabe si la descarga se completó).

## No verificado
La suma SHA-256 detecta daños/alteraciones accidentales, NO es una firma: quien edite el archivo puede recalcularla. Archivos cerca de 5 MB en dispositivos lentos; descarga/selector de archivos en otros navegadores y móviles; Edge/Firefox/Safari; revisión humana de textos; no hay cifrado del respaldo (contiene tu nombre y actividad en claro).
