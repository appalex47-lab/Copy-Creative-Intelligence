# Estrategia de IA de CCI

> Documento formal del §14. Fuente de contenido: `../09_ANALISIS_IA.md` (sin cambios de fondo). Estado: propuesta para revisión; nada aprobado ni implementado.

Principios del propietario: la IA ayuda a crear, analizar y sugerir; reglas y cálculos son deterministas; ninguna promoción se aprueba por sugerencia de IA; la aprobación final es humana; no se exponen claves privadas en el frontend; no se guardan secretos en Local Storage ni IndexedDB.

## 1. Alternativas
| ID | Alternativa | Compatible con browser-only | Qué requiere | Riesgos | Cubre |
|---|---|---|---|---|---|
| IA-A | **Sin IA remota**: plantillas, reglas y listas de verificación deterministas | Sí | nada | capacidad limitada de generación | validación, reglas, cálculos |
| IA-B | **Flujo manual**: la app arma prompts; el usuario los usa en un proveedor externo y pega el resultado | Sí | ninguna clave en la app | fricción; el usuario decide qué datos envía | generación y sugerencias de hallazgos |
| IA-C | **Llamada directa del navegador con clave del propio usuario (BYOK)**, solo en memoria de la sesión | Técnicamente sí, **con riesgo alto** | clave ingresada en cada sesión; política CORS del proveedor (**no verificada**) | clave expuesta a XSS/extensiones/herramientas de desarrollo; costos y límites a cargo del usuario; datos salen del dispositivo | generación y análisis |
| IA-D | **Modelo local en el navegador** (WASM/WebGPU) | Sí | descarga de modelo (peso, red solo al descargar) | calidad, rendimiento y soporte de navegador **no verificados** | tareas acotadas |
| IA-E | **Servicio intermedio / backend propio** (proxy que guarde la clave) | **No** compatible con el alcance vigente | infraestructura de servidor | contradice la decisión vigente | todas |
Si el propietario eligiera IA-E, debe decidirlo expresamente: **no se implementa unilateralmente**.

## 2. Reglas propuestas
1. Nunca persistir claves (ni en Local Storage ni en IndexedDB ni en exportaciones).
2. Si se admite IA-C: clave solo en memoria; advertencia explícita de riesgos; sin telemetría; mostrar qué texto se enviará antes de enviarlo.
3. Toda salida de IA se marca como **sugerencia** con procedencia; el usuario la acepta o descarta; las puntuaciones y reglas no cambian por IA.
4. La falta de red o un fallo de IA nunca bloquea las funciones locales esenciales (se prueba en Fase 2).
5. Prompts, salidas y llaves no se escriben en logs.
6. Privacidad: el contenido comercial enviado a un proveedor queda sujeto a su política; el usuario decide.

## 3. Límites inherentes (honestos)
- Auditoría **visual**: contraste y legibilidad (relaciones de luminancia, tamaño) pueden calcularse de forma determinista en el navegador; jerarquía, distribución y congruencia copy-pieza **no** se resuelven con certeza sin IA/visión; sin IA (IA-A/IA-B) esas comprobaciones quedan como lista de verificación manual.
- Corrección ortográfica determinista requiere un **diccionario** (dependencia o recurso; P13).
- Costos, límites y capacidades de proveedores: **no evaluados** en esta fase.

## 4. Recomendación (no es decisión)
Para Fases 1–2: IA-A + IA-B (sin claves en la app) como base; evaluar IA-C solo si el propietario acepta sus riesgos. IA-D como opción de investigación posterior. Decisión: P8.
