# Índice de conciliación de `docs/fase0/` (2026-11-22)
**Naturaleza:** índice de conciliación; **no modifica ni reescribe** ningún archivo de `docs/fase0/` (verificado: sin diferencias respecto de `main`). Aplica P3 → (b): «antecedentes históricos» y «referencia conceptual no vinculante».

## Advertencia de vigencia (aplica a los 59 archivos)
1. `docs/fase0/` documenta la **línea anterior de diseño** (G-1, G-5, G-10; modelo con PostgreSQL/Supabase, RLS, permisos y multiusuario). **No es la arquitectura vigente de CCI**, que es browser-only (un usuario por navegador; ver `01_INDICE_MAESTRO_FASE0.md`).
2. Los archivos raíz declaran «Fase 0 v3.3 COMPLETADA Y ACEPTADA COMO LÍNEA BASE DOCUMENTAL, CON LIMITACIONES» y «Fase 1 no está autorizada»; otros documentos del expediente anterior dicen «NO ACEPTADA». Esa contradicción es **C-2 y permanece abierta**. **Ninguna de esas frases acepta la Fase 0 vigente** ni autoriza la Fase 1 vigente.
3. Los 17 permisos, RLS, SQL, disparadores y la arquitectura multiusuario **no están aprobados ni son requisitos actuales** (P3, condición 5). Solo el vocabulario conceptual (campañas, piezas, versiones, aprobaciones, historial) puede consultarse, y cada concepto recuperado debe aprobarse en P4 (condiciones 3–4).
4. Los 59 archivos se leyeron **por completo por líneas únicas** (ver `12_REGISTRO_LECTURA_Y_LIMITACIONES.md` v2.1 y su limitación: no se re-mostraron duplicados exactos de líneas ya vistas); tamaño y SHA-256 de esta tabla verificados contra los archivos (0 discrepancias).

## A. Archivos raíz (5) — línea anterior; antecedente no vinculante
| Archivo | Tamaño (bytes) | SHA-256 | Clasificación |
|---|---|---|---|
| `AUDITORIA_FINAL_G1_G5_G10.md` | 183271 | `0d70ecf2a69c993b9b086aff60e1cf1726b5c29ff2d37d86b3c31853a0a27793` | Antecedente (versión v15 de la línea anterior; no vinculante) |
| `ESPECIFICACION_TECNICA_G1_G5_G10.md` | 928169 | `910cc893a4591d3f4b937def76ea60fb600edadef0c86825c703cd0153a1c6a2` | Antecedente (versión v15 de la línea anterior; no vinculante) |
| `INFORME_CIERRE_G1_G5_G10.md` | 15988 | `a09c421760922655a5edb71d6c8e9738aa60ada2a902e02cc0b91e06ff3ccce4` | Antecedente (versión v15 de la línea anterior; no vinculante) |
| `REGISTRO_HISTORICO_VERSIONES.md` | 91511 | `47bc2a5ebebfd33d10a3dbda00d28ac74a54f994b29069b242ed2a23515e3be7` | Antecedente (versión v15 de la línea anterior; no vinculante) |
| `ROADMAP_Y_TRAZABILIDAD_G1_G5_G10.md` | 53968 | `164e860f1ce8481d94fea8f850510f4cc613bb8e87084b7a4dd83aab84cc52c6` | Antecedente (versión v15 de la línea anterior; no vinculante) |

## B. Herramientas (2) — verificadores/modelos de la línea anterior
| Archivo | Tamaño | SHA-256 | Clasificación |
|---|---|---|---|
| `herramientas/modelo_estructural.py` | 332438 | `cc87236a19b924617e13346f80eb642d0dc5f0090664908d1e96d8780f4fc52a` | Histórico (no ejecutado en esta auditoría) |
| `herramientas/verificar_expediente.py` | 181862 | `1acec85dc5e76c9e004d8f2b7ed942c94826377ff240c346bee9f2792e7a035a` | Histórico (no ejecutado en esta auditoría) |

