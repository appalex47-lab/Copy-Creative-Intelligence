// Política de entorno y modo de datos. Módulo PURO (sin imports): lo usan la aplicación (en ejecución) y
// vite.config.ts (en build/dev/test) para que ambos apliquen exactamente la misma regla.
//
// IMPORTANTE: esto evita configuraciones ACCIDENTALES. No es una barrera de seguridad: cualquier código del
// navegador puede ser alterado por quien lo recibe. La seguridad real dependerá de Auth, RLS y backend.

export type AppEnvName = 'development' | 'test' | 'preview' | 'production';
export type DataModeName = 'demo';

export type PolicyResult =
  | { readonly ok: true; readonly appEnv: AppEnvName; readonly dataMode: DataModeName }
  | {
      readonly ok: false;
      readonly code: 'invalid_configuration' | 'not_implemented';
      readonly message: string;
    };

type RawEnv = Readonly<Record<string, string | undefined>>;

const ENVS: readonly AppEnvName[] = ['development', 'test', 'preview', 'production'];
const isEnvName = (v: string): v is AppEnvName => (ENVS as readonly string[]).includes(v);

/** Entornos donde se permite servir datos DEMO. Producción NO está en la lista. */
export const DEMO_ALLOWED_ENVS: readonly AppEnvName[] = ['development', 'test', 'preview'];

/**
 * Reglas:
 *  - `MODE` (el modo de Vite: development | test | preview | production) es obligatorio y define el entorno.
 *  - `VITE_APP_ENV` es opcional; si se define debe coincidir con `MODE` (si no, es una configuración contradictoria).
 *  - `VITE_DATA_MODE` (por defecto `demo`): solo existe `demo`; `supabase` aún no está implementado.
 *  - DEMO solo se permite en development, test y preview. Producción rechaza DEMO.
 *  - `vite preview` solo sirve un build ya generado: no es producción ni tiene backend conectado.
 */
export function evaluateEnvPolicy(raw: RawEnv): PolicyResult {
  const mode = raw['MODE'];
  if (mode === undefined || mode === '') {
    return {
      ok: false,
      code: 'invalid_configuration',
      message: 'Falta el modo de ejecución (MODE). Use development, test, preview o production.',
    };
  }
  if (!isEnvName(mode)) {
    return {
      ok: false,
      code: 'invalid_configuration',
      message: `Modo de ejecución inválido: "${mode}". Use development, test, preview o production.`,
    };
  }
  const declared = raw['VITE_APP_ENV'];
  if (declared !== undefined && declared !== '') {
    if (!isEnvName(declared)) {
      return {
        ok: false,
        code: 'invalid_configuration',
        message: `VITE_APP_ENV inválido: "${declared}".`,
      };
    }
    if (declared !== mode) {
      return {
        ok: false,
        code: 'invalid_configuration',
        message: `Configuración contradictoria: VITE_APP_ENV="${declared}" pero el modo de ejecución es "${mode}".`,
      };
    }
  }
  const dataMode =
    raw['VITE_DATA_MODE'] === undefined || raw['VITE_DATA_MODE'] === ''
      ? 'demo'
      : raw['VITE_DATA_MODE'];
  if (dataMode === 'supabase') {
    return {
      ok: false,
      code: 'not_implemented',
      message: 'El adaptador Supabase no existe todavía; no se puede usar VITE_DATA_MODE=supabase.',
    };
  }
  if (dataMode !== 'demo') {
    return {
      ok: false,
      code: 'invalid_configuration',
      message: `VITE_DATA_MODE inválido: "${dataMode}".`,
    };
  }
  if (!DEMO_ALLOWED_ENVS.includes(mode)) {
    return {
      ok: false,
      code: 'invalid_configuration',
      message:
        'Un entorno de producción no puede usar datos DEMO y aún no existe un backend real. ' +
        'Para un build local de demostración use el modo "preview" (npm run build).',
    };
  }
  return { ok: true, appEnv: mode, dataMode: 'demo' };
}
