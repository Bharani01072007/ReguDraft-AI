import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { FileText, Eye, PenTool, Download, Search, Filter } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import DashboardLayout from "@/components/DashboardLayout";
import { toast } from "sonner";
import { projectService, Project, DocumentResponse } from "@/services/projectService";
import { draftService } from "@/services/draftService";

const statusColors: Record<string, string> = {
  DRAFT: "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300",
  IN_REVIEW: "bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300",
  APPROVED: "bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-300",
  EXPORTED: "bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300",
};

interface HistoryItem extends DocumentResponse {
  projectName: string;
}

const HistoryPage = () => {
  const [search, setSearch] = useState("");
  const [items, setItems] = useState<HistoryItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [downloadingId, setDownloadingId] = useState<string | null>(null);

  const loadHistory = () => {
    projectService.list()
      .then((projects) => {
        const docItems: HistoryItem[] = [];
        projects.forEach((proj: any) => {
          const docs = proj.documents || [];
          docs.forEach((doc: any) => {
            docItems.push({
              ...doc,
              projectName: proj.name,
            });
          });
        });
        setItems(docItems);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        toast.error("Failed to load history logs");
        setLoading(false);
      });
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const handleDownload = async (item: HistoryItem) => {
    if (!item.current_version_id) {
      toast.error("No compiled version available to download.");
      return;
    }
    setDownloadingId(item.id);
    try {
      toast.info("Generating PDF export...");
      const res = await draftService.exportVersion(item.current_version_id, "pdf");
      toast.success("Download started!");
      window.open(res.file_url, "_blank");
    } catch (err: any) {
      console.error(err);
      toast.error(err?.message || "Failed to download PDF draft");
    } finally {
      setDownloadingId(null);
    }
  };

  const filtered = items.filter(
    (h) =>
      h.name.toLowerCase().includes(search.toLowerCase()) ||
      h.type.toLowerCase().includes(search.toLowerCase()) ||
      h.projectName.toLowerCase().includes(search.toLowerCase())
  );

  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </DashboardLayout>
    );
  }

  return (
    <DashboardLayout>
      <div className="max-w-5xl mx-auto">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <div className="flex items-center justify-between mb-6">
            <div>
              <h1 className="font-display text-2xl font-bold">History Logs</h1>
              <p className="text-sm text-muted-foreground">View and manage your previous drafts.</p>
            </div>
          </div>

          {/* Search */}
          <div className="flex gap-3 mb-6">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
              <Input
                value={search}
                onChange={(e) => setSearch(e.target.value)}
                placeholder="Search by draft name, type, or project..."
                className="pl-10"
              />
            </div>
            <Button variant="outline" size="icon"><Filter className="h-4 w-4" /></Button>
          </div>

          {/* Table */}
          <div className="bg-card rounded-xl border border-border shadow-elegant overflow-hidden">
            {filtered.length === 0 ? (
              <div className="p-12 text-center text-muted-foreground">
                <FileText className="h-12 w-12 mx-auto text-muted-foreground/30 mb-4" />
                <p className="text-sm">No historical documents matching your search.</p>
              </div>
            ) : (
              <div className="overflow-x-auto">
                <table className="w-full text-left">
                  <thead>
                    <tr className="border-b border-border bg-muted/50">
                      <th className="text-xs font-medium text-muted-foreground px-6 py-3">Draft Name</th>
                      <th className="text-xs font-medium text-muted-foreground px-6 py-3">Project</th>
                      <th className="text-xs font-medium text-muted-foreground px-6 py-3">Type</th>
                      <th className="text-xs font-medium text-muted-foreground px-6 py-3">Date</th>
                      <th className="text-xs font-medium text-muted-foreground px-6 py-3">Status</th>
                      <th className="text-xs font-medium text-muted-foreground px-6 py-3 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {filtered.map((item) => (
                      <tr key={item.id} className="border-b border-border last:border-0 hover:bg-muted/30 transition-colors">
                        <td className="px-6 py-4">
                          <div className="flex items-center gap-3">
                            <div className="w-8 h-8 rounded-lg gradient-accent flex items-center justify-center">
                              <FileText className="h-4 w-4 text-accent-foreground" />
                            </div>
                            <span className="font-semibold text-sm">{item.name}</span>
                          </div>
                        </td>
                        <td className="px-6 py-4 text-sm text-muted-foreground">{item.projectName}</td>
                        <td className="px-6 py-4 text-sm">{item.type}</td>
                        <td className="px-6 py-4 text-sm text-muted-foreground">
                          {new Date(item.created_at).toLocaleDateString()}
                        </td>
                        <td className="px-6 py-4">
                          <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${statusColors[item.status] || "bg-gray-100"}`}>
                            {item.status}
                          </span>
                        </td>
                        <td className="px-6 py-4">
                          <div className="flex items-center justify-end gap-1">
                            <Link to={`/editor/${item.id}`}>
                              <Button variant="ghost" size="icon" className="h-8 w-8"><Eye className="h-3.5 w-3.5" /></Button>
                            </Link>
                            <Link to={`/editor/${item.id}`}>
                              <Button variant="ghost" size="icon" className="h-8 w-8"><PenTool className="h-3.5 w-3.5" /></Button>
                            </Link>
                            <Button 
                              variant="ghost" 
                              size="icon" 
                              className="h-8 w-8" 
                              disabled={downloadingId === item.id || !item.current_version_id}
                              onClick={() => handleDownload(item)}
                            >
                              <Download className="h-3.5 w-3.5" />
                            </Button>
                          </div>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            )}
          </div>
        </motion.div>
      </div>
    </DashboardLayout>
  );
};

export default HistoryPage;
