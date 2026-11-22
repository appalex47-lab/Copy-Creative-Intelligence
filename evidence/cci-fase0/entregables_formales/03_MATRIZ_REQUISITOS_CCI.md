# Matriz de requisitos de CCI

> Documento formal del §14. Fuente de contenido: `../04_MATRIZ_REQUISITOS.md` (sin cambios de fondo). Estado: propuesta para revisión; nada aprobado ni implementado.

Nota: los IDs R-001…R-062 son no contiguos por agrupación por fase (45 filas).
Origen: instrucción maestra (secciones entre paréntesis). Estado de pruebas de todas las filas: **definida, no ejecutada** (ninguna existe aún salvo las de la infraestructura, `02_INVENTARIO_FUNCIONAL_CCI.md`). Tipos: U unitaria · R repositorio · P persistencia real en navegador · M migración · E E2E · A accesibilidad · X exportación/importación · F fallo/recuperación · D rendimiento.
| REQ | Requisito | Fase | Criterio | Pruebas |
|---|---|---|---|---|
| R-001 | Aplicación local, un usuario por navegador, sin cuentas/login/backend (§1.1) | 1 | AC1-01 | prueba de arquitectura: sin `fetch`/SDK de servidor; E |
| R-002 | TypeScript estricto, estructura modular (§4) | 1 | AC1-02 | typecheck, lint |
| R-003 | Diseño visual y navegación entre módulos (§4) | 1 | AC1-03 | E, A |
| R-004 | Componentes reutilizables (§4) | 1 | AC1-04 | U, A |
| R-005 | Modelo de dominio inicial aprobado (§4, P4) | 1 | AC1-05 | U |
| R-006 | IndexedDB con repositorios; la UI no accede directamente (§3C, §4) | 1 | AC1-06 | R, P, arquitectura |
| R-007 | Migraciones locales versionadas (§4) | 1 | AC1-07 | M |
| R-008 | Manejo centralizado de errores (§4) | 1 | AC1-08 | U, F |
| R-009 | Preferencias ligeras en Local Storage (no base paralela) (§3E, §4) | 1 | AC1-09 | U, P |
| R-010 | Mostrar estado real del almacenamiento (§4) | 1 | AC1-10 | E, P |
| R-011 | Command Center con datos reales, pendientes y actividad real; sin datos ficticios como operativos (§4) | 1 | AC1-11 | E |
| R-012 | Recarga conserva datos; recuperación ante errores (§4) | 1 | AC1-12 | P, E, F |
| R-013 | Responsive y accesibilidad (§4) | 1 | AC1-13 | E, A |
| R-014 *(propuesto a partir de P1)* | Perfil local opcional sin identidad autenticada; sin organización, membresía ni roles (P1) | 1 | AC1-14 | U, arquitectura, E |
| R-020 | Brief: campaña, objetivo, producto, audiencia, oferta, beneficio, vigencia, condiciones, tono, mensaje, canal, formato, CTA (§5) | 2 | AC2-01 | U, E |
| R-021 | Briefs incompletos se detectan y se explican (§5) | 2 | AC2-02 | U |
| R-022 | Generación de titulares, textos, descripciones, CTA, variantes, tonos, objetivos, A/B según alternativa IA aprobada (§5, P8) | 2 | AC2-03 | U, F |
| R-023 | Editor: crear, editar, duplicar, comparar, guardar, recuperar, etiquetar, buscar, exportar, historial (§5) | 2 | AC2-04 | U, P, E |
| R-024 | Reglas de copy deterministas: longitud, ortografía, obligatorias, prohibidas, consistencia, tono, CTA, formato — ejecutadas en código (§5) | 2 | AC2-05 | U |
| R-025 | La IA no sustituye la validación comercial; fallos de IA no bloquean lo local (§5) | 2 | AC2-06 | F |
| R-026 | Copys y variantes persistentes con versiones (§5, §1.2) | 2 | AC2-07 | R, P, M |
| R-027 | Exportación de copys (§5) | 2 | AC2-08 | X |
| R-030 | Auditoría de copy: claridad, ortografía, legibilidad, tono, consistencia, coherencia con brief, CTA, marca, afirmaciones no respaldadas, riesgos (§6) | 3 | AC3-01 | U |
| R-031 | Auditoría visual: legibilidad, contraste, jerarquía, distribución, marca, elementos obligatorios, congruencia copy-pieza, formato (§6) | 3 | AC3-02 | U (cálculo determinista), manual para lo no determinista |
| R-032 | Hallazgo con id, elemento, evidencia, categoría, severidad, regla, recomendación, estado, resolución (§6) | 3 | AC3-03 | U, P |
| R-033 | Puntuación explicable, determinista, con ponderaciones documentadas (§6, Q-5) | 3 | AC3-04 | U |
| R-034 | La IA puede sugerir hallazgos, no modificar puntuaciones ni reglas (§6) | 3 | AC3-05 | U |
| R-035 | Corregir, reauditar, comparar versiones, conservar historial, documentar pendientes (§6) | 3 | AC3-06 | U, P, E |
| R-036 | Imágenes inválidas y archivos no compatibles se rechazan con mensaje (§6) | 3 | AC3-07 | U, F |
| R-040 | Validar precio original, promocional, descuento, vigencia, restricciones, productos, exclusiones, condiciones, texto legal, coherencia oferta-copy (§7) | 4 | AC4-01 | U |
| R-041 | Descuento (%) = ((Precio original − Precio promocional) / Precio original) × 100; redondeo y tolerancias configurables (§7, Q-1) | 4 | AC4-02 | U |
| R-042 | Distinguir error comprobado, inconsistencia, información faltante, no verificable, advertencia, bloqueo justificado (§7) | 4 | AC4-03 | U |
| R-043 | No inventar información comercial (§7, §1.2) | 4 | AC4-04 | U |
| R-044 | Adaptaciones a canales aprobados con reglas de longitud, estructura, formato, tono, CTA, restricciones, elementos obligatorios (§7, Q-2) | 4 | AC4-05 | U, E |
| R-045 | Trazabilidad: copy fuente, canal, adaptación, versión, reglas, diferencias, estado de revisión (§7) | 4 | AC4-06 | R, P |
| R-050 | Biblioteca: campañas, copys, piezas, búsqueda, filtros, etiquetas, versiones, auditorías, reutilización (§8) | 5 | AC5-01 | E, P |
| R-051 | Workflow con estados aprobados; sin usuarios, permisos ni aprobaciones multiusuario simulados (§8, Q-3) | 5 | AC5-02 | U, E |
| R-052 | Aprobación final humana; ninguna aprobación automática por IA (§1.2, §8) | 5 | AC5-03 | U, E |
| R-053 | Versionado: historial, comparación, fecha, cambios, estado, auditorías vinculadas, motivos; no sobrescribir contenido aprobado (§8) | 5 | AC5-04 | U, P |
| R-054 | Performance Intelligence con datos manuales/importados/calculados; fórmulas documentadas; no mostrar indicadores sin datos (§8) | 5 | AC5-05 | U, E |
| R-055 | Exportación completa y selectiva, importación, validación, integridad, compatibilidad, confirmación de reemplazo, restauración segura, recuperación; sin restauraciones parciales (§8) | 5 | AC5-06 | X, F |
| R-056 | Flujo integrado Brief → Copy → Auditor → Validator → Adaptación → Revisión humana → Biblioteca → Performance (§8) | 5 | AC5-07 | E |
| R-057 | Calidad final: regresión, E2E, accesibilidad, responsive, rendimiento, persistencia, recuperación, seguridad local, compatibilidad, documentación, manuales (§8) | 5 | AC5-08 | todas |
| R-060 | Datos comerciales no inventados; hallazgos explicables; limitaciones comunicadas (§1.2) | todas | transversal | revisión + U |
| R-061 | No exponer claves; no guardar secretos en Local Storage/IndexedDB (§3F) | todas | transversal | `check-secrets`, arquitectura |
| R-062 | Reportar pruebas con estado exacto (definida/ejecutada/aprobada/fallida/bloqueada/no ejecutada) (§9) | todas | transversal | informes |
