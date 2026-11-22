# Ejecución

- `npm run dev`: servidor de desarrollo (modo DEMO).
- `npm run build` y `npm run preview`: build local de preview y su servidor.
  `npm run build` genera el build de **preview** (modo `preview`, DEMO). `npm run build:production` falla a propósito (producción no admite DEMO y no hay backend). `npm run preview` solo sirve el build ya generado (no es producción). `VITE_DATA_MODE=supabase` se rechaza con `not_implemented`. Ver ENTORNOS_Y_MODO_DEMO.md.
