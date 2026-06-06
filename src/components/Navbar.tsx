import { Link, useLocation } from "react-router-dom";
import logoIcon from "@/assets/logo-icon.jpeg";
import { Button } from "@/components/ui/button";

const Navbar = () => {
  const location = useLocation();
  const isLanding = location.pathname === "/";

  return (
    <nav className="sticky top-0 z-50 glass border-b border-border/50">
      <div className="container mx-auto flex h-16 items-center justify-between px-4">
        <Link to="/" className="flex items-center gap-3">
          <img src={logoIcon} alt="ReguDraft AI" className="h-9 w-9 rounded-lg object-contain" />
          <span className="font-display font-bold text-lg">
            <span className="text-foreground">ReguDraft</span>{" "}
            <span className="text-gradient-accent">AI</span>
          </span>
        </Link>

        {isLanding ? (
          <div className="flex items-center gap-3">
            <Link to="/dashboard">
              <Button variant="ghost" size="sm">Dashboard</Button>
            </Link>
            <Link to="/generate">
              <Button size="sm" className="gradient-primary text-primary-foreground border-0">
                Generate Draft
              </Button>
            </Link>
          </div>
        ) : (
          <div className="flex items-center gap-3">
            <Link to="/">
              <Button variant="ghost" size="sm">Home</Button>
            </Link>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
