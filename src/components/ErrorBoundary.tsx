import { Component, type ReactNode } from 'react';
import { ErrorNotice } from '@/components/StatusNotices';
import { UNEXPECTED_MESSAGE } from '@/lib/errorMessages';

interface Props {
  readonly children: ReactNode;
}
interface State {
  readonly failed: boolean;
}

/** Captura errores inesperados de renderizado. No muestra mensajes ni trazas internas. */
export class ErrorBoundary extends Component<Props, State> {
  override state: State = { failed: false };

  static getDerivedStateFromError(): State {
    return { failed: true };
  }

  override componentDidCatch(error: Error): void {
    console.error('[cci] error de renderizado:', error.name);
  }

  override render(): ReactNode {
    if (this.state.failed) {
      return (
        <ErrorNotice
          message={UNEXPECTED_MESSAGE}
          onRetry={() => this.setState({ failed: false })}
        />
      );
    }
    return this.props.children;
  }
}
