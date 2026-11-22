# ADR-001 (PROPUESTO, NO PUBLICADO) — Reemplazo de las partes incompatibles de DEC-D2, DEC-D3, DEC-D4, del apartado «Fuente de verdad» y del apartado «Seguridad por diseño»
**Estado:** redactado en el expediente documental por decisión **P2 = (a)** del propietario (2026-11-22). **No está publicado en el repositorio ni en GitHub.** Publicarlo, o anotar los documentos del repositorio, requiere una autorización específica posterior.
**Fecha de la decisión:** 2026-11-22 (P2 = (a)); **alcance ampliado el mismo día** para incluir «Seguridad por diseño» (ver `REGISTRO_DECISIONES_RESUELTAS.md`). La ampliación se limita al expediente: no autoriza modificar el repositorio ni publicar. **Decide:** propietario del proyecto. **Referencias:** `docs/decisions/DECISIONES.md` (commit `ffb47bc319db0806250bcecf91d390fa59fa0d70`), `docs/architecture/ARQUITECTURA.md` §«Fuente de verdad».
## 1. Contexto
Los registros DEC-D2, DEC-D3 y DEC-D4 y el apartado «Fuente de verdad» responden a una arquitectura con backend remoto (Supabase/PostgreSQL). La decisión vigente del propietario es: aplicación web local, un usuario por navegador, sin cuentas, autenticación, backend, servidor ni sincronización multidispositivo, con IndexedDB como almacenamiento principal.
## 2. Decisión (alcance literal del propietario)
Se declaran **históricas** las partes incompatibles de los registros siguientes. Los textos originales se **conservan íntegros e intactos**; este ADR no los reescribe.
| Registro | Texto original (sin alterar) | **Queda reemplazado (histórico)** | **Permanece vigente** |
|---|---|---|---|
| DEC-D2 | «Contratos tipados + adaptadores intercambiables; DEMO ahora, Supabase futuro no conectado.» | Supabase como implementación prevista o dependencia de la arquitectura actual. Una eventual implementación con backend requerirá **una nueva decisión del propietario** | La separación entre contratos y adaptadores como principio arquitectónico |
| DEC-D3 | «PostgreSQL/Supabase como fuente de verdad; caché local solo después.» | Íntegro: PostgreSQL y Supabase ya no son la fuente de verdad de CCI. La persistencia principal es **IndexedDB en el navegador** | — |
| DEC-D4 | «Entornos CCI-DEV y CCI-PROD independientes; no reutilizar RevNavigator.» | CCI-DEV y CCI-PROD como proyectos Supabase independientes dejan de ser requisitos de la arquitectura vigente | — (la instrucción de no reutilizar proyectos Supabase de RevNavigator se conserva como **antecedente histórico, no como requisito operativo**; la arquitectura vigente no utiliza Supabase) |
| «Fuente de verdad» (`ARQUITECTURA.md`) | «PostgreSQL/Supabase será la fuente central; IndexedDB/localStorage solo como caché futura. Hoy no hay persistencia.» | Íntegro | Nueva formulación vigente en el apartado siguiente |
| «Seguridad por diseño» (`ARQUITECTURA.md`) | «Sin claves en el cliente (`VITE_*` es público); `.env*` ignorados salvo `.env.example`; los roles del cliente son informativos, la autoridad será el backend (RLS, funciones, Edge Functions). No hay autenticación ni aislamiento por organización simulados.» | Los planteamientos de **autoridad del backend, RLS, funciones y Edge Functions**, el carácter «informativo» de los roles del cliente y el **aislamiento por organización** como objetivo | «Sin claves en el cliente» y «`.env*` ignorados salvo `.env.example`»; «no hay autenticación ni aislamiento por organización simulados» (consistente con la decisión vigente; **sentido conservado, a confirmar**) |

