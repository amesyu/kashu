import React, { useState, useCallback } from 'react';

interface FileUploadProps {
  onTextLoaded: (text: string) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onTextLoaded }) => {
  const [isDragging, setIsDragging] = useState(false);

  const handleDrag = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
  }, []);

  const handleDragIn = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(true);
  }, []);

  const handleDragOut = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    e.stopPropagation();
    setIsDragging(false);

    const files = e.dataTransfer.files;
    if (files && files[0]) {
      const file = files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        onTextLoaded(text);
      };
      reader.readAsText(file);
    }
  }, [onTextLoaded]);

  const handleFileInput = useCallback((e: React.ChangeEvent<HTMLInputElement>) => {
    const files = e.target.files;
    if (files && files[0]) {
      const file = files[0];
      const reader = new FileReader();
      reader.onload = (e) => {
        const text = e.target?.result as string;
        onTextLoaded(text);
      };
      reader.readAsText(file);
    }
  }, [onTextLoaded]);

  return (
    <div
      className={`w-full p-8 border-2 border-dashed rounded-lg text-center 
        ${isDragging ? 'border-blue-500 bg-blue-50' : 'border-gray-300'} 
        transition-colors duration-200 ease-in-out cursor-pointer`}
      onDragOver={handleDrag}
      onDragEnter={handleDragIn}
      onDragLeave={handleDragOut}
      onDrop={handleDrop}
    >
      <div className="space-y-4">
        <p className="text-lg text-gray-600">
          テキストファイルをドラッグ＆ドロップ
          <br />
          または
        </p>
        <label className="inline-block px-4 py-2 bg-blue-500 text-white rounded-lg cursor-pointer hover:bg-blue-600 transition-colors">
          ファイルを選択
          <input
            type="file"
            className="hidden"
            accept=".txt"
            onChange={handleFileInput}
          />
        </label>
      </div>
    </div>
  );
};
