import { createContext, useContext, type ReactNode } from 'react';
import type { Services } from '@/services/contracts';

const ServicesContext = createContext<Services | null>(null);

export function ServicesProvider({
  services,
  children,
}: {
  services: Services;
  children: ReactNode;
}) {
  return <ServicesContext.Provider value={services}>{children}</ServicesContext.Provider>;
}

// eslint-disable-next-line react-refresh/only-export-components -- hook de contexto, patrón estándar
export function useServices(): Services {
  const services = useContext(ServicesContext);
  if (services === null) throw new Error('useServices debe usarse dentro de <ServicesProvider>');
  return services;
}
