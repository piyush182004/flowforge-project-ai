import os
import json
import math
from typing import Dict, List, Any, Tuple
from datetime import datetime

class WorkflowGenerator:
    """Generate beautiful, connected workflow graphs from project analysis"""
    
    def __init__(self):
        self.node_types = {
            'setup': {'color': '#3B82F6', 'icon': '⚙️'},
            'development': {'color': '#10B981', 'icon': '💻'},
            'testing': {'color': '#F59E0B', 'icon': '🧪'},
            'deployment': {'color': '#8B5CF6', 'icon': '🚀'},
            'auth': {'color': '#EF4444', 'icon': '🔐'},
            'design': {'color': '#06B6D4', 'icon': '🎨'},
            'documentation': {'color': '#84CC16', 'icon': '📚'},
            'database': {'color': '#F97316', 'icon': '🗄️'},
            'api': {'color': '#EC4899', 'icon': '🔌'},
            'frontend': {'color': '#6366F1', 'icon': '🖥️'},
            'backend': {'color': '#14B8A6', 'icon': '⚡'}
        }
    
    def generate_workflow_graph(self, project_id: str, analysis_result: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a complete workflow graph from analysis results"""
        
        # Create nodes from existing features
        feature_nodes = self._create_feature_nodes(analysis_result['existing_features'])
        
        # Create nodes from missing features
        missing_nodes = self._create_missing_feature_nodes(analysis_result['missing_features'])
        
        # Create workflow suggestion nodes based on project type
        workflow_nodes = self._create_project_specific_workflows(analysis_result)
        
        # Create nodes from the workflows
        workflow_node_list = self._create_workflow_nodes(workflow_nodes)
        
        # Combine all nodes
        all_nodes = feature_nodes + missing_nodes + workflow_node_list
        
        # Generate edges connecting the nodes
        edges = self._generate_edges(all_nodes, analysis_result)
        
        # Apply layout algorithm
        positioned_nodes = self._apply_layout(all_nodes)
        
        return {
            'nodes': positioned_nodes,
            'edges': edges,
            'metadata': {
                'project_id': project_id,
                'generated_at': datetime.now().isoformat(),
                'total_nodes': len(positioned_nodes),
                'total_edges': len(edges),
                'node_types': list(set(node['type'] for node in positioned_nodes)),
                'analysis_summary': {
                    'project_type': analysis_result.get('project_type', 'unknown'),
                    'existing_features': len(analysis_result['existing_features']),
                    'missing_features': len(analysis_result['missing_features']),
                    'workflow_suggestions': len(analysis_result['workflow_suggestions'])
                }
            }
        }
    
    def _create_feature_nodes(self, existing_features: List[Dict]) -> List[Dict]:
        """Create nodes for existing features"""
        nodes = []
        
        for i, feature in enumerate(existing_features):
            node_type = self._map_feature_to_node_type(feature['name'])
            node_style = self.node_types.get(node_type, self.node_types['development'])
            
            nodes.append({
                'id': f"feature_{i}",
                'label': feature['name'].title(),
                'type': node_type,
                'category': 'existing_feature',
                'data': {
                    'description': feature['description'],
                    'confidence': feature['confidence'],
                    'files': feature['files'],
                    'feature_name': feature['name']
                },
                'style': {
                    'backgroundColor': node_style['color'],
                    'color': 'white',
                    'borderColor': node_style['color'],
                    'borderWidth': 2,
                    'fontSize': 14,
                    'fontWeight': 'bold'
                },
                'position': {'x': 0, 'y': 0},  # Will be set by layout
                'icon': node_style['icon']
            })
        
        return nodes
    
    def _create_missing_feature_nodes(self, missing_features: List[Dict]) -> List[Dict]:
        """Create nodes for missing features"""
        nodes = []
        
        for i, feature in enumerate(missing_features):
            node_type = self._map_feature_to_node_type(feature['name'])
            node_style = self.node_types.get(node_type, self.node_types['development'])
            
            nodes.append({
                'id': f"missing_{i}",
                'label': f"Add {feature['name'].title()}",
                'type': node_type,
                'category': 'missing_feature',
                'data': {
                    'description': feature['description'],
                    'priority': feature['priority'],
                    'implementation': feature['implementation'],
                    'feature_name': feature['name']
                },
                'style': {
                    'backgroundColor': node_style['color'],
                    'color': 'white',
                    'borderColor': '#6B7280',
                    'borderWidth': 2,
                    'borderStyle': 'dashed',
                    'fontSize': 14,
                    'fontWeight': 'bold',
                    'opacity': 0.8
                },
                'position': {'x': 0, 'y': 0},  # Will be set by layout
                'icon': node_style['icon']
            })
        
        return nodes
    
    def _create_project_specific_workflows(self, analysis_result: Dict[str, Any]) -> List[Dict]:
        """Create workflow suggestions specific to the project type"""
        project_type = analysis_result.get('project_type', 'unknown')
        workflows = []
        
        if project_type == "static_website" or project_type == "html_template":
            workflows.extend(self._create_static_website_workflows(analysis_result))
        elif project_type == "nodejs_application":
            workflows.extend(self._create_nodejs_workflows(analysis_result))
        elif project_type == "python_application":
            workflows.extend(self._create_python_workflows(analysis_result))
        else:
            workflows.extend(self._create_generic_workflows(analysis_result))
        
        return workflows
    
    def _create_static_website_workflows(self, analysis_result: Dict[str, Any]) -> List[Dict]:
        """Create workflow suggestions for static websites"""
        workflows = []
        
        # Website Enhancement Workflow
        workflows.append({
            'id': 'website_enhancement',
            'name': 'Website Enhancement',
            'description': 'Improve website functionality and user experience',
            'steps': [
                {
                    'name': 'SEO Optimization',
                    'type': 'design',
                    'description': 'Add meta tags, structured data, and sitemap'
                },
                {
                    'name': 'Performance Optimization',
                    'type': 'development',
                    'description': 'Optimize images, minify CSS/JS, enable caching'
                },
                {
                    'name': 'Accessibility Audit',
                    'type': 'testing',
                    'description': 'Ensure WCAG compliance and screen reader support'
                },
                {
                    'name': 'Mobile Testing',
                    'type': 'testing',
                    'description': 'Test on various devices and screen sizes'
                }
            ]
        })
        
        # Content Management Workflow
        if 'contact_forms' in [f['name'] for f in analysis_result['existing_features']]:
            workflows.append({
                'id': 'content_management',
                'name': 'Content Management',
                'description': 'Manage and update website content',
                'steps': [
                    {
                        'name': 'Content Planning',
                        'type': 'design',
                        'description': 'Plan content updates and new pages'
                    },
                    {
                        'name': 'Content Creation',
                        'type': 'development',
                        'description': 'Create new content and update existing pages'
                    },
                    {
                        'name': 'Content Review',
                        'type': 'testing',
                        'description': 'Review content for accuracy and SEO'
                    },
                    {
                        'name': 'Content Deployment',
                        'type': 'deployment',
                        'description': 'Deploy updated content to live site'
                    }
                ]
            })
        
        return workflows
    
    def _create_nodejs_workflows(self, analysis_result: Dict[str, Any]) -> List[Dict]:
        """Create workflow suggestions for Node.js applications"""
        workflows = []
        
        # Development Workflow
        workflows.append({
            'id': 'nodejs_development',
            'name': 'Node.js Development',
            'description': 'Standard development workflow for Node.js applications',
            'steps': [
                {
                    'name': 'Environment Setup',
                    'type': 'setup',
                    'description': 'Set up development environment and dependencies'
                },
                {
                    'name': 'Feature Development',
                    'type': 'development',
                    'description': 'Develop new features and functionality'
                },
                {
                    'name': 'Unit Testing',
                    'type': 'testing',
                    'description': 'Write and run unit tests'
                },
                {
                    'name': 'Integration Testing',
                    'type': 'testing',
                    'description': 'Test API endpoints and database integration'
                },
                {
                    'name': 'Code Review',
                    'type': 'testing',
                    'description': 'Review code for quality and best practices'
                },
                {
                    'name': 'Deployment',
                    'type': 'deployment',
                    'description': 'Deploy to staging and production environments'
                }
            ]
        })
        
        # API Development Workflow
        if 'api' in [f['name'] for f in analysis_result['existing_features']]:
            workflows.append({
                'id': 'api_development',
                'name': 'API Development',
                'description': 'API endpoint development and testing',
                'steps': [
                    {
                        'name': 'API Design',
                        'type': 'design',
                        'description': 'Design API endpoints and data models'
                    },
                    {
                        'name': 'Endpoint Implementation',
                        'type': 'development',
                        'description': 'Implement API endpoints and business logic'
                    },
                    {
                        'name': 'API Testing',
                        'type': 'testing',
                        'description': 'Test API endpoints with Postman or similar tools'
                    },
                    {
                        'name': 'Documentation',
                        'type': 'documentation',
                        'description': 'Create API documentation with Swagger'
                    }
                ]
            })
        
        return workflows
    
    def _create_python_workflows(self, analysis_result: Dict[str, Any]) -> List[Dict]:
        """Create workflow suggestions for Python applications"""
        workflows = []
        
        # Python Development Workflow
        workflows.append({
            'id': 'python_development',
            'name': 'Python Development',
            'description': 'Standard development workflow for Python applications',
            'steps': [
                {
                    'name': 'Virtual Environment',
                    'type': 'setup',
                    'description': 'Set up virtual environment and install dependencies'
                },
                {
                    'name': 'Code Development',
                    'type': 'development',
                    'description': 'Develop application features and functionality'
                },
                {
                    'name': 'Testing',
                    'type': 'testing',
                    'description': 'Run unit tests and integration tests'
                },
                {
                    'name': 'Code Quality',
                    'type': 'testing',
                    'description': 'Run linting and code quality checks'
                },
                {
                    'name': 'Documentation',
                    'type': 'documentation',
                    'description': 'Update documentation and docstrings'
                },
                {
                    'name': 'Deployment',
                    'type': 'deployment',
                    'description': 'Deploy application to production'
                }
            ]
        })
        
        return workflows
    
    def _create_generic_workflows(self, analysis_result: Dict[str, Any]) -> List[Dict]:
        """Create generic workflow suggestions for unknown project types"""
        return [
            {
                'id': 'basic_development',
                'name': 'Basic Development',
                'description': 'Standard development process',
                'steps': [
                    {
                        'name': 'Project Setup',
                        'type': 'setup',
                        'description': 'Set up development environment'
                    },
                    {
                        'name': 'Feature Development',
                        'type': 'development',
                        'description': 'Develop new features'
                    },
                    {
                        'name': 'Testing',
                        'type': 'testing',
                        'description': 'Test functionality'
                    },
                    {
                        'name': 'Deployment',
                        'type': 'deployment',
                        'description': 'Deploy to production'
                    }
                ]
            }
        ]
    
    def _map_feature_to_node_type(self, feature_name: str) -> str:
        """Map feature names to node types"""
        mapping = {
            'authentication': 'auth',
            'database': 'database',
            'api': 'api',
            'frontend': 'frontend',
            'backend': 'backend',
            'deployment': 'deployment',
            'testing': 'testing',
            'documentation': 'documentation'
        }
        return mapping.get(feature_name, 'development')
    
    def _generate_edges(self, nodes: List[Dict], analysis_result: Dict) -> List[Dict]:
        """Generate edges connecting the nodes"""
        edges = []
        edge_id = 0
        
        # Connect existing features to missing features
        existing_nodes = [n for n in nodes if n['category'] == 'existing_feature']
        missing_nodes = [n for n in nodes if n['category'] == 'missing_feature']
        
        for existing in existing_nodes:
            for missing in missing_nodes:
                if self._should_connect_features(existing, missing):
                    edges.append({
                        'id': f"edge_{edge_id}",
                        'source': existing['id'],
                        'target': missing['id'],
                        'type': 'feature_dependency',
                        'style': {
                            'stroke': '#6B7280',
                            'strokeWidth': 2,
                            'strokeDasharray': '5,5'
                        },
                        'label': 'Suggests'
                    })
                    edge_id += 1
        
        # Connect workflow steps
        workflow_nodes = [n for n in nodes if n['category'] == 'workflow']
        step_nodes = [n for n in nodes if n['category'] == 'workflow_step']
        
        for workflow in workflow_nodes:
            workflow_id = workflow['data']['workflow_id']
            workflow_steps = [n for n in step_nodes if n['data']['workflow_id'] == workflow_id]
            
            # Connect workflow to its steps
            for step in workflow_steps:
                edges.append({
                    'id': f"edge_{edge_id}",
                    'source': workflow['id'],
                    'target': step['id'],
                    'type': 'workflow_step',
                    'style': {
                        'stroke': '#3B82F6',
                        'strokeWidth': 2
                    },
                    'label': 'Contains'
                })
                edge_id += 1
            
            # Connect steps in sequence
            for i in range(len(workflow_steps) - 1):
                edges.append({
                    'id': f"edge_{edge_id}",
                    'source': workflow_steps[i]['id'],
                    'target': workflow_steps[i + 1]['id'],
                    'type': 'step_sequence',
                    'style': {
                        'stroke': '#10B981',
                        'strokeWidth': 3,
                        'strokeDasharray': '0'
                    },
                    'label': 'Next'
                })
                edge_id += 1
        
        # Connect features to relevant workflow steps
        for feature in existing_nodes:
            for step in step_nodes:
                if self._should_connect_feature_to_step(feature, step):
                    edges.append({
                        'id': f"edge_{edge_id}",
                        'source': feature['id'],
                        'target': step['id'],
                        'type': 'feature_workflow',
                        'style': {
                            'stroke': '#F59E0B',
                            'strokeWidth': 2,
                            'strokeDasharray': '3,3'
                        },
                        'label': 'Enables'
                    })
                    edge_id += 1
        
        return edges
    
    def _should_connect_features(self, existing: Dict, missing: Dict) -> bool:
        """Determine if two features should be connected"""
        existing_name = existing['data']['feature_name']
        missing_name = missing['data']['feature_name']
        
        # Common feature relationships
        relationships = {
            'frontend': ['backend', 'api', 'authentication'],
            'backend': ['database', 'api', 'authentication'],
            'api': ['database', 'authentication'],
            'authentication': ['database'],
            'database': ['deployment'],
            'testing': ['deployment'],
            'documentation': ['deployment']
        }
        
        return missing_name in relationships.get(existing_name, [])
    
    def _should_connect_feature_to_step(self, feature: Dict, step: Dict) -> bool:
        """Determine if a feature should connect to a workflow step"""
        feature_name = feature['data']['feature_name']
        step_type = step['data']['step_type']
        
        # Map features to relevant step types
        feature_step_mapping = {
            'authentication': ['auth'],
            'database': ['database'],
            'api': ['api', 'development'],
            'frontend': ['frontend', 'development'],
            'backend': ['backend', 'development'],
            'testing': ['testing'],
            'documentation': ['documentation'],
            'deployment': ['deployment']
        }
        
        return step_type in feature_step_mapping.get(feature_name, [])
    
    def _apply_layout(self, nodes: List[Dict]) -> List[Dict]:
        """Apply a layout algorithm to position nodes"""
        # Simple grid layout for now
        # In a real implementation, you might use force-directed layout
        
        # Separate nodes by category
        existing_features = [n for n in nodes if n['category'] == 'existing_feature']
        missing_features = [n for n in nodes if n['category'] == 'missing_feature']
        workflows = [n for n in nodes if n['category'] == 'workflow']
        workflow_steps = [n for n in nodes if n['category'] == 'workflow_step']
        
        # Position existing features in a circle
        radius = 200
        center_x, center_y = 400, 300
        for i, node in enumerate(existing_features):
            angle = (2 * math.pi * i) / len(existing_features) if existing_features else 0
            node['position'] = {
                'x': center_x + radius * math.cos(angle),
                'y': center_y + radius * math.sin(angle)
            }
        
        # Position missing features in an outer circle
        outer_radius = 350
        for i, node in enumerate(missing_features):
            angle = (2 * math.pi * i) / len(missing_features) if missing_features else 0
            node['position'] = {
                'x': center_x + outer_radius * math.cos(angle),
                'y': center_y + outer_radius * math.sin(angle)
            }
        
        # Position workflows in a grid below
        workflow_start_y = 600
        workflow_spacing = 150
        for i, workflow in enumerate(workflows):
            workflow['position'] = {
                'x': 200 + (i * workflow_spacing),
                'y': workflow_start_y
            }
        
        # Position workflow steps in columns under their workflows
        step_spacing = 80
        for step in workflow_steps:
            workflow_id = step['data']['workflow_id']
            step_index = step['data']['step_index']
            
            # Find the workflow this step belongs to
            workflow = next((w for w in workflows if w['data']['workflow_id'] == workflow_id), None)
            if workflow:
                step['position'] = {
                    'x': workflow['position']['x'],
                    'y': workflow['position']['y'] + 100 + (step_index * step_spacing)
                }
        
        return nodes
    
    def generate_simple_workflow(self, project_id: str) -> Dict[str, Any]:
        """Generate a simple workflow for projects without detailed analysis"""
        nodes = [
            {
                'id': 'start',
                'label': 'Project Start',
                'type': 'setup',
                'position': {'x': 200, 'y': 100},
                'style': {
                    'backgroundColor': '#3B82F6',
                    'color': 'white',
                    'borderColor': '#3B82F6',
                    'borderWidth': 2
                }
            },
            {
                'id': 'develop',
                'label': 'Development',
                'type': 'development',
                'position': {'x': 400, 'y': 100},
                'style': {
                    'backgroundColor': '#10B981',
                    'color': 'white',
                    'borderColor': '#10B981',
                    'borderWidth': 2
                }
            },
            {
                'id': 'test',
                'label': 'Testing',
                'type': 'testing',
                'position': {'x': 600, 'y': 100},
                'style': {
                    'backgroundColor': '#F59E0B',
                    'color': 'white',
                    'borderColor': '#F59E0B',
                    'borderWidth': 2
                }
            },
            {
                'id': 'deploy',
                'label': 'Deployment',
                'type': 'deployment',
                'position': {'x': 800, 'y': 100},
                'style': {
                    'backgroundColor': '#8B5CF6',
                    'color': 'white',
                    'borderColor': '#8B5CF6',
                    'borderWidth': 2
                }
            }
        ]
        
        edges = [
            {
                'id': 'edge_1',
                'source': 'start',
                'target': 'develop',
                'type': 'sequence',
                'style': {
                    'stroke': '#6B7280',
                    'strokeWidth': 3
                }
            },
            {
                'id': 'edge_2',
                'source': 'develop',
                'target': 'test',
                'type': 'sequence',
                'style': {
                    'stroke': '#6B7280',
                    'strokeWidth': 3
                }
            },
            {
                'id': 'edge_3',
                'source': 'test',
                'target': 'deploy',
                'type': 'sequence',
                'style': {
                    'stroke': '#6B7280',
                    'strokeWidth': 3
                }
            }
        ]
        
        return {
            'nodes': nodes,
            'edges': edges,
            'metadata': {
                'project_id': project_id,
                'generated_at': datetime.now().isoformat(),
                'total_nodes': len(nodes),
                'total_edges': len(edges),
                'type': 'simple_workflow'
            }
        }
    
    def _create_workflow_nodes(self, workflows: List[Dict]) -> List[Dict]:
        """Create nodes for workflow suggestions"""
        nodes = []
        
        for workflow in workflows:
            workflow_id = workflow['id']
            
            # Create workflow container node
            nodes.append({
                'id': f"workflow_{workflow_id}",
                'label': workflow['name'],
                'type': 'workflow',
                'category': 'workflow',
                'data': {
                    'description': workflow['description'],
                    'workflow_id': workflow_id,
                    'steps': workflow['steps']
                },
                'style': {
                    'backgroundColor': '#1F2937',
                    'color': 'white',
                    'borderColor': '#374151',
                    'borderWidth': 3,
                    'fontSize': 16,
                    'fontWeight': 'bold',
                    'width': 200,
                    'height': 60
                },
                'position': {'x': 0, 'y': 0},  # Will be set by layout
                'icon': '🔄'
            })
            
            # Create step nodes for each workflow
            for j, step in enumerate(workflow['steps']):
                step_type = step.get('type', 'development')
                node_style = self.node_types.get(step_type, self.node_types['development'])
                
                nodes.append({
                    'id': f"step_{workflow_id}_{j}",
                    'label': step['name'],
                    'type': step_type,
                    'category': 'workflow_step',
                    'data': {
                        'workflow_id': workflow_id,
                        'step_index': j,
                        'step_type': step_type,
                        'description': step.get('description', '')
                    },
                    'style': {
                        'backgroundColor': node_style['color'],
                        'color': 'white',
                        'borderColor': node_style['color'],
                        'borderWidth': 2,
                        'fontSize': 12,
                        'fontWeight': 'normal'
                    },
                    'position': {'x': 0, 'y': 0},  # Will be set by layout
                    'icon': node_style['icon']
                })
        
        return nodes
