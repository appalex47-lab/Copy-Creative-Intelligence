# D-1 — ¿Qué objetos son «contenido» en CCI? (análisis y recomendación) — 2026-11-22
**Naturaleza:** análisis y propuesta; **no aprueba nada**. No resuelve D-2 ni D-3. No cambia las definiciones de las entidades 1–8. Hallazgo de auditoría (9) sigue sin decisión. Referencias: A = Fase 0 (`de49cc27`), B = instrucción maestra (`5a9f5585`).

## 1. Evidencia textual original (E)
- **E1** Ciclo de vida de la comunicación comercial: «Brief → Copy → Adaptación creativa → Auditoría → Validación promocional → Corrección → Aprobación humana → Biblioteca → Medición» (B l.17–19; A l.44).
- **E2** Flujo de integración: «Brief → Copy Studio → Creative Auditor → Promotion Validator → Channel Adaptation → Revisión humana → Biblioteca → Performance Intelligence» (B l.673). **Orden y nombres distintos de E1.**
- **E3** Fase 2: «creación y administración de contenido comercial» (B l.341); alcance: campañas, brief, generación de copy, variantes (A l.575–578); resultado: crear campañas, completar briefs, «generar o escribir copys» y administrar variantes (B l.414).
- **E4** Fase 4: «adaptar contenidos a canales» (B l.502); canales: Ecommerce, App, WhatsApp, Email, Redes sociales, Banners, Landing pages y otros formatos aprobados (B l.538–547); reglas por canal: longitud, estructura, formato, tono, CTA, restricciones, elementos obligatorios (B l.549–557); trazabilidad: copy fuente, canal, adaptación, versión, reglas, diferencias, estado de revisión (B l.559–566); pruebas: adaptaciones, trazabilidad, persistencia (B l.579–581); A l.603 «Adaptación por canal».
- **E5** Fase 3: «Auditar copys y piezas visuales» (B l.422); auditoría de copy (B l.426), visual (B l.439) y «Congruencia copy-pieza» (B l.447). Promotion Validator: «Coherencia entre oferta y copy» (B l.517).
- **E6** Creative Library: Campañas, Copys, Piezas, Búsqueda, Filtros, Etiquetas, Versiones, Auditorías, Reutilización (B l.596–605). **No lista Adaptaciones ni Variantes.**
- **E7** Versiones: «Las versiones deben conservar trazabilidad» (B l.68); sección Versionado (B l.623–633), que cierra con «No sobrescribir silenciosamente contenido aprobado» (B l.633); editor de copy: «Consultar historial» (B l.383); «Comparar versiones», «Conservar historial» (B l.476–477).
- **E8** Aprobación: «La aprobación final es humana» (B l.65); «Ninguna promoción debe aprobarse automáticamente por una sugerencia de IA» (B l.64); siete estados del flujo (B l.609–617); sin multiusuario (B l.621). Estos estados no dicen a qué objeto se aplican.
- **E9** «Contenido» como campo del registro de resultados (B l.641), sin decir a qué objeto apunta. A l.514: la IA ayuda en «Análisis de contenido».
- **E10** Editor de Copy Studio (crear, editar, duplicar, comparar, guardar, recuperar, etiquetar, buscar, exportar, historial: B l.374–383) y generación de titulares, textos principales, descripciones y CTA (B l.363–366): describen la edición de **copys**.

## 2. Decisiones tuyas ya aprobadas y aplicables
- **Copy:** «contenido textual creado o escrito por el usuario», objeto de edición, auditoría, validación y adaptación a canales.
- **Variante de copy:** «alternativa de contenido textual» (deja abierta su delimitación frente a ContentVersion).
- **Pieza creativa:** «recurso visual» objeto de auditoría visual y conservable en Library.
- **Auditoría creativa:** evaluación «sobre un copy o una pieza creativa»; abierto si el objeto se referencia directo o por versión; abierto si la reauditoría crea o modifica registro.
- **Brief:** reúne información para «creación de contenido (copy)». **Oferta:** asociada «al contenido que se crea o revisa». **Campaña:** criterio de catalogación en Library.
- No aprobaste relaciones, cardinalidades, atributos ni fases.
- Efecto práctico: tus propias definiciones ya usan «contenido» para el texto («contenido textual», «contenido (copy)») y «recurso visual» para la pieza.

