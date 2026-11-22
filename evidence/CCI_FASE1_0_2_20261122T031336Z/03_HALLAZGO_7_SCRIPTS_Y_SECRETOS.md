# Hallazgo 7 — scripts, ESLint y escáner de secretos
Original: los `.mjs` no pasaban por ESLint (ningún bloque de configuración los cubría; `eslint scripts` no devolvía nada); patrones limitados; archivos comprimidos omitidos en silencio.
Corrección: bloque ESLint para `**/*.{js,mjs,cjs}` (recomendado + globals de Node), `**/*.mts` en el bloque TS, `eslint . --max-warnings 0` con lista explícita de exclusiones (docs, evidencia, evidence, AUDITORIA_*, ARTEFACTOS_*, builds). Verificado: un `.mjs` con variable indefinida falla (`no-undef`).
Escáner: +14 patrones (Supabase sbp_, Stripe, npm, Hugging Face, Groq, SendGrid, .npmrc, Authorization, además de Cohere/AWS/GitHub/Google/Slack de 1.0.1), nombres de archivos secretos (`*.pem`, `*.key`, `id_rsa`, `credentials.json`, `.netrc`, `.envrc`), marcadores de ejemplo ignorados, sin imprimir valores, ZIP/TAR **listados como NO inspeccionados** (hoy 2 ZIP en la raíz), ruta opcional. 43 pruebas con valores ficticios construidos por partes.
Límites documentados en `docs/architecture/CONTROL_DE_SECRETOS.md`. No se afirma haber revisado el contenido de ningún ZIP.
Resultado: PASS (heurístico).
