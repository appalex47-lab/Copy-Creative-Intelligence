# INFORME DE CIERRE TÉCNICO DE FASE 0 — CCI

Complementario a V26; no reinicia la auditoría. Sin commit/push/merge; sin operaciones en Supabase.

## 1. Alcance y método
Revisión local sobre PostgreSQL 16.15 temporal (clúster UTF8 autoritativo; SQL_ASCII sólo contraste) y el modelo K47 en memoria, con el fixture V20 sin modificar. Herramientas protegidas (`modelo_estructural.py`, `verificar_expediente.py`) sin cambios.

## 2. Resultados de las corridas locales
| Corrida | Resultado |
|---|---|
| Base V20 (UTF8) | 63/63; mutaciones 14/14 |
| Extensión local (UTF8) | 80/80 (SQL_ASCII 77/80: 3 fallos multibyte por codificación, DEF-ENV-01) |
| Concurrencia CC-01/CC-02 | PASS |
| Hash encadenado de referencia | 16/16 (incluye pgcrypto) |
| Revisión estática T-47/T-124 | 10 PASS, 2 SIN_DATOS |
| K47 por escenario | 25/25 detectadas (mapeo = inferencia del revisor) |
| 22 funciones | 366 casos, 0 fallos |
| Experimento PK DG-19 | 63/63 |

## 3. Escenarios PARCIAL (12)
6 PASS a nivel modelo/prototipo (T-03, T-47, T-137..T-140) y 6 PARTIAL (T-06, T-10, T-78, T-80, T-124, T-166). Ver MATRIZ_12_ESCENARIOS_PARCIALES.csv.

## 4. T-409..T-422 y 22 funciones
14 dossiers con nivel MODELO_EN_MEMORIA. 22 funciones revisadas; defectos DEF-F01..F05 sin efecto en resultados.

## 5. Modelo lógico/físico
41 tablas; 28 sin prueba física; el fixture V20 no tiene RLS ni roles. Ver MATRIZ_MODELO_LOGICO_FISICO.md.

## 6. Paquete CCI-DEV
Scripts 01–05 preparados y **no ejecutados** (01/02 sólo smoke local; 03 sobre shim local; 04 plantilla sin probar).

## 7. Hallazgos nuevos
DEF-01 (btrim «no vacío»), DEF-DG12-01 (concat_ws ambiguo), DEF-DG19-01 (normalización débil), DEF-NAME-01 (`approver` vs `decided_by`), DEF-ENV-01 (codificación local). Ninguno modifica resultados de V26.

## 8. Decisiones
21 decisiones con recomendación; todas `REQUIERE_APROBACION_DEL_PROPIETARIO`. DG-20: el análisis respalda mantener la ampliación mínima, **sin marcarla aprobada**.

## 9. Revisión de calidad de V26 (§11)
Sin contradicciones nuevas respecto a las cifras de Fase 0 (231 reglas, 780 escenarios, 22 funciones/366 casos, 41 tablas, 17 claves, 13 transiciones). Persisten las limitaciones heredadas (LR-01..LR-03). La discrepancia «12 tablas» se aclara en la matriz del modelo (LR-18).

## 10. Verificaciones finales (§15)
Pruebas locales reejecutadas (ver §2); SHA-256 en el manifiesto; V26 sigue en `439777c9…`; `git status` sólo muestra esta carpeta; ningún script se ejecutó contra Supabase; ningún PASS sin evidencia; ninguna decisión marcada como aprobada.

## A. RESUELTO TÉCNICAMENTE
Línea base reproducida; prototipos locales de DG-16/18/19/20, G-9, DG-12; reclasificación de 12 escenarios; dossiers T-409..T-422; revisión de 22 funciones; paquete CCI-DEV preparado.

## B. RECOMENDADO PARA APROBACIÓN
G-1, G-5, G-10, DG-19 (PK natural + normalización), DG-20, DG-12 (formato canónico), DG-16, DG-18, G-9, RP-01 (perfil), P-02, PO-05 (tras revisar la Adenda v9).

## C. PENDIENTE DEL PROPIETARIO
Aprobar las decisiones de B; DG-09 y DEP-RET-01 (política y procedimiento); P-01, P-03, P-04, P-05, P-10; entrega de la Adenda v9/OD-13; confirmar PO-05=v9 (HV-02); designar RP-01; catálogo real de canales y formatos (DG-19); umbrales 30/10 (DG-16).

## D. PENDIENTE DE CCI-DEV
Inventario de esquema, RLS y privilegios, triggers R1–R9, concurrencia CONC-03..06, K47 físico, funciones en base real, versión/extensiones de Supabase.

## Veredicto global: PREPARADO_CON_LIMITACIONES
Fase 0 **no** queda aceptada ni Fase 1 autorizada por este informe.
