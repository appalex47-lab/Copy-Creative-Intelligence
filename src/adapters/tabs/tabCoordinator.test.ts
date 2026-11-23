import { describe, expect, it, vi } from 'vitest';
import { createTabCoordinator, type LockManagerLike } from './tabCoordinator';

/** Web Locks simulado: un bloqueo exclusivo con cola y liberación explícita. */
function fakeLocks() {
  let held = false;
  const queue: (() => void)[] = [];
  let release: () => void = () => undefined;
  const grant = (cb: (l: unknown) => unknown) => {
    held = true;
    const p = Promise.resolve(cb({ name: 'x' }));
    release = () => {
      held = false;
      queue.shift()?.();
    };
    return p;
  };
  const locks: LockManagerLike = {
    request: (_name: string, a: unknown, b?: unknown) => {
      const opts = typeof a === 'function' ? undefined : (a as { ifAvailable: boolean });
      const cb = (typeof a === 'function' ? a : b) as (l: unknown) => unknown;
      if (!held) return grant(cb);
      if (opts?.ifAvailable) return Promise.resolve(cb(null));
      return new Promise((resolve) => queue.push(() => resolve(grant(cb))));
    },
  } as LockManagerLike;
  return { locks, free: () => release() };
}
const tick = () => new Promise((r) => setTimeout(r, 0));

describe('coordinación entre pestañas (P12)', () => {
  it('la primera pestaña escribe; la segunda queda en solo lectura y recibe el control al liberarse', async () => {
    vi.useFakeTimers();
    const { locks, free } = fakeLocks();
    const a = createTabCoordinator(locks, 50);
    await vi.advanceTimersByTimeAsync(0);
    expect(a.getState()).toBe('writer');
    const b = createTabCoordinator(locks, 50);
    await vi.advanceTimersByTimeAsync(0);
    expect(b.getState()).toBe('checking');
    await vi.advanceTimersByTimeAsync(60);
    expect(b.getState()).toBe('reader');
    const seen: string[] = [];
    b.subscribe(() => seen.push(b.getState()));
    free(); // la pestaña A se cierra
    await vi.advanceTimersByTimeAsync(0);
    expect(b.getState()).toBe('writer');
    expect(seen).toEqual(['writer']);
    vi.useRealTimers();
  });

  it('whenWriter: true si escribe, false si no lo obtiene a tiempo, true si el permiso llega antes del límite', async () => {
    vi.useFakeTimers();
    const { locks, free } = fakeLocks();
    const a = createTabCoordinator(locks, 50);
    await vi.advanceTimersByTimeAsync(0);
    expect(await a.whenWriter(10)).toBe(true);
    const b = createTabCoordinator(locks, 50);
    await vi.advanceTimersByTimeAsync(0);
    const timedOut = b.whenWriter(100);
    await vi.advanceTimersByTimeAsync(101);
    expect(await timedOut).toBe(false);
    const waits = b.whenWriter(1000);
    free();
    await vi.advanceTimersByTimeAsync(0);
    expect(await waits).toBe(true);
    vi.useRealTimers();
  });

  it('sin Web Locks se falla de forma conservadora: solo lectura, nunca escritura', async () => {
    const c = createTabCoordinator(undefined);
    expect(c.getState()).toBe('reader');
    expect(await c.whenWriter(5)).toBe(false);
  });

  it('un error al pedir el bloqueo deja solo lectura', async () => {
    const broken: LockManagerLike = {
      request: () => Promise.reject(new Error('x')),
    } as LockManagerLike;
    const c = createTabCoordinator(broken, 10);
    await tick();
    await tick();
    expect(c.getState()).toBe('reader');
  });
});
