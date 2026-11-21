# Auditoría de reproducibilidad (H-01)
**Corridas válidas** (clústeres nuevos, sin roles previos salvo `cci_test`, **en serie**): árbol corregido en cluster1 22/22 y cluster2 22/22; rama publicada d365a16 en un tercer clúster 22/22 y guarda 109/109 (confirma lo declarado; histórico). **Corridas no válidas / históricas:** dos baterías lanzadas en paralelo (carpetas distintas, clústeres distintos) fallaron en `exc_modelo14` — el arnés no soporta ejecución paralela; no se borró esa evidencia (`bat2_*` en el historial de la auditoría); una primera corrida del árbol corregido falló por defectos propios reales (escáner SQL por un DROP y aserciones del smoke) y se corrigió.
| Comprobación | Resultado |
|---|---|
| Sin roles heredados | `nuevo_cluster.sh` imprime roles_supabase_like=0; `precondicion_roles_cluster*.txt` muestra antes (sin anon/authenticated/service_role) y después |
| Precondiciones explícitas | La batería crea anon/authenticated/service_role (nologin, sin privilegios) y lo registra (corregido F-07) |
| Cada paso con esperado | `EXP[]` por paso; estado OK sólo si rc=0 **y** la salida contiene lo esperado |
| Rechazo de negocio vs error técnico | PASS/FAIL en pruebas = coincidencia con el código esperado; rc≠0 sin coincidencia = FALLO; el arnés de la guarda ahora exige `ERROR: NO EJECUTADO [código]` (F-08) |
| Salidas no reutilizadas | La batería borra las salidas regenerables al inicio; ningún archivo de resultados con fecha anterior al inicio (comprobado por mtime vs `epoch_inicio`) |
| Independencia del orden | NOT VERIFIED en forma exhaustiva: sólo se ejecutó el orden definido; la guarda y el smoke se ejecutaron además de forma aislada |
| Equivalencia entre clústeres | 30/30 comparaciones, salvo temporización normalizada y registrada |
