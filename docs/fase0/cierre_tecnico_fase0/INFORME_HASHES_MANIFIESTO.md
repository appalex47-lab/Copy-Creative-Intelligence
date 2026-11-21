# INFORME DE HASHES Y MANIFIESTO

## Reglas del manifiesto (nuevas)
- `MANIFIESTO_SHA256_CIERRE.txt` usa rutas **relativas** a `docs/fase0/cierre_tecnico_fase0/`, formato `sha256sum -c`.
- **No se lista a sí mismo** (un archivo no puede contener su propio hash). Tampoco lista `INFORME_PUBLICACION_GITHUB.md`, que documenta la publicación (incluye resultados posteriores al push). Ambas exclusiones están declaradas en `ct_gen_manifiesto.py`, en `ct_verificar_publicacion.py` y en el LEEME.
- Excluidos además `__pycache__/` y `*.pyc` (no se versionan).

## Discrepancias detectadas en la publicación anterior (e6caebf)
| # | Discrepancia | Tratamiento |
|---|---|---|
| 1 | El manifiesto anterior listaba 51 archivos y **el propio manifiesto estaba comprometido en el commit** sin poder contener su hash | Se regenera sin autoinclusión; la verificación exige que no aparezca |
| 2 | La verificación anterior comparaba contra copias locales | Ahora se verifica contra descargas desde GitHub (dos vías independientes) |
| 3 | No se comprobaban rutas duplicadas/absolutas/inseguras ni archivos extra/faltantes | `ct_verificar_publicacion.py` las comprueba; control negativo: 5 FAIL ante manipulación (`resultados/verificador_control_negativo.txt`) |

## Procedimiento de verificación de la publicación
1. **Vía A (git):** clon fresco de la rama (`git clone --branch audit/cierre-tecnico-fase0`) en un directorio nuevo; `ct_verificar_publicacion.py dir <clon>/docs/fase0/cierre_tecnico_fase0` y `sha256sum -c`.
2. **Vía B (API de GitHub, independiente):** `ct_verificar_publicacion.py api _ <repo> <rama>` descarga cada *blob* por la API (`git/trees` + `git/blobs`, base64) y recalcula el SHA-256, sin usar la copia local ni el clon.
3. Resultados y SHAs de los commits: `INFORME_PUBLICACION_GITHUB.md` (posterior al push).

## Alcance y límites
El SHA-256 prueba que los archivos publicados son idénticos a los listados, no que su contenido sea correcto. Una comparación entre dos copias locales no se considera prueba.
