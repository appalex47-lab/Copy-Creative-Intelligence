# Informe de integridad de archivos y manifiestos — ronda de lectura completa (2026-11-22)
**Versión:** 3.0 (base `13b25ca447c0ab17f46b3143615b4c2156661b79`; los hallazgos de la v2.0 sobre `8dc47b2` se conservan como antecedente; el resultado real de esta versión figura en el informe de entrega)
**Versión anterior:** 2.0 · **Fecha:** 2026-11-22 · **Estado:** vigente · **Referencias:** `05_INFORME_AUDITORIA_INTEGRAL.md`, `07_CONTROL_DE_CAMBIOS_AUDITORIA_INTEGRAL.md`, `11_INDICE_CONCILIACION_DOCS_FASE0.md`.
**Quién verificó qué:** todo lo siguiente fue ejecutado por Claude con los comandos reproducibles de §4. No se toma nada de informes de otro proceso. Lo que no pude comprobar se marca «no verificado».

## 1. Verificaciones previas a la publicación (ejecutadas)
| Comprobación | Resultado |
|---|---|
| HEAD de la rama por API al iniciar la ronda de lectura | `13b25ca447c0ab17f46b3143615b4c2156661b79` (v2.0: `8dc47b24…`); `main` = `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`; 0 PR |
| Árbol real de la rama en `8dc47b2` (API; v2.0) | 164 blobs = 104 (`evidence/cci-fase0/`) + 59 (`docs/fase0/`) + 1 (`README.md` raíz); en `13b25ca`: 107 + 59 + 1 = 167 |
| `docs/fase0/` frente a `main` | `git ls-tree -r` idéntico (huella 5be2c1e469d5bf49 en ambos); 0 archivos modificados bajo `docs/` |
| Duplicados de nombre en el expediente | 0 |
| Archivos de texto fuera de `logs/` no mencionados en `00_INDICE`, `README_ENTREGA`, `16_INDICE` ni en la tabla de `05_` | 0 |
| `MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` (manifiesto fechado anterior) | 0/7 hashes coinciden con los archivos actuales (esperado; histórico; no se altera) |

## 2. Qué incluye y excluye cada manifiesto (sin referencias circulares)
- **`MANIFEST.sha256`:** líneas `sha256  ./ruta` de todos los archivos de `evidence/cci-fase0/` **excepto** `MANIFEST.sha256` e `INVENTARIO_PUBLICADO.sha256` → **105** líneas.
- **`INVENTARIO_PUBLICADO.sha256`:** líneas `sha256  tamaño  ruta` de todos los archivos **excepto él mismo** (sí lista a `MANIFEST.sha256`) → **106** líneas.
- Total de archivos bajo `evidence/cci-fase0/` tras esta ronda: **107**. Los 59 archivos de `docs/fase0/` quedan **fuera** de ambos manifiestos (se contrastan con `main` y por los hashes de `11_`).
- El hash del commit no puede constar dentro de los archivos que contiene; el resultado de la verificación sobre el commit publicado se informa en la entrega y se comprueba por API.

## 3. Verificación posterior a la publicación (procedimiento y reporte)
Se ejecuta sobre un **clon limpio** del commit publicado y se informa: archivos encontrados, inventariados, verificados por hash, verificados por tamaño, con fallo y excluidos. Resultado esperado: 107 encontrados · 106 inventariados · 106 verificados por hash y tamaño · 0 fallos · 1 excluido (`INVENTARIO_PUBLICADO.sha256`, no se lista a sí mismo) · `MANIFEST.sha256`: 105/105 con `sha256sum -c`. **El resultado real figura en el informe de entrega (no verificado dentro de este archivo).**

## 4. Procedimiento reproducible
```
git clone --branch evidence/cci-fase0-review https://github.com/appalex47-lab/Copy-Creative-Intelligence
cd Copy-Creative-Intelligence/evidence/cci-fase0
find . -type f | wc -l                            # archivos encontrados
sha256sum -c MANIFEST.sha256                      # excluye MANIFEST.sha256 e INVENTARIO_PUBLICADO.sha256
grep -v 'INVENTARIO_PUBLICADO.sha256$' INVENTARIO_PUBLICADO.sha256 | while read h s f; do
  [ "$(sha256sum "$f"|cut -d' ' -f1)" = "$h" ] && [ "$(stat -c%s "$f")" = "$s" ] || echo FALLO $f; done
# docs/fase0 frente a main
git ls-tree -r origin/main docs/fase0 | sha256sum ; git ls-tree -r HEAD docs/fase0 | sha256sum
```

## 5. Exclusiones y límites
- Un archivo que no esté en el inventario no queda verificado por él; los manifiestos no se incluyen a sí mismos.
- Los hashes de `logs/` prueban que el archivo publicado no cambió, no que la ejecución que registra se repita.
- **Autoverificación:** las comprobaciones las ejecuté yo; no sustituyen una verificación independiente. No verificado: que otro proceso (p. ej. ChatGPT) reproduzca estos resultados.

## 6. Nota de la ronda de lectura
Se verificó además que los 59 tamaños y SHA-256 de `11_` coinciden con los archivos de `docs/fase0/` (0 discrepancias) y que el SHA-256 del anexo coincide con `anexos/MANIFEST_informe_browser_only.sha256`. Los dos manifiestos principales se regeneran por script al final de la ronda; no se afirma aquí su resultado.
