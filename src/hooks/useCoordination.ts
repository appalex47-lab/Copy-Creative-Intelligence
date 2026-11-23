import { useSyncExternalStore } from 'react';
import { useServices } from '@/hooks/ServicesContext';
import type { CoordinationState } from '@/services/contracts';

/** Estado de escritura de esta pestaña (P12). */
export function useCoordination(): CoordinationState {
  const { coordination } = useServices();
  return useSyncExternalStore(coordination.subscribe, coordination.getState, coordination.getState);
}
