import { motion } from "framer-motion";
import { User, Bell, Shield, Palette, Key, Globe } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Switch } from "@/components/ui/switch";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import DashboardLayout from "@/components/DashboardLayout";
import { toast } from "sonner";
import { useState } from "react";

const SettingsPage = () => {
  const [profile, setProfile] = useState({ name: "", email: "", organization: "" });
  const [prefs, setPrefs] = useState({
    emailNotifications: true,
    draftReady: true,
    weeklyDigest: false,
    theme: "system",
    language: "en",
  });
  const [apiKey, setApiKey] = useState("");

  const save = () => toast.success("Settings saved");

  return (
    <DashboardLayout>
      <div className="max-w-4xl mx-auto space-y-6">
        <motion.div initial={{ opacity: 0, y: 12 }} animate={{ opacity: 1, y: 0 }}>
          <h1 className="font-display text-2xl font-bold mb-2">Settings</h1>
          <p className="text-muted-foreground text-sm mb-8">
            Manage your profile, preferences, and integrations.
          </p>
        </motion.div>

        {/* Profile */}
        <section className="bg-card rounded-xl border border-border p-6 shadow-elegant">
          <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
            <User className="h-4 w-4 text-secondary" /> Profile
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <Label>Full Name</Label>
              <Input value={profile.name} onChange={(e) => setProfile({ ...profile, name: e.target.value })} placeholder="Jane Doe" />
            </div>
            <div>
              <Label>Email</Label>
              <Input type="email" value={profile.email} onChange={(e) => setProfile({ ...profile, email: e.target.value })} placeholder="jane@company.com" />
            </div>
            <div className="md:col-span-2">
              <Label>Organization</Label>
              <Input value={profile.organization} onChange={(e) => setProfile({ ...profile, organization: e.target.value })} placeholder="Acme Pharma" />
            </div>
          </div>
        </section>

        {/* Notifications */}
        <section className="bg-card rounded-xl border border-border p-6 shadow-elegant">
          <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
            <Bell className="h-4 w-4 text-secondary" /> Notifications
          </h2>
          <div className="space-y-4">
            {[
              { key: "emailNotifications", label: "Email notifications", desc: "Receive product updates by email" },
              { key: "draftReady", label: "Draft ready alerts", desc: "Get notified when a draft finishes generating" },
              { key: "weeklyDigest", label: "Weekly digest", desc: "Summary of your drafting activity" },
            ].map((item) => (
              <div key={item.key} className="flex items-center justify-between gap-4 py-2 border-b border-border last:border-0">
                <div>
                  <p className="text-sm font-medium">{item.label}</p>
                  <p className="text-xs text-muted-foreground">{item.desc}</p>
                </div>
                <Switch
                  checked={prefs[item.key as keyof typeof prefs] as boolean}
                  onCheckedChange={(v) => setPrefs({ ...prefs, [item.key]: v })}
                />
              </div>
            ))}
          </div>
        </section>

        {/* Appearance */}
        <section className="bg-card rounded-xl border border-border p-6 shadow-elegant">
          <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
            <Palette className="h-4 w-4 text-secondary" /> Appearance
          </h2>
          <div className="grid md:grid-cols-2 gap-4">
            <div>
              <Label>Theme</Label>
              <Select value={prefs.theme} onValueChange={(v) => setPrefs({ ...prefs, theme: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="light">Light</SelectItem>
                  <SelectItem value="dark">Dark</SelectItem>
                  <SelectItem value="system">System</SelectItem>
                </SelectContent>
              </Select>
            </div>
            <div>
              <Label>Language</Label>
              <Select value={prefs.language} onValueChange={(v) => setPrefs({ ...prefs, language: v })}>
                <SelectTrigger><SelectValue /></SelectTrigger>
                <SelectContent>
                  <SelectItem value="en">English</SelectItem>
                  <SelectItem value="es">Spanish</SelectItem>
                  <SelectItem value="fr">French</SelectItem>
                  <SelectItem value="de">German</SelectItem>
                </SelectContent>
              </Select>
            </div>
          </div>
        </section>

        {/* API & Integrations */}
        <section className="bg-card rounded-xl border border-border p-6 shadow-elegant">
          <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
            <Key className="h-4 w-4 text-secondary" /> API & Integrations
          </h2>
          <div className="space-y-4">
            <div>
              <Label>n8n Webhook URL</Label>
              <Input value={apiKey} onChange={(e) => setApiKey(e.target.value)} placeholder="https://n8n.example.com/webhook/..." />
              <p className="text-xs text-muted-foreground mt-1">
                Connect your Regulatory Knowledge Agent for AI-powered drafting.
              </p>
            </div>
            <div className="flex items-center gap-2 text-sm text-muted-foreground">
              <Globe className="h-4 w-4" /> Connected services: <span className="text-foreground font-medium">Supabase</span>
            </div>
          </div>
        </section>

        {/* Security */}
        <section className="bg-card rounded-xl border border-border p-6 shadow-elegant">
          <h2 className="font-display font-semibold flex items-center gap-2 mb-4">
            <Shield className="h-4 w-4 text-secondary" /> Security
          </h2>
          <div className="space-y-3">
            <Button variant="outline" size="sm">Change password</Button>
            <Button variant="outline" size="sm" className="ml-2">Enable two-factor auth</Button>
          </div>
        </section>

        <div className="flex justify-end">
          <Button onClick={save} className="gradient-primary text-primary-foreground border-0">
            Save Changes
          </Button>
        </div>
      </div>
    </DashboardLayout>
  );
};

export default SettingsPage;
