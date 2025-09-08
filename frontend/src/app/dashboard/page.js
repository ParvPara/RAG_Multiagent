'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';
import FileUpload from '@/components/FileUpload';
import ChatInterface from '@/components/ChatInterface';
import DocumentList from '../../components/DocumentList';
import LoadingScreen from '@/components/LoadingScreen';
import { api } from '@/services/api';

export default function Dashboard() {
  const [documents, setDocuments] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const router = useRouter();
  
  useEffect(() => {
    const isAuthenticated = localStorage.getItem('isAuthenticated');
    if (!isAuthenticated) {
      router.push('/login');
      return;
    }

    const checkBackend = async () => {
      try {
        await api.getDocuments();
        setTimeout(() => setIsLoading(false), 500);
      } catch (error) {
        console.log('Backend not ready, retrying...');
        setTimeout(checkBackend, 1000);
      }
    };

    checkBackend();
  }, [router]);

  const handleLogout = () => {
    localStorage.removeItem('isAuthenticated');
    router.push('/login');
  };

  return (
    <>
      <LoadingScreen isLoading={isLoading} />
      
      <motion.main
        initial={{ opacity: 0 }}
        animate={{ 
          opacity: isLoading ? 0 : 1,
          transition: { duration: 0.5, delay: 0.2 }
        }}
        className="min-h-screen flex flex-col"
      >
        <div className="relative">
          <motion.h1
            initial={{ y: -20 }}
            animate={{ 
              y: 0,
              transition: { duration: 0.5, delay: 0.3 }
            }}
            className="text-5xl font-bold text-center pt-8 text-blue-100 
              tracking-wide hover:scale-105 transition-transform duration-300
              cursor-default drop-shadow-[0_0_15px_rgba(59,130,246,0.5)]"
          >
            CompendAI
          </motion.h1>
          
          <button
            onClick={handleLogout}
            className="absolute top-4 right-4 px-4 py-2 rounded bg-blue-600/50 
              hover:bg-blue-500/50 text-blue-100 text-sm transition-colors duration-200"
          >
            Logout
          </button>
        </div>
        
        <motion.div
          initial={{ y: 20 }}
          animate={{ 
            y: 0,
            transition: { duration: 0.5, delay: 0.4 }
          }}
          className="flex-grow flex items-center"
        >
          <div className="w-full max-w-6xl mx-auto p-8">
            <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
              <div className="space-y-6">
                <FileUpload onUploadSuccess={() => {}} />
                <DocumentList documents={documents} setDocuments={setDocuments} />
              </div>
              
              <div>
                <ChatInterface />
              </div>
            </div>
          </div>
        </motion.div>
      </motion.main>
    </>
  );
} 