**Fuente de verdad vigente:** los datos operativos se conservan **localmente en el navegador**. No hay cuentas, autenticación, backend, servidor ni sincronización multidispositivo. La **exportación e importación local** forman parte de la estrategia de respaldo y recuperación (diseño en `08_RESPALDO_IMPORTACION_RECUPERACION.md`, propuesta).
## 2 bis. Formulación vigente de seguridad (aplicación local, un usuario por navegador)
**Alcance:** aplicación local sin backend, cuentas ni permisos multiusuario. La seguridad se limita a lo que el navegador puede ofrecer y **no promete confidencialidad frente a otras personas con acceso al dispositivo, al perfil del navegador o al mismo origen**.
- **Sin autoridad externa:** ninguna regla de acceso se hace cumplir por un servidor; no existen permisos ni roles de autorización (P1). Las validaciones comerciales y de integridad son del código local.
- **Datos locales no protegidos:** IndexedDB y Local Storage **no cifran** y **no son una frontera de seguridad**; cualquier persona o programa con acceso al perfil del navegador, y cualquier script del **mismo origen**, puede leerlos y modificarlos. El almacenamiento es por origen, no por ruta.
- **Amenazas reales a documentar:** XSS y contenido de usuario no confiable; extensiones y software malicioso del equipo; acceso físico o compartido al dispositivo; archivos cargados (tipo, tamaño y contenido no confiable); exportaciones en claro (el archivo exportado hereda la exposición del lugar donde se guarda); cadena de suministro de dependencias; borrado o expulsión de datos por el navegador o por el usuario.
- **Secretos:** no se incluyen claves en el código distribuido ni se guardan secretos en IndexedDB o Local Storage (se conserva la parte vigente de la formulación original).
- **Responsabilidades del usuario:** proteger su dispositivo y sesión, custodiar sus exportaciones y respaldarse; la aplicación no puede garantizar recuperación automática.
- **Controles técnicos propuestos (sujetos a P13 y a su fase; no decididos):** escape de contenido, validación estricta de importaciones, límites de tipo y tamaño de archivos, ausencia de ejecución de contenido importado, revisión de dependencias. Detalle de diseño: `04_ARQUITECTURA_BROWSER_ONLY.md` y `08_RESPALDO_IMPORTACION_RECUPERACION.md`.

## 3. Conservación histórica
- No se borra ni se reescribe DEC-D2, DEC-D3, DEC-D4 ni ningún registro histórico (incluidos DEC-D1, D5–D7 y F11-D1–D9, que **no** se tocan).
- No se modifican retroactivamente las aceptaciones anteriores (Fase 1.0/1.1, B1–B3): fueron válidas en su momento y su historia se conserva.
## 4. Alternativas no adoptadas
(b) Solo una nota; (c) no tocar.
## 5. Lo que este ADR NO cubre (no se amplía el alcance)
- Otros textos del repositorio que repiten el enfoque anterior (`README.md`, `ROADMAP.md`, `INTEGRACION_SUPABASE_ESTADO.md`, `.env.example`, `supabase/`, `database/`): se tratarían con su propia autorización.
- La política de entorno y `VITE_DATA_MODE` (P9), las dependencias y `AppErrorCode` (P13), el tratamiento de `docs/fase0` (P3).
- Una eventual evolución a backend: requiere nueva decisión del propietario.
## 6. Consecuencias
**Documentales (futuras, con autorización):** publicar este ADR; marcar en `DECISIONES.md` y `ARQUITECTURA.md` (apartados «Fuente de verdad» y «Seguridad por diseño») el estado de los registros sin borrar el texto; realinear `README.md` y `ROADMAP.md`.
**Técnicas (futuras, con Fase 1 autorizada):** el código no contiene Supabase; subsisten el tipo `'backend'` en `DataOrigin`/`AppState.dataMode`, el rechazo de `VITE_DATA_MODE=supabase` como `not_implemented` y las guardas anti-Supabase, que deberán reevaluarse en P9 y P13. Los contratos y adaptadores siguen siendo la base.
