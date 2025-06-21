import React from 'react';
import { Link } from 'react-router-dom';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { 
  ArrowUp, 
  Code, 
  Calendar, 
  Settings, 
  User,
  ChevronRight,
  CheckCircle,
  GitBranch,
  BarChart3,
  Zap
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

const Index = () => {
  const { isAuthenticated } = useAuth();
  const features = [
    {
      icon: GitBranch,
      title: "AI-Powered Workflow Generator",
      description: "Automatically generate connected, visual workflows from your project structure with intelligent task mapping.",
      color: "from-violet-500 to-purple-600"
    },
    {
      icon: Code,
      title: "Private Repository Integration",
      description: "Securely upload and manage your project folders with enterprise-grade security and version control.",
      color: "from-blue-500 to-cyan-600"
    },
    {
      icon: Calendar,
      title: "Scrum & Agile Management",
      description: "Complete sprint boards, task assignment, stand-up logs, and calendar views for agile teams.",
      color: "from-emerald-500 to-teal-600"
    },
    {
      icon: BarChart3,
      title: "Advanced Analytics",
      description: "Real-time insights into team performance, project velocity, and workflow efficiency metrics.",
      color: "from-orange-500 to-red-600"
    },
    {
      icon: Zap,
      title: "Smart Automation",
      description: "Intelligent task prioritization, automated code reviews, and workflow optimization suggestions.",
      color: "from-pink-500 to-rose-600"
    },
    {
      icon: Settings,
      title: "Enterprise Integration",
      description: "Seamless integration with popular tools like Jira, GitHub, Slack, and CI/CD pipelines.",
      color: "from-indigo-500 to-purple-600"
    }
  ];

  return (
    <div className="min-h-screen bg-background">
      {/* Navigation */}
      <nav className="glass-effect border-b border-white/10 sticky top-0 z-50">
        <div className="container mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-gradient-to-r from-violet-500 to-purple-600 rounded-lg flex items-center justify-center animate-glow">
                <span className="text-white font-bold text-sm">FF</span>
              </div>
              <span className="text-2xl font-bold gradient-text">FlowForge</span>
            </div>
            
            <div className="flex items-center space-x-4">
              {!isAuthenticated && (
                <>
                  <Link to="/auth">
                    <Button variant="outline" className="border-violet-500/50 hover-glow">
                      <User className="w-4 h-4 mr-2" />
                      Sign In
                    </Button>
                  </Link>
                  <Link to="/dashboard">
                    <Button className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 animate-glow">
                      Get Started
                      <ChevronRight className="w-4 h-4 ml-2" />
                    </Button>
                  </Link>
                </>
              )}
            </div>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="relative overflow-hidden">
        <div className="absolute inset-0 futuristic-grid opacity-30"></div>
        <div className="absolute inset-0 bg-gradient-to-br from-violet-900/20 via-transparent to-purple-900/20"></div>
        
        <div className="relative container mx-auto px-6 py-20 lg:py-32">
          <div className="text-center max-w-4xl mx-auto">
            <div className="animate-fade-in">
              <h1 className="text-5xl md:text-7xl font-bold mb-6 leading-tight">
                <span className="gradient-text">AI-Powered</span><br />
                <span className="text-white">Project Management</span><br />
                <span className="text-violet-400">Reimagined</span>
              </h1>
              
              <p className="text-xl md:text-2xl text-muted-foreground mb-8 max-w-3xl mx-auto leading-relaxed">
                Transform your development workflow with intelligent automation, 
                visual project mapping, and enterprise-grade collaboration tools.
              </p>

              <div className="flex flex-col sm:flex-row gap-4 justify-center mb-12">
                {!isAuthenticated && (
                  <>
                    <Link to="/dashboard">
                      <Button size="lg" className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 text-lg px-8 py-6 animate-glow">
                        Start Free Trial
                        <ArrowUp className="w-5 h-5 ml-2 rotate-45" />
                      </Button>
                    </Link>
                  </>
                )}
                <Link to="/workflows">
                  <Button size="lg" variant="outline" className="border-violet-500/50 hover-glow text-lg px-8 py-6">
                    Get Started
                    <ChevronRight className="w-5 h-5 ml-2" />
                  </Button>
                </Link>
              </div>

              <div className="flex items-center justify-center space-x-8 text-sm text-muted-foreground">
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Free 14-day trial</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>No credit card required</span>
                </div>
                <div className="flex items-center space-x-2">
                  <CheckCircle className="w-4 h-4 text-green-500" />
                  <span>Enterprise security</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section className="py-20 lg:py-32 relative">
        <div className="container mx-auto px-6">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
              Everything You Need
            </h2>
            <p className="text-xl text-muted-foreground max-w-3xl mx-auto">
              FlowForge combines the power of AI with proven project management methodologies 
              to deliver unparalleled productivity for development teams.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
            {features.map((feature, index) => {
              const Icon = feature.icon;
              return (
                <Card 
                  key={index} 
                  className="glass-effect hover-glow group transition-all duration-300 hover:scale-105 animate-fade-in"
                  style={{ animationDelay: `${index * 0.1}s` }}
                >
                  <CardHeader>
                    <div className={`w-12 h-12 rounded-lg bg-gradient-to-r ${feature.color} flex items-center justify-center mb-4 group-hover:animate-float`}>
                      <Icon className="w-6 h-6 text-white" />
                    </div>
                    <CardTitle className="text-xl text-white group-hover:text-violet-400 transition-colors">
                      {feature.title}
                    </CardTitle>
                  </CardHeader>
                  <CardContent>
                    <CardDescription className="text-muted-foreground text-base leading-relaxed">
                      {feature.description}
                    </CardDescription>
                  </CardContent>
                </Card>
              );
            })}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 relative">
        <div className="absolute inset-0 bg-gradient-to-r from-violet-900/20 to-purple-900/20"></div>
        <div className="relative container mx-auto px-6 text-center">
          <h2 className="text-4xl md:text-5xl font-bold mb-6 gradient-text">
            Ready to Transform Your Workflow?
          </h2>
          <p className="text-xl text-muted-foreground mb-8 max-w-2xl mx-auto">
            Join thousands of development teams who have revolutionized their 
            project management with FlowForge's intelligent automation.
          </p>
          {!isAuthenticated && (
            <Link to="/auth">
              <Button size="lg" className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 text-lg px-8 py-6 animate-glow">
                Start Your Free Trial
                <ChevronRight className="w-5 h-5 ml-2" />
              </Button>
            </Link>
          )}
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12">
        <div className="container mx-auto px-6">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 mb-4 md:mb-0">
              <div className="w-6 h-6 bg-gradient-to-r from-violet-500 to-purple-600 rounded flex items-center justify-center">
                <span className="text-white font-bold text-xs">FF</span>
              </div>
              <span className="text-lg font-bold gradient-text">FlowForge</span>
            </div>
            <p className="text-muted-foreground text-sm">
              © 2024 FlowForge. Revolutionizing project management with AI.
            </p>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Index;
