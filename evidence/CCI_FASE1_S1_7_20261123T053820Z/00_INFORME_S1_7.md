# S1.7 — Catálogo de errores de persistencia (decisiones de Claude bajo delegación)

## Qué se hizo
Cinco códigos nuevos (AC1-08), cada uno con mensaje en español propio, sin texto interno, y con política de reintento:
| Código | Causa observable | Reintento |
|---|---|---|
| storage_unavailable | sin IndexedDB / SecurityError / modo bloqueado | no |
| storage_blocked | otra conexión/pestaña bloquea la actualización | sí |
| storage_quota_exceeded | QuotaExceededError | no |
| storage_newer_schema | VersionError (datos de versión más nueva; no se escribe nada) | no |
| storage_failed | migración abortada u otro fallo (datos anteriores intactos) | sí |
Clasificación solo por NOMBRE de excepción (`src/adapters/persistenceErrors.ts`); el texto interno nunca llega a la UI.

## Verificación (logs en esta carpeta)
- typecheck, lint, format, secretos, build OK; 170 pruebas unitarias OK.
- Chrome real: 51/51 en 3 corridas consecutivas. Nuevas: blocked y migración fallida con IndexedDB real; base v99 → mensaje y sin reintento, versión intacta; cuota de Local Storage → mensaje y tema sin cambiar; axe sin violaciones.
- Mutación: mapear VersionError a storage_failed hace fallar las pruebas unitaria y de navegador.

## Supuestos míos (reversibles)
Textos de los mensajes; qué códigos son reintentables; InvalidState/NotSupported → storage_unavailable.

## No verificado
Cuota real (solo simulada); modo privado real de cada navegador; Edge/Firefox/Safari; revisión humana de los textos.
