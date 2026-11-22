# Auditoría de seguridad previa a la publicación de `review/cci-fase1-1-audit`

Fecha de la auditoría: 2026-11-22 (UTC). Rama base: `origin/main` = `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046`.
Repositorio: `appalex47-lab/Copy-Creative-Intelligence` — **público** (`private: false`, `visibility: public`, comprobado con la API REST de GitHub).

## 1. Alcance
193 archivos (192 nuevos + `README.md` modificado) listados en `INVENTARIO_ARCHIVOS.txt` (ruta, bytes, SHA-256). Este informe y los dos archivos de inventario no se listan a sí mismos.
Código y pruebas (`src/`, `tests/`, `e2e/`, `scripts/`, `public/`), configuración reproducible (`package.json`, `package-lock.json`, `tsconfig*.json`, `vite.config.ts`, `eslint.config.js`, `playwright.config.ts`, `.prettier*`, `.gitignore`, `.env.example`, `index.html`, `.github/workflows/ci.yml`), documentación de la aplicación (`docs/architecture|decisions|product|roadmap`, `database/README.md`, `supabase/README.md`, `README.md`) y los expedientes `evidence/CCI_FASE1_0_*`, `…1_0_1_*`, `…1_0_2_*`, `…1_1_*`, `…1_1_A1_*` descomprimidos, con sus manifiestos.

**Excluido:** `docs/fase0/`, `evidencia/` (31 archivos de Fase 0), `AUDITORIA_*`, `ARTEFACTOS_*`, ZIP/tar/bundles, `node_modules/`, `dist/`, `test-results/`, `.env*` reales (no existen), respaldos.

## 2. Métodos
1. Escáner del proyecto (`scripts/check-secrets.mjs`) sobre la copia de los archivos: **OK, sin secretos**.
2. Escáner independiente (expresiones regulares propias, no las del proyecto) sobre todos los archivos de texto: claves privadas, JWT, AWS, tokens de GitHub/Slack/Google/Supabase, `sk-`, cadenas de conexión, `Authorization: Bearer`, asignaciones `password/secret/token/api_key`, cadenas largas, correos, IPv4, teléfonos, rutas locales, URL privadas y nombres propios: **0 coincidencias** en las 12 familias de credenciales (claves privadas, JWT, AWS, GitHub, `sk-`, Slack, Google, Supabase, URL de Supabase, cadenas de conexión, Bearer, asignaciones) y en correos e IPv4.
3. Búsqueda por nombre de archivos sensibles (`.env*`, `.pem`, `.key`, `.npmrc`, credenciales): solo `.env.example` (revisado: solo valores no secretos y comentarios).
4. Revisión visual de las 15 capturas PNG (hoja de contactos): solo la interfaz DEMO («Persona DEMO», «Organización DEMO»); sin datos personales; sin metadatos EXIF/texto en los PNG.
5. `package-lock.json`: los 262 enlaces `resolved` apuntan a `registry.npmjs.org`; sin registros privados; `package.json` sin `preinstall/postinstall/prepare`.
6. Historial: las rutas seleccionadas (salvo `README.md`) **no tienen historial** en ninguna rama local ni remota (`git log --all` sobre esas rutas: 0 commits). `README.md` solo tiene el commit inicial en `origin/main` (28 bytes). La rama se construye desde `origin/main` sin importar historia.

## 3. Hallazgos que no son secretos (documentados, sin ocultar ni modificar)
| Hallazgo | Archivos | Valoración |
|---|---|---|
| Rutas de directorios temporales del entorno de trabajo (`/tmp/aud2`, `/tmp/clean102`, `/home/claude`) | 8 logs de expedientes 1.0/1.0.1/1.0.2, `01_ESTADO_INICIAL_REPOSITORIO.md` (1.0), `01_ESTADO_GIT_Y_PRESERVACION.md` (1.1-A1) | Rutas de sandbox, sin usuario real ni datos privados. **No se editaron** para no invalidar los manifiestos de los expedientes |
| URL `http://localhost:4173/5173/5198/5199` | `playwright.config.ts`, `e2e/*`, logs de 1.0 y 1.0.2 | Locales; sin exposición |
| Identificador `appalex47` | `evidence/CCI_FASE1_0_…/00_RESUMEN_EJECUTIVO.md` (nombre del repositorio) | Ya público en la URL del repositorio |
| Valores ficticios con forma de secreto | `tests/secrets.test.ts` | Construidos por partes y claramente de prueba (secuencias `a1B2c3D4…`); el escáner del proyecto los trata como fixtures del test. Posible aviso de escáneres externos: no verificado |
| Cadenas hexadecimales/hash largas | manifiestos SHA-256, logs de Vite/Playwright | Hashes de integridad y de chunks; no credenciales |
| Teléfonos (falsos positivos del patrón) | `package-lock.json` (versiones), `npm_outdated.txt`, trazas | Números de versión, no teléfonos |

## 4. Decisiones de selección que debes revisar
1. **`.github/workflows/ci.yml` incluido.** `npm run format:check` y `npm run verify` fallan (código 2, «No files matching the pattern: .github») si `.github` no existe. Sin modificar código, la única forma de que `verify` sea reproducible fue incluir el archivo. Disparadores: `pull_request`, `push` solo a `development/**` y `workflow_dispatch`; por tanto **no se ejecuta con el push de esta rama**. Permisos `contents: read`, sin secretos, sin despliegue; acciones ancladas a `@v4` (sin verificar). Si prefieres no publicarlo, hay que decidir cómo ajustar `format:check` (cambio de código).
2. **Logs dentro de los expedientes.** Se pidió excluir logs y a la vez incluir los expedientes con sus manifiestos; se conservaron los `logs/` de cada expediente porque los manifiestos los cubren y son evidencia. No hay logs sueltos fuera de ellos.
3. **`README.md` de `origin/main` reemplazado** en esta rama (el original tenía 28 bytes: solo el título). El cambio existe únicamente en la rama de revisión.
4. No se incluyó LICENSE y no se eligió licencia (`docs/decisions/LICENCIA_PENDIENTE.md`).

## 5. Verificación de reproducibilidad en la copia limpia
`npm ci` + `npm run verify` (typecheck, lint con 0 avisos, prettier, 130/130 pruebas, secretos, build en modo preview): código de salida 0. `npm run test:e2e` (Chrome real, axe, responsive): 29/29. Sin cambios en archivos rastreados tras las ejecuciones.

## 6. Limitaciones
- Escaneo heurístico: no garantiza ausencia total de secretos; ZIPs no inspeccionados (no hay ninguno en la selección).
- No se inspeccionó el historial de commits de la rama original porque no se publica.
- No se verificó el comportamiento de GitHub secret scanning / push protection ante los fixtures ficticios.
- Las rutas de sandbox permanecen visibles en los logs de evidencia por decisión de conservar los manifiestos.
