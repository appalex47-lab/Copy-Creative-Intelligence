# Publicación controlada — reconstrucción y verificación

**Estado: FASE0_BLOCKED — IMPLEMENTACIÓN TÉCNICA COMPLETADA, VALIDACIONES EXTERNAS PENDIENTES.** Fase 0 no está aceptada. La auditoría independiente (ChatGPT) está PENDIENTE; nada aquí afirma que haya auditado o aceptado.

| Elemento | Valor |
|---|---|
| Rama | `audit/fase0-operadores-cierre` |
| Punto de partida (publicado en `audit/fase0-resolucion-final`) | `120c89fc020e63b8f63c7d6dbe0bcca588bd8d59` |
| Código evaluado por la ejecución integral | `2c516414ebc3271b166a2ebc1d1079618002883e` (`RESULTADO_ORQUESTADOR.json`: HEAD, run `CCI-RUN-20261121T232214Z-422150a8`) |
| Commit final reportado (resultados + expediente) | `ceb4eb02aea40015a10b9814b2f096a34258f363` |
| Punta publicada | `ceb4eb02…` + UN commit de empaquetado que sólo añade esta carpeta (`ARTEFACTOS_REVISION_PUBLICACION/operadores/`): ACLARACIONES, este documento, el ZIP y el bundle. No modifica código, resultados ni el expediente de 157 archivos. |
| SHA-256 `OPERADORES_CIERRE_FASE0.zip` | `b725c1d3da6f0c77c062b39b046a142558a0785b9f11f30d2d4e011fccd00cbb` |
| SHA-256 `fase0-operadores-cierre.bundle` | `1958fd595587711273d720e0f9ef5f03b21ad05aaed68b09d7bff25d6d6b8c9c` |

## Resultados de la corrida (pertenecen al código evaluado; no se mezclan con ejecuciones anteriores)
Suite adversarial 39/39 · autorización de operadores 22/22 · orquestador 67 PASS, 0 FAIL, 10 BLOCKED, 1 NOT_TESTED, 11 etapas · manifiesto de 157 archivos. La ejecución anterior (`CCI-RUN-20261121T223416Z-67eb098f`, 66 PASS) está en `AUDITORIA_FINAL_CIERRE_FASE0_RESOLUCION/` y se conserva intacta. El commit de empaquetado se hizo DESPUÉS de la ejecución integral y no se re-ejecutó el orquestador sobre él (no cambia código; una nueva ejecución sería una versión nueva).

## Dependencias para reconstruir desde el bundle
El bundle es incremental: contiene los commits `120c89f..ceb4eb0` y **requiere** el commit `120c89fc020e63b8f63c7d6dbe0bcca588bd8d59` (publicado en la rama `audit/fase0-resolucion-final`).
```
git init rec && cd rec
git fetch https://github.com/appalex47-lab/Copy-Creative-Intelligence.git audit/fase0-resolucion-final   # trae 120c89f
git fetch ../fase0-operadores-cierre.bundle audit/fase0-operadores-cierre:refs/heads/rec
git rev-parse rec        # ceb4eb02aea40015a10b9814b2f096a34258f363
git checkout rec && (cd AUDITORIA_FINAL_CIERRE_FASE0_OPERADORES && sha256sum -c MANIFIESTO_SHA256.txt)
```
Reproducir las pruebas: PostgreSQL 16 local (`/usr/lib/postgresql/16/bin`), root para `ct_nuevo_cluster.sh`; `python3 -I -B docs/fase0/cierre_tecnico_fase0/scripts_validacion/ct_orquestador_fase0.py <repo> <salida>` (ver `REPRODUCIR_VALIDACION.md` del expediente anterior). La suite de operadores puede ejecutarse sola: `ct_pruebas_operadores_cierre.py <socket> <puerto> <salida.json>` (instala y retira una extensión de prueba `cci_evilext` en el directorio de extensiones local).

## Dónde está cada evidencia
Guarda: `docs/fase0/cierre_tecnico_fase0/scripts_validacion/cci_dev_NO_EJECUTADOS/00_guarda_destino.sql` · scripts 01–05: mismo directorio · suite: `…/scripts_validacion/ct_pruebas_operadores_cierre.py` · matriz: `AUDITORIA_FINAL_CIERRE_FASE0_OPERADORES/MATRIZ_PRUEBAS_OPERADORES.csv` · logs íntegros: `…/LOG_COMPLETO_EJECUCION.txt` y `pasos/` · procedimiento de roles (plantilla NO ejecutada): `…/PROCEDIMIENTO_ROLES_CCI_DEV.sql` · limitaciones: `…/LIMITACIONES_RESIDUALES.md` · aclaraciones: `ACLARACIONES_AUDITORIA_INDEPENDIENTE.md` (esta carpeta).
