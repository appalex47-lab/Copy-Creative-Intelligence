# INFORME DE AUDITORÍA DE FECHAS Y HORAS

Generado por `scripts_validacion/ct_gen_auditoria_fechas.py`; cada marca procede del reloj del entorno, de git o de la API de GitHub. **No se modificó ninguna fecha para que parezca coherente y no se escribió ninguna a mano.**

## Reloj y zona horaria del entorno (leídos al generar este informe)
| Magnitud | Valor |
|---|---|
| UTC (`date -u`) | 2026-11-21T23:21:57Z |
| Local (`date`) | 2026-11-21T23:21:57+0000 (UTC) |
| Variable TZ | (sin definir) |
| Diferencia local−UTC | +0000 |

**Criterio:** la zona local del entorno es la del usuario (America/Mexico_City, UTC−06:00 en noviembre). Las marcas con sufijo `Z` están en UTC; las de git y las columnas `*_local` llevan el desfase explícito. Una hora UTC y una hora local de la misma ejecución difieren en 6 h (p. ej. 02:36Z = 20:36 local): comparar sin convertir produce una discrepancia aparente de 6 h.

## Batería final: inicio, fin y zona de cada paso (datos del entorno)
| Paso | Inicio UTC | Fin UTC | Inicio local | Fin local | Zona |
|---|---|---|---|---|---|
| v20_pe | 2026-11-21T23:17:20Z | 2026-11-21T23:17:20Z | 2026-11-21T23:17:20+0000 | 2026-11-21T23:17:20+0000 | UTC |
| v20_mutaciones | 2026-11-21T23:17:20Z | 2026-11-21T23:17:22Z | 2026-11-21T23:17:20+0000 | 2026-11-21T23:17:22+0000 | UTC |
| extension_local | 2026-11-21T23:17:22Z | 2026-11-21T23:17:23Z | 2026-11-21T23:17:22+0000 | 2026-11-21T23:17:23+0000 | UTC |
| concurrencia_local | 2026-11-21T23:19:12Z | 2026-11-21T23:19:18Z | 2026-11-21T23:19:12+0000 | 2026-11-21T23:19:18+0000 | UTC |
| dg19 | 2026-11-21T23:17:23Z | 2026-11-21T23:17:23Z | 2026-11-21T23:17:23+0000 | 2026-11-21T23:17:23+0000 | UTC |
| hash_encadenado | 2026-11-21T23:17:23Z | 2026-11-21T23:17:23Z | 2026-11-21T23:17:23+0000 | 2026-11-21T23:17:23+0000 | UTC |
| estatica_T47_T124 | 2026-11-21T23:17:29Z | 2026-11-21T23:17:29Z | 2026-11-21T23:17:29+0000 | 2026-11-21T23:17:29+0000 | UTC |
| k47_por_escenario | 2026-11-21T23:17:29Z | 2026-11-21T23:17:30Z | 2026-11-21T23:17:29+0000 | 2026-11-21T23:17:30+0000 | UTC |
| t409_individual | 2026-11-21T23:17:30Z | 2026-11-21T23:17:30Z | 2026-11-21T23:17:30+0000 | 2026-11-21T23:17:30+0000 | UTC |
| t409_repro_2a_corrida | 2026-11-21T23:17:30Z | 2026-11-21T23:17:30Z | 2026-11-21T23:17:30+0000 | 2026-11-21T23:17:30+0000 | UTC |
| t409_repro_comparacion | 2026-11-21T23:17:30Z | 2026-11-21T23:17:30Z | 2026-11-21T23:17:30+0000 | 2026-11-21T23:17:30+0000 | UTC |
| t409_correspondencia | 2026-11-21T23:17:30Z | 2026-11-21T23:17:30Z | 2026-11-21T23:17:30+0000 | 2026-11-21T23:17:30+0000 | UTC |
| funciones_22 | 2026-11-21T23:17:30Z | 2026-11-21T23:18:24Z | 2026-11-21T23:17:30+0000 | 2026-11-21T23:18:24+0000 | UTC |
| exc_modelo14 | 2026-11-21T23:18:24Z | 2026-11-21T23:19:09Z | 2026-11-21T23:18:24+0000 | 2026-11-21T23:19:09+0000 | UTC |
| catalogo_except | 2026-11-21T23:19:09Z | 2026-11-21T23:19:12Z | 2026-11-21T23:19:09+0000 | 2026-11-21T23:19:12+0000 | UTC |
| arnes_r1r9 | 2026-11-21T23:19:12Z | 2026-11-21T23:19:12Z | 2026-11-21T23:19:12+0000 | 2026-11-21T23:19:12+0000 | UTC |
| smoke_6_scripts | 2026-11-21T23:17:23Z | 2026-11-21T23:17:29Z | 2026-11-21T23:17:23+0000 | 2026-11-21T23:17:29+0000 | UTC |
| aserciones_smoke | 2026-11-21T23:17:29Z | 2026-11-21T23:17:29Z | 2026-11-21T23:17:29+0000 | 2026-11-21T23:17:29+0000 | UTC |
| guarda_destino | 2026-11-21T23:14:16Z | 2026-11-21T23:14:21Z | 2026-11-21T23:14:16+0000 | 2026-11-21T23:14:21+0000 | UTC |
| escaner_sql | 2026-11-21T23:14:10Z | 2026-11-21T23:14:11Z | 2026-11-21T23:14:11+0000 | 2026-11-21T23:14:11+0000 | UTC |
| escaner_texto | 2026-11-21T23:14:11Z | 2026-11-21T23:14:11Z | 2026-11-21T23:14:11+0000 | 2026-11-21T23:14:11+0000 | UTC |
| escaner_autoprueba | 2026-11-21T23:14:11Z | 2026-11-21T23:14:11Z | 2026-11-21T23:14:11+0000 | 2026-11-21T23:14:11+0000 | UTC |

