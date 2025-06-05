import React, { useState } from 'react';

interface SearchFormProps {
  onSearch: (params: SearchParams) => void;
}

export interface SearchParams {
  searchTerm: string;
  inputMode: 'word' | 'pos' | 'ner';
  window: number;
  outputMode: 'kwic' | 'frequency' | 'right_sort' | 'left_sort' | 'position';
}

export const SearchForm: React.FC<SearchFormProps> = ({ onSearch }) => {
  const [searchTerm, setSearchTerm] = useState('');
  const [inputMode, setInputMode] = useState<'word' | 'pos' | 'ner'>('word');
  const [window, setWindow] = useState(5);
  const [outputMode, setOutputMode] = useState<'kwic' | 'frequency' | 'right_sort' | 'left_sort' | 'position'>('kwic');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();    onSearch({
      searchTerm,
      inputMode,
      window,
      outputMode,
    });
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div>
        <label htmlFor="search-term" className="block text-sm font-medium text-gray-700 mb-1">
          検索語
        </label>
        <input
          id="search-term"
          type="text"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
          placeholder={inputMode === 'pos' ? 'NNP, VBD など' : inputMode === 'ner' ? 'PERSON, LOCATION など' : '検索したい単語'}
          required
        />
      </div>

      <div>
        <label htmlFor="input-mode" className="block text-sm font-medium text-gray-700 mb-1">
          検索モード
        </label>
        <select
          id="input-mode"
          value={inputMode}
          onChange={(e) => setInputMode(e.target.value as 'word' | 'pos' | 'ner')}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
        >
          <option value="word">単語検索</option>
          <option value="pos">POSタグ検索</option>
          <option value="ner">固有表現検索</option>
        </select>      </div>

      <div>
        <label htmlFor="output-mode" className="block text-sm font-medium text-gray-700 mb-1">
          出力モード
        </label>
        <select
          id="output-mode"
          value={outputMode}
          onChange={(e) => setOutputMode(e.target.value as 'kwic' | 'frequency' | 'right_sort' | 'left_sort' | 'position')}
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"        >
          <option value="kwic">KWIC（キーワード順）</option>
          <option value="frequency">頻度順（コロケーション）</option>
          <option value="right_sort">右文脈順</option>
          <option value="left_sort">左文脈順</option>
          <option value="position">出現順</option>
        </select>
      </div>

      <div>
        <label htmlFor="window-size" className="block text-sm font-medium text-gray-700 mb-1">
          コンテキストウィンドウ（前後の単語数）
        </label>
        <input
          id="window-size"
          type="number"
          value={window}
          onChange={(e) => setWindow(parseInt(e.target.value) || 5)}
          min="1"
          max="10"
          className="w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
        />
      </div>

      <button
        type="submit"
        className="w-full py-2 px-4 border border-transparent rounded-md shadow-sm text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
      >
        検索
      </button>
    </form>
  );
};
