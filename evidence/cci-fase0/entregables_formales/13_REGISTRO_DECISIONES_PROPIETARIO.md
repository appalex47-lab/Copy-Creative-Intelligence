# Registro de decisiones del propietario
> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; no es decisión nueva de este documento):** P4 (P4.A 18/18, P4.B, P4.C, P4.E), P5, P9, P11, P12, P13, P14 y Q-4 quedan resueltas por su contenido; P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5 y Q-6 tienen **aplazamiento aceptado (no resueltas)**. Las «Recomendaciones» y opciones de este documento son anteriores y conservan su carácter de propuesta; el texto de cada decisión está en `REGISTRO_DECISIONES_RESUELTAS.md`. Aprobaciones 0.1–0.7, aceptación de Fase 0 y autorización de Fase 1: pendientes.

> Documento formal del §14. Fuente de contenido: `../10_REGISTRO_DECISIONES.md` (sin cambios de fondo). Estado: propuesta para revisión; nada aprobado ni implementado.

Ninguna se responde por el propietario. *[Nota de la ronda de coherencia 2026-11-22: texto del momento de elaboración; P1, P2 y P3 fueron resueltas, P4 parcialmente y Q-7 resuelta (ver la tabla y `REGISTRO_DECISIONES_RESUELTAS.md`); el resto sigue pendiente.]* «Recomendación» es una propuesta técnica. «Informada por la instrucción maestra» indica que el texto del propietario ya apunta en una dirección, pero **falta confirmación expresa**.
Indispensabilidad para cerrar Fase 0: **I** = indispensable · **F1/F2/F5** = debe resolverse antes de iniciar esa fase (no bloquea el cierre de Fase 0) · **A** = puede quedar abierta con consecuencia documentada.

| ID | Tema | Clase |
|---|---|---|
| P1 | Identidad, organización, membresías y roles | I — **RESUELTA 2026-11-22 (b)** |
| P2 | Sustituir formalmente DEC-D2–D4 | I — **RESUELTA 2026-11-22 (a)** |
| P3 | Tratamiento de `docs/fase0/` | I — **RESUELTA 2026-11-22 (b)** |
| P4 | Dominio de producto y definición de MVP | I — **RESUELTA por ratificación 2026-11-22 15:56 (B1–B5, B7)**; antes: PARCIAL (nombres confirmados; ver `DECISIONES_P4_PENDIENTES.md`) |
| P5 | Binarios en IndexedDB | I (afecta esquema y formato de exportación) — **RESUELTA por ratificación 2026-11-22 15:56 (B6)** |
| P6 | Formato de exportación | F2 (diseño lógico ya propuesto) — **APLAZADA, aplazamiento aceptado 2026-11-22 15:56 (B8); no resuelta** |
| P7 | Cifrado local con frase de paso | F5 — **APLAZADA, aplazamiento aceptado 2026-11-22 15:56 (B8); no resuelta** |
| P8 | Alternativa de IA y política de claves | F2 — **APLAZADA, aplazamiento aceptado 2026-11-22 15:56 (B8); no resuelta** |
| P9 | Qué es «producción» en modo local | I — **RESUELTA por ratificación 2026-11-22 15:56 (B6)** |
| P10 | Hosting y origen | F5 (en Fase 1 basta `localhost`) — **APLAZADA, aplazamiento aceptado 2026-11-22 15:56 (B8); no resuelta** |
| P11 | Navegadores soportados | I — **RESUELTA por ratificación 2026-11-22 15:56 (B6)** |
| P12 | Política multi-pestaña | I — **RESUELTA por ratificación 2026-11-22 15:56 (B6)** |
| P13 | Dependencias y ampliación de `AppErrorCode` | I — **RESUELTA por ratificación 2026-11-22 15:56 (B6)** |
| P14 | ¿Prueba de concepto en Fase 0? | I — **RESUELTA por ratificación 2026-11-22 15:56 (B6)** |
| P15 | Pendientes previos (licencia, enlace de sesión, rama local, F11-D4, F5/G-1, F6, Fase 0 anterior) | A / mixto — **APLAZADA, aplazamiento aceptado 2026-11-22 15:56 (B8); no resuelta** |

