# INFORME DE PUBLICACIÓN EN GITHUB

Repositorio: `appalex47-lab/Copy-Creative-Intelligence` · Rama: `audit/cierre-tecnico-fase0` (https://github.com/appalex47-lab/Copy-Creative-Intelligence/tree/audit/cierre-tecnico-fase0).
Publicación exclusivamente para revisión independiente: no implica aprobación, aceptación, fusión ni autorización de la siguiente fase. Sin PR ni merge. Sin `force push`.

## Commits
| Commit | SHA | Contenido |
|---|---|---|
| Primera publicación | `e6caebf61947d94ac8867ecd62f6ebe079fe64ef` (padre V26 `439777c9ea7db464fe49299adfeb2112abfd285c`) | expediente inicial (52 archivos) |
| Corrección final consolidada | `182b83293f0a207d29d7ca06c3284ad2a672298d` (padre `e6caebf…`) | 44 archivos añadidos, 25 modificados, 0 eliminados respecto de e6caebf |
| Informe y salidas de verificación; ajuste del manifiesto | commits posteriores en la misma rama (el SHA vigente no puede constar en este contenido: ver `git log` y el mensaje final) | este informe, `verificacion_remota_via*.txt` y manifiesto actualizado a 96 entradas (las dos salidas de verificación se incorporan al manifiesto; una primera comprobación del HEAD posterior detectó esas dos como «extra no declarados» y se corrigió) |

## Verificación remota del commit 182b832 (independiente)
| Vía | Método | Resultado |
|---|---|---|
| A | clon fresco desde GitHub; `ct_verificar_publicacion.py dir` y `sha256sum -c` | 94/94 SHA-256 coinciden; sin faltantes, extra, duplicados, rutas absolutas ni inseguras |
| B | API de GitHub (`git/trees` + `git/blobs`), sin usar la copia local ni el clon | 94/94 coinciden; mismas comprobaciones |

Salidas íntegras: `scripts_validacion/resultados/verificacion_remota_viaA.txt` y `…_viaB.txt`. El manifiesto de 182b832 (94 entradas) no se lista a sí mismo ni lista este informe (exclusiones declaradas).

## Integridad de otras ramas y alcance
- `main` = `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` (sin cambios).
- `audit/fase0-v26-review` = `439777c9ea7db464fe49299adfeb2112abfd285c` (sin cambios).
- Diferencia entre V26 y la rama del cierre: solo archivos añadidos bajo `docs/fase0/cierre_tecnico_fase0/` (0 rutas fuera del dossier; 0 archivos de V26 modificados).
- CCI-DEV y CCI-PROD: no se tocaron; no se ejecutó ningún script contra Supabase.

## Limitaciones de esta verificación
El SHA-256 prueba identidad de archivos, no corrección de contenido. La verificación de `main`/V26 es por SHA de referencia remota.

## Verificación del HEAD final
Tras actualizar el manifiesto (96 entradas) se repiten las vías A y B sobre el HEAD de la rama; resultado en el mensaje final y en `git log`.
