# DICTAMEN DE PREPARACIÓN DE FASE 0 (CCI)

**Naturaleza:** dictamen técnico documental del revisor. **No es** aceptación formal de Fase 0, **no** firma la Adenda v9 y **no** autoriza Fase 1. Esas decisiones son exclusivas del propietario.

## Veredicto global: PREPARADO_CON_LIMITACIONES

No se emite PREPARADO_DOCUMENTALMENTE porque subsisten limitaciones que no son defectos corregibles aquí (físicas y de aprobación, ver abajo). Ningún defecto corregible dentro del alcance queda abierto: el defecto del script R1–R9 (falso PASS) está corregido y su corrección probada.

## 1. Resuelto técnicamente (con evidencia local)
- Base V20 reproducida en PostgreSQL 16.15 temporal (UTF8): 63/63 pruebas, 14/14 mutaciones. Extensión local: 80/80.
- Concurrencia local CC-01/CC-02 PASS; hash de referencia 16/16; revisión estática T-47/T-124: 10 PASS + 2 SIN_DATOS; DG-19 experimento 63/63.
- 12 escenarios PARCIAL reevaluados: 5 PASS_PROTOTYPE, 1 PASS_STATIC, 6 PARTIAL (ninguno es aceptación física).
- T-409..T-422: 26 variantes individuales detectadas en modelo; la relación con K47-Mxx concretas es inferida (separada de la demostrada).
- 22 funciones: 366 evaluaciones (354 fixtures distintos), 0 fallos, 0 defectos funcionales (DEF-F01..F06 clasificados).
- Script `04_trigger_r1_r9` v2: arnés con clasificador de errores; 28/28 autopruebas; se reproduce el defecto de v1 (11 falsos PASS). Los seis scripts CCI-DEV (v2) pasan el escáner estático (0 FAIL; totales en `INFORME_CIFRAS_DEFINITIVAS.md`) y el smoke local con aserciones de contenido.
- 21 decisiones con recomendación técnica, alternativas, impacto y pruebas.

## 2. Documentado pero NO validado físicamente
Esquema de 41 tablas, RLS, privilegios, triggers R1–R9, SECURITY DEFINER, concurrencia CONC-03..06, K47 físico: todo preparado como plan y scripts **NO EJECUTADOS**. La lógica R1–R9 es **NO VERIFICABLE EN ENTORNO FÍSICO**.

## 3. Requiere CCI-DEV
Ejecución de los scripts 01–05 con autorización; versión y extensiones de Supabase; `auth.uid()` y roles reales; RLS-06.

## 4. Requiere aprobación del propietario
G-1, G-5, G-10, DG-19, DG-20, DG-12, DG-16, DG-18, G-9, RP-01, P-01..P-05, P-10, PO-05, DG-09, DEP-RET-01, OD-13 (y HV-02). Ninguna está aprobada; el registro tiene 21 filas, todas `REQUIERE_APROBACION_DEL_PROPIETARIO`. Además: contrato de error de R1–R9 (BRECHA-R1R9-01).

## 5. No pudo verificarse
Texto de la Adenda v9 y de OD-13 (fuera del expediente); que PO-05 apunte a la v9 (HV-02); valores reales de canales/formatos (DG-19); política de retención; responsables reales; infraestructura Supabase; que una guarda distinga DEV de PROD (LR-22).

## 6. Qué impide la aceptación formal de Fase 0
Decisiones sin aprobar; validación física pendiente; 5 controles NO VERIFICADO y 4 PARCIAL heredados de V26; dependencias externas (Adenda v9, OD-13, catálogo real). Ver `MATRIZ_LIMITACIONES_RESIDUALES.csv` (27 filas; la LR-28 se fusionó con la LR-05, ver `INFORME_CIFRAS_DEFINITIVAS.md`).

## 7. Condiciones antes de considerar Fase 1 (a decidir por el propietario)
Aprobación de las decisiones de la sección 4; confirmación del proyecto CCI-DEV (P1); ejecución y resultado de E2–E8 del plan; definición del contrato de error de R1–R9; entrega de los datos externos. Este dictamen **no** autoriza Fase 1.

## Límite
La evidencia es local (PostgreSQL temporal, modelo en memoria, prototipos, shim). No equivale a Supabase. Trazabilidad: `MATRIZ_TRAZABILIDAD_MAESTRA.csv`. Reconciliación: `INFORME_RECONCILIACION_INTEGRAL.md`.
