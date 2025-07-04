import os
import re
import json
from pathlib import Path
from typing import Dict, List, Any

class AIAnalyzer:
    """AI-powered code analyzer for feature detection and workflow generation"""
    
    def __init__(self):
        self.analysis_cache = {}
    
    def analyze_codebase(self, project_path: str) -> Dict[str, Any]:
        """Comprehensive analysis of the entire codebase"""
        print(f"Starting AI analysis of: {project_path}")
        
        analysis_result = {
            'project_overview': self._analyze_project_structure(project_path),
            'existing_features': self._detect_existing_features(project_path),
            'missing_features': [],
            'workflow_suggestions': [],
            'complexity_analysis': self._analyze_complexity(project_path),
            'technology_stack': self._detect_tech_stack(project_path),
            'recommendations': []
        }
        
        # Generate AI-powered insights
        ai_insights = self._generate_ai_insights(project_path, analysis_result)
        analysis_result.update(ai_insights)
        
        return analysis_result
    
    def _analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
        """Analyze the overall project structure"""
        structure = {
            'total_files': 0,
            'file_types': {},
            'directories': [],
            'main_components': [],
            'entry_points': []
        }
        
        for root, dirs, files in os.walk(project_path):
            # Skip common directories
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git', 'build', 'dist']]
            
            for file in files:
                structure['total_files'] += 1
                ext = Path(file).suffix.lower()
                structure['file_types'][ext] = structure['file_types'].get(ext, 0) + 1
                
                # Detect entry points
                if self._is_entry_point(file):
                    structure['entry_points'].append(os.path.join(root, file))
        
        return structure
    
    def _detect_existing_features(self, project_path: str) -> List[Dict[str, Any]]:
        """Detect existing features in the codebase"""
        features = []
        
        # Common feature patterns
        feature_patterns = {
            'authentication': {
                'patterns': [
                    r'auth|login|signin|signup|register|password|jwt|token',
                    r'firebase|auth0|oauth|google.*auth|facebook.*auth'
                ],
                'files': ['auth', 'login', 'user', 'session']
            },
            'database': {
                'patterns': [
                    r'database|db|sql|mongodb|postgres|mysql|sqlite',
                    r'prisma|sequelize|mongoose|django.*models'
                ],
                'files': ['database', 'models', 'schema', 'migration']
            },
            'api': {
                'patterns': [
                    r'api|endpoint|route|controller|rest|graphql',
                    r'fetch|axios|http|request|response'
                ],
                'files': ['api', 'routes', 'controllers', 'endpoints']
            },
            'frontend': {
                'patterns': [
                    r'react|vue|angular|component|jsx|tsx',
                    r'html|css|javascript|typescript|frontend'
                ],
                'files': ['components', 'pages', 'views', 'frontend']
            },
            'backend': {
                'patterns': [
                    r'server|backend|express|flask|django|fastapi',
                    r'node|python|java|spring|dotnet'
                ],
                'files': ['server', 'backend', 'app', 'main']
            },
            'deployment': {
                'patterns': [
                    r'docker|kubernetes|deploy|ci|cd|github.*actions',
                    r'heroku|vercel|netlify|aws|azure|gcp'
                ],
                'files': ['dockerfile', 'deploy', 'ci', 'github']
            },
            'testing': {
                'patterns': [
                    r'test|spec|jest|mocha|pytest|unittest',
                    r'cypress|selenium|playwright|testing'
                ],
                'files': ['test', 'spec', 'testing', '__tests__']
            },
            'documentation': {
                'patterns': [
                    r'readme|docs|documentation|wiki|guide',
                    r'comment|docstring|javadoc|jsdoc'
                ],
                'files': ['readme', 'docs', 'documentation']
            }
        }
        
        for feature_name, patterns in feature_patterns.items():
            if self._detect_feature_in_project(project_path, patterns):
                features.append({
                    'name': feature_name,
                    'confidence': self._calculate_feature_confidence(project_path, patterns),
                    'files': self._find_feature_files(project_path, patterns),
                    'description': self._get_feature_description(feature_name)
                })
        
        return features
    
    def _detect_feature_in_project(self, project_path: str, patterns: Dict) -> bool:
        """Check if a feature exists in the project"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            # Check file names
            for file in files:
                file_lower = file.lower()
                if any(pattern in file_lower for pattern in patterns['files']):
                    return True
            
            # Check file contents
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.md')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            for pattern in patterns['patterns']:
                                if re.search(pattern, content, re.IGNORECASE):
                                    return True
                    except:
                        continue
        
        return False
    
    def _calculate_feature_confidence(self, project_path: str, patterns: Dict) -> float:
        """Calculate confidence score for feature detection"""
        matches = 0
        total_checks = 0
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                total_checks += 1
                file_lower = file.lower()
                
                # Check file names
                if any(pattern in file_lower for pattern in patterns['files']):
                    matches += 1
                
                # Check file contents
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.md')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            for pattern in patterns['patterns']:
                                if re.search(pattern, content, re.IGNORECASE):
                                    matches += 1
                                    break
                    except:
                        continue
        
        return min(matches / max(total_checks, 1), 1.0)
    
    def _find_feature_files(self, project_path: str, patterns: Dict) -> List[str]:
        """Find files related to a specific feature"""
        feature_files = []
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, project_path)
                
                # Check file names
                file_lower = file.lower()
                if any(pattern in file_lower for pattern in patterns['files']):
                    feature_files.append(relative_path)
                    continue
                
                # Check file contents
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.md')):
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            for pattern in patterns['patterns']:
                                if re.search(pattern, content, re.IGNORECASE):
                                    feature_files.append(relative_path)
                                    break
                    except:
                        continue
        
        return list(set(feature_files))
    
    def _get_feature_description(self, feature_name: str) -> str:
        """Get description for a detected feature"""
        descriptions = {
            'authentication': 'User authentication and authorization system',
            'database': 'Database integration and data management',
            'api': 'API endpoints and data communication',
            'frontend': 'User interface and client-side functionality',
            'backend': 'Server-side logic and business processes',
            'deployment': 'Deployment and CI/CD configuration',
            'testing': 'Testing framework and test coverage',
            'documentation': 'Project documentation and guides'
        }
        return descriptions.get(feature_name, f'{feature_name} functionality')
    
    def _analyze_complexity(self, project_path: str) -> Dict[str, Any]:
        """Analyze code complexity and maintainability"""
        complexity = {
            'cyclomatic_complexity': 0,
            'lines_of_code': 0,
            'function_count': 0,
            'class_count': 0,
            'comment_ratio': 0.0,
            'maintainability_index': 0
        }
        
        total_lines = 0
        comment_lines = 0
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            lines = f.readlines()
                            total_lines += len(lines)
                            
                            for line in lines:
                                stripped = line.strip()
                                if stripped.startswith('#') or stripped.startswith('//') or stripped.startswith('/*'):
                                    comment_lines += 1
                    except:
                        continue
        
        complexity['lines_of_code'] = total_lines
        complexity['comment_ratio'] = comment_lines / max(total_lines, 1)
        complexity['maintainability_index'] = self._calculate_maintainability_index(complexity)
        
        return complexity
    
    def _calculate_maintainability_index(self, complexity: Dict) -> float:
        """Calculate maintainability index (0-100, higher is better)"""
        # Simplified maintainability calculation
        loc = complexity['lines_of_code']
        cc = complexity['cyclomatic_complexity']
        comment_ratio = complexity['comment_ratio']
        
        if loc == 0:
            return 100.0
        
        # Basic formula: higher comments, lower complexity = better maintainability
        maintainability = 100.0
        maintainability -= min(cc / 10, 50)  # Penalty for high complexity
        maintainability += min(comment_ratio * 20, 20)  # Bonus for comments
        maintainability -= min(loc / 1000, 30)  # Penalty for very large codebase
        
        return max(0.0, min(100.0, maintainability))
    
    def _detect_tech_stack(self, project_path: str) -> Dict[str, Any]:
        """Detect the technology stack used in the project"""
        tech_stack = {
            'languages': set(),
            'frameworks': set(),
            'databases': set(),
            'tools': set(),
            'platforms': set()
        }
        
        # Check for package files
        package_files = {
            'package.json': 'nodejs',
            'requirements.txt': 'python',
            'pom.xml': 'java',
            'build.gradle': 'java',
            'Cargo.toml': 'rust',
            'go.mod': 'go'
        }
        
        for file, language in package_files.items():
            if os.path.exists(os.path.join(project_path, file)):
                tech_stack['languages'].add(language)
        
        # Detect frameworks and tools
        framework_patterns = {
            'react': r'react|jsx|tsx',
            'vue': r'vue|vuex',
            'angular': r'angular|ng-',
            'express': r'express|express\.js',
            'django': r'django',
            'flask': r'flask',
            'fastapi': r'fastapi',
            'spring': r'spring|@spring',
            'laravel': r'laravel',
            'rails': r'rails|ruby.*on.*rails'
        }
        
        for framework, pattern in framework_patterns.items():
            if self._search_pattern_in_project(project_path, pattern):
                tech_stack['frameworks'].add(framework)
        
        # Detect databases
        db_patterns = {
            'postgresql': r'postgres|postgresql|psycopg2',
            'mysql': r'mysql|mysqldb',
            'mongodb': r'mongo|mongodb',
            'sqlite': r'sqlite',
            'redis': r'redis',
            'elasticsearch': r'elasticsearch|elastic'
        }
        
        for db, pattern in db_patterns.items():
            if self._search_pattern_in_project(project_path, pattern):
                tech_stack['databases'].add(db)
        
        # Convert sets to lists for JSON serialization
        return {k: list(v) for k, v in tech_stack.items()}
    
    def _search_pattern_in_project(self, project_path: str, pattern: str) -> bool:
        """Search for a pattern in the entire project"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.md', '.txt')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if re.search(pattern, content, re.IGNORECASE):
                                return True
                    except:
                        continue
        
        return False
    
    def _is_entry_point(self, filename: str) -> bool:
        """Check if a file is likely an entry point"""
        entry_patterns = [
            'main.py', 'app.py', 'index.py', '__main__.py',
            'main.js', 'index.js', 'app.js',
            'main.ts', 'index.ts', 'app.ts',
            'package.json', 'requirements.txt', 'setup.py'
        ]
        return filename.lower() in entry_patterns
    
    def _generate_ai_insights(self, project_path: str, analysis_result: Dict) -> Dict[str, Any]:
        """Generate AI-powered insights and recommendations"""
        return self._generate_mock_ai_insights(analysis_result)
    
    def _generate_mock_ai_insights(self, analysis_result: Dict) -> Dict[str, Any]:
        """Generate mock AI insights when OpenAI is not available"""
        existing_features = [f['name'] for f in analysis_result['existing_features']]
        
        # Common missing features based on existing ones
        missing_features = []
        if 'authentication' not in existing_features:
            missing_features.append({
                'name': 'authentication',
                'priority': 'high',
                'description': 'User authentication system',
                'implementation': 'Add login/signup functionality with JWT tokens'
            })
        
        if 'testing' not in existing_features:
            missing_features.append({
                'name': 'testing',
                'priority': 'medium',
                'description': 'Automated testing framework',
                'implementation': 'Implement unit and integration tests'
            })
        
        if 'documentation' not in existing_features:
            missing_features.append({
                'name': 'documentation',
                'priority': 'low',
                'description': 'Project documentation',
                'implementation': 'Add README and API documentation'
            })
        
        # Generate workflow suggestions
        workflow_suggestions = self._generate_workflow_suggestions(analysis_result)
        
        return {
            'missing_features': missing_features,
            'workflow_suggestions': workflow_suggestions,
            'recommendations': [
                'Consider adding automated testing for better code quality',
                'Implement proper error handling and logging',
                'Add API documentation for better developer experience',
                'Consider implementing CI/CD pipeline for automated deployment'
            ]
        }
    
    def _generate_workflow_suggestions(self, analysis_result: Dict) -> List[Dict[str, Any]]:
        """Generate workflow suggestions based on analysis"""
        suggestions = []
        
        # Add feature-specific workflows
        existing_features = [f['name'] for f in analysis_result['existing_features']]
        
        if 'authentication' in existing_features:
            suggestions.append({
                'id': 'auth_flow',
                'name': 'Authentication Flow',
                'description': 'User registration and login process',
                'steps': [
                    {'name': 'User Registration', 'type': 'auth'},
                    {'name': 'Email Verification', 'type': 'auth'},
                    {'name': 'User Login', 'type': 'auth'},
                    {'name': 'Session Management', 'type': 'auth'}
                ]
            })
        
        if 'api' in existing_features:
            suggestions.append({
                'id': 'api_flow',
                'name': 'API Development Flow',
                'description': 'API endpoint development process',
                'steps': [
                    {'name': 'API Design', 'type': 'design'},
                    {'name': 'Endpoint Implementation', 'type': 'development'},
                    {'name': 'API Testing', 'type': 'testing'},
                    {'name': 'Documentation', 'type': 'documentation'}
                ]
            })
        
        # Always add basic workflow
        suggestions.append({
            'id': 'basic_flow',
            'name': 'Basic Development Flow',
            'description': 'Standard development process',
            'steps': [
                {'name': 'Project Setup', 'type': 'setup'},
                {'name': 'Feature Development', 'type': 'development'},
                {'name': 'Testing', 'type': 'testing'},
                {'name': 'Deployment', 'type': 'deployment'}
            ]
        })
        
        return suggestions
