# Estado Git y declaración de operaciones

> **AVISO DE VIGENCIA (ronda final 2026-11-22; el contenido original no se altera).** Copia previa del expediente (raíz): **histórica / propuesta anterior**. No constituye estado vigente ni acepta Fase 0 ni autoriza Fase 1. Estado vigente y jerarquía de fuentes: `00_INDICE_VIGENTES_E_HISTORICOS.md`, `entregables_formales/REGISTRO_DECISIONES_RESUELTAS.md` y `auditoria_integral/01_INDICE_MAESTRO_FASE0.md`.

## Estado de partida (verificado al iniciar esta fase)
- Clon auditado (solo lectura): rama `integration/cci-fase1-1-accepted`, HEAD `ffb47bc319db0806250bcecf91d390fa59fa0d70`, árbol limpio (0 entradas, incl. ignorados). Es una rama **local**, no publicada.
- Base: `7bcba74e05577761081d68ca14fdc19f2400248d`; 5 commits propios: `7822410` (B1–B3), `6bfff37` (docs B5), `5cee199` (corrección E2E), `ad602d3` (expediente B4–B5, con sus logs), `ffb47bc` (expediente E2E).
- GitHub (`ls-remote`, lectura): 20 ramas; `main` = `6a1af2424ef39e0960b8f7e09d4e19ec52e6f046` sin cambios; rama `review/cci-auditoria-fase0-browser-only` = `8f6ef104b464520280a571a7c94e9c35cf0137da` (un archivo); ninguna rama `integration/*`.
- Los 7 manifiestos de expedientes de aplicación verifican con 0 fallos en checkout limpio (verificado en la fase de auditoría de commits y en la entrega).
## Operaciones Git de esta fase (Fase 0)
**Realizadas:** ninguna sobre el repositorio de desarrollo. Solo lectura (`git archive`, `ls-remote`, `status`, `rev-parse`).
**No realizadas:** commit, push, PR, merge, modificación de `main`, release, despliegue, cambio de visibilidad, Supabase/SQL, cambio de credenciales o permisos, instalación de dependencias, modificación de código o documentos del repositorio.
## Operaciones previas en esta conversación (por transparencia; todas con autorización expresa del propietario)
- Commits **locales** de preservación (rama `integration/cci-fase1-1-accepted`; reescritura de los dos últimos commits locales).
- **Un push** de una rama nueva al repositorio **público** (`review/cci-auditoria-fase0-browser-only`, commit `8f6ef10…`, un único archivo `docs/auditorias/INFORME_AUDITORIA_FASE0_BROWSER_ONLY.md`), ordenado expresamente por el propietario a las 10:16. La instrucción maestra posterior (§10) dice no usar el repositorio público como sustituto de uno privado: **esa rama ya existe y es pública**; su eliminación requiere autorización expresa.
- `appalex47-lab/CCI-Evidence`: **no existe/inaccesible** para esta sesión; la creación falló por permisos (403). Nada subido allí. La autorización para crearlo expiró con ese intento; no presupongo que cubra nuevas publicaciones.
## Respecto del destino privado (§10 de la instrucción)
No existe acceso privado confirmado: este expediente se entrega como adjuntos descargables y no se afirma que ChatGPT pueda acceder a ningún repositorio privado.
