'use client';
import { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { api } from '@/services/api';

export default function ChatInterface() {
  const [question, setQuestion] = useState('');
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!question.trim()) return;

    try {
      setLoading(true);
      setError(null);
      setAnswer('Thinking...');  // Show thinking state immediately
      const data = await api.sendQuestion(question);
      setAnswer(data.answer);
    } catch (error) {
      setError(error.message);
      setAnswer('');  // Clear the thinking state on error
    } finally {
      setLoading(false);
    }
  };

  const ThinkingDots = () => (
    <div className="flex space-x-1 ml-2">
      {[0, 1, 2].map((i) => (
        <motion.span
          key={i}
          initial={{ opacity: 0.2 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0.2 }}
          transition={{
            duration: 0.5,
            repeat: Infinity,
            repeatType: "reverse",
            delay: i * 0.2
          }}
          className="text-blue-300"
        >
          •
        </motion.span>
      ))}
    </div>
  );

  return (
    <div className="p-6 bg-blue-900/30 backdrop-blur-sm rounded-lg shadow-xl border border-blue-700/30">
      <motion.h2
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-xl font-semibold mb-4 text-blue-100"
      >
        Ask a Question
      </motion.h2>
      
      <form onSubmit={handleSubmit} className="space-y-4">
        <motion.textarea
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          value={question}
          onChange={(e) => setQuestion(e.target.value)}
          placeholder="Ask a question about your documents..."
          className="w-full p-3 bg-blue-950/50 border border-blue-700/50 rounded-lg resize-none h-32
            text-blue-100 placeholder-blue-300/50 focus:outline-none focus:border-blue-500
            transition-colors"
          disabled={loading}
        />
        
        <motion.button
          type="submit"
          disabled={loading}
          whileHover={{ scale: loading ? 1 : 1.02 }}
          whileTap={{ scale: loading ? 1 : 0.98 }}
          className="w-full py-2 px-4 bg-blue-600 text-blue-50 rounded-lg
            hover:bg-blue-500 disabled:bg-blue-800/50 disabled:text-blue-200/50
            transition-colors duration-200"
        >
          {loading ? 'Getting Answer...' : 'Ask Question'}
        </motion.button>

        <AnimatePresence>
          {error && (
            <motion.div
              initial={{ opacity: 0, y: -10 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -10 }}
              className="text-red-300 mt-2"
            >
              Error: {error}
            </motion.div>
          )}
        </AnimatePresence>
      </form>

      <AnimatePresence>
        {answer && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: 20 }}
            transition={{ type: "spring", damping: 15 }}
            className="mt-6"
          >
            <h3 className="font-semibold mb-2 text-blue-200">Answer:</h3>
            <div className="text-blue-100 bg-blue-800/30 p-4 rounded-lg">
              {loading ? (
                <div className="flex items-center">
                  <motion.span
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ duration: 0.3 }}
                  >
                    {answer}
                  </motion.span>
                  <ThinkingDots />
                </div>
              ) : (
                <motion.p
                  initial={{ opacity: 0 }}
                  animate={{ opacity: 1 }}
                  transition={{ duration: 0.5 }}
                  className="whitespace-pre-wrap"
                >
                  {answer}
                </motion.p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
} 