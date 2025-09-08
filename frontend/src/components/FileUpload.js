'use client';
import { useState } from 'react';
import { api } from '@/services/api';

const SUPPORTED_EXTENSIONS = '.pdf,.docx,.doc,.pptx,.ppt,.xlsx,.xls,.csv,.epub,.html,.md,.txt';

export default function FileUpload({ onUploadSuccess }) {
  const [uploading, setUploading] = useState(false);
  const [status, setStatus] = useState('');

  const handleFileUpload = async (event) => {
    const file = event.target.files?.[0];
    if (!file) return;

    try {
      setUploading(true);
      setStatus('Uploading file...');
      
      await api.uploadDocument(file);
      setStatus('File uploaded successfully!');
      
      // Trigger refresh of document list
      onUploadSuccess();
      
    } catch (error) {
      console.error('Upload error:', error);
      setStatus(`Error: ${error.message}`);
    } finally {
      setUploading(false);
    }
  };

  return (
    <div className="p-6 bg-blue-900/30 backdrop-blur-sm rounded-lg shadow-xl border border-blue-700/30">
      <h2 className="text-xl font-semibold mb-4 text-blue-100">Upload Document</h2>
      
      <input
        type="file"
        onChange={handleFileUpload}
        disabled={uploading}
        accept={SUPPORTED_EXTENSIONS}
        className="block w-full text-blue-200
          file:mr-4 file:py-2 file:px-4
          file:rounded-full file:border-0
          file:text-sm file:font-semibold
          file:bg-blue-700 file:text-blue-100
          hover:file:bg-blue-600
          file:transition-colors
          disabled:opacity-50"
      />
      
      <p className="mt-2 text-blue-300/70 text-sm">
        Supported formats: PDF, Word, PowerPoint, Excel, CSV, EPUB, HTML, Markdown, and Text files
      </p>
      
      {status && (
        <p className={`mt-2 ${
          status.includes('Error') 
            ? 'text-red-300' 
            : status.includes('success') 
              ? 'text-green-300' 
              : 'text-blue-200'
        }`}>
          {status}
        </p>
      )}
    </div>
  );
} 