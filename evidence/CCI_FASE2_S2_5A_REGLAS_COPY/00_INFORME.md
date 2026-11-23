# CCI Fase 2 · S2.5a — Reglas deterministas de copy

Decisiones de Claude bajo delegación (revocables). Aplica las decisiones del propietario Q-1, Q-2 y Q-5.

## Qué entra
- `src/domain/copyRules.ts`: motor puro (sin IA, sin red). Reglas: longitud por canal (7 canales), CTA obligatorio/recomendado, términos de marca prohibidos (palabra completa, sin mayúsculas ni acentos, solo sugiere), leyendas obligatorias activas por canal (crítica si faltan), porcentajes del copy vs. oferta del brief con tolerancia 0.5 pp, redacción mecánica (espacios dobles, signos repetidos, titular en mayúsculas).
- Puntaje 0–100 con pesos Q-5 (25/25/15/15/10/10), tope por categoría, crítica limita a 59; apto ≥85, revisar 60–84, no apto <60.
- Botón «Revisar reglas» en cada copy (muestra puntaje, veredicto y hallazgos).

## Supuestos de Claude (reversibles)
- Mapeo de campos del canal al copy de 4 campos (asunto/título/H1→Titular, preheader→Descripción, mensaje→Texto).
- Deducción = peso de categoría × factor de severidad; tope por categoría.
- Porcentaje distinto del brief = crítica; porcentaje sin respaldo en el brief = mayor.
- Términos de marca de ejemplo: plantilla NO validada, aún no editable.

## No incluido (S2.5b)
- Pantalla para capturar/editar leyendas y términos de marca, persistencia en IndexedDB y respaldo. Hasta entonces las leyendas están vacías y NO se revisan.
- Ortografía (no hay corrector determinista); precios absolutos (el brief no tiene precios numéricos).

## Verificación
- `npm run verify` exit 0 (246 pruebas unitarias, 12 nuevas del motor).
- Playwright completo ×3: verdes (ver logs).
- Longitudes por canal NO verificadas contra plataformas.
