# 07 — Limitaciones y lo no verificado

- **Fase 0 no está aprobada**: ninguna conclusión valida contra un diseño cerrado.
- **Lectura parcial**: la especificación F3 (937 KB) no se leyó íntegra; se leyeron los pasajes citados y los resultados de búsquedas por palabra clave. Las matrices CSV de Fase 0 (escenarios, trazabilidad maestra, 231 reglas) no se leyeron.
- **Columnas**: ni F2 ni F3 definen columnas de `profiles`, `organizations`, `memberships`; solo el fixture (11 tablas, PostgreSQL 16.15 temporal) aporta `activo`/PK compuesta, y no es equivalente a Supabase.
- **Permisos**: se verificó la lista de 17 en F2 y su presencia parcial en F3; la correspondencia permiso→rol solo se leyó en F2. No se verificó si `audit.image`, `audit.text`, `copy.analyze`, `copy.compare`, `copy.generate` (aparecen en F2) son permisos o nombres de función.
- **13 transiciones (T-02)**: no verificadas.
- **Aprobaciones**: no existe fuente primaria localizada de las «decisiones expresas aprobadas» (D-01…D-08); se tratan como declaradas.
- **Sin PostgreSQL ni Supabase**: nada se ejecutó; no hay validación contra base real (PG17 ausente; evidencia CCI-DEV del administrador, no verificada).
- Las claves de rol `diseno` y `revisor_aprobador` provienen de una sola línea de F2 (l.424); podrían ser etiquetas y no identificadores físicos.
- Los recuentos de este expediente se hicieron por script y a mano sobre texto Markdown; una tabla mal formateada podría haberse omitido (el cruce 27/41 dio conjuntos idénticos, lo que reduce ese riesgo pero no lo elimina).
- Entorno: todo vive en el espacio temporal; los respaldos entregados son la copia duradera.
