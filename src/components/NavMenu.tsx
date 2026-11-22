export interface NavItem {
  readonly id: string;
  readonly label: string;
}

interface Props {
  readonly items: readonly NavItem[];
  readonly activeId: string;
  readonly onNavigate: (id: string) => void;
}

/** Navegación inicial por estado (sin enrutador: aún no hay rutas de producto). */
export function NavMenu({ items, activeId, onNavigate }: Props) {
  return (
    <nav className="nav-menu" aria-label="Navegación principal">
      <ul>
        {items.map((item) => (
          <li key={item.id}>
            <button
              type="button"
              aria-current={item.id === activeId ? 'page' : undefined}
              onClick={() => onNavigate(item.id)}
            >
              {item.label}
            </button>
          </li>
        ))}
      </ul>
    </nav>
  );
}
