# CCI Fase 2 · S2.5b — Leyendas y términos de marca configurables

Decisiones de Claude bajo delegación (revocables).

## Qué entra
- Pantalla «Reglas»: leyendas (texto, canales, obligatoria, activa) y términos de marca (texto, prohibido/preferido, severidad, sugerencia): agregar, editar, activar/desactivar leyendas, eliminar con confirmación, restaurar plantilla de ejemplo. Cada cambio se guarda al instante.
- Persistencia en IndexedDB v5 (almacén `rules`, un documento) y respaldo `cci-backup` v4 (`data.rules`; null = nunca configurado; se siguen aceptando v1–v3).
- La revisión de copys (S2.5a) usa lo capturado; sin configuración usa la plantilla (leyendas vacías, términos de ejemplo NO validados) y lo avisa en pantalla.
- Duplicados (sin distinguir mayúsculas ni acentos) y datos inválidos se rechazan con motivo; la escritura pasa por la guarda de pestaña única (P12).
- El permiso/aviso de publicidad sigue omitido por decisión del propietario.
- Ajustes de pantalla móvil: la revisión se muestra debajo de los botones; se quitó el hueco sobre el título de las tarjetas; el aviso ya no dice que los términos sean editables cuando no lo eran.

## Corrección de una prueba intermitente
- `closing.spec.ts` (teclado) pulsaba Tab antes de que la interfaz estuviera montada (causa ya documentada en S1.2 para app.spec). Se añadió la espera; 30 repeticiones seguidas pasaron. Es una causa probable del fallo intermitente de S2.3, no demostrada.

## Verificación
- `npm run verify` exit 0 (256 pruebas unitarias).
- Playwright completo ×3: 81/81 en cada corrida (Chrome 153).

## Límites
- No se probó la importación de un respaldo con reglas en navegador (sí en dominio y contrato de repositorios) ni la pestaña de solo lectura sobre Reglas.
- Sin prueba en Edge/Firefox/Safari/móvil real/lector de pantalla.
- La tolerancia de porcentaje (0.5 pp) no es editable en pantalla todavía.