---
### P1 — Identidad, organización, membresías y roles
- **ESTADO: RESUELTA por el propietario el 2026-11-22 → opción (b)** (perfil local opcional; sin roles ni etiquetas de autorización). Texto literal y consecuencias: `REGISTRO_DECISIONES_RESUELTAS.md`. La recomendación original se conserva debajo como antecedente.
- **Pregunta:** ¿Qué ocurre con `UserIdentity`, `Organization`, `Membership`, los 5 roles (`admin`, `ecommerce`, `design`, `marketing`, `reviewer`) y `Membership.active`?
- **Contexto:** Modelo de la arquitectura anterior (multiusuario). La instrucción maestra fija un usuario por navegador sin cuentas y prohíbe «simular usuarios, permisos o aprobaciones multiusuario». Los roles reflejan las áreas que originaron el producto (Ecommerce, Diseño, Marketing).
- **Opciones:** (a) eliminar del dominio vigente (conservar como histórico); (b) reducir a un «perfil/espacio local» de un registro; (c) conservar los roles solo como **etiquetas** informativas en Aprobaciones (p. ej. «revisado por área: Diseño»).
- **Recomendación:** (b) con (c) opcional; sin permisos.
- **Implicaciones:** (a)/(b) simplifican `HomePage`, contratos y fixtures; (c) añade un catálogo de etiquetas. F11-D1–D3 (aplicadas y aceptadas) no se reabren: esta decisión fija su destino; ver `CONCILIACION_D1_D9_VERIFICADA.md`.
- **Riesgos:** reintroducir sin querer autorización aparente por roles; reescritura de pruebas actuales.
- **Dependencias:** P4, P2.
- **Si no se decide:** Fase 1 no puede definir el dominio inicial ni retirar `Organization/Membership`; riesgo de arrastrar un modelo multiusuario sin sentido.
- **Informada por la instrucción maestra:** sí (no simular multiusuario).

### P2 — Sustituir formalmente DEC-D2–D4 de `DECISIONES.md` y la sección «Fuente de verdad»
- **ESTADO: RESUELTA por el propietario el 2026-11-22 → opción (a)**. Texto literal, alcance y ADR propuesto: `REGISTRO_DECISIONES_RESUELTAS.md`. La recomendación original se conserva debajo como antecedente.
- **Pregunta:** ¿Se registra un ADR que declare reemplazadas DEC-D2 (parcial), DEC-D3 y DEC-D4 y el apartado «Fuente de verdad», conservándolas como históricas?
- **Contexto:** K2/K4 contradicen la decisión vigente (PostgreSQL/Supabase como fuente de verdad; CCI-DEV/CCI-PROD).
- **Opciones:** (a) ADR de reemplazo con condición «HISTÓRICA»; (b) dejar los textos y añadir solo una nota; (c) no tocar.
- **Recomendación:** (a).
- **Implicaciones:** documentación vigente coherente; revisores externos no se confunden.
- **Riesgos:** si no se hace, la documentación afirma lo contrario de lo decidido.
- **Dependencias:** P3. **Si no se decide:** persiste la contradicción; el criterio de aceptación de Fase 0 «ningún documento vigente declara PG/Supabase como fuente de verdad» no se cumple.
- **Informada por la instrucción maestra:** sí.