## 3. Derivaciones razonables (D, con su base)
- **D-a** «Contenido comercial» en Fase 2 es el material que se crea en Copy Studio, es decir, copys y sus variantes (E3, E10).
- **D-b** El ciclo trabaja con dos modalidades: textual (Copy, Variante) y visual (Pieza) (E5, tus definiciones).
- **D-c** La adaptación es un objeto con trazabilidad propia (copy fuente, canal, versión, reglas, diferencias, estado de revisión) y se persiste (E4). Está separada del «copy fuente» en esa lista, y tu definición de Copy la presenta como algo que se hace **sobre** un copy.
- **D-d** Auditable de forma explícita: copy y pieza visual (E5). Validable por reglas comerciales: la coherencia oferta–copy y los elementos promocionales (B l.508–517).
- **D-e** Versionable: la adaptación (lleva «Versión» en su trazabilidad, E4); copy y pieza (aparecen junto a «Versiones» en la Library, E6; historial de copy, E7). Evidencia más débil para pieza.
- **D-f** Aprobable: hay «contenido aprobado» (B l.633) y «promoción» (B l.64); el objeto exacto no está dicho.

## 4. Propuestas mías (P, **no aprobadas**)
- **P-1** Usar «contenido» como **concepto paraguas no persistido**, no como entidad.
- **P-2** Tratar Adaptación de canal como concepto propio derivado de un Copy fuente, ni Copy ni Pieza.
- **P-3** Matriz de capacidades de la sección 6.
- **P-4** Diferenciar Copy y Pieza por **modalidad** (texto frente a recurso visual) y por tipo de auditoría, no por ciclo de vida.

## 5. Copy frente a Pieza creativa
- **Respaldo textual:** Copy = titulares, textos principales, descripciones y CTA (B l.363–366) con criterios de claridad, ortografía, tono, CTA, afirmaciones (B l.428–437). Pieza = recurso visual con criterios de legibilidad, contraste, jerarquía, distribución, consistencia de marca, elementos obligatorios y formato (B l.441–448). La relación entre ambos es una **congruencia** (B l.447).
- **Lo que no dicen las instrucciones:** si el texto dentro de una pieza es un Copy, o si una pieza contiene o referencia un Copy. No lo resuelvo; no hay relación aprobada.

## 6. Capacidades por objeto (evidencia, no decisión)
| Objeto | Auditar | Versionar | Aprobar |
|---|---|---|---|
| Copy | **Explícito** (B l.422) y en tu definición | Derivado (E6, E7) | Derivado (B l.633) |
| Pieza creativa | **Explícito** (B l.422) y en tu definición | Derivado, más débil (E6) | Derivado, ambiguo |
| Adaptación de canal | **Sin cita** (solo «estado de revisión» y reglas por canal) | **Explícito** (B l.565) | Derivado (flujo «Revisión humana» tras Channel Adaptation, B l.673) |
| Variante de copy | Sin cita | Sin cita | Sin cita (**depende de D-2**) |
| Brief, Campaña, Oferta, Producto | Sin cita | Sin cita | «Promoción» aprobable (B l.64): objeto no definido; no equivale a Oferta por tu decisión |

## 7. Relación conceptual entre contenido, variante, versión y auditoría (sin resolver D-2)
- **Variante:** según tu definición es una alternativa de contenido **textual**; no se decide aquí cómo se relaciona con el Copy ni con la versión.
- **Versión:** estado fechado y trazable de un contenido (E7); su frontera con la variante es D-2.
- **Auditoría:** evalúa copy y pieza (E5); si apunta al objeto o a su versión sigue abierto (tu alcance en la entidad 8).
- **Propuesta mía:** contenido es el objeto sobre el que operan versión, auditoría y aprobación; la variante queda **fuera** de esta tabla hasta D-2.

