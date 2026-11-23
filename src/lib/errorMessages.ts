import type { AppError, AppErrorCode } from '@/services/contracts';

/**
 * Mensajes para la persona usuaria. Se derivan del CÓDIGO del error, nunca del texto interno
 * (que podría contener detalles técnicos). El detalle interno no se muestra en la interfaz.
 */
const MESSAGES: Readonly<Record<AppErrorCode, string>> = {
  not_found: 'No se encontró la información solicitada.',
  not_implemented: 'Esta función todavía no está disponible.',
  unavailable: 'El servicio no está disponible en este momento.',
  invalid_configuration: 'La configuración de la aplicación no es válida.',
  validation_error: 'La solicitud contiene datos no válidos.',
  conflict:
    'No se puede hacer porque hay datos que dependen de este. Elimina primero lo que depende de él.',
  storage_unavailable:
    'Este navegador no permite guardar datos locales (por ejemplo, en modo privado o con el almacenamiento bloqueado). Revisa la configuración del navegador.',
  storage_blocked:
    'El almacenamiento está en uso por otra pestaña de la aplicación. Cierra las demás pestañas e intenta de nuevo.',
  storage_quota_exceeded:
    'No hay espacio suficiente en el navegador para guardar. Libera espacio y vuelve a intentarlo.',
  storage_newer_schema:
    'Los datos guardados pertenecen a una versión más reciente de la aplicación. Actualiza la aplicación; no se modificó nada.',
  storage_read_only:
    'Esta pestaña está en solo lectura porque otra pestaña de la aplicación tiene el control de escritura. Cierra la otra pestaña; esta recibirá el control automáticamente.',
  storage_failed:
    'No se pudo completar la operación de almacenamiento. Tus datos anteriores no se modificaron. Intenta de nuevo.',
};

export const UNEXPECTED_MESSAGE = 'Ocurrió un error inesperado. Intenta de nuevo.';

export function describeError(error: AppError): string {
  return MESSAGES[error.code];
}

/** Solo tiene sentido reintentar cuando el fallo puede ser transitorio. */
export function isRetryable(code: AppErrorCode): boolean {
  return code === 'unavailable' || code === 'storage_blocked' || code === 'storage_failed';
}
