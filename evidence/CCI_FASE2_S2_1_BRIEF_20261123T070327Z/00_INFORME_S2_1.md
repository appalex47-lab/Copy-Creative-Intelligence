# Fase 2, S2.1 — Dominio del Brief (AC2-01, AC2-02)

Fecha: 2026-11-23. Ejecutado por Claude por orden del propietario ("Ya no voy a decidir yo nada. Lo harás tú siempre. Ejecuta lo que sigue").
Precondiciones de Fase 2 (P6, P8, Q-6): resueltas y aprobadas por el propietario (S1.13).

## Entregado
- `src/domain/brief.ts`: 13 campos (R-020), validación por campo, `evaluateBrief` que devuelve estado (completo/incompleto), campos faltantes y campos inválidos con motivo; nada se rellena ni se infiere.
- `src/domain/brief.test.ts`: 11 pruebas (completo, cada obligatorio ausente, entrada vacía/no objeto, solo espacios, frontera de longitud, tipos/saltos/control, canal con 7 aprobados y Llamadas fuera, vigencia con fechas reales y bisiestos, determinismo).
- Bug propio hallado por las pruebas y corregido: los campos de una línea convertían el salto de línea en espacio en vez de rechazarlo.

## Supuestos de Claude (reversibles; el propietario delegó todas las decisiones)
- Obligatorios: campaña, objetivo, producto, audiencia, mensaje, canal, CTA. Opcionales: oferta, beneficio, vigencia, condiciones, tono, formato.
- Longitud máxima 120 (una línea) y 500 (texto largo). Vigencia como rango de fechas AAAA-MM-DD.
- Canal restringido a los 7 aprobados (Q-2).

## Plan de la Fase 2 (siguientes cortes)
S2.2 persistencia de briefs/campañas (IndexedDB v3, contrato de repositorio, respaldo) · S2.3 pantalla de brief con validación por campo · S2.4 copys, variantes y versiones inmutables · S2.5 reglas de copy deterministas · S2.6 flujo manual sin IA y plantillas (IA-A/IA-B) · S2.7 buscar/etiquetar/comparar/historial · S2.8 exportación round-trip · S2.9 cierre y acta.

## No verificado
Que los obligatorios/longitudes sean los que el negocio quiere en la práctica (se verá con la pantalla de S2.3). Sin cambios de UI en este corte: no se corrieron E2E nuevos.
