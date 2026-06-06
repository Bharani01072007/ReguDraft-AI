import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { FileText, Brain, Shield, Download, ArrowRight, Upload, Cpu, Layers, PenTool, CheckCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import Navbar from "@/components/Navbar";
import logoFull from "@/assets/logo-full.jpeg";

const features = [
  { icon: Brain, title: "AI Regulatory Drafting", desc: "Generate CSR, CTD, and IND documents using advanced AI agents." },
  { icon: FileText, title: "Clinical Data Extraction", desc: "Automatically extract and structure data from clinical trial results." },
  { icon: Layers, title: "Automated Structuring", desc: "Documents are structured to meet ICH and FDA regulatory standards." },
  { icon: Shield, title: "Compliance Built-In", desc: "Every draft follows regulatory guidelines out of the box." },
  { icon: PenTool, title: "Rich Draft Editor", desc: "Edit, annotate, and refine documents in a Notion-style editor." },
  { icon: Download, title: "Multi-Format Export", desc: "Export to PDF, DOCX, TXT, and Markdown instantly." },
];

const workflowSteps = [
  { icon: Upload, label: "Upload Clinical Data", color: "bg-primary" },
  { icon: Cpu, label: "AI Processing", color: "bg-secondary" },
  { icon: Layers, label: "Regulatory Structuring", color: "bg-accent" },
  { icon: FileText, label: "Draft Generation", color: "bg-secondary" },
  { icon: PenTool, label: "Edit & Export", color: "bg-primary" },
];

const fadeUp = {
  hidden: { opacity: 0, y: 24 },
  visible: (i: number) => ({ opacity: 1, y: 0, transition: { delay: i * 0.1, duration: 0.5 } }),
};

const LandingPage = () => {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* Hero */}
      <section className="gradient-hero relative overflow-hidden">
        <div className="absolute inset-0 opacity-30 pointer-events-none" style={{
          backgroundImage: "radial-gradient(circle at 20% 50%, hsl(217 91% 60% / 0.08) 0%, transparent 50%), radial-gradient(circle at 80% 20%, hsl(199 89% 48% / 0.06) 0%, transparent 50%)"
        }} />
        <div className="container mx-auto px-4 py-24 lg:py-32">
          <div className="flex flex-col lg:flex-row items-center gap-12 lg:gap-20">
            <motion.div
              className="flex-1 text-center lg:text-left"
              initial={{ opacity: 0, x: -30 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.6 }}
            >
              <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full bg-secondary/10 text-secondary text-sm font-medium mb-6">
                <Cpu className="h-3.5 w-3.5" />
                AI-Powered Platform
              </div>
              <h1 className="font-display text-4xl md:text-5xl lg:text-6xl font-extrabold leading-tight mb-6">
                <span className="text-foreground">ReguDraft</span>{" "}
                <span className="text-gradient-accent">AI</span>
              </h1>
              <p className="text-xl md:text-2xl text-muted-foreground font-medium mb-4">
                AI-Powered Regulatory Drug Documentation
              </p>
              <p className="text-muted-foreground max-w-lg mb-8">
                Automatically generate CSR, CTD, and IND documents from clinical trial data.
                Built for pharma companies, CROs, and biotech startups.
              </p>
              <div className="flex flex-wrap gap-4 justify-center lg:justify-start">
                <Link to="/generate">
                  <Button size="lg" className="gradient-primary text-primary-foreground border-0 shadow-elegant font-semibold px-8">
                    Generate Draft <ArrowRight className="ml-2 h-4 w-4" />
                  </Button>
                </Link>
                <Link to="/dashboard">
                  <Button size="lg" variant="outline" className="font-semibold px-8">
                    View Demo
                  </Button>
                </Link>
              </div>
            </motion.div>

            <motion.div
              className="flex-1 flex justify-center"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.6, delay: 0.2 }}
            >
              <div className="relative">
                <div className="absolute -inset-4 rounded-3xl bg-secondary/5 blur-2xl" />
                <img
                  src={logoFull}
                  alt="ReguDraft AI - AI-Powered Regulatory Drug Documentation"
                  className="relative w-full max-w-md rounded-2xl shadow-elegant"
                />
              </div>
            </motion.div>
          </div>
        </div>
      </section>

      {/* Features */}
      <section className="py-24 bg-card">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
              Platform Capabilities
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              Everything you need to generate, edit, and export regulatory documents.
            </p>
          </motion.div>

          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f, i) => (
              <motion.div
                key={f.title}
                custom={i}
                variants={fadeUp}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                className="group p-6 rounded-xl bg-background border border-border hover:shadow-elegant hover:border-secondary/30 transition-all duration-300"
              >
                <div className="w-10 h-10 rounded-lg gradient-accent flex items-center justify-center mb-4">
                  <f.icon className="h-5 w-5 text-accent-foreground" />
                </div>
                <h3 className="font-display font-semibold text-lg mb-2">{f.title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{f.desc}</p>
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* Workflow */}
      <section className="py-24 bg-background">
        <div className="container mx-auto px-4">
          <motion.div
            className="text-center mb-16"
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
          >
            <h2 className="font-display text-3xl md:text-4xl font-bold mb-4">
              How It Works
            </h2>
            <p className="text-muted-foreground max-w-2xl mx-auto">
              From raw clinical data to polished regulatory documents in minutes.
            </p>
          </motion.div>

          <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-2">
            {workflowSteps.map((step, i) => (
              <motion.div
                key={step.label}
                custom={i}
                variants={fadeUp}
                initial="hidden"
                whileInView="visible"
                viewport={{ once: true }}
                className="flex items-center gap-2"
              >
                <div className="flex flex-col items-center gap-3 px-6 py-5 rounded-xl glass shadow-elegant min-w-[160px]">
                  <div className={`w-10 h-10 rounded-lg ${step.color} flex items-center justify-center`}>
                    <step.icon className="h-5 w-5 text-primary-foreground" />
                  </div>
                  <span className="text-sm font-medium text-center">{step.label}</span>
                </div>
                {i < workflowSteps.length - 1 && (
                  <ArrowRight className="h-5 w-5 text-muted-foreground hidden md:block shrink-0" />
                )}
              </motion.div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20">
        <div className="container mx-auto px-4">
          <div className="gradient-primary rounded-2xl p-12 text-center shadow-elegant">
            <h2 className="font-display text-3xl font-bold text-primary-foreground mb-4">
              Ready to streamline your regulatory workflow?
            </h2>
            <p className="text-primary-foreground/80 mb-8 max-w-lg mx-auto">
              Start generating regulatory documents in minutes, not weeks.
            </p>
            <Link to="/generate">
              <Button size="lg" variant="secondary" className="font-semibold px-8">
                Get Started <ArrowRight className="ml-2 h-4 w-4" />
              </Button>
            </Link>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-border py-8">
        <div className="container mx-auto px-4 text-center text-sm text-muted-foreground">
          © 2026 ReguDraft AI. AI-Powered Regulatory Drug Documentation.
        </div>
      </footer>
    </div>
  );
};

export default LandingPage;
