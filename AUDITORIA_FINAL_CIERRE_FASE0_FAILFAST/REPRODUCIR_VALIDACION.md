# Reproducir
Requisitos: root, PostgreSQL 16 en /usr/lib/postgresql/16/bin, usuario `postgres`, git, python3. Repositorio limpio en la rama evaluada.
`python3 -I -B docs/fase0/cierre_tecnico_fase0/scripts_validacion/ct_orquestador_fase0.py <raiz_repo> <dir_salida>`
El orquestador crea dos clústeres nuevos, ejecuta A–K en orden, se detiene en el primer FAIL (exit 1), termina con exit 2 si hay dependencias externas BLOCKED y con exit 0 sólo si todo PASS y nada BLOCKED. Genera RESULTADO_ORQUESTADOR.json y LOG_COMPLETO_EJECUCION.txt. Para desbloquear: aportar custodio del hash (`CCI_HASH_CUSTODIO_EXTERNO_CONFIRMADO`), listas de destinos reales, verificación de controles V26 y validación Supabase autorizada.
