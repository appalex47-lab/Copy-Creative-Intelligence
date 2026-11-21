# INFORME DE AUDITORÍA DE FECHAS Y HORAS

Generado por `scripts_validacion/ct_gen_auditoria_fechas.py`; cada marca procede del reloj del entorno, de git o de la API de GitHub. **No se modificó ninguna fecha para que parezca coherente y no se escribió ninguna a mano.**

## Reloj y zona horaria del entorno (leídos al generar este informe)
| Magnitud | Valor |
|---|---|
| UTC (`date -u`) | 2026-11-21T18:09:32Z |
| Local (`date`) | 2026-11-21T12:09:32-0600 (CST) |
| Variable TZ | America/Mexico_City |
| Diferencia local−UTC | -0600 |

**Criterio:** la zona local del entorno es la del usuario (America/Mexico_City, UTC−06:00 en noviembre). Las marcas con sufijo `Z` están en UTC; las de git y las columnas `*_local` llevan el desfase explícito. Una hora UTC y una hora local de la misma ejecución difieren en 6 h (p. ej. 02:36Z = 20:36 local): comparar sin convertir produce una discrepancia aparente de 6 h.

## Batería final: inicio, fin y zona de cada paso (datos del entorno)
| Paso | Inicio UTC | Fin UTC | Inicio local | Fin local | Zona |
|---|---|---|---|---|---|
| v20_pe | 2026-11-21T18:01:47Z | 2026-11-21T18:01:48Z | 2026-11-21T12:01:47-0600 | 2026-11-21T12:01:48-0600 | CST |
| v20_mutaciones | 2026-11-21T18:01:48Z | 2026-11-21T18:01:50Z | 2026-11-21T12:01:48-0600 | 2026-11-21T12:01:50-0600 | CST |
| extension_local | 2026-11-21T18:01:50Z | 2026-11-21T18:01:51Z | 2026-11-21T12:01:50-0600 | 2026-11-21T12:01:51-0600 | CST |
| concurrencia_local | 2026-11-21T18:01:51Z | 2026-11-21T18:01:57Z | 2026-11-21T12:01:51-0600 | 2026-11-21T12:01:57-0600 | CST |
| dg19 | 2026-11-21T18:01:57Z | 2026-11-21T18:01:57Z | 2026-11-21T12:01:57-0600 | 2026-11-21T12:01:57-0600 | CST |
| hash_encadenado | 2026-11-21T18:01:57Z | 2026-11-21T18:01:57Z | 2026-11-21T12:01:57-0600 | 2026-11-21T12:01:57-0600 | CST |
| estatica_T47_T124 | 2026-11-21T18:01:57Z | 2026-11-21T18:01:57Z | 2026-11-21T12:01:57-0600 | 2026-11-21T12:01:57-0600 | CST |
| k47_por_escenario | 2026-11-21T18:01:57Z | 2026-11-21T18:01:57Z | 2026-11-21T12:01:57-0600 | 2026-11-21T12:01:57-0600 | CST |
| t409_individual | 2026-11-21T18:01:57Z | 2026-11-21T18:01:58Z | 2026-11-21T12:01:57-0600 | 2026-11-21T12:01:58-0600 | CST |
| t409_repro_2a_corrida | 2026-11-21T18:01:58Z | 2026-11-21T18:01:58Z | 2026-11-21T12:01:58-0600 | 2026-11-21T12:01:58-0600 | CST |
| t409_repro_comparacion | 2026-11-21T18:01:58Z | 2026-11-21T18:01:58Z | 2026-11-21T12:01:58-0600 | 2026-11-21T12:01:58-0600 | CST |
| t409_correspondencia | 2026-11-21T18:01:58Z | 2026-11-21T18:01:58Z | 2026-11-21T12:01:58-0600 | 2026-11-21T12:01:58-0600 | CST |
| funciones_22 | 2026-11-21T18:01:58Z | 2026-11-21T18:02:40Z | 2026-11-21T12:01:58-0600 | 2026-11-21T12:02:40-0600 | CST |
| exc_modelo14 | 2026-11-21T18:02:40Z | 2026-11-21T18:03:15Z | 2026-11-21T12:02:40-0600 | 2026-11-21T12:03:15-0600 | CST |
| catalogo_except | 2026-11-21T18:03:15Z | 2026-11-21T18:03:17Z | 2026-11-21T12:03:15-0600 | 2026-11-21T12:03:17-0600 | CST |
| arnes_r1r9 | 2026-11-21T18:03:17Z | 2026-11-21T18:03:17Z | 2026-11-21T12:03:17-0600 | 2026-11-21T12:03:17-0600 | CST |
| smoke_6_scripts | 2026-11-21T18:03:17Z | 2026-11-21T18:03:23Z | 2026-11-21T12:03:17-0600 | 2026-11-21T12:03:23-0600 | CST |
| aserciones_smoke | 2026-11-21T18:03:23Z | 2026-11-21T18:03:23Z | 2026-11-21T12:03:23-0600 | 2026-11-21T12:03:23-0600 | CST |
| guarda_destino | 2026-11-21T18:03:23Z | 2026-11-21T18:03:27Z | 2026-11-21T12:03:23-0600 | 2026-11-21T12:03:27-0600 | CST |
| escaner_sql | 2026-11-21T18:03:27Z | 2026-11-21T18:03:27Z | 2026-11-21T12:03:27-0600 | 2026-11-21T12:03:27-0600 | CST |
| escaner_texto | 2026-11-21T18:03:27Z | 2026-11-21T18:03:27Z | 2026-11-21T12:03:27-0600 | 2026-11-21T12:03:27-0600 | CST |
| escaner_autoprueba | 2026-11-21T18:03:27Z | 2026-11-21T18:03:27Z | 2026-11-21T12:03:27-0600 | 2026-11-21T12:03:27-0600 | CST |

Batería completa: inicio 2026-11-21T18:01:47Z UTC / 2026-11-21T12:01:47-0600 local; fin 2026-11-21T18:03:27Z UTC / 2026-11-21T12:03:27-0600 local. Fuente: `scripts_validacion/resultados/bateria_final/ENTORNO.txt` e `INDICE_BATERIA.csv` (generados por `ct_bateria_final.sh` con `date`, sin edición manual; las salidas anteriores se borran antes de ejecutar, por lo que ningún resultado es de una corrida previa; cada salida tiene su SHA-256 en el índice).

## Commits de la rama (marcas de git y de GitHub)
| Commit | Fecha de commit (git, con desfase) | Fecha de commit en UTC | Fecha de la API de GitHub |
|---|---|---|---|
| `d365a162e548` | 2026-11-21T11:02:28-06:00 | 2026-11-21T17:02:28Z | 2026-11-21T17:02:28Z |
| `df70dc5d1cc6` | 2026-11-21T11:02:28-06:00 | 2026-11-21T17:02:28Z | 2026-11-21T17:02:28Z |
| `b7442baf6058` | 2026-11-21T11:02:28-06:00 | 2026-11-21T17:02:28Z | 2026-11-21T17:02:28Z |
| `5b008485706b` | 2026-11-20T23:10:44-06:00 | 2026-11-21T05:10:44Z | 2026-11-21T05:10:44Z |
| `d0840871d9ab` | 2026-11-20T23:09:29-06:00 | 2026-11-21T05:09:29Z | 2026-11-21T05:09:29Z |
| `942a7f66bfd2` | 2026-11-20T23:07:59-06:00 | 2026-11-21T05:07:59Z | 2026-11-21T05:07:59Z |
| `bdd4a6d78a68` | 2026-11-20T20:46:27-06:00 | 2026-11-21T02:46:27Z | 2026-11-21T02:46:27Z |
| `6a041cb9ca7c` | 2026-11-20T20:45:13-06:00 | 2026-11-21T02:45:13Z | 2026-11-21T02:45:13Z |

La fecha de un commit la escribe el reloj de quien lo crea (aquí, el reloj del entorno); la API de GitHub devuelve ese mismo campo, **no** una hora de recepción. Sirve para comprobar que git y GitHub coinciden, no como prueba externa de la hora.

## Contraste del reloj con el servidor de GitHub (cabecera HTTP `Date`)
| Magnitud | Valor |
|---|---|
| `Date` de api.github.com | Sat, 21 Nov 2026 18:09:38 GMT |
| Reloj del entorno (punto medio de la consulta) | Sat, 21 Nov 2026 18:09:38 GMT |
| Diferencia entorno − servidor | +0.1 s (resolución de 1 s; la consulta duró 0.5 s) |

Esta lectura contrasta el reloj del entorno con un reloj externo en el instante de la consulta; no acredita las horas de ejecuciones anteriores, solo que el reloj no estaba desviado en este momento.

## Hora de recepción de los push según GitHub (eventos del repositorio, hora del servidor)
| Evento (UTC, servidor GitHub) | Rama | HEAD empujado |
|---|---|---|

Estas marcas son del servidor de GitHub y permiten contrastar la hora del entorno; solo cubren los eventos que la API conserva (ventana limitada).

## Conclusión
- Zona horaria del entorno: ver tabla (UTC−06:00 CST). Todas las evidencias distinguen hora de inicio, de finalización y zona.
- La discrepancia observada entre la batería (UTC, sufijo Z) y la hora de revisión (local) es de un desfase de 6 horas; no hay evidencia de ejecuciones reutilizadas (las salidas se borran antes de cada batería y llevan SHA-256 en el índice).
- **Parcialmente acreditado:** el reloj del entorno se contrastó con la cabecera `Date` de GitHub solo en el momento de generar este informe (tabla anterior); no hay fuente NTP verificable para las horas de las ejecuciones pasadas. Las horas se presentan como las que el entorno reporta, no como horas verificadas externamente; los push se contrastan con el servidor de GitHub cuando la API los devuelve.
