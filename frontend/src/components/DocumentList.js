'use client';
import { useEffect, useState } from 'react';
import { api } from '../services/api';

export default function DocumentList({ documents, setDocuments }) {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deletingFiles, setDeletingFiles] = useState(new Set());

  const fetchDocuments = async () => {
    try {
      setError(null);
      const response = await api.getDocuments();
      console.log('API Response:', response);
      setDocuments(response.files || []);
    } catch (error) {
      console.error('Error fetching documents:', error);
      setError(error.message);
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (filename) => {
    try {
      setDeletingFiles(prev => new Set([...prev, filename]));
      await api.deleteDocument(filename);
      await fetchDocuments(); // Refresh the list
    } catch (error) {
      console.error('Error deleting document:', error);
      setError(`Error deleting ${filename}: ${error.message}`);
    } finally {
      setDeletingFiles(prev => {
        const newSet = new Set(prev);
        newSet.delete(filename);
        return newSet;
      });
    }
  };

  useEffect(() => {
    fetchDocuments();
    
    const interval = setInterval(() => {
      fetchDocuments();
    }, 2000);

    return () => clearInterval(interval);
  }, []);

  return (
    <div className="p-6 bg-blue-900/30 backdrop-blur-sm rounded-lg shadow-xl border border-blue-700/30">
      <h2 className="text-xl font-semibold mb-4 text-blue-100">Documents</h2>
      
      {loading && (
        <p className="text-blue-200">Loading documents...</p>
      )}
      
      {error && (
        <p className="text-red-300">Error: {error}</p>
      )}
      
      {!loading && !error && documents.length === 0 && (
        <p className="text-blue-200/70">No documents uploaded yet</p>
      )}
      
      {!loading && !error && documents.length > 0 && (
        <ul className="space-y-2">
          {documents.map((doc) => (
            <li key={doc.name} className="text-blue-100 bg-blue-800/30 p-2 rounded flex items-center gap-3">
              <button
                onClick={() => handleDelete(doc.name)}
                disabled={deletingFiles.has(doc.name)}
                className="w-5 h-5 flex items-center justify-center rounded-full 
                  bg-gray-600/50 hover:bg-gray-500/50 disabled:bg-gray-800/50 
                  transition-colors duration-200 text-xs"
                title="Delete document"
              >
                {deletingFiles.has(doc.name) ? (
                  <span>...</span>
                ) : (
                  <span>×</span>
                )}
              </button>
              
              <span className="flex-grow">{doc.name}</span>
              
              <div className="flex-shrink-0">
                {doc.status === 'processing' ? (
                  <span className="text-yellow-300 text-sm">Processing...</span>
                ) : doc.status === 'completed' ? (
                  <span className="text-green-300 text-sm">✓ Processed</span>
                ) : doc.status?.startsWith('error') ? (
                  <span className="text-red-300 text-sm">Error</span>
                ) : null}
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}