# Diagnóstico integral de coherencia de las 18 entidades — 2026-11-22

> **AVISO DE VIGENCIA (ronda final 2026-11-22; el contenido original no se altera).** Diagnóstico y propuestas de las 11:58 (**antecedente histórico**). Sus recomendaciones (orden D-1…D-8, tratamiento de Perfil local como parte de Configuración, diferir 15 y 17, etc.) fueron **superadas o resueltas por decisiones del propietario** (D-1…D-8; D7.a=A mantiene Perfil local como concepto propio). Estado vigente: `REGISTRO_DECISIONES_RESUELTAS.md`; P4.A vigente 9/18.
Diagnóstico y propuestas. **No aprueba nada ni modifica decisiones ya tomadas.** Matriz completa en `MATRIZ_CONSOLIDADA_18_ENTIDADES.md`. Referencias: A = Fase 0 (`de49cc27`), B = instrucción maestra (`5a9f5585`).

## 1. Resultado general
- **Decisiones 1–8:** no encontré contradicción interna ni definición con implicaciones sin respaldo en las instrucciones. Los alcances que fijaste dejan abiertos justo los puntos conflictivos (objeto auditado, reauditoría, Variante frente a Versión). **No propongo modificar ninguna de ellas.**
- **Todas las entidades de A tienen existencia respaldada** por A o B. Ninguna parece duplicada de otra sin más; sí hay **solapamientos de frontera** que conviene decidir antes de aprobar 9–18.
- Matiz de asimetría en 1–8 (no es contradicción): Producto se define «referenciado en un Brief» y Oferta «asociada al contenido»; el Brief tiene campos para ambos. Se resuelve en P4.B.
- Naming: tu definición de Campaña dice «Resultado de desempeño»; A usa `PerformanceRecord` y B «Resultados». Propongo **Resultado de desempeño** como nombre canónico de la 16 (pendiente de tu confirmación, D-8).

## 2. Puntos que pediste revisar
**Variante de copy (6) frente a Versión de contenido (14).** Criterio propuesto (mío, no solicitado): la variante es una alternativa **simultánea** de un mismo copy (B l.367–370); la versión es el **estado a lo largo del tiempo** (B l.623–633: historial, fecha, cambios, motivos). Riesgo: «Propuestas A/B» y «Comparar versiones» (B l.476) comparan cosas distintas; si se mezclan, el historial se contamina. Afecta: entidad 6 ya aprobada (sin cambio, pues dejaste la delimitación abierta) y 14.

**Auditoría creativa (8) frente a Hallazgo (9).** Mi lectura: son entidades distintas. La auditoría es la ejecución; el hallazgo tiene identificador, estado y resolución propios (B l.452–462) y se «documenta pendiente» (l.478), por lo que puede persistir tras una reauditoría. Ambas listas, A y B, los nombran por separado. Recomiendo mantener 9 como independiente. Depende de D-1 (elemento afectado) y de la semántica de reauditoría.

**ReglaDeMarca (10) frente a ReglaComercial (11).** P4.2 = (b) se respeta. Hallazgo nuevo: B distingue «Reglas de copy» (l.385), «Reglas de marca» (l.435), reglas del validador comercial (l.504–523) y reglas por canal (l.549). En mi trabajo previo **fundí las reglas de copy dentro de ReglaDeMarca**: eso es derivación mía, no instrucción tuya. Hace falta decidir a qué familia pertenecen las reglas de copy y si las reglas de canal quedan dentro de Canal (componente) o forman otra familia. Esto no reabre P4.2.

**Copy (5) frente a Pieza creativa (7).** Separación clara: texto frente a recurso visual, con «Congruencia copy-pieza» como relación (B l.447). Ambigüedad: los canales «Banners» y «Landing pages» (B l.545–546) pueden ser salidas visuales; no está dicho si una adaptación a banner produce un Copy, una Pieza o ambos (D-4).

