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
};

export const UNEXPECTED_MESSAGE = 'Ocurrió un error inesperado. Intenta de nuevo.';

export function describeError(error: AppError): string {
  return MESSAGES[error.code];
}

/** Solo tiene sentido reintentar cuando el fallo puede ser transitorio. */
export function isRetryable(code: AppErrorCode): boolean {
  return code === 'unavailable';
}
