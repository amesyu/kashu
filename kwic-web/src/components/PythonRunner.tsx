import React, { useEffect, useState } from 'react';
import { loadPyodide } from 'pyodide';
import type { PyodideInterface } from 'pyodide';

interface PythonRunnerProps {
  children: (props: {
    pyodide: PyodideInterface | null;
    loading: boolean;
    error: string | null;
  }) => React.ReactNode;
}

export const PythonRunner: React.FC<PythonRunnerProps> = ({ children }) => {
  const [pyodide, setPyodide] = useState<PyodideInterface | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function initPyodide() {
      try {
        setLoading(true);
        const pyodideInstance = await loadPyodide({
          indexURL: "https://cdn.jsdelivr.net/pyodide/v0.27.6/full/",        });        console.log('カスタムトークン化の初期化中...');

        // Load our custom Python code
        const response = await fetch('/src/python/kwic.py');
        const pythonCode = await response.text();
        await pyodideInstance.runPythonAsync(pythonCode);

        setPyodide(pyodideInstance);
        setError(null);
      } catch (err) {
        console.error('Pyodide initialization error:', err);
        setError(err instanceof Error ? err.message : '初期化エラー');
      } finally {
        setLoading(false);
      }
    }

    initPyodide();
  }, []);

  return <>{children({ pyodide, loading, error })}</>;
};
