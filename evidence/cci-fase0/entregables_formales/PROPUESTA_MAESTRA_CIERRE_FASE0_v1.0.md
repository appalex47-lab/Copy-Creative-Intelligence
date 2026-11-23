CCI — Documento maestro propuesto para completar y cerrar Fase 0

Versión: 1.0 — Propuesta de resolución para revisión del propietario
Base documental: rama "evidence/cci-fase0-review", expediente publicado hasta "e049fcda41aad7e8b47f61b60c313c69164210cc".
Estado: PROPUESTA. No constituye aprobación ni modifica el registro oficial de decisiones.

---

1. Objetivo

Completar las decisiones indispensables de Fase 0, cerrar las ambigüedades del dominio browser-only y dejar preparados:

- El modelo conceptual de CCI.
- Las decisiones técnicas de la arquitectura local.
- El alcance del MVP.
- Las convenciones de datos.
- El roadmap y sus criterios de aceptación.
- Las aprobaciones formales 0.1–0.7.

La propuesta respeta las decisiones ya emitidas:

- Aplicación local, un usuario por navegador.
- Sin cuentas, autenticación, backend, Supabase, PostgreSQL, SQL ni sincronización multidispositivo.
- IndexedDB como persistencia principal.
- Local Storage exclusivamente para preferencias ligeras.
- Exportación e importación local como mecanismos de respaldo y recuperación.
- Separación entre contenido, variantes, versiones y decisiones humanas de aprobación.
- La IA no sustituye reglas deterministas, cálculos ni aprobación humana.
- No se incorpora automáticamente ningún elemento de los expedientes históricos.

2. Decisiones anteriores que permanecen cerradas

No se vuelven a solicitar:

Decisión| Estado que se conserva
P1| Perfil local opcional; sin identidad autenticada, organizaciones, membresías ni roles operativos.
P2| ADR de sustitución de los diseños incompatibles con browser-only; históricos conservados.
P3| "docs/fase0/" y expedientes anteriores como antecedentes no vinculantes.
P4.1| Lista de referencia de 18 entidades. Solo nombres aprobados inicialmente.
P4.2| "ReglaDeMarca" y "ReglaComercial" son entidades separadas.
P4.3| Evento de actividad, Etiqueta y Perfil local aprobados en el alcance definido; Colección excluida mientras no se justifique.
Q-7| Campaña es una entidad propia, distinta de Project.
D1–D3| Decisiones conceptuales sobre contenido, adaptación, variantes y familias de reglas.
D4.a–d| Todas aprobadas; Adaptación conserva las limitaciones de M-1 y D5.3.
D5.a–d| Fuera del alcance vigente. No reabrir.
D6.a–b| Aprobadas.
D6.c| A0: Metric es definición de métrica; los valores pertenecen a Resultado de desempeño.
D7.a–c| Aprobadas; Q-1 y Q-2 siguen pendientes.
D8| Nombre canónico: Resultado de desempeño.

La aprobación de una definición mínima no implica aprobación de sus atributos, cardinalidades, mecanismos ni implementación.

---

PARTE I — MODELO DE DOMINIO

3. P4.A — Entidades todavía sin definición mínima

Se propone aprobar únicamente existencia y definición mínima para las nueve entidades restantes. No se aprueban estructuras de datos, atributos ni mecanismos.

PE-09 — Hallazgo de auditoría

Propuesta de definición:

Hallazgo de auditoría es una entidad propia de CCI que representa un problema u observación identificado durante una auditoría creativa y que puede explicarse, consultarse y seguirse hasta su resolución.

Límites:

- No constituye una auditoría independiente.
- No tiene necesariamente una puntuación propia.
- No se aprueban niveles de severidad, categorías ni estados.
- No se presupone que cada hallazgo tenga una regla identificada.
- No se convierte en una entidad de aprobación.

Recomendación: aprobar la definición mínima. Mantener clara su diferencia frente a Auditoría creativa: la auditoría es la evaluación; el hallazgo es una observación identificada en ella.

