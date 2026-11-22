# Entornos y protección del modo DEMO

| Entorno          | Cómo se obtiene                                             | DEMO          | Backend       |
| ---------------- | ----------------------------------------------------------- | ------------- | ------------- |
| Desarrollo local | `npm run dev` (modo `development`, con React StrictMode)    | permitido     | ninguno       |
| Pruebas          | `vitest` (modo `test`) y arnés e2e                          | permitido     | ninguno       |
| Preview          | `npm run build` (modo `preview`) + `npm run preview`        | permitido     | ninguno       |
| Producción       | `vite build --mode production` (`npm run build:production`) | **rechazado** | aún no existe |

- `vite preview` solo **sirve un build ya generado**; no es producción ni tiene backend conectado. Por eso el script `preview` usa `--mode preview`.
- El modo de Vite (`MODE`) define el entorno. `VITE_APP_ENV` es opcional y, si se define, debe coincidir; si no, es una configuración contradictoria y falla.
- `VITE_DATA_MODE` por defecto es `demo`; `supabase` se rechaza (`not_implemented`) hasta que exista el adaptador.
- Una regla única (`src/app/envPolicy.ts`) se aplica en **build/dev/test** (plugin `cci-env-guard` en `vite.config.ts`: el build falla con mensaje claro) y **en ejecución** (`parseEnv` en `main.tsx`: si el bundle llegara a estar mal configurado, muestra un error de configuración y nunca datos DEMO).
- La interfaz siempre muestra el aviso DEMO y la página «Estado de conexión» (entorno y «no conectada a ningún backend»).

## Alcance real de la protección

Evita configuraciones **accidentales**. No es una garantía de seguridad: el código del navegador puede ser alterado por quien lo recibe, y cualquier modo puede construirse localmente. La seguridad real dependerá de Auth, RLS y backend (fases futuras, no implementadas). Mientras no exista backend, un build de producción **no puede** generarse con este repositorio, a propósito.
