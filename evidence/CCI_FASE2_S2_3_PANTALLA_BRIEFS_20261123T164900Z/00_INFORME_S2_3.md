# Fase 2, S2.3 — Servicio y pantalla de Briefs (AC2-01, AC2-02, AC2-04 parcial)

Fecha: 2026-11-23. Ejecutado por Claude (delegación total del propietario).

## Entregado
- `BriefService` (listar, leer, guardar, borrar). Ids y fechas los pone el servicio; guardar con un id desconocido no crea nada; toda escritura pasa por `writable()` (solo la pestaña escritora guarda, P12). Modo local (IndexedDB) y DEMO (memoria).
- Pantalla «Briefs» (segunda opción del menú): lista con estado Completo/Incompleto y el motivo por campo; formulario con los 13 campos (obligatorio/opcional indicado; canal solo los 7 aprobados; vigencia con fechas); borrador incompleto se guarda; error por campo al guardar, foco en el primero con error, se limpia al corregir; editar; borrar con confirmación; estado vacío explícito.
- Compatibilidad: respaldo (v2) ya incluía briefs desde S2.2; ahora se ven y editan.

## Defectos propios hallados por las pruebas y corregidos
1. El registro rechazaba lo que enviaba el formulario (vigencia vacía `{from:'',to:''}` se trataba como clave no permitida). Solo lo detectó el E2E; se añadió prueba unitaria.
2. Validar al salir de un campo insertaba el mensaje de error y desplazaba el botón «Guardar» justo antes del clic, perdiendo el clic. Ahora se valida al guardar y se revalida al escribir solo si el campo ya tiene error.
3. El foco volvía al título antes de que el formulario desapareciera; ahora vuelve después del renderizado.

## Verificación
- 218 pruebas unitarias; typecheck, lint, formato, secretos y build (verify = 0).
- E2E Chrome 153: 79 pruebas; 3 pruebas nuevas de Briefs (crear incompleto → persistir → completar → borrar; campo inválido; segunda pestaña en solo lectura), con axe sin violaciones, y la vista Briefs incluida en la matriz de anchos 320–1440 px y ambos temas.
- 7 corridas completas consecutivas en verde y 48 repeticiones de Briefs/multitab sin fallo.
- **Intermitencia no explicada:** 1 de las 8 corridas completas posteriores a los cambios tuvo 1 prueba fallida cuyo nombre no se registró; no se reprodujo en 55 corridas posteriores. Se declara abierta.

## Supuestos de Claude (reversibles)
Orden de campos del formulario, textos de ayuda, confirmación de borrado en línea, «Briefs» como segunda opción del menú; la actividad local no registra eventos de briefs.

## No verificado
Teclado/lector de pantalla real en el formulario; navegadores distintos de Chrome 153; uso con muchos briefs; duplicar/comparar/etiquetar/buscar (cortes siguientes).
