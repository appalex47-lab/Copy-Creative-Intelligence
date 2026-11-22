# Ficha Q-7 — ¿La entidad «Campaña» de la instrucción vigente y la decisión F11-D5 (retiro de `Project`)?
Estado: **RESUELTA por el propietario el 2026-11-22 → (a)**, con 5 condiciones (ver `REGISTRO_DECISIONES_RESUELTAS.md`). Esta ficha conserva el planteamiento original.
**Pregunta:** ¿Cómo se incorpora `Campaña` al dominio browser-only sin reabrir F11-D5, sin equiparar `Project` con `Campaña` y sin recuperar `Project` por inferencia?
## Contexto y problema (leído de los registros originales)
- **F11-D5 (dictamen B0–B5):** «Retirar Project»; aplicada: retirado de dominio, contrato, DEMO, `HomePage`, pruebas y documentos vigentes; «sin Campaign». Corresponde a la alternativa **P-D** del registro `05_PROJECT_PENDIENTE_DE_DECISION.md` («eliminar `Project` del contrato hasta que exista el diseño»).
- Ese mismo registro dice: «Por instrucción del propietario no se asume que `Project` equivale a `campaigns`». En el diseño histórico existe `campaigns` («agrupa el trabajo — padre de briefs, piezas, promociones»); ninguna tabla se llama `project`.
- Tus instrucciones vigentes piden `Campaign`/«Campañas»: Fase 0 A l.348; maestra B l.197, l.347 (campo del Brief), l.597 (Library), l.639 (Performance).
- Es entidad padre de Brief, Oferta, Pieza y Resultado: sin ella no se puede cerrar P4.4.
## Opciones y consecuencias
| Opción | Qué implica | Consecuencias |
|---|---|---|
| (a) **Campaña es una entidad nueva del dominio browser-only, definida por tus instrucciones vigentes; F11-D5 se conserva intacta como historia** | No hay equivalencia ni migración con `Project`; el vocabulario de `campaigns` histórico sigue siendo solo referencia no vinculante (P3) | Satisface tu lista sin tocar F11-D5; hay que registrar que Campaña **no** restituye `Project`; el código de `Project` ya no existe y no se recupera |
| (b) Equiparar expresamente `Project` = `Campaña` (alternativa P-A) | Decisión tuya explícita de que «proyecto» y «campaña» son el mismo concepto | Reinterpreta F11-D5 (el retiro pasaría a ser un renombre); contradice la cautela original de no asumir la equivalencia; más ambiguo en la trazabilidad |
| (c) No incluir `Campaña` en el dominio | Brief, Oferta, Pieza y Resultado sin padre | Contradice tus listas A y B; Library y Performance pierden su eje (campaña) |
## Recomendación razonada
**(a).** Es la única que cumple tu lista sin inferir equivalencias ni reabrir F11-D5: el retiro de `Project` fue una decisión sobre un concepto sin respaldo; `Campaña` es un concepto que tú has definido después y de forma explícita. Criterio mío; tú decides.
## Documentos y módulos afectados
`05_MODELO_DOMINIO_CCI.md`, `06_MODELO_DATOS_CCI.md`, `07`, `FICHA_P4.md` (P4.4), `LISTA_ORIGINAL_18_ENTIDADES.md`, `CONCILIACION_D1_D9_VERIFICADA.md`. Módulos: Copy Studio, Command Center, Library, Performance Intelligence. **No** se toca el repositorio.
## Relación con decisiones anteriores
F11-D5 se **conserva íntegra** y no se invalida retroactivamente. Se apoya en P3 (el vocabulario histórico no es vinculante) y en P1 (sin multiusuario). Condiciona P4.4.
## Dependencias y efecto de no decidir
Bloquea P4.4 y por ello la aprobación 0.3. Sin respuesta, Fase 1 no puede fijar la raíz del dominio.
## Respuesta
`Q-7 → (a)` — **respondida** (2026-11-22).
