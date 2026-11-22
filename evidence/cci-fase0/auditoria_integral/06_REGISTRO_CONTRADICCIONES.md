# Registro de contradicciones y su resolución — ronda de lectura completa (2026-11-22)
**Versión:** 3.0 (conserva CR-01…CR-18 de la v2.0 y añade CR-19…CR-22 hallados al cerrar la brecha de lectura) · **Fecha:** 2026-11-22 · **Estado:** vigente · **Referencias:** `12_REGISTRO_LECTURA_Y_LIMITACIONES.md`, `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt`.

**Estados finales permitidos:** RESUELTA_DOCUMENTALMENTE · RESUELTA_POR_DECISION_PROPIETARIO · HISTORICA_CON_ADVERTENCIA · PENDIENTE_PROPIETARIO · NO_RESOLUBLE_POR_FALTA_DE_EVIDENCIA. **Criterio:** una contradicción se marca «resuelta» solo si la corrección está reflejada en **todos los documentos vigentes** (no solo en una nota); los textos históricos se conservan con aviso. Sin reemplazos globales.

**Auditoría sistemática (patrones):** conteos de entidades (8/18, 9/18), definición de la entidad 13, entidad 9, Q-7/P4.4, D1–D8, D4.d, D5.a–d, D6.b/D6.c, P4.B/C/E, Q-1/Q-2, C-2/C-3, aprobaciones 0.1–0.7, aceptación de Fase 0, autorización de Fase 1, arquitectura browser-only, Supabase/PostgreSQL/Auth/RLS/backend/multiusuario históricos. Salida: `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt`; **límite:** es un escaneo de patrones sobre los archivos de `evidence/cci-fase0/` (sin `auditoria_integral/` ni `logs/`); la lectura completa posterior (ver `12_` v2.0: expediente íntegro; `docs/fase0/` por líneas únicas) no halló más contradicciones que CR-19…CR-22 y las observaciones no-CR de §«Observaciones de la lectura». **Límite:** la lectura de `docs/fase0/` omitió duplicados exactos de línea ya mostrados; no se ejecutó ningún código.

**Resumen:** 22 registradas · HISTORICA_CON_ADVERTENCIA: 5 · NO_RESOLUBLE_POR_FALTA_DE_EVIDENCIA: 1 · PENDIENTE_PROPIETARIO: 1 · RESUELTA_DOCUMENTALMENTE: 13 · RESUELTA_POR_DECISION_PROPIETARIO: 2

## CR-01 — Conteo de P4.A «8/18» presentado como vigente frente a 9/18
1. **Ubicación exacta:** `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` (aviso «Actualización posterior», línea 4 actual; nota final), `DECISIONES_P4_PENDIENTES.md` (sección P4.A y actualización cronológica), `RONDA_UNICA…`, `D3_FAMILIAS_DE_REGLAS.md`, informes de cierre, `PAQUETE_DECISION_D4…`
2. **Contradicción:** Texto «8/18 aprobadas… Prevalece este aviso» frente al ESTADO VIGENTE 9/18
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro: D4.c=A → entidad 13 aprobada; «Aclaración documental» (9/18 = 50 %; 9/18 pendientes)
5. **Clasificación del texto:** Texto 8/18 = histórico superado; 9/18 = vigente
6. **Corrección aplicada:** Ronda final: marcador «[ANTECEDENTE HISTÓRICO SUPERADO — ya no prevalece]» antes del aviso, reescritura de la frase «Prevalece este aviso» y de «(8/18) no se modifica» en la nota final de MATRIZ_18; marcador inline en DECISIONES_P4_PENDIENTES; marca en la frase del registro «no se determina aquí si D4.c lo eleva a 9». Corregido en las dos regularizaciones previas el resto
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Escaneo `logs/escaneo_contradicciones_2026-11-22_ronda_final.txt`: «Prevalece este aviso» ya no aparece como texto vigente; los archivos con «8/18» llevan aviso de vigencia; única coincidencia sin aviso: `FICHA_P4A_08` («8 de 18» = número de entidad)
9. **¿Requiere decisión del propietario?** No

