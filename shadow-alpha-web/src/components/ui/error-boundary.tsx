"use client";

import { Component, type ReactNode } from "react";
import { AlertTriangle, RefreshCw } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false, error: null };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  handleReset = () => {
    this.setState({ hasError: false, error: null });
  };

  render() {
    if (this.state.hasError) {
      if (this.props.fallback) return this.props.fallback;

      return (
        <div className="flex items-center justify-center min-h-[400px] p-8">
          <Card className="glass-panel max-w-md w-full">
            <CardContent className="p-8 text-center">
              <div className="h-16 w-16 rounded-full bg-danger/10 flex items-center justify-center mx-auto mb-4">
                <AlertTriangle className="h-8 w-8 text-danger" />
              </div>
              <h2 className="text-xl font-display font-bold text-white mb-2">
                Quelque chose s&apos;est mal passé
              </h2>
              <p className="text-sm text-muted-foreground mb-6">
                {this.state.error?.message || "Une erreur inattendue est survenue."}
              </p>
              <Button onClick={this.handleReset} variant="secondary">
                <RefreshCw className="mr-2 h-4 w-4" />
                Réessayer
              </Button>
            </CardContent>
          </Card>
        </div>
      );
    }

    return this.props.children;
  }
}
