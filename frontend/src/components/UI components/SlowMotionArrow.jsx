import React from 'react';
import { motion } from 'framer-motion';
import { ArrowBigDown, ChevronDown, ArrowDown } from 'lucide-react';

const SlowMotionArrow = () => {
  return (
    <div className="flex justify-center items-center h-40">
      <motion.div
        animate={{ y: [0, 15, 0] }} 
        transition={{
          duration: 3, 
          repeat: Infinity,
          ease: "easeInOut", 
        }}
      >
        <ArrowDown className="w-96 h-72 text-white" />
      </motion.div>
    </div>
  );
};

export default SlowMotionArrow;