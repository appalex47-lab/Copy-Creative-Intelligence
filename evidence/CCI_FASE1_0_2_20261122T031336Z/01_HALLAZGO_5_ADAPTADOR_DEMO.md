# Hallazgo 5 — consistencia del adaptador DEMO
Original: `memberships.listForOrganization` devolvía lista vacía para una organización inexistente; `projects` devolvía `not_found`.
Corrección: semántica uniforme documentada (`docs/architecture/SEMANTICA_DE_SERVICIOS.md` y comentario en el contrato): parámetro inválido → `validation_error` (código nuevo, aditivo); padre inexistente → `not_found`; padre existente sin elementos → lista vacía; fallo ≠ lista vacía. El adaptador valida la integridad referencial de su conjunto de datos y se niega a crearse si es inconsistente. `AppState.environment` admite `preview`.
Escenarios probados (21 pruebas en `demoServices.test.ts`): org existente sin membresías/proyectos; org inexistente; parámetro inválido (vacío, espacios, undefined, null, número, objeto); org válida con datos; integridad (membresía→org inexistente, membresía de usuario inexistente, proyecto→org inexistente, duplicados, origin, prefijo); sin escritura ni autenticación.
«Usuario inexistente»: no existe contrato por usuario → no aplica a nivel de contrato (se valida en el dataset). Sin reglas de negocio ni permisos multiusuario inventados.
Resultado: PASS.
