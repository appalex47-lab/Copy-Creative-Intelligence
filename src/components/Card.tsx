import { useId, type ReactNode } from 'react';

interface CardProps {
  readonly title: string;
  /** Nivel del encabezado; debe continuar la jerarquía de la página (el `h1` lo pone el diseño). */
  readonly headingLevel?: 2 | 3 | 4;
  readonly children: ReactNode;
}

/** Tarjeta: una región con nombre accesible tomado de su encabezado. */
export function Card({ title, headingLevel = 2, children }: CardProps) {
  const id = useId();
  const Heading = `h${headingLevel}` as const;
  return (
    <section className="card" aria-labelledby={id}>
      <Heading id={id} className="card-title">
        {title}
      </Heading>
      {children}
    </section>
  );
}