### P3 — Tratamiento de `docs/fase0/` (59 archivos) y expedientes de Supabase/SQL/RLS/multiusuario
- **ESTADO: RESUELTA por el propietario el 2026-11-22 → opción (b)**, con condiciones. Texto literal: `REGISTRO_DECISIONES_RESUELTAS.md`; índice: `INDICE_ANTECEDENTES_HISTORICOS.md`. La recomendación original se conserva debajo.
- **Pregunta:** ¿Se conservan solo como antecedente histórico, o también como fuente parcial del dominio local?
- **Contexto:** 41 tablas, 231 reglas, 780 escenarios, 17 permisos; **no aprobados**. Contienen vocabulario de producto (piezas, copy_versions, activos, revisiones) utilizable.
- **Opciones:** (a) solo histórico; (b) histórico + referencia no vinculante para el dominio; (c) migrar partes al nuevo diseño.
- **Recomendación:** (b).
- **Implicaciones:** no se presentan como trabajo aceptado para la nueva arquitectura (exigencia del propietario).
- **Riesgos:** (c) reintroduce complejidad de servidor.
- **Dependencias:** P2, P4. **Si no se decide:** ambigüedad de estatus; sin impacto técnico inmediato.
- **Informada por la instrucción maestra:** sí (conservar como antecedentes).

### P4 — Dominio de producto local y definición de MVP
- **Pregunta:** ¿Se aprueba el modelo de entidades de `05_MODELO_DOMINIO_CCI.md` y que el MVP sea Command Center + Copy Studio persistentes (fin de Fase 2)?
- **Contexto:** la instrucción maestra enumera entidades y módulos; falta fijar atributos y la clasificación MVP/posterior/futura.
- **Opciones:** (a) aprobar la propuesta; (b) aprobar con cambios; (c) definir un MVP distinto (p. ej. hasta Creative Auditor).
- **Recomendación:** (a), pidiendo cambios por entidad.
- **Implicaciones:** define stores de IndexedDB, pruebas y alcance de Fase 1–2. Incluye añadir `Evento de actividad` (no está en la lista del propietario).
- **Riesgos:** dominio equivocado → migraciones costosas.
- **Dependencias:** P1, P5, Q-3. **Si no se decide:** Fase 1 no puede crear el esquema inicial.
- **Informada por la instrucción maestra:** parcial (lista de entidades y módulos).

### P5 — Binarios (imágenes/archivos) en IndexedDB
- **Pregunta:** ¿Se almacenan piezas creativas como Blobs en IndexedDB, o solo metadatos/referencias?
- **Contexto:** Fase 3 audita piezas visuales (imágenes inválidas, archivos no compatibles). Cuotas variables por navegador (no verificadas).
- **Opciones:** (a) Blobs en IndexedDB con tope de tamaño; (b) solo metadatos y que el usuario reabra el archivo; (c) decidir en Fase 3.
- **Recomendación:** (a) con tope configurable y avisos de cuota; documentar el esquema desde ahora.
- **Implicaciones:** tamaño de exportaciones; auditoría visual necesita los píxeles.
- **Riesgos:** cuota llena, rendimiento, respaldo grande.
- **Dependencias:** P6, P11. **Si no se decide:** el diseño de `pieces`/exportación queda abierto; la Fase 3 se bloquea.
- **Informada por la instrucción maestra:** no.

### P6 — Formato de exportación
- **Pregunta:** ¿JSON con base64, contenedor ZIP, o cifrado opcional del archivo?
- **Contexto:** el formato lógico (`08_RESPALDO_IMPORTACION_RECUPERACION.md`) es independiente del contenedor; ZIP implica una dependencia (P13).
- **Opciones:** (a) JSON; (b) ZIP con JSON + binarios; (c) (a) o (b) con cifrado opcional.
- **Recomendación:** (a) para texto en Fase 2; (b) si P5=a.
- **Implicaciones:** tamaño, dependencia, facilidad de revisión.
- **Riesgos:** JSON+base64 pesa ~33 % más; ZIP añade superficie de ataque (zip bombs) a validar.
- **Dependencias:** P5, P13. **Si no se decide:** Fase 2 no puede cerrar «Exportar».
- **Informada por la instrucción maestra:** no.

