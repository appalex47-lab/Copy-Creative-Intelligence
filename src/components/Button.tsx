import type { ButtonHTMLAttributes } from 'react';

interface ButtonProps extends Omit<ButtonHTMLAttributes<HTMLButtonElement>, 'className' | 'type'> {
  /** `primary` para la acción principal de una zona; `secondary` para el resto. */
  readonly variant?: 'primary' | 'secondary';
  /** Por defecto `button`: nunca envía un formulario sin que se pida. */
  readonly type?: 'button' | 'submit' | 'reset';
}

/** Botón reutilizable. El foco visible y el tamaño táctil mínimo vienen de los estilos globales. */
export function Button({ variant = 'secondary', type = 'button', ...rest }: ButtonProps) {
  return <button {...rest} type={type} className={`btn btn-${variant}`} />;
}