PE-10 — ReglaDeMarca

Propuesta de definición:

ReglaDeMarca es una entidad propia de CCI que representa un criterio de marca aplicable al contenido creativo y que puede utilizarse como referencia durante su evaluación.

Límites:

- No se inventa un catálogo de reglas.
- No se incorporan automáticamente reglas de copy.
- No se definen pesos, prioridades, severidades ni mecanismos.
- Su contenido concreto deberá justificarse con información de marca aportada por el propietario.

Recomendación: aprobar la existencia y definición mínima; aplazar el catálogo de reglas.

PE-11 — ReglaComercial

Propuesta de definición:

ReglaComercial es una entidad propia de CCI que representa un criterio comercial utilizado para evaluar información de ofertas y promociones.

Límites:

- Sus tolerancias son parámetros de la propia regla, conforme a D7.b.
- No se aprueban fórmulas ni valores de tolerancia.
- No se aprueba redondeo ni tratamiento de excepciones.
- Q-1 se resuelve antes de implementar Promotion Validator.

Recomendación: aprobar la definición mínima.

PE-12 — Canal

Propuesta de definición:

Canal es una entidad propia de CCI que representa un medio o formato de comunicación para el que puede prepararse contenido y respecto del cual pueden considerarse reglas específicas de adaptación.

Límites:

- Se conserva la lista inicial aprobada por D7.c.
- Las reglas por canal son una dimensión del Canal, no entidades independientes.
- No se aprueba un catálogo editable ni un mecanismo automático de ampliación.
- Los canales adicionales requieren decisión expresa del propietario.

Recomendación: aprobar la definición mínima.

PE-14 — Versión de contenido

Propuesta de definición:

Versión de contenido es una entidad propia de CCI que representa un estado fechado y trazable de un contenido a lo largo de su evolución o revisión.

Límites:

- Es distinta de Variante de copy.
- Copy, Pieza creativa y Adaptación pueden tener versiones, conforme a D1.d.
- Las variantes no tienen versiones propias por ahora, conforme a D2.b.
- No se aprueban todavía mecanismos de comparación, almacenamiento ni historial.

Recomendación: aprobar la definición mínima y conservar la distinción conceptual entre variante y versión.

PE-15 — Aprobación

Propuesta de definición:

Aprobación es una entidad propia de CCI que representa una decisión humana respecto de la conformidad de un contenido específico, en las condiciones en que fue revisado, para permitir su paso a Creative Library.

Límites:

- La aprobación es humana, nunca automática por IA.
- El usuario es único y local; no hay aprobadores simulados.
- No constituye certificación legal, comercial ni de marca.
- No implica publicación o distribución externa.
- No se confunde con los estados del contenido.
- La identificación técnica exacta de la versión aprobada deberá definirse en el diseño del módulo.

Recomendación: aprobar la definición mínima.

PE-16 — Resultado de desempeño

Propuesta de definición:

Resultado de desempeño es una entidad propia de CCI que representa información de desempeño proporcionada o registrada por el usuario respecto de una campaña, contenido u otra referencia pertinente.

Límites:

- Se conserva el nombre aprobado por D8.
- Los valores de las métricas pertenecen al Resultado.
- No se aprueban fórmulas, indicadores, atributos ni métodos de importación.
- A0-1, A0-2 y A0-3 se resuelven por separado.

Recomendación: aprobar la definición mínima.

PE-17 — Métrica

Propuesta de definición:

Métrica es una entidad propia de CCI que representa la definición conceptual de un indicador utilizado para describir o evaluar desempeño.

Límites:

- No almacena los valores de desempeño.
- No se aprueba un catálogo de métricas.
- No se aprueban fórmulas ni fuentes de datos.
- La relación de referencia con Resultado queda sujeta a A0-3.

Recomendación: aprobar la definición mínima.

PE-18 — Configuración de la aplicación

Propuesta de definición:

