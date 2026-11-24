# S2.8 — Catálogo (Campaña/Producto/Oferta), adaptaciones por canal y búsqueda de copys

Fecha: 2026-11-23. Autor: Claude, bajo delegación del propietario («Hagamos las demás funciones de la fase 2 en una sola pasada»). Decisiones revocables; el propietario no las ha validado.

## Qué se construyó
- **Catálogo** (nueva vista): campañas, productos y ofertas como registros simples (nombre ≤120, nota opcional ≤500). Nombre único por tipo sin distinguir mayúsculas ni acentos; hasta 500 por tipo. Sin precios, vigencias, estados ni relación Producto–Oferta (no están definidos por el propietario).
- **Campaña en el brief** (opcional): el brief puede referenciar una campaña registrada (`campaignId`). Una campaña en uso no se borra (`conflict`) hasta quitar la referencia. El selector copia el nombre al campo «Campaña».
- **Adaptación por canal** (función 7): entidad derivada de un copy con copy y versión de origen, canal de destino y contenido propio; se edita en su lugar. Los límites del canal se muestran solo como información; NO se audita, puntúa ni aprueba. Un copy con adaptaciones no se borra (`conflict`).
- **Búsqueda de copys** por nombre, etiqueta y texto actual/variantes (sin mayúsculas ni acentos; todas las palabras deben aparecer).
- **Persistencia**: IndexedDB v6 (`entities`, `adaptations`), respaldo v6 (acepta v1–v6; integridad referencial: brief→campaña, adaptación→copy y versión existentes; la suma canónica no cambia para versiones anteriores).

## Fuera de alcance (declarado)
Auditoría creativa y hallazgos guardados, ReglaComercial como entidad, aprobaciones (Fase 5, Q-3), resultados de desempeño, IA-B, comparación/selección de variantes (por definir).

## Verificación
- `npm run verify`: salida 0 (tipos, lint, formato, 288 pruebas unitarias, secretos, build).
- Playwright (Chrome del sistema): 86/86 en 3 corridas consecutivas.
- Pruebas nuevas: servicios de catálogo y adaptaciones, búsqueda, respaldo v6 (referencias, duplicados, versiones previas), contrato de repositorios y 4 pruebas E2E con axe.

## No verificado
Despliegue en GitHub Pages (no se desplegó), uso en móvil real, rendimiento con miles de registros.
