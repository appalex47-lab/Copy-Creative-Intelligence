# INFORME FINAL V21 — CIERRE DOCUMENTAL Y VALIDACIÓN INTEGRAL DE FASE 0

**Versión:** V21 · **Fecha:** 2026-11-20 · **Fuente:** `REPORTE_VALIDACION_INTEGRAL_V21.md`, `MATRIZ_CONCILIACION_V21.md`, `REGISTRO_CAMBIOS_V20_V21.md`, salidas de `salidas/` · **Estado de verificación:** ejecutado; todo resultado citado procede de una salida archivada. V21 es la última intervención técnica de conciliación documental de Fase 0: **no** es aceptación de G-1/G-5/G-10, ni inicio de Fase 1, ni validación de infraestructura real, ni autorización para modificar Supabase, fusionar ramas o publicar en producción.

## 1. Estado de partida y de llegada
- Rama `audit/fase0-v19-review`; HEAD de partida y base: `ac84133b776cc73c0cb3416e51e2767039bb5132` (V20). `main` en `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`, sin cambio (local y `git ls-remote`).
- Árbol de partida limpio, sin modificaciones ajenas. Todo el trabajo V21 está en el árbol local, **sin commit ni push** (no autorizados todavía).

## 2. Qué se corrigió
Once defectos documentales (detalle en `REGISTRO_CAMBIOS_V20_V21.md`, D-01 a D-11), entre ellos: el inventario de decisiones conservaba la distribución anterior de clases (B 3, E 5) frente a la vigente A 1, B 8, C 69, D 153, E 0; la descripción de DG-20; los números de línea a la especificación de las matrices de 231 reglas (198 filas), 780 escenarios (780 filas), 90 citas de narrativa y cuatro documentos V20; el bloque de estado de los cinco documentos activos (decía que V20 no estaba publicado); y la falta de avisos de sustitución/histórico en documentos V20 y V16–V19.

## 3. Qué se verificó y qué se volvió a ejecutar
- **Cifras centrales** recomputadas desde la evidencia primaria (`MATRIZ_CONCILIACION_V21.md`): 231 reglas, 780 escenarios, 41 tablas (27 + 14), 22 funciones, 366 casos, 63 pruebas y 14 mutaciones PostgreSQL, 59 comprobaciones / 28 controles / 300 mutaciones del verificador. Todas las cifras declaradas en V20 coinciden con la evidencia; **363 vs 366 queda resuelto**: 366 = 363 + 3 positivos de K45 que el script V18 imprimía pero no contaba.
- **Reejecutado en V21**: 22 funciones (tercera corrida, idéntica a las dos de V20); PostgreSQL 16.15 temporal (`initdb` en `/tmp`, socket Unix; 63/63 PASS y 14/14 mutaciones detectadas, idénticas a V20; clúster eliminado al terminar); verificador completo ×2 en copias limpias, 59/59, 28/28 y 300/300, con salidas idénticas entre sí y a V20 (`salidas/salida_verificador_V21_corrida1.txt`, `…corrida2.txt`).
- **Batería de cierre V21** (`scripts/v21_bateria_cierre.py`): estructural, semántica, de referencias, de conteos, de vigencia y de ausencia de cambios funcionales, con registro de identificador, objetivo, entrada, esperado, obtenido, PASS/FAIL/BLOCKED, evidencia y observaciones; dos corridas. Resultados: `REPORTE_VALIDACION_INTEGRAL_V21.md`.
- **Controles negativos** (`scripts/v21_controles_negativos.py`): 25 defectos inyectados en copias del repositorio; cada uno debe hacer fallar su prueba. Resultado en `salidas/salida_controles_negativos_V21.txt`.
- **Integridad**: manifiesto `MANIFIESTO_EVIDENCIAS_SHA256_V21.txt` verificado por dos métodos independientes (hashlib y `sha256sum -c`), más comprobaciones estructurales y de regenerabilidad; salidas `salidas/salida_integridad_V21_corrida1.txt` y `…corrida2.txt`.

## 4. Conciliación de las 231 reglas
A 1 · B 8 · C 69 · D 153 · E 0 = 231, idéntica en la matriz, el inventario, los informes V20/V21 y la matriz de conciliación; derivada de forma independiente por V21-A02. Las cinco reglas reclasificadas (IG1-05, IG1-06, IG1-10, IG1-21, IG5-36) pasaron de E a B por su ejecución en el fixture de PostgreSQL temporal: **no** significa implementadas en el producto ni aceptadas. La trazabilidad V18 → V19 → V20 → V21 está en `MATRIZ_CONCILIACION_V21.md`.

## 5. Defectos del motor
Ninguno detectado. Observación sobre el verificador protegido: sus 59 comprobaciones son 58 numeradas (K01..K59 sin K43) más `K55-V12`; no afecta a ningún resultado (detalle en `REGISTRO_CAMBIOS_V20_V21.md`). El motor (22 funciones), el verificador, `historico/`, la v3.3 y las salidas originales no se modificaron (SHA-256 y diff comprobados).

## 6. Limitaciones que permanecen (externas, no defectos documentales)
Sin esquema físico ni CCI-DEV: no se validó RLS, privilegios, concurrencia real, Supabase/Storage ni PE-01..PE-05 contra el esquema real; el PostgreSQL temporal **no equivale** al esquema físico aprobado de CCI ni a una validación de Supabase. El trigger de elegibilidad R1–R9 no se ejecutó (requiere 12 tablas más). 12 escenarios PARCIAL; T-409..T-422 sin ejecución individual propia. Las 22 funciones no se leyeron línea a línea (evidencia indirecta: mutaciones e independencia del auditor).

## 7. Decisiones que requieren al propietario
Ver `REGISTRO_DECISIONES_ABIERTAS_V21.md`: PO-05 / HV-02 (confirmar que se refiere a la Adenda v9; NO VERIFICABLE sin esa confirmación); aceptación de G-1, G-5 y G-10; DG-19 y la clave primaria de `channel_formats`; DG-20; DG-09, DG-12, DG-16, DG-18, DEP-RET-01; G-9; RP-01; P-01..P-05 y P-10; OD-13. V21 no creó ninguna decisión nueva ni marcó ninguna como aprobada.

## 8. Condiciones para la aceptación formal
1. Decisión expresa del propietario sobre cada punto del registro de decisiones (en particular PO-05/Adenda v9 y G-1/G-5/G-10).
2. Autorización expresa para crear el esquema físico y validar en **CCI-DEV** (proyecto propio de CCI; nunca proyectos de RevNavigator): repetir PE-01..PE-05 y los 12 escenarios PARCIAL contra el esquema real, y validar RLS, privilegios y concurrencia.
3. Evidencia archivada de esa validación antes de considerar cualquier promoción a **CCI-PROD**.
4. Autorización expresa para publicar V21 (commit/push) si el propietario lo desea.

## 9. Actividades que siguen prohibidas o no autorizadas
Modificar `main`; fusionar ramas; Fase 1 (NO INICIADA, NO AUTORIZADA); implementar G-1, G-5 o G-10; modificar el motor o el comportamiento del producto; crear o modificar proyectos Supabase; ejecutar migraciones contra CCI-DEV o CCI-PROD; reutilizar proyectos de RevNavigator; publicar en producción; commit, merge o push de V21 sin autorización expresa.