Configuración de la aplicación es una entidad propia de CCI que representa preferencias y parámetros duraderos que determinan el comportamiento o la presentación de la aplicación.

Límites:

- Es distinta de Perfil local.
- No representa identidad ni autorización.
- No se aprueban todavía atributos ni ubicación definitiva de almacenamiento.
- Local Storage se reserva para preferencias ligeras; la información necesaria para respaldos deberá persistir en IndexedDB.

Recomendación: aprobar la definición mínima.

---

4. P4.B — Relaciones y cardinalidades

Propuesta de resolución: aprobar únicamente relaciones justificadas por el significado aprobado y por las instrucciones originales. No inventar cardinalidades obligatorias.

Relaciones con fundamento documental

1. Campaña puede ser referenciada por Brief.
2. Campaña puede ser referenciada por Resultado de desempeño.

La palabra «puede» no significa que la relación sea obligatoria.

Relaciones propuestas para ratificación

Relación| Propuesta| Motivo
Copy – Variante de copy| Una alternativa textual se deriva conceptualmente de un Copy de referencia.| Distinguir el contenido original de sus alternativas.
Copy – Versión de contenido| Un Copy puede evolucionar mediante versiones.| Trazabilidad temporal.
Pieza creativa – Versión| Una pieza puede conservar versiones.| D1.d.
Adaptación – Versión| Una adaptación puede conservar versiones.| D1.d.
Auditoría creativa – Copy| La auditoría evalúa Copy.| D1.c.
Auditoría creativa – Pieza| La auditoría evalúa Pieza creativa.| D1.c.
Auditoría creativa – Hallazgo| Una auditoría puede producir hallazgos.| Separación evaluación/observación.
Aprobación – contenido revisado| La aprobación debe identificar el contenido al que se refiere.| Trazabilidad de M-1.
Resultado – Métrica| Un resultado contiene valores correspondientes a métricas.| D6.c=A0.
Adaptación – Canal| La adaptación tiene un canal de destino.| D4.a=A.
Adaptación – Pieza| Puede existir un vínculo, pero no se presupone.| D4.b=A.

Relaciones que no deben darse por aprobadas

- Campaña–Oferta.
- Campaña–Pieza.
- Brief–Oferta.
- Brief–Producto.
- Reglas de copy–ReglaDeMarca.
- Reglas por canal como entidades independientes.
- Evento de actividad con cualquier entidad específica, salvo que la especificación del módulo lo justifique.

Recomendación: aprobar las relaciones propuestas individualmente, sin establecer cardinalidades obligatorias en esta fase. Las cardinalidades se especificarán con los flujos de cada módulo.

---

5. P4.C — Atributos

Propuesta de resolución:

Diferir la definición completa de atributos hasta la especificación de cada módulo.

Antes de implementar una entidad solo podrán aprobarse los atributos indispensables para el alcance autorizado de esa fase, siempre acompañados de:

1. Necesidad funcional.
2. Fuente o justificación.
3. Tipo y formato.
4. Obligatoriedad.
5. Validación.
6. Comportamiento ante ausencia o valor desconocido.

No se aprueba un esquema completo de 18 entidades en Fase 0.

Recomendación: cerrar P4.C mediante esta regla de gobierno del modelo, no mediante la invención anticipada de atributos.

---

6. P4.E — Convenciones transversales

Se propone convertir las siguientes convenciones preliminares en decisiones definitivas:

E1 — Fechas y zonas horarias

- Instantes técnicos: ISO-8601 UTC con "Z".
- Fechas comerciales sin hora: "YYYY-MM-DD".
- Cuando una operación dependa de hora local, conservar hora y zona IANA correspondiente.
- No convertir fechas comerciales en instantes UTC si eso cambia su significado.

E2 — Campo "revision"

- No será obligatorio en todas las entidades.
- Se incorporará solo cuando un caso de uso demuestre necesidad de control de concurrencia o detección de conflictos.
- La política multi-pestaña se resuelve en P12.