### P7 — Cifrado local con frase de paso
- **Pregunta:** ¿Se ofrece cifrado (Web Crypto) de datos locales o de exportaciones?
- **Contexto:** IndexedDB no está cifrado; cifrar no mitiga XSS ni extensiones; añade riesgo de **pérdida irrecuperable** por olvido de la frase.
- **Opciones:** (a) no; (b) solo exportaciones; (c) datos y exportaciones.
- **Recomendación:** (a) para el MVP; reconsiderar en Fase 5.
- **Implicaciones:** complejidad y pruebas criptográficas.
- **Riesgos:** pérdida de datos; falsa sensación de seguridad.
- **Dependencias:** P6. **Si no se decide:** se asume (a); sin bloqueo.
- **Informada por la instrucción maestra:** no.

### P8 — Alternativa de IA y política de claves
- **Pregunta:** ¿Cuál de IA-A…IA-E (`09_ESTRATEGIA_IA_CCI.md`) se adopta, y se admite BYOK en memoria?
- **Contexto:** principios del propietario; IA-E contradice el alcance vigente.
- **Opciones:** IA-A+IA-B; + IA-C; + IA-D; IA-E (requiere decisión de alcance).
- **Recomendación:** IA-A + IA-B para Fases 1–2; evaluar IA-C solo con aceptación explícita de riesgos.
- **Implicaciones:** define el alcance real de «generación» en Copy Studio.
- **Riesgos:** IA-C expone claves; IA-A/B limitan automatización.
- **Dependencias:** P13. **Si no se decide:** Fase 2 no puede definir «Generación» (se limitaría a escritura manual + plantillas).
- **Informada por la instrucción maestra:** parcial (restricciones de claves).

### P9 — Qué significa «producción» en modo local
- **Pregunta:** ¿Se redefine la política de entorno para que `build:production` sea un build local legítimo sin DEMO, y qué ocurre con la regla «producción rechaza DEMO» y con `VITE_DATA_MODE`?
- **Contexto:** hoy `build:production` falla a propósito y `supabase` está rechazado (K6, K14). Con persistencia local el modo `demo` deja de ser el único.
- **Opciones:** (a) modo `local` real + `demo` solo en test; producción permitida con `local`; (b) mantener bloqueo hasta Fase 5; (c) eliminar la política.
- **Recomendación:** (a), conservando el bloqueo de DEMO en producción.
- **Implicaciones:** reescribir `envPolicy.ts`, `vite.config.ts`, docs, pruebas de build.
- **Riesgos:** publicar por error con datos ficticios si se debilita la guarda.
- **Dependencias:** P10. **Si no se decide:** Fase 1 arranca con una política incoherente.
- **Informada por la instrucción maestra:** parcial.

### P10 — Hosting y origen
- **Pregunta:** ¿Dónde se ejecutará la app (localhost, archivo local, dominio propio, otro) y con qué origen?
- **Contexto:** el almacenamiento es por **origen**, no por ruta. Un origen compartido con otras aplicaciones expone datos. `file://` tiene comportamiento de almacenamiento distinto según navegador (no verificado). Rutas de assets actuales son absolutas (`/assets/`).
- **Opciones:** (a) `localhost` (Vite) para desarrollo y uso personal; (b) hosting estático en origen **dedicado**; (c) otro.
- **Recomendación:** (a) en Fases 1–4; (b) con origen propio en Fase 5; configurar `base` y `noindex`.
- **Implicaciones:** aislamiento de datos; despliegue y acceso.
- **Riesgos:** compartir origen; pérdida de datos si cambia el origen.
- **Dependencias:** P9, P11. **Si no se decide:** Fase 5 no puede publicar; no bloquea Fase 1.
- **Informada por la instrucción maestra:** no (la entrega a ChatGPT es otro tema).

### P11 — Navegadores soportados
- **Pregunta:** ¿Qué navegadores y versiones se soportan y se prueban?
- **Contexto:** hoy solo Chrome (Playwright `channel: 'chrome'`). Comportamientos de almacenamiento varían (cuotas, expulsión).
- **Opciones:** (a) Chromium (Chrome/Edge) completo; (b) + Firefox; (c) + Safari/WebKit.
- **Recomendación:** (a) completo, (b) soporte con pruebas, (c) mejor esfuerzo documentado.
- **Implicaciones:** matriz E2E y configuración de Playwright (instalar navegadores requiere autorización).
- **Riesgos:** diferencias de IndexedDB/Web Locks entre motores.
- **Dependencias:** P12. **Si no se decide:** el criterio de compatibilidad (Fases 1 y 5) no es verificable.
- **Informada por la instrucción maestra:** no.