## 8. Ambigüedades del texto original (requieren tu decisión)
- **A-1** «Adaptación creativa» (E1) frente a «Channel Adaptation» (E2, A l.603 «Adaptación por canal»): ¿mismo concepto? Además cambia el orden: antes de la auditoría (E1) o después del validador (E2). No hay módulo llamado «Adaptación creativa» en la lista de módulos (B l.19–30).
- **A-2** ¿Las adaptaciones a Banners y Landing pages son textuales, visuales o ambas?
- **A-3** ¿Se audita una adaptación? Fase 3 solo nombra copy y pieza.
- **A-4** Objeto de «Aprobación» y de «Contenido» en Resultados (B l.641).
- **A-5** Si la Pieza contiene o referencia Copy.

## 9. Alternativas, consecuencias y recomendación

### D-1.a ¿Qué es «contenido»?
- **(A) Concepto paraguas, no persistido** (**recomendada**): el material de comunicación que CCI crea, adapta, audita, aprueba y mide; hoy lo componen Copy, Pieza creativa y Adaptación de canal. Sin tabla «Contenido». Consecuencia: permite redactar D-2 a D-5 sin comprometer una estructura. No añade entidades.
- **(B) Entidad supertipo (`ContentItem`):** Copy, Pieza y Adaptación serían subtipos. Resuelve el polimorfismo, pero añade una entidad 19 no pedida y exigiría una **revisión explícita de P4.1**. No recomendada.
- **(C) Contenido = solo texto** (Copy y Variante): encaja con tus definiciones de Brief y Oferta, pero deja sin término genérico «contenido aprobado» (B l.633) ni «Contenido» en Resultados (B l.641).

### D-1.b ¿Qué es una adaptación a banner, landing u otro canal?
- **(i) Un Copy derivado:** simple, pero mezcla texto con formatos visuales y confunde «copy fuente» con «adaptación» (B l.563–565).
- **(ii) Concepto propio, «Adaptación de canal»** (**recomendada**): referencia un copy fuente y un canal, conserva diferencias y estado de revisión; ni Copy ni Pieza. Consecuencias: coincide con la lista A y con la trazabilidad de B. Queda abierto si, en canales visuales, se vincula a una Pieza (A-2).
- **(iii) Pieza o Copy según el canal:** la naturaleza depende de un dato del canal. Complica la regla y no tiene respaldo textual.

### D-1.c ¿Se audita la adaptación?
- **(a) No; se auditan Copy y Pieza, y la adaptación se rige por reglas de canal** (**recomendada**): sigue B l.422 literalmente y es compatible con tu definición de la entidad 8.
- **(b) Sí:** ampliaría el alcance de la entidad 8 («sobre un copy o una pieza creativa»); exigiría tu autorización expresa para modificarlo.

### D-1.d Capacidades de versión y aprobación
- **(a)** Reconocer como versionables y aprobables Copy, Pieza y Adaptación (**recomendada**), como **capacidades contempladas**, sin atributos ni reglas. Variante: excluida hasta D-2. Brief, Campaña, Oferta, Producto: sin evidencia; no se decide.
- **(b)** Reconocer solo la Adaptación y el Copy, y dejar la Pieza pendiente por su evidencia más débil.
- El objeto de «promoción aprobada» (B l.64) pasa a D-5.

### D-1.e «Adaptación creativa» frente a «Channel Adaptation»
- **(a)** Mismo concepto; el orden distinto es una inconsistencia de las instrucciones originales que se documenta sin corregirla. (**Recomendada** como lectura de trabajo, pendiente de tu confirmación.)
- **(b)** Conceptos distintos: «adaptación creativa» sería crear la pieza visual a partir del copy; añadiría un concepto no listado entre las 18 entidades.

## 10. Consecuencias de la recomendación completa (A, ii, a, a, a) — la decisión final difiere en D-1.d (no se aprueba aprobabilidad; ver Resultado)
- No se añade ni retira ninguna entidad; no se modifica ninguna decisión aprobada.
- Auditoría, versión y aprobación se redactan como capacidades sobre Copy, Pieza y Adaptación.
- Quedan abiertas: relación entre Pieza y Copy (A-5), objeto de «Contenido» en Resultados (A-4, a P4.B), objeto de la aprobación (D-5) y variante (D-2).

## 11. No verificado
Los números de línea de B/A citados se obtuvieron por búsqueda de texto y lectura puntual; las listas de A l.575–578 y A l.603 las leí sin su encabezado completo; no verifiqué si existen otros pasajes que usen «contenido» en el expediente histórico.