E3 — Archivar y eliminar

- Archivar y eliminar son operaciones diferentes.
- Archivar es reversible y conserva historial y referencias.
- Eliminar físicamente requiere confirmación explícita.
- No se permitirá eliminar silenciosamente información referenciada por versiones, auditorías o aprobaciones.
- Cuando exista historial dependiente, la opción predeterminada será archivar.

E4 — Valores desconocidos

- "null": valor conocido como desconocido o no disponible.
- Campo ausente: propiedad opcional que no fue proporcionada.
- "0": valor numérico real igual a cero.
- No aplicable: representación explícita y diferenciada.
- Ningún cálculo interpretará "null" como cero.

E5 — Hash de versiones

- Versiones inmutables como principio de trazabilidad.
- SHA-256 sobre contenido canónico cuando corresponda.
- El hash permite detectar modificaciones o corrupción.
- No garantiza autoría ni seguridad frente a alguien con acceso local capaz de modificar los datos y recalcular el hash.

Recomendación: aprobar E1, E2, E3, E4 y E5 con estas delimitaciones.

---

7. D6.c=A0 — Subdecisiones pendientes

Se propone:

- A0-1: no exigir clasificación del origen (manual/importado/calculado) en el modelo inicial. Añadirla cuando una funcionalidad concreta necesite distinguirlo.
- A0-2: diferir la elección entre L1 y L2 hasta que existan fórmulas y casos de uso reales. No conservar valores calculados sin una decisión de trazabilidad.
- A0-3: aprobar que Resultado de desempeño pueda referenciar la definición de Métrica cuando sea necesario identificar el origen de un valor calculado.

A0-3 es independiente de L1/L2.

Recomendación: A0-1=(b), A0-2=diferir, A0-3=sí. Evita sobrediseñar el módulo de desempeño antes de tener datos y fórmulas aprobadas.

---

PARTE II — DECISIONES TÉCNICAS INDISPENSABLES

8. P5 — Archivos binarios en IndexedDB

Propuesta: (a), almacenar binarios en IndexedDB.

- Usar "Blob" o equivalente, no Base64 dentro de registros de texto.
- Separar metadatos y contenido binario.
- Validar tipo, tamaño y contenido real del archivo.
- Consultar cuota disponible cuando el navegador lo permita.
- Mostrar advertencias de almacenamiento y permitir exportación.
- No prometer recuperación automática si el navegador elimina datos.
- Definir límites de producto después de pruebas reales de navegador, no inventar una cuota universal.

La decisión permite preparar el almacenamiento de piezas creativas sin convertir Fase 1 en un módulo de auditoría visual.

9. P9 — Modo de producción local

Propuesta: (a).

- Introducir un modo operativo "local".
- Mantener DEMO exclusivamente para pruebas o demostraciones explícitamente identificadas.
- El build de producción debe utilizar persistencia local real.
- Un build de producción nunca debe mostrar datos DEMO como si fueran datos del usuario.
- Mantener guardas que impidan configurar accidentalmente un modo DEMO como producción.

10. P11 — Navegadores soportados

Propuesta:

- Chrome/Chromium estable: navegador primario y matriz E2E completa.
- Edge estable: compatibilidad esperada por compartir motor Chromium, con validación específica antes de declararlo plenamente soportado.
- Firefox: compatibilidad secundaria, sujeta a pruebas.
- Safari/WebKit: mejor esfuerzo hasta contar con pruebas suficientes.

No se declarará soporte completo de un navegador sin pruebas reales. La matriz deberá documentar versión, sistema operativo y resultados.

11. P12 — Política multi-pestaña

Propuesta: (b), una pestaña de escritura y las demás en solo lectura.