## C. Históricos (52) — versiones conservadas (`historico/`)
| Archivo | Tamaño | SHA-256 | Clasificación |
|---|---|---|---|
| `historico/AUDITORIA_FINAL_G1_G5_G10_v10_historica.md` | 99686 | `586a20f5c407901ade39eab815087fd207fe99528e74bb3e772e7f9d26a46963` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v11_historica.md` | 111397 | `cfc8066add89d050e0dab6180f7d23b843426c2f9bd4ed3300c5568bd86eb558` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v12_historica.md` | 121471 | `cdbc44464fa35080f8864a5b16ed79245cc368f90c1f19ce4138567fe1743414` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v13_historica.md` | 136372 | `3a5a7b32b69b94d9370feee31bb836975ba9b471da7d6270b65d4c7dbd3afd34` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v14_historica.md` | 165790 | `a5b57cc8f8e94fc2b9b20ba3894a8220c175d6770befe628450aeb797b7e228d` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v3_historica.md` | 7409 | `21df21970222ef3c8eb8ad5e23b236aa7852bbc85526f98b11fe6fb27950bd93` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v4_historica.md` | 18735 | `0fef2e4827a30fb264df8a4a8da10d3447ce7b00d32955fd24e03e6970d0964a` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v5_historica.md` | 22445 | `3222ee6a594dc0f1cb8b33cabe49c29e93bfa161d2ade3e811f43757cef98725` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v6_historica.md` | 44339 | `103b02d0ce401f696b1c78727af66474d668d4209e349d8dbbca15f9da94c784` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v7_historica.md` | 52220 | `ddb8f26e28c13c8cdef9d3ab3e1653f5e366d62cbc56fac006dc644992645a84` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v8_historica.md` | 66226 | `595ac923cbde40c6471523be076ffa7aee3687eacaeb14f76957f5dbd0120160` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/AUDITORIA_FINAL_G1_G5_G10_v9_historica.md` | 83744 | `82004d7836e3b4310a564614517a0f7fe752dc074d3281714c67e8e4c96cf642` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v10_historica.md` | 610939 | `3840f24c7b3dae264deb3ef068d6ab57e1503da7d09bc171423274ddec076698` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v11_historica.md` | 648733 | `25a928a9e639ac981f8c2bcc1e650741b5118b90b4b81370249d8f7adcca1404` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v12_historica.md` | 686178 | `d743011acccb813a02e19c593debd583b6fa750b958ecbc8590c04a808525f52` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v13_historica.md` | 751312 | `055c7b0b67ca49fbfabb0a1380d437cd1c2404b1a5104e7ca8fa00ea4ca5985e` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v14_historica.md` | 864519 | `ee3b32df3d5673d183496ba2cfa6d17900286a859917f27f242b6f488ae93b6d` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v2_historica.md` | 142614 | `1b57b17786bd6dd67c0cc4de826bd73502194e0e9a597c201fbbf03694d652c0` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v3_historica.md` | 221806 | `dcadd62f2d35effba71324b6e91fb54128c4ed772f1591e70fe36bf56b6921a8` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v4_historica.md` | 282512 | `1f4396c649fdd62ab469ec60cd599901c2b6ccb875c9e554428c5dff6d6bc1d8` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v5_historica.md` | 365632 | `38fc3f2ae9edce94ecd705f8a972f7deba999c4df13208b732c48876c8399e79` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v6_historica.md` | 483700 | `f557efde8ed7a04d4a3ad602e0436638404af32401b9e669d8a1514a8491de3a` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v7_historica.md` | 525789 | `f285de3ec033aab43d9978da617803034db556668ad02828feae22a4e8842fdf` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v8_historica.md` | 559699 | `3962dd534a3cd44e4f6565bdd5d93fc1f870fddb4f80a3e66d09dac5c32223f6` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ESPECIFICACION_TECNICA_G1_G5_G10_v9_historica.md` | 568254 | `d8692cadbd1e95c70b5c54878166316129ee5dcd414fe897bf7780682dcf1067` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/EXTRACCION_V2_G1_G5_G10_historica.md` | 96490 | `7af04c3fe5a5f9acb8a580f525da7397f7154553d14a397a5afcf148eade641d` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v10_historico.md` | 11058 | `59cb3d2fb4341740f445c322efcb6b76b934f6c2b478b2d18107c88d9cf4cac8` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v11_historico.md` | 12814 | `e305664c7b47b6fba6c82e49ee6bd754b1f2a7446631bfc7f22fe46caf3c316b` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v12_historico.md` | 11742 | `ceca548a3bb76748ba9ed7ca0cb0c0b67923db0dfbf22060b54346eaf302581c` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v13_historico.md` | 12361 | `ee8e010a744058e387c7cb467d0a8658cbbe230e2cbc5b2052be63d5ed16558b` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v14_historico.md` | 16253 | `261a3f149b21b8dd8e1df36a45aa03fb82b29fe967e5658f99d2d33b0f31a288` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v2_historico.md` | 12529 | `f949bd63e0453be05dd7711af1314e40077686075b99b8cac5d88d3b5fc29bb3` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v3_historico.md` | 11629 | `72d27958d8ad2591d070e16412d935ecea47be4d130c43795d6e661494e920bb` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v4_historico.md` | 11872 | `72ca4be269a0aad89adfad6f5881ba2f0cdb4f67d25230f8f8632b78a6eb9b2c` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v5_historico.md` | 13810 | `55ededfa7494113919340f82db90ecd12927a4a53e2e1affea2f7c884b130ad4` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v6_historico.md` | 8703 | `1f720820b3ec41400d087c89147fe575c2afbd2ae7da8507c6e9680f88e3b14f` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v7_historico.md` | 9599 | `54fcc0b099c4ea7bcc108bcae05668991bb6a0dfb7028b470258e71f81482b41` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v8_historico.md` | 10458 | `3a63f80acd1b4a874893771ff72ddd8afed96bcd20a50d98ea1e7c42373a6546` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/INFORME_CIERRE_G1_G5_G10_v9_historico.md` | 12044 | `19a725ed244992ea4363401eec24d543f74cef251cc9f02c4b8cd291c7ea84fe` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v10_historico.md` | 53709 | `302add91be435a50813f181ce604e13063e13e0017c776c63c3e616d8655bc31` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v11_historico.md` | 53763 | `9f4880b23a1378aa5e5e096eff9fe09990996745cdb5a4d72fbd3261f239396e` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v12_historico.md` | 53763 | `5a86e71aeb4c3dc9d95a78290a717a7684527ef408c784277e0e5634c4151776` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v13_historico.md` | 53862 | `ced4705d2aba09aadb193ec8631b4a0ea63e2dbca644b444d2588ea8b673327d` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v14_historico.md` | 53951 | `9b0ae8b1a6a29bff3e933d4fa9c25dee413153abaeac7c9d58210b883d3efa13` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v2_historico.md` | 33143 | `adea2199076db57df5744a5eb38f01a2dab00f104a688e9227ca9ac4817ef7f6` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v3_historico.md` | 35813 | `0b8d8a162430dec89e6ea6f268c52e649191220d3aa30a4ddf2d08212c7f50c4` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v4_historico.md` | 42360 | `2b87c0e546381ed52feb824d1ce09ca22a2f7b70cd21cef7882dee96f534e328` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v5_historico.md` | 50062 | `68a311e269cfb49c0df0f3039f060e8ce7df7a5d04733ac5a991354f014f958f` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v6_historico.md` | 53029 | `9e920516ed07cdf447d3513522ea1b0e215d61d89e8ed78717476b0686e48432` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v7_historico.md` | 53499 | `315fe95325a345a66df89439eeee4cac74629cc43ac325ed952f12302cd38f6c` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v8_historico.md` | 53643 | `7a8f08e90d23689ef5de42c96652af5b63e05de3fc1c7d5e7f22d0f603318691` | Histórico superado por la versión v15 de su línea; no vinculante |
| `historico/ROADMAP_Y_TRAZABILIDAD_G1_G5_G10_v9_historico.md` | 53705 | `63b26a3e4fc3ed91b367f51fc8bfe90717e36a2f55c3d7e7ff6f809fcc971f66` | Histórico superado por la versión v15 de su línea; no vinculante |
