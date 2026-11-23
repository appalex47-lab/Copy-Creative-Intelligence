# Control de cambios — registro de la autorización de la subfase S1.0 (2026-11-22)
> **Documento fechado, no es decisión nueva.** Base: commit local `b81591979e2eec9cc80e64b671e7b744003dc3ce`. Registra qué se cambió en el expediente para reflejar la respuesta del propietario del 2026-11-22 20:59. Solo documental: no se modificó código de la aplicación, `docs/fase0`, `main` ni la vista previa privada.

## 1. Decisión registrada (texto literal del propietario)
Ver el texto íntegro en `REGISTRO_DECISIONES_RESUELTAS.md`, sección «Autorización de la subfase S1.0». Resumen de efectos:
- **Autoriza únicamente la subfase S1.0** de la Fase 1: rama `fase1/s1-0-auditoria` desde el commit `7bcba74e05577761081d68ca14fdc19f2400248d` de `appalex47-lab/Copy-Creative-Intelligence`; lectura del repositorio, pruebas existentes sin modificarlas y solo documentación y evidencia; commit y push solo a esa rama.
- **S1.1 y S1.2** quedan autorizadas solo tras la aprobación expresa del propietario de los resultados de S1.0; **no están activas**.
- Procedencia: texto, rama, commit base y permiso de pruebas fueron propuestos por Claude y adoptados literalmente por el propietario; que el commit sea la línea base del diagnóstico aprobado no fue verificado.

## 2. Lo que NO se registró
- **No se autorizó la Fase 1 en su conjunto**; no se aprobó la descomposición S1.0–S1.12 más allá de los nombres S1.0, S1.1 y S1.2; no se aprobó ningún atributo, esquema, catálogo ni formato.
- No se resolvieron C-2, C-3 ni los 10 aplazamientos; no se reabrió D5.a–d.
- Los commits de este expediente se hicieron **localmente en la rama del expediente** (no se publicaron): son el registro documental de la decisión, distinto del trabajo de S1.0, que va a la rama `fase1/s1-0-auditoria`.

## 3. Archivos modificados
- `REGISTRO_DECISIONES_RESUELTAS.md`: sección autoritativa nueva.
- `APROBACIONES_FASE0.md`: fila «Aparte» = AUTORIZADA SOLO S1.0 y nota fechada.
- 29 documentos más con una nota fechada de las 20:59 añadida al final (texto anterior conservado), incluidos los de `auditoria_integral/` y el paquete de decisión de la autorización.
- `logs/verificacion_semantica_fase0.py` (A1 actualizado; nuevos S5c, S17 y A5; 83 pruebas), `logs/prueba_mutacion_semantica.py` (M10 reapuntada; nuevas M20–M23; 23 mutaciones), `logs/verificacion_coherencia_posterior.py` (X5c/X5d y tupla de autoexclusión).
- `auditoria_integral/05`, `07` (R16), `08` y `12` (filas, cifras y §14); `MANIFEST.sha256` e `INVENTARIO_PUBLICADO.sha256` (regenerados).
Cifras tras la ronda: 163 archivos; manifiestos de 161 y 162 líneas; 223 blobs.
