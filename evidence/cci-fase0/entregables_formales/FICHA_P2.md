# Ficha P2 — Sustitución formal de DEC-D2–D4 y de la sección «Fuente de verdad»
Estado: **RESUELTA por el propietario el 2026-11-22 → (a)**. Ver `REGISTRO_DECISIONES_RESUELTAS.md` y `ADR_PROPUESTO_REEMPLAZO_DEC_D2_D3_D4.md`.
**Pregunta:** ¿Se registra un ADR (registro de decisión arquitectónica) que declare **reemplazadas** DEC-D2 (parcial), DEC-D3 y DEC-D4 de `DECISIONES.md` y el apartado «Fuente de verdad» de `ARQUITECTURA.md`, conservándolas como históricas (sin borrarlas ni reescribirlas)?
## Contexto y problema (verificado en `ffb47bc`)
- **DEC-D2:** «Contratos tipados + adaptadores intercambiables; DEMO ahora, Supabase futuro no conectado».
- **DEC-D3:** «PostgreSQL/Supabase como fuente de verdad; caché local solo después».
- **DEC-D4:** «Entornos CCI-DEV y CCI-PROD independientes; no reutilizar RevNavigator». En el contexto del repositorio, CCI-DEV/CCI-PROD son los proyectos Supabase (`INTEGRACION_SUPABASE_ESTADO.md`, `ROADMAP.md`).
- **`ARQUITECTURA.md`:** «Fuente de verdad» dice PostgreSQL/Supabase como fuente central e IndexedDB solo como caché futura; «Seguridad por diseño» dice que la autoridad será el backend (RLS, Edge Functions) y habla de aislamiento por organización.
- Otros textos que repiten el enfoque anterior: `README.md` (líneas 7 y 41), `ROADMAP.md`, `INTEGRACION_SUPABASE_ESTADO.md`, `.env.example` (reserva para adaptador Supabase) y `supabase/`.
- La decisión vigente dice lo contrario: IndexedDB como almacenamiento principal, sin backend ni Supabase. Hoy la documentación vigente **se contradice a sí misma**.
- P1 ya resuelta (sin organizaciones/membresías/roles): el pendiente «Auth/multi-organización» de `DECISIONES.md` queda respondido para el alcance vigente, pero **eso no sustituye** el ADR.
## Opciones y consecuencias
| Opción | Qué implica | Consecuencias |
|---|---|---|
| (a) ADR de reemplazo con estado «HISTÓRICA» | Un documento nuevo declara qué se reemplaza y qué se conserva (p. ej. de DEC-D2 siguen vigentes contratos y adaptadores; de DEC-D4, «no reutilizar RevNavigator»); los textos originales permanecen visibles con una marca de estado | Documentación coherente y trazable; revisores externos no se confunden; hace falta una autorización específica para escribirlo en el repositorio |
| (b) Solo una nota | Una nota en los documentos señalando el cambio | Más barato, pero la contradicción sigue a la vista y es fácil de pasar por alto |
| (c) No tocar | Todo igual | Persiste la contradicción; no se cumple el criterio «ningún documento vigente declara PostgreSQL/Supabase como fuente de verdad» |
## Recomendación razonada
**(a).** Corrige la contradicción sin borrar historia, que es lo que pediste (conservar y distinguir decisiones históricas, aceptadas, sustituidas y pendientes). Es la única opción que permite cumplir el criterio de Fase 0 sobre documentación vigente sin contradicciones.
## Documentos y módulos afectados
En el repositorio (**no se modifican sin autorización específica**): `DECISIONES.md`, `ARQUITECTURA.md` (dos apartados), `README.md`, `ROADMAP.md`, `INTEGRACION_SUPABASE_ESTADO.md`, `.env.example`. En este expediente: `README_PROPUESTA_VIGENTE.md`, `CONCILIACION_D1_D9_VERIFICADA.md`, `04`. Módulos: ninguno de producto; es documentación y política de entorno (se enlaza con P9).
## Relación con decisiones anteriores
Es el **único** punto que decide el destino de DEC-D2/D3/D4; no toca F11-D#. Conserva DEC-D1, D5, D6 y D7 (compatibles). Coherente con la instrucción vigente y con P1.
## Dependencias y efecto de no decidir
Antecede a P3 y condiciona la aprobación 0.2. Sin respuesta, la contradicción persiste y el criterio de cierre sobre documentación vigente no se cumple.
## Respuesta
`P2 → (a)` — **respondida** (2026-11-22).
