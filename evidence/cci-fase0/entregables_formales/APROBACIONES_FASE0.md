# Aprobaciones de Fase 0 — fichas individuales (ninguna aprobada)
> **Versión regularizada 2026-11-22 (posterior a la ratificación B1–B10; no es decisión nueva).** Reescribe la tabla de prerrequisitos y añade las siete fichas con el contenido exigido. **Ninguna aprobación está emitida: 0.1–0.7 = 0/7 PENDIENTES; Fase 0 no aceptada; Fase 1 no autorizada.** Las «Recomendaciones» son **[Rec. Claude], no vinculantes**; no son decisiones del propietario ni equivalen a una aprobación. La ratificación B1–B10 y estas aprobaciones son actos distintos; ni el silencio ni «Confirmo todo» emiten una aprobación (el registro lo declara en B10). Fuente autoritativa del estado: `REGISTRO_DECISIONES_RESUELTAS.md`. Síntesis de decisión: `PAQUETE_DECISION_APROBACIONES_0_1_A_0_7.md`.
Respuesta esperada por ficha: «aprobada», «rechazada» o «con cambios: …».

## 1. Tabla vigente de prerrequisitos
| ID | Qué se solicita aprobar | Documentos | Decisiones resueltas que la sustentan | Aplazamientos aceptados que NO bloquean (se resuelven antes de la fase indicada) | Fuera de alcance | Estado | Respuesta |
|---|---|---|---|---|---|---|---|
| 0.1 Diagnóstico | inventario y estado real del repositorio (fundación comprobada; producto inexistente) | `01`, `02`, `03`, `../03_CONCILIACION_DOCUMENTAL.md`, `../13_VERIFICACION_EJECUTADA.md` | P3, P14 | — | no valida diseño ni el funcionamiento del código | PENDIENTE | — |
| 0.2 Arquitectura | especificación browser-only y sus límites | `04` | P1, P2, P9, P12, P13 (con P5, P11 en lo que `04` los cita) | P7 (antes de Fase 5), P10 (antes de publicar) | no aprueba dominio ni persistencia detallada | PENDIENTE | — |
| 0.3 Dominio | entidades, relaciones y responsabilidades | `05`, `06`, `MATRIZ_CONSOLIDADA_18_ENTIDADES.md` | P1, Q-7, P4: P4.A 18/18 (solo existencia y definición mínima), P4.B (13 relaciones sin cardinalidades obligatorias), P4.C (atributos diferidos a cada módulo), P4.E (E1–E5), A0-1/A0-2/A0-3 | Q-1, Q-2 (antes de Fase 4) | no aprueba atributos, cardinalidades, estados, fórmulas, catálogos ni asignación de fase | PENDIENTE | — |
| 0.4 Persistencia | IndexedDB, Local Storage, archivos y recuperación | `07`, `08` | P5, P9, P11, P12, P13 | P6 (antes de cerrar Fase 2), P7 (antes de Fase 5), P10 (antes de publicar) | no aprueba cifrado, hosting, formato final de exportación ni límites de producto | PENDIENTE | — |
| 0.5 IA | estrategia de IA inicial y privacidad (sin claves privadas en el frontend) | `09` | principios del propietario; P1 | **P8** (antes de generación en Fase 2). Es un aplazamiento aceptado, **no** una aprobación de integración de IA | no autoriza ninguna integración, proveedor ni clave | PENDIENTE | — |
| 0.6 MVP | alcance y prioridades; el MVP termina al concluir Fase 2 | `10` | Q-4 (resuelta) | Q-6 (antes de Fase 2) | las columnas marcadas [P] siguen sin validar; no autoriza ninguna fase | PENDIENTE | — |
| 0.7 Roadmap | Fases 1–5 y criterios AC como puertas de aceptación | `11`, `12`, `15` | Q-4, P4 y las decisiones de arquitectura; las limitaciones expresas C-2 y C-3 | P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6 (cada una antes de su fase) | no inicia ninguna fase | PENDIENTE | — |
| Final | cerrar formalmente Fase 0 | todo el expediente | 0.1–0.7 emitidas | las limitaciones C-2 y C-3 permanecen abiertas salvo decisión expresa o evidencia primaria | **no** autoriza la Fase 1 | PENDIENTE | — |
| Aparte | autorizar el inicio de Fase 1 | — | cierre de Fase 0 | — | — | PENDIENTE | — |
Las condiciones previas antiguas (P3, P4 parcial, P5, P9, P11–P13, Q-4 sin resolver) quedaron **superadas**: ya están resueltas (ver §3). Inseparables técnicamente: ninguna; 0.3 y 0.4 pueden responderse por separado.

