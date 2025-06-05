import React from 'react';

interface SearchResult {
  left: string[];
  keyword: string;
  right: string[];
  start: number;
  end: number;
  pos_tags?: string[];
  next_word?: string;
  next_pos?: string;
  entity_label?: string;
}

interface ResultsDisplayProps {
  results: SearchResult[];
  loading?: boolean;
}

export const ResultsDisplay: React.FC<ResultsDisplayProps> = ({ results, loading }) => {
  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (results.length === 0) {
    return (
      <div className="text-center py-8 text-gray-500">
        検索結果がありません
      </div>
    );
  }
  return (
    <div className="space-y-4">
      <div className="bg-gray-50 p-4 rounded-lg">
        <p className="text-sm text-gray-600">検索結果: {results.length}件</p>
      </div>
      <div className="divide-y divide-gray-200">
        {results.map((result, index) => (
          <div key={index} className="py-4">
            <div className="flex items-center space-x-1 font-mono text-sm leading-relaxed">
              <span className="text-gray-600">
                {result.left.join(' ')}
              </span>
              {result.left.length > 0 && <span className="text-gray-400">|</span>}
              <span className="font-bold text-white bg-blue-600 px-2 py-1 rounded shadow-sm">
                {result.keyword}
              </span>
              {result.right.length > 0 && (
                <>
                  <span className="text-gray-400">|</span>
                  <span className="text-cyan-600 font-medium">
                    {result.right[0]}
                  </span>
                  {result.right.length > 1 && (
                    <span className="text-gray-600">
                      {' ' + result.right.slice(1).join(' ')}
                    </span>
                  )}
                </>
              )}
            </div>            <div className="mt-2 flex items-center justify-between">
              <span className="text-xs text-gray-400">
                位置: {result.start} - {result.end}
              </span>
              <div className="flex items-center space-x-2 text-xs">
                <span className="bg-blue-100 text-blue-800 px-2 py-1 rounded-full">
                  キーワード
                </span>
                {result.next_word && (
                  <span className="bg-cyan-100 text-cyan-800 px-2 py-1 rounded-full">
                    コロケーション: {result.next_word}
                  </span>
                )}
                {result.pos_tags && result.pos_tags.length > 0 && (
                  <span className="bg-green-100 text-green-800 px-2 py-1 rounded-full">
                    POSタグ: {result.pos_tags.join(', ')}
                  </span>
                )}
                {result.entity_label && (
                  <span className="bg-purple-100 text-purple-800 px-2 py-1 rounded-full">
                    固有表現: {result.entity_label}
                  </span>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};
