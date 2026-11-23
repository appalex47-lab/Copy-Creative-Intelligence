import type { AppSettings } from '@/domain/settings';

/** Aplica el tema: `system` sigue la preferencia del sistema (sin atributo); `light` y `dark` lo fuerzan. */
export function applyTheme(
  theme: AppSettings['theme'],
  root: HTMLElement = document.documentElement,
) {
  if (theme === 'system') delete root.dataset['theme'];
  else root.dataset['theme'] = theme;
}
