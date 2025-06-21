import React, { useState, useRef, useEffect } from 'react';
import Layout from '@/components/Layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Progress } from '@/components/ui/progress';
import WorkflowGraph from '@/components/WorkflowGraph';
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
  CheckCircle,
  Upload,
  FileText,
  Brain,
  Zap,
  AlertCircle,
  Sparkles,
  Eye,
  Download
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

const Dashboard = () => {
  const { user } = useAuth();
  const fileInputRef = useRef<HTMLInputElement>(null);
  
  // Upload and analysis states
  const [uploading, setUploading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [uploadProgress, setUploadProgress] = useState(0);
  const [analysisProgress, setAnalysisProgress] = useState(0);
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [projectId, setProjectId] = useState<string | null>(null);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [graphData, setGraphData] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);
  const [currentStep, setCurrentStep] = useState<'idle' | 'uploading' | 'analyzing' | 'complete'>('idle');
  
  // Workflow graph states
  const [showWorkflowGraph, setShowWorkflowGraph] = useState(false);
  const [workflowGraphData, setWorkflowGraphData] = useState<any>(null);
  const [loadingGraph, setLoadingGraph] = useState(false);

  // Recent analyses state
  const [recentAnalyses, setRecentAnalyses] = useState<any[]>([]);

  // Load recent analyses from localStorage on mount
  useEffect(() => {
    const savedAnalyses = localStorage.getItem('recentAnalyses');
    if (savedAnalyses) {
      try {
        const parsed = JSON.parse(savedAnalyses);
        setRecentAnalyses(parsed);
      } catch (error) {
        console.error('Error loading recent analyses:', error);
      }
    }
  }, []);

  // Save recent analyses to localStorage when they change
  useEffect(() => {
    localStorage.setItem('recentAnalyses', JSON.stringify(recentAnalyses));
  }, [recentAnalyses]);

  // View analysis details
  const handleViewAnalysis = (analysis: any) => {
    setAnalysisResult(analysis.analysis);
    setGraphData(analysis.graph);
    setProjectId(analysis.id);
    setCurrentStep('complete');
  };

  const quickStats = [
    {
      title: 'Projects Analyzed',
      value: recentAnalyses.length.toString(),
      change: '+1',
      icon: Code,
      color: 'text-violet-400'
    },
    {
      title: 'Features Detected',
      value: recentAnalyses.reduce((sum, analysis) => sum + analysis.features.existing, 0).toString(),
      change: '+5',
      icon: CheckCircle,
      color: 'text-emerald-400'
    },
    {
      title: 'Improvements Suggested',
      value: recentAnalyses.reduce((sum, analysis) => sum + analysis.features.missing, 0).toString(),
      change: '+3',
      icon: Users,
      color: 'text-blue-400'
    },
    {
      title: 'Workflows Generated',
      value: recentAnalyses.reduce((sum, analysis) => sum + analysis.features.workflows, 0).toString(),
      change: '+2',
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

  // Handle file selection
  const handleFileSelect = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file) {
      if (file.type === 'application/zip' || file.name.endsWith('.zip')) {
        setUploadedFile(file);
        setError(null);
      } else {
        setError('Please select a ZIP file containing your codebase');
        setUploadedFile(null);
      }
    }
  };

  // Handle file upload
  const handleUpload = async () => {
    if (!uploadedFile) return;

    setCurrentStep('uploading');
    setUploading(true);
    setUploadProgress(0);
    setError(null);

    try {
      const formData = new FormData();
      formData.append('project', uploadedFile);

      console.log(`📤 Starting upload for file: ${uploadedFile.name}`);

      // Simulate upload progress
      const progressInterval = setInterval(() => {
        setUploadProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 10;
        });
      }, 200);

      const response = await fetch('http://localhost:5000/api/upload', {
        method: 'POST',
        body: formData,
      });

      clearInterval(progressInterval);
      setUploadProgress(100);

      console.log(`📊 Upload response status: ${response.status}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ Upload failed with status ${response.status}:`, errorText);
        throw new Error(`Upload failed with status ${response.status}: ${errorText}`);
      }

      const result = await response.json();
      console.log('✅ Upload completed successfully:', result);
      
      if (!result.project_id) {
        console.error('❌ Invalid upload response:', result);
        throw new Error('Invalid upload response from server');
      }

      setProjectId(result.project_id);
      
      // Start AI analysis
      await handleAnalysis(result.project_id);

    } catch (err) {
      console.error('❌ Upload error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Upload failed. Please try again.';
      setError(errorMessage);
      setCurrentStep('idle');
    } finally {
      setUploading(false);
    }
  };

  // Handle AI analysis with retry mechanism
  const handleAnalysis = async (projectId: string, retryCount = 0) => {
    const maxRetries = 2;
    
    setCurrentStep('analyzing');
    setAnalyzing(true);
    setAnalysisProgress(0);
    setError(null);

    try {
      // Simulate analysis progress
      const progressInterval = setInterval(() => {
        setAnalysisProgress(prev => {
          if (prev >= 90) {
            clearInterval(progressInterval);
            return 90;
          }
          return prev + 5;
        });
      }, 300);

      console.log(`🔍 Starting analysis for project: ${projectId} (attempt ${retryCount + 1})`);

      // Generate AI-powered workflow graph
      const response = await fetch(`http://localhost:5000/api/generate-graph/${projectId}`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
      });

      clearInterval(progressInterval);
      setAnalysisProgress(100);

      console.log(`📊 Analysis response status: ${response.status}`);

      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ Analysis failed with status ${response.status}:`, errorText);
        
        // Retry on server errors (5xx) but not client errors (4xx)
        if (response.status >= 500 && retryCount < maxRetries) {
          console.log(`🔄 Retrying analysis (${retryCount + 1}/${maxRetries})...`);
          await new Promise(resolve => setTimeout(resolve, 1000)); // Wait 1 second before retry
          return handleAnalysis(projectId, retryCount + 1);
        }
        
        throw new Error(`Analysis failed with status ${response.status}: ${errorText}`);
      }

      const result = await response.json();
      console.log('✅ Analysis completed successfully:', result);

      if (!result.analysis || !result.graph) {
        console.error('❌ Invalid response format:', result);
        throw new Error('Invalid response format from server');
      }

      setAnalysisResult(result.analysis);
      setGraphData(result.graph);
      setCurrentStep('complete');

      // Add to recent analyses
      const newAnalysis = {
        id: projectId,
        name: uploadedFile?.name || 'Unknown Project',
        timestamp: new Date().toISOString(),
        analysis: result.analysis,
        graph: result.graph,
        status: 'completed',
        features: {
          existing: result.analysis.existing_features?.length || 0,
          missing: result.analysis.missing_features?.length || 0,
          workflows: result.analysis.workflow_suggestions?.length || 0
        }
      };
      
      setRecentAnalyses(prev => [newAnalysis, ...prev.slice(0, 4)]); // Keep only 5 most recent

    } catch (err) {
      console.error('❌ Analysis error:', err);
      const errorMessage = err instanceof Error ? err.message : 'Analysis failed. Please try again.';
      setError(errorMessage);
      setCurrentStep('idle');
    } finally {
      setAnalyzing(false);
    }
  };

  // Reset the process
  const handleReset = () => {
    setCurrentStep('idle');
    setUploadedFile(null);
    setProjectId(null);
    setAnalysisResult(null);
    setGraphData(null);
    setError(null);
    setUploadProgress(0);
    setAnalysisProgress(0);
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  // Clear recent analyses
  const handleClearAnalyses = () => {
    setRecentAnalyses([]);
    localStorage.removeItem('recentAnalyses');
  };

  // Handle viewing workflow graph
  const handleViewWorkflowGraph = async () => {
    if (!projectId) {
      setError('No project ID available');
      return;
    }

    setLoadingGraph(true);
    setError(null);

    try {
      console.log(`🔍 Fetching workflow graph for project: ${projectId}`);
      
      const response = await fetch(`http://localhost:5000/api/graph/${projectId}`);
      
      if (!response.ok) {
        const errorText = await response.text();
        console.error(`❌ Failed to fetch graph with status ${response.status}:`, errorText);
        throw new Error(`Failed to fetch workflow graph: ${errorText}`);
      }

      const graphData = await response.json();
      console.log('✅ Workflow graph fetched successfully:', {
        nodesCount: graphData.nodes?.length || 0,
        edgesCount: graphData.edges?.length || 0,
        metadata: graphData.metadata
      });
      
      setWorkflowGraphData(graphData);
      setShowWorkflowGraph(true);
      
    } catch (err) {
      console.error('❌ Error fetching workflow graph:', err);
      const errorMessage = err instanceof Error ? err.message : 'Failed to load workflow graph';
      setError(errorMessage);
    } finally {
      setLoadingGraph(false);
    }
  };

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
                  Welcome back, <span className="font-semibold text-violet-400">{user.name || user.email}</span>! Upload your codebase for AI-powered analysis.
                </>
              ) : (
                <>Welcome back! Upload your codebase for AI-powered analysis.</>
              )}
            </p>
          </div>
        </div>

        {/* AI Codebase Upload Section */}
        <Card className="glass-effect mb-8 animate-fade-in">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <Brain className="w-6 h-6 mr-3 text-violet-400" />
              AI-Powered Codebase Analysis
            </CardTitle>
            <CardDescription>
              Upload your project ZIP file and let our AI analyze your codebase to generate intelligent workflow suggestions
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Upload Area */}
            {currentStep === 'idle' && (
              <div className="border-2 border-dashed border-violet-500/30 rounded-lg p-8 text-center hover:border-violet-500/50 transition-colors">
                <Upload className="w-12 h-12 mx-auto mb-4 text-violet-400" />
                <h3 className="text-lg font-semibold text-white mb-2">Upload Your Codebase</h3>
                <p className="text-muted-foreground mb-4">
                  Drag and drop your project ZIP file here, or click to browse
                </p>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".zip"
                  onChange={handleFileSelect}
                  className="hidden"
                />
                <Button 
                  onClick={() => fileInputRef.current?.click()}
                  className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700"
                >
                  <FileText className="w-4 h-4 mr-2" />
                  Choose ZIP File
                </Button>
                {uploadedFile && (
                  <div className="mt-4 p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
                    <p className="text-green-400 text-sm">
                      Selected: {uploadedFile.name} ({(uploadedFile.size / 1024 / 1024).toFixed(2)} MB)
                    </p>
                    <Button 
                      onClick={handleUpload}
                      className="mt-2 bg-gradient-to-r from-green-500 to-emerald-600 hover:from-green-600 hover:to-emerald-700"
                      disabled={uploading}
                    >
                      <Zap className="w-4 h-4 mr-2" />
                      {uploading ? 'Uploading...' : 'Start AI Analysis'}
                    </Button>
                  </div>
                )}
              </div>
            )}

            {/* Upload Progress */}
            {currentStep === 'uploading' && (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Upload className="w-5 h-5 text-violet-400 animate-pulse" />
                  <span className="text-white font-medium">Uploading Codebase...</span>
                </div>
                <Progress value={uploadProgress} className="h-2" />
                <p className="text-sm text-muted-foreground">
                  Uploading {uploadedFile?.name}... {uploadProgress}%
                </p>
              </div>
            )}

            {/* Analysis Progress */}
            {currentStep === 'analyzing' && (
              <div className="space-y-4">
                <div className="flex items-center space-x-3">
                  <Brain className="w-5 h-5 text-violet-400 animate-pulse" />
                  <span className="text-white font-medium">AI Analyzing Codebase...</span>
                </div>
                <Progress value={analysisProgress} className="h-2" />
                <p className="text-sm text-muted-foreground">
                  Analyzing project structure, detecting features, generating workflows... {analysisProgress}%
                </p>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mt-4">
                  <div className="text-center p-3 bg-violet-500/10 rounded-lg">
                    <Sparkles className="w-6 h-6 mx-auto mb-2 text-violet-400" />
                    <p className="text-sm text-white">Feature Detection</p>
                  </div>
                  <div className="text-center p-3 bg-blue-500/10 rounded-lg">
                    <Code className="w-6 h-6 mx-auto mb-2 text-blue-400" />
                    <p className="text-sm text-white">Code Analysis</p>
                  </div>
                  <div className="text-center p-3 bg-green-500/10 rounded-lg">
                    <GitBranch className="w-6 h-6 mx-auto mb-2 text-green-400" />
                    <p className="text-sm text-white">Workflow Generation</p>
                  </div>
                </div>
              </div>
            )}

            {/* Analysis Results */}
            {currentStep === 'complete' && analysisResult && (
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h3 className="text-xl font-semibold text-white flex items-center">
                    <CheckCircle className="w-5 h-5 mr-2 text-green-400" />
                    Analysis Complete!
                  </h3>
                  <Button onClick={handleReset} variant="outline" size="sm">
                    Analyze Another Project
                  </Button>
                </div>

                {/* Analysis Summary */}
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                  <Card className="bg-violet-500/10 border-violet-500/20">
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-violet-400">
                        {analysisResult.existing_features?.length || 0}
                      </div>
                      <p className="text-sm text-muted-foreground">Existing Features</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-orange-500/10 border-orange-500/20">
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-orange-400">
                        {analysisResult.missing_features?.length || 0}
                      </div>
                      <p className="text-sm text-muted-foreground">Missing Features</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-blue-500/10 border-blue-500/20">
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-blue-400">
                        {analysisResult.workflow_suggestions?.length || 0}
                      </div>
                      <p className="text-sm text-muted-foreground">Workflow Suggestions</p>
                    </CardContent>
                  </Card>
                  <Card className="bg-green-500/10 border-green-500/20">
                    <CardContent className="p-4 text-center">
                      <div className="text-2xl font-bold text-green-400">
                        {graphData?.nodes?.length || 0}
                      </div>
                      <p className="text-sm text-muted-foreground">Graph Nodes</p>
                    </CardContent>
                  </Card>
                </div>

                {/* Detected Features */}
                {analysisResult.existing_features && analysisResult.existing_features.length > 0 && (
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
                      <CheckCircle className="w-4 h-4 mr-2 text-green-400" />
                      Detected Features
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {analysisResult.existing_features.map((feature: any, index: number) => (
                        <div key={index} className="p-3 bg-green-500/10 border border-green-500/20 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-medium text-green-400">{feature.name}</span>
                            <Badge variant="secondary" className="text-xs">
                              {(feature.confidence * 100).toFixed(0)}%
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground">{feature.description}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Missing Features */}
                {analysisResult.missing_features && analysisResult.missing_features.length > 0 && (
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
                      <AlertCircle className="w-4 h-4 mr-2 text-orange-400" />
                      Suggested Improvements
                    </h4>
                    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                      {analysisResult.missing_features.map((feature: any, index: number) => (
                        <div key={index} className="p-3 bg-orange-500/10 border border-orange-500/20 rounded-lg">
                          <div className="flex items-center justify-between mb-2">
                            <span className="font-medium text-orange-400">{feature.name}</span>
                            <Badge 
                              variant={feature.priority === 'high' ? 'destructive' : 'secondary'}
                              className="text-xs"
                            >
                              {feature.priority}
                            </Badge>
                          </div>
                          <p className="text-sm text-muted-foreground mb-2">{feature.description}</p>
                          <p className="text-xs text-orange-300">{feature.implementation}</p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}

                {/* Technology Stack */}
                {analysisResult.technology_stack && (
                  <div>
                    <h4 className="text-lg font-semibold text-white mb-3 flex items-center">
                      <Code className="w-4 h-4 mr-2 text-blue-400" />
                      Technology Stack
                    </h4>
                    <div className="flex flex-wrap gap-2">
                      {analysisResult.technology_stack.languages?.map((lang: string, index: number) => (
                        <Badge key={index} variant="outline" className="text-blue-400 border-blue-400/30">
                          {lang}
                        </Badge>
                      ))}
                      {analysisResult.technology_stack.frameworks?.map((framework: string, index: number) => (
                        <Badge key={index} variant="outline" className="text-green-400 border-green-400/30">
                          {framework}
                        </Badge>
                      ))}
                      {analysisResult.technology_stack.databases?.map((db: string, index: number) => (
                        <Badge key={index} variant="outline" className="text-purple-400 border-purple-400/30">
                          {db}
                        </Badge>
                      ))}
                    </div>
                  </div>
                )}

                {/* Action Buttons */}
                <div className="flex flex-wrap gap-3">
                  <Button 
                    onClick={handleViewWorkflowGraph}
                    disabled={loadingGraph || !projectId}
                    className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700"
                  >
                    <Eye className="w-4 h-4 mr-2" />
                    {loadingGraph ? 'Loading Graph...' : 'View Workflow Graph'}
                  </Button>
                  <Button variant="outline">
                    <Download className="w-4 h-4 mr-2" />
                    Download Analysis Report
                  </Button>
                  <Button variant="outline">
                    <GitBranch className="w-4 h-4 mr-2" />
                    Export Workflow
                  </Button>
                </div>
              </div>
            )}

            {/* Error Display */}
            {error && (
              <div className="p-4 bg-red-500/10 border border-red-500/20 rounded-lg">
                <div className="flex items-center space-x-2">
                  <AlertCircle className="w-4 h-4 text-red-400" />
                  <span className="text-red-400">{error}</span>
                </div>
                <div className="flex space-x-2 mt-2">
                  <Button 
                    onClick={handleReset}
                    variant="outline" 
                    size="sm"
                  >
                    Try Again
                  </Button>
                  {projectId && currentStep === 'idle' && (
                    <Button 
                      onClick={() => handleAnalysis(projectId)}
                      variant="outline" 
                      size="sm"
                      className="bg-blue-500/10 border-blue-500/20 text-blue-400 hover:bg-blue-500/20"
                    >
                      Retry Analysis
                    </Button>
                  )}
                </div>
              </div>
            )}

            {/* Debug Information (only show in development) */}
            {process.env.NODE_ENV === 'development' && (
              <div className="p-4 bg-blue-500/10 border border-blue-500/20 rounded-lg">
                <h4 className="text-sm font-semibold text-blue-400 mb-2">Debug Info</h4>
                <div className="text-xs text-muted-foreground space-y-1">
                  <div>Current Step: {currentStep}</div>
                  <div>Project ID: {projectId || 'None'}</div>
                  <div>Upload Progress: {uploadProgress}%</div>
                  <div>Analysis Progress: {analysisProgress}%</div>
                  <div>Uploading: {uploading ? 'Yes' : 'No'}</div>
                  <div>Analyzing: {analyzing ? 'Yes' : 'No'}</div>
                  <div>Has Analysis Result: {analysisResult ? 'Yes' : 'No'}</div>
                  <div>Has Graph Data: {graphData ? 'Yes' : 'No'}</div>
                </div>
              </div>
            )}
          </CardContent>
        </Card>

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
                <div className="flex items-center justify-between">
                  <div>
                    <CardTitle className="text-white flex items-center">
                      <Code className="w-5 h-5 mr-2" />
                      Recent Analysis
                    </CardTitle>
                    <CardDescription>Your recently analyzed projects</CardDescription>
                  </div>
                  {recentAnalyses.length > 0 && (
                    <Button 
                      variant="outline" 
                      size="sm"
                      onClick={handleClearAnalyses}
                      className="text-red-400 border-red-400/30 hover:bg-red-400/10"
                    >
                      Clear All
                    </Button>
                  )}
                </div>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentAnalyses.length > 0 ? (
                  recentAnalyses.map((analysis, index) => (
                    <div 
                      key={analysis.id} 
                      className="glass-effect p-4 rounded-lg hover-glow cursor-pointer transition-all duration-200 hover:scale-[1.02]"
                      onClick={() => handleViewAnalysis(analysis)}
                    >
                      <div className="flex items-center justify-between mb-3">
                        <h3 className="font-semibold text-white">{analysis.name}</h3>
                        <Badge variant="default" className="bg-green-500/20 text-green-400 border-green-500/30">
                          {analysis.status}
                        </Badge>
                      </div>
                      
                      <div className="grid grid-cols-3 gap-4 mb-3">
                        <div className="text-center">
                          <div className="text-lg font-bold text-violet-400">{analysis.features.existing}</div>
                          <div className="text-xs text-muted-foreground">Features</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-orange-400">{analysis.features.missing}</div>
                          <div className="text-xs text-muted-foreground">Improvements</div>
                        </div>
                        <div className="text-center">
                          <div className="text-lg font-bold text-blue-400">{analysis.features.workflows}</div>
                          <div className="text-xs text-muted-foreground">Workflows</div>
                        </div>
                      </div>
                      
                      <div className="flex items-center justify-between text-sm text-muted-foreground">
                        <div className="flex items-center space-x-4">
                          <span className="flex items-center">
                            <Brain className="w-4 h-4 mr-1" />
                            AI Analyzed
                          </span>
                          <span>{(analysis.graph?.nodes?.length || 0) + (analysis.graph?.edges?.length || 0)} elements</span>
                        </div>
                        <span className="flex items-center">
                          <Clock className="w-4 h-4 mr-1" />
                          {new Date(analysis.timestamp).toLocaleDateString()}
                        </span>
                      </div>
                    </div>
                  ))
                ) : (
                  <div className="text-center py-8 text-muted-foreground">
                    <Brain className="w-12 h-12 mx-auto mb-4 opacity-50" />
                    <p className="text-lg font-medium mb-2">No analyses yet</p>
                    <p className="text-sm">Upload your first project to see analysis results here</p>
                  </div>
                )}
              </CardContent>
            </Card>
          </div>

          {/* Recent Activity */}
          <div>
            <Card className="glass-effect">
              <CardHeader>
                <CardTitle className="text-white flex items-center">
                  <Clock className="w-5 h-5 mr-2" />
                  Recent Activity
                </CardTitle>
                <CardDescription>Latest project activities</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                {recentActivity.map((activity, index) => (
                  <div key={index} className="flex items-start space-x-3">
                    <div className={`w-2 h-2 rounded-full mt-2 ${
                      activity.type === 'success' ? 'bg-green-400' :
                      activity.type === 'warning' ? 'bg-yellow-400' :
                      'bg-blue-400'
                    }`}></div>
                    <div className="flex-1">
                      <p className="text-sm text-white font-medium">{activity.action}</p>
                      <p className="text-xs text-muted-foreground">{activity.item}</p>
                      <p className="text-xs text-muted-foreground mt-1">
                        {activity.user} • {activity.time}
                      </p>
                    </div>
                  </div>
                ))}
              </CardContent>
            </Card>
          </div>
        </div>
      </div>

      {/* Workflow Graph Modal */}
      {showWorkflowGraph && workflowGraphData && (
        <WorkflowGraph
          graphData={workflowGraphData}
          onClose={() => setShowWorkflowGraph(false)}
        />
      )}
    </Layout>
  );
};

export default Dashboard;
