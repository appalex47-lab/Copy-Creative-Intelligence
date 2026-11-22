# Lista original de entidades y su trazabilidad (para P4.1)
**Estado de P4.1 (2026-11-22): la LISTA DE NOMBRES quedó confirmada como referencia del modelo** (lista A, líneas 348–365; la lista B se conserva como antecedente de alcance general). **No están aprobadas** las definiciones, relaciones, atributos, dependencias ni asignaciones de fase de las tablas siguientes: siguen siendo derivadas (D) o propuesta mía (P). Este documento no aprueba esas columnas. Reproduce las listas del propietario **leyéndolas de los adjuntos originales**, no de memoria ni de mi modelo.
## 1. Fuentes y hallazgo
| Fuente | Archivo adjunto | Contenido |
|---|---|---|
| **A — Instrucción de Fase 0 («CCI — FASE 0»), §7** | `de49cc27-attachment.txt`, líneas 342–389 (lista en **348–365**) | **18 entidades** en inglés: «Evalúa las siguientes entidades» |
| **B — Instrucción maestra de desarrollo, §3 (Fase 0) apartado D** | `5a9f5585-attachment.txt`, líneas 190–214 (lista en **197–212**) | **16 conceptos** en español: «Propón las entidades necesarias para»; «Clasifica cada entidad como imprescindible para el MVP, necesaria para una fase posterior o futura» |
**Hallazgo que debía haberte señalado antes:** existen **dos listas del propietario con diferencias**. La lista B tiene «Reglas» (una sola), no tiene «Canal» como entidad y no menciona «Perfil»; la lista A separa `BrandRule`/`CommercialRule`, añade `Channel` y usa nombres distintos (`CreativeAsset` ≈ «Piezas creativas», `ContentVersion` ≈ «Versiones», `PerformanceRecord` ≈ «Resultados», `ApplicationSettings` ≈ «Configuraciones»). Mi propuesta anterior (una sola `Regla`) coincidía con la lista B, pero en la ficha P4 presenté la lista A como «tu lista» sin explicar la diferencia. Tomo como vigente la lista A (más reciente y específica); tu respuesta P4.2 = (b) la sigue.
**Qué dicen tus listas y qué no:** solo **nombres**. Ninguna define el propósito, campos ni relaciones de cada entidad; esas definiciones las **derivé** de otros pasajes de tus instrucciones (se citan) o son **propuesta mía** (se marcan).
## 2. Lista A completa, con trazabilidad (referencias: A = Fase 0, B = instrucción maestra; «l.» = línea)
Estado del **nombre**: *solicitado por el propietario* (todas). Estado de la **definición** y las **relaciones**: *derivada* (D, con cita) o *propuesta mía* (P).
| # | Nombre original (A) | Definición funcional | Fase / módulo | Relaciones propuestas (P) | Referencias exactas | Estado |
|---|---|---|---|---|---|---|
| 1 | Campaign (A l.348) — **Q-7 = (a): entidad nueva, no equivale a `Project`** | Unidad a la que se asocian brief, contenidos, piezas y resultados (D) | Fase 2 Copy Studio; Library y Performance (Fase 5) | 1–N Brief, Oferta, Copy, Pieza, Resultado | B l.197 «Campañas»; B l.347 «Campaña» (campo del Brief); B l.597; B l.639 | Nombre: solicitado · definición: D · relaciones: P · **sujeta a Q-7** |
| 2 | Brief (A l.349) | Requerimiento de contenido con 13 campos: campaña, objetivo, producto, audiencia, oferta, beneficio, vigencia, condiciones, tono, mensaje central, canal, formato, CTA (D) | Fase 2 | pertenece a Campaña; refiere Producto y Oferta; 1–N Copy | B l.198; B l.345–359 | solicitado · D · P |
| 3 | Product (A l.350) | Producto comercial referido por el brief y por la validación promocional (D) | Fase 2; Fase 4 | N–N Oferta | B l.199; B l.349; B l.513 «Productos incluidos» | solicitado · D · P |
| 4 | Offer (A l.351) | Oferta con beneficio, precios original/promocional, vigencia, restricciones, exclusiones y condiciones (D) | Fase 2; Fase 4 Promotion Validator | pertenece a Campaña; N–N Producto | B l.200; B l.351–354; B l.508–516 | solicitado · D · P |
| 5 | Copy (A l.352) | Contenido textual: titulares, textos principales, descripciones, CTA (D) | Fase 2 | pertenece a Brief/Campaña; 1–N Variante y Versión | B l.201; B l.363–366 | solicitado · D · P |
| 6 | CopyVariant (A l.353) | Alternativa de un copy: tono, objetivo o prueba A/B (D) | Fase 2 | pertenece a Copy | B l.202; B l.367–370 | solicitado · D · P |
| 7 | CreativeAsset (A l.354) | Pieza visual a auditar y reutilizar (D) | Fase 3 Creative Auditor; Library (5) | pertenece a Campaña; vinculada a Copy | B l.203 «Piezas creativas»; B l.439–448; B l.599 | solicitado · D · P |
| 8 | CreativeAudit (A l.355) | Ejecución de auditoría de copy o pieza, con puntuación explicable (D) | Fase 3 | 1–N Hallazgo; sobre una Versión | B l.204; B l.426–448; B l.464–466 (puntuación) | solicitado · D · P |
| 9 | AuditFinding (A l.356) | Hallazgo con 9 campos: identificador, elemento afectado, evidencia, categoría, severidad, regla, recomendación, estado, resolución (D) | Fase 3 | pertenece a Auditoría; refiere una Regla | B l.205; B l.450–462 | solicitado · D · P |
| 10 | BrandRule (A l.357) | Regla de marca y de copy (tono, palabras obligatorias/prohibidas, formato, CTA…) (D) | Fase 2–3 | aplica a Copy/Pieza | B l.206 «Reglas»; B l.385–394; B l.435 «Reglas de marca» | solicitado · D · P · **P4.2 = (b): entidad independiente `ReglaDeMarca`** |
| 11 | CommercialRule (A l.358) | Regla comercial (precios, descuento, vigencia, exclusiones, tolerancias) (D) | Fase 4 | aplica a Oferta | B l.206; B l.504–523 | solicitado · D · P · **P4.2 = (b): `ReglaComercial`** |
| 12 | Channel (A l.359) | Canal aprobado con reglas de longitud, estructura, formato, tono, CTA, restricciones y elementos obligatorios (D) | Fase 4 | usado por Adaptación | B l.538–557 (**no está en la lista B**) | solicitado (solo en A) · D · P |
| 13 | ChannelAdaptation (A l.360) | Adaptación de un copy fuente a un canal, trazable (D) | Fase 4 | de Copy; por Canal | B l.207 «Adaptaciones»; B l.559–569 | solicitado · D · P |
| 14 | ContentVersion (A l.361) | Versión del contenido con historial, fecha, cambios, estado, auditorías vinculadas y motivo; sin sobrescribir contenido aprobado (D) | Fase 2 (historial) y 5 | de Copy/Variante/Pieza/Adaptación | B l.208 «Versiones»; B l.383; B l.623–633 | solicitado · D · P |
| 15 | Approval (A l.362) | Aprobación **humana** en flujo de un usuario (P1) (D) | Fase 5 Workflow & Approvals | de Copy/Pieza/Adaptación | B l.209; B l.607–621 | solicitado · D · P |
| 16 | PerformanceRecord (A l.363) | Dato de desempeño proporcionado por el usuario: campaña, canal, contenido, fecha, impresiones, clics, conversiones, inversión, ventas; manual/importado/calculado (D) | Fase 5 Performance Intelligence | pertenece a Campaña | B l.210 «Resultados»; B l.635–649 | solicitado · D · P |
| 17 | Metric (A l.364) | Indicador calculado con fórmula documentada; no se muestra si faltan datos (D) | Fase 5 | deriva de PerformanceRecord | B l.211; B l.651 | solicitado · D · P |
| 18 | ApplicationSettings (A l.365) | Preferencias y configuraciones duraderas (D) | Fase 1 | — | B l.212 «Configuraciones»; B l.311 y l.51 (preferencias/configuraciones ligeras) | solicitado · D · P |
## 3. Entidades que **no** están en ninguna de tus listas
| Entidad | Origen | Estado de tu decisión (P4.3) |
|---|---|---|
| Evento de actividad | **Derivada** de B l.314 («datos reales, pendientes y actividad real» del Command Center); la entidad es mía | **Aprobada como entidad propuesta**; estructura y eventos por especificar después |
| Etiqueta | **Derivada** de B l.380 («Etiquetar») y l.602 («Etiquetas») | **Aprobada** |
| Perfil local | **Derivada** de tu decisión P1 | **Aprobado** (sin autenticación ni identidad) |
| Colección | **Propuesta mía sin sustento**: la Creative Library de B l.595–604 no menciona colecciones | **Pendiente**; ver `FICHA_P4.md` y el análisis siguiente |
**Análisis de Colección (pedido por ti):** busqué qué necesidad funcional resolvería que no cubran las etiquetas y los filtros. **No encontré ninguna en tus instrucciones**: la Library pide «Búsqueda, Filtros, Etiquetas, Versiones, Auditorías, Reutilización». «Reutilización» se resuelve con etiquetas, filtros y duplicar. Mi propuesta original no tenía respaldo. **Recomendación: no crear la entidad;** la saqué del modelo hasta que exista una justificación.
## 4. Contraste de cantidad
Lista A: 18 · Lista B: 16 · Modelo mío tras tus respuestas: 18 de A (con reglas separadas, por P4.2) + Evento de actividad + Etiqueta + Perfil local = **21**; Colección excluida; Campaña sujeta a Q-7. Lo pendiente de P4 está en `DECISIONES_P4_PENDIENTES.md`.


**Nota 2026-11-22 (D-3):** la fila 10 (BrandRule) describe «regla de marca **y de copy**»; la inclusión de las reglas de copy es **derivación mía no aprobada** y el propietario indicó que NO debe darse por incorporada (ver `D3_FAMILIAS_DE_REGLAS.md`).