### P12 — Política multi-pestaña
- **Pregunta:** ¿Bloqueo exclusivo (una pestaña escribe), aviso y solo lectura, o varias pestañas con control optimista?
- **Contexto:** sin coordinación puede haber escrituras cruzadas.
- **Opciones:** (a) bloqueo con Web Locks; (b) aviso + solo lectura en las demás; (c) permitir con `revision` optimista.
- **Recomendación:** (b), con (c) como respaldo.
- **Implicaciones:** diseño de repositorios y pruebas E2E multi-pestaña.
- **Riesgos:** soporte de Web Locks no verificado en todos los navegadores.
- **Dependencias:** P11. **Si no se decide:** Fase 1 no puede cerrar el diseño de concurrencia.
- **Informada por la instrucción maestra:** no.

### P13 — Política de dependencias y ampliación de `AppErrorCode`
- **Pregunta:** ¿Se permiten dependencias de ejecución (envoltorio de IndexedDB, validación, ZIP, diccionario ortográfico) y de desarrollo (`fake-indexeddb`, navegadores de Playwright)? ¿Se amplía `AppErrorCode`? ¿Se conservan las guardas anti-Supabase?
- **Contexto:** hoy solo React/React-DOM en ejecución; instalar requiere autorización.
- **Opciones:** (a) cero dependencias de ejecución nuevas (IndexedDB y validadores propios); (b) un conjunto mínimo aprobado con versión exacta; (c) libre.
- **Recomendación:** (b) acotado y justificado una por una; ampliar `AppErrorCode` (`04_ARQUITECTURA_BROWSER_ONLY.md`); conservar guardas como control genérico.
- **Implicaciones:** superficie de ataque, tamaño, mantenimiento.
- **Riesgos:** cadena de suministro; `npm audit` no ejecutado en esta fase.
- **Dependencias:** P5, P6, P8. **Si no se decide:** Fase 1 no puede instalar nada ni extender errores.
- **Informada por la instrucción maestra:** no (instrucción prohíbe instalar ahora).

### P14 — ¿Prueba de concepto ejecutable dentro de Fase 0?
- **Pregunta:** ¿Se incluye un PoC de IndexedDB en Fase 0?
- **Contexto:** la instrucción maestra prohíbe modificar código en Fase 0 y asigna «Implementar IndexedDB» a Fase 1.
- **Opciones:** (a) no; (b) PoC aislado fuera del repositorio.
- **Recomendación:** (a).
- **Implicaciones:** los supuestos sobre el navegador (cuota, Web Locks) quedan sin verificar hasta Fase 1.
- **Riesgos:** descubrir tarde una limitación.
- **Dependencias:** ninguna. **Si no se decide:** se asume (a).
- **Informada por la instrucción maestra:** sí (resuelta de hecho por la instrucción; confirmar).

### P15 — Pendientes previos
- **Pregunta:** ¿Cómo se cierran: licencia, enlace de sesión en el historial, publicación de la rama local, F11-D4 (T-01/T-02), F5/G-1, F6 y aprobación de la Fase 0 anterior?
- **Contexto:** F11-D4/F5/G-1/F6 pertenecen al diseño de servidor; la licencia está pendiente y el repositorio es público; los commits contienen un identificador de sesión.
- **Opciones:** declarar F11-D4/F5/G-1/F6 «históricos, no aplican»; decidir licencia antes de publicar; decidir si se reescribe o se acepta el historial.
- **Recomendación:** históricos los de servidor; licencia antes de cualquier publicación del producto; no reescribir historia salvo decisión expresa.
- **Implicaciones:** legal y de reputación.
- **Riesgos:** publicar sin licencia.
- **Dependencias:** P2, P3. **Si no se decide:** sin impacto técnico; bloquea la publicación (Fase 5).
- **Informada por la instrucción maestra:** parcial.

