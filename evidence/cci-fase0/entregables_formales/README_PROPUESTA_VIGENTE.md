# Copy Creative Intelligence (CCI) — README (PROPUESTA de documentación vigente)
> Propuesta. No sustituye el `README.md` del repositorio hasta que el propietario lo autorice. El histórico no se modifica.
## Qué es
Aplicación web local para gestionar el ciclo de la comunicación comercial: brief → copy → adaptación → auditoría → validación promocional → corrección → aprobación humana → biblioteca → medición.
## Arquitectura vigente (decisión del propietario)
Un usuario por navegador; sin cuentas, login, backend, Supabase, PostgreSQL, SQL, servidor ni sincronización. IndexedDB = almacenamiento principal; Local Storage = preferencias ligeras. Un backend futuro sería solo una evolución potencial, fuera del alcance actual.
## Estado real
Existe la fundación (React 19, TypeScript estricto, Vite, adaptador DEMO en memoria, pruebas). **No existen** persistencia, módulos de producto ni IA. Detalle: `02_INVENTARIO_FUNCIONAL_CCI.md`.
## Clasificación documental
| Categoría | Qué es | Dónde |
|---|---|---|
| Histórico | Supabase/PostgreSQL/RLS/organizaciones/multiusuario; se conserva | `docs/fase0/historico`, `evidence/`, D2–D4 |
| Aceptado | infraestructura Fase 1.0/1.1 (DEMO, calidad) | expedientes `evidence/` |
| Sustituido (decisión P2, 2026-11-22; ADR redactado, **no publicado**) | partes incompatibles de DEC-D2/D3/D4, «Fuente de verdad» y «Seguridad por diseño» | `ADR_PROPUESTO_REEMPLAZO_DEC_D2_D3_D4.md` |
| Referencia conceptual no vinculante (P3 = b) | vocabulario de `docs/fase0/` y expedientes; nada se incorpora sin P4 | `INDICE_ANTECEDENTES_HISTORICOS.md` |
| Pendiente | P1–P15, Q-1…Q-6 | `13_REGISTRO_DECISIONES_PROPIETARIO.md` |
| Propuesta no aprobada | todo en este expediente | esta carpeta |
## Fases
0 Auditoría · 1 Fundamentos y Command Center · 2 Copy Studio · 3 Creative Auditor · 4 Promotion Validator y Channel Adaptation · 5 Integración. Cada una requiere autorización independiente. Ver `11_ROADMAP_FASES_0_A_5.md`.

> **Nota de actualización posterior (ronda de lectura 2026-11-22; el texto original no se altera):** la fila «Pendiente | P1–P15, Q-1…Q-6» es del momento de elaboración y contradice el estado vigente. **Resueltas por el propietario:** P1 = (b), P2 = (a), P3 = (b) con condiciones, Q-7 = (a), D-1…D-3, D-5 y D4/D6/D7/D8 (11 selecciones). **Siguen pendientes:** P4.B, P4.C, P4.E (E1–E5), P5–P15 (según su registro), Q-1…Q-6, C-2, C-3 y entidades P4.A 9–12 y 14–18 (P4.A vigente 9/18). Fuente autoritativa: `REGISTRO_DECISIONES_RESUELTAS.md`.

> **Nota fechada 2026-11-22 15:56 (ratificación del propietario «Confirmo todo» sobre la propuesta maestra B1–B10; el texto original no se altera):** P4 (A, B, C, E), P5, P9, P11, P12, P13, P14 y Q-4 quedan resueltas; P6, P7, P8, P10, P15, Q-1, Q-2, Q-3, Q-5 y Q-6 con aplazamiento aceptado. Fuente y texto literal: `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md`, sección «Ratificación de la propuesta maestra de cierre de Fase 0 (B1–B10)». Aprobaciones 0.1–0.7, aceptación de Fase 0 y autorización de Fase 1 siguen pendientes.
