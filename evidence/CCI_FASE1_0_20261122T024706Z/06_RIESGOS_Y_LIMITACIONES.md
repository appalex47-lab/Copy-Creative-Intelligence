# Riesgos y limitaciones
- Contratos y entidades provisionales; pueden no coincidir con las 41 tablas diseñadas en Fase 0.
- Fase 0 sigue FASE0_BLOCKED (PG17 ausente, Docker sin daemon, bloqueadores externos, evidencia CCI-DEV solo aportada por admin y no verificada); no se avanzó ni se cerró.
- Sin backend, auth, aislamiento por organización ni persistencia: todo es DEMO.
- Responsive y UI verificados solo por CSS/pruebas jsdom, no visualmente.
- TypeScript 6.0.3 anclado por compatibilidad con typescript-eslint; revisar al actualizar.
- Rama local no publicada: existe solo en este clon de trabajo (`/tmp`), vulnerable a pérdida si no se respalda.
- Verificador documental de Fase 0 no ejecutable (timeouts) — heredado.
