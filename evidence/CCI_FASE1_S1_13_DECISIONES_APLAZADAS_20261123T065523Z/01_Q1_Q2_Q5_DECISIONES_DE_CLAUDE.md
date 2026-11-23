# Q-1, Q-2, Q-5 — decisiones de Claude bajo delegación (revocables)

Fecha: 2026-11-23. Delegación: "Te dejo proponer y decidir". Son **supuestos reversibles**, no hechos del negocio ni requisitos regulatorios. Todo valor es **configurable** (regla de la propia ReglaComercial/ReglaDeMarca). Ninguno está implementado todavía (Q-5 antes de Fase 3; Q-1/Q-2 antes de Fase 4).

## Q-1 — Descuento
- Fórmula (documentada, R-041): ((Precio original − Precio promocional) / Precio original) × 100.
- Redondeo: 2 decimales, mitad hacia arriba, al calcular.
- Tolerancia por defecto: **0.5 puntos porcentuales**, configurable. Motivo: permite que una pieza diga el % redondeado a entero sin falso error. Si la diferencia supera la tolerancia → hallazgo **crítico**.
- Precio original ≤ 0 o promocional > original → dato inválido (no se calcula).

## Q-5 — Scoring de auditoría (determinista y explicable)
- Escala: 0–100 por pieza; cada hallazgo muestra categoría, regla, peso y evidencia.
- Categorías y pesos por defecto (suman 100):
  | Categoría | Peso | Crítica |
  |---|---|---|
  | Cumplimiento regulatorio/legal (medicamentos, leyendas obligatorias) | 25 | Sí |
  | Precios y promoción (descuento, vigencia, condiciones) | 25 | Sí |
  | Marca (tono, términos prohibidos, identidad) | 15 | No |
  | Claridad del mensaje y CTA | 15 | No |
  | Adecuación al canal (longitudes, formato) | 10 | No |
  | Ortografía y redacción | 10 | No |
- Severidades: **Crítica** (bloquea la aprobación, cap de la nota en 59), **Mayor** (resta el peso completo de la regla), **Menor** (resta la mitad), **Aviso** (no resta).
- Cálculo: 100 − suma de descuentos por hallazgos, mínimo 0; resultado: ≥85 apto, 60–84 revisar, <60 no apto. Umbrales configurables.

## Q-2 — Reglas por canal (7 aprobados; Llamadas fuera)
Valores **orientativos y NO verificados** contra las plataformas ni contra la regulación; sirven de punto de partida editable. Siempre aplican: leyendas regulatorias obligatorias y términos prohibidos de la regla de marca (las define el propietario).
| Canal | Estructura | Longitud orientativa | CTA |
|---|---|---|---|
| Ecommerce | título, descripción, CTA | título ≤ 70; descr. ≤ 300 | obligatorio |
| App | push/in-app: título + cuerpo | título ≤ 40; cuerpo ≤ 120 | obligatorio |
| WhatsApp | mensaje de texto | ≤ 600 caracteres | obligatorio |
| Email | asunto, preheader, cuerpo | asunto ≤ 60; preheader ≤ 100 | obligatorio |
| Redes sociales | texto de publicación | ≤ 280 | recomendado |
| Banners | titular + CTA | titular ≤ 40 | obligatorio |
| Landing pages | H1, subtítulo, CTA | H1 ≤ 70 | obligatorio |
- "Otros formatos aprobados" por el propietario se añaden como reglas nuevas.
