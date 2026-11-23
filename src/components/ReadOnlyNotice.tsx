import { useCoordination } from '@/hooks/useCoordination';

/** Aviso visible cuando otra pestaña tiene el control de escritura (P12). */
export function ReadOnlyNotice() {
  if (useCoordination() !== 'reader') return null;
  return (
    <div role="status" aria-live="polite" className="error-notice" data-testid="solo-lectura">
      <p>
        <strong>Solo lectura.</strong> Otra pestaña de la aplicación tiene el control de escritura.
        Aquí puedes ver tus datos pero no cambiarlos. Cierra la otra pestaña: esta recibirá el
        control automáticamente.
      </p>
    </div>
  );
}