**Campaña, Brief, Producto, Oferta (1–4).** Coherentes entre sí. Riesgo residual: Brief repite Campaña/Producto/Oferta/Vigencia/Condiciones como campos; si luego el Brief solo **contiene** esos datos en lugar de referenciarlos, Producto y Oferta quedarían parcialmente redundantes. Se decide en P4.B junto con la duplicidad de Vigencia/Condiciones; no requiere cambiar 1–4.

**Perfil local, Etiqueta, Evento de actividad.** Aprobados en P4.3; no los reabro. Observaciones:
- Perfil local no aparece en A ni en B; viene de P1 y solo tiene un nombre visible opcional. Solapa con Configuración (18). **Propuesta pendiente de tu autorización:** tratarlo como componente de Configuración (afecta P4.3).
- Etiqueta: sin conflicto.
- Evento de actividad: puede duplicar historiales de Versión (14), Aprobación (15) y Auditoría (8). Mantener, pero delimitar.

## 3. Entidades 10–18: otras observaciones
- **Aprobación (15):** los siete estados de B l.609–617 son estados del **contenido**, no de una «aprobación»; con un único usuario local (P1; B l.621) puede ser un cambio de estado más que una entidad. Recomiendo **diferir** hasta D-5.
- **Métrica (17):** puede ser definición de indicador o valor calculado; si es valor calculado a partir de Resultados (B l.651), no necesita entidad. Recomiendo **diferir** hasta D-6. «Calculados» en la 16 (B l.649) debe delimitarse frente a la 17.
- **Canal (12):** solo está en A, no en la lista B (l.197–212). Falta decidir si es catálogo editable o lista fija (D-7).
- **Adaptación (13):** debe delimitarse frente a Copy, Variante y Versión (D-4).
- **Configuración (18):** la decisión de dónde se guarda (Local Storage o IndexedDB) es independiente de si es entidad.

## 4. Conceptos posiblemente faltantes
No encontré un concepto que tus instrucciones **exijan** y falte. Candidatos con evidencia débil, **sin proponer su incorporación**: «Reglas de copy» como familia propia (B l.385); «Texto legal» (B l.516) como contenido de Oferta; «pendientes» del Command Center (B l.314), derivables de estados. Esta conclusión se basa en búsqueda de texto; no verifiqué exhaustividad.

## 5. Dependencias conceptuales a resolver (orden sugerido, propuesta mía)
| ID | Pregunta | Afecta |
|---|---|---|
| D-1 | ¿Qué objetos son «contenido» auditable, versionable y aprobable (Copy, Variante, Pieza, Adaptación)? | 8, 9, 14, 15, 16 |
| D-2 | Variante frente a Versión: ¿alternativa simultánea frente a historial temporal? | 6, 14 |
| D-3 | Familias de reglas: reglas de copy, de marca, comerciales y de canal | 9, 10, 11, 12 |
| D-4 | Adaptación de canal: ¿produce un Copy, una Pieza o un registro propio? | 5, 7, 13 |
| D-5 | Aprobación: ¿registro de decisión o estado del contenido? | 14, 15, 19 |
| D-6 | Métrica: ¿definición, valor calculado o ambos? ¿«Calculado» en Resultado? | 16, 17 |
| D-7 | Configuración, Perfil local, tolerancias y canales: ¿qué vive dónde? | 11, 12, 18, Perfil |
| D-8 | Nombre canónico de la 16 | 16 |

## 6. Modificaciones que tocarían decisiones anteriores (todas pendientes de tu autorización expresa)
1. **Perfil local → componente de Configuración** (afecta P4.3). Justificación: un único campo opcional sin respaldo en A ni B.
2. Ninguna sobre 1–8, P4.1, P4.2, Q-7 ni F11-D5.

## 7. No verificado
Exhaustividad de conceptos (solo búsqueda de texto); las líneas de B citadas fuera de las ya presentadas se tomaron de lecturas por grep; consistencia de atributos/relaciones/fases de los documentos 05, 06 y 07, que siguen siendo propuestas mías.

> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; el texto original no se altera):** las propuestas y el diagnóstico de este documento siguen siendo antecedente histórico; las definiciones mínimas de las entidades 9–12 y 14–18 fueron aprobadas por la ratificación (18/18). Fuente y texto literal: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)». 
