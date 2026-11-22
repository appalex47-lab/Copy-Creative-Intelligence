# Informe de integridad de archivos y manifiestos (2026-11-22)
**Quién verificó qué:** todo lo siguiente fue ejecutado por mí (comandos reproducibles abajo); nada se toma de informes de otro proceso salvo donde se indica.

## 1. Verificaciones previas a la publicación
| Comprobación | Resultado |
|---|---|
| HEAD de la rama por API antes de editar | `1bb831a32219898616e7a7ad8d12092aac16f253` (coincide con la referencia); `main` = `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` |
| Estado de la integridad heredada (commit 1bb831a, clon limpio, ejecutado en la tarea anterior) | `MANIFEST.sha256` correcto; 92/92 archivos de `INVENTARIO_PUBLICADO.sha256` coinciden en tamaño y SHA-256 (0 fallos) |
| `docs/fase0/` frente a `main` | 59/59 entradas de árbol idénticas (`git ls-tree` sin diferencias; `git diff` sin cambios) |
| Duplicados de nombre en el expediente | 0 |
| Archivos de texto no mencionados en índices (antes de esta auditoría) | 0 |
| `MANIFIESTO_ENTREGA_2026-11-22_D4_D6_D7_D8.txt` (manifiesto fechado anterior) | 0/7 hashes coinciden con los archivos actuales (esperado: se modificaron después). Es histórico; el vigente es MANIFEST + INVENTARIO. No se alteró |
## 2. Cobertura de vigencia (documentación)
- Archivos de texto del expediente previos a esta auditoría (excluye `logs/` y `auditoria_integral/`): **78**. Todos clasificados por vigencia en `05_INFORME_AUDITORIA_INTEGRAL.md` §1.
- Con nota o estado de vigencia **en el propio archivo** (búsqueda de patrón): **53/78**. Los 25 restantes son entregables propuestos o antecedentes cuya vigencia se establece en el índice maestro, no en su texto. Indicador orientativo; no mide corrección de contenido.
## 3. Verificación posterior a la publicación (clon limpio)
Se completa tras publicar (sección actualizada en el segundo commit de esta auditoría).
## 4. Procedimiento reproducible
```
git clone --branch evidence/cci-fase0-review https://github.com/appalex47-lab/Copy-Creative-Intelligence
cd Copy-Creative-Intelligence/evidence/cci-fase0
sha256sum -c MANIFEST.sha256                      # excluye MANIFEST.sha256 e INVENTARIO_PUBLICADO.sha256
# inventario: cada línea es «sha256  tamaño  ruta» (excluye INVENTARIO_PUBLICADO.sha256)
grep -v 'INVENTARIO_PUBLICADO.sha256$' INVENTARIO_PUBLICADO.sha256 | while read h s f; do
  [ "$(sha256sum "$f"|cut -d' ' -f1)" = "$h" ] && [ "$(stat -c%s "$f")" = "$s" ] || echo FALLO $f; done
```
## 5. Exclusiones y límites
- `MANIFEST.sha256` e `INVENTARIO_PUBLICADO.sha256` no se incluyen a sí mismos (INVENTARIO sí lista a MANIFEST). Un archivo que no esté en el inventario no queda verificado.
- Los 59 archivos de `docs/fase0/` están **fuera** de los manifiestos del expediente (viven fuera de `evidence/cci-fase0/`); su integridad se contrasta con `main` y sus hashes figuran en `11_INDICE_CONCILIACION_DOCS_FASE0.md`.
- Los hashes de `logs/` prueban que el archivo publicado no cambió, no que la ejecución que registra se repita.
