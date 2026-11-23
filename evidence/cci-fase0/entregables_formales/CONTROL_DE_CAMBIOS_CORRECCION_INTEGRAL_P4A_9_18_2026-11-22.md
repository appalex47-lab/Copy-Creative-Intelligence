# Control de cambios — Corrección integral y cierre de regularización P4.A 9/18 (2026-11-22)
**Commit base:** `74486fa8cad79093cc7286c3c6ecf7da36d70d34` (HEAD real verificado antes de editar; sin cambios posteriores). **Rama:** `evidence/cci-fase0-review`. Autoridad: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`. Las 11 decisiones D4/D6/D7/D8 no se modifican.

## 1. Los cuatro hallazgos
| # | Archivo | Corrección | Fundamento |
|---|---|---|---|
| 1 | DECISIONES_P4_PENDIENTES.md | P4.D / Q-7 marcada **resuelta → (a)**, P4.4 cerrada, sin respuestas pendientes; planteamiento original conservado como antecedente; alcance de Q-7 sin ampliar (solo existencia de Campaña) | Registro, sección Q-7 |
| 2 | MATRIZ_CONSOLIDADA_18_ENTIDADES.md | Fila 13: columna de definición = texto **literal** de D4.c copiado programáticamente del registro; propuesta anterior como antecedente; estado «Aprobada — definición mínima», fundamento D4.c=A; notas de encabezado alineadas | Registro, bloque D4.c |
| 3 | RONDA_UNICA_…_MATRIZ_CONSOLIDADA.md | Nota de **antecedente superado** inmediatamente antes de «Estado: propuesta consolidada…» y antes de «Cómo responder»; marcador en la línea P4.A 8/18 | Registro, 11 selecciones |
| 4 | 16_INDICE_EVIDENCIAS_FASE0.md | D1, D2, D3 y D5: estado histórico / vigente / documento autoritativo (D5.a–d fuera de alcance); Q-7; DECISIONES_P4_PENDIENTES | Registro, D-1, D-2, D-3, D-5 |
| + | REGISTRO_DECISIONES_RESUELTAS.md | Nota fechada: D4.d respondida con A (límites M-1/D-5.3) supera la nota histórica de D-5.2; texto de decisiones intacto (solo se añade) | D4.d, D-5.3 |

## 2. Auditoría cruzada realizada (búsqueda de texto + lectura de contexto en `evidence/cci-fase0/`)
Patrones: «pendiente de decisión», «sin responder», «siguen pendientes», «PENDIENTE», «8/18», «10/18», D-4…D-8, D4./D6./D7., P4.D, Q-7, Supabase/backend/PostgreSQL, «Fase 0 aceptada», «Fase 1 autorizada». Resultado: los estados obsoletos hallados eran informes o análisis fechados; se conservaron y recibieron nota fechada (no hubo reemplazos globales):
| Archivo | Hallazgo | Acción |
|---|---|---|
| INFORME_CIERRE_…PAQUETE_D4_D6_D7_D8, …REGLA_PERMANENTE_12_43, …CORRECCION_DOCUMENTAL | 8/18 y D-4…D-8 pendientes (estado a su hora) | Nota fechada |
| D3_FAMILIAS_DE_REGLAS.md | Cuadro §8: 8/18, D-1…D-8 2/8 | Nota fechada |
| MATRIZ_DECISIONES_PROPIETARIO.md | «Ninguna está respondida» | Nota fechada |
| APROBACIONES_FASE0.md | 0.3 con Q-7 y P4 parcial | Nota fechada: todas siguen PENDIENTES |
| FICHA_P4.md | «P4.4 aplazado a Q-7» | Nota fechada |
Sin hallazgo (sin cambio): 00_INDICE y README (ya con registro autoritativo, 9/18, matriz respondida), CATALOGO_DEPENDENCIAS_D4_D8 y DECISIONES_P4_PENDIENTES (corregidos en la regularización previa), docs 05/06/07 (ya con advertencia de vigencia), FICHA_Q7 (ya marcada resuelta), 10/13 registros (Q-7 ya resuelta). Menciones a Supabase/backend en índice/README: solo en la revisión de seguridad, no como arquitectura vigente. No se encontró texto que dé por aceptada Fase 0 ni por autorizada Fase 1.

## 3. Estados que permanecen abiertos (sin resolver aquí)
P4.B, P4.C, P4.E (E1–E5), Q-1, Q-2, C-2, C-3; entidad 9 suspendida; entidades 10–12 y 14–18 sin aprobación vigente; aprobaciones 0.1–0.7; aceptación formal de Fase 0; Fase 1 no autorizada; en D6.c=A0: origen del valor (manual/importado/calculado), L1, L2, L3 sin decidir y A0 no aprueba D6.b=A. D5.a–d fuera de alcance (no reabiertas). P4.A: **9/18 (50 %)**. *[Antecedente superado por la ratificación 15:56: la entidad 9 ya no está suspendida y las entidades 10–12 y 14–18 tienen definición mínima aprobada.]*

## 4. Históricos preservados
Todos los registros y análisis originales (D1, D2, D3, D5 originales, fichas, paquetes, informes anteriores, `docs/fase0`): solo se añadieron notas fechadas; no se eliminó ni reescribió texto.
## 5. Limitaciones
Verificación por búsqueda de texto y lectura de contexto, no lectura línea a línea de los 52 documentos de `docs/fase0` ni de todos los anexos; la arquitectura browser-only se comprobó por coincidencia de texto en índice/README; sin pruebas, build ni CI de la aplicación; acceso de ChatGPT no verificado.

> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; el texto original no se altera):** este control de cambios es un registro histórico: el conteo P4.A 9/18 y la suspensión de la entidad 9 que menciona están **superados** (P4.A vigente: 18/18). Fuente: `REGISTRO_DECISIONES_RESUELTAS.md`, sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)».
