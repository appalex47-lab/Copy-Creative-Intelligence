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