## 2. Fichas 0.1–0.7
Todas **PENDIENTES**. Cada ficha indica: 1 qué se solicita; 2 evidencia; 3 decisiones resueltas; 4 limitaciones vigentes; 5 exclusiones; 6 consecuencias de aprobar; 7 consecuencias de rechazar o aprobar con cambios. La recomendación, el fundamento, los riesgos y el texto de decisión están en el paquete.

### Ficha 0.1 Diagnóstico — PENDIENTE
1. **Qué se solicita:** Aceptar que el diagnóstico describe fielmente el estado real: el repositorio de la aplicación contiene la fundación comprobada y el producto CCI no existe; la línea `docs/fase0` (Supabase/RLS) es histórica y está superada.
2. **Documentos de evidencia:** `01_INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md`, `02_INVENTARIO_FUNCIONAL_CCI.md`, `03_MATRIZ_REQUISITOS_CCI.md`, `../03_CONCILIACION_DOCUMENTAL.md`, `../13_VERIFICACION_EJECUTADA.md`, `../auditoria_integral/05_INFORME_AUDITORIA_INTEGRAL.md`, `../auditoria_integral/08_INFORME_INTEGRIDAD_ARCHIVOS.md`
3. **Decisiones resueltas:** P3, P14 (sin PoC ejecutable en Fase 0), P1 y P2 en cuanto fijan el marco.
4. **Limitaciones aún vigentes:** C-2 (no se declara aceptada la Fase 0 v3.3 anterior como línea base vigente sin evidencia primaria). No se ejecutaron pruebas, build, E2E ni CI de la aplicación; `CCI-Evidence` devolvió 403 y no se usó; los anexos A/B y los documentos del repositorio de la aplicación no se leyeron.
5. **Exclusiones expresas:** No valida el diseño, no certifica que el código funcione, no declara aceptada la Fase 0 v3.3 anterior, no reabre D5.a–d.
6. **Consecuencias de aprobar:** El diagnóstico pasa a ser la base de lectura del estado real; no cambia nada técnico.
7. **Consecuencias de rechazar o aprobar con cambios:** Rechazar: habría que indicar qué hecho del inventario es inexacto y se corregiría el diagnóstico antes de las demás fichas. Con cambios: texto exacto de lo que se corrige.

### Ficha 0.2 Arquitectura — PENDIENTE
1. **Qué se solicita:** Aprobar la especificación de arquitectura browser-only: un usuario por navegador; sin cuentas, login, backend, Supabase, PostgreSQL, SQL, servidor, multiusuario ni sincronización; IndexedDB como persistencia principal; Local Storage solo para preferencias ligeras; exportación/importación local como respaldo.
2. **Documentos de evidencia:** `04_ARQUITECTURA_BROWSER_ONLY.md`, `REGISTRO_DECISIONES_RESUELTAS.md` (P1, P2, B6), `14_MATRIZ_RIESGOS_CCI.md`
3. **Decisiones resueltas:** P1, P2; P9 (modo `local`; DEMO solo en pruebas o demostraciones identificadas); P11 (Chrome/Chromium primario; Edge a validar; Firefox secundario; Safari mejor esfuerzo); P12 (una pestaña de escritura y las demás en solo lectura; fallar de forma conservadora); P13 (dependencias mínimas justificadas una por una); P14 (sin PoC ejecutable en Fase 0).
4. **Limitaciones aún vigentes:** P7 (cifrado local) y P10 (hosting y origen) aplazados. Ningún soporte de navegador está probado: la matriz E2E se hará en Fase 1 o posterior. Web Locks, cuotas de IndexedDB y compatibilidad de navegadores no se verificaron técnicamente. La mitigación multi-pestaña depende de una implementación futura.
5. **Exclusiones expresas:** No aprueba dominio, persistencia detallada ni cifrado; no autoriza instalar dependencias ni escribir código; no mezcla CCI con RevNavigator ni con RGT Execution OS; no fusiona con la vista previa privada.
6. **Consecuencias de aprobar:** Queda fijada la arquitectura vigente: no hay backend ni Supabase; incorporarlos exigiría una decisión nueva del propietario.
7. **Consecuencias de rechazar o aprobar con cambios:** Rechazar o cambiar: indicar el punto de arquitectura (p. ej. alcance de P12 o P11) y se reformula `04` sin tocar decisiones ratificadas, salvo decisión expresa.

