# Paquete consolidado de decisiones que el propietario todavía debe resolver (2026-11-22)
**Naturaleza:** preparación documental. **No registra decisiones, no aprueba nada y no solicita aceptar Fase 0 ni autorizar Fase 1.** Subordinado a `../entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Lo ya resuelto (incluidas D1–D8, D5.a–d fuera de alcance) **no se vuelve a preguntar**.
**Convenciones:** **[P]** = texto propuesto por Claude (no es decisión); **[Rec. Claude]** = recomendación no vinculante; **[Fuente]** = evidencia del expediente. Las opciones listadas son las que constan en el expediente; donde la evidencia no alcanza se indica qué información falta, sin inventar opciones.
**Respuesta sugerida:** una línea por ID (p. ej. `PE-09 = a`). Una letra significa aceptar **solo** el contenido de esa alternativa; el silencio no aprueba.

## Orden y agrupación
PAQ-1 y PAQ-2 (entidades; pueden responderse juntos) → PAQ-3 (P4.B) → PAQ-4 (P4.C/P4.E) · PAQ-5 (Q/C) y PAQ-6 (técnicas de Fase 0) independientes · PAQ-7 (posteriores, antes de su fase). Después, y solo después, las aprobaciones 0.1–0.7.

---
## PAQ-1 — Entidades 9 a 12 (P4.A)
Para cada entidad las opciones reales son: **(a)** aprobar la definición mínima propuesta tal cual; **(b)** aprobar con los cambios que indique el propietario; **(c)** mantener sin aprobar. Aprobar una definición mínima **no** aprueba atributos, relaciones, cardinalidades, estructura, persistencia, mecanismos, reglas ni fase (como en las entidades 1–8 y 13).

**PE-09 Hallazgo de auditoría** — suspendida. [P] «Problema u observación identificado durante una auditoría creativa, que debe poder explicarse y seguirse hasta su resolución.» [Fuente] A l.356; B l.205, 450–462, 67; `FICHA_P4A_09_HALLAZGO.md`. Resuelto que condiciona: D-1.c (la Auditoría creativa se limita a Copy y Pieza; no audita Adaptación). Riesgo/contradicción: frontera con la entidad 8 (el hallazgo tiene estado y resolución propios y puede sobrevivir a una reauditoría). Riesgo de arrastrar «Regla» genérica (D-3 la excluye). [Rec. Claude] (a), aclarando que «seguimiento hasta su resolución» no fija estados. Consecuencia de (c): P4.B no puede cerrar la relación Auditoría–Hallazgo ni Q-5.
**PE-10 Regla de marca** — [P] «Regla de marca que aplica al contenido y se usa en auditoría.» [Fuente] B l.435; P4.2=(b); D-3. **Información faltante:** las instrucciones originales no contienen una lista específica de reglas de marca (limitación documentada en D-3); no se inventa. [Rec. Claude] (a) solo existencia y propósito, sin contenido de reglas; alternativa legítima (c) hasta que el propietario aporte criterios. Riesgo: confundir con reglas de copy (D-3.c: ubicación pendiente de P4.B).
**PE-11 Regla comercial** — [P] «Regla comercial usada por el validador promocional; sus tolerancias son parámetros de la propia regla.» (la segunda cláusula es D7.b=A, ya decidida). [Fuente] B l.206, 504–523; D7.b. Depende de Q-1 para valores (no se aprueban aquí). [Rec. Claude] (a).
**PE-12 Canal** — [P] «Canal de comunicación aprobado por el propietario; las reglas por canal son una dimensión de aplicación del Canal.» (D-3.c; D7.c=C: lista inicial Ecommerce, App, WhatsApp, Email, Redes sociales, Banners, Landing pages, más otros formatos aprobados por el propietario, sin mecanismo de ampliación). [Fuente] B l.538–547. Depende de Q-2 para reglas concretas. [Rec. Claude] (a) sin lista definitiva ni reglas.
**¿Conjunta?** Sí: las cuatro pueden resolverse en una respuesta. **Se registra en:** registro autoritativo (sección P4.A, nuevas entidades) + conteo en matrices 03.

## PAQ-2 — Entidades 14 a 18 y subcuestiones de A0
**PE-14 Versión de contenido** — [P] «Estado fechado y trazable de un contenido a lo largo del tiempo» (D-2: Versión = evolución o revisión temporal; D-1.d: Copy, Pieza y Adaptación pueden tener versiones; Variante sin versiones propias por ahora). Riesgo: solapamiento con Evento de actividad. [Rec. Claude] (a). Opciones (a)/(b)/(c).
**PE-15 Aprobación** — [P] «Registro de una decisión humana de aprobación» (D-5.3 M-1: decisión humana final de que un contenido, en las condiciones revisadas, está conforme para pasar a la Biblioteca; aprobables: Copy, Pieza, Adaptación (D4.d=A); un único usuario local, P1). Riesgo: los 7 estados del flujo son estados del contenido, no de una aprobación → se trata en Q-3. [Rec. Claude] (a) sin definir estados ni identidad técnica del contenido aprobado.
**PE-16 Resultado de desempeño** — nombre fijado por D8=A. [P] «Registro de desempeño proporcionado por el usuario; los valores de las métricas pertenecen al Resultado (D6.c=A0).» Opciones (a)/(b)/(c). [Rec. Claude] (a) manteniendo pendientes A0-1/2/3.
**PE-17 Métrica** — [P] «Definición de una métrica (indicador); los valores no pertenecen a la Métrica sino al Resultado (D6.c=A0).» Sin fórmulas ni catálogo. [Rec. Claude] (a).
**PE-18 Configuración de la aplicación** — [P] «Preferencias y configuraciones duraderas de la aplicación; distinta del Perfil local (D7.a=A).» Dónde se guarda es decisión aparte. [Rec. Claude] (a).
**A0-1 Clasificación del origen del valor** (manual / importado / calculado). Opciones: (a) clasificarlo conceptualmente en el Resultado; (b) no clasificarlo todavía (puede quedar pendiente, como permite A0); (c) otra decisión del propietario. **Relación con D6.b (ya decidida, independiente):** D6.b=A fijó el significado conceptual de «valor calculado» (valor cuyo origen es un cálculo). D6.c=A0 no presupone ni aprueba D6.b=A y deja abierta, aquí, la clasificación del origen de los valores en el Resultado. Las dos decisiones son independientes; **no hay tensión que el propietario deba confirmar** (ver CR-16 en `06_REGISTRO_CONTRADICCIONES.md`, resuelta por la independencia ya decidida). Esta pregunta A0-1 solo concierne a la clasificación del origen. [Rec. Claude] (b) si el MVP no requiere distinguir el origen.
**A0-2 L1 frente a L2** (mutuamente excluyentes). L1 = el valor calculado se deriva al mostrarse y no se conserva; L2 = se conserva en el Resultado. Consecuencias: L1 evita inconsistencias entre valor y fórmula pero requiere conservar entradas; L2 conserva el histórico del cálculo pero puede divergir de la definición vigente. Opciones: L1, L2, diferir. [Rec. Claude] diferir hasta definir fórmulas (no decididas).
**A0-3 L3** (el Resultado referencia la definición de la métrica que originó el cálculo). Independiente de L1/L2; combinable con cualquiera (A4 = A0+L1+L3; A5 = A0+L2+L3). Opciones: sí, no, diferir. [Rec. Claude] diferir.
**¿Conjunta?** PE-14…PE-18 sí; A0-1…3 pueden responderse al mismo tiempo o diferirse. **Registro:** registro autoritativo.

## PAQ-3 — P4.B Relaciones y cardinalidades (después de PAQ-1 y PAQ-2)
**Posición ya registrada del propietario (11:38):** se conservan como con fundamento solo las relaciones respaldadas expresamente por las instrucciones; las cardinalidades se presentan y justifican por separado; Campaña–Oferta y Campaña–Pieza son propuestas a resolver individualmente después de P4.A.
**Con base [D]:** Campaña–Brief (maestra l.347), Campaña–Resultado (l.639). **Propuestas [P] sin base explícita:** Campaña–Oferta, Campaña–Pieza. **También pendientes:** ubicación de las reglas de copy (D-3), relación Adaptación–Pieza (D4.b: «puede relacionarse»; sin relación definida), relaciones de las entidades 9–12 y 14–18, relación Métrica–Resultado (A0).
Opciones reales (de `DECISIONES_P4_PENDIENTES.md`): aprobar solo las [D]; aprobar también las [P] que el propietario elija; rechazar. [Rec. Claude] aprobar [D] y decidir las [P] una a una.
**Información faltante para preparar la matriz completa:** no pueden enumerarse las relaciones de las entidades 9–12 y 14–18 mientras sus definiciones no estén aprobadas; se presentarán al cerrar PAQ-1/PAQ-2 (no se inventan ahora). **Registro:** registro autoritativo (sección P4.B).

## PAQ-4 — P4.C Atributos y P4.E Convenciones
**P4.C:** el propietario difirió los atributos a la especificación de cada módulo; solo se presentarán antes los indispensables para el MVP, con justificación; ninguno aprobado. Opciones: especificarlos al cerrar P4.A/B, o diferirlos. [Rec. Claude] diferir, aprobando antes solo los obligatorios del MVP. **Depende de Q-4** (alcance del MVP). **Información faltante:** la lista de atributos «indispensables» no existe todavía; requiere Q-4 y P4.B.
**P4.E (P4.5 sigue PRELIMINAR):**
- **E1 Fechas:** confirmar ISO-8601 UTC solo para almacenamiento y cómo se guardan fechas comerciales y zona horaria. [P] campo de fecha local `YYYY-MM-DD` + zona declarada.
- **E2 `revision`:** no obligatoria; justificar necesidad real (ligada a P12). [Rec. Claude] mantener abierta hasta P12.
- **E3 Archivar frente a eliminar:** definir semántica de `archivedAt` y del borrado.
- **E4 Desconocido/cero/vacío/no aplicable:** [P] null vs ausente vs 0 vs marca explícita.
- **E5 Hash de versiones:** redacción como integridad/trazabilidad, no seguridad.
[Rec. Claude] aprobar E1, E3, E4, E5 con las propuestas de `CONVENCIONES_P4_5_CONDICIONES.md`; E2 abierta. **Registro:** registro autoritativo (P4.5 definitiva).

## PAQ-5 — Cuestiones Q y contradicciones C
- **Q-1** (redondeo y tolerancias del descuento): [Fuente] fórmula dada; el propietario decide valores. [Rec. Claude] redondeo a 2 decimales «mitad hacia arriba» y tolerancia configurable en puntos porcentuales (D7.b: la tolerancia es parámetro de ReglaComercial). **Falta:** los valores reales; no se inventan.
- **Q-2** (canales aprobados y reglas por canal): lista inicial ya fijada por D7.c=C. **Falta:** límites reales por canal (longitudes, estructura) que solo puede aportar el propietario.
- **Q-3** (estados del flujo): [Fuente] siete estados propuestos en las instrucciones (B l.609–617). Opciones: aprobar los 7 y transiciones; modificar; diferir a Fase 5. [Rec. Claude] aprobar los 7 estados y transiciones como estados del **contenido** (no de la Aprobación), un solo usuario local.
- **Q-4** (MVP): opciones (a) fin de Fase 2; (b) fin de Fase 3; (c) producto completo (Fase 5). [Rec. Claude] (a). Las columnas de módulos 6–9 del MVP son propuestas no sustentadas.
- **Q-5** (ponderaciones de puntuación): el propietario define categorías y pesos; **falta** esa información. Se pospone a antes de Fase 3.
- **Q-6** (idioma y diccionario): [Rec. Claude] español inicial; el diccionario depende de P13.
- **C-2** y **C-3:** contradicciones históricas de los expedientes anteriores (Fase 0 v3.3; D-04). La evidencia localizada no permite resolverlas; **requieren decisión o aclaración expresa del propietario**. Opciones documentadas en P15/INDICE_ANTECEDENTES: declararlas históricas sin efecto sobre la Fase 0 browser-only; o aportar la aceptación/aprobación faltante. No se resuelve aquí.
**Registro:** registro autoritativo.

## PAQ-6 — Decisiones técnicas indispensables de Fase 0
- **P5 Binarios:** (a) Blobs con tope; (b) solo metadatos; (c) diferir a Fase 3. [Rec. Claude] (a) con tope y avisos de cuota. Falta: cuotas por navegador (no verificadas).
- **P9 «Producción» local:** (a) modo `local` real + `demo` solo en test; (b) mantener bloqueo hasta Fase 5; (c) eliminar la política. [Rec. Claude] (a) manteniendo el bloqueo de DEMO en producción.
- **P11 Navegadores:** (a) Chromium; (b) + Firefox; (c) + Safari/WebKit. [Rec. Claude] (a) completo, (b) con pruebas, (c) esfuerzo documentado. Solo Chrome está verificado.
- **P12 Multi-pestaña:** (a) Web Locks; (b) aviso + solo lectura; (c) `revision` optimista. [Rec. Claude] (b) con (c) de respaldo. Depende de P11; condiciona E2.
- **P13 Dependencias y `AppErrorCode`:** (a) cero nuevas; (b) conjunto mínimo aprobado una por una; (c) libre. [Rec. Claude] (b). `npm audit` no se ha ejecutado.
- **P14 PoC IndexedDB:** (a) no; (b) PoC aislado fuera del repositorio. [Rec. Claude] (a); el expediente la considera resuelta de hecho, requiere confirmación.
**Conjunta:** sí, en una sola respuesta por bloque (P5+P11+P12+P13 están relacionadas). **Registro:** registro autoritativo.

## PAQ-7 — Decisiones posteriores (antes de su fase; no bloquean la preparación del cierre)
- **P6 Formato de exportación** (antes de Fase 2): (a) JSON; (b) ZIP con JSON + binarios; (c) con cifrado opcional. [Rec. Claude] (a) para texto; (b) si P5=(a).
- **P7 Cifrado local** (antes de Fase 5): (a) no; (b) solo exportaciones; (c) datos y exportaciones. [Rec. Claude] (a) para el MVP.
- **P8 IA y claves** (antes de Fase 2): IA-A+IA-B; +IA-C; +IA-D; IA-E (contradice el alcance vigente). [Rec. Claude] IA-A+IA-B.
- **P10 Hosting/origen** (antes de Fase 5): (a) `localhost`; (b) hosting estático en origen dedicado; (c) otro. [Rec. Claude] (a) en Fases 1–4; (b) en Fase 5.
- **P15 Pendientes previos** (licencia, historial, F11-D4/F5/G-1/F6, Fase 0 anterior): [Rec. Claude] declarar históricos los de servidor; licencia antes de publicar; no reescribir historia salvo decisión expresa.

---
## Lo que NO se solicita todavía
Aprobaciones 0.1–0.7, aceptación formal de Fase 0 y autorización de Fase 1. Cada una será una decisión distinta, con su propia ficha, cuando el propietario considere resueltos los paquetes anteriores. No son una formalidad automática.
