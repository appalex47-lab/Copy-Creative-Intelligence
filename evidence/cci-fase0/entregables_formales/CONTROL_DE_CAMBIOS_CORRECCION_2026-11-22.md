# Control de cambios — corrección documental posterior a la publicación (2026-11-22)
Base: rama `evidence/cci-fase0-review`, HEAD previo `793d3197a9b506d518e5de339e472cf23ed76767`. Solo documentos del expediente; sin código, sin `main`. Ninguna de las 11 decisiones del paquete vigente se resuelve ni se aprueba por esta corrección. Los registros históricos no se reescriben: se añaden notas de actualización posterior.
**Decisión que sustenta las correcciones D5:** instrucción del propietario (corrección documental, 2026-11-22 ~12:58): D-5 resuelta; D5.a–d fuera del alcance vigente; no pendientes, no abiertas, no condicionan D-4 ni otras decisiones, no se vuelven a preguntar; no se aprueban individualmente.

| Archivo | Contradicción detectada | Corrección aplicada | Decisión o evidencia | Estado final |
|---|---|---|---|---|
| `entregables_formales/PAQUETE_DECISION_D4_D6_D7_D8.md` | D5.a–d «abiertas» (cabecera, §10); D4.d condicionaba D5.c (§7, §8); D4.d alternativa C y D4.a alternativa D mencionaban D5.c | Reescritas esas referencias; añadida «Base de evaluación» de D4.d (D-1, D-2, D-5.3); matriz §8 y orden lógico sin dependencia D4.d→D5.c; nota de corrección al inicio | Instrucción del propietario; D-5.2/5.3 en el registro | Corregido; las 11 decisiones siguen sin responder |
| `entregables_formales/INFORME_CIERRE_2026-11-22_PAQUETE_D4_D6_D7_D8.md` (12:35) | Registraba D5.a–d como pendientes | Texto original conservado; nota de actualización posterior y marcas en las líneas afectadas | ídem | Histórico con nota |
| `entregables_formales/INFORME_CIERRE_2026-11-22_REGLA_PERMANENTE_12_43.md` (12:43) | ídem | ídem | ídem | Histórico con nota |
| `00_INDICE_VIGENTES_E_HISTORICOS.md` | D5.a–d descritas como antecedente ambiguo; rutas sin carpeta; sin referencia a esta corrección; afirmaba que 05/06/07 «no están alineados» sin advertencia en ellos | Declara D5.a–d fuera del alcance; rutas completas; añade este control e informe; describe las advertencias en 05/06/07 | ídem | Corregido |
| `entregables_formales/DECISIONES_P4_PENDIENTES.md` | Actualización de 12:35 decía «D5.a–d abiertas»; otra línea listaba G2 (D5.a–d) como pendiente | Bloque «ESTADO VIGENTE» al inicio; línea de 12:35 corregida a «fuera del alcance»; línea G2 marcada superada; nueva actualización fechada | ídem | Corregido |
| `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` | Nota de 12:35 y registro de 12:29 mencionaban cuestiones abiertas | **No se modifican**; se añade nota fechada que fija la clasificación vigente | ídem | Histórico preservado |
| `entregables_formales/D5_APROBACION.md` | Lista «Siguen abiertas» sin aviso | Nota de actualización posterior al inicio | ídem | Histórico con nota |
| `entregables_formales/MATRIZ_CONSOLIDADA_18_ENTIDADES.md` | Aviso de 12:29: «cinco cuestiones abiertas» | Nota de actualización posterior (prevalece); estados de entidades sin cambios | ídem | Corregido |
| `entregables_formales/CATALOGO_DEPENDENCIAS_D4_D8.md` | D-5 descrita como la más cargada, hereda aprobabilidad | Nota de actualización posterior | ídem | Histórico con nota |
| `entregables_formales/PAQUETE_DECISION_D1_D8.md` | Presentaba G2 (D5.a–d) como decisiones y D4.d→D5.c | Texto original conservado (sustituido); nota de actualización posterior | ídem | Histórico con nota |
| `05_ARQUITECTURA_BROWSER_ONLY.md`, `06_MODELO_DE_DOMINIO.md`, `07_DISENO_PERSISTENCIA.md` | Propuestas históricas sin advertencia; `06` contiene fila genérica «Regla» | Advertencia de vigencia visible; en `06`, nota bajo la tabla: «Regla» no es entidad vigente | D-1, D-2, D-3, D-5, P1, P2, P3, P4.A | Corregido (contenido original intacto) |
| `entregables_formales/05_MODELO_DOMINIO_CCI.md`, `06_MODELO_DATOS_CCI.md`, `07_DISENO_PERSISTENCIA_INDEXEDDB.md` | ídem; `05` describe ReglaDeMarca como «de marca y de copy» | Advertencia de vigencia; en `05`, nota bajo la tabla: inclusión de reglas de copy no aprobada | D-3 | Corregido (contenido original intacto) |
| `README_ENTREGA.md`, `entregables_formales/16_INDICE_EVIDENCIAS_FASE0.md` | No listaban esta corrección | Líneas añadidas | — | Corregido |
| `MANIFEST.sha256`, `INVENTARIO_PUBLICADO.sha256` | Hashes desactualizados | Regenerados | — | Regenerados |

## Contradicciones que permanecen y motivo
- Ninguna sobre D5.a–d en documentos **vigentes**. Permanecen, como antecedente con nota, en los informes de 12:35 y 12:43, `PAQUETE_DECISION_D1_D8.md`, `D5_APROBACION.md` y las notas fechadas de `REGISTRO_DECISIONES_RESUELTAS.md` (no se reescribe la cronología).
- Los documentos 05/06/07 conservan sus propuestas (relaciones, atributos, stores, MVP): siguen **sin aprobar**; no se alinearon porque no se autorizó reescribirlos ni inventar decisiones.
- Las celdas antiguas de la matriz consolidada siguen sin reescribirse; prevalecen los avisos.
