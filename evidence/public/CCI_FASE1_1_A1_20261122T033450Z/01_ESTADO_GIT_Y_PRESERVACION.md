> **COPIA DE CONSULTA PÚBLICA, no es evidencia original.** Derivada del archivo `evidence/CCI_FASE1_1_A1_20261122T033450Z/01_ESTADO_GIT_Y_PRESERVACION.md` (expediente original; SHA-256 del original: `7b59140fa3fdd485e70c7ddbfe22a820a1c4f1a73dfb654cd7a93883cf2044c1`). Solo se sustituyeron rutas del entorno temporal de ejecución por descripciones neutrales; el resto es idéntico. Ver `evidence/public/README.md`.

# 01 — Estado Git y preservación (solo lectura)

Comandos: `git status --short -uall`, `git ls-files`, `git diff --stat HEAD`, `git rev-list`. No se modificó, eliminó, restauró ni movió ningún archivo.

## 1. Las «cuatro entradas» de `src/tests/e2e/scripts`
Son **cuatro directorios completos**, no cuatro archivos. `git status --short` colapsa un directorio sin seguimiento en una sola línea.

| Ruta | Estado exacto | Archivos dentro | Archivos rastreados | Diferencia frente a HEAD |
|---|---|---|---|---|
| `e2e/` | `??` untracked | 6 | 0 | No existe en HEAD: todo es contenido nuevo |
| `scripts/` | `??` untracked | 2 | 0 | Ídem |
| `src/` | `??` untracked | 34 | 0 | Ídem |
| `tests/` | `??` untracked | 7 | 0 | Ídem |
| **Total** | | **49** | **0** | |

(`git status -uall` lista los 49 archivos individuales; `git ls-files src tests e2e scripts` devuelve 0.)

## 2. Por qué `git diff --stat` muestra un solo archivo
`git diff` compara únicamente archivos **rastreados**. El único rastreado con cambios es `README.md` (`M`, 38 inserciones, 1 eliminación; reescrito en Fase 1.0). Todo lo demás creado en 1.0–1.1-A (los cuatro directorios, `package.json`, `docs/architecture/`, `docs/decisions/`, `.github/`, `evidence/`, etc.) es **untracked**, y `git diff` no lo ve. Por eso no son cambios «ocultos»: son archivos nuevos todavía no añadidos al índice, coherente con la prohibición de commits.

Otros elementos sin seguimiento en la raíz (comprobado con `git ls-files --others --exclude-standard`): `.env.example`, `.github/workflows/ci.yml`, `.gitignore`, `.prettier*`, `database/README.md`, `docs/architecture|decisions|product|roadmap/`, `eslint.config.js`, `index.html`, `package.json`, `package-lock.json`, `playwright.config.ts`, `public/favicon.svg`, `supabase/README.md`, `tsconfig*.json`, `evidence/` (106 archivos) y `evidencia/` (31 archivos).

## 3. Observación que corrijo/precizo
`evidencia/` (31 archivos de Fase 0) **no está rastreada en esta rama** (0 archivos rastreados en `evidencia/` y `evidence/`). Existe en disco, con hash idéntico a la línea base guardada. Quien clone la rama sin copiar el árbol de trabajo no la recibirá. No se tocó.

## 4. Confirmaciones
| Elemento | Resultado |
|---|---|
| Rama | `development/cci-app-foundation` |
| HEAD | `9950e709e504a8d6c4a1cf599f1af5144129b8a2` |
| Commits locales no presentes en ninguna rama remota | **6** (`f19ec7a`, `c26c594`, `317e466`, `8c5c96e`, `d51bc27`, `9950e70`) |
| Commits sobre `origin/main` | 62 (los 56 restantes ya existen en ramas remotas `audit/*` heredadas) |
| `origin/main` | `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` (sin cambio) |
| `docs/fase0` | 0 entradas en `git status`; `git diff HEAD -- docs/fase0` vacío |
| Expedientes anteriores (`evidence/CCI_FASE1_0_*`, `…1_0_1_*`, `…1_0_2_*`, `…1_1_2026…`) y `evidencia/` | Comparados con las líneas base `[archivo temporal de líneas base]` y `[archivo temporal de líneas base]`: 0 diferencias (para el expediente 1.1-A se usó su `MANIFEST.sha256`) |
| Respaldos | `[directorio temporal de respaldos]/`: SHA256SUMS verificado OK en la sesión anterior (incluye `…fase1_1_previo…` y `…fase1_1_a…`) |

No verificado: que `[archivo temporal de líneas base]` cubra el expediente 1.1-A (se verificó con su propio manifiesto).
