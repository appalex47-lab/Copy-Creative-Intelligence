# Estado inicial
- Ruta: clon de trabajo `/tmp/aud2/work` (raíz git confirmada). Rama inicial `audit/fase0-operadores-cierre-v2`, HEAD `9950e709e504a8d6c4a1cf599f1af5144129b8a2`.
- Estado: solo `?? evidencia/` (3 expedientes locales sin versionar). Sin archivos modificados ni ignorados. Sin `.gitignore` raíz.
- 24 referencias de rama (8 locales, 16 remotas). No existía rama de desarrollo apropiada (ninguna `develop*`/`foundation`); `origin/main` = `6a1af24…` (sin cambios).
- 0 behind / 6 ahead de `origin/audit/fase0-operadores-cierre`: f19ec7a, c26c594, 317e466, 8c5c96e, d51bc27, 9950e70 (locales, no publicados, preservados).
- Raíz: `AUDITORIA_*` (dirs y zips), `ARTEFACTOS_REVISION_PUBLICACION`, `README.md` (una línea), `docs/fase0`, `evidencia`. No existían src/public/tests/database/supabase/evidence ni archivos de configuración Node. Sin conflictos de nombres.
- Rama nueva elegida porque no había una apropiada y para conservar los 6 commits locales como base.
