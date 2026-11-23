# Leyendas y términos de marca — decisiones (2026-11-23)

Decididas por el propietario en chat; diseño por Claude. Revocables.

## Decisiones del propietario
- **Permiso/aviso de publicidad: se omite.** La app no pedirá, validará ni marcará como faltante el permiso de publicidad ni su clave. (La empresa no lo coloca en sus piezas.) Claude no lo ha verificado jurídicamente; ver advertencia en el informe del chat.
- **Leyendas y términos de marca: configurables** por el usuario, no fijos en el código.

## Diseño (se construye en S2.5, antes de las reglas de copy)
- Leyenda: texto, canales a los que aplica, obligatoria sí/no, categoría de producto opcional. Activar/desactivar, editar, borrar. Auditoría: obligatoria y ausente = hallazgo faltante.
- Término de marca: texto, tipo (prohibido/preferido), severidad (crítica/mayor/menor/aviso), sustituto sugerido opcional. Coincidencia sin distinguir mayúsculas ni acentos, por palabra completa.
- Todo vive en IndexedDB y entra en el respaldo (export/import).
- Sin leyendas cargadas por defecto: la lista de leyendas parte vacía; el propietario las captura.

## Términos de marca de ejemplo (plantilla editable, NO validada; el usuario puede borrarlos o cambiarlos)
Prohibidos: "cura" (mayor), "milagro" (mayor), "garantizado" (mayor), "100% efectivo" (mayor), "sin efectos secundarios" (crítica), "adelgaza rápido" (mayor), "el mejor" (menor), nombres de competidores (menor, el propietario los captura).
Preferidos: "te acompañamos", "consulta a tu médico", "disponible en", "precio especial".
Sin reglas de sustitución automática: solo se sugiere, nunca se reescribe solo.
