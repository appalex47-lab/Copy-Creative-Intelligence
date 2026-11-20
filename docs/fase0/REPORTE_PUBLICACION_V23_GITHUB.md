# REPORTE DE PUBLICACIÓN V23 EN GITHUB

- **Repositorio:** `appalex47-lab/Copy-Creative-Intelligence`
- **Rama creada:** `audit/fase0-v23-review` (nueva; no existía; sin force push)
- **SHA de origen:** `ac84133b776cc73c0cb3416e51e2767039bb5132` (V20, rama `audit/fase0-v19-review`); `git merge-base` = ese SHA.
- **Commit del expediente:** `8be8acecffce64e2a4660383bc8d5306a303c9c1` (padre `ac84133…`). El commit de este reporte se identifica por el HEAD de la rama; un archivo no puede contener el SHA de su propio commit.
- **`main`:** inicial y final `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` (sin cambios).
- **Rama V20 (`audit/fase0-v19-review`):** sin modificar, sigue en `ac84133b776cc73c0cb3416e51e2767039bb5132`.
- **Otras ramas:** `docs/g1-g5-g10-v2` (`1134c3d42ccef604117ed566e045fb885dfe267e`), sin tocar. Sin PR abiertos ni cerrados (REST `pulls?state=all` = 0).

## Archivos publicados
- 255 archivos añadidos (todos `A`; 0 modificados, 0 eliminados), todos bajo `docs/fase0/`:
  - `docs/fase0/expediente_final_v23/` (253 archivos: contenido íntegro del ZIP, con estructura `00_LEEME … 08_INTEGRIDAD_Y_MANIFIESTOS`),
  - `docs/fase0/VALIDACION_ZIP_V23.md`,
  - `docs/fase0/entregas/CCI_FASE0_EXPEDIENTE_V21_V23.zip`.
- Más este reporte (1 archivo adicional en el segundo commit).
- Ningún archivo fuera de `docs/fase0/`; ninguno en `docs/fase0/herramientas/` ni `docs/fase0/historico/` reales (las copias dentro del expediente están en `…/05_LOGS_Y_EVIDENCIAS/arbol_original_docs_fase0/`).
- No se publicó el árbol V21 sin comprometer como cambios sobre `docs/fase0/` de la rama: la rama conserva los documentos V20 en su ubicación original; la versión V21 de los documentos activos está en el snapshot dentro del expediente V23.

## ZIP original
`CCI_FASE0_EXPEDIENTE_V21_V23.zip` · 4 376 868 bytes · SHA-256 `7dd5e3b8c758c38ee55a780b5575f2042528f2cdb2a4ffeb745347820960d93f` (igual al declarado en `VALIDACION_ZIP_V23.md`). Se subió sin modificar, sin Git LFS.

## Verificaciones previas al commit
Rama local `audit/fase0-v23-review` con base `ac84133`; diff limitado a `docs/fase0/` (0 archivos fuera); 0 cambios en rutas funcionales; ZIP con el SHA esperado; manifiesto interno 252/252 OK (`sha256sum -c` desde la raíz del expediente).

## Verificaciones posteriores al push (directamente en GitHub: `ls-remote` y API REST)
1. La rama `audit/fase0-v23-review` existe y apunta a `8be8acec…`: PASS.
2. El commit está disponible remotamente (REST `commits/8be8acec…`, padre `ac84133…`, 255 archivos): PASS.
3. `main` conserva `6a1af242…`: PASS. La rama V20 conserva `ac84133…`: PASS.
4. Árbol remoto completo (REST `git/trees?recursive`, no truncado) idéntico al árbol local: 382 blobs, 0 diferencias: PASS. Hay 253 archivos bajo `expediente_final_v23/`: PASS.
5. El ZIP descargado desde GitHub tiene SHA-256 `7dd5e3b8…d93f` y 4 376 868 bytes: PASS.
6. `VALIDACION_ZIP_V23.md` accesible y con hash igual al local (`39de6438…9245`): PASS.
7. `SHA256SUMS.txt` publicado, hash igual al local (`ab83883f…53e4`): PASS.
8. Scripts (`03_SCRIPTS/`) y resultados (`04_RESULTADOS_DE_PRUEBAS/`) presentes en el árbol remoto idéntico: PASS.
9. Sin archivos omitidos, truncados ni sustituidos (árbol remoto = local, 0 modificados/eliminados respecto a V20): PASS.
10. Sin cambios funcionales ni archivos ajenos: PASS.

## Archivos no publicados
Ninguno.

## Limitaciones
- El reporte (este archivo) se publica en un segundo commit; su verificación remota se hizo después y se informa en la respuesta de entrega, no aquí.
- La verificación de contenido remoto se hizo con la API de GitHub (árbol y blobs) y descarga de archivos clave; no se reabrió el ZIP publicado dentro de GitHub más allá de su SHA-256.
- Se conservan todas las limitaciones del expediente (sin esquema físico ni CCI-DEV, PostgreSQL temporal ≠ esquema aprobado, RLS/privilegios/concurrencia sin validar, R1–R9 no ejecutado, 12 escenarios PARCIAL, T-409..T-422 sin ejecución individual, 22 funciones validadas indirectamente, HV-02 NO VERIFICABLE) y las decisiones pendientes del propietario (PO-05, G-1, G-5, G-10, DG-19, DG-20, DG-09, DG-12, DG-16, DG-18, DEP-RET-01, G-9, RP-01, P-01 a P-05, P-10, OD-13).

## Confirmaciones
Sin merge, sin PR, sin force push, sin cambios en `main` ni en la rama V20; no se tocó Supabase, CCI-DEV ni CCI-PROD; no se inició Fase 1. Esta publicación no representa aceptación formal de Fase 0 ni aprobación de producción.