---
## Decisiones adicionales descubiertas (no estaban entre las 15)
| ID | Pregunta | Clase | Contexto | Recomendación |
|---|---|---|---|---|
| Q-1 | Reglas de redondeo y tolerancias del descuento | F4 | instrucción §7 lo condiciona a «decisión aprobada»; fórmula dada | redondeo a 2 decimales «mitad hacia arriba» y tolerancia configurable en puntos porcentuales; el propietario decide valores |
| Q-2 | Canales aprobados y reglas de cada uno (longitudes, estructura…) | F4 | lista de canales dada, sin reglas | el propietario aporta límites reales; no se inventan |
| Q-3 | Estados del flujo de Workflow & Approvals | F5 (afecta dominio) | estados «propuestos» en la instrucción | aprobar los 7 estados propuestos + transiciones |
| Q-4 | Definición de MVP | I (ligada a P4) | — | fin de Fase 2 |
| Q-5 | Criterios y ponderaciones de la puntuación de auditoría | F3 | «explicables, documentados» | el propietario define categorías y pesos; el sistema los calcula |
| Q-6 | Idioma(s) del producto y fuente del diccionario ortográfico | F2 | corrección ortográfica determinista necesita diccionario (P13) | español como idioma inicial |
| Q-7 (**RESUELTA 2026-11-22 → (a)**) | ¿La entidad `Campaña` de la instrucción vigente sustituye el retiro de `Project` (F11-D5)? | F1 (antes de P4) | F11-D5 retiró `Project` sin `Campaign`; la instrucción vigente incluye `Campaña` | el propietario decide; no se asume |

## Resumen: qué es indispensable para cerrar Fase 0
~~P1~~, ~~P2~~ y ~~P3~~ (resueltas 2026-11-22), **P4, P5, P9, P11, P12, P13, P14** y **Q-4**. Con la recomendación como base, el propietario puede cerrarlas con una respuesta por decisión. Las demás se resuelven antes de su fase: P6, P8, Q-6 (antes de Fase 2); Q-5 (Fase 3); Q-1, Q-2 (Fase 4); P7, P10, Q-3, P15 (antes de Fase 5).

> **Nota fechada 2026-11-22 20:26 (respuesta del propietario; no es decisión nueva de este documento):** el propietario aceptó formalmente la Fase 0 («Acepto formalmente la Fase 0, con las limitaciones expresas C-2 y C-3 abiertas y los 10 aplazamientos pendientes. No autoriza la Fase 1.»; redacción propuesta por Claude y adoptada literalmente). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «Fase 0 no aceptada» o a la aceptación formal como pendiente describen el estado previo y quedan superadas en ese punto. **C-2, C-3 y los 10 aplazamientos siguen abiertos y la autorización de la Fase 1 sigue PENDIENTE** (acto independiente). Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.

> **Nota fechada 2026-11-22 20:59 (respuesta del propietario; no es decisión nueva de este documento):** el propietario autorizó **únicamente la subfase S1.0** de la Fase 1 (auditoría técnica y definición del alcance ejecutable; rama `fase1/s1-0-auditoria` desde `7bcba74e05577761081d68ca14fdc19f2400248d`; solo lectura, pruebas existentes sin modificar y documentación/evidencia). Las subfases S1.1 y S1.2 quedan autorizadas solo tras su aprobación expresa de los resultados de S1.0 (no activas). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Autorización de la subfase S1.0». Las menciones anteriores de este documento a la autorización de la Fase 1 como pendiente o a «Fase 1 no autorizada» describen el estado previo y quedan superadas en ese punto; la Fase 1 en su conjunto NO está autorizada. **C-2, C-3 y los 10 aplazamientos siguen abiertos.**