## CR-02 — Entidad 13 «No presentada» frente a aprobada (D4.c=A)
1. **Ubicación exacta:** `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` fila 13 y notas
2. **Contradicción:** Estado anterior «No presentada», columnas de propuesta («Dependencias: D-1, D-4», «Mantener; delimitar») frente a aprobación con definición mínima
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro D4.c=A (texto literal)
5. **Clasificación del texto:** Columnas de propuesta = histórico; definición literal = vigente
6. **Corrección aplicada:** Fila 13 con la definición literal de D4.c; ronda final: columnas históricas de la propuesta rotuladas como tales y declarando que no se aprueban atributos, relaciones, cardinalidades, mecanismos, estructura, persistencia, versionado ni fase
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Verificación textual de la fila 13 en HEAD de la ronda; `03_MATRIZ_MAESTRA_ENTIDADES_P4A.md` extrae la definición literal con script
9. **¿Requiere decisión del propietario?** No

## CR-03 — Entidad 9: «pendiente de decisión» frente a suspendida
1. **Ubicación exacta:** `FICHA_P4A_09_HALLAZGO.md` (título), matriz 18, índice 16
2. **Contradicción:** Título «PENDIENTE DE DECISIÓN» frente a «SUSPENDIDA (11:58)»
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro, «Ajuste de método de P4.A — 11:58»
5. **Clasificación del texto:** El título es el estado al elaborar la ficha; el encabezado «Estado» aclara la suspensión
6. **Corrección aplicada:** Sin cambio de texto (coherente); índice 16 indica «SUSPENDIDA, sin aprobar»
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Lectura íntegra de la ficha 09 y del índice 16 en esta ronda
9. **¿Requiere decisión del propietario?** No

## CR-04 — Q-7/P4.D «pendiente» y P4.4 «aplazado» frente a resueltas/cerrada
1. **Ubicación exacta:** `FICHA_P4.md`, `MATRIZ_DECISIONES_PROPIETARIO.md`, `DECISIONES_P4_PENDIENTES.md`, `LISTA_ORIGINAL_18_ENTIDADES.md` (línea 41), registro (encabezado «P4.4 — APLAZADO»)
2. **Contradicción:** «Campaña sujeta a Q-7», «P4.4 APLAZADO», «Q-7 pendiente»
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro: «Q-7 — RESUELTA → (a)» y «Confirmaciones 11:38» (P4.4 cerrada)
5. **Clasificación del texto:** Textos de pendiente/aplazado = cronológicos superados
6. **Corrección aplicada:** Notas fechadas en registro, FICHA_P4 y MATRIZ_DECISIONES (rondas previas); ronda final: nota inline en `LISTA_ORIGINAL_18_ENTIDADES.md` y bloque «Ya resuelto» de `DECISIONES_P4_PENDIENTES.md`
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Escaneo: `Q-7 pendiente` / `P4.4 aplazado` solo en archivos con aviso; verificación específica de FICHA_P1 y LISTA_ORIGINAL
9. **¿Requiere decisión del propietario?** No

## CR-05 — D-1, D-2, D-3 y D-5 «pendiente de decisión» en el índice 16
1. **Ubicación exacta:** `16_INDICE_EVIDENCIAS_FASE0.md`
2. **Contradicción:** Entradas con estado histórico frente a resueltas
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro (D-1…D-5)
5. **Clasificación del texto:** Estado histórico al elaborarse = antecedente
6. **Corrección aplicada:** Entradas con «estado histórico … estado vigente RESUELTA»
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Lectura íntegra del índice 16 en esta ronda
9. **¿Requiere decisión del propietario?** No

