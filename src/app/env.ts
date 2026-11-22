import { fail, ok, type Result } from '@/services/contracts';
import { evaluateEnvPolicy, type AppEnvName, type DataModeName } from './envPolicy';

// Variables de entorno PÚBLICAS (todo VITE_* termina en el navegador). Aquí nunca van secretos.
export interface AppEnv {
  readonly appEnv: AppEnvName;
  readonly dataMode: DataModeName;
}

type RawEnv = Readonly<Record<string, string | undefined>>;

/** Aplica la política de entorno (la misma que valida el build) y la expresa como `Result`. */
export function parseEnv(raw: RawEnv): Result<AppEnv> {
  const policy = evaluateEnvPolicy(raw);
  if (!policy.ok) return fail(policy.code, policy.message);
  return ok({ appEnv: policy.appEnv, dataMode: policy.dataMode });
}
