import React, { useState, useCallback } from 'react';
import Layout from '@/components/Layout';
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { Button } from '@/components/ui/button';
import { Badge } from '@/components/ui/badge';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { 
  Plus, 
  MoreVertical, 
  User, 
  Calendar, 
  Clock, 
  Flag, 
  MessageSquare,
  CheckCircle,
  Circle,
  AlertCircle,
  Play,
  Pause,
  Square,
  Users,
  BarChart3,
  Filter,
  Search,
  PlusCircle,
  X,
  Edit,
  Trash2,
  Eye
} from 'lucide-react';
import { useAuth } from '@/contexts/AuthContext';

interface Task {
  id: string;
  title: string;
  description: string;
  status: 'backlog' | 'todo' | 'in-progress' | 'review' | 'done';
  priority: 'low' | 'medium' | 'high' | 'urgent';
  assignee: string;
  storyPoints: number;
  dueDate: string;
  tags: string[];
}

const ScrumBoard = () => {
  const { user } = useAuth();
  const [tasks, setTasks] = useState<Task[]>([
    {
      id: '1',
      title: 'Implement user authentication',
      description: 'Add JWT-based authentication with login/signup functionality',
      status: 'in-progress',
      priority: 'high',
      assignee: 'Sarah Chen',
      storyPoints: 8,
      dueDate: '2025-06-25',
      tags: ['backend', 'security']
    },
    {
      id: '2',
      title: 'Design responsive dashboard',
      description: 'Create mobile-friendly dashboard with modern UI components',
      status: 'todo',
      priority: 'medium',
      assignee: 'Mike Johnson',
      storyPoints: 5,
      dueDate: '2025-06-28',
      tags: ['frontend', 'design']
    },
    {
      id: '3',
      title: 'Set up CI/CD pipeline',
      description: 'Configure automated testing and deployment workflow',
      status: 'review',
      priority: 'high',
      assignee: 'Alex Rodriguez',
      storyPoints: 13,
      dueDate: '2025-06-30',
      tags: ['devops', 'testing']
    },
    {
      id: '4',
      title: 'Write API documentation',
      description: 'Create comprehensive API documentation with examples',
      status: 'done',
      priority: 'low',
      assignee: 'Emma Wilson',
      storyPoints: 3,
      dueDate: '2025-06-22',
      tags: ['documentation']
    }
  ]);

  const [showAddTask, setShowAddTask] = useState(false);
  const [showEditTask, setShowEditTask] = useState(false);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [newTask, setNewTask] = useState({
    title: '',
    description: '',
    priority: 'medium' as const,
    assignee: '',
    storyPoints: 1,
    dueDate: '',
    tags: ''
  });

  const columns = [
    { id: 'backlog', title: 'Backlog', color: 'bg-slate-100 dark:bg-slate-800' },
    { id: 'todo', title: 'To Do', color: 'bg-blue-50 dark:bg-blue-900/20' },
    { id: 'in-progress', title: 'In Progress', color: 'bg-yellow-50 dark:bg-yellow-900/20' },
    { id: 'review', title: 'Review', color: 'bg-purple-50 dark:bg-purple-900/20' },
    { id: 'done', title: 'Done', color: 'bg-green-50 dark:bg-green-900/20' }
  ];

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'urgent': return 'bg-red-500 text-white';
      case 'high': return 'bg-orange-500 text-white';
      case 'medium': return 'bg-yellow-500 text-white';
      case 'low': return 'bg-green-500 text-white';
      default: return 'bg-gray-500 text-white';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'done': return <CheckCircle className="w-4 h-4 text-green-500" />;
      case 'in-progress': return <Play className="w-4 h-4 text-blue-500" />;
      case 'review': return <Eye className="w-4 h-4 text-purple-500" />;
      case 'todo': return <Circle className="w-4 h-4 text-gray-400" />;
      default: return <Square className="w-4 h-4 text-gray-400" />;
    }
  };

  const getTasksByStatus = (status: string) => {
    return tasks.filter(task => task.status === status);
  };

  const handleAddTask = () => {
    if (!newTask.title.trim()) return;

    const task: Task = {
      id: Date.now().toString(),
      title: newTask.title,
      description: newTask.description,
      status: 'backlog',
      priority: newTask.priority,
      assignee: newTask.assignee,
      storyPoints: newTask.storyPoints,
      dueDate: newTask.dueDate,
      tags: newTask.tags.split(',').map(tag => tag.trim()).filter(Boolean)
    };

    setTasks([...tasks, task]);
    setNewTask({
      title: '',
      description: '',
      priority: 'medium',
      assignee: '',
      storyPoints: 1,
      dueDate: '',
      tags: ''
    });
    setShowAddTask(false);
  };

  const handleEditTask = () => {
    if (!editingTask || !editingTask.title.trim()) return;

    setTasks(prev => prev.map(task => 
      task.id === editingTask.id ? editingTask : task
    ));
    setEditingTask(null);
    setShowEditTask(false);
  };

  const handleDeleteTask = (taskId: string) => {
    setTasks(prev => prev.filter(task => task.id !== taskId));
  };

  const openEditTask = (task: Task) => {
    setEditingTask(task);
    setShowEditTask(true);
  };

  const moveTask = useCallback((taskId: string, newStatus: Task['status']) => {
    setTasks(prev => prev.map(task => 
      task.id === taskId ? { ...task, status: newStatus } : task
    ));
  }, []);

  const handleDragStart = (e: React.DragEvent, taskId: string) => {
    e.dataTransfer.setData('taskId', taskId);
  };

  const handleDragOver = (e: React.DragEvent) => {
    e.preventDefault();
  };

  const handleDrop = (e: React.DragEvent, newStatus: Task['status']) => {
    e.preventDefault();
    const taskId = e.dataTransfer.getData('taskId');
    moveTask(taskId, newStatus);
  };

  const getSprintStats = () => {
    const totalTasks = tasks.length;
    const completedTasks = tasks.filter(t => t.status === 'done').length;
    const progress = totalTasks > 0 ? (completedTasks / totalTasks) * 100 : 0;
    const totalStoryPoints = tasks.reduce((sum, task) => sum + task.storyPoints, 0);
    const completedStoryPoints = tasks
      .filter(t => t.status === 'done')
      .reduce((sum, task) => sum + task.storyPoints, 0);

    return {
      totalTasks,
      completedTasks,
      progress,
      totalStoryPoints,
      completedStoryPoints
    };
  };

  const stats = getSprintStats();

  return (
    <Layout>
      <div className="container mx-auto px-6 py-8">
        {/* Header */}
        <div className="flex flex-col lg:flex-row justify-between items-start lg:items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold gradient-text mb-2">Scrum Board</h1>
            <p className="text-muted-foreground">
              Manage your agile development workflow with our interactive scrum board
            </p>
          </div>
          <div className="flex items-center space-x-3 mt-4 lg:mt-0">
            <Button variant="outline" className="flex items-center space-x-2">
              <Filter className="w-4 h-4" />
              <span>Filter</span>
            </Button>
            <Button variant="outline" className="flex items-center space-x-2">
              <Search className="w-4 h-4" />
              <span>Search</span>
            </Button>
            <Button 
              onClick={() => setShowAddTask(true)}
              className="bg-gradient-to-r from-violet-500 to-purple-600 hover:from-violet-600 hover:to-purple-700"
            >
              <PlusCircle className="w-4 h-4 mr-2" />
              Add Task
            </Button>
          </div>
        </div>

        {/* Sprint Stats */}
        <Card className="mb-8 glass-effect">
          <CardHeader>
            <CardTitle className="text-white flex items-center">
              <BarChart3 className="w-5 h-5 mr-2 text-violet-400" />
              Sprint 12 - Core Features
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="grid grid-cols-1 md:grid-cols-5 gap-6">
              <div className="text-center">
                <div className="text-2xl font-bold text-violet-400">{stats.completedTasks}/{stats.totalTasks}</div>
                <p className="text-sm text-muted-foreground">Tasks Completed</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-green-400">{stats.progress.toFixed(1)}%</div>
                <p className="text-sm text-muted-foreground">Progress</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-blue-400">{stats.completedStoryPoints}/{stats.totalStoryPoints}</div>
                <p className="text-sm text-muted-foreground">Story Points</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-orange-400">9</div>
                <p className="text-sm text-muted-foreground">Days Remaining</p>
              </div>
              <div className="text-center">
                <div className="text-2xl font-bold text-cyan-400">24</div>
                <p className="text-sm text-muted-foreground">Velocity</p>
              </div>
            </div>
            <div className="mt-4">
              <div className="flex justify-between text-sm text-muted-foreground mb-1">
                <span>Progress</span>
                <span>{stats.progress.toFixed(1)}%</span>
              </div>
              <div className="w-full bg-slate-700 rounded-full h-2">
                <div 
                  className="bg-gradient-to-r from-violet-500 to-purple-600 h-2 rounded-full transition-all duration-300"
                  style={{ width: `${stats.progress}%` }}
                ></div>
              </div>
            </div>
          </CardContent>
        </Card>

        {/* Scrum Board */}
        <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">
          {columns.map((column) => (
            <div key={column.id} className="space-y-4">
              <div className="flex items-center justify-between">
                <h3 className="font-semibold text-white">{column.title}</h3>
                <Badge variant="secondary" className="bg-slate-700 text-slate-300">
                  {getTasksByStatus(column.id).length}
                </Badge>
              </div>
              <div 
                className={`${column.color} rounded-lg p-4 space-y-4`}
                onDragOver={handleDragOver}
                onDrop={(e) => handleDrop(e, column.id as Task['status'])}
              >
                {getTasksByStatus(column.id).map((task) => (
                  <Card 
                    key={task.id} 
                    className="cursor-pointer hover:shadow-lg transition-all duration-200 group"
                    draggable
                    onDragStart={(e) => handleDragStart(e, task.id)}
                  >
                    <CardContent className="p-4">
                      <div className="flex items-start justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          {getStatusIcon(task.status)}
                          <h4 className="font-medium text-sm line-clamp-2">{task.title}</h4>
                        </div>
                        <div className="opacity-0 group-hover:opacity-100 transition-opacity">
                          <div className="flex items-center space-x-1">
                            <Button 
                              variant="ghost" 
                              size="sm" 
                              className="h-6 w-6 p-0"
                              onClick={() => openEditTask(task)}
                            >
                              <Edit className="w-3 h-3" />
                            </Button>
                            <Button 
                              variant="ghost" 
                              size="sm" 
                              className="h-6 w-6 p-0 text-red-500 hover:text-red-700"
                              onClick={() => handleDeleteTask(task.id)}
                            >
                              <Trash2 className="w-3 h-3" />
                            </Button>
                          </div>
                        </div>
                      </div>
                      
                      <p className="text-xs text-muted-foreground mb-3 line-clamp-2">
                        {task.description}
                      </p>

                      <div className="flex items-center justify-between mb-3">
                        <Badge className={`text-xs ${getPriorityColor(task.priority)}`}>
                          {task.priority}
                        </Badge>
                        <div className="flex items-center space-x-1 text-xs text-muted-foreground">
                          <Flag className="w-3 h-3" />
                          <span>{task.storyPoints}</span>
                        </div>
                      </div>

                      <div className="flex items-center justify-between text-xs text-muted-foreground">
                        <div className="flex items-center space-x-1">
                          <User className="w-3 h-3" />
                          <span>{task.assignee}</span>
                        </div>
                        <div className="flex items-center space-x-1">
                          <Calendar className="w-3 h-3" />
                          <span>{new Date(task.dueDate).toLocaleDateString()}</span>
                        </div>
                      </div>

                      {task.tags.length > 0 && (
                        <div className="flex flex-wrap gap-1 mt-2">
                          {task.tags.map((tag, index) => (
                            <Badge key={index} variant="outline" className="text-xs">
                              {tag}
                            </Badge>
                          ))}
                        </div>
                      )}
                    </CardContent>
                  </Card>
                ))}
                
                {/* Empty state for columns with no tasks */}
                {getTasksByStatus(column.id).length === 0 && (
                  <div className="text-center py-8 text-muted-foreground">
                    <div className="text-sm opacity-50">No tasks</div>
                    <div className="text-xs opacity-30 mt-1">Drop tasks here</div>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Add Task Modal */}
        {showAddTask && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
            <Card className="w-full max-w-md">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Add New Task</CardTitle>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={() => setShowAddTask(false)}
                    className="h-6 w-6 p-0"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
                <CardDescription>Create a new task for your scrum board</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Title</label>
                  <Input
                    value={newTask.title}
                    onChange={(e) => setNewTask({ ...newTask, title: e.target.value })}
                    placeholder="Enter task title"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Description</label>
                  <Textarea
                    value={newTask.description}
                    onChange={(e) => setNewTask({ ...newTask, description: e.target.value })}
                    placeholder="Enter task description"
                    rows={3}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">Priority</label>
                    <select
                      value={newTask.priority}
                      onChange={(e) => setNewTask({ ...newTask, priority: e.target.value as any })}
                      className="w-full p-2 border rounded-md bg-background"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="urgent">Urgent</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Story Points</label>
                    <Input
                      type="number"
                      value={newTask.storyPoints}
                      onChange={(e) => setNewTask({ ...newTask, storyPoints: parseInt(e.target.value) })}
                      min="1"
                      max="21"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">Assignee</label>
                    <Input
                      value={newTask.assignee}
                      onChange={(e) => setNewTask({ ...newTask, assignee: e.target.value })}
                      placeholder="Enter assignee"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium">Due Date</label>
                    <Input
                      type="date"
                      value={newTask.dueDate}
                      onChange={(e) => setNewTask({ ...newTask, dueDate: e.target.value })}
                    />
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium">Tags (comma-separated)</label>
                  <Input
                    value={newTask.tags}
                    onChange={(e) => setNewTask({ ...newTask, tags: e.target.value })}
                    placeholder="frontend, backend, bug"
                  />
                </div>
                <div className="flex space-x-2">
                  <Button onClick={handleAddTask} className="flex-1">
                    Add Task
                  </Button>
                  <Button variant="outline" onClick={() => setShowAddTask(false)}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}

        {/* Edit Task Modal */}
        {showEditTask && editingTask && (
          <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50">
            <Card className="w-full max-w-md">
              <CardHeader>
                <div className="flex items-center justify-between">
                  <CardTitle>Edit Task</CardTitle>
                  <Button 
                    variant="ghost" 
                    size="sm" 
                    onClick={() => setShowEditTask(false)}
                    className="h-6 w-6 p-0"
                  >
                    <X className="w-4 h-4" />
                  </Button>
                </div>
                <CardDescription>Update task details</CardDescription>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <label className="text-sm font-medium">Title</label>
                  <Input
                    value={editingTask.title}
                    onChange={(e) => setEditingTask({ ...editingTask, title: e.target.value })}
                    placeholder="Enter task title"
                  />
                </div>
                <div>
                  <label className="text-sm font-medium">Description</label>
                  <Textarea
                    value={editingTask.description}
                    onChange={(e) => setEditingTask({ ...editingTask, description: e.target.value })}
                    placeholder="Enter task description"
                    rows={3}
                  />
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">Priority</label>
                    <select
                      value={editingTask.priority}
                      onChange={(e) => setEditingTask({ ...editingTask, priority: e.target.value as any })}
                      className="w-full p-2 border rounded-md bg-background"
                    >
                      <option value="low">Low</option>
                      <option value="medium">Medium</option>
                      <option value="high">High</option>
                      <option value="urgent">Urgent</option>
                    </select>
                  </div>
                  <div>
                    <label className="text-sm font-medium">Story Points</label>
                    <Input
                      type="number"
                      value={editingTask.storyPoints}
                      onChange={(e) => setEditingTask({ ...editingTask, storyPoints: parseInt(e.target.value) })}
                      min="1"
                      max="21"
                    />
                  </div>
                </div>
                <div className="grid grid-cols-2 gap-4">
                  <div>
                    <label className="text-sm font-medium">Assignee</label>
                    <Input
                      value={editingTask.assignee}
                      onChange={(e) => setEditingTask({ ...editingTask, assignee: e.target.value })}
                      placeholder="Enter assignee"
                    />
                  </div>
                  <div>
                    <label className="text-sm font-medium">Due Date</label>
                    <Input
                      type="date"
                      value={editingTask.dueDate}
                      onChange={(e) => setEditingTask({ ...editingTask, dueDate: e.target.value })}
                    />
                  </div>
                </div>
                <div>
                  <label className="text-sm font-medium">Tags (comma-separated)</label>
                  <Input
                    value={editingTask.tags.join(', ')}
                    onChange={(e) => setEditingTask({ 
                      ...editingTask, 
                      tags: e.target.value.split(',').map(tag => tag.trim()).filter(Boolean)
                    })}
                    placeholder="frontend, backend, bug"
                  />
                </div>
                <div className="flex space-x-2">
                  <Button onClick={handleEditTask} className="flex-1">
                    Update Task
                  </Button>
                  <Button variant="outline" onClick={() => setShowEditTask(false)}>
                    Cancel
                  </Button>
                </div>
              </CardContent>
            </Card>
          </div>
        )}
      </div>
    </Layout>
  );
};

export default ScrumBoard; 