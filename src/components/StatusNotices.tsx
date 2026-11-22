interface AsyncStatusProps {
  readonly status: 'loading' | 'success' | 'error';
  readonly loadingLabel?: string;
}

/**
 * Región de estado PERSISTENTE (siempre en el DOM) para que los lectores de pantalla anuncien los cambios
 * de carga → éxito. Los errores se anuncian aparte con `ErrorNotice` (role="alert").
 */
export function AsyncStatus({ status, loadingLabel = 'Cargando…' }: AsyncStatusProps) {
  return (
    <div
      role="status"
      aria-live="polite"
      aria-atomic="true"
      className={status === 'loading' ? 'status-region' : 'status-region sr-only'}
    >
      {status === 'loading' ? loadingLabel : status === 'success' ? 'Contenido cargado.' : ''}
    </div>
  );
}

interface ErrorNoticeProps {
  readonly message: string;
  /** Si se entrega, se muestra el botón "Reintentar". */
  readonly onRetry?: (() => void) | undefined;
}

export function ErrorNotice({ message, onRetry }: ErrorNoticeProps) {
  return (
    <div role="alert" className="error-notice">
      <p>{message}</p>
      {onRetry && (
        <button type="button" onClick={onRetry}>
          Reintentar
        </button>
      )}
    </div>
  );
}
