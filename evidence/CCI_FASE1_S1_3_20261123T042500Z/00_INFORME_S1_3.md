# S1.3 (parcial) — Dominio de la Fase 1, validadores y pruebas

Decisiones de Claude bajo la delegación del propietario (ver `../CCI_FASE1_S1_0_DECISIONES_DELEGADAS_20261123T033116Z/`). Trabajo directo sobre `main`.

## Hecho (aditivo; el dominio provisional de la era Supabase NO se eliminó todavía)
- `src/domain/profile.ts`: perfil local con nombre visible opcional (máx. 60 caracteres, sin caracteres de control; texto no confiable).
- `src/domain/settings.ts`: configuración con lista permitida de las 5 categorías documentadas y defaults; descarta claves y valores inválidos.
- `src/domain/activity.ts`: evento de actividad con tipo cerrado y marca de tiempo; sin contenido del usuario ni campos extra.
- 11 pruebas unitarias nuevas; el dominio no importa otras capas (regla de S1.1).

## SUPUESTOS míos, marcados y reversibles (no vienen de un documento aprobado)
Máximo de 60 caracteres; valores `theme` (system/light/dark), `language` (es), vistas válidas, tope de 50 avisos vistos; los seis tipos de evento. Solo el nombre opcional del perfil, las cinco categorías de configuración y la existencia del Evento de actividad están aprobados.

## Pendiente
Retirar `UserIdentity`, `Organization`, `Membership` y `Project` (contradicen P1) junto con servicios, adaptador DEMO y páginas que los usan; esquema de IndexedDB, migraciones v0–v2 y repositorios (S1.4 y S1.5).
