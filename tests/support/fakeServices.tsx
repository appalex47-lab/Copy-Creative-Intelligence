import { render } from '@testing-library/react';
import type { ReactElement } from 'react';
import { ServicesProvider } from '@/hooks/ServicesContext';
import { createDemoServices } from '@/services/adapters/demo/demoServices';
import type { Services } from '@/services/contracts';

/** Servicios DEMO con sobrescrituras parciales para simular fallos. */
export function servicesWith(overrides: Partial<Services> = {}): Services {
  return { ...createDemoServices('test'), ...overrides };
}

export function renderWithServices(ui: ReactElement, services: Services) {
  return render(<ServicesProvider services={services}>{ui}</ServicesProvider>);
}

/** Texto con forma de dato interno sensible: nunca debe aparecer en la interfaz. */
export const INTERNAL_DETAIL = 'ERR_INTERNO_TABLA_secreta_stack_xyz';
