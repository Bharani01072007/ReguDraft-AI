import { motion } from "framer-motion";

const CapsuleLoader = ({ text = "Generating Regulatory Draft..." }: { text?: string }) => {
  return (
    <div className="flex flex-col items-center justify-center gap-8 p-12">
      {/* Document outline background */}
      <div className="relative">
        <div className="absolute inset-0 flex items-center justify-center opacity-10">
          <div className="w-32 h-40 rounded-lg border-2 border-primary" />
        </div>

        {/* Rotating capsules */}
        <motion.div
          className="relative w-24 h-24"
          animate={{ rotate: 360 }}
          transition={{ duration: 3, repeat: Infinity, ease: "linear" }}
        >
          {[0, 120, 240].map((angle, i) => (
            <motion.div
              key={i}
              className="absolute w-6 h-14 rounded-full overflow-hidden"
              style={{
                top: "50%",
                left: "50%",
                transformOrigin: "center",
                transform: `translate(-50%, -50%) rotate(${angle}deg) translateY(-20px)`,
              }}
              animate={{ opacity: [0.4, 1, 0.4] }}
              transition={{ duration: 2, repeat: Infinity, delay: i * 0.3 }}
            >
              <div className="w-full h-1/2 bg-primary" />
              <div className="w-full h-1/2 bg-secondary" />
            </motion.div>
          ))}
        </motion.div>

        {/* Glow */}
        <motion.div
          className="absolute inset-0 rounded-full"
          style={{ background: "radial-gradient(circle, hsl(217 91% 60% / 0.2), transparent)" }}
          animate={{ scale: [1, 1.3, 1], opacity: [0.3, 0.6, 0.3] }}
          transition={{ duration: 2, repeat: Infinity }}
        />
      </div>

      <motion.p
        className="text-muted-foreground font-medium font-display text-sm tracking-wide"
        animate={{ opacity: [0.5, 1, 0.5] }}
        transition={{ duration: 2, repeat: Infinity }}
      >
        {text}
      </motion.p>
    </div>
  );
};

export default CapsuleLoader;
