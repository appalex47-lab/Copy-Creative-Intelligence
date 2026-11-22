# 06 — Brechas, decisiones que requiere el propietario y recomendación

**Todo validado contra un diseño NO aprobado (Fase 0 no aceptada).** Ninguna decisión se resolvió aquí, incluido G-1.

## A. Discrepancias (el código difiere del diseño leído)
| ID | Brecha | Fuente | Gravedad | Decisión necesaria |
|---|---|---|---|---|
| B1 | Claves de rol `design`/`reviewer` vs `diseno`/`revisor_aprobador` | F2 l.424 | Media | D1 |
| B2 | `active` vs `activo` (diseño físico solo en fixture; `channel_formats.active` en F3) | F4 #3, F3 l.387 | Baja | D2 |
| B3 | `Membership.roles` admite lista vacía; diseño: «roles no vacío» | F2 #3, F4 #3 | Baja | D3 (¿el contrato lo impone?) |
| B4 | **Contradicción entre fuentes:** T-01 (17 permisos) y T-02 «NO APROBADA» en F2 vs «APROBADOS/vigentes» en F3 l.34 | F2, F3 | Media (afecta cualquier modelo de permisos) | D4 |

## B. Sin diseño (el diseño no define el dato)
| ID | Brecha | Efecto |
|---|---|---|
| S1 | Columnas de `profiles`, `organizations`, `memberships` (nombre visible, nombre de organización, tipos) | `displayName` y `name` sin respaldo físico |
| S2 | Entornos de la **aplicación** (`preview`, `test`) | Sin contradicción; sin respaldo |
| S3 | Contrato de errores de **lectura** de la UI (`validation_error`, etc.) | Decisión propia de la app; sin respaldo |

## C. Sin representación en el contrato (el diseño tiene más que el código)
| ID | Brecha |
|---|---|
| R-1 | Permisos (`role_permissions`, `membership_permission_grants`, `has_permission`) |
| R-2 | Operaciones de escritura y sus errores (R1–R9, `RJ001…RJ010` si se aprueba F6) |
| R-3 | 28 de 41 tablas sin prueba alguna; ninguna con RLS probada |

## D. Decisiones del propietario pendientes
| ID | Decisión | Alternativas | Mi recomendación (no vinculante) |
|---|---|---|---|
| D1 | Clave canónica de roles | (a) mantener `design`/`reviewer` y mapear en el adaptador futuro; (b) adoptar `diseno`/`revisor_aprobador`; (c) otras | (a) si la base mantiene nombres en español, mapear en el adaptador; decidir **antes** de que exista esquema físico. Lo esencial es una sola fuente de verdad |
| D2 | `active` vs `activo` | mapear en adaptador / alinear | Mapear en el adaptador: la UI no debe copiar el nombre físico |
| D3 | ¿Imponer «roles no vacío» en el contrato/DEMO? | sí / no | Sí, validar en `validateDemoDataset` (cambio pequeño); tipo no vacío opcional |
| D4 | ¿T-01 (17 permisos) y T-02 están aprobadas? ¿Dónde consta? | aprobadas / no aprobadas | Aclararlo antes de modelar permisos; mientras tanto no modelar permisos |
| D5 | `Project` | P-A…P-E (`05_…`) | P-E ahora (no tocar), documentándolo «sin respaldo»; decidir tras responder si «proyecto» = campaña. Si el propietario confirma P-A, 1.1-B lo renombra |
| D6 | R1–R9: aprobar/rechazar F6 (alternativa B, orden R1→R9, firma) | A/B/C/D | No es necesario para 1.1-B (no hay escritura); decidir antes de cualquier servicio de escritura |
| D7 | G-1 y las demás 20 decisiones de F5 | — | No resueltas; mantener «validado contra diseño no aprobado» |
| D8 | Aprobación de Fase 0 / aceptación de la v15 de la especificación | — | Prerrequisito para pasar de «provisional» a «contrato validado» |

## E. Recomendación de alcance para 1.1-B (solo si se autoriza)
Con D1–D5 respondidas, cambios acotados: (1) alineación de claves de rol o mapeo documentado (D1); (2) validación «roles no vacío» en el conjunto DEMO (D3); (3) tratamiento de `Project` según D5 (nada, renombrar o retirar); (4) comentarios de contrato que citen esta trazabilidad; (5) misma regresión de 1.0.2. **Si no se responde D1/D5, 1.1-B no cambia nada de esos puntos.** Sin Supabase, sin escritura, sin permisos.