Batería completa: inicio None UTC / None local; fin None UTC / None local. Fuente: `scripts_validacion/resultados/bateria_final/ENTORNO.txt` e `INDICE_BATERIA.csv` (generados por `ct_bateria_final.sh` con `date`, sin edición manual; las salidas anteriores se borran antes de ejecutar, por lo que ningún resultado es de una corrida previa; cada salida tiene su SHA-256 en el índice).

## Commits de la rama (marcas de git y de GitHub)
| Commit | Fecha de commit (git, con desfase) | Fecha de commit en UTC | Fecha de la API de GitHub |
|---|---|---|---|
| `17f2865f56bc` | 2026-11-21T17:14:08-06:00 | 2026-11-21T23:14:08Z | (no disponible) |
| `d997cbec187b` | 2026-11-21T17:09:09-06:00 | 2026-11-21T23:09:09Z | (no disponible) |
| `120c89fc020e` | 2026-11-21T16:45:42-06:00 | 2026-11-21T22:45:42Z | (no disponible) |
| `404f5adc69d6` | 2026-11-21T16:42:11-06:00 | 2026-11-21T22:42:11Z | (no disponible) |
| `cd8689b55e2f` | 2026-11-21T16:34:16-06:00 | 2026-11-21T22:34:16Z | (no disponible) |
| `b5365f12115e` | 2026-11-21T16:33:33-06:00 | 2026-11-21T22:33:33Z | (no disponible) |
| `15083ea62b7b` | 2026-11-21T16:19:40-06:00 | 2026-11-21T22:19:40Z | (no disponible) |
| `2e45345edce5` | 2026-11-21T16:08:44-06:00 | 2026-11-21T22:08:44Z | (no disponible) |

La fecha de un commit la escribe el reloj de quien lo crea (aquí, el reloj del entorno); la API de GitHub devuelve ese mismo campo, **no** una hora de recepción. Sirve para comprobar que git y GitHub coinciden, no como prueba externa de la hora.

## Contraste del reloj con el servidor de GitHub
No se obtuvo la cabecera `Date` (no acreditado).

## Hora de recepción de los push según GitHub (eventos del repositorio, hora del servidor)
| Evento (UTC, servidor GitHub) | Rama | HEAD empujado |
|---|---|---|

Estas marcas son del servidor de GitHub y permiten contrastar la hora del entorno; solo cubren los eventos que la API conserva (ventana limitada).

## Conclusión
- Zona horaria del entorno: ver tabla (UTC−06:00 CST). Todas las evidencias distinguen hora de inicio, de finalización y zona.
- La discrepancia observada entre la batería (UTC, sufijo Z) y la hora de revisión (local) es de un desfase de 6 horas; no hay evidencia de ejecuciones reutilizadas (las salidas se borran antes de cada batería y llevan SHA-256 en el índice).
- **Parcialmente acreditado:** el reloj del entorno se contrastó con la cabecera `Date` de GitHub solo en el momento de generar este informe (tabla anterior); no hay fuente NTP verificable para las horas de las ejecuciones pasadas. Las horas se presentan como las que el entorno reporta, no como horas verificadas externamente; los push se contrastan con el servidor de GitHub cuando la API los devuelve.
