# INFORME DE HASHES Y MANIFIESTO

## Reglas del manifiesto (herramienta única `scripts_validacion/ct_manifiesto.py`)
- `MANIFIESTO_SHA256_CIERRE.txt`: rutas **relativas** a `docs/fase0/cierre_tecnico_fase0/`, formato `sha256sum -c`, orden bytewise, LF, sin CR, rutas únicas y seguras (sin absolutas, `..`, ni duplicadas).
- **Exclusiones (solo dos, declaradas en el generador y en el verificador):** el propio manifiesto (no puede contener su hash) y el directorio `evidencia_verificacion/` (contiene las salidas de verificar el commit de contenido; no puede formar parte de lo que verifica).
- Enlaces simbólicos, archivos no regulares, `__pycache__` y `*.pyc` son **error** (antes se omitían en silencio).
- El SHA-256 se calcula sobre los bytes reales (disco / clon / blob descargado por API).

## Diseño de punto fijo (por qué el HEAD final puede verificarse sin autorreferencia)
1. Commit de contenido `C_content`: todo el dossier + manifiesto regenerado.
2. Se verifican A (clon fresco) y B (API) sobre `C_content`; las salidas se guardan en `evidencia_verificacion/` y se publican en `C_evid`.
3. `C_evid` solo toca `evidencia_verificacion/`; se verifica A y B sobre el HEAD final con `--base C_content`, que comprueba que lo único cambiado desde `C_content` es ese directorio y que 100 % de las entradas del manifiesto coinciden.
4. Limitación reconocida: el resultado de la verificación del HEAD final (`C_evid`) no puede constar en el propio `C_evid`; consta en el mensaje final y es reproducible con los comandos de `evidencia_verificacion/`.

## Verificación
- Vía A (git): clon fresco en directorio nuevo; `ct_manifiesto.py dir <clon>/docs/fase0/cierre_tecnico_fase0 --repo <clon> [--base SHA] [--detalle f]`.
- Vía B (API de GitHub, `git/trees` + `git/blobs`): `ct_manifiesto.py api appalex47-lab/Copy-Creative-Intelligence <SHA> [--base SHA] [--detalle f]`.
- Ambas escriben HEAD, fecha, número de archivos y resultado por archivo.
- Controles negativos aislados (36/36, vía A y vía B con `gh` simulado, 18 casos c/u + determinismo + `--base`): `resultados/controles_negativos_manifiesto.txt`.

## Defectos de la ronda anterior (corregidos)
Verificador v1 omitía enlaces simbólicos en silencio, usaba lista de «extras» permitidos, no probaba la vía B con control negativo y el informe de publicación afirmaba verificaciones de commits anteriores. Herramientas antiguas (generador y verificador v1) eliminadas; su control negativo se conserva como histórico en `resultados/historico_verificador_v1_control_negativo.txt`.

## Alcance
El SHA-256 prueba identidad de bytes, no corrección de contenido. Comparar dos copias locales no se considera prueba.
