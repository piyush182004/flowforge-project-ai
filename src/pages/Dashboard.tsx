import React from 'react';
import Layout from '@/components/Layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { 
  BarChart3, 
  Calendar, 
  Code, 
  Settings, 
  Plus,
  ArrowUp,
  GitBranch,
  Users,
  Clock,
  CheckCircle
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const projects = [
    {
      name: 'E-commerce Platform',
      status: 'Active',
      progress: 78,
      team: 5,
      lastUpdate: '2 hours ago',
      color: 'from-violet-500 to-purple-600'
    },
    {
      name: 'Mobile App Redesign',
      status: 'In Review',
      progress: 92,
      team: 3,
      lastUpdate: '1 day ago',
      color: 'from-blue-500 to-cyan-600'
    },
    {
      name: 'API Integration',
      status: 'Planning',
      progress: 34,
      team: 4,
      lastUpdate: '3 days ago',
      color: 'from-emerald-500 to-teal-600'
    }
  ];

  const quickStats = [
    {
      title: 'Active Projects',
      value: '12',
      change: '+3',
      icon: Code,
      color: 'text-violet-400'
    },
    {
      title: 'Tasks Completed',
      value: '84',
      change: '+12',
      icon: CheckCircle,
      color: 'text-emerald-400'
    },
    {
      title: 'Team Members',
      value: '23',
      change: '+2',
      icon: Users,
      color: 'text-blue-400'
    },
    {
      title: 'Avg. Velocity',
      value: '8.4',
      change: '+0.8',
      icon: BarChart3,
      color: 'text-orange-400'
    }
  ];

  const recentActivity = [
    {
      action: 'Task completed',
      item: 'User authentication module',
      user: 'Sarah Chen',
      time: '5 minutes ago',
      type: 'success'
    },
    {
      action: 'Workflow generated',
      item: 'Payment processing flow',
      user: 'AI Assistant',
      time: '1 hour ago',
      type: 'info'
    },
    {
      action: 'Code review requested',
      item: 'Database optimization',
      user: 'Mike Johnson',
      time: '2 hours ago',
      type: 'warning'
    },
    {
      action: 'Sprint planning',
      item: 'Sprint 12 kickoff',
      user: 'Team Alpha',
      time: '1 day ago',
      type: 'info'
    }
  ];

  return (
    <Layout>
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold gradient-text mb-2">Dashboard</h1>
            <p className="text-muted-foreground">
              {user?.name || user?.email ? (
                <>
                  Welcome back, <span className="font-semibold text-violet-400">{user.name || user.email}</span>! Here's what's happening with your projects.
                </>
              ) : (
                <>Welcome back! Here's what's happening with your projects.</>
              )}
            </p>
          </div>
          <Button className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700 mt-4 lg:mt-0">
            <Plus className="w-4 h-4 mr-2" />
            New Project
          </Button>
        </div>

        {/* Quick Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          {quickStats.map((stat, index) => {
            const Icon = stat.icon;
            return (
              <Card key={index} className="glass-effect hover-glow animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
                <CardContent className="p-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <p className="text-sm text-muted-foreground mb-1">{stat.title}</p>
                      <p className="text-2xl font-bold text-white">{stat.value}</p>
                      <p className="text-sm text-emerald-400 flex items-center mt-1">
                        <ArrowUp className="w-3 h-3 mr-1" />
                        {stat.change}
                      </p>
                    </div>
                    <Icon className={`w-8 h-8 ${stat.color}`} />
                  </div>
                </CardContent>
              </Card>
            );
          })}
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Active Projects */}
          <div className="lg:col-span-2">
            <Card className="glass-effect">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Code className="w-5 h-5 mr-2" />
                  Active Projects
                </CardTitle>
                <CardDescription>Your current project portfolio</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {projects.map((project, index) => (
                  <div key={index} className="glass-effect p-4 rounded-lg hover-glow">
                    <div className="flex items-center justify-between mb-3">
                      <h3 className="font-semibold text-white">{project.name}</h3>
                      <Badge variant={project.status === 'Active' ? 'default' : 'secondary'}>
                        {project.status}
                      </Badge>
                    </div>
                    
                    <div className="w-full bg-white/10 rounded-full h-2 mb-3">
                      <div 
                        className={`h-2 rounded-full bg-gradient-to-r ${project.color}`}
                        style={{ width: `${project.progress}%` }}
                      ></div>
                    </div>
                    
                    <div className="flex items-center justify-between text-sm text-muted-foreground">
                      <div className="flex items-center space-x-4">
                        <span className="flex items-center">
                          <Users className="w-4 h-4 mr-1" />
                          {project.team} members
                        </span>
                        <span>{project.progress}% complete</span>
                      </div>
                      <span className="flex items-center">
                        <Clock className="w-4 h-4 mr-1" />
                        {project.lastUpdate}
                      </span>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity */}
          <div>
            <Card className="glass-effect">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Calendar className="w-5 h-5 mr-2" />
                  Recent Activity
                </CardTitle>
                <CardDescription>Latest updates across all projects</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-start space-x-3 pb-3 border-b border-white/10 last:border-0">
                    <div className={`w-2 h-2 rounded-full mt-2 ${
                      activity.type === 'success' ? 'bg-emerald-400' :
                      activity.type === 'warning' ? 'bg-orange-400' : 'bg-blue-400'
                    }`}></div>
                    <div className="flex-1 min-w-0">
                      <p className="text-sm text-white">
                        <span className="font-medium">{activity.action}</span>
                      </p>
                      <p className="text-sm text-violet-400 truncate">{activity.item}</p>
                      <div className="flex items-center justify-between mt-1">
                        <p className="text-xs text-muted-foreground">{activity.user}</p>
                        <p className="text-xs text-muted-foreground">{activity.time}</p>
                      </div>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>
    </Layout>
  );
};

export default Dashboard;
