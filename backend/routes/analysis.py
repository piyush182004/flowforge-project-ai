from flask import Blueprint, request, jsonify
import os
import re
from pathlib import Path
from utils.ai_analyzer import AIAnalyzer

analysis_bp = Blueprint('analysis', __name__)

EXTRACTED_FOLDER = 'extracted'

@analysis_bp.route('/analyze/<project_id>', methods=['POST'])
def analyze_project(project_id):
    """Analyze the uploaded project and generate insights"""
    try:
        project_path = os.path.join(EXTRACTED_FOLDER, project_id)
        
        if not os.path.exists(project_path):
            return jsonify({'error': 'Project not found'}), 404
        
        # Initialize AI analyzer
        ai_analyzer = AIAnalyzer()
        
        # Perform comprehensive AI analysis
        analysis_result = ai_analyzer.analyze_codebase(project_path)
        
        return jsonify({
            'project_id': project_id,
            'analysis': analysis_result,
            'message': 'AI analysis completed successfully'
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Analysis failed: {str(e)}'}), 500

@analysis_bp.route('/features/<project_id>', methods=['GET'])
def get_project_features(project_id):
    """Get detected features for a project"""
    try:
        project_path = os.path.join(EXTRACTED_FOLDER, project_id)
        
        if not os.path.exists(project_path):
            return jsonify({'error': 'Project not found'}), 404
        
        ai_analyzer = AIAnalyzer()
        analysis_result = ai_analyzer.analyze_codebase(project_path)
        
        return jsonify({
            'project_id': project_id,
            'existing_features': analysis_result['existing_features'],
            'missing_features': analysis_result['missing_features'],
            'technology_stack': analysis_result['technology_stack']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get features: {str(e)}'}), 500

@analysis_bp.route('/workflow-suggestions/<project_id>', methods=['GET'])
def get_workflow_suggestions(project_id):
    """Get workflow suggestions for a project"""
    try:
        project_path = os.path.join(EXTRACTED_FOLDER, project_id)
        
        if not os.path.exists(project_path):
            return jsonify({'error': 'Project not found'}), 404
        
        ai_analyzer = AIAnalyzer()
        analysis_result = ai_analyzer.analyze_codebase(project_path)
        
        return jsonify({
            'project_id': project_id,
            'workflow_suggestions': analysis_result['workflow_suggestions'],
            'recommendations': analysis_result['recommendations']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get workflow suggestions: {str(e)}'}), 500

@analysis_bp.route('/complexity/<project_id>', methods=['GET'])
def get_project_complexity(project_id):
    """Get complexity analysis for a project"""
    try:
        project_path = os.path.join(EXTRACTED_FOLDER, project_id)
        
        if not os.path.exists(project_path):
            return jsonify({'error': 'Project not found'}), 404
        
        ai_analyzer = AIAnalyzer()
        analysis_result = ai_analyzer.analyze_codebase(project_path)
        
        return jsonify({
            'project_id': project_id,
            'complexity_analysis': analysis_result['complexity_analysis'],
            'project_overview': analysis_result['project_overview']
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Failed to get complexity analysis: {str(e)}'}), 500

# Legacy functions for backward compatibility
def perform_code_analysis(project_path):
    """Legacy function - now uses AI analyzer"""
    ai_analyzer = AIAnalyzer()
    return ai_analyzer.analyze_codebase(project_path)

def analyze_file(file_path, relative_path):
    """Legacy function - kept for compatibility"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
            lines = content.split('\n')
    except Exception:
        return None
    
    file_analysis = {
        'path': relative_path,
        'lines': len(lines),
        'language': get_language_from_extension(file_path),
        'is_entry_point': False,
        'dependencies': []
    }
    
    # Determine if it's an entry point
    if is_entry_point(file_path, content):
        file_analysis['is_entry_point'] = True
    
    # Extract dependencies based on file type
    file_analysis['dependencies'] = extract_dependencies(file_path, content)
    
    return file_analysis

def get_language_from_extension(file_path):
    """Get programming language from file extension"""
    ext = Path(file_path).suffix.lower()
    language_map = {
        '.py': 'Python',
        '.js': 'JavaScript',
        '.ts': 'TypeScript',
        '.jsx': 'React JSX',
        '.tsx': 'React TSX',
        '.html': 'HTML',
        '.css': 'CSS',
        '.json': 'JSON',
        '.md': 'Markdown',
        '.txt': 'Text'
    }
    return language_map.get(ext, 'Unknown')

def is_entry_point(file_path, content):
    """Determine if a file is an entry point"""
    filename = os.path.basename(file_path).lower()
    
    # Common entry point patterns
    entry_patterns = [
        'main.py', 'app.py', 'index.py', '__main__.py',
        'main.js', 'index.js', 'app.js',
        'main.ts', 'index.ts', 'app.ts',
        'package.json', 'requirements.txt', 'setup.py'
    ]
    
    if filename in entry_patterns:
        return True
    
    # Check for common entry point indicators in content
    entry_indicators = [
        'if __name__ == "__main__"',
        'def main(',
        'function main(',
        'export default',
        'ReactDOM.render',
        'createApp('
    ]
    
    return any(indicator in content for indicator in entry_indicators)

def extract_dependencies(file_path, content):
    """Extract dependencies from file content"""
    dependencies = []
    ext = Path(file_path).suffix.lower()
    
    if ext == '.py':
        # Python imports
        import_pattern = r'^(?:from\s+(\w+(?:\.\w+)*)\s+import|import\s+(\w+(?:\.\w+)*))'
        matches = re.findall(import_pattern, content, re.MULTILINE)
        for match in matches:
            dep = match[0] if match[0] else match[1]
            if dep and not dep.startswith('.'):
                dependencies.append(dep.split('.')[0])
    
    elif ext in ['.js', '.jsx', '.ts', '.tsx']:
        # JavaScript/TypeScript imports
        import_patterns = [
            r'import\s+(?:\{[^}]*\}|\w+)\s+from\s+[\'"]([^\'"]+)[\'"]',
            r'require\s*\(\s*[\'"]([^\'"]+)[\'"]\s*\)',
            r'import\s+[\'"]([^\'"]+)[\'"]'
        ]
        for pattern in import_patterns:
            matches = re.findall(pattern, content)
            dependencies.extend(matches)
    
    elif ext == '.json':
        # Package.json dependencies
        try:
            import json
            data = json.loads(content)
            if 'dependencies' in data:
                dependencies.extend(data['dependencies'].keys())
            if 'devDependencies' in data:
                dependencies.extend(data['devDependencies'].keys())
        except:
            pass
    
    return list(set(dependencies))

def calculate_complexity_score(analysis):
    """Calculate a complexity score based on analysis"""
    score = 0
    
    # Base score from file count
    score += min(analysis['file_count'] * 2, 50)
    
    # Language diversity penalty
    lang_count = len(analysis['languages'])
    score += lang_count * 10
    
    # Lines of code factor
    score += min(analysis['lines_of_code'] // 100, 30)
    
    # Dependencies factor
    score += min(len(analysis['dependencies']) * 3, 40)
    
    return min(score, 100)  # Cap at 100

def generate_structure_insights(project_path):
    """Generate insights about project structure"""
    insights = {
        'has_frontend': False,
        'has_backend': False,
        'has_database': False,
        'framework': None,
        'build_tools': [],
        'structure_type': 'unknown'
    }
    
    # Check for common patterns
    files = []
    for root, dirs, filenames in os.walk(project_path):
        files.extend([os.path.join(root, f) for f in filenames])
    
    file_names = [os.path.basename(f).lower() for f in files]
    
    # Detect frameworks and tools
    if 'package.json' in file_names:
        insights['has_frontend'] = True
        insights['build_tools'].append('npm/yarn')
    
    if 'requirements.txt' in file_names or 'setup.py' in file_names:
        insights['has_backend'] = True
        insights['build_tools'].append('pip')
    
    if any('docker' in f for f in file_names):
        insights['build_tools'].append('docker')
    
    if any('webpack' in f for f in file_names):
        insights['build_tools'].append('webpack')
    
    # Determine structure type
    if insights['has_frontend'] and insights['has_backend']:
        insights['structure_type'] = 'fullstack'
    elif insights['has_frontend']:
        insights['structure_type'] = 'frontend'
    elif insights['has_backend']:
        insights['structure_type'] = 'backend'
    
    return insights 