## CR-06 — D4/D6/D7/D8 «pendientes» en documentos de apoyo
1. **Ubicación exacta:** `CATALOGO_DEPENDENCIAS_D4_D8.md`, `DECISIONES_P4_PENDIENTES.md`, `PAQUETE_DECISION_D4_D6_D7_D8.md`, `PAQUETE_DECISION_D1_D8.md`, `RONDA_UNICA…`
2. **Contradicción:** «pendiente», «sin responder» frente a 11/11 resueltas
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro (D4.a–d, D6.a–c, D7.a–c, D8)
5. **Clasificación del texto:** Texto de estado pendiente = histórico superado
6. **Corrección aplicada:** Encabezados vigentes y columna «Estado» en CATALOGO; ronda final: aviso «PAQUETE RESPONDIDO» en `PAQUETE_DECISION_D4_D6_D7_D8.md` y marcadores inline en DECISIONES_P4_PENDIENTES; `PAQUETE_DECISION_D1_D8` ya figura como SUSTITUIDO
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Lectura íntegra de CATALOGO y DECISIONES_P4_PENDIENTES; escaneo
9. **¿Requiere decisión del propietario?** No

## CR-07 — D4.d aprobada frente a «Adaptación pendiente de D-4» / «D4.d no aprobada»
1. **Ubicación exacta:** Registro (D-5.2 y nota 12:35/corrección: «D4.d… no está aprobada»), `MATRIZ_CONSOLIDADA_18_ENTIDADES.md` (aviso 12:29), `PAQUETE_DECISION_D1_D8.md`, `PAQUETE_DECISION_D4_D6_D7_D8.md` (§D4.d), `RONDA_UNICA…` (alternativa C), `CONTROL_DE_CAMBIOS_REGISTRO…`
2. **Contradicción:** Adaptación como pendiente/no aprobada frente a D4.d=A
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro: D4.d=A (limitada por M-1 y D-5.3) y «Nota fechada: D4.d»
5. **Clasificación del texto:** «pendiente» = histórico superado; D4.d=A = vigente (sin auditoría directa de Adaptación, sin publicación/distribución, sin certificación legal/comercial/de marca, sin reglas adicionales inferidas)
6. **Corrección aplicada:** Nota fechada en el registro (rondas previas); ronda final: marcas inline en las dos frases del registro, aviso en MATRIZ_18, aviso «PAQUETE RESPONDIDO», fila 13 de MATRIZ_18. Barrido completo de «D4.d … pendiente/no aprobada»: las coincidencias restantes están en documentos con aviso de vigencia (paquetes, matriz de la ronda, controles de cambio)
7. **Estado final:** **RESUELTA_POR_DECISION_PROPIETARIO**
8. **Evidencia de verificación:** Escaneo, patrón `D4.d pendiente`: coincidencias solo en archivos con `aviso_vigencia=True`; sin D4.d presentada como pendiente en documentos vigentes (índice maestro, matrices 02/03/04, 09, MATRIZ_18 vigente, DECISIONES_P4 vigente)
9. **¿Requiere decisión del propietario?** No

## CR-08 — Fichas P4.A 01–08 «pendiente» en el índice 16
1. **Ubicación exacta:** `16_INDICE_EVIDENCIAS_FASE0.md`
2. **Contradicción:** «pendiente» frente a resueltas
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro (entidades 1–8)
5. **Clasificación del texto:** «pendiente» = estado al elaborarse la ficha
6. **Corrección aplicada:** Entradas con estado vigente; histórico preservado en cada ficha
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Lectura íntegra del índice 16 y cabeceras de las fichas 01–08
9. **¿Requiere decisión del propietario?** No