- Una pestaña activa conserva el permiso de escritura.
- Las demás detectan que existe una sesión de edición y operan en solo lectura.
- Mostrar aviso visible y permitir recuperar el permiso cuando la pestaña activa se cierre o libere el bloqueo.
- Utilizar un mecanismo de coordinación del navegador; evaluar Web Locks y un canal de comunicación entre pestañas.
- Si no puede demostrarse quién tiene el bloqueo, fallar de forma conservadora y no permitir escrituras concurrentes.

No se implementará concurrencia optimista generalizada ni se exigirá "revision" en todos los registros.

12. P13 — Dependencias y errores

Propuesta: (b), dependencias mínimas y justificadas una por una.

Reglas:

- Preferir APIs nativas del navegador cuando sean suficientes.
- No instalar una dependencia de ejecución sin justificar su necesidad, mantenimiento, licencia y riesgo.
- Las dependencias de desarrollo y pruebas se evalúan por separado.
- Cualquier dependencia nueva debe fijar versión y contar con pruebas.
- Mantener las guardas contra Supabase y servicios de backend.
- Ampliar "AppErrorCode" solo con errores reales que requieran tratamiento específico.

Propuesta inicial:

- IndexedDB nativo, salvo que una evaluación técnica demuestre que un wrapper aporta una ventaja necesaria.
- Validaciones explícitas en los límites de entrada.
- Dependencias de pruebas permitidas cuando sean necesarias y autorizadas.
- ZIP solo cuando se decida el formato de exportación en P6.

No autoriza instalar paquetes durante Fase 0.

13. P14 — Prueba de concepto en Fase 0

Propuesta: (a), no realizar PoC ejecutable.

Fase 0 permanece documental. IndexedDB se implementará y probará en Fase 1, con evidencia real de navegador.

---

PARTE III — ALCANCE DEL MVP Y PENDIENTES POR FASE

14. Q-4 — Definición del MVP

Propuesta: (a), el MVP termina al concluir Fase 2.

El MVP comprende:

Fase 1 — Fundamentos y Command Center

- Arquitectura local.
- Persistencia real.
- Navegación y sistema visual.
- Perfil local opcional.
- Preferencias.
- Actividad real.
- Estado del almacenamiento.
- Command Center con información real y estados vacíos honestos.
- Exportación/importación básica de respaldo si se aprueba dentro del alcance de persistencia.

Fase 2 — Copy Studio

- Campañas.
- Brief.
- Copy.
- Variantes.
- Editor.
- Etiquetas y búsqueda.
- Reglas deterministas iniciales.
- Flujo de creación y conservación de contenido.

No se considera parte del MVP:

- Auditoría creativa avanzada.
- Promotion Validator completo.
- Auditoría visual avanzada.
- Workflow & Approvals completo.
- Performance Intelligence avanzado.
- Integraciones de backend.
- Colaboración multiusuario.

La aceptación del MVP no significa que el producto completo esté terminado.

15. Decisiones que pueden aplazarse sin bloquear Fase 0

Se propone diferir las siguientes decisiones hasta antes de la fase que las necesita:

Decisión| Momento de resolver
P6 — Formato final de exportación| Antes de cerrar Fase 2.
P7 — Cifrado local| Antes de Fase 5; no prometer cifrado mientras no se implemente.
P8 — Estrategia de IA| Antes de generación en Fase 2.
P10 — Hosting y origen| Antes de publicación del producto.
P15 — Licencia y pendientes históricos de publicación| Antes de publicación externa.
Q-1 — Redondeo y tolerancias comerciales| Antes de Fase 4.
Q-2 — Reglas y límites por canal| Antes de Fase 4.
Q-3 — Estados y transiciones de Workflow & Approvals| Antes de Fase 5.
Q-5 — Criterios y ponderaciones de auditoría| Antes de Fase 3.
Q-6 — Idioma y diccionario ortográfico| Antes de Fase 2.

Recomendaciones iniciales para esos pendientes

