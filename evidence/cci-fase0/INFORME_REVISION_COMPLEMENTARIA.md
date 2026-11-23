> **AVISO DE VIGENCIA (ronda de lectura 2026-11-22; el contenido original no se altera).** Copia previa del expediente (raíz): **histórica / propuesta anterior**. No constituye estado vigente ni acepta Fase 0 ni autoriza Fase 1. Decisiones posteriores del propietario (P1, P2, P3, Q-7, D-1…D-8, P4.A 9/18) en `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`; jerarquía de fuentes en `auditoria_integral/01_INDICE_MAESTRO_FASE0.md`.

# Informe de revisión complementaria del expediente de Fase 0
Fecha: 2026-11-22. Alcance: solo documentación local. Sin cambios en el repositorio de desarrollo, sin ramas fusionadas ni borradas, sin commits/push/PR/publicaciones/despliegues, sin tocar CCI-DEV/CCI-PROD, sin subir nada a `CCI-Evidence` (esa autorización previa no se asume cubierta).
## 1. Dictamen
**LISTO CON LIMITACIONES DOCUMENTADAS** (antes: listo para revisión). La Fase 0 **no está aceptada**; sigue sin recomendarse aceptarla mientras las 11 decisiones indispensables estén abiertas.
## 2. Qué se hizo y qué quedó comprobado
| Punto | Resultado | Cómo se comprobó |
|---|---|---|
| Referencias con numeración antigua | **Corregidas** en 01, 02, 03, 07, 13, 15 y 06: ahora apuntan a nombres formales o a `../` | grep de patrones `§0N`, `` `NN` ``; luego verificación de que cada archivo `.md` citado existe (solo «faltan» `DECISIONES.md`, `README.md`, `ROADMAP.md`, `ARQUITECTURA.md`, `CI.md`, que son del repositorio y no del expediente) |
| Manifiesto nuevo | 49 archivos (47 previos + informe de revisión + matriz de decisiones); 0 fallos | `sha256sum -c` |
| 17 entregables presentes | Sí: 17 archivos con nombre formal | listado |
| Respeto de browser-only | Los términos Supabase/PostgreSQL/SQL/RLS/login/backend/multiusuario aparecen solo como exclusión, antecedente histórico o alternativa descartada (IA-E) | grep en los documentos de diseño y lectura de cada coincidencia |
| Cifras entre documentos | 162/162, 29/29 ×3, K1–K20 (20 filas), 42 criterios AC, 11 indispensables: coinciden | conteo por grep |
| Matriz de requisitos | 45 filas con IDs R-001…R-062 **no contiguos** (agrupados por fase). No es un defecto; antes yo había descrito «R-001…R-062» sin aclararlo | conteo |
| Originales 00–14 | **Sin alteraciones** | manifiesto previo: coinciden |
| Manifiesto previo | 37 de 47 coincidían; los 10 que difieren son exactamente los que edité en esta revisión (esperado) | `sha256sum -c` antes de regenerar |
| Git | HEAD `ffb47bc319db0806250bcecf91d390fa59fa0d70`, rama `integration/cci-fase1-1-accepted`, 0 cambios sin confirmar; `main` remoto `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` sin cambios (lectura con `ls-remote`) | comandos de solo lectura sobre el clon auditado |
## 3. MVP: propuestas no sustentadas
`10_DEFINICION_MVP_CCI.md` marca cada celda como [S] (dicho por ti), [D] (derivado de decisiones o riesgos del expediente) o [P] (propuesta mía sin sustento). La **complejidad** es [P] en los 9 módulos. El módulo 9 (Brand Intelligence / Settings) no aparece en tus seis fases; su ubicación en Fases 1 y 3 es [P]. Dependencias, datos y riesgos de los módulos 6 y 8 son casi todos [P].
## 4. Decisiones y aprobaciones
`MATRIZ_DECISIONES_PROPIETARIO.md` (11 fichas individuales, todas **sin respuesta**) y `APROBACIONES_FASE0.md` (0.1–0.7, final y Fase 1 por separado, todas **PENDIENTE**). Cambio editorial a confirmar: P4 se presenta separado de Q-4 (el registro original los combinaba).
## 5. Qué sigue siendo propuesta
Todo el diseño (arquitectura, dominio, datos, persistencia, respaldo, IA, MVP, roadmap, riesgos, README). Nada está aprobado ni implementado.
## 6. Qué requiere tu decisión
Las 11 indispensables (P1, P2, P3, P4, P5, P9, P11, P12, P13, P14, Q-4); las aprobaciones 0.1–0.7 y el cierre; la autorización de Fase 1 (aparte); qué hacer con la rama pública `review/cci-auditoria-fase0-browser-only`; entrega a `CCI-Evidence` (requiere autorización específica nueva y que exista el repositorio).
## 7. Qué no he podido verificar
- No repetí hoy las pruebas (162/162, E2E, build): su evidencia es de la ejecución anterior, sobre el mismo commit.
- `npm audit`, CI real, navegadores distintos de Chrome, cuota/expulsión/Web Locks.
- Que ChatGPT acceda a algún repositorio privado; que `CCI-Evidence` exista (la credencial de esta sesión no puede crearlo).
- Los registros de decisiones originales D1–D9 no se releyeron en esta revisión; **Corregido el 2026-11-22:** ahora sí se leyeron los registros originales (ver `entregables_formales/CONCILIACION_D1_D9_VERIFICADA.md`); mi cita «D4 = CCI-DEV/PROD» dentro de D1–D9 era errónea (hay dos series de IDs).
- Estimaciones de probabilidad/impacto de la matriz de riesgos y de complejidad del MVP: juicio mío.
- Las copias formales conservan el contenido base; solo cambié referencias, cabeceras y los documentos señalados.

> **Nota fechada 2026-11-22 20:14 (respuesta del propietario; no es decisión nueva de este documento):** el propietario emitió las aprobaciones 0.1–0.7 (7/7; la 0.5 solo en cuanto a principios, con P8 sin resolver y sin ninguna integración aprobada) y respondió «sí» a R-1 (aplazamiento aceptado de las seis cuestiones residuales, no resolución). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a aprobaciones «PENDIENTES» o «abiertas» describen el estado previo y quedan superadas en ese punto. **La aceptación formal de Fase 0 y la autorización independiente de Fase 1 siguen PENDIENTES.**

> **Nota fechada 2026-11-22 20:26 (respuesta del propietario; no es decisión nueva de este documento):** el propietario aceptó formalmente la Fase 0 («Acepto formalmente la Fase 0, con las limitaciones expresas C-2 y C-3 abiertas y los 10 aplazamientos pendientes. No autoriza la Fase 1.»; redacción propuesta por Claude y adoptada literalmente). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «Fase 0 no aceptada» o a la aceptación formal como pendiente describen el estado previo y quedan superadas en ese punto. **C-2, C-3 y los 10 aplazamientos siguen abiertos y la autorización de la Fase 1 sigue PENDIENTE** (acto independiente). Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.
