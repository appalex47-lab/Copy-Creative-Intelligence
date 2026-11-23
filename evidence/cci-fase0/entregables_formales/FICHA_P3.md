# Ficha P3 — Tratamiento de `docs/fase0/` y de los expedientes de Supabase/SQL/RLS/multiusuario
Estado: **RESUELTA por el propietario el 2026-11-22 → (b), con condiciones** (ver `REGISTRO_DECISIONES_RESUELTAS.md`).
**Pregunta:** ¿Se conservan solo como antecedente histórico, o además como referencia **no vinculante** para el vocabulario del dominio local? (¿Y se migra algo?)
## Contexto y problema (verificado en `ffb47bc`)
- `docs/fase0/`: **59 archivos** = 5 documentos principales + 52 en `historico/` + 2 en `herramientas/`. Describen un diseño de servidor: **41 tablas, 231 reglas, 780 escenarios** (`AUDITORIA_FINAL_G1_G5_G10.md`) y **17 permisos** (`ESPECIFICACION_TECNICA…md`).
- Contiene vocabulario de producto reutilizable: `copy_versions` (105 menciones), `creative_pieces`/piezas (85), `approvals` (70), `activity_logs`, `campaigns` (6).
- Estado documental **no uniforme**: el informe de cierre dice que la «Fase 0 v3.3» fue aceptada como línea base documental **con limitaciones** y que el complemento v15 (G-1, G-5, G-10) está pendiente de aceptación formal; el encabezado de la especificación v3.3 dice lo contrario (es la contradicción **C-2**, abierta, F11-D9). Los 17 permisos constan **no aprobados** (F11-D4). **Nada de esto se ejecutó** (el propio informe: sin SQL, Supabase ni PostgreSQL).
- Otros materiales del mismo enfoque: `supabase/README.md`, `database/README.md`, `INTEGRACION_SUPABASE_ESTADO.md` y los expedientes de `evidence/` que mencionan CCI-DEV/CCI-PROD.
- P2 ya resuelta: PostgreSQL/Supabase dejan de ser fuente de verdad, así que estos materiales son **históricos en lo arquitectónico**. P3 decide solo si además sirven como **referencia de vocabulario**.
## Opciones y consecuencias
| Opción | Qué implica | Consecuencias |
|---|---|---|
| (a) Solo histórico | Se conservan sin uso; nada se toma de ellos | Separación limpia; se pierde la oportunidad de reutilizar vocabulario y trazabilidad de ideas |
| (b) Histórico + referencia no vinculante | Se consultan para nombres y conceptos; **ningún elemento entra al dominio sin aprobarlo en P4, entidad por entidad** | Aprovecha el vocabulario sin presentarlo como trabajo aceptado para browser-only (exigencia tuya); requiere marcar su estatus en el índice |
| (c) Migrar partes al nuevo diseño | Se adaptan tablas, reglas o escenarios | Reintroduce complejidad de servidor (RLS, disparadores, claves foráneas compuestas) que IndexedDB no tiene; mayor esfuerzo y riesgo de arrastrar supuestos no aprobados |
**Qué no cambia con ninguna opción:** los archivos originales no se modifican ni se borran; el marcado de estatus iría en índices o documentos **nuevos**, no dentro de los originales.
## Recomendación razonada
**(b).** Conserva todo el antecedente, permite reutilizar nombres y conceptos útiles y mantiene el control: lo que entre al dominio lo apruebas tú en P4. (c) importa conceptos de servidor que no aplican.
## Documentos y módulos afectados
En este expediente: `../03_CONCILIACION_DOCUMENTAL.md`, `05_MODELO_DOMINIO_CCI.md` (nota de procedencia de vocabulario), `README_PROPUESTA_VIGENTE.md` y el índice. En el repositorio: **ningún cambio** (`docs/fase0/`, `supabase/`, `database/`, `evidence/` se conservan). Módulos: ninguno de producto; influye en el vocabulario de Copy Studio, Creative Auditor y Workflow & Approvals si eliges (b).
## Relación con decisiones anteriores
Se apoya en P2 (resuelta). Respeta F11-D4 (permisos no aprobados), F11-D8 y F11-D9 (Fase 0 anterior no aprobada y C-2/C-3 abiertas): no las reabre; el destino de esas Fase 0 anteriores se trata en P15. Informa P4; no sustituye a P4.
## Dependencias y efecto de no decidir
Sigue a P2; informa P4 y la aprobación 0.1. Sin respuesta queda ambiguo el estatus de estos documentos; no hay impacto técnico inmediato.
## Respuesta
`P3 → (b)` — **respondida** (2026-11-22).
