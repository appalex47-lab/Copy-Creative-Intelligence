# ESPECIFICACIÓN DE IDENTIDAD DE ENTORNO FIRMADA (AG-18)

Estado: **implementada y probada en local** (42/42 casos con clones físicos reales + 9 casos de cadena completa). **No hay autoridad emisora ni claves reales**: no se inventaron. Las claves de las pruebas son efímeras.

## Problema (causa raíz)
Un clon físico de PROD (`pg_basebackup`, restauración, snapshot) conserva `system_identifier`, bases, roles y tablas. Cualquier identidad guardada *dentro* de la base se clona con ella. Por eso una guarda SQL por sí sola no puede distinguir DEV de un clon de PROD (probado: ID-05). La identidad confiable debe provenir de **fuera del contenido clonable**.

## Diseño
Una **autoridad externa** (la define el propietario) firma con Ed25519 dos documentos JSON (firma separada, sobre los bytes exactos del archivo):

| Archivo | Contenido firmado |
|---|---|
| `token.json` + `token.sig` | `schema=cci-identidad-entorno/1`, `tipo=identidad_entorno`, `entorno` (CCI-DEV/CCI-PROD), `project_id`, `endpoint` (`host:puerto` tal como se conecta), `base`, `system_identifier`, `serial` (entero), `emitida_utc`, `expira_utc` (≤ 7 días), `emisor` |
| `politica.json` + `politica.sig` | `schema=cci-politica-confianza/1`, `tipo=politica_confianza`, `entornos{CCI-DEV,CCI-PROD:{proyectos_autorizados, serial_minimo, seriales_revocados}}`, `claves_revocadas_sha256`, `emitida_utc`, `expira_utc` |

La **clave pública** y su **SHA-256** los entrega el propietario por un canal ajeno al repositorio y a la base de datos (`CCI_AUTORIDAD_PUBKEY`, `CCI_AUTORIDAD_PUBKEY_SHA256`); el directorio de identidad en `CCI_IDENTIDAD_DIR`. Nada de esto puede venir de una variable de sesión, una GUC, una tabla clonada o configuración controlada por el operador de la base.

Verificador: `scripts_validacion/cci_dev_NO_EJECUTADOS/ct_identidad_entorno.py` (parte del conjunto de 11 archivos cuyo SHA-256 aprueba el custodio). Lo invoca `ejecutar_script_verificado.sh` en modo CCI-DEV **antes** de ejecutar nada; el `system_identifier` lo lee el propio ejecutor del servidor real (`pg_control_system()`).

## Por qué un clon de PROD no puede pasar como DEV
El token liga **endpoint + base + system_identifier + proyecto + entorno** y lo firma la autoridad. Un clon físico: (a) en otro endpoint → `I-ENDPOINT-DISTINTO`; (b) en el endpoint de DEV pero con el `system_identifier` de PROD → `I-SYSID-DISTINTO`; (c) con identidad PROD → `I-ENTORNO-DISTINTO`; (d) con un token copiado de la base clonada → no sirve (no se lee de la base). Deny por defecto: cualquier ausencia, alteración, caducidad o inconsistencia = rechazo.

## Códigos de rechazo (rc=3; rc=4 = error técnico, nunca confundido con aceptación)
`I-CLAVE-NO-APROBADA`, `I-CLAVE-AUSENTE`, `I-AUSENTE`, `I-POLITICA-AUSENTE`, `I-POLITICA-FIRMA-INVALIDA`, `I-POLITICA-NO-VIGENTE`, `I-POLITICA-CADUCADA`, `I-POLITICA-CONTRADICTORIA`, `I-POLITICA-VALIDEZ-EXCESIVA`, `I-CLAVE-REVOCADA`, `I-FIRMA-INVALIDA`, `I-FORMATO`, `I-VALIDEZ-EXCESIVA`, `I-NO-VIGENTE-AUN`, `I-CADUCADA`, `I-ENTORNO-NO-EN-POLITICA`, `I-ENTORNO-DISTINTO`, `I-PROYECTO-NO-AUTORIZADO`, `I-ENDPOINT-DISTINTO`, `I-BASE-DISTINTA`, `I-SYSID-DISTINTO`, `I-SERIAL-OBSOLETO`, `I-REVOCADA`, `I-ERROR-TECNICO`. En el ejecutor se prefijan `V-IDENTIDAD-…`.

## Quién emite, qué firma, dónde vive la clave, cómo se rota (procedimiento para el propietario)
1. **Definir la autoridad** (persona/sistema, p. ej. un HSM o una persona distinta del operador y del administrador de la base). Decisión del propietario; no definida.
2. **Generar el par**: `openssl genpkey -algorithm ed25519 -out autoridad.pem; openssl pkey -in autoridad.pem -pubout -out autoridad.pub`. La privada nunca sale de la autoridad. Registrar `sha256sum autoridad.pub` por un canal independiente.
3. **Emitir la política** (`politica.json`) con los `project_id` reales de CCI-DEV y CCI-PROD (un proyecto no puede estar en ambos) y firmarla: `openssl pkeyutl -sign -inkey autoridad.pem -rawin -in politica.json -out politica.sig`.
4. **Emitir el token de CCI-DEV** tras leer *en el servidor real*: `select system_identifier from pg_control_system()`, el `host:puerto` de conexión y la base. Firmar igual. Vigencia ≤ 7 días.
5. **Entregar** al operador: `token.*`, `politica.*`, `autoridad.pub`; el SHA-256 de la clave por canal aparte.
6. **Rotación**: nueva clave → nueva política y nuevos tokens firmados con ella; el verificador se ancla al SHA-256 nuevo (probado AG-32/AG-33); la clave anterior se añade a `claves_revocadas_sha256`. **Revocación** de un token: subir `serial_minimo` o listar el serial en `seriales_revocados` (probado AG-29/AG-30).
7. **Tras clonar/restaurar DEV**: emitir un token nuevo (nuevo serial/endpoint) y revocar el anterior.

## Límites honestos
- La verificación corre en el **cliente** (ejecutor). Quien tenga control total de la máquina del operador puede saltarse el ejecutor y llamar a `psql` directamente; las defensas restantes son el preflight de la guarda (hash aprobado), la autorización de operadores en la guarda SQL y los privilegios del rol en el servidor.
- Un clon físico de DEV que **ocupa el endpoint exacto** de DEV es indistinguible de DEV (probado E2E-09): no es un riesgo AG-18 (solo contiene datos de DEV).
- La autenticidad real depende de que el propietario custodie la clave y su SHA-256: es la dependencia EXT-01/EXT-02, **no resuelta**.
- Alias DNS/poolers que oculten el endpoint real: validar en CCI-DEV (EXT-02).

## Pruebas (reproducibles)
`ct_pruebas_identidad_firmada.py` (AG-00…AG-41: DEV, PROD, clon físico de DEV y de PROD, ausente, falsificada, firma inválida, firma de otro entorno, caducada, proyecto equivocado, reutilización de identidad anterior, parámetros alterados, rotación) y `ct_pruebas_ext01_y_e2e_dev.py` (E2E-01…09).
