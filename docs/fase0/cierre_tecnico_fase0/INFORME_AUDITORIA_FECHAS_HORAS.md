# INFORME DE AUDITORÍA DE FECHAS Y HORAS

Generado por `scripts_validacion/ct_gen_auditoria_fechas.py`; cada marca procede del reloj del entorno, de git o de la API de GitHub. **No se modificó ninguna fecha para que parezca coherente y no se escribió ninguna a mano.**

## Reloj y zona horaria del entorno (leídos al generar este informe)
| Magnitud | Valor |
|---|---|
| UTC (`date -u`) | 2026-11-21T21:49:47Z |
| Local (`date`) | 2026-11-21T21:49:47+0000 (UTC) |
| Variable TZ | (sin definir) |
| Diferencia local−UTC | +0000 |

**Criterio:** la zona local del entorno es la del usuario (America/Mexico_City, UTC−06:00 en noviembre). Las marcas con sufijo `Z` están en UTC; las de git y las columnas `*_local` llevan el desfase explícito. Una hora UTC y una hora local de la misma ejecución difieren en 6 h (p. ej. 02:36Z = 20:36 local): comparar sin convertir produce una discrepancia aparente de 6 h.

## Batería final: inicio, fin y zona de cada paso (datos del entorno)
| Paso | Inicio UTC | Fin UTC | Inicio local | Fin local | Zona |
|---|---|---|---|---|---|
| v20_pe | 2026-11-21T21:44:44Z | 2026-11-21T21:44:45Z | 2026-11-21T21:44:44+0000 | 2026-11-21T21:44:45+0000 | UTC |
| v20_mutaciones | 2026-11-21T21:44:45Z | 2026-11-21T21:44:47Z | 2026-11-21T21:44:45+0000 | 2026-11-21T21:44:47+0000 | UTC |
| extension_local | 2026-11-21T21:44:47Z | 2026-11-21T21:44:47Z | 2026-11-21T21:44:47+0000 | 2026-11-21T21:44:47+0000 | UTC |
| concurrencia_local | 2026-11-21T21:46:57Z | 2026-11-21T21:47:03Z | 2026-11-21T21:46:57+0000 | 2026-11-21T21:47:03+0000 | UTC |
| dg19 | 2026-11-21T21:44:47Z | 2026-11-21T21:44:47Z | 2026-11-21T21:44:47+0000 | 2026-11-21T21:44:47+0000 | UTC |
| hash_encadenado | 2026-11-21T21:44:47Z | 2026-11-21T21:44:47Z | 2026-11-21T21:44:47+0000 | 2026-11-21T21:44:47+0000 | UTC |
| estatica_T47_T124 | 2026-11-21T21:44:53Z | 2026-11-21T21:44:53Z | 2026-11-21T21:44:53+0000 | 2026-11-21T21:44:53+0000 | UTC |
| k47_por_escenario | 2026-11-21T21:44:53Z | 2026-11-21T21:44:54Z | 2026-11-21T21:44:53+0000 | 2026-11-21T21:44:54+0000 | UTC |
| t409_individual | 2026-11-21T21:44:54Z | 2026-11-21T21:44:54Z | 2026-11-21T21:44:54+0000 | 2026-11-21T21:44:54+0000 | UTC |
| t409_repro_2a_corrida | 2026-11-21T21:44:54Z | 2026-11-21T21:44:54Z | 2026-11-21T21:44:54+0000 | 2026-11-21T21:44:54+0000 | UTC |
| t409_repro_comparacion | 2026-11-21T21:44:54Z | 2026-11-21T21:44:54Z | 2026-11-21T21:44:54+0000 | 2026-11-21T21:44:54+0000 | UTC |
| t409_correspondencia | 2026-11-21T21:44:54Z | 2026-11-21T21:44:54Z | 2026-11-21T21:44:54+0000 | 2026-11-21T21:44:54+0000 | UTC |
| funciones_22 | 2026-11-21T21:44:54Z | 2026-11-21T21:46:00Z | 2026-11-21T21:44:54+0000 | 2026-11-21T21:46:00+0000 | UTC |
| exc_modelo14 | 2026-11-21T21:46:00Z | 2026-11-21T21:46:54Z | 2026-11-21T21:46:00+0000 | 2026-11-21T21:46:54+0000 | UTC |
| catalogo_except | 2026-11-21T21:46:54Z | 2026-11-21T21:46:56Z | 2026-11-21T21:46:54+0000 | 2026-11-21T21:46:56+0000 | UTC |
| arnes_r1r9 | 2026-11-21T21:46:57Z | 2026-11-21T21:46:57Z | 2026-11-21T21:46:57+0000 | 2026-11-21T21:46:57+0000 | UTC |
| smoke_6_scripts | 2026-11-21T21:44:47Z | 2026-11-21T21:44:53Z | 2026-11-21T21:44:47+0000 | 2026-11-21T21:44:53+0000 | UTC |
| aserciones_smoke | 2026-11-21T21:44:53Z | 2026-11-21T21:44:53Z | 2026-11-21T21:44:53+0000 | 2026-11-21T21:44:53+0000 | UTC |
| guarda_destino | 2026-11-21T21:42:14Z | 2026-11-21T21:42:19Z | 2026-11-21T21:42:14+0000 | 2026-11-21T21:42:19+0000 | UTC |
| escaner_sql | 2026-11-21T21:42:08Z | 2026-11-21T21:42:08Z | 2026-11-21T21:42:08+0000 | 2026-11-21T21:42:08+0000 | UTC |
| escaner_texto | 2026-11-21T21:42:08Z | 2026-11-21T21:42:08Z | 2026-11-21T21:42:08+0000 | 2026-11-21T21:42:08+0000 | UTC |
| escaner_autoprueba | 2026-11-21T21:42:08Z | 2026-11-21T21:42:08Z | 2026-11-21T21:42:08+0000 | 2026-11-21T21:42:08+0000 | UTC |

Batería completa: inicio None UTC / None local; fin None UTC / None local. Fuente: `scripts_validacion/resultados/bateria_final/ENTORNO.txt` e `INDICE_BATERIA.csv` (generados por `ct_bateria_final.sh` con `date`, sin edición manual; las salidas anteriores se borran antes de ejecutar, por lo que ningún resultado es de una corrida previa; cada salida tiene su SHA-256 en el índice).

## Commits de la rama (marcas de git y de GitHub)
| Commit | Fecha de commit (git, con desfase) | Fecha de commit en UTC | Fecha de la API de GitHub |
|---|---|---|---|
| `50d124efeaeb` | 2026-11-21T15:42:06-06:00 | 2026-11-21T21:42:06Z | (no disponible) |
| `8eabe4dcf471` | 2026-11-21T15:33:09-06:00 | 2026-11-21T21:33:09Z | (no disponible) |
| `8bc391386ccb` | 2026-11-21T15:28:07-06:00 | 2026-11-21T21:28:07Z | (no disponible) |
| `3bc7c00c61bc` | 2026-11-21T15:26:25-06:00 | 2026-11-21T21:26:25Z | (no disponible) |
| `a424b22ace00` | 2026-11-21T15:21:04-06:00 | 2026-11-21T21:21:04Z | (no disponible) |
| `c98ade0a2977` | 2026-11-21T14:45:13-06:00 | 2026-11-21T20:45:13Z | (no disponible) |
| `eb0ac4a7a5b1` | 2026-11-21T14:38:46-06:00 | 2026-11-21T20:38:46Z | (no disponible) |
| `e1ce57d2d162` | 2026-11-21T14:33:10-06:00 | 2026-11-21T20:33:10Z | (no disponible) |

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
