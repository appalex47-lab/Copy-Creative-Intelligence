import { fireEvent, render, screen } from '@testing-library/react';
import { describe, expect, it, vi } from 'vitest';
import { Button } from './Button';
import { Card } from './Card';
import { EmptyState } from './EmptyState';

describe('Button', () => {
  it('es un botón con nombre accesible y tipo "button" por defecto', () => {
    render(<Button>Guardar</Button>);
    const b = screen.getByRole('button', { name: 'Guardar' });
    expect(b).toHaveAttribute('type', 'button');
    expect(b).toHaveClass('btn', 'btn-secondary');
  });

  it('acepta la variante principal y el tipo "submit"', () => {
    render(
      <Button variant="primary" type="submit">
        Enviar
      </Button>,
    );
    const b = screen.getByRole('button', { name: 'Enviar' });
    expect(b).toHaveAttribute('type', 'submit');
    expect(b).toHaveClass('btn-primary');
  });

  it('llama a onClick y no lo llama si está deshabilitado', () => {
    const onClick = vi.fn();
    const { rerender } = render(<Button onClick={onClick}>Ok</Button>);
    fireEvent.click(screen.getByRole('button', { name: 'Ok' }));
    expect(onClick).toHaveBeenCalledTimes(1);
    rerender(
      <Button onClick={onClick} disabled>
        Ok
      </Button>,
    );
    expect(screen.getByRole('button', { name: 'Ok' })).toBeDisabled();
    fireEvent.click(screen.getByRole('button', { name: 'Ok' }));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('es alcanzable por teclado', () => {
    render(<Button>Ir</Button>);
    const b = screen.getByRole('button', { name: 'Ir' });
    b.focus();
    expect(b).toHaveFocus();
  });
});

describe('Card', () => {
  it('es una región con nombre tomado de su encabezado (h2 por defecto)', () => {
    render(<Card title="Resumen">contenido</Card>);
    const region = screen.getByRole('region', { name: 'Resumen' });
    expect(region).toHaveTextContent('contenido');
    expect(screen.getByRole('heading', { level: 2, name: 'Resumen' })).toBeInTheDocument();
  });

  it('respeta el nivel de encabezado pedido y genera ids distintos', () => {
    render(
      <>
        <Card title="A" headingLevel={3}>
          a
        </Card>
        <Card title="B" headingLevel={3}>
          b
        </Card>
      </>,
    );
    const [h1, h2] = screen.getAllByRole('heading', { level: 3 });
    expect(h1?.id).not.toBe('');
    expect(h1?.id).not.toBe(h2?.id);
    expect(screen.getByRole('region', { name: 'A' })).toBeInTheDocument();
    expect(screen.getByRole('region', { name: 'B' })).toBeInTheDocument();
  });
});

describe('EmptyState', () => {
  it('dice qué no hay y por qué, sin parecer un error ni una carga', () => {
    render(
      <EmptyState title="Sin actividad reciente" description="Aún no hay acciones locales." />,
    );
    expect(screen.getByRole('region', { name: 'Sin actividad reciente' })).toBeInTheDocument();
    expect(screen.getByText('Aún no hay acciones locales.')).toBeInTheDocument();
    expect(screen.queryByRole('alert')).toBeNull();
    expect(screen.queryByRole('status')).toBeNull();
  });

  it('muestra la acción opcional solo si se entrega', () => {
    const { rerender } = render(<EmptyState title="Vacío" description="d" />);
    expect(screen.queryByRole('button')).toBeNull();
    rerender(<EmptyState title="Vacío" description="d" action={<Button>Crear</Button>} />);
    expect(screen.getByRole('button', { name: 'Crear' })).toBeInTheDocument();
  });
});
