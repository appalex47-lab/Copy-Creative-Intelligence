# Publicación en GitHub Pages (preparada, NO ejecutada)

## Lo preparado (en `main`)
- `vite.config.ts`: `base: './'` (rutas relativas; funciona en `/Copy-Creative-Intelligence/`). Verificado en Chrome sirviendo el build desde esa subruta: carga, guarda el nombre y persiste tras recargar, sin errores ni fallos de red.
- `index.html`: `noindex, nofollow`, título sin «DEMO».
- `.github/workflows/pages.yml`: manual (`workflow_dispatch`), ejecuta `npm run verify`, construye con `VITE_DATA_MODE=local` y despliega con acciones ancladas por SHA.
- `tests/buildGuard.test.ts`: el build usa rutas relativas y `noindex`; sin marcas DEMO.

## Lo que debe hacer el propietario para activar
1. GitHub → repositorio → Settings → Pages → **Build and deployment → Source: «GitHub Actions»** (hoy el workflow dinámico «pages build and deployment» publica la rama; con esto deja de publicar el contenido del repositorio).
2. Dar la orden de desplegar (o ejecutar Actions → «Publicar en GitHub Pages» → Run workflow).

## Riesgos conocidos
- Origen compartido `appalex47-lab.github.io` (ver `01_`). Si hay otras apps con datos locales en esa cuenta, usar dominio propio.
- Repositorio público: el código y el expediente son visibles. Licencia pendiente (P15).
- La app es solo local: cada persona (y cada navegador) tiene sus propios datos; no hay datos compartidos ni copia de seguridad en la nube.
