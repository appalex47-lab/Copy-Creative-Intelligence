# INFORME DE CORRECCIONES V24

**Alcance:** corrección documental puntual de las observaciones OBS-01, OBS-02 y OBS-03 de la revisión independiente de V23. No se repitió la auditoría de Fase 0 ni se modificaron pruebas, resultados, reglas, clasificaciones, decisiones ni evidencias técnicas. **La publicación no representa aceptación formal de Fase 0**; esa aceptación corresponde exclusivamente al propietario.

## 1. Matriz de observaciones
| Observación | Corrección | Evidencia | Estado |
|---|---|---|---|
| OBS-01 | Identificación diferenciada: expediente **V21** (sin cambio retroactivo), corrección documental del paquete **V23**, revisión documental actual **V24**; relación explicada en §1 del LEEME (el empaquetado inicial fue V22) | `00_LEEME/LEEME_EXPEDIENTE_V21.md` §1 y §2 | PASS |
| OBS-02 | Las declaraciones de los apartados 3 y 15 se conservan como registro histórico y llevan una nota que aclara: describen el estado al generar V21/V23; V23 se publicó después en `audit/fase0-v23-review`; no es aceptación formal; sin merge ni cambios en `main` | LEEME §3 y §15 | PASS |
| OBS-03 | Los documentos de limitaciones de V23 (`07_…/00_ESTADOS_DE_VERIFICACION_Y_LIMITACIONES.md`, `INFORME_FINAL_V21.md`) **ya contenían** correctamente cada limitación, por lo que **no se modificaron**. Se amplió solo el LEEME §13 para que sea autónomo: pruebas sobre fixture temporal ≠ validación física en CCI-DEV, con las 7 limitaciones enumeradas | LEEME §13; `07_…` e `INFORME_FINAL_V21.md` sin cambio | PASS |

## 2. Limitaciones que se conservan (sin convertirlas en PASS)
PostgreSQL temporal: 63/63 pruebas y 14/14 mutaciones según la evidencia existente (fixture, no esquema aprobado); 12 escenarios PARCIAL; T-409 a T-422 sin ejecución individual propia; 22 funciones validadas indirectamente por ejecución, no por lectura línea por línea; sin validación física en CCI-DEV; sin validar RLS, privilegios, concurrencia real ni esquema físico aprobado; trigger R1–R9 no ejecutado; HV-02 / PO-05 sin verificación. Decisiones pendientes del propietario: PO-05, G-1, G-5, G-10, DG-19, DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10, OD-13.

## 3. Archivos modificados y conservados (V23 → V24)
Dentro de `docs/fase0/expediente_final_v24/` (copia autónoma del expediente V23; `expediente_final_v23/` no se tocó):
| Archivo | SHA-256 antes (V23) | SHA-256 después (V24) |
|---|---|---|
| `00_LEEME/LEEME_EXPEDIENTE_V21.md` | `9e8a6f41a5e5d5d1a2fa299eba84d4a6dc6fbdbc846b223b64b67c79fc68fc26` | `815ca814e11dca35729199c00a6225aa5f39249106e47d346188c1c7b08313fd` |
| `08_INTEGRIDAD_Y_MANIFIESTOS/SHA256SUMS.txt` (manifiesto interno regenerado por el cambio del LEEME; 252 entradas, sin incluirse a sí mismo) | `ab83883f94c49a8e299e955b2e5f07a9b19f1213ac63acde9c58a44b80ec53e4` | `e182a66f58dab6fecfea107a4fa1376fba2a997789ce50ef9f61d79387e947d3` |

- **Conservados con el mismo SHA-256 que en V23:** los otros 251 archivos (incluidos los 9 documentos principales, 6 scripts V21, 11 evidencias V21, resultados, matrices, diff y documentos de limitaciones). El inventario completo previo a la modificación (253 hashes) se tomó antes de editar y está reflejado en `MANIFIESTO_SHA256_V24.txt`.
- **Nuevos de V24** (en `docs/fase0/expediente_final_v24/`): `INFORME_CORRECCIONES_V24.md`, `MATRIZ_OBSERVACIONES_V23_V24.md`, `REPORTE_VALIDACION_V24.md`, `MANIFIESTO_SHA256_V24.txt` (hashes de todos los archivos de V24 salvo él mismo).
- Reproducir la diferencia: `diff -r docs/fase0/expediente_final_v23 docs/fase0/expediente_final_v24` (solo esos dos archivos difieren, más los 4 nuevos).

## 4. Pruebas realizadas
Ver `REPORTE_VALIDACION_V24.md`. No se repitieron las 46 pruebas V21, los 26 controles negativos ni PostgreSQL; se verificó que sus resultados originales permanecen idénticos (mismo SHA-256 de cada archivo de resultados).

## 5. Referencias (SHA y URLs)
- Origen de V24: commit `8674114c69881ff1ebda3c5db1f89f2a4d6d31c6` (rama V23, `audit/fase0-v23-review`); commit del expediente V23: `8be8acecffce64e2a4660383bc8d5306a303c9c1`.
- V20 (`audit/fase0-v19-review`): `ac84133b776cc73c0cb3416e51e2767039bb5132`. `main`: `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`.
- SHA del commit V24 y verificación remota: un archivo no puede contener el SHA de su propio commit; constan en `../REPORTE_PUBLICACION_V24_GITHUB.md` (verificado directamente en GitHub).
- Rama de publicación: `audit/fase0-v24-review`. Documentos: `https://github.com/appalex47-lab/Copy-Creative-Intelligence/blob/audit/fase0-v24-review/docs/fase0/expediente_final_v24/` + nombre de archivo.

## 6. Observaciones adicionales (registradas, sin ampliar alcance)
1. El LEEME conserva el nombre `LEEME_EXPEDIENTE_V21.md` (nombre original del expediente; no se renombra para conservar rutas).
2. Los nombres `MANIFIESTO_EVIDENCIAS_SHA256_V21.txt` (manifiesto del expediente V21) y `SHA256SUMS.txt` (manifiesto del paquete) siguen siendo históricos; el manifiesto vigente de la revisión V24 es `MANIFIESTO_SHA256_V24.txt`.
3. Ninguna inconsistencia adicional impide cerrar OBS-01, OBS-02 ni OBS-03.
