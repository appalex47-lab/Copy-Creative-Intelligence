// GALERÍA DE COMPONENTES PARA PRUEBAS DE NAVEGADOR. No forma parte de la aplicación ni del build.
import { StrictMode } from 'react';
import { createRoot } from 'react-dom/client';
import '@/styles/global.css';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { EmptyState } from '@/components/EmptyState';

createRoot(document.getElementById('root') as HTMLElement).render(
  <StrictMode>
    <main id="contenido">
      <h1>Galería de componentes</h1>
      <Card title="Botones">
        <p>
          <Button variant="primary">Principal</Button> <Button>Secundario</Button>{' '}
          <Button disabled>Deshabilitado</Button>
        </p>
      </Card>
      <EmptyState
        title="Sin actividad reciente"
        description="Aún no hay acciones locales registradas."
        headingLevel={2}
        action={<Button>Entendido</Button>}
      />
    </main>
  </StrictMode>,
);
