# Control de cambios — Registro de decisiones D4, D6, D7 y D8 (2026-11-22)
**Base:** HEAD `cb653b2343d795af08fd81d88618ccaf465f2cc5`. **Alcance:** solo documentación del expediente `evidence/cci-fase0/`; sin código, sin `main`, sin merge/PR/deploy.

## 1. Selección registrada (decisiones del propietario)
D4.a=A · D4.b=A · D4.c=A · D4.d=A · D6.a=A · D6.b=A · D6.c=A0 · D7.a=A · D7.b=A · D7.c=C · D8=A. Texto literal en `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` (sección «D-4, D-6, D-7 y D-8 — RESUELTAS»).

## 2. Verificación de compatibilidad (documental; sin inventar decisiones)
| Punto | Resultado | Evidencia |
|---|---|---|
| D4.a–d frente a D-1 | Compatible | D-1.b: Adaptación concepto propio, derivado de Copy; D4.a/D4.c lo repiten. D-1.c (no auditar adaptaciones) no se altera: D4.b no decide auditabilidad. |
| D4.a–d frente a D-2 | Compatible | D4.a distingue Adaptación de Variante y Versión; no concede versiones a Variante (D-2.b). |
| D4.d frente a D-5.3 | Compatible | D4.d=A resuelve la «Adaptación pendiente de D-4» (D-5.2) bajo los límites de M-1; no se reabre D-5. |
| D6.a=A, D6.b=A, D6.c=A0 | Compatibles según la matriz (§6) | D6.b exige D6.a=A o B; A0 exige D6.a=A y admite cualquier D6.b. A0 no presupone ni aprueba D6.b=A. |
| D7.a, D7.b, D7.c frente a decisiones previas | Sin contradicción | D7.b alinea con D-3.b (ReglaComercial); D7.c=C no fija mecanismo; Q-1 y Q-2 siguen abiertas. |
| D8=A frente a D6.c=A0 | Compatible | «Resultado de desempeño» recibe los valores; Metric = definición. |
| Contradicción real detectada | **Ninguna** | — |
Limitación: compatibilidad comprobada por lectura de la matriz y del registro, no por revisión línea a línea de los 52 documentos históricos de `docs/fase0`.

## 3. Archivos
- **Modificados:** REGISTRO_DECISIONES_RESUELTAS.md (sección nueva), RONDA_UNICA_D4_D6_D7_D8_MATRIZ_CONSOLIDADA.md, PAQUETE_DECISION_D4_D6_D7_D8.md, DECISIONES_P4_PENDIENTES.md, CATALOGO_DEPENDENCIAS_D4_D8.md, MATRIZ_CONSOLIDADA_18_ENTIDADES.md, 16_INDICE_EVIDENCIAS_FASE0.md (todas con nota de actualización, sin reescritura), 00_INDICE_VIGENTES_E_HISTORICOS.md, README_ENTREGA.md, MANIFEST.sha256, INVENTARIO_PUBLICADO.sha256.
- **Creados:** este control de cambios e INFORME_CIERRE_2026-11-22_REGISTRO_D4_D6_D7_D8.md.
- **Preservados sin cambios:** todos los demás (históricos incluidos).

## 4. Límites
No registra D5.a–d; no cierra C-2, C-3, P4.B, P4.C, E1–E5, Q-1, Q-2; no aprueba entidades, atributos, relaciones, cardinalidades, persistencia, fórmulas, catálogo de métricas ni mecanismos; no acepta Fase 0 ni autoriza Fase 1.
