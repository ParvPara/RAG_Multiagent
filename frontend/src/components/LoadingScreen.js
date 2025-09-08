'use client';
import { motion, AnimatePresence } from 'framer-motion';

export default function LoadingScreen({ isLoading }) {
  return (
    <AnimatePresence>
      {isLoading && (
        <motion.div
          initial={{ opacity: 1 }}
          exit={{ 
            opacity: 0,
            transition: { duration: 0.5 }
          }}
          className="fixed inset-0 bg-blue-900/90 backdrop-blur-sm flex items-center justify-center z-50"
        >
          <motion.div 
            initial={{ scale: 0.8, opacity: 0 }}
            animate={{ 
              scale: 1, 
              opacity: 1,
              transition: { duration: 0.5 }
            }}
            exit={{ 
              scale: 1.2, 
              opacity: 0,
              transition: { duration: 0.5 }
            }}
            className="text-center"
          >
            <motion.h2 
              animate={{ 
                scale: [1, 1.02, 1],
                transition: { 
                  repeat: Infinity,
                  duration: 2
                }
              }}
              className="text-3xl font-bold text-blue-100 mb-4"
            >
              CompendAI
            </motion.h2>
            <p className="text-blue-200">Initializing system and loading documents...</p>
            <p className="text-blue-300 text-sm mt-2">This may take a few moments</p>
          </motion.div>
        </motion.div>
      )}
    </AnimatePresence>
  );
} 