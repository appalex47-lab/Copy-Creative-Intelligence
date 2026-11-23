import type { CoordinationService, CoordinationState } from '@/services/contracts';

/** Subconjunto de `navigator.locks` que se usa (P12: una pestaña escribe y las demás quedan en solo lectura). */
export interface LockManagerLike {
  request(name: string, callback: (lock: unknown) => unknown): Promise<unknown>;
  request(
    name: string,
    options: { ifAvailable: boolean },
    callback: (lock: unknown) => unknown,
  ): Promise<unknown>;
}

export const WRITER_LOCK_NAME = 'cci-writer';

/**
 * Coordinación entre pestañas con Web Locks. La pestaña que obtiene el bloqueo escribe; las demás quedan en solo
 * lectura y reciben el permiso AUTOMÁTICAMENTE cuando la pestaña escritora se cierra (el bloqueo se libera solo).
 * Si el navegador no ofrece Web Locks no se puede demostrar quién escribe, y se falla de forma conservadora:
 * solo lectura. Un bloqueo no se "roba" nunca.
 */
export function createTabCoordinator(
  locks: LockManagerLike | undefined,
  settleMs = 600,
): CoordinationService {
  let state: CoordinationState = locks ? 'checking' : 'reader';
  const listeners = new Set<() => void>();
  const set = (next: CoordinationState) => {
    if (state === next) return;
    state = next;
    for (const l of [...listeners]) l();
  };
  const hold = () => {
    set('writer');
    return new Promise<never>(() => undefined); // se conserva hasta que la página se cierra
  };

  if (locks) {
    void locks
      .request(WRITER_LOCK_NAME, { ifAvailable: true }, (lock) => (lock === null ? null : hold()))
      .then(
        (result) => {
          if (result !== null) return;
          // Otra pestaña escribe. Se espera un instante (p. ej. una recarga libera el bloqueo enseguida) y se pone en
          // cola: cuando el bloqueo se libere, esta pestaña pasa a escribir sin intervención.
          setTimeout(() => {
            if (state === 'checking') set('reader');
          }, settleMs);
          void locks.request(WRITER_LOCK_NAME, () => hold());
        },
        () => set('reader'),
      );
  }

  return {
    getState: () => state,
    subscribe: (listener) => {
      listeners.add(listener);
      return () => listeners.delete(listener);
    },
    whenWriter: (timeoutMs = 1500) =>
      new Promise<boolean>((resolve) => {
        if (state === 'writer') return resolve(true);
        const done = (value: boolean) => {
          clearTimeout(timer);
          listeners.delete(onChange);
          resolve(value);
        };
        const onChange = () => {
          if (state === 'writer') done(true);
        };
        const timer = setTimeout(() => done(false), timeoutMs);
        listeners.add(onChange);
      }),
  };
}

export function createBrowserTabCoordinator(): CoordinationService {
  return createTabCoordinator(typeof navigator === 'undefined' ? undefined : navigator.locks);
}
