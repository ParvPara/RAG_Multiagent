'use client';
import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { motion } from 'framer-motion';

export default function Login() {
  const [key, setKey] = useState('');
  const [error, setError] = useState('');
  const router = useRouter();

  // Check if already authenticated
  useEffect(() => {
    const isAuthenticated = localStorage.getItem('isAuthenticated');
    if (isAuthenticated === 'true') {
      router.push('/dashboard');
    }
  }, [router]);

  const handleSubmit = (e) => {
    e.preventDefault();
    // Access key
    const validKey = 'sopatech2024@compendai';
    
    if (key === validKey) {
      localStorage.setItem('isAuthenticated', 'true');
      router.push('/dashboard');
    } else {
      setError('Invalid key');
      setTimeout(() => setError(''), 3000);
    }
  };

  return (
    <motion.div 
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      className="min-h-screen flex items-center justify-center bg-gradient-to-b from-blue-900 to-black"
    >
      <div className="w-full max-w-md p-8 bg-blue-900/30 backdrop-blur-sm rounded-lg shadow-xl border border-blue-700/30">
        <motion.h1 
          initial={{ y: -20 }}
          animate={{ y: 0 }}
          className="text-4xl font-bold text-center mb-8 text-blue-100"
        >
          CompendAI
        </motion.h1>
        
        <form onSubmit={handleSubmit} className="space-y-6">
          <div>
            <label className="block text-blue-200 mb-2">Access Key</label>
            <input
              type="password"
              value={key}
              onChange={(e) => setKey(e.target.value)}
              className="w-full p-3 rounded bg-blue-800/50 border border-blue-700/50 
                text-blue-100 focus:outline-none focus:border-blue-500"
              placeholder="Enter your access key"
            />
          </div>
          
          {error && (
            <motion.p 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              className="text-red-400 text-center"
            >
              {error}
            </motion.p>
          )}
          
          <button
            type="submit"
            className="w-full py-3 px-6 rounded bg-blue-600 hover:bg-blue-500 
              text-white font-semibold transition-colors duration-200"
          >
            Login
          </button>
        </form>
      </div>
    </motion.div>
  );
} 