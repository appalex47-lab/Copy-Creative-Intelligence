# S1.13 — Aplazamientos: qué existe y qué decide Claude bajo delegación

Fecha: 2026-11-23. Estado: **revocable**. Son decisiones de Claude bajo la delegación del propietario ("Ya los tienes", "decide tú"), no del propietario.

## 1. Hallazgo (verificado por dos vías)
Una revisión independiente (ChatGPT, pegada por el propietario) y la búsqueda propia de Claude en el repositorio y en chats coinciden: **no existen valores decididos** para Q-1 (redondeo/tolerancia), Q-2 (reglas por canal), Q-5 (pesos), P7, P6, P8, Q-3, Q-6 ni P15. Los 10 aplazamientos fueron ratificados (B8, 22-11-2026), no resueltos. Las "Recomendaciones iniciales" no son decisiones (REGISTRO_DECISIONES_RESUELTAS.md).
Existe como definición documental: fórmula de descuento (R-041) y lista inicial de canales (D7.c: Ecommerce, App, WhatsApp, Email, Redes sociales, Banners, Landing pages; "Llamadas" no aparece).

## 2. Decisiones de Claude bajo delegación (supuestos reversibles)
| Punto | Supuesto adoptado | Nota |
|---|---|---|
| Q-1 | Redondeo a 2 decimales, mitad hacia arriba; tolerancia configurable en puntos porcentuales | **Valor de tolerancia: no definido.** Sin valor por defecto inventado |
| P6 | JSON (ya implementado en S1.9) | ZIP no adoptado |
| P7 | Sin cifrado en el MVP; reconsiderar antes de Fase 5. No se promete cifrado | |
| P8 | IA-A + IA-B para Fases 1–2; sin BYOK | IA-C solo con aceptación explícita de riesgos |
| Q-3 | Estados propuestos en 06_MODELO_DE_DOMINIO: Borrador, En revisión, Requiere corrección, Corregido, Aprobado, Archivado; Rechazado como salida alterna | Transiciones permitidas: **sin definir** |
| Q-6 | Español como idioma inicial | |
| P15 | Todos los derechos reservados (ver docs/decisions/LICENCIA_PENDIENTE.md) | Titularidad no verificada |

## 3. Siguen pendientes del propietario (Claude no los inventa)
- Q-2: límites/reglas reales por canal, y si "Llamadas" debe incluirse.
- Q-5: categorías, escalas, pesos y severidades.
- Q-1: valor de la tolerancia.
- Q-3: transiciones permitidas.
- Plazos: Q-5 antes de Fase 3; Q-1 y Q-2 antes de Fase 4; Q-3, P7 antes de Fase 5.

## 4. Confirmaciones del propietario
URL en vivo: "Funciona". Dominio propio: "No" (a futuro, no ahora).

## 5. Confirmación posterior del propietario
Q-2: "Llamadas" NO entra en la lista de canales (confirmado por el propietario, 2026-11-23).

## 6. Aprobación del propietario (2026-11-23 01:01, CDMX)
"Si a todo": el propietario aprueba como suyas P6, P7, P8, P15, Q-6 y los 7 estados de Q-3 (tabla §2), además de Q-1, Q-2 y Q-5 (ver 01_). Siguen abiertas, a entregar por el propietario al iniciar la Fase 3: leyendas regulatorias obligatorias y términos de marca prohibidos. Q-3: transiciones permitidas, para la Fase 5. Salvedades vigentes: titularidad del código (P15) y longitudes de Q-2 no verificadas.