- P6: JSON como formato inicial; ZIP solo si los binarios lo hacen necesario.
- P8: IA-A + IA-B para empezar: funciones deterministas locales y flujo manual de prompts con proveedor externo. Sin claves en la aplicación.
- Q-1: redondeo decimal explícito y configurable; los valores de tolerancia deben provenir de reglas comerciales reales.
- Q-2: conservar la lista de canales ya aprobada; no inventar límites de longitud ni estructuras.
- Q-3: mantener estados del contenido separados de la entidad Aprobación.
- Q-5: no inventar ponderaciones; deben definirse con criterios de negocio y marca.
- Q-6: español como idioma inicial, si se confirma, con diccionario identificable y mantenible.

---

PARTE IV — CONTRADICCIONES HISTÓRICAS

16. C-2 y C-3

No propongo resolverlas unilateralmente.

C-2 — Fase 0 v3.3 anterior

Mantener abierta la contradicción histórica. No declarar aceptada esa versión como línea base vigente sin evidencia primaria.

Propuesta de tratamiento para el cierre actual: reconocer que los documentos de la versión anterior existen, conservarlos íntegros y declarar que no sustituyen la arquitectura browser-only ni la aceptación de esta Fase 0.

C-3 — D-04 y los roles

Mantener abierta la contradicción sobre la aprobación histórica de las claves concretas de roles.

La decisión P1 vigente descarta los roles operativos y de autorización en el dominio browser-only. No se debe inferir que D-04 aprobó las claves técnicas de roles.

Propuesta de tratamiento: conservar el antecedente y dejar constancia de que no tiene efecto operativo en la arquitectura actual.

Estas dos contradicciones solo podrán cerrarse mediante decisión expresa o evidencia primaria. Su permanencia debe figurar como limitación aceptada si decides cerrar Fase 0 sin resolverlas.

---

PARTE V — APROBACIONES FORMALES

17. Propuesta de contenido de las aprobaciones 0.1–0.7

Aprobación| Propuesta de resolución| Condición
0.1 Diagnóstico| Aprobar el inventario y el diagnóstico del estado real.| Confirmar que la fundación existe, pero no equivale al producto terminado.
0.2 Arquitectura| Aprobar browser-only, capas y persistencia local.| P9, P11, P12 y P13 resueltas.
0.3 Dominio| Aprobar el modelo conceptual y sus límites.| P4.A, P4.B, P4.C y P4.E resueltas en el alcance aquí propuesto.
0.4 Persistencia| Aprobar IndexedDB, preferencias, archivos y recuperación local.| P5 y las convenciones de persistencia definidas. P6 puede diferirse hasta Fase 2.
0.5 IA| Aprobar una estrategia inicial sin claves privadas en la aplicación.| P8 puede aprobar IA-A + IA-B, sin autorizar proveedor ni integración automática.
0.6 MVP| Aprobar el MVP hasta el final de Fase 2.| Q-4 resuelta.
0.7 Roadmap| Aprobar la secuencia de Fases 1–5 y sus puertas de aceptación.| Los pendientes específicos se resuelven antes de su fase.

Ninguna aprobación formal se considera emitida por este documento.

---

PARTE VI — CRITERIOS DE CIERRE

18. Qué significa que Fase 0 esté lista para aceptación

Fase 0 estará lista para que el propietario decida su aceptación cuando:

1. Las decisiones indispensables P4, P5, P9, P11, P12, P13, P14 y Q-4 estén resueltas.
2. Las entidades del alcance conceptual estén definidas o expresamente aplazadas/excluidas.
3. P4.B, P4.C y P4.E tengan una resolución explícita.
4. Las subcuestiones A0 tengan resolución o aplazamiento justificado.
5. C-2 y C-3 estén expresamente reconocidas como limitaciones abiertas.
6. El roadmap tenga alcance, dependencias y criterios de aceptación claros.
7. Las aprobaciones 0.1–0.7 se hayan revisado y emitido.
8. La reserva técnica X4 esté corregida y documentada.
9. El expediente final refleje las decisiones reales, sin contradicciones conocidas no declaradas.

La aceptación de Fase 0 no autoriza por sí misma la implementación de Fase 1.

