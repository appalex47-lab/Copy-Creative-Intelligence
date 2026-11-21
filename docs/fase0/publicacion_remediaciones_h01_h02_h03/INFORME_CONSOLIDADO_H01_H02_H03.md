# Informe consolidado de remediación H-01 / H-02 / H-03 — CCI Fase 0
Repositorio: appalex47-lab/Copy-Creative-Intelligence · Rama: `audit/fase0-remediaciones-h01-h02-h03` · Base: `audit/cierre-tecnico-fase0` @ `5b008485706bde3e9cf8407e71c0652cfd0497a5` (sin alterar) · `main` y V26 sin tocar. Sin PR, merge, tag ni release. Sin conexión a CCI-DEV/CCI-PROD/Supabase.

## Alcance publicado
55 archivos modificados + 4 nuevos (ver `MATRIZ_ARCHIVOS_MODIFICADOS_Y_NUEVOS.csv`, con SHA-256), todos dentro de `docs/fase0/cierre_tecnico_fase0/`; más este directorio de expediente. Cantidades coinciden con lo reportado (55+4). Sin archivos eliminados.

## H-01 — independencia del entorno de pruebas
La batería crea explícitamente los roles requeridos en un clúster limpio (sin depender de roles heredados) y registra la precondición. Se revalidó en **dos clústeres nuevos** (socket Unix, PostgreSQL 16): 22/22 pasos OK en cada uno; comparación paso a paso 30/30 idéntica salvo lo legítimamente distinto (marcas de tiempo, rutas, puerto, system_identifier). Errores técnicos se registran distintos de rechazos de negocio (estado FALLO vs. códigos de rechazo). Nota honesta: dos baterías lanzadas **en paralelo** interfirieron (paso `exc_modelo14`); se repitieron en serie.

## H-02 — consistencia documental y cifras
Fuente única estructurada → Markdown/TXT generados; verificador de consistencia 58/58; controles negativos del verificador 7/7 y del manifiesto 36/36 (demuestran que detecta manipulaciones); matriz de reconciliación regenerada; manifiesto SHA-256 con 137 entradas, 0 hashes incorrectos (verificación independiente en ambos árboles).

## H-03 — protección DEV/PROD
`00_guarda_destino.sql` integrada en los seis scripts; identidad = system_identifier + base (+ roles de plataforma sólo en modo local); denylist PROD precede; listas literales y **vacías** (no se inventan identificadores) → fail-closed; `search_path` blindado; sin bypass por variables, search_path, roles, nombre de base ni flags de psql. Revalidado: 109/109 (incluye GD-13 guarda vacía/truncada y GD-14 stdin, añadidos tras la auditoría independiente que halló AUD-G1/AUD-G3). Rechazo de destino PROD simulado: 20 casos `G-PROD-RECHAZADO` en los 6 scripts. **No** se afirma compatibilidad con Supabase real: disponibilidad/permisos de `pg_control_system()` **no verificados** (ver `MATRIZ_COMPATIBILIDAD_SUPABASE.md`).

## Resultados de validación (ejecución de esta publicación)
| Área | Pruebas ejecutadas | PASS | FAIL | SIN DATOS | Evidencia |
|---|---|---|---|---|---|
| H-01 | 22 pasos × 2 clústeres + 12 aserciones smoke | 22/22 por clúster; 12/12 | 0 | 0 | `evidencia/INDICE_BATERIA_cluster*.csv` |
| H-02 | 58 reconciliación + 58 consistencia | 58 / 58 | 0 | 0 | `scripts_validacion/resultados/reconciliacion_integral.txt` |
| H-03 | 109 guarda + 25 casos AG | 109 / 25 conformes | 0 | 0 | `scripts_validacion/resultados/guarda_destino.txt`, `evidencia/huecos_AG_post_correccion.txt` |
| Integración | 30 comparaciones entre clústeres; manifiesto 137 | 30; 137 | 0 | 0 | `evidencia/comparacion_clusteres.txt`, `integridad_independiente_*.json` |
| Controles negativos | 37 autoprueba escáner + 36 manifiesto + 7 consistencia | todos | 0 | 0 | `resultados/escaner_seguridad_autoprueba.txt`, `controles_negativos_manifiesto.txt`, `controles_consistencia_informe.txt` |
El paso heredado `estatica_T47_T124` conserva 2 SIN_DATOS (esperado en la batería, no es de esta remediación). Cifras previas (85/85, 33/33) son **históricas**.

## Limitaciones y dictamen
Ver `LIMITACIONES_NO_RESUELTAS.md` y `DICTAMEN_H03.md`. **Dictamen de la publicación: PUBLICADA CON LIMITACIONES.** No se declara Fase 0 aceptada ni Fase 1 autorizada; esas decisiones son exclusivas del propietario. Documentos históricos conservados; el dictamen de preparación vigente es `../cierre_tecnico_fase0/DICTAMEN_PREPARACION_FASE0.md`. La auditoría de la guarda publicada antes en la rama `audit/guarda-dev-prod-h03` (carpeta `docs/fase0/auditoria_guarda_h03/`) queda **sustituida** por los documentos de este directorio.
