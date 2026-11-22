# D-3 — Familias de reglas (copy, marca, comerciales y por canal) — RESUELTA (2026-11-22 12:14)
## Resultado de D-3 (decisiones del propietario, con sus límites)
| Sub-decisión | Decisión | Límite exacto |
|---|---|---|
| D-3.a | **(a)** Cuatro familias distintas: copy, marca, comerciales y por canal | Fundamentada en propósito, objeto regulado y contexto funcional; no implica cuatro entidades |
| D-3.b | **(a)** Solo ReglaDeMarca y ReglaComercial son entidades independientes | No se autorizan entidades para reglas de copy ni de canal; sin atributos, estructuras, relaciones, cardinalidades ni mecanismos de administración |
| D-3.c (canal) | **(i)** Dimensión de aplicación del Canal | Sin entidad independiente ni especialización automática de ReglaDeMarca; sin aprobar su representación ni su relación con Canal/Adaptación |
| D-3.c (copy) | **(i)** Familia conceptual diferenciada | Ubicación en el modelo pendiente de **P4.B**; no se incorpora a ReglaDeMarca ni es entidad sin decisión posterior |
| D-3.d | **Aprobado**: criterios propósito, objeto regulado y contexto/fase | Solapamiento de longitud, formato, tono y CTA entre reglas de copy y de canal **documentado**; no autoriza duplicar reglas ni fijar prioridades, precedencias o resolución de conflictos |

**Corrección de antecedentes (conservada):** la inclusión de reglas de copy en ReglaDeMarca fue derivación mía y queda sin efecto.
**Limitación de la evidencia:** las instrucciones originales no contienen una lista específica de reglas de marca; no se inventa una. Solo constan «Reglas de marca» como criterio de auditoría (B l.435; A l.589), «Consistencia de marca» (B l.444) y el módulo «Brand Intelligence / Settings» (B l.31; A l.56, l.536).
**Sigue abierto:** ubicación de las reglas de copy (P4.B); representación de las reglas por canal; contenido de las reglas de marca; D-4 a D-8. P4.1, P4.2, D-1 y D-2 intactas; entidades 1–8 sin cambios; Hallazgo (9) sin aprobar.

---
*Lo que sigue es el análisis original previo a la decisión, conservado como antecedente (su §8 refleja el estado a las 12:11).*
**Naturaleza:** análisis y propuesta; **no aprueba nada.** Conserva D-1, D-2, P4.1, P4.2 y las entidades 1–8. No aprueba atributos, relaciones, cardinalidades, prioridades, severidades, fórmulas ni mecanismos; no avanza a D-4, D-5, P4.B ni P4.C. Referencias: A = Fase 0 (`de49cc27`), B = instrucción maestra (`5a9f5585`); «l.» = línea.

## 1. Evidencia textual original (E), por familia
### Reglas de copy
- Sección propia «Reglas de copy» dentro de Fase 2, con ocho elementos: longitud, ortografía, palabras obligatorias, palabras prohibidas, consistencia, tono, CTA, formato (B l.385–393). A l.580 «Reglas» en el alcance de Fase 2; B l.406 «Reglas» en las pruebas de Fase 2.
- Aplicación: «Las reglas deterministas se ejecutan en código» (B l.396); «La IA no sustituye la validación comercial» (B l.397).
- **Regula:** el copy (su forma textual). Fase 2; sus criterios afines reaparecen en la auditoría de copy de Fase 3 (ortografía, tono, consistencia, CTA: B l.428–434).
- **Sin texto** sobre configurarlas, administrarlas o reutilizarlas.

### Reglas de marca
- «Reglas de marca» como **un criterio más** de la auditoría de copy, junto a ortografía, tono, consistencia y CTA (B l.435); «Consistencia de marca» en la auditoría visual (B l.444). A l.589: «Reglas de marca» en el alcance de Fase 3. A l.357 `BrandRule`; B l.206 «Reglas» (una sola, en la lista de entidades de B).
- Módulo objetivo 9 «Brand Intelligence / Settings» (B l.31; A l.56 y l.536). No localicé sección de fase específica para ese módulo: «Brand» solo aparece en la lista de módulos.
- **Regula:** copy y pieza visual (como criterio de auditoría). Fase 3.
- **Sin texto** sobre qué contienen (no hay lista de elementos como en las demás familias) ni cómo se configuran; el módulo «Brand Intelligence / Settings» **sugiere** administración, sin decirlo.

### Reglas comerciales
- Promotion Validator valida precio original, precio promocional, descuento, vigencia, restricciones, productos incluidos, exclusiones, condiciones, texto legal y coherencia oferta–copy (B l.508–517); fórmula de descuento (B l.521); «reglas de redondeo y tolerancias **configurables** según decisión aprobada» (B l.523); clases de resultado: error comprobado, inconsistencia, información faltante o no verificable, advertencia, bloqueo justificado (B l.525–530); «No inventar información comercial» (B l.534).
- Principios: reglas de negocio deterministas (B l.63); «Las reglas comerciales deben ejecutarse en código» (A l.92; A l.518). A l.599–602 («Descuentos», «Tolerancias», «Condiciones»).
- **Regula:** la oferta y su coherencia con el copy. Fase 4. Es la **única familia con texto explícito de configurabilidad** (tolerancias y redondeo).

