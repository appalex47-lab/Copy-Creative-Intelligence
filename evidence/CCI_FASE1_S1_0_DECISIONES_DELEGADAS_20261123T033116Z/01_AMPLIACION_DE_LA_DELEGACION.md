# Ampliación de la delegación (2026-11-22 21:43)

**Texto literal del propietario:** «Ya te dije, autorizo todo lo que tú consideres y creas necesario. Ya no necesitas de ahora en adelante mis autorizaciones. Si tú lo estás haciendo como un especialista en las aristas para el mejor desarrollo de la aplicación, tú tienes toda la autoridad para hacerlo.»

## Cómo la interpreta Claude
- Las subfases S1.3 en adelante de la Fase 1 quedan autorizadas por el propietario, y Claude decide su orden y su contenido. Se trabaja en la rama `fase1/s1-0-auditoria` o en ramas `fase1/*` derivadas, con commit y push solo a ellas.
- Cada decisión se registra aquí o en el expediente como **decisión de Claude bajo delegación**, revocable por el propietario.

## Límites que Claude se impone (no por falta de autoridad, sino por riesgo)
- **Merge a `main`, deploy, publicación externa y borrado de datos de terceros:** no se hacen sin una orden expresa de esa acción concreta (la autorización del 20:59 los prohibía y la delegación no los menciona).
- **No se inventan hechos de negocio.** Los atributos, eventos y valores se derivan de los documentos aprobados; lo que no tiene fuente se deja como supuesto marcado y reversible, nunca como hecho.
- **C-2, C-3 y los aplazamientos** solo se resuelven si una subfase los necesita, con el motivo escrito.
- **Fase 2 y la aceptación de la Fase 1:** quedan fuera; la aceptación exige evidencia independiente de esta sesión.
- Sigue vigente: arquitectura solo navegador, sin cuentas, backend ni sincronización.

## Fuentes aprobadas disponibles para S1.3
- Perfil local: nombre visible **opcional**, tratado como texto no confiable (P1, P4.3).
- Configuración de la aplicación: cinco categorías documentadas (tema, idioma, última vista, avisos vistos, copia de la fecha del último respaldo), sin valores ni defaults.
- Evento de actividad: entidad aprobada, estructura y eventos **sin especificar**: Claude los especificará como supuesto marcado, sin contenido del usuario.
