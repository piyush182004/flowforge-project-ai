from flask import Blueprint, request, jsonify, make_response
import os
import json
from datetime import datetime
from utils.ai_analyzer import AIAnalyzer
from utils.workflow_generator import WorkflowGenerator

graph_bp = Blueprint('graph', __name__)

EXTRACTED_FOLDER = 'extracted'
ANALYSIS_FOLDER = 'analysis'

@graph_bp.route('/generate-graph/<project_id>', methods=['POST', 'OPTIONS'])
def generate_graph(project_id):
    """Generate a beautiful workflow graph from the analyzed project"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = make_response()
        return response
    
    try:
        project_path = os.path.join(EXTRACTED_FOLDER, project_id)
        
        if not os.path.exists(project_path):
            return jsonify({'error': 'Project not found'}), 404
        
        # Initialize AI analyzer and workflow generator
        ai_analyzer = AIAnalyzer()
        workflow_generator = WorkflowGenerator()
        
        # Perform AI analysis
        print(f"Starting AI analysis for project: {project_id}")
        analysis_result = ai_analyzer.analyze_codebase(project_path)
        
        # Generate beautiful workflow graph
        print(f"Generating workflow graph for project: {project_id}")
        graph_data = workflow_generator.generate_workflow_graph(project_id, analysis_result)
        
        # Save graph data
        os.makedirs(ANALYSIS_FOLDER, exist_ok=True)
        graph_file = os.path.join(ANALYSIS_FOLDER, f"{project_id}_workflow_graph.json")
        with open(graph_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        # Save analysis result
        analysis_file = os.path.join(ANALYSIS_FOLDER, f"{project_id}_analysis.json")
        with open(analysis_file, 'w') as f:
            json.dump(analysis_result, f, indent=2)
        
        return jsonify({
            'project_id': project_id,
            'graph': graph_data,
            'analysis': analysis_result,
            'message': 'AI-powered workflow graph generated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Graph generation failed: {str(e)}'}), 500

@graph_bp.route('/graph/<project_id>', methods=['GET'])
def get_graph(project_id):
    """Get the generated workflow graph for a project"""
    try:
        graph_file = os.path.join(ANALYSIS_FOLDER, f"{project_id}_workflow_graph.json")
        
        if not os.path.exists(graph_file):
            return jsonify({'error': 'Workflow graph not found. Generate it first.'}), 404
        
        with open(graph_file, 'r') as f:
            graph_data = json.load(f)
        
        return jsonify(graph_data), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to load graph: {str(e)}'}), 500

@graph_bp.route('/analysis/<project_id>', methods=['GET'])
def get_analysis(project_id):
    """Get the AI analysis results for a project"""
    try:
        analysis_file = os.path.join(ANALYSIS_FOLDER, f"{project_id}_analysis.json")
        
        if not os.path.exists(analysis_file):
            return jsonify({'error': 'Analysis not found. Generate it first.'}), 404
        
        with open(analysis_file, 'r') as f:
            analysis_data = json.load(f)
        
        return jsonify(analysis_data), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to load analysis: {str(e)}'}), 500

@graph_bp.route('/simple-graph/<project_id>', methods=['POST'])
def generate_simple_graph(project_id):
    """Generate a simple workflow graph without AI analysis"""
    try:
        workflow_generator = WorkflowGenerator()
        graph_data = workflow_generator.generate_simple_workflow(project_id)
        
        # Save simple graph data
        os.makedirs(ANALYSIS_FOLDER, exist_ok=True)
        graph_file = os.path.join(ANALYSIS_FOLDER, f"{project_id}_simple_graph.json")
        with open(graph_file, 'w') as f:
            json.dump(graph_data, f, indent=2)
        
        return jsonify({
            'project_id': project_id,
            'graph': graph_data,
            'message': 'Simple workflow graph generated successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Simple graph generation failed: {str(e)}'}), 500

# Legacy functions for backward compatibility
def create_project_graph(project_path, project_id):
    """Legacy function - now uses workflow generator"""
    workflow_generator = WorkflowGenerator()
    return workflow_generator.generate_simple_workflow(project_id)

def should_include_file(file_path):
    """Legacy function - kept for compatibility"""
    ext = os.path.splitext(file_path)[1].lower()
    include_extensions = {'.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.json', '.md'}
    return ext in include_extensions

def create_node(node_id, filename, relative_path, full_path):
    """Legacy function - kept for compatibility"""
    ext = os.path.splitext(filename)[1].lower()
    
    # Determine node type and styling
    node_type = get_node_type(ext)
    node_style = get_node_style(ext)
    
    return {
        'id': node_id,
        'label': filename,
        'type': node_type,
        'data': {
            'path': relative_path,
            'full_path': full_path,
            'extension': ext,
            'language': get_language_name(ext)
        },
        'style': node_style,
        'position': {
            'x': 0,  # Will be set by the graph layout algorithm
            'y': 0
        }
    }

def get_node_type(extension):
    """Legacy function - kept for compatibility"""
    type_mapping = {
        '.py': 'python',
        '.js': 'javascript',
        '.ts': 'typescript',
        '.jsx': 'react',
        '.tsx': 'react',
        '.html': 'html',
        '.css': 'css',
        '.json': 'config',
        '.md': 'documentation'
    }
    return type_mapping.get(extension, 'file')

def get_node_style(extension):
    """Legacy function - kept for compatibility"""
    style_mapping = {
        '.py': {
            'backgroundColor': '#3776ab',
            'color': 'white',
            'borderColor': '#2d5aa0'
        },
        '.js': {
            'backgroundColor': '#f7df1e',
            'color': 'black',
            'borderColor': '#d4af37'
        },
        '.ts': {
            'backgroundColor': '#3178c6',
            'color': 'white',
            'borderColor': '#235a97'
        },
        '.jsx': {
            'backgroundColor': '#61dafb',
            'color': 'black',
            'borderColor': '#4fa8c5'
        },
        '.tsx': {
            'backgroundColor': '#61dafb',
            'color': 'black',
            'borderColor': '#4fa8c5'
        },
        '.html': {
            'backgroundColor': '#e34c26',
            'color': 'white',
            'borderColor': '#c73e1d'
        },
        '.css': {
            'backgroundColor': '#1572b6',
            'color': 'white',
            'borderColor': '#0f5a8a'
        },
        '.json': {
            'backgroundColor': '#000000',
            'color': 'white',
            'borderColor': '#333333'
        },
        '.md': {
            'backgroundColor': '#ffffff',
            'color': 'black',
            'borderColor': '#cccccc'
        }
    }
    return style_mapping.get(extension, {
        'backgroundColor': '#6c757d',
        'color': 'white',
        'borderColor': '#495057'
    })

def get_language_name(extension):
    """Legacy function - kept for compatibility"""
    language_mapping = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React JSX',
        '.tsx': 'React TSX',
        '.html': 'HTML',
        '.css': 'CSS',
        '.json': 'JSON',
        '.md': 'Markdown'
    }
    return language_mapping.get(extension, 'Unknown')

def create_file_relationships(project_path, file_to_node):
    """Legacy function - kept for compatibility"""
    edges = []
    edge_id_counter = 0
    
    # Create hierarchical relationships based on directory structure
    for file_path, node_id in file_to_node.items():
        # Find parent directory
        parent_dir = os.path.dirname(file_path)
        if parent_dir and parent_dir != '.':
            # Look for index/main files in parent directory
            parent_files = [f for f in file_to_node.keys() if os.path.dirname(f) == parent_dir]
            for parent_file in parent_files:
                if parent_file != file_path:
                    parent_node_id = file_to_node[parent_file]
                    edge_id = f"edge_{edge_id_counter}"
                    edge_id_counter += 1
                    
                    edges.append({
                        'id': edge_id,
                        'source': parent_node_id,
                        'target': node_id,
                        'type': 'hierarchical',
                        'style': {
                            'stroke': '#6c757d',
                            'strokeWidth': 1,
                            'strokeDasharray': '5,5'
                        }
                    })
    
    # Create import/require relationships (simplified)
    for file_path, node_id in file_to_node.items():
        full_path = os.path.join(project_path, file_path)
        if os.path.exists(full_path):
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    
                # Find imports/requires
                imports = find_imports(content, file_path)
                for imported_file in imports:
                    if imported_file in file_to_node:
                        imported_node_id = file_to_node[imported_file]
                        edge_id = f"edge_{edge_id_counter}"
                        edge_id_counter += 1
                        
                        edges.append({
                            'id': edge_id,
                            'source': node_id,
                            'target': imported_node_id,
                            'type': 'dependency',
                            'style': {
                                'stroke': '#28a745',
                                'strokeWidth': 2
                            }
                        })
            except Exception:
                continue
    
    return edges

def find_imports(content, file_path):
    """Legacy function - kept for compatibility"""
    imports = []
    ext = os.path.splitext(file_path)[1].lower()
    
    if ext == '.py':
        # Python imports
        import re
        import_pattern = r'^(?:from\s+(\w+(?:\.\w+)*)\s+import|import\s+(\w+(?:\.\w+)*))'
        matches = re.findall(import_pattern, content, re.MULTILINE)
        for match in matches:
            module = match[0] if match[0] else match[1]
            if module and not module.startswith('.'):
                # Convert module name to potential file path
                module_file = f"{module.replace('.', '/')}.py"
                imports.append(module_file)
    
    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        # JavaScript/TypeScript imports
        import re
        import_patterns = [
            r'import\s+(?:\{[^}]*\}|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)'
        ]
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            imports.extend(matches)
    
    return imports 