## CR-09 — `docs/fase0/` declara «Fase 0 v3.3 COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL» y diseña Supabase/PostgreSQL/RLS/multiusuario frente a Fase 0 vigente no aceptada y browser-only
1. **Ubicación exacta:** 59 archivos de `docs/fase0/` (52 históricos + 5 raíz v15 + 2 herramientas)
2. **Contradicción:** Aceptación de una Fase 0 anterior y arquitectura con backend
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** P1, P2, P3 (b, condiciones 3–5 y 7); aceptación formal de la Fase 0 vigente: no aceptada
5. **Clasificación del texto:** Histórico no vinculante (línea anterior)
6. **Corrección aplicada:** Los archivos NO se modifican (prohibido); advertencia en `11_INDICE_CONCILIACION_DOCS_FASE0.md`, `12_REGISTRO_LECTURA_Y_LIMITACIONES.md`, `01_INDICE_MAESTRO_FASE0.md` e `INDICE_ANTECEDENTES_HISTORICOS.md`. **C-2 sigue abierta** (ver CR-17)
7. **Estado final:** **HISTORICA_CON_ADVERTENCIA**
8. **Evidencia de verificación:** Conteos de escaneo (aceptación/Supabase/PostgreSQL/RLS) en `12_` §5; hash y tamaño idénticos a `main` (11_)
9. **¿Requiere decisión del propietario?** No

## CR-10 — Referencias a Supabase/PostgreSQL/RLS/multiusuario dentro del expediente actual
1. **Ubicación exacta:** `anexos/INFORME_AUDITORIA…` (34 menciones Supabase), `03_CONCILIACION_DOCUMENTAL.md`, `ADR_PROPUESTO…`, `FICHA_P2.md`, `FICHA_P3.md`, `MATRIZ_DECISIONES_PROPIETARIO.md`, `REGISTRO_DECISIONES_RESUELTAS.md`, `13_REGISTRO…`, `10_REGISTRO…`, copias previas de la raíz
2. **Contradicción:** Vocabulario de la arquitectura anterior en documentos del expediente
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Arquitectura vigente: browser-only (P1, P2, P3)
5. **Clasificación del texto:** Descripción de la línea anterior, negaciones («sin Supabase») o propuestas históricas; no requisitos
6. **Corrección aplicada:** Revisión por contexto en rondas previas; ronda final: aviso de vigencia en las copias previas de la raíz (10 archivos) además de las advertencias existentes en 05/06/07 de la raíz y `entregables_formales`
7. **Estado final:** **HISTORICA_CON_ADVERTENCIA**
8. **Evidencia de verificación:** Escaneo (`Supabase/PostgreSQL/RLS`, `multiusuario`) por archivo; sin presencia como requisito en documentos vigentes (`04_ARQUITECTURA`, índice maestro)
9. **¿Requiere decisión del propietario?** No

## CR-11 — Fórmulas de «Pre-condición: Fase 0 aceptada y Fase 1 autorizada» en roadmap y criterios
1. **Ubicación exacta:** `11_ROADMAP…`, `12_CRITERIOS…`, copias raíz
2. **Contradicción:** Parece afirmar aceptación
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Son condiciones de entrada de cada fase, no afirmaciones de estado
5. **Clasificación del texto:** Condición (vigente como requisito futuro)
6. **Corrección aplicada:** Sin cambio; no se cuenta como contradicción real
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Lectura de contexto; Fase 0 no aceptada y Fase 1 no autorizada (índice maestro)
9. **¿Requiere decisión del propietario?** No

## CR-12 — Referencias a archivos que no existen en la rama (documentos de la aplicación, adjuntos A y B, expedientes anteriores)
1. **Ubicación exacta:** Ver `05_INFORME_AUDITORIA_INTEGRAL.md` §4 y `12_` §6
2. **Contradicción:** Citas a documentos que no pueden verificarse aquí
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** —
5. **Clasificación del texto:** Referencias externas al expediente
6. **Corrección aplicada:** Clasificadas; no se inventa su contenido
7. **Estado final:** **NO_RESOLUBLE_POR_FALTA_DE_EVIDENCIA**
8. **Evidencia de verificación:** Búsqueda de referencias a archivos en la rama; los archivos citados no existen en el árbol de la API
9. **¿Requiere decisión del propietario?** No

## CR-13 — Copias previas de la raíz (00–14) frente a `entregables_formales/` (01–16) con numeración distinta; `00_DICTAMEN` «LISTO PARA REVISIÓN / Recomendación de aceptación»
1. **Ubicación exacta:** Raíz y `entregables_formales/`
2. **Contradicción:** Dos series de documentos con estados distintos; recomendación de aceptación en el dictamen previo
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro y `00_INDICE_VIGENTES_E_HISTORICOS.md`: prevalece `entregables_formales/`
5. **Clasificación del texto:** Raíz = histórico (copia previa)
6. **Corrección aplicada:** Ronda final: **aviso de vigencia añadido a 10 copias previas de la raíz** (00, 01, 02, 04, 08, 09, 11, 12, 13, 14); el contenido original no se altera
7. **Estado final:** **HISTORICA_CON_ADVERTENCIA**
8. **Evidencia de verificación:** Aviso presente en los 10 archivos (verificado por escaneo de «AVISO DE VIGENCIA»)
9. **¿Requiere decisión del propietario?** No

## CR-14 — `MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` con 7 hashes que ya no coinciden
1. **Ubicación exacta:** `entregables_formales/MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt`
2. **Contradicción:** Hashes de un paquete anterior frente a archivos modificados después
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Vigentes: `MANIFEST.sha256` e `INVENTARIO_PUBLICADO.sha256`
5. **Clasificación del texto:** Manifiesto histórico fechado
6. **Corrección aplicada:** No se altera para forzar coincidencia; clasificado «Integridad (histórico)»
7. **Estado final:** **HISTORICA_CON_ADVERTENCIA**
8. **Evidencia de verificación:** Comprobación 0/7 coincidencias (esperado)
9. **¿Requiere decisión del propietario?** No

## CR-15 — Numeración «19» y Evento de actividad: D-1.a «no añade una entidad 19» frente a P4.3 (Evento de actividad aprobada como entidad propuesta)
1. **Ubicación exacta:** Registro (D-1.a, P4.3, D-5, «D-4 reformulada y D-5 presentada»); `CATALOGO_DEPENDENCIAS_D4_D8.md` §1; `LISTA_ORIGINAL…` (conteo 21)
2. **Contradicción:** Aparente conflicto entre «sin entidad 19» y una entidad añadida
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Registro: D-1.a se refiere a «Contenido» (concepto paraguas); P4.3 añade Evento de actividad fuera de la lista de 18; la asociación «19»=Evento fue una inferencia de Claude **no confirmada y no asumida** (registro, 12:21)
5. **Clasificación del texto:** «19» = etiqueta de trabajo no confirmada (no es un dato del propietario)
6. **Corrección aplicada:** Aclaración: no hay contradicción entre decisiones; se **deja de usar «19»**; el conteo 9/18 se calcula solo sobre la lista de 18 (P4.1); Evento de actividad, Etiqueta y Perfil local (P4.3) están aprobados fuera de ese conteo; el «21» de LISTA_ORIGINAL = 18 + 3 de P4.3. **No es una pregunta para el propietario** (antes figuraba como «Abierta» por error de enfoque)
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Registro, secciones D-1.a, P4.3 y «D-4 reformulada»; documentado en `03_` §D
9. **¿Requiere decisión del propietario?** No

## CR-16 — «Tensión» D6.b=A frente a D6.c=A0
1. **Ubicación exacta:** Antes: `06_REGISTRO_CONTRADICCIONES.md` (CR-16 anterior), `09_PAQUETE…` (observación en A0-1), `10_INFORME_EJECUTIVO…` (riesgos y paso 5)
2. **Contradicción:** Lectura incorrecta: que A0 y D6.b=A se condicionaran entre sí y requirieran confirmación
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Decisión del propietario: **D6.b=A es independiente**; D6.c=A0 deja abiertas la clasificación del origen, L1, L2 y L3; **A0 no presupone ni aprueba D6.b=A**; D6.b=A **no resuelve** la clasificación del origen
5. **Clasificación del texto:** Interpretación incorrecta de Claude (no decisión del propietario)
6. **Corrección aplicada:** La aparente contradicción se resuelve por la independencia ya decidida. Se mantienen abiertas las cuatro subcuestiones de A0 (origen de valores, L1/L2, L3). Se eliminó la «Observación» de tensión en PAQ-2 (A0-1) y se retiró este ítem del informe ejecutivo. **No es una decisión del propietario ni se le pide confirmación**
7. **Estado final:** **RESUELTA_POR_DECISION_PROPIETARIO**
8. **Evidencia de verificación:** Registro (D6.b, D6.c, «Efectos y límites»); `09_` A0-1 reescrito; `10_` actualizado.
9. **¿Requiere decisión del propietario?** No

