# Decisiones arquitectónicas vigentes

Vigente desde Fase 1 (browser-only). Las decisiones D2/D3 originales (Supabase/PostgreSQL, Auth, multi-organización) quedaron **superadas** y se conservan solo como historia.

- D1 React + TypeScript estricto + Vite.
- D2 Contratos tipados + adaptadores intercambiables (DEMO en memoria y local en IndexedDB).
- D3 (vigente) IndexedDB es la fuente de verdad local; Local Storage solo para preferencias ligeras; respaldo local exportar/importar. Sin servidor ni cuentas. _Reemplaza_ «PostgreSQL/Supabase como fuente de verdad».
- D4 Sin reutilizar RevNavigator. No hay entornos de servidor.
- D5 TypeScript 6.0.3 (7.x incompatible con typescript-eslint).
- D6 Herramientas acotadas a rutas de la app.
- D7 Navegación por estado (sin router) hasta que existan rutas de producto.
- D8 Hospedaje en GitHub Pages (P10), despliegue manual.
- D9 Licencia: todos los derechos reservados.
- D10 Aplazamientos P6, P7, P8, P15, Q-1…Q-6 resueltos y aprobados por el propietario: ver `evidence/CCI_FASE1_S1_13_DECISIONES_APLAZADAS_20261123T065523Z`.
