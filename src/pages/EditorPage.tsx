import { useEffect, useState, useRef } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Save, Download, Wand2, Minimize2, Maximize2, List, ChevronRight, CheckCircle, RefreshCw, AlertTriangle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import DashboardLayout from "@/components/DashboardLayout";
import { toast } from "sonner";
import { draftService, DocumentDetailResponse } from "@/services/draftService";

const sections = [
  "1. Title Page",
  "2. Synopsis",
  "3. Introduction",
  "4. Study Design",
  "5. Results",
  "6. Safety Analysis",
  "7. Conclusions",
];

const EditorPage = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const textareaRef = useRef<HTMLTextAreaElement>(null);
  
  const [documentDetail, setDocumentDetail] = useState<DocumentDetailResponse | null>(null);
  const [content, setContent] = useState("");
  const [loading, setLoading] = useState(true);
  const [refining, setRefining] = useState(false);
  const [saving, setSaving] = useState(false);
  const [exporting, setExporting] = useState(false);
  const [showSections, setShowSections] = useState(true);

  // Load document details
  const loadDocument = () => {
    if (!id || id === "demo") {
      setLoading(false);
      return;
    }
    setLoading(true);
    draftService.getById(id)
      .then((data) => {
        setDocumentDetail(data);
        if (data.current_version) {
          setContent(data.current_version.content_markdown);
        }
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        toast.error("Failed to load document draft");
        setLoading(false);
      });
  };

  useEffect(() => {
    loadDocument();
  }, [id]);

  const handleSave = async () => {
    if (!id || id === "demo") {
      toast.success("Demo draft saved successfully (mock)");
      return;
    }
    setSaving(true);
    try {
      await draftService.submitReview(id, {
        action: "EDIT",
        edited_content: content,
        comments: ["Manual editor changes"],
      });
      toast.success("Draft saved successfully");
      loadDocument(); // Refresh to update score
    } catch (err: any) {
      console.error(err);
      toast.error(err?.message || "Failed to save draft changes");
    } finally {
      setSaving(false);
    }
  };

  const handleApprove = async () => {
    if (!id || id === "demo") {
      toast.success("Demo draft approved and exported (mock)");
      return;
    }
    try {
      toast.info("Approving and compiling final exports...");
      const result = await draftService.submitReview(id, {
        action: "APPROVE",
        comments: ["Approved by regulatory writer"],
      });
      toast.success("Document approved and compiled!");
      loadDocument();
    } catch (err: any) {
      console.error(err);
      toast.error(err?.message || "Failed to approve draft");
    }
  };

  const handleExport = async (format: string) => {
    if (!id || id === "demo") {
      toast.success(`Exporting as ${format.toUpperCase()} (mock)`);
      return;
    }
    if (!documentDetail?.current_version) {
      toast.error("No version available to export");
      return;
    }
    setExporting(true);
    try {
      toast.info(`Generating ${format.toUpperCase()} export...`);
      const res = await draftService.exportVersion(documentDetail.current_version.id, format);
      toast.success(`${format.toUpperCase()} generated! Downloading...`);
      
      // Open in a new window or trigger download
      window.open(res.file_url, "_blank");
    } catch (err: any) {
      console.error(err);
      toast.error(err?.message || `Failed to export document as ${format.toUpperCase()}`);
    } finally {
      setExporting(false);
    }
  };

  const handleAiTool = async (action: "IMPROVE" | "SUMMARIZE" | "EXPAND") => {
    setRefining(true);
    
    // Check selection in textarea
    let textToRefine = content;
    let selectionStart = 0;
    let selectionEnd = content.length;
    let hasSelection = false;

    if (textareaRef.current) {
      const start = textareaRef.current.selectionStart;
      const end = textareaRef.current.selectionEnd;
      if (start !== end) {
        textToRefine = content.substring(start, end);
        selectionStart = start;
        selectionEnd = end;
        hasSelection = true;
      }
    }

    try {
      toast.info(`Running AI inline action: ${action}...`);
      const res = await draftService.refine({ content: textToRefine, action });
      
      let updatedContent = "";
      if (hasSelection) {
        updatedContent = 
          content.substring(0, selectionStart) + 
          res.refined_content + 
          content.substring(selectionEnd);
      } else {
        updatedContent = res.refined_content;
      }
      
      setContent(updatedContent);
      toast.success("AI refinement complete!");
    } catch (err: any) {
      console.error(err);
      toast.error(err?.message || "AI refinement failed");
    } finally {
      setRefining(false);
    }
  };

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </DashboardLayout>
    );
  }

  const complianceReport = documentDetail?.compliance_report;
  const score = complianceReport?.compliance_score ?? 100;
  const issues = complianceReport?.issues ?? [];
  const suggestions = complianceReport?.suggestions ?? [];

  return (
    <DashboardLayout>
      <div className="max-w-7xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          {/* Toolbar */}
          <div className="flex flex-wrap items-center justify-between gap-4 mb-6">
            <div>
              <h1 className="font-display text-xl font-bold">{documentDetail?.name || "Demo Document"}</h1>
              <p className="text-sm text-muted-foreground">
                {documentDetail?.type || "CSR"} — Version {documentDetail?.current_version?.version_number || 1} ({documentDetail?.status || "DRAFT"})
              </p>
            </div>
            <div className="flex items-center gap-2">
              <Button disabled={refining} variant="outline" size="sm" onClick={() => handleAiTool("IMPROVE")}>
                <Wand2 className="h-3.5 w-3.5 mr-1.5" /> Improve Writing
              </Button>
              <Button disabled={refining} variant="outline" size="sm" onClick={() => handleAiTool("SUMMARIZE")}>
                <Minimize2 className="h-3.5 w-3.5 mr-1.5" /> Summarize
              </Button>
              <Button disabled={refining} variant="outline" size="sm" onClick={() => handleAiTool("EXPAND")}>
                <Maximize2 className="h-3.5 w-3.5 mr-1.5" /> Expand
              </Button>
              
              <div className="w-px h-6 bg-border mx-1" />
              
              <Button disabled={saving} variant="outline" size="sm" onClick={handleSave}>
                <Save className="h-3.5 w-3.5 mr-1.5" /> {saving ? "Saving..." : "Save"}
              </Button>
              
              {documentDetail?.status === "IN_REVIEW" && (
                <Button size="sm" className="bg-green-600 hover:bg-green-700 text-white border-0 font-semibold" onClick={handleApprove}>
                  <CheckCircle className="h-3.5 w-3.5 mr-1.5" /> Approve Draft
                </Button>
              )}
            </div>
          </div>

          <div className="flex gap-6">
            {/* Section Navigation */}
            {showSections && (
              <div className="hidden lg:block w-56 shrink-0">
                <div className="bg-card rounded-xl border border-border p-4 sticky top-24">
                  <h3 className="font-display font-semibold text-sm mb-3 flex items-center gap-2">
                    <List className="h-4 w-4" /> Sections
                  </h3>
                  <nav className="space-y-1">
                    {sections.map((s) => (
                      <button
                        key={s}
                        className="w-full text-left text-xs px-3 py-2 rounded-lg text-muted-foreground hover:bg-muted hover:text-foreground transition-colors flex items-center gap-1"
                      >
                        <ChevronRight className="h-3 w-3" /> {s}
                      </button>
                    ))}
                  </nav>
                </div>
              </div>
            )}

            {/* Editor */}
            <div className="flex-1 min-w-0">
              <div className="bg-card rounded-xl border border-border shadow-elegant">
                <div className="border-b border-border px-6 py-3 flex items-center justify-between">
                  <span className="text-xs text-muted-foreground">Markdown Editor</span>
                  <div className="flex gap-2">
                    {["PDF", "DOCX", "TXT", "MD"].map((fmt) => (
                      <button
                        key={fmt}
                        disabled={exporting}
                        onClick={() => handleExport(fmt.toLowerCase())}
                        className="text-xs px-2 py-1 rounded bg-muted text-muted-foreground hover:text-foreground transition-colors disabled:opacity-50"
                      >
                        {fmt}
                      </button>
                    ))}
                  </div>
                </div>
                <Textarea
                  ref={textareaRef}
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  className="min-h-[70vh] border-0 rounded-none rounded-b-xl font-mono text-sm leading-relaxed resize-none focus-visible:ring-0 p-6"
                />
              </div>
            </div>

            {/* Right panel - AI Suggestions */}
            <div className="hidden xl:block w-72 shrink-0">
              <div className="bg-card rounded-xl border border-border p-4 sticky top-24 space-y-4 max-h-[80vh] overflow-y-auto">
                <div className="flex items-center justify-between">
                  <h3 className="font-display font-semibold text-sm">AI Compliance Report</h3>
                  <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${
                    score >= 90 ? "bg-green-100 text-green-700" :
                    score >= 75 ? "bg-amber-100 text-amber-700" :
                    "bg-red-100 text-red-700"
                  }`}>
                    {score}% Score
                  </span>
                </div>
                
                {issues.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-xs font-semibold text-destructive flex items-center gap-1">
                      <AlertTriangle className="h-3 w-3" /> Found Issues ({issues.length})
                    </p>
                    {issues.map((issue: any, index: number) => (
                      <div key={index} className="p-2.5 rounded bg-red-50 dark:bg-red-950/20 border border-red-100 dark:border-red-900/30 text-[11px] text-muted-foreground">
                        <p className="font-semibold text-destructive mb-0.5">Section: {issue.section}</p>
                        <p>{issue.message}</p>
                      </div>
                    ))}
                  </div>
                )}

                {suggestions.length > 0 && (
                  <div className="space-y-2">
                    <p className="text-xs font-semibold text-amber-600 dark:text-amber-500 flex items-center gap-1">
                      <Wand2 className="h-3 w-3" /> Suggestions ({suggestions.length})
                    </p>
                    {suggestions.map((sug: any, index: number) => (
                      <div key={index} className="p-2.5 rounded bg-amber-50/50 dark:bg-amber-950/10 border border-amber-100/50 dark:border-amber-900/10 text-[11px] text-muted-foreground">
                        <p className="font-semibold text-amber-600 dark:text-amber-500 mb-0.5">Section: {sug.section}</p>
                        <p>{sug.message}</p>
                      </div>
                    ))}
                  </div>
                )}

                {issues.length === 0 && suggestions.length === 0 && (
                  <div className="p-3 rounded-lg bg-green-50 dark:bg-green-950/10 border border-green-100 dark:border-green-950/20 text-xs text-muted-foreground">
                    <p className="font-medium text-green-700 dark:text-green-500 mb-1">✓ Fully Compliant</p>
                    No structural or regulatory compliance issues were identified in this version.
                  </div>
                )}
              </div>
            </div>
          </div>
        </motion.div>
      </div>
    </DashboardLayout>
  );
};

export default EditorPage;
