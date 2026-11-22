# Corrección de precisión del encabezado de ci.yml

Base: `review/cci-publication-cleanup-final` @ `4c7ed671f1bff840947c1c68dfdf34891426a2ad`.

## Cambio
`.github/workflows/ci.yml`, línea 7 (solo comentario).

- Antes: `# - No despliega ni publica la aplicación; no usa credenciales, secretos, Supabase ni servicios externos.`
- Después: `# - No utiliza credenciales ni secretos del proyecto, no se conecta a Supabase y no despliega ni publica la aplicación.`

Motivo: la afirmación «ni servicios externos» era demasiado absoluta (el workflow usa acciones de GitHub y registros de paquetes).

## Alcance
- La misma afirmación no aparece en otro documento vigente (búsqueda en el árbol fuera de `evidence/` y dentro de `evidence/`): sin otras correcciones.
- Desde `name: CI` hasta el final el archivo es idéntico al commit base; el YAML interpretado es igual.
- Sin cambios en disparadores, jobs, steps, permisos, versiones de acciones, comandos ni variables.
- No se modificaron expedientes históricos ni manifiestos.
