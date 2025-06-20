
import React, { useState } from 'react';
import Layout from '@/components/Layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { 
  Code, 
  Plus, 
  Upload, 
  GitBranch, 
  Calendar, 
  File, 
  Search,
  Folder,
  Star,
  Download
} from 'lucide-react';

const Repositories = () => {
  const [searchTerm, setSearchTerm] = useState('');

  const repositories = [
    {
      name: 'ecommerce-platform',
      description: 'Full-stack e-commerce solution with React and Node.js',
      language: 'TypeScript',
      size: '45.2 MB',
      lastUpdate: '2 hours ago',
      branches: 8,
      commits: 342,
      isPrivate: true,
      starred: true
    },
    {
      name: 'mobile-app-redesign',
      description: 'React Native mobile application redesign project',
      language: 'JavaScript',
      size: '28.7 MB',
      lastUpdate: '1 day ago',
      branches: 3,
      commits: 156,
      isPrivate: true,
      starred: false
    },
    {
      name: 'api-gateway-service',
      description: 'Microservices API gateway with authentication',
      language: 'Python',
      size: '15.3 MB',
      lastUpdate: '3 days ago',
      branches: 5,
      commits: 89,
      isPrivate: false,
      starred: true
    },
    {
      name: 'data-analytics-dashboard',
      description: 'Real-time analytics dashboard with D3.js visualizations',
      language: 'JavaScript',
      size: '32.1 MB',
      lastUpdate: '1 week ago',
      branches: 4,
      commits: 203,
      isPrivate: true,
      starred: false
    }
  ];

  const filteredRepos = repositories.filter(repo =>
    repo.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
    repo.description.toLowerCase().includes(searchTerm.toLowerCase())
  );

  const getLanguageColor = (language: string) => {
    const colors: { [key: string]: string } = {
      'TypeScript': 'bg-blue-500',
      'JavaScript': 'bg-yellow-500',
      'Python': 'bg-green-500',
      'Java': 'bg-red-500',
      'Go': 'bg-cyan-500'
    };
    return colors[language] || 'bg-gray-500';
  };

  return (
    <Layout>
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold gradient-text mb-2">Private Repositories</h1>
            <p className="text-muted-foreground">Manage your secure project repositories and code assets.</p>
          </div>
          <div className="flex space-x-3 mt-4 lg:mt-0">
            <Button variant="outline" className="border-violet-500/50 hover-glow">
              <Upload className="w-4 h-4 mr-2" />
              Upload Repository
            </Button>
            <Button className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700">
              <Plus className="w-4 h-4 mr-2" />
              New Repository
            </Button>
          </div>
        </div>

        {/* Search and Filters */}
        <div className="flex flex-col sm:flex-row gap-4 mb-8">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <Input
              placeholder="Search repositories..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="pl-10 bg-white/5 border-white/20 focus:border-violet-500"
            />
          </div>
          <div className="flex space-x-2">
            <Button variant="outline" size="sm" className="border-white/20">
              <Star className="w-4 h-4 mr-2" />
              Starred
            </Button>
            <Button variant="outline" size="sm" className="border-white/20">
              <Folder className="w-4 h-4 mr-2" />
              Private
            </Button>
          </div>
        </div>

        {/* Repository Stats */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8">
          <Card className="glass-effect">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Total Repositories</p>
                  <p className="text-2xl font-bold text-white">{repositories.length}</p>
                </div>
                <Code className="w-8 h-8 text-violet-400" />
              </div>
            </CardContent>
          </Card>

          <Card className="glass-effect">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Total Size</p>
                  <p className="text-2xl font-bold text-white">121.3 MB</p>
                </div>
                <File className="w-8 h-8 text-blue-400" />
              </div>
            </CardContent>
          </Card>

          <Card className="glass-effect">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Total Commits</p>
                  <p className="text-2xl font-bold text-white">790</p>
                </div>
                <GitBranch className="w-8 h-8 text-emerald-400" />
              </div>
            </CardContent>
          </Card>

          <Card className="glass-effect">
            <CardContent className="p-6">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm text-muted-foreground mb-1">Last Activity</p>
                  <p className="text-2xl font-bold text-white">2h</p>
                </div>
                <Calendar className="w-8 h-8 text-orange-400" />
              </div>
            </CardContent>
          </Card>
        </div>

        {/* Repository List */}
        <div className="space-y-4">
          {filteredRepos.map((repo, index) => (
            <Card key={index} className="glass-effect hover-glow animate-fade-in" style={{ animationDelay: `${index * 0.1}s` }}>
              <CardContent className="p-6">
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <div className="flex items-center space-x-3 mb-2">
                      <h3 className="text-lg font-semibold text-white hover:text-violet-400 transition-colors cursor-pointer">
                        {repo.name}
                      </h3>
                      {repo.starred && <Star className="w-4 h-4 text-yellow-400 fill-current" />}
                      <Badge variant={repo.isPrivate ? 'secondary' : 'outline'} className="text-xs">
                        {repo.isPrivate ? 'Private' : 'Public'}
                      </Badge>
                    </div>
                    
                    <p className="text-muted-foreground text-sm mb-3">{repo.description}</p>
                    
                    <div className="flex items-center space-x-6 text-sm text-muted-foreground">
                      <div className="flex items-center space-x-1">
                        <div className={`w-3 h-3 rounded-full ${getLanguageColor(repo.language)}`}></div>
                        <span>{repo.language}</span>
                      </div>
                      
                      <div className="flex items-center space-x-1">
                        <GitBranch className="w-4 h-4" />
                        <span>{repo.branches} branches</span>
                      </div>
                      
                      <div className="flex items-center space-x-1">
                        <File className="w-4 h-4" />
                        <span>{repo.commits} commits</span>
                      </div>
                      
                      <div className="flex items-center space-x-1">
                        <Download className="w-4 h-4" />
                        <span>{repo.size}</span>
                      </div>
                      
                      <div className="flex items-center space-x-1">
                        <Calendar className="w-4 h-4" />
                        <span>Updated {repo.lastUpdate}</span>
                      </div>
                    </div>
                  </div>
                  
                  <div className="flex space-x-2 ml-4">
                    <Button variant="outline" size="sm" className="border-white/20 hover-glow">
                      <Code className="w-4 h-4 mr-2" />
                      Clone
                    </Button>
                    <Button variant="outline" size="sm" className="border-violet-500/50 hover-glow">
                      <GitBranch className="w-4 h-4 mr-2" />
                      Generate Workflow
                    </Button>
                  </div>
                </div>
              </CardContent>
            </Card>
          ))}
        </div>

        {filteredRepos.length === 0 && (
          <Card className="glass-effect">
            <CardContent className="p-12 text-center">
              <Code className="w-12 h-12 text-muted-foreground mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">No repositories found</h3>
              <p className="text-muted-foreground mb-4">
                {searchTerm ? 'Try adjusting your search terms.' : 'Upload your first repository to get started.'}
              </p>
              <Button className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700">
                <Plus className="w-4 h-4 mr-2" />
                Add Repository
              </Button>
            </CardContent>
          </Card>
        )}
      </div>
    </Layout>
  );
};

export default Repositories;