### Reglas por canal
- «Cada canal tendrá reglas de» longitud, estructura, formato, tono, CTA, restricciones, elementos obligatorios (B l.549–556), para los canales aprobados (Ecommerce, App, WhatsApp, Email, Redes sociales, Banners, Landing pages, otros: B l.538–547). La trazabilidad de la adaptación conserva «Reglas» (B l.567). A l.603–604 «Adaptación por canal», «Reglas de formato». A l.359 `Channel`.
- **Regula:** la adaptación a cada canal. Fase 4.
- **Sin texto** sobre cómo se administran; se dice que cada canal «tendrá» sus reglas (posesión).

### Elementos transversales
- Hallazgo: campo «Regla» (B l.459); pruebas de «Reglas bloqueantes» (B l.486); la IA no modifica reglas unilateralmente (B l.470). Estos textos **no dicen de qué familia** es la regla citada.

## 2. Decisiones tuyas aplicables
- **P4.2 = (b):** ReglaDeMarca y ReglaComercial independientes (nombres 10 y 11 confirmados en P4.1). No dijiste que las reglas de copy pertenezcan a ReglaDeMarca ni que las de canal sean entidades.
- **P4.1:** de las cuatro familias, solo tienen nombre de entidad confirmado BrandRule, CommercialRule y Channel; **no existe** una entidad de reglas de copy ni de reglas de canal.
- **D-1.b/e:** la adaptación es concepto propio (entidad 13) derivado de un copy fuente. **D-1.c:** Auditoría sobre Copy o Pieza.
- **D-2:** variantes y versiones separadas.
- Las entidades 10, 11 y 12 no tienen definición aprobada (solo nombre).

## 3. Derivaciones razonables (D)
- **D-a** El texto presenta las cuatro familias por separado, con fase y objeto regulado distintos: copy (forma del texto, Fase 2), marca (criterio de auditoría de copy y pieza, Fase 3), comercial (oferta, Fase 4), canal (adaptación, Fase 4).
- **D-b** «Reglas de marca» figura **como elemento aparte** dentro de la lista de criterios de la auditoría de copy: indicio textual de que no es lo mismo que las reglas de copy (ortografía, tono, consistencia, CTA). El contenido de las reglas de marca, en cambio, **no está definido**.
- **D-c** «Cada canal tendrá reglas» sugiere que las reglas por canal se **aplican por canal**: son una dimensión de aplicación vinculada al Canal más que una familia con identidad propia.
- **D-d** **Solapamiento de dimensiones:** longitud, formato, tono y CTA aparecen en las reglas de copy (B l.385–393) **y** en las reglas de canal (B l.549–556); «elementos obligatorios» aparece en canal (B l.555) y en la auditoría visual (B l.445); tono y palabras obligatorias/prohibidas son rasgos típicos de marca y figuran en reglas de copy.
- **D-e** Todas se evalúan de forma determinista en código (B l.63, l.396, l.585; A l.92). Solo las comerciales declaran configurabilidad.

## 4. Propuestas mías (P, **no aprobadas**)
- **P-1** Distinguir las familias por tres criterios: propósito, objeto regulado y fase de aplicación.
- **P-2** Tratar las reglas por canal como **dimensión de aplicación** del Canal (no como familia independiente con entidad propia).
- **P-3** No asignar las reglas de copy a ninguna entidad todavía.
- **Corrección de mi trabajo previo:** en `LISTA_ORIGINAL_18_ENTIDADES.md` describí BrandRule como «regla de marca y de copy»: esa inclusión fue **derivación mía no aprobada** y la dejo sin efecto.

## 5. Alternativas
**A. Cuatro familias conceptuales diferenciadas.**
- **A-1:** cada familia es entidad propia. Exigiría **revisar P4.1** (dos entidades nuevas: reglas de copy y reglas de canal).
- **A-2:** las cuatro se **distinguen conceptualmente**, pero solo se materializan como entidad las ya confirmadas (ReglaDeMarca, ReglaComercial); las reglas por canal quedan como dimensión de Canal (entidad 12); las reglas de copy quedan como familia sin ubicación decidida.

**B. Dos entidades (ReglaDeMarca y ReglaComercial), con copy y canal como categorías.** Las reglas de copy irían a ReglaDeMarca (lo que indicaste que no debe darse por hecho) y las de canal a una de las dos, sin que ninguna encaje (longitud, estructura o formato no son marca ni comercial).

**C. Modelo genérico:** una entidad común «Regla» con clasificación por familia. Exigiría **revisar P4.2 y los nombres 10 y 11 de P4.1**, que confirmaste como separados.

| Aspecto | A-1 | A-2 | B | C |
|---|---|---|---|---|
| Ventajas | Claridad máxima | Respeta P4.1 y P4.2; refleja el texto | Pocas entidades | Un solo lugar y un solo destino para «Regla» del Hallazgo |
| Desventajas | Añade 2 entidades; riesgo de proliferación | Deja una familia (copy) sin hogar | Fuerza clasificaciones sin respaldo | Borra la separación aprobada |
| Riesgo de duplicidad | Dimensiones repetidas en 3 lugares (D-d) | Igual, pero visible | Se ocultan bajo categorías | Menor estructural; las dimensiones se repiten como datos |
| Claridad de responsabilidades | Alta | Alta, salvo copy | Baja (copy en marca) | Media (la familia es un dato) |
| Copy | Tiene sus reglas | Reglas de copy por ubicar | Reglas dentro de marca | Clasificadas |
| Pieza creativa | Marca | Marca | Marca | Marca |
| Adaptación | Reglas de canal | Reglas de Canal | Sin hogar claro | Clasificadas |
| Auditoría creativa | Consume 3 familias | Consume copy y marca (sin cambio de D-1.c) | Igual | Igual |
| Fase 2 / 3 / 4 | Cada familia en su fase | Cada familia en su fase | Mezcla copy (2) con marca (3) | Todas en un solo tipo |
| Decisiones previas | Exige revisar P4.1 | Conserva todas | Conserva, pero contradice tu instrucción sobre copy | Exige revisar P4.1 y P4.2 |

## 6. Recomendación: **A-2**
Respeta P4.1, P4.2, D-1 y D-2; sigue la separación textual de las cuatro familias; evita forzar clasificaciones (B) o borrar la separación aprobada (C); y deja sin decidir lo que las instrucciones no resuelven (el hogar de las reglas de copy y el contenido de las reglas de marca).

## 7. Decisiones concretas que necesito
**D-3.a — Qué familias existen.** (a) Cuatro familias conceptualmente distintas (copy, marca, comerciales y por canal), distinguidas por propósito, objeto regulado y fase (**recomendada**) · (b) tres (copy y marca juntas) · (c) otra.
**D-3.b — Cuáles necesitan entidad independiente.** (a) Solo las ya confirmadas, ReglaDeMarca y ReglaComercial (P4.2) (**recomendada**) · (b) también reglas de copy y/o canal, con revisión explícita de P4.1.
**D-3.c — Cuáles pueden ser clasificación o especialización.** Reglas por canal: (i) dimensión de aplicación del Canal (**recomendada**) · (ii) entidad propia (revisión de P4.1) · (iii) especialización de ReglaDeMarca. Reglas de copy: (i) familia conceptual sin ubicación decidida por ahora, pendiente de P4.B (**recomendada**) · (ii) categoría de ReglaDeMarca, con justificación funcional que hoy no existe · (iii) entidad propia (revisión de P4.1) · (iv) otra.
**D-3.d — Diferencias funcionales a preservar.** Confirmar como criterios de distinción (no mecanismos): propósito, objeto regulado y fase de aplicación (**recomendada**), dejando constancia del solapamiento de dimensiones (longitud, formato, tono, CTA, elementos obligatorios) como **riesgo de duplicidad** que se resolverá después.

## 8. Resumen cuantitativo de avance
| Indicador | Valor | Estado |
|---|---|---|
| Entidades P4.A aprobadas (def. mínima) | **8 de 18 (44,4 %)** | Pendientes: 10 de 18 (55,6 %) |
| Dependencias D-1 a D-8 | **2 de 8 resueltas (25 %)** | D-3 a D-8 pendientes (75 %); D-3 en análisis |
| Documentación y evidencias | ver nota | Verificado frente a reportado |
| Repositorio | ver nota | No equivale a avance funcional |

**Nota de verificación (esta sesión):** *Verificado por mí:* manifiesto SHA-256 con `sha256sum -c` (sin fallos), líneas de los adjuntos originales leídas con `sed`/`grep`, estado Git del clon de solo lectura. *Solo reportado, no re-ejecutado hoy:* pruebas (162/162 unitarias; 29/29 E2E), compilación, CI, `npm audit`, navegadores distintos de Chrome 153; contenido de los 52 archivos históricos (solo búsquedas dirigidas). **No presento porcentaje global de Fase 0**: falta una ponderación objetiva y verificable.

## 9. No verificado
Que «Brand Intelligence / Settings» no tenga descripción en otros pasajes; el contenido de las reglas de marca; si «Reglas» en A l.309/375 (dominio, modelo de datos) se refieren a estas familias; la prioridad entre reglas solapadas (no analizada, por tu instrucción).

> **Nota fechada 2026-11-22 (auditoría cruzada):** El cuadro §8 (P4.A 8/18; D-1 a D-8 2/8) refleja el momento de elaboración; D-3 quedó resuelta el 12:14. Estado vigente y fuente: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`; P4.A vigente 9/18; D-1…D-8 resueltas en su alcance. Este documento se conserva como evidencia histórica.