### Ficha 0.3 Dominio — PENDIENTE
1. **Qué se solicita:** Aprobar el modelo de dominio conceptual: 18 entidades con existencia y definición mínima (18/18), 13 relaciones sin cardinalidades obligatorias, atributos diferidos a cada módulo y convenciones transversales E1–E5.
2. **Documentos de evidencia:** `05_MODELO_DOMINIO_CCI.md`, `06_MODELO_DATOS_CCI.md`, `MATRIZ_CONSOLIDADA_18_ENTIDADES.md`, `CONVENCIONES_P4_5_CONDICIONES.md`, `../auditoria_integral/03_MATRIZ_MAESTRA_ENTIDADES_P4A.md`, `CONCILIACION_30_DECISIONES_Y_APLAZAMIENTOS.md`
3. **Decisiones resueltas:** P1; Q-7; P4: P4.A 18/18 (solo existencia y definición mínima), P4.B (13 relaciones: 2 con fundamento documental y 11 propuestas, una por una), P4.C (atributos diferidos a cada módulo), P4.E (E1–E5); A0-1 (sin clasificación de origen inicial), A0-2 (diferir L1/L2), A0-3 (sí); D-1…D-8 en su alcance.
4. **Limitaciones aún vigentes:** No se aprueban atributos, cardinalidades obligatorias, estados, ciclos de vida, persistencia, fórmulas, catálogos de métricas ni asignación de fase. Q-1 y Q-2 siguen aplazadas (antes de Fase 4). Subcuestiones residuales de D-3 (ubicación de las reglas de copy) y D-5 (puntos 1, 2, 3 y 5) no tienen decisión propia: se plantean en la pregunta R-1 del paquete.
5. **Exclusiones expresas:** No aprueba Campaña–Oferta, Campaña–Pieza, Brief–Oferta, Brief–Producto, Reglas de copy–ReglaDeMarca, reglas por canal como entidades independientes ni Evento de actividad con entidad específica; no equivale a modelo de datos completo ni autoriza implementar.
6. **Consecuencias de aprobar:** El dominio queda como referencia conceptual; los atributos se aprobarán por módulo antes de implementar cada entidad.
7. **Consecuencias de rechazar o aprobar con cambios:** Con cambios: citar entidad o relación y el texto exacto; si el cambio amplía lo ratificado se trata como decisión nueva.

### Ficha 0.4 Persistencia — PENDIENTE
1. **Qué se solicita:** Aprobar el diseño conceptual de persistencia local: IndexedDB principal, binarios como Blob separados de los metadatos, Local Storage solo para preferencias ligeras, exportación/importación como respaldo y recuperación, política de archivar frente a eliminar y hash SHA-256 de versiones.
2. **Documentos de evidencia:** `07_DISENO_PERSISTENCIA_INDEXEDDB.md`, `08_RESPALDO_IMPORTACION_RECUPERACION.md`, `CONVENCIONES_P4_5_CONDICIONES.md`
3. **Decisiones resueltas:** P5 (Blob en IndexedDB; validar tipo, tamaño y contenido; consultar cuota si el navegador lo permite; sin promesa de recuperación automática); P9; P11; P12; P13; P4.E (E1 fechas, E2 `revision` no obligatorio, E3 archivar/eliminar, E4 nulos, E5 hash sin garantía de autoría ni seguridad).
4. **Limitaciones aún vigentes:** El alcance exacto del respaldo en Fase 1 es condicional («si se aprueba dentro del alcance de persistencia», B7) y lo decide el propietario al autorizar Fase 1. P6 (formato final de exportación) antes de cerrar Fase 2; P7 y P10 aplazadas. No hay límites de producto: dependen de pruebas reales de navegador. Cuotas y comportamiento de IndexedDB no se verificaron técnicamente.
5. **Exclusiones expresas:** No aprueba cifrado (P7), hosting (P10), formato final de exportación (P6), cuotas ni límites numéricos; no autoriza crear almacenes ni código.
6. **Consecuencias de aprobar:** Queda fijado el diseño conceptual de persistencia y recuperación; no hay promesa de recuperación automática.
7. **Consecuencias de rechazar o aprobar con cambios:** Con cambios: indicar sección de `07` u `08`; ampliar el alcance del respaldo en Fase 1 es decisión del propietario, no cambio documental.

