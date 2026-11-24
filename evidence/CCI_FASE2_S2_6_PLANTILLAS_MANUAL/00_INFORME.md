# CCI Fase 2 · S2.6 — Flujo manual sin IA: plantillas por canal

Decisión de Claude bajo delegación (revocable). Corresponde a IA-A (sin IA), ya aprobada por el propietario.

- `src/domain/copyTemplates.ts`: dos plantillas («Directo» y «Oferta») que solo REORDENAN datos del brief para los campos que usa el canal; no inventan precios, porcentajes ni beneficios. Si falta un dato, el campo queda vacío.
- «Nuevo copy» ofrece «Empezar desde una plantilla (opcional)»; todo es editable antes de guardar.
- Supuestos de Claude: qué campos del copy usa cada canal y la redacción de las plantillas.
- Verificación: `npm run verify` exit 0 (261 pruebas unitarias); Playwright completo ×3: 82/82.
- No verificado: que la redacción de las plantillas sea la que el propietario quiere; Edge/Firefox/Safari/móvil/lector de pantalla.