19. Condiciones para iniciar Fase 1

Una vez aceptada Fase 0, deberá emitirse una autorización independiente para iniciar Fase 1.

La autorización deberá especificar:

- Subfases autorizadas.
- Repositorio y rama permitidos.
- Archivos o áreas que pueden modificarse.
- Pruebas exigidas.
- Prohibiciones de commit, merge, push o deploy que sigan vigentes.
- Criterios de aceptación y evidencia.

20. Estado de avance: base verificable

Dimensión| Estado actual
Regularización documental| Sustancialmente completada, con reserva X4
Decisiones conceptuales| 12/30 según indicador orientativo del expediente
Entidades con definición mínima aprobada| 9/18
Aprobaciones formales| 0/7
Aceptación de Fase 0| Pendiente
Autorización de Fase 1| Pendiente

No se calcula un porcentaje global de Fase 0.

---

PARTE VII — RATIFICACIÓN DEL PROPIETARIO

Las propuestas de este documento deben registrarse como decisiones solo después de tu confirmación expresa.

Para agilizar la revisión, propongo que puedas responder por bloques:

- B1 — Entidades: aceptar las definiciones mínimas PE-09 a PE-18, con cambios o mantener alguna pendiente.
- B2 — Relaciones: aceptar, modificar o aplazar cada relación propuesta en P4.B.
- B3 — Atributos: diferir el esquema completo a cada módulo, como se propone en P4.C.
- B4 — Convenciones: ratificar E1–E5.
- B5 — Métricas: ratificar A0-1=(b), A0-2=diferir, A0-3=sí.
- B6 — Arquitectura técnica: ratificar P5, P9, P11, P12, P13 y P14.
- B7 — MVP: ratificar Q-4=(a), final de Fase 2.
- B8 — Pendientes posteriores: aceptar el aplazamiento de P6–P8, P10, P15 y Q-1–Q-3, Q-5–Q-6 hasta sus fases.
- B9 — Contradicciones: mantener C-2 y C-3 abiertas como limitaciones expresas.
- B10 — Aprobaciones: revisar 0.1–0.7 una vez incorporadas las decisiones ratificadas.

Regla final: ninguna propuesta de este documento modifica automáticamente "REGISTRO_DECISIONES_RESUELTAS.md", "APROBACIONES_FASE0.md" ni el repositorio. Primero debe existir ratificación expresa del propietario; después se actualiza la documentación y se verifica su consistencia.

Resultado esperado: un expediente de Fase 0 completo, coherente, con decisiones trazables y listo para aceptación formal, sin iniciar Fase 1 por inferencia.

> **Nota fechada 2026-11-22 20:14 (respuesta del propietario; no es decisión nueva de este documento):** el propietario emitió las aprobaciones 0.1–0.7 (7/7; la 0.5 solo en cuanto a principios, con P8 sin resolver y sin ninguna integración aprobada) y respondió «sí» a R-1 (aplazamiento aceptado de las seis cuestiones residuales, no resolución). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «0/7», «PENDIENTES» o «R-1 pendiente» describen el estado previo y quedan superadas en ese punto; el resto del texto no se altera. **La aceptación formal de Fase 0 y la autorización independiente de Fase 1 siguen PENDIENTES.** Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.

> **Nota fechada 2026-11-22 20:26 (respuesta del propietario; no es decisión nueva de este documento):** el propietario aceptó formalmente la Fase 0 («Acepto formalmente la Fase 0, con las limitaciones expresas C-2 y C-3 abiertas y los 10 aplazamientos pendientes. No autoriza la Fase 1.»; redacción propuesta por Claude y adoptada literalmente). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «Fase 0 no aceptada» o a la aceptación formal como pendiente describen el estado previo y quedan superadas en ese punto. **C-2, C-3 y los 10 aplazamientos siguen abiertos y la autorización de la Fase 1 sigue PENDIENTE** (acto independiente). Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.
