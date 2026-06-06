import { useState, useCallback } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Upload, FileText, AlertTriangle, FlaskConical, Pill, Users, X } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Textarea } from "@/components/ui/textarea";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import DashboardLayout from "@/components/DashboardLayout";
import CapsuleLoader from "@/components/CapsuleLoader";
import { toast } from "sonner";
import { projectService } from "@/services/projectService";
import { draftService } from "@/services/draftService";

const GeneratePage = () => {
  const navigate = useNavigate();
  const [isGenerating, setIsGenerating] = useState(false);
  const [uploadedFiles, setUploadedFiles] = useState<File[]>([]);
  const [dragOver, setDragOver] = useState(false);

  const [form, setForm] = useState({
    drugName: "",
    drugType: "",
    targetDisease: "",
    trialPhase: "",
    studyDesign: "",
    participants: "",
    primaryOutcomes: "",
    secondaryOutcomes: "",
    adverseEvents: "",
    toxicitySummary: "",
    documentType: "" as string,
  });

  const update = (key: string, value: string) => setForm((f) => ({ ...f, [key]: value }));

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragOver(false);
    const files = Array.from(e.dataTransfer.files).filter((f) =>
      ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document", "text/plain"].includes(f.type)
    );
    setUploadedFiles((prev) => [...prev, ...files]);
  }, []);

  const removeFile = (idx: number) => setUploadedFiles((f) => f.filter((_, i) => i !== idx));

  const handleSubmit = async () => {
    if (!form.drugName || !form.documentType) {
      toast.error("Please fill in required fields (Drug Name, Document Type)");
      return;
    }
    setIsGenerating(true);
    try {
      // 1. Create a Project
      const project = await projectService.create({
        name: `${form.drugName} Study Project`,
        description: `Regulatory clinical trial project for ${form.drugName} (${form.targetDisease || 'Unspecified disease'})`,
      });

      // 2. Create a Document
      const doc = await projectService.createDocument(project.id, {
        name: `${form.documentType} - ${form.drugName}`,
        type: form.documentType,
      });

      // 3. Upload context files
      if (uploadedFiles.length > 0) {
        for (const file of uploadedFiles) {
          await draftService.uploadFile(project.id, doc.id, file);
        }
      }

      // 4. Trigger AI draft generation with form data
      await draftService.generate(doc.id, {
        drugName: form.drugName,
        drugType: form.drugType,
        targetDisease: form.targetDisease,
        trialPhase: form.trialPhase,
        studyDesign: form.studyDesign,
        participants: form.participants,
        primaryOutcomes: form.primaryOutcomes,
        secondaryOutcomes: form.secondaryOutcomes,
        adverseEvents: form.adverseEvents,
        toxicitySummary: form.toxicitySummary
      });

      toast.success("Draft generated successfully!");
      navigate(`/editor/${doc.id}`);
    } catch (err: any) {
      console.error(err);
      toast.error(err?.message || "Failed to generate regulatory draft");
    } finally {
      setIsGenerating(false);
    }
  };

  if (isGenerating) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <CapsuleLoader />
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-display text-2xl font-bold mb-2">Generate Regulatory Draft</h1>
          <p className="text-muted-foreground text-sm mb-8">
            Fill in your clinical trial data to generate a regulatory document.
          </p>

          <div className="space-y-8">
            {/* Document Type */}
            <div className="bg-card rounded-xl border border-border p-6 shadow-elegant">
              <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
                <FileText className="h-4 w-4 text-secondary" /> Document Type
              </h2>
              <Select value={form.documentType} onValueChange={(v) => update("documentType", v)}>
                <SelectTrigger><SelectValue placeholder="Select document type" /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="CSR">CSR — Clinical Study Report</SelectItem>
                  <SelectItem value="CTD">CTD — Common Technical Document</SelectItem>
                  <SelectItem value="IND">IND — Investigational New Drug Application</SelectItem>
                </SelectContent>
              </Select>
            </div>

            {/* Drug Information */}
            <div className="bg-card rounded-xl border border-border p-6 shadow-elegant">
              <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
                <Pill className="h-4 w-4 text-secondary" /> Drug Information
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div><Label>Drug Name *</Label><Input value={form.drugName} onChange={(e) => update("drugName", e.target.value)} placeholder="e.g. Acetaminophen" /></div>
                <div><Label>Drug Type</Label><Input value={form.drugType} onChange={(e) => update("drugType", e.target.value)} placeholder="e.g. Small Molecule" /></div>
                <div className="md:col-span-2"><Label>Target Disease</Label><Input value={form.targetDisease} onChange={(e) => update("targetDisease", e.target.value)} placeholder="e.g. Type 2 Diabetes" /></div>
              </div>
            </div>

            {/* Clinical Trial Details */}
            <div className="bg-card rounded-xl border border-border p-6 shadow-elegant">
              <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
                <FlaskConical className="h-4 w-4 text-secondary" /> Clinical Trial Details
              </h2>
              <div className="grid md:grid-cols-2 gap-4">
                <div>
                  <Label>Trial Phase</Label>
                  <Select value={form.trialPhase} onValueChange={(v) => update("trialPhase", v)}>
                    <SelectTrigger><SelectValue placeholder="Select phase" /></SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Phase 1">Phase 1</SelectItem>
                      <SelectItem value="Phase 2">Phase 2</SelectItem>
                      <SelectItem value="Phase 3">Phase 3</SelectItem>
                      <SelectItem value="Phase 4">Phase 4</SelectItem>
                    </SelectContent>
                  </Select>
                </div>
                <div><Label>Study Design</Label><Input value={form.studyDesign} onChange={(e) => update("studyDesign", e.target.value)} placeholder="e.g. Randomized, double-blind" /></div>
                <div className="md:col-span-2"><Label>Number of Participants</Label><Input value={form.participants} onChange={(e) => update("participants", e.target.value)} placeholder="e.g. 500" /></div>
              </div>
            </div>

            {/* Results */}
            <div className="bg-card rounded-xl border border-border p-6 shadow-elegant">
              <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
                <Users className="h-4 w-4 text-secondary" /> Results
              </h2>
              <div className="space-y-4">
                <div><Label>Primary Outcomes</Label><Textarea value={form.primaryOutcomes} onChange={(e) => update("primaryOutcomes", e.target.value)} placeholder="Describe primary outcomes..." rows={3} /></div>
                <div><Label>Secondary Outcomes</Label><Textarea value={form.secondaryOutcomes} onChange={(e) => update("secondaryOutcomes", e.target.value)} placeholder="Describe secondary outcomes..." rows={3} /></div>
              </div>
            </div>

            {/* Safety Data */}
            <div className="bg-card rounded-xl border border-border p-6 shadow-elegant">
              <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
                <AlertTriangle className="h-4 w-4 text-secondary" /> Safety Data
              </h2>
              <div className="space-y-4">
                <div><Label>Adverse Events</Label><Textarea value={form.adverseEvents} onChange={(e) => update("adverseEvents", e.target.value)} placeholder="List adverse events..." rows={3} /></div>
                <div><Label>Toxicity Summary</Label><Textarea value={form.toxicitySummary} onChange={(e) => update("toxicitySummary", e.target.value)} placeholder="Summarize toxicity data..." rows={3} /></div>
              </div>
            </div>

            {/* File Upload */}
            <div className="bg-card rounded-xl border border-border p-6 shadow-elegant">
              <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
                <Upload className="h-4 w-4 text-secondary" /> Upload Clinical Data
              </h2>
              <div
                onDrop={handleDrop}
                onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
                onDragLeave={() => setDragOver(false)}
                className={`border-2 border-dashed rounded-xl p-8 text-center transition-colors ${dragOver ? "border-secondary bg-secondary/5" : "border-border"}`}
              >
                <Upload className="h-8 w-8 text-muted-foreground mx-auto mb-3" />
                <p className="text-sm text-muted-foreground mb-1">Drag & drop files here, or click to browse</p>
                <p className="text-xs text-muted-foreground">Supports PDF, DOCX, TXT</p>
                <input
                  type="file"
                  multiple
                  accept=".pdf,.docx,.txt"
                  className="hidden"
                  id="file-upload"
                  onChange={(e) => setUploadedFiles((prev) => [...prev, ...Array.from(e.target.files || [])])}
                />
                <Button variant="outline" size="sm" className="mt-3" onClick={() => document.getElementById("file-upload")?.click()}>
                  Browse Files
                </Button>
              </div>
              {uploadedFiles.length > 0 && (
                <div className="mt-4 space-y-2">
                  {uploadedFiles.map((f, i) => (
                    <div key={i} className="flex items-center justify-between bg-muted rounded-lg px-4 py-2 text-sm">
                      <span className="truncate">{f.name}</span>
                      <button onClick={() => removeFile(i)} className="text-muted-foreground hover:text-destructive">
                        <X className="h-4 w-4" />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            {/* Submit */}
            <Button size="lg" className="w-full gradient-primary text-primary-foreground border-0 font-semibold" onClick={handleSubmit}>
              Generate Draft
            </Button>
          </div>
        </motion.div>
      </div>
    </DashboardLayout>
  );
};

export default GeneratePage;