## CR-17 — C-2 (estado de la Fase 0 v3.3 anterior) y C-3 (D-04 «APROBADA», cinco roles)
1. **Ubicación exacta:** `INDICE_ANTECEDENTES_HISTORICOS.md` §5; registro P3 condición 7
2. **Contradicción:** Contradicciones históricas entre documentos anteriores
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** P3 cond. 7: se mantienen abiertas; no se resuelven por inferencia
5. **Clasificación del texto:** Contradicciones históricas abiertas
6. **Corrección aplicada:** Ninguna (no se pueden resolver con las decisiones ya emitidas)
7. **Estado final:** **PENDIENTE_PROPIETARIO**
8. **Evidencia de verificación:** Registro P3; PAQ-5 de `09_`
9. **¿Requiere decisión del propietario?** Sí (contradicción histórica abierta por P3, condición 7)

## CR-18 — Conteos de clasificación: «93/93 archivos clasificados» frente a 104 archivos reales; 99 filas únicas; cinco documentos de auditoría sin clasificar
1. **Ubicación exacta:** `05_INFORME_AUDITORIA_INTEGRAL.md` (versión anterior), `10_INFORME_EJECUTIVO…`, `08_INFORME_INTEGRIDAD_ARCHIVOS.md`
2. **Contradicción:** 93 frente a 104 (93 previos + 11 nuevos); la tabla omitía 05, 06, 07, 08 y 10
3. **Documentos en conflicto:** véase la ubicación; el vigente es el indicado en el punto 4.
4. **Decisión o fuente prevalente:** Árbol real de la rama (API): 164 blobs = 104 en `evidence/cci-fase0/` + 59 en `docs/fase0/` + 1 `README.md` de raíz
5. **Clasificación del texto:** Error propio de la auditoría anterior
6. **Corrección aplicada:** `05_` rehecho con la clasificación de **todos** los archivos actuales (incluidos los 12 documentos de la auditoría y los 2 archivos de log nuevos); 93/93 ya no se presenta como cobertura del total; 10_ y 08_ actualizados
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Recuento `05_` §1 generado por script y comparado con el árbol de la API
9. **¿Requiere decisión del propietario?** No

## CR-19 — `README_PROPUESTA_VIGENTE.md`: fila «Pendiente: P1–P15, Q-1…Q-6» frente a decisiones ya emitidas
1. **Ubicación exacta:** `entregables_formales/README_PROPUESTA_VIGENTE.md` (tabla de estado, fila «Pendiente»)
2. **Contradicción:** Presenta P1–P15 y Q-1…Q-6 como pendientes, mientras el mismo documento marca P2 «Sustituido» y P3=b, y el registro resuelve P1, P2, P3 y Q-7
3. **Documentos en conflicto:** `README_PROPUESTA_VIGENTE.md` frente a `REGISTRO_DECISIONES_RESUELTAS.md`
4. **Decisión o fuente prevalente:** Registro: P1=(b), P2=(a)+Seguridad por diseño, P3=(b), Q-7=(a), D-1…D-3, D-5, D4/D6/D7/D8; P4.A 9/18
5. **Clasificación del texto:** Estado anterior superado (propuesta previa); el original se conserva
6. **Corrección aplicada:** «Nota de actualización posterior» añadida al final del archivo, sin alterar el texto original; enumera lo resuelto y lo que sigue pendiente (P4.B/C/E, P5–P15, Q-1…Q-6, C-2, C-3, entidades 9–12 y 14–18)
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Lectura íntegra del archivo y del registro; `git diff` de la nota; cifras comprobadas contra el registro
9. **¿Requiere decisión del propietario?** No (lo pendiente sigue siendo del propietario y no se resolvió)

