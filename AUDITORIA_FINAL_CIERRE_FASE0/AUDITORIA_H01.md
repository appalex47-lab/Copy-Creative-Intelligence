# Auditoría H-01 (reproducibilidad de la batería)
Batería de 22 pasos en dos clústeres PostgreSQL 16 nuevos y vacíos: **22/22 OK ×2** (`evidencia/cluster1|2/INDICE_BATERIA.csv`, logs en `logs/`).
Permutaciones: 24 órdenes de {01,02,03,04} + 3 repeticiones → salidas normalizadas idénticas, sin cambios persistentes; 05A/05B invertidos → iguales (pero dependientes por diseño A→B).
## Comparación clúster 1 vs clúster 2
- Batería: 22/22 OK en ambos; pasos y rc idénticos.
- Diferencias NO normalizadas (se muestran tal cual):
| Paso | Clúster 1 | Clúster 2 |
|---|---|---|
| concurrencia_local | CC-02 \| IG1-14 numeración de versión única bajo concurrencia \| esperado: B bloqueada >=1.5s y luego  | CC-02 \| IG1-14 numeración de versión única bajo concurrencia \| esperado: B bloqueada >=1.5s y luego  |
| escaner_texto | TOTAL=781 FAIL=0 | TOTAL=751 FAIL=0 |

- Adversarial 166 casos: estados idénticos; diferencias de salida:
| Caso | Clúster 1 | Clúster 2 |
|---|---|---|
| WRAP-23-TOCTOU | rc=0 ejecuciones=25 ok=9 rechazadas=16 pwned=0 | rc=0 ejecuciones=25 ok=16 rechazadas=9 pwned=0 |

- `escaner_texto` difiere (781 vs 751 archivos escaneados) porque el árbol del clúster 2 es una copia previa a la adición de documentos nuevos; no refleja diferencia del clúster. `WRAP-23-TOCTOU` es una carrera: el reparto ok/rechazadas varía, pwned=0 en ambos.
- Búsqueda de rutas/ids/timestamps: sólo varían las marcas de tiempo, rutas de socket y puertos.

**Veredicto H-01: APROBADO CON LIMITACIONES.** Limitaciones: el orden de los 22 pasos de la batería no está probado independiente (sólo los seis scripts se permutan); 05A/05B dependientes; las suites no son paralelizables; diferencias de tiempo no normalizadas.