### Ficha 0.5 IA inicial — PENDIENTE
1. **Qué se solicita:** Aprobar solo los principios de IA: la IA ayuda a crear, analizar y sugerir; reglas y cálculos deterministas; la aprobación final es humana; no hay claves privadas en el frontend ni secretos en Local Storage o IndexedDB. No es una aprobación de integración.
2. **Documentos de evidencia:** `09_ESTRATEGIA_IA_CCI.md`
3. **Decisiones resueltas:** Principios del propietario; P1 (browser-only, sin backend).
4. **Limitaciones aún vigentes:** P8 (estrategia de IA) está aplazada hasta antes de generación en Fase 2. La viabilidad de llamadas directas desde el navegador (CORS del proveedor) no fue verificada; el doc 09 es una propuesta de alternativas, no una decisión de proveedor.
5. **Exclusiones expresas:** No autoriza ninguna integración, proveedor, clave ni llamada remota; no resuelve P8.
6. **Consecuencias de aprobar:** Fija las reglas de privacidad iniciales; cualquier integración exige resolver P8 antes de Fase 2.
7. **Consecuencias de rechazar o aprobar con cambios:** Rechazar o con cambios: indicar la regla afectada; no impide Fase 1 porque la generación llega en Fase 2.

### Ficha 0.6 MVP — PENDIENTE
1. **Qué se solicita:** Aprobar la definición del MVP: termina al concluir Fase 2 (Fase 1 Fundamentos y Command Center; Fase 2 Copy Studio).
2. **Documentos de evidencia:** `10_DEFINICION_MVP_CCI.md`, `REGISTRO_DECISIONES_RESUELTAS.md` (B7)
3. **Decisiones resueltas:** Q-4 (el MVP termina al concluir Fase 2); P1 y P4 en lo que delimitan el alcance.
4. **Limitaciones aún vigentes:** Q-6 (idioma y diccionario) antes de Fase 2; P8 antes de generación en Fase 2; P6 antes de cerrar Fase 2. Las columnas de prioridad marcadas [P] siguen sin validar.
5. **Exclusiones expresas:** No forman parte del MVP: auditoría creativa avanzada, Promotion Validator completo, auditoría visual avanzada, Workflow & Approvals completo, Performance Intelligence avanzado, integraciones de backend y colaboración multiusuario. La aceptación del MVP no significa producto completo; no autoriza ninguna fase ni implementación.
6. **Consecuencias de aprobar:** Fija el perímetro del MVP en el fin de Fase 2.
7. **Consecuencias de rechazar o aprobar con cambios:** Con cambios: citar el elemento; mover el fin del MVP contradiría Q-4 y exigiría decisión nueva.

### Ficha 0.7 Roadmap — PENDIENTE
1. **Qué se solicita:** Aprobar el roadmap Fases 1–5 y sus criterios de aceptación como puertas de aceptación de referencia.
2. **Documentos de evidencia:** `11_ROADMAP_FASES_0_A_5.md`, `12_CRITERIOS_ACEPTACION_FASES.md`, `15_PLAN_CALIDAD_Y_PRUEBAS.md`, `../auditoria_integral/04_MATRIZ_MAESTRA_DEPENDENCIAS.md`
3. **Decisiones resueltas:** Q-4; P1, P4, P5, P9, P11–P14; limitaciones expresas C-2 y C-3 mantenidas.
4. **Limitaciones aún vigentes:** Diez aplazamientos aceptados, cada uno con fase límite: P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5, Q-6. Los criterios de aceptación y las estimaciones son propuestas hasta aprobarse. P10 y P15 se resuelven antes de publicación, no antes de Fase 1.
5. **Exclusiones expresas:** No inicia ni autoriza ninguna fase; las Fases 3–5 no forman parte del MVP; no aprueba funcionalidades concretas.
6. **Consecuencias de aprobar:** El roadmap pasa a ser referencia de planificación; cada fase seguirá requiriendo autorización independiente.
7. **Consecuencias de rechazar o aprobar con cambios:** Con cambios: indicar fase y criterio; el orden de fases y el fin del MVP no se cambian sin decisión expresa.