## CR-20 — Copias previas de la raíz sin aviso de vigencia (`03_CONCILIACION_DOCUMENTAL.md`, `10_REGISTRO_DECISIONES.md`, `INFORME_REVISION_COMPLEMENTARIA.md`) y cabecera del manifiesto de entrega
1. **Ubicación exacta:** `03_CONCILIACION_DOCUMENTAL.md`, `10_REGISTRO_DECISIONES.md`, `INFORME_REVISION_COMPLEMENTARIA.md` (raíz de `evidence/cci-fase0/`); `entregables_formales/MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt`
2. **Contradicción:** Propuestas/registros anteriores (anteriores a P1, P2, P3, Q-7, D-1…D-8) se leían como estado vigente por no llevar aviso, a diferencia de 05, 06 y 07; el manifiesto de entrega conserva 7 hashes que ya no coinciden (ver CR-14)
3. **Documentos en conflicto:** las tres copias frente a `REGISTRO_DECISIONES_RESUELTAS.md` y `01_INDICE_MAESTRO_FASE0.md`
4. **Decisión o fuente prevalente:** Registro de decisiones resueltas; jerarquía de fuentes del índice maestro; P3=(b) para antecedentes
5. **Clasificación del texto:** Histórico / propuesta anterior; se conserva
6. **Corrección aplicada:** «AVISO DE VIGENCIA» (blockquote) antepuesto a las tres copias y línea `# NOTA` de cabecera en el manifiesto; el contenido original no se altera (los 7 hashes siguen sin coincidir, por diseño: ver CR-14)
7. **Estado final:** **HISTORICA_CON_ADVERTENCIA**
8. **Evidencia de verificación:** `git diff` (solo líneas añadidas); lectura íntegra de cada copia
9. **¿Requiere decisión del propietario?** No

## CR-21 — Regresión propia: `00_INDICE_VIGENTES_E_HISTORICOS.md` y `README_ENTREGA.md` truncados en el commit `1cf96e3`
1. **Ubicación exacta:** `00_INDICE_VIGENTES_E_HISTORICOS.md` (5 184 → 510 B) y `README_ENTREGA.md` (4 545 → 342 B) en el commit `1cf96e3` de la auditoría integral
2. **Contradicción:** Al añadir una línea se escribió solo esa línea y el contenido previo (de `1bb831a`) desapareció del árbol (no de la historia de git); los dos índices dejaron de cumplir su función
3. **Documentos en conflicto:** versión publicada en `1cf96e3`/`13b25ca` frente a la de `1bb831a`
4. **Decisión o fuente prevalente:** Contenido de `1bb831a`, restaurado íntegro
5. **Clasificación del texto:** Defecto propio de la auditoría (no del propietario ni del expediente anterior)
6. **Corrección aplicada:** Restauración desde `1bb831a` con nota «RESTAURACIÓN» y el texto añadido de la auditoría; el resto no se reescribió. Un barrido de tamaños sobre el historial de git de `evidence/cci-fase0/` (repetido en la ronda de coherencia, todos los commits) no halló otra reducción mayor al 10 %
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE**
8. **Evidencia de verificación:** Tamaños actuales 6 601 B y 5 255 B; comparación con la historia; manifiestos regenerados
9. **¿Requiere decisión del propietario?** No (se informa para transparencia)

