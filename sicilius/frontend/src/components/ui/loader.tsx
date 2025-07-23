"use client";

import Image from 'next/image';
import { motion } from 'framer-motion';
import { Logo } from '@/components/ui/logo';

const Loader = () => {
  return (
    <div className="flex flex-col items-center justify-center h-full w-full fixed inset-0 bg-background/80 backdrop-blur-sm z-50">
      <div className="flex flex-col items-center justify-center">
        <motion.div
          initial={{ scale: 0.95, opacity: 0.8 }}
          animate={{ scale: 1, opacity: 1 }}
          transition={{
            duration: 0.8,
            repeat: Infinity,
            repeatType: "reverse",
            ease: "easeInOut",
          }}
        >
          <Logo className="h-32 w-32" />
        </motion.div>
      </div>
    </div>
  );
};

export default Loader;
