'use client';

import { motion, Variants } from 'framer-motion';
import Link from 'next/link';
import { Button } from '@/components/ui/button';

export default function HomePage() {
    const containerVariants: Variants = {
    hidden: { opacity: 0 },
    visible: {
      opacity: 1,
      transition: {
        staggerChildren: 0.3,
        delayChildren: 0.2,
      },
    },
  };

    const itemVariants: Variants = {
    hidden: { y: 20, opacity: 0 },
    visible: {
      y: 0,
      opacity: 1,
      transition: {
        duration: 0.6,
        ease: 'easeOut',
      },
    },
  };

  return (
    <div className="relative flex items-center justify-center min-h-screen w-full overflow-hidden bg-black">
      <div className="absolute inset-0 z-0">
        <div className="absolute inset-0 bg-gradient-to-br from-gray-900 via-black to-gray-800"></div>
      </div>
      <motion.div
        className="z-10 text-center px-4"
        variants={containerVariants}
        initial="hidden"
        animate="visible"
      >
        <motion.h1
          className="text-5xl md:text-7xl font-bold text-white mb-4 tracking-tight"
          variants={itemVariants}
        >
          Sicilius Platform
        </motion.h1>
        <motion.p
          className="text-lg md:text-2xl text-gray-300 max-w-2xl mx-auto mb-8"
          variants={itemVariants}
        >
          Veri yönetimi ve analizinde yeni bir dönem. Hızlı, güvenli ve akıllı çözümlerle işinizi geleceğe taşıyın.
        </motion.p>
        <motion.div variants={itemVariants}>
          <Link href="/login" passHref>
            <Button
              size="lg"
              className="bg-white text-black font-semibold hover:bg-gray-200 transition-colors duration-300 shadow-lg scale-100 hover:scale-105 active:scale-95"
            >
              Giriş Yap
            </Button>
          </Link>
        </motion.div>
      </motion.div>
    </div>
  );
}