## CR-22 — Roadmap del anexo original (Fases 0–5 con Persistencia, Capacidades, IA y Endurecimiento) frente al roadmap vigente `11_ROADMAP_FASES_0_A_5.md` (Fases 1–5 de producto) y roadmaps históricos
1. **Ubicación exacta:** `anexos/INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md` §15; `docs/fase0/historico/ROADMAP_Y_TRAZABILIDAD_…_v2_historico.md` (Fases 0–9); `entregables_formales/11_ROADMAP_FASES_0_A_5.md`
2. **Contradicción:** Tres definiciones distintas del contenido de las fases (p. ej. Fase 2 = «Persistencia local» en el anexo frente a «Copy Studio» en el roadmap de entregables_formales; Fases 0–9 en el roadmap histórico v2)
3. **Documentos en conflicto:** véase la ubicación
4. **Decisión o fuente prevalente:** Las seis fases generales son del propietario; su contenido está **propuesto, no aprobado**, en `entregables_formales/11_ROADMAP_FASES_0_A_5.md` (propuesta vigente, subordinada al registro). El anexo es el informe original (hash declarado; inmodificable) y los roadmaps de `docs/fase0` son históricos (P3=b)
5. **Clasificación del texto:** Anexo = antecedente; `docs/fase0` = histórico con advertencia; `11_ROADMAP…` = propuesta vigente pendiente de aprobación
6. **Corrección aplicada:** Nota de vigencia en `00_INDICE_VIGENTES_E_HISTORICOS.md` y en `01_INDICE_MAESTRO_FASE0.md`; el anexo y `docs/fase0` no se modifican
7. **Estado final:** **RESUELTA_DOCUMENTALMENTE** (en cuanto a cuál texto es vigente; **no** se decide el contenido de las fases)
8. **Evidencia de verificación:** Lectura íntegra de los tres textos; el anexo sigue coincidiendo con su SHA-256 declarado
9. **¿Requiere decisión del propietario?** El contenido y la aprobación de las fases (P5–P15 / fases) siguen siendo del propietario; la vigencia documental no

## Observaciones de la lectura (no son contradicciones nuevas)
- Los documentos 05 (§3, §4 y §5), 06 (preámbulo), 07 (R6), 10 (fila de lectura) y 11 (advertencia 4) afirmaban «lectura parcial / no íntegra»: actualizados en la ronda de lectura.
- `docs/fase0` (históricos, inmutables): erratas internas (p. ej. v14 cita `…_v12_historica.md` donde existe `…_v13_historica.md`; filas T-698/T-701 truncadas en origen; residuos «v14» dentro de la v15; rangos «T-777 a T-777»; huella 69f465850efed7d3 compartida por «registro v8» y «vigente» como anotación). No se corrigen (P3=b; sin modificar `docs/fase0`).
- Artefactos del método de líneas únicas (encabezados repetidos omitidos en la visualización) no son defectos de los archivos.

## Descartes y limitaciones
- La versión anterior de este registro contaba 16 contradicciones y dejaba CR-15 y CR-16 como «Abiertas — requieren al propietario»; **ambas eran incorrectas** (ver CR-15 y CR-16 de esta versión).
- Este registro **no** declara que Fase 0 esté libre de contradicciones: afirma solo las verificadas por escaneo y lectura (ver `12_`). No se ejecutó código ni se re-verificaron resultados de pruebas.

## Verificación de coherencia posterior (2026-11-22; base `580c51f`)
Esta ronda verificó la coherencia de los archivos modificados desde la regularización (informe: `13_INFORME_VERIFICACION_COHERENCIA_POSTERIOR.md`). **No cambió el estado de ningún CR** (CR-01…CR-22 conservan el estado indicado arriba); los hallazgos F1–F8 son anotaciones desactualizadas o referencias erróneas corregidas sin alterar decisiones (ver `07_` R8). CR-17 (C-2/C-3) sigue pendiente del propietario y CR-12 sigue no resoluble por falta de evidencia. CR-22 permanece como registro de versiones de roadmap: `11_ROADMAP_FASES_0_A_5.md` sigue siendo propuesta no aprobada.
