# Reproducir
Requisitos: root, PostgreSQL 16 en /usr/lib/postgresql/16/bin, usuario `postgres`, openssl 3, git, python3, red hacia GitHub (la etapa A comprueba con `git ls-remote` que las ramas protegidas no cambiaron). Repositorio **limpio** en la rama evaluada.

```
python3 -I -B docs/fase0/cierre_tecnico_fase0/scripts_validacion/ct_orquestador_fase0.py <raiz_repo> <dir_salida>
```
- Crea clústeres nuevos, ejecuta A–K en orden, se detiene en el primer FAIL (exit 1), exit 2 si hay dependencias externas BLOCKED/NOT_TESTED, exit 0 solo si todo PASS (y sin BLOCKED/NOT_TESTED).
- Desbloqueos automáticos (K): `CCI_APROBACION_CUSTODIO`, `CCI_CUSTODIO_PUBKEY`, `CCI_CUSTODIO_PUBKEY_SHA256` (EXT-01); `CCI_EXT02_REPORTE`, `CCI_EXT02_REPORTE_SHA256` (EXT-02); listas reales en la guarda (EXT-03); ver `PLAN_DESBLOQUEO_EXTERNOS.md`.
- Meta-prueba de fallos inducidos (se ejecuta en la etapa B): `CCI_ORQ_SIMULAR=1 CCI_ORQ_FALLO_EN=<ETAPA>:<FAIL|BLOCKED|EXC|MUTAR_CRITICO|NOT_TESTED>` sobre una **copia** del repo; nunca produce veredicto real (estado `SIMULACION_*`).
- Suites individuales: `ct_pruebas_identidad_firmada.py <dir> <puerto> <out>` (AG-18, clones físicos), `ct_pruebas_ext01_y_e2e_dev.py` (EXT-01 + cadena DEV), `ct_pruebas_autorizacion_operadores.py <sock> <puerto> <out>`, `ct_pruebas_05_secuencia.py <sock> <puerto> <out>`, `ct_pruebas_validador_listas.py <out>`, `ct_pruebas_ext02_sonda.py <sock> <puerto> <out>`, `ct_pruebas_orquestador_fallos.py <repo> <out>`, `ct_anclas_evidencia.py controles <dir_cierre> <out>`.
- Verificar el expediente: `sha256sum -c MANIFIESTO_SHA256.txt`.
