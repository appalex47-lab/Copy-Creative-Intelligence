# LEEME — Cierre técnico, arquitectónico y documental de Fase 0 (CCI)

Expediente **complementario** a V26 (no es V27). Rama local `local/cierre-tecnico-fase0` desde `439777c9…`; **sin commit, push ni merge**. Nada se ejecutó contra Supabase.

## Orden de lectura
1. DICTAMEN_PREPARACION_FASE0.md → 2. INFORME_CIERRE_TECNICO_FASE0.md → 3. INFORME_DECISIONES_ARQUITECTONICAS.md (+ REGISTRO_DECISIONES_RECOMENDADAS.csv) → 4. MATRIZ_LIMITACIONES_RESIDUALES.csv.
Detalle: MATRIZ_12_ESCENARIOS_PARCIALES.csv, EXPEDIENTE_T409_T422.md, REVISION_22_FUNCIONES.md, MATRIZ_FUNCION_REGLA_ESCENARIO_PRUEBA.csv, MATRIZ_MODELO_LOGICO_FISICO.md, PLAN_VALIDACION_CCI_DEV.md, PRUEBAS_RLS_PRIVILEGIOS_CONCURRENCIA.md, PLAN_VALIDACION_TRIGGER_R1_R9.md.

## scripts_validacion/
- `local_ext/ejecutar_ext.sh <socket> <puerto>`; `ct_concurrencia_local.sh <socket> <puerto>`; `ct_dg19_pk_experimento.sh <socket> <puerto>`; `ct_hash_cadena_referencia.py [--pg <socket> <puerto>]`; `ct_revision_estatica_T47_T124.py <docs/fase0>`; `ct_k47_por_escenario.py <herramientas> [csv]`; generadores `ct_gen_*.py`. Usar `python3 -I -B`. Sólo clústeres PostgreSQL temporales locales.
- `cci_dev_NO_EJECUTADOS/`: scripts para CCI-DEV. **NO EJECUTADOS — REQUIEREN AUTORIZACIÓN Y CCI-DEV.** Llevan guarda `cci.validacion_autorizada='SI-CCI-DEV'`; no usar en PROD.
- `resultados/`: salidas de las corridas locales (UTF8 es la autoritativa; SQL_ASCII se conserva como contraste).

## Integridad
`MANIFIESTO_SHA256_CIERRE.txt` (verificar con `sha256sum -c` desde esta carpeta).
