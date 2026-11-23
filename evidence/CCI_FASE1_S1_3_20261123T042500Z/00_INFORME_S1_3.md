# S1.3 (parcial) — Dominio de la Fase 1, validadores y pruebas

Decisiones de Claude bajo la delegación del propietario (ver `../CCI_FASE1_S1_0_DECISIONES_DELEGADAS_20261123T033116Z/`). Trabajo directo sobre `main`.

## Hecho (aditivo; el dominio provisional de la era Supabase NO se eliminó todavía)
- `src/domain/profile.ts`: perfil local con nombre visible opcional (máx. 60 caracteres, sin caracteres de control; texto no confiable).
- `src/domain/settings.ts`: configuración con lista permitida de las 5 categorías documentadas y defaults; descarta claves y valores inválidos.
- `src/domain/activity.ts`: evento de actividad con tipo cerrado y marca de tiempo; sin contenido del usuario ni campos extra.
- 11 pruebas unitarias nuevas; el dominio no importa otras capas (regla de S1.1).

## SUPUESTOS míos, marcados y reversibles (no vienen de un documento aprobado)
Máximo de 60 caracteres; valores `theme` (system/light/dark), `language` (es), vistas válidas, tope de 50 avisos vistos; los seis tipos de evento. Solo el nombre opcional del perfil, las cinco categorías de configuración y la existencia del Evento de actividad están aprobados.

## Retirada del dominio provisional (completada)
- Se eliminaron `UserIdentity`, `Organization`, `Membership` (con roles) y `Project`, los datos de demostración de esas entidades y los servicios que los exponían. `src/domain/entities.ts` conserva solo `AppState`.
- El contrato `Services` queda en `appState` y `activity` (lista de actividad reciente). El adaptador DEMO **no inventa actividad**: devuelve lista vacía.
- «Resumen» muestra la actividad real o un **estado vacío explícito** («Sin actividad reciente»); un fallo de servicio no se disfraza de estado vacío (prueba).
- Pruebas unitarias y E2E reescritas para el nuevo contrato. Resultado: 143 pruebas unitarias; Playwright 35/35 en 3 corridas consecutivas (Chrome for Testing 153); typecheck, lint, formato, secretos y build sin errores. La cifra de unitarias baja de 160 a 143 porque se retiraron las pruebas de los datos de la era Supabase.
- El `AppErrorCode` no se amplió.

## Pendiente
Esquema de IndexedDB, repositorios y migraciones v0–v2 (S1.4 y S1.5); preferencias, perfil, almacenamiento, Command Center con datos reales, respaldo.