## 3. Estado de las condiciones previas antiguas
Las condiciones que figuraban en versiones anteriores (P3, P4 parcial, P5, P9, P11, P12, P13, Q-4) están **resueltas** por el registro (decisiones previas y ratificación B1–B10). Los aplazamientos P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5 y Q-6 **no están resueltos**: no bloquean la revisión documental de estas fichas, pero cada uno debe resolverse antes de la fase indicada.

## 4. Antecedente histórico (versión anterior a la regularización; se conserva sin cambios de contenido)
> **ANTECEDENTE SUPERADO:** lo que sigue es el texto previo, con prerrequisitos y conteos (por ejemplo «P4 parcial», «P5, P11, P12 pendientes», «P4.A 9/18») que **ya no son vigentes**. Se conserva para trazabilidad.

### Texto anterior conservado (tabla de la versión previa a la regularización)
> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; no es decisión nueva de este documento):** las condiciones previas de 0.1–0.7 listadas en la tabla (P4, P5, P9, P11–P14, Q-4) quedaron resueltas; B10 ratifica el contenido propuesto para revisar cada aprobación, **pero no emite ninguna**: 0.1–0.7 siguen **PENDIENTES (0/7)**, la aceptación de Fase 0 sigue **no aceptada** y la Fase 1 **no autorizada**. Se requiere respuesta expresa del propietario «aprobada / rechazada / con cambios» ficha por ficha.
Estado de todas: **PENDIENTE**. Ninguna se marca ni se infiere. Orden sugerido: primero las decisiones de `MATRIZ_DECISIONES_PROPIETARIO.md`, después estas aprobaciones, al final el cierre. Responder: «aprobada», «rechazada» o «con cambios: …».
| ID | Qué aceptas | Documentos que revisar | Requiere antes resueltas | Qué dejas fuera | Estado | Respuesta |
|---|---|---|---|---|---|---|
| 0.1 Diagnóstico | inventario y estado real del repositorio (fundación comprobada; producto inexistente) | `01`, `02`, `../03_CONCILIACION_DOCUMENTAL.md`, `../13_VERIFICACION_EJECUTADA.md` | ~~P3~~ resuelta (2026-11-22), P14 | no valida el diseño | PENDIENTE | — |
| 0.2 Arquitectura | especificación browser-only y sus límites | `04` | ~~P1~~ y ~~P2~~ resueltas (2026-11-22), P9, P12, P13 | no aprueba el dominio ni la persistencia detallada | PENDIENTE | — |
| 0.3 Dominio | entidades, relaciones y responsabilidades | `05`, `06` | ~~P1~~ resuelta (2026-11-22), ~~Q-7~~ resuelta (2026-11-22), P4 (parcial: nombres confirmados; ver `DECISIONES_P4_PENDIENTES.md`) | no aprueba el alcance del MVP | PENDIENTE | — |
| 0.4 Persistencia | IndexedDB, Local Storage, archivos y recuperación | `07`, `08` | P5, P11, P12 (P6 antes de Fase 2) | no aprueba cifrado (P7) ni hosting (P10) | PENDIENTE | — |
| 0.5 IA | estrategia de integración y privacidad | `09` | P8 (antes de Fase 2; no bloquea el cierre de Fase 0) | no autoriza ninguna integración | PENDIENTE | — |
| 0.6 MVP | alcance y prioridades | `10` | Q-4 | las columnas marcadas [P] siguen sin validar | PENDIENTE | — |
| 0.7 Roadmap | Fases 1–5 y criterios AC | `11`, `12`, `15` | las que cada fase declara | no inicia ninguna fase | PENDIENTE | — |
| Final | cerrar formalmente Fase 0 | todo el expediente | las 11 indispensables y 0.1–0.7 | **no** autoriza la Fase 1 | PENDIENTE | — |
| Aparte | autorizar el inicio de Fase 1 | — | cierre de Fase 0 | — | PENDIENTE | — |
Inseparables técnicamente: ninguna. 0.3 y 0.4 se tocan por P4/P5 (el modelo determina los stores), pero pueden responderse por separado.

> **Nota fechada 2026-11-22 (auditoría cruzada):** Todas las aprobaciones 0.1–0.7, la final y la de Fase 1 siguen **PENDIENTES**; en 0.3, Q-7 está resuelta (a) y P4 sigue parcial (P4.B, P4.C, P4.E, entidades 9–12 y 14–18 abiertas). Estado vigente y fuente: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`; P4.A vigente 9/18; D-1…D-8 resueltas en su alcance. Este documento se conserva como evidencia histórica.
