import { useEffect, useState } from "react";
import { Link } from "react-router-dom";
import { motion } from "framer-motion";
import { FilePlus, Clock, FileText, BookOpen, ArrowRight, TrendingUp, AlertCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import DashboardLayout from "@/components/DashboardLayout";
import logoFull from "@/assets/logo-full.jpeg";
import { projectService, Project, DocumentResponse } from "@/services/projectService";
import { toast } from "sonner";

const quickActions = [
  { title: "Generate New Draft", desc: "Create a CSR, CTD, or IND document", icon: FilePlus, path: "/generate", color: "gradient-primary" },
  { title: "View History", desc: "Access your previous drafts", icon: Clock, path: "/history", color: "gradient-accent" },
  { title: "Regulatory Knowledge", desc: "Browse ICH and FDA guidelines", icon: BookOpen, path: "/knowledge", color: "gradient-primary" },
];

const DashboardPage = () => {
  const [projects, setProjects] = useState<Project[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    projectService.list()
      .then((data) => {
        setProjects(data);
        setLoading(false);
      })
      .catch((err) => {
        console.error(err);
        toast.error("Failed to load dashboard data");
        setLoading(false);
      });
  }, []);

  // Compute stats dynamically
  const allDocuments: (DocumentResponse & { projectName: string })[] = [];
  projects.forEach((proj: any) => {
    const docs = proj.documents || [];
    docs.forEach((doc: any) => {
      allDocuments.push({
        ...doc,
        projectName: proj.name,
      });
    });
  });

  const draftsGenerated = allDocuments.length;
  const inProgress = allDocuments.filter(d => d.status === "DRAFT" || d.status === "IN_REVIEW").length;
  
  // Render loading state
  if (loading) {
    return (
      <DashboardLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </DashboardLayout>
    );
  }

  const stats = [
    { label: "Drafts Generated", value: draftsGenerated.toString(), icon: FileText },
    { label: "In Progress", value: inProgress.toString(), icon: Clock },
    { label: "Templates Available", value: "12", icon: BookOpen },
    { label: "System Status", value: "Online", icon: TrendingUp },
  ];

  return (
    <DashboardLayout>
      <div className="max-w-6xl mx-auto space-y-8">
        {/* Welcome */}
        <motion.div
          initial={{ opacity: 0, y: 12 }}
          animate={{ opacity: 1, y: 0 }}
          className="glass rounded-2xl p-8 flex flex-col md:flex-row items-center gap-6"
        >
          <img src={logoFull} alt="ReguDraft AI" className="w-32 h-auto rounded-xl shadow-md" />
          <div>
            <h1 className="font-display text-2xl font-bold mb-2">Welcome to ReguDraft AI</h1>
            <p className="text-muted-foreground">
              Your AI-powered regulatory drafting workspace. Generate, edit, and export regulatory documents with ease.
            </p>
          </div>
        </motion.div>

        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          {stats.map((s, i) => (
            <motion.div
              key={s.label}
              initial={{ opacity: 0, y: 12 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-card rounded-xl border border-border p-5 shadow-elegant"
            >
              <div className="flex items-center gap-3 mb-3">
                <div className="w-8 h-8 rounded-lg bg-secondary/10 flex items-center justify-center">
                  <s.icon className="h-4 w-4 text-secondary" />
                </div>
              </div>
              <p className="text-2xl font-bold font-display">{s.value}</p>
              <p className="text-xs text-muted-foreground mt-1">{s.label}</p>
            </motion.div>
          ))}
        </div>

        {/* Quick Actions */}
        <div>
          <h2 className="font-display font-semibold text-lg mb-4">Quick Actions</h2>
          <div className="grid md:grid-cols-3 gap-4">
            {quickActions.map((a, i) => (
              <motion.div
                key={a.title}
                initial={{ opacity: 0, y: 12 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.3 + i * 0.1 }}
              >
                <Link to={a.path} className="block group">
                  <div className="bg-card rounded-xl border border-border p-6 hover:shadow-elegant hover:border-secondary/30 transition-all duration-300">
                    <div className={`w-10 h-10 rounded-lg ${a.color} flex items-center justify-center mb-4`}>
                      <a.icon className="h-5 w-5 text-primary-foreground" />
                    </div>
                    <h3 className="font-display font-semibold mb-1">{a.title}</h3>
                    <p className="text-sm text-muted-foreground">{a.desc}</p>
                    <ArrowRight className="h-4 w-4 text-secondary mt-3 group-hover:translate-x-1 transition-transform" />
                  </div>
                </Link>
              </motion.div>
            ))}
          </div>
        </div>

        {/* Drafts List / Empty State */}
        <div>
          <h2 className="font-display font-semibold text-lg mb-4">Active Drafts</h2>
          {allDocuments.length === 0 ? (
            <div className="bg-card rounded-xl border border-border p-12 text-center shadow-elegant">
              <FileText className="h-12 w-12 text-muted-foreground/30 mx-auto mb-4" />
              <h3 className="font-display font-semibold text-lg mb-2">No drafts yet</h3>
              <p className="text-muted-foreground text-sm mb-6">
                Start generating your first regulatory document.
              </p>
              <Link to="/generate">
                <Button className="gradient-primary text-primary-foreground border-0 font-semibold">
                  <FilePlus className="h-4 w-4 mr-2" /> Generate Draft
                </Button>
              </Link>
            </div>
          ) : (
            <div className="bg-card rounded-xl border border-border shadow-elegant overflow-hidden">
              <div className="overflow-x-auto">
                <table className="w-full text-left border-collapse">
                  <thead>
                    <tr className="border-b border-border bg-muted/30">
                      <th className="text-xs font-semibold text-muted-foreground px-6 py-4">Draft Name</th>
                      <th className="text-xs font-semibold text-muted-foreground px-6 py-4">Project</th>
                      <th className="text-xs font-semibold text-muted-foreground px-6 py-4">Type</th>
                      <th className="text-xs font-semibold text-muted-foreground px-6 py-4">Status</th>
                      <th className="text-xs font-semibold text-muted-foreground px-6 py-4">Created At</th>
                      <th className="text-xs font-semibold text-muted-foreground px-6 py-4 text-right">Actions</th>
                    </tr>
                  </thead>
                  <tbody>
                    {allDocuments.map((doc) => (
                      <tr key={doc.id} className="border-b border-border last:border-0 hover:bg-muted/10 transition-colors">
                        <td className="px-6 py-4 text-sm font-semibold">
                          <Link to={`/editor/${doc.id}`} className="hover:text-primary transition-colors flex items-center gap-2">
                            <FileText className="h-4 w-4 text-primary" /> {doc.name}
                          </Link>
                        </td>
                        <td className="px-6 py-4 text-sm text-muted-foreground">{doc.projectName}</td>
                        <td className="px-6 py-4 text-sm">{doc.type}</td>
                        <td className="px-6 py-4">
                          <span className={`text-xs px-2.5 py-1 rounded-full font-medium ${
                            doc.status === "APPROVED" ? "bg-green-100 text-green-700 dark:bg-green-950 dark:text-green-300" :
                            doc.status === "IN_REVIEW" ? "bg-amber-100 text-amber-700 dark:bg-amber-950 dark:text-amber-300" :
                            doc.status === "EXPORTED" ? "bg-blue-100 text-blue-700 dark:bg-blue-950 dark:text-blue-300" :
                            "bg-gray-100 text-gray-700 dark:bg-gray-800 dark:text-gray-300"
                          }`}>
                            {doc.status}
                          </span>
                        </td>
                        <td className="px-6 py-4 text-sm text-muted-foreground">{new Date(doc.created_at).toLocaleDateString()}</td>
                        <td className="px-6 py-4 text-right">
                          <Link to={`/editor/${doc.id}`}>
                            <Button size="sm" variant="ghost" className="font-semibold text-xs text-primary hover:text-primary">
                              Edit <ArrowRight className="ml-1 h-3.5 w-3.5" />
                            </Button>
                          </Link>
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
      </div>
    </DashboardLayout>
  );
};

export default DashboardPage;
