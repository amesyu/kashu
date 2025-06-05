import { useState } from 'react';
import { FileUpload } from './components/FileUpload';
import { SearchForm, type SearchParams } from './components/SearchForm';
import { ResultsDisplay } from './components/ResultsDisplay';
import { PythonRunner } from './components/PythonRunner';

function App() {
  const [text, setText] = useState<string>('');
  const [results, setResults] = useState<any[]>([]);
  const [searching, setSearching] = useState(false);

  const handleSearch = async (pyodide: any, params: SearchParams) => {
    if (!text) return;
    
    try {
      setSearching(true);
      const searchResults = await pyodide.runPythonAsync(`kwic_search("""${text}""", """${params.searchTerm}""", input_mode="${params.inputMode}", output_mode="${params.outputMode}", window=${params.window})`);
      setResults(searchResults);
    } catch (error) {
      console.error('Search error:', error);
      setResults([]);
    } finally {
      setSearching(false);
    }
  };

  return (
    <PythonRunner>
      {({ pyodide, loading, error }) => (
        <div className="min-h-screen bg-gray-50 py-8">
          <div className="max-w-4xl mx-auto px-4">
            <h1 className="text-3xl font-bold text-gray-900 mb-8 text-center">
              KWIC検索
            </h1>

            {error ? (
              <div className="bg-red-50 border border-red-400 text-red-700 px-4 py-3 rounded relative mb-4">
                <strong className="font-bold">エラー: </strong>
                <span className="block sm:inline">{error}</span>
              </div>
            ) : loading ? (
              <div className="text-center py-12">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto"></div>
                <p className="mt-4 text-gray-600">Pythonランタイムを初期化中...</p>
              </div>
            ) : (
              <div className="space-y-8">
                {!text && (
                  <div className="bg-white shadow-sm rounded-lg p-6">
                    <FileUpload onTextLoaded={setText} />
                  </div>
                )}

                {text && (
                  <>
                    <div className="bg-white shadow-sm rounded-lg p-6">
                      <SearchForm
                        onSearch={(params) => handleSearch(pyodide, params)}
                      />
                    </div>

                    <div className="bg-white shadow-sm rounded-lg p-6">
                      <ResultsDisplay results={results} loading={searching} />
                    </div>
                  </>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </PythonRunner>
  );
}

export default App;
