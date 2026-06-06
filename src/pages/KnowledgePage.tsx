import { useState, useEffect } from "react";
import { motion } from "framer-motion";
import { BookOpen, Search, Filter, ShieldAlert, Cpu } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import DashboardLayout from "@/components/DashboardLayout";
import { toast } from "sonner";
import { regulatoryService, KnowledgeSearchResult } from "@/services/regulatoryService";

const KnowledgePage = () => {
  const [search, setSearch] = useState("");
  const [results, setResults] = useState<KnowledgeSearchResult[]>([]);
  const [loading, setLoading] = useState(false);

  const handleSearch = (queryText: string) => {
    setLoading(true);
    regulatoryService.search(queryText || "regulatory", undefined, 10)
      .then((res) => {
        setResults(res.results || []);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        toast.error("Failed to query regulatory knowledge database");
        setLoading(false);
      });
  };

  // Run initial search on load
  useEffect(() => {
    handleSearch("");
  }, []);

  const triggerSearch = (e: React.FormEvent) => {
    e.preventDefault();
    handleSearch(search);
  };

  return (
    <DashboardLayout>
      <div className="max-w-5xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="font-display text-2xl font-bold">Regulatory Knowledge Base</h1>
              <p className="text-sm text-muted-foreground">Search and browse ICH, FDA guidelines, and compliance rules.</p>
            </div>
          </div>

          {/* Search Bar */}
          <form onSubmit={triggerSearch} className="flex gap-3 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Query FDA, ICH guidelines semantically (e.g. 'CSR structure', 'adverse event reporting')..."
                className="pl-10 text-sm"
              />
            </div>
            <Button type="submit" className="gradient-primary text-primary-foreground border-0 font-semibold px-6">
              Search
            </Button>
          </form>

          {/* Guidelines Results */}
          <div className="space-y-4">
            {loading ? (
              <div className="flex justify-center py-12">
                <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
              </div>
            ) : results.length === 0 ? (
              <div className="bg-card rounded-xl border border-border p-12 text-center shadow-elegant text-muted-foreground">
                <BookOpen className="h-12 w-12 mx-auto text-muted-foreground/30 mb-4" />
                <p className="text-sm">No guidelines found matching your search. Try adjusting the keywords.</p>
              </div>
            ) : (
              <div className="grid gap-4">
                {results.map((item, idx) => (
                  <motion.div
                    key={idx}
                    initial={{ opacity: 0, y: 10 }}
                    animate={{ opacity: 1, y: 0 }}
                    transition={{ delay: idx * 0.05 }}
                    className="p-6 rounded-xl bg-card border border-border shadow-sm space-y-3"
                  >
                    <div className="flex items-start justify-between gap-4">
                      <div>
                        <div className="flex items-center gap-2 mb-1.5">
                          <span className="text-xs font-semibold px-2 py-0.5 rounded bg-primary/10 text-primary uppercase">
                            {item.metadata?.guideline_type || "ICH Guideline"}
                          </span>
                          <span className="text-xs text-muted-foreground font-mono">
                            Section: {item.metadata?.section_code || "N/A"}
                          </span>
                          {item.metadata?.document_type && (
                            <span className="text-xs text-muted-foreground font-mono">
                              Doc Type: {item.metadata?.document_type}
                            </span>
                          )}
                        </div>
                        <h3 className="font-display font-semibold text-base leading-snug">
                          {item.metadata?.title || `Guideline Standard ${item.metadata?.section_code || ""}`}
                        </h3>
                      </div>
                      
                      {/* Score Indicator */}
                      <div className="text-right">
                        <span className="text-xs font-semibold text-secondary flex items-center gap-1">
                          <Cpu className="h-3 w-3" /> Semantic Score: {Math.round(item.score * 100)}%
                        </span>
                      </div>
                    </div>
                    
                    <div className="text-sm text-muted-foreground leading-relaxed whitespace-pre-line border-l-2 border-muted pl-4 py-1 italic font-sans">
                      "{item.text}"
                    </div>
                  </motion.div>
                ))}
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </DashboardLayout>
  );
};

export default KnowledgePage;
