import { useCallback, useRef, useState, type FormEvent } from 'react';
import { applyTheme } from '@/lib/theme';
import { Button } from '@/components/Button';
import { Card } from '@/components/Card';
import { AsyncStatus, ErrorNotice } from '@/components/StatusNotices';
import { DISPLAY_NAME_MAX, validateDisplayName, type LocalProfile } from '@/domain/profile';
import { THEMES, type AppSettings } from '@/domain/settings';
import { useAsyncResource } from '@/hooks/useAsyncResource';
import { useServices } from '@/hooks/ServicesContext';
import { describeError } from '@/lib/errorMessages';
import { ok } from '@/services/contracts';

const THEME_LABEL: Record<AppSettings['theme'], string> = {
  system: 'Seguir al sistema',
  light: 'Claro',
  dark: 'Oscuro',
};

/** Perfil local opcional y preferencias. El nombre es texto no confiable: React lo escapa al mostrarlo. */
export function SettingsPage() {
  const services = useServices();
  const heading = useRef<HTMLHeadingElement>(null);
  const load = useCallback(async () => {
    const [profile, settings] = await Promise.all([
      services.profile.get(),
      services.preferences.get(),
    ]);
    if (!profile.ok) return profile;
    if (!settings.ok) return settings;
    return ok({ profile: profile.value, settings: settings.value });
  }, [services]);
  const { state, retry } = useAsyncResource(load);
  const onRetry = () => {
    heading.current?.focus();
    retry();
  };

  return (
    <section aria-labelledby="titulo-ajustes">
      <h2 id="titulo-ajustes" tabIndex={-1} ref={heading}>
        Perfil y preferencias
      </h2>
      <AsyncStatus status={state.status} />
      {state.status === 'error' && (
        <ErrorNotice message={state.message} onRetry={state.retryable ? onRetry : undefined} />
      )}
      {state.status === 'success' && (
        <>
          <ProfileForm initial={state.data.profile} />
          <ThemeForm initial={state.data.settings.theme} />
        </>
      )}
    </section>
  );
}

function ProfileForm({ initial }: { readonly initial: LocalProfile }) {
  const services = useServices();
  const [saved, setSaved] = useState<string | undefined>(initial.displayName);
  const [draft, setDraft] = useState(initial.displayName ?? '');
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState('');

  const onSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setNotice('');
    const v = validateDisplayName(draft);
    if (!v.ok) {
      setError(v.reason);
      return;
    }
    setError(null);
    const r = await services.profile.save(draft);
    if (!r.ok) {
      setError(describeError(r.error));
      return;
    }
    setSaved(r.value.displayName);
    setDraft(r.value.displayName ?? '');
    setNotice(r.value.displayName ? 'Nombre guardado.' : 'Nombre borrado.');
  };
  const onClear = async () => {
    setNotice('');
    const r = await services.profile.clear();
    if (!r.ok) {
      setError(describeError(r.error));
      return;
    }
    setError(null);
    setSaved(undefined);
    setDraft('');
    setNotice('Nombre borrado.');
  };

  return (
    <Card title="Perfil local" headingLevel={3}>
      <p>
        Nombre visible actual: <strong>{saved ?? 'sin nombre'}</strong>
      </p>
      <form onSubmit={(e) => void onSubmit(e)} noValidate>
        <div className="field">
          <label htmlFor="nombre-visible">Nombre visible (opcional)</label>
          <input
            id="nombre-visible"
            type="text"
            value={draft}
            autoComplete="off"
            aria-describedby={error ? 'nombre-ayuda nombre-error' : 'nombre-ayuda'}
            aria-invalid={error ? true : undefined}
            onChange={(e) => setDraft(e.target.value)}
          />
          <p id="nombre-ayuda" className="field-hint">
            Hasta {DISPLAY_NAME_MAX} caracteres. Solo se guarda en este navegador.
          </p>
          {error && (
            <p id="nombre-error" className="field-error" role="alert">
              {error}
            </p>
          )}
        </div>
        <div className="form-actions">
          <Button type="submit" variant="primary">
            Guardar nombre
          </Button>
          <Button onClick={() => void onClear()} disabled={saved === undefined}>
            Borrar nombre
          </Button>
        </div>
        <p role="status" aria-live="polite">
          {notice}
        </p>
      </form>
    </Card>
  );
}

function ThemeForm({ initial }: { readonly initial: AppSettings['theme'] }) {
  const services = useServices();
  const [theme, setTheme] = useState(initial);
  const [notice, setNotice] = useState('');
  const [error, setError] = useState<string | null>(null);

  const onChange = async (value: string) => {
    const next = THEMES.find((t) => t === value);
    if (next === undefined) return;
    const r = await services.preferences.update({ theme: next });
    if (!r.ok) {
      setError(describeError(r.error));
      return;
    }
    setError(null);
    setTheme(r.value.theme);
    applyTheme(r.value.theme);
    setNotice(`Tema: ${THEME_LABEL[r.value.theme]}.`);
  };

  return (
    <Card title="Preferencias" headingLevel={3}>
      <div className="field">
        <label htmlFor="tema">Tema</label>
        <select id="tema" value={theme} onChange={(e) => void onChange(e.target.value)}>
          {THEMES.map((t) => (
            <option key={t} value={t}>
              {THEME_LABEL[t]}
            </option>
          ))}
        </select>
        {error && (
          <p className="field-error" role="alert">
            {error}
          </p>
        )}
      </div>
      <p role="status" aria-live="polite">
        {notice}
      </p>
    </Card>
  );
}
