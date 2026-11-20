# Informe de reproducción desde una copia del paquete (V22, 2026-11-20)

Se copió `05_LOGS_Y_EVIDENCIAS/` a un directorio temporal (sin Git, sin acceso al repositorio) y se ejecutó:

| Prueba | Comando (desde `arbol_original_docs_fase0/`) | Resultado | Comparación con lo archivado |
|---|---|---|---|
| 22 funciones | `python3 -I evidencia_v16/instrumentar_22_funciones_v20.py herramientas ESPECIFICACION_TECNICA_G1_G5_G10.md` | `TOTAL funciones=22 casos=366 fallos=0` (≈71 s) | Idéntica línea por línea a `salida_22_funciones_V21_corrida3.txt`, salvo la línea `EXIT=0` que el archivo añade |
| Verificador completo | `env -i … python3 -I herramientas/verificar_expediente.py --dir . --v33 ../original_externo_v3_3/fase0_v3_3_integral.md` | 59 comprobaciones, 59 aprueban; 28/28 controles; 300/300 mutaciones (≈21 min); el v3.3 empaquetado tiene SHA-256 `b5dccdc7…c1da` | Idéntica a `salida_verificador_V21_corrida1.txt` salvo las líneas `EXIT=0` y `DURACION_S` |
| Manifiesto V21 (`v21_manifiesto.py --verificar`) | ídem | 8 de 9 controles PASS (entradas, v3.3, rutas, cobertura, hashlib, `sha256sum -c`, regenerable). **FAIL esperado**: «historico/ idénticos al commit V20», porque compara con el commit V20 vía Git y la copia no tiene repositorio | No es una discrepancia de contenido; es una dependencia de Git |

Salidas de esta reproducción: `04_RESULTADOS_DE_PRUEBAS/V22_reproduccion_desde_copia/`.

## No reproducido desde el paquete
- Batería V21 (46 pruebas) y controles negativos (26): requieren el repositorio Git (consultan el commit V20); se re-ejecutaron en el repositorio original antes de empaquetar: batería 46/46 PASS e integridad V21 TODO PASS (2026-11-20 09:1x local).
- PostgreSQL 63 pruebas y 14 mutaciones: requieren binarios de PostgreSQL 16 y un clúster temporal; **no se volvieron a ejecutar en V22**; se conservan las salidas originales (V20 y V21 corrida 3).
- Lo que depende de CCI-DEV, Supabase o el esquema físico no existe ni se ejecutó.
