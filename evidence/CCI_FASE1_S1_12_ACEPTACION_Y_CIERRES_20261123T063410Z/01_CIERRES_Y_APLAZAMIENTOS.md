# Cierres y aplazamientos (decisiones de Claude bajo delegación, revocables)

## Resuelto con decisión del propietario
- **P10 Hosting y origen:** el propietario decidió (2026-11-23 00:26) «Todo se va a alojar en GitHub Pages». Condiciones que Claude registra: origen de Pages de proyecto (`https://appalex47-lab.github.io/Copy-Creative-Intelligence/`); build con rutas relativas y `noindex`; despliegue manual por workflow (`pages.yml`); **riesgo vigente:** el almacenamiento es por ORIGEN y `appalex47-lab.github.io` es compartido por todas las páginas de proyecto de esa cuenta (cualquier otra app publicada ahí puede leer la base `cci` y las preferencias `cci.prefs.v1`). Mitigación: claves con prefijo `cci`; solución completa: dominio propio para esta app. Ver `02_`.

## Cerradas por Claude (sin objeto)
- **C-2 y C-3:** son verificaciones de ciclos de claves foráneas (`contribution_events` ↔ `creative_assets`) del diseño de servidor PostgreSQL v3.3 (documentos históricos, P3). La arquitectura vigente es solo navegador (IndexedDB), sin PostgreSQL ni claves foráneas, y P1 eliminó los «cinco roles» (D-04). Se cierran como **sin objeto** (superadas por P1/P2/P3). Reabrir solo si se reintroduce un servidor.

## Siguen aplazadas (no las cierro: dependen de datos del negocio o de una fase futura)
| Id | Qué falta | Vence | Qué necesito del propietario |
|---|---|---|---|
| P6 Formato de exportación | decidir si el formato de respaldo de Fase 1 (JSON v1) pasa a ser el de exportación de contenido | antes de F2 | confirmar o cambiar |
| P8 IA alternativa y claves | política de claves y proveedor | antes de F2 | decidir |
| Q-6 Idioma y diccionario | español inicial (ya usado); fuente del diccionario | antes de F2 | fuente del diccionario |
| Q-5 Puntuación de auditoría | categorías y pesos | F3 | define los pesos |
| Q-1 Redondeo/tolerancia del descuento | valores (rec.: 2 decimales «mitad hacia arriba», tolerancia en puntos porcentuales) | F4 | valores |
| Q-2 Canales y reglas | límites reales por canal | F4 | aporta límites (no se inventan) |
| P7 Cifrado local | frase de paso | F5 | decidir |
| Q-3 Estados de Workflow | aprobar los 7 estados propuestos | F5 | aprobar |
| P15 Pendientes previos | licencia (publicar sin licencia es riesgo), enlace de sesión, etc. | antes de F5 (la licencia, antes de publicar) | decidir licencia |
