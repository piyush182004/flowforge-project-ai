import { Button } from "@/components/ui/button";
import { useAuth } from "@/contexts/AuthContext";
import { useNavigate } from "react-router-dom";
import { useEffect } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";

export function Login() {
  const { signIn, isLoading, isAuthenticated } = useAuth();
  const navigate = useNavigate();

  useEffect(() => {
    // Redirect if already authenticated
    if (isAuthenticated) {
      navigate("/");
    }
  }, [isAuthenticated, navigate]);

  return (
    <div className="min-h-screen flex items-center justify-center bg-background py-12 px-4 sm:px-6 lg:px-8">
      <div className="max-w-md w-full">
        <Card className="glass-effect glow-border animate-fade-in">
          <CardHeader className="text-center">
            <CardTitle className="text-2xl gradient-text mb-2">
              Welcome to FlowForge
            </CardTitle>
            <CardDescription className="text-muted-foreground">
              Sign in to access your dashboard and projects
            </CardDescription>
          </CardHeader>
          
          <CardContent className="space-y-6">
            <Button
              onClick={() => signIn()}
              disabled={isLoading}
              className="w-full bg-gradient-to-r from-blue-500 to-cyan-600 hover:from-blue-600 hover:to-cyan-700 animate-glow"
            >
              {isLoading ? "Signing in..." : "Sign in with Civic"}
            </Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}