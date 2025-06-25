"use client";

import Image from 'next/image';
import { motion } from 'framer-motion';

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
          <Image
            src="/sicilius-logo.svg"
            alt="Sicilius Yükleniyor..."
            width={128}
            height={128}
            priority
          />
        </motion.div>
      </div>
    </div>
  );
};

export default Loader;
