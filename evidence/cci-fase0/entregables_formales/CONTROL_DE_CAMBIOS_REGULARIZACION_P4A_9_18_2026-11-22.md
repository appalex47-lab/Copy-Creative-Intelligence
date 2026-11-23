# Control de cambios — Regularización documental posterior al registro D4/D6/D7/D8 (2026-11-22)
**Commit base:** `004a736de6ad6702587aedb12a64c7c0e60f04d9` (HEAD real verificado; sin cambios posteriores). **Rama:** `evidence/cci-fase0-review`.
**Motivo:** la revisión de ChatGPT halló el registro correcto, pero estados secundarios anteriores y conteo P4.A 8/18 sin actualizar.
**Cambio de P4.A:** de 8/18 (44,4 %) a **9/18 (50 %)**; fundamento **D4.c=A** (entidad 13, solo definición mínima). Las 11 decisiones y su alcance no se modifican. *[Antecedente superado por la ratificación 15:56: P4.A vigente 18/18.]*

## Archivos modificados y justificación
| Archivo | Justificación |
|---|---|
| DECISIONES_P4_PENDIENTES.md | Encabezado vigente: D4/D6/D7/D8 resueltas; P4.A 9/18; pendientes reales |
| CATALOGO_DEPENDENCIAS_D4_D8.md | Nota vigente y columna «Estado» D-4…D-8 (D-5 también, ya resuelta el 12:29) |
| RONDA_UNICA_D4_D6_D7_D8_MATRIZ_CONSOLIDADA.md | Nota visible inicial: ronda respondida, antecedente |
| MATRIZ_CONSOLIDADA_18_ENTIDADES.md | Estado vigente 9/18 y fila 13 aprobada (def. mínima) |
| REGISTRO_DECISIONES_RESUELTAS.md | Aclaración fechada del efecto de D4.c en P4.A (decisiones intactas) |
| INFORME_CIERRE_2026-11-22_REGISTRO_D4_D6_D7_D8.md | Reescrito: 11/11, 9/18, pendientes reales |
| CONTROL_DE_CAMBIOS_REGISTRO_D4_D6_D7_D8_2026-11-22.md | Nota posterior sobre el conteo |
| 16_INDICE_EVIDENCIAS_FASE0.md, 00_INDICE_VIGENTES_E_HISTORICOS.md, README_ENTREGA.md | Autoridad del registro, 9/18, enlaces |
| MANIFEST.sha256, INVENTARIO_PUBLICADO.sha256 | Regenerados en el formato existente |
**Creado:** este documento.

## Estados secundarios corregidos
D4/D6/D7/D8 ya no figuran como pendientes vigentes en los documentos anteriores; D5.a–d permanecen fuera de alcance.
## Históricos preservados (sin cambios)
`D3_FAMILIAS_DE_REGLAS.md` (cuadro 8/18 fechado), `INFORME_CIERRE_…PAQUETE_D4_D6_D7_D8.md`, `…REGLA_PERMANENTE_12_43.md`, `…CORRECCION_DOCUMENTAL.md`, `PAQUETE_DECISION_D4_D6_D7_D8.md` (con su nota previa), `FICHA_P4A_*`, docs `docs/fase0` y demás: son informes fechados; su 8/18 corresponde a su momento.
## Sin cambios de fondo
D5.a–d, C-2, C-3, P4.B, P4.C, E1–E5, Q-1, Q-2, entidad 9, entidades 10–12 y 14–18, aprobaciones 0.1–0.7: abiertas/pendientes. Fase 0 sin aceptación formal; Fase 1 no autorizada.
## Verificaciones y limitaciones
Ver el informe de entrega (HEAD, API, comparación con main, hashes). No se ejecutaron pruebas/build/CI de la aplicación; la coherencia se verificó por búsqueda de texto en el expediente, no por lectura línea a línea de `docs/fase0`.

> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; el texto original no se altera):** este control de cambios es un registro histórico: el conteo P4.A 9/18 y la suspensión de la entidad 9 que menciona están **superados** (P4.A vigente: 18/18). Fuente: `REGISTRO_DECISIONES_RESUELTAS.md`, sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)».

> **Nota fechada 2026-11-22 20:14 (respuesta del propietario; no es decisión nueva de este documento):** el propietario emitió las aprobaciones 0.1–0.7 (7/7; la 0.5 solo en cuanto a principios, con P8 sin resolver y sin ninguna integración aprobada) y respondió «sí» a R-1 (aplazamiento aceptado de las seis cuestiones residuales, no resolución). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a aprobaciones «PENDIENTES» o «abiertas» describen el estado previo y quedan superadas en ese punto. **La aceptación formal de Fase 0 y la autorización independiente de Fase 1 siguen PENDIENTES.**

> **Nota fechada 2026-11-22 20:26 (respuesta del propietario; no es decisión nueva de este documento):** el propietario aceptó formalmente la Fase 0 («Acepto formalmente la Fase 0, con las limitaciones expresas C-2 y C-3 abiertas y los 10 aplazamientos pendientes. No autoriza la Fase 1.»; redacción propuesta por Claude y adoptada literalmente). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las menciones anteriores de este documento a «Fase 0 no aceptada» o a la aceptación formal como pendiente describen el estado previo y quedan superadas en ese punto. **C-2, C-3 y los 10 aplazamientos siguen abiertos y la autorización de la Fase 1 sigue PENDIENTE** (acto independiente). Conteos de decisiones sin cambio: 20/30 resueltas, 10/30 con aplazamiento aceptado, 0 abiertas.

> **Nota fechada 2026-11-22 20:59 (respuesta del propietario; no es decisión nueva de este documento):** el propietario autorizó **únicamente la subfase S1.0** de la Fase 1 (auditoría técnica y definición del alcance ejecutable; rama `fase1/s1-0-auditoria` desde `7bcba74e05577761081d68ca14fdc19f2400248d`; solo lectura, pruebas existentes sin modificar y documentación/evidencia). Las subfases S1.1 y S1.2 quedan autorizadas solo tras su aprobación expresa de los resultados de S1.0 (no activas). Registro autoritativo: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Autorización de la subfase S1.0». Las menciones anteriores de este documento a la autorización de la Fase 1 como pendiente o a «Fase 1 no autorizada» describen el estado previo y quedan superadas en ese punto; la Fase 1 en su conjunto NO está autorizada. **C-2, C-3 y los 10 aplazamientos siguen abiertos.**
