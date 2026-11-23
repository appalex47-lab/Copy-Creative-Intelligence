import { useEffect, useRef, type ReactNode } from 'react';
import { DemoBanner } from '@/components/DemoBanner';
import { NavMenu, type NavItem } from '@/components/NavMenu';

interface Props {
  readonly isDemo: boolean;
  readonly items: readonly NavItem[];
  readonly activeId: string;
  readonly onNavigate: (id: string) => void;
  readonly children: ReactNode;
}

export function AppLayout({ isDemo, items, activeId, onNavigate, children }: Props) {
  const mainRef = useRef<HTMLElement>(null);
  const previous = useRef<string | null>(null);

  // Al cambiar de página: actualiza el título del documento y mueve el foco al encabezado de la página
  // (así los lectores de pantalla anuncian el cambio y el teclado continúa desde el contenido nuevo).
  // No actúa en el montaje inicial ni en la doble ejecución de StrictMode.
  useEffect(() => {
    const label = items.find((i) => i.id === activeId)?.label;
    const suffix = isDemo ? ' (DEMO)' : '';
    document.title = label
      ? `${label} — Copy Creative Intelligence${suffix}`
      : 'Copy Creative Intelligence';
    if (previous.current !== null && previous.current !== activeId) {
      mainRef.current?.querySelector<HTMLElement>('h2')?.focus();
    }
    previous.current = activeId;
  }, [activeId, items, isDemo]);

  return (
    <div className="app-layout">
      <a className="skip-link" href="#contenido">
        Saltar al contenido
      </a>
      {isDemo && <DemoBanner />}
      <header className="app-header">
        <h1>Copy Creative Intelligence</h1>
        <p>Fundación técnica en construcción — identidad visual provisional</p>
      </header>
      <div className="app-body">
        <NavMenu items={items} activeId={activeId} onNavigate={onNavigate} />
        <main id="contenido" className="app-main" tabIndex={-1} ref={mainRef}>
          {children}
        </main>
      </div>
    </div>
  );
}
