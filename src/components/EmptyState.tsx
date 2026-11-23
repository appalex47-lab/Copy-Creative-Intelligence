import { useId, type ReactNode } from 'react';

interface EmptyStateProps {
  /** Qué no hay (p. ej. «Sin actividad reciente»). */
  readonly title: string;
  /** Por qué no hay y qué se puede hacer; texto explícito, nunca datos ficticios. */
  readonly description: string;
  readonly headingLevel?: 2 | 3 | 4;
  /** Acción opcional (p. ej. un `Button`). */
  readonly action?: ReactNode;
}

/** Estado vacío explícito: sustituye a una lista sin elementos para que nunca parezca un error ni una carga. */
export function EmptyState({ title, description, headingLevel = 3, action }: EmptyStateProps) {
  const id = useId();
  const Heading = `h${headingLevel}` as const;
  return (
    <section className="empty-state" aria-labelledby={id}>
      <Heading id={id} className="empty-state-title">
        {title}
      </Heading>
      <p>{description}</p>
      {action}
    </section>
  );
}
