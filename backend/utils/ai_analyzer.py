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
            'missing_features': self._identify_missing_features(project_path),
            'workflow_suggestions': [],
            'complexity_analysis': self._analyze_complexity(project_path),
            'technology_stack': self._detect_tech_stack(project_path),
            'recommendations': [],
            'project_type': self._determine_project_type(project_path)
        }
        
        # Generate AI-powered insights
        ai_insights = self._generate_ai_insights(project_path, analysis_result)
        analysis_result.update(ai_insights)
        
        return analysis_result
    
    def _determine_project_type(self, project_path: str) -> str:
        """Determine the type of project based on its structure and files"""
        html_files = 0
        js_files = 0
        py_files = 0
        package_json = False
        requirements_txt = False
        dockerfile = False
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith('.html'):
                    html_files += 1
                elif file.endswith('.js') or file.endswith('.jsx') or file.endswith('.ts') or file.endswith('.tsx'):
                    js_files += 1
                elif file.endswith('.py'):
                    py_files += 1
                elif file == 'package.json':
                    package_json = True
                elif file == 'requirements.txt':
                    requirements_txt = True
                elif file.lower() == 'dockerfile':
                    dockerfile = True
        
        # Determine project type
        if html_files > 0 and js_files > 0 and not package_json and not py_files:
            return "static_website"
        elif package_json and js_files > 0:
            return "nodejs_application"
        elif requirements_txt and py_files > 0:
            return "python_application"
        elif dockerfile:
            return "containerized_application"
        elif html_files > 0:
            return "html_template"
        else:
            return "unknown"
    
    def _analyze_project_structure(self, project_path: str) -> Dict[str, Any]:
        """Analyze the overall project structure"""
        structure = {
            'total_files': 0,
            'file_types': {},
            'directories': [],
            'main_components': [],
            'entry_points': [],
            'project_structure': {}
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
        
        # Build project structure tree
        structure['project_structure'] = self._build_structure_tree(project_path)
        
        return structure
    
    def _build_structure_tree(self, project_path: str, max_depth: int = 3) -> Dict:
        """Build a tree representation of the project structure"""
        def build_tree(path, depth=0):
            if depth >= max_depth:
                return None
            
            tree = {
                'name': os.path.basename(path),
                'type': 'directory' if os.path.isdir(path) else 'file',
                'children': []
            }
            
            if os.path.isdir(path):
                try:
                    for item in os.listdir(path):
                        item_path = os.path.join(path, item)
                        
                        # Skip hidden files and common build directories
                        if item.startswith('.') or item in ['node_modules', '__pycache__', '.git', 'build', 'dist']:
                            continue
                        
                        child_tree = build_tree(item_path, depth + 1)
                        if child_tree:
                            tree['children'].append(child_tree)
                except:
                    pass
            
            return tree
        
        return build_tree(project_path)
    
    def _detect_existing_features(self, project_path: str) -> List[Dict[str, Any]]:
        """Detect existing features in the codebase with improved accuracy"""
        features = []
        project_type = self._determine_project_type(project_path)
        
        # Enhanced feature patterns based on project type
        if project_type == "static_website" or project_type == "html_template":
            features = self._detect_static_website_features(project_path)
        elif project_type == "nodejs_application":
            features = self._detect_nodejs_features(project_path)
        elif project_type == "python_application":
            features = self._detect_python_features(project_path)
        else:
            features = self._detect_generic_features(project_path)
        
        return features
    
    def _detect_static_website_features(self, project_path: str) -> List[Dict[str, Any]]:
        """Detect features specific to static websites"""
        features = []
        
        # Check for responsive design
        if self._has_responsive_design(project_path):
            features.append({
                'name': 'responsive_design',
                'confidence': 0.9,
                'files': self._find_css_files(project_path),
                'description': 'Mobile-responsive design with CSS media queries'
            })
        
        # Check for interactive elements
        if self._has_interactive_elements(project_path):
            features.append({
                'name': 'interactive_elements',
                'confidence': 0.8,
                'files': self._find_js_files(project_path),
                'description': 'JavaScript-powered interactive components'
            })
        
        # Check for contact forms
        if self._has_contact_forms(project_path):
            features.append({
                'name': 'contact_forms',
                'confidence': 0.7,
                'files': self._find_html_files(project_path),
                'description': 'Contact forms for user interaction'
            })
        
        # Check for image galleries
        if self._has_image_galleries(project_path):
                features.append({
                'name': 'image_gallery',
                'confidence': 0.6,
                'files': self._find_image_files(project_path),
                'description': 'Image gallery or carousel functionality'
                })
        
        return features
    
    def _detect_nodejs_features(self, project_path: str) -> List[Dict[str, Any]]:
        """Detect features specific to Node.js applications"""
        features = []
        
        # Check package.json for dependencies
        package_json_path = os.path.join(project_path, 'package.json')
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                dependencies = package_data.get('dependencies', {})
                dev_dependencies = package_data.get('devDependencies', {})
                all_deps = {**dependencies, **dev_dependencies}
                
                # Check for specific frameworks and libraries
                if 'express' in all_deps:
                    features.append({
                        'name': 'express_server',
                        'confidence': 0.9,
                        'files': [package_json_path],
                        'description': 'Express.js web server framework'
                    })
                
                if 'react' in all_deps:
                    features.append({
                        'name': 'react_frontend',
                        'confidence': 0.9,
                        'files': [package_json_path],
                        'description': 'React.js frontend framework'
                    })
                
                if 'mongodb' in all_deps or 'mongoose' in all_deps:
                    features.append({
                        'name': 'mongodb_database',
                        'confidence': 0.8,
                        'files': [package_json_path],
                        'description': 'MongoDB database integration'
                    })
                
                if 'jest' in all_deps or 'mocha' in all_deps:
                    features.append({
                        'name': 'testing_framework',
                        'confidence': 0.7,
                        'files': [package_json_path],
                        'description': 'Testing framework for unit tests'
                    })
                
            except:
                pass
        
        return features
    
    def _detect_python_features(self, project_path: str) -> List[Dict[str, Any]]:
        """Detect features specific to Python applications"""
        features = []
        
        # Check requirements.txt for dependencies
        requirements_path = os.path.join(project_path, 'requirements.txt')
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, 'r') as f:
                    requirements = f.read().lower()
                
                if 'flask' in requirements:
                    features.append({
                        'name': 'flask_web_framework',
                        'confidence': 0.9,
                        'files': [requirements_path],
                        'description': 'Flask web application framework'
                    })
                
                if 'django' in requirements:
                    features.append({
                        'name': 'django_framework',
                        'confidence': 0.9,
                        'files': [requirements_path],
                        'description': 'Django web application framework'
                    })
                
                if 'sqlalchemy' in requirements:
                    features.append({
                        'name': 'sql_database',
                        'confidence': 0.8,
                        'files': [requirements_path],
                        'description': 'SQL database integration with SQLAlchemy'
                    })
                
                if 'pytest' in requirements:
                    features.append({
                        'name': 'pytest_framework',
                        'confidence': 0.7,
                        'files': [requirements_path],
                        'description': 'Pytest testing framework'
                    })
                
            except:
                pass
        
        return features
    
    def _detect_generic_features(self, project_path: str) -> List[Dict[str, Any]]:
        """Detect generic features for unknown project types"""
        features = []
        
        # Check for common file patterns
        if self._has_config_files(project_path):
            features.append({
                'name': 'configuration_management',
                'confidence': 0.6,
                'files': self._find_config_files(project_path),
                'description': 'Configuration files for project settings'
            })
        
        if self._has_documentation(project_path):
            features.append({
                'name': 'documentation',
                'confidence': 0.7,
                'files': self._find_documentation_files(project_path),
                'description': 'Project documentation and guides'
            })
        
        return features
    
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
        """Detect the technology stack used in the project with accurate analysis"""
        tech_stack = {
            'languages': [],
            'frameworks': [],
            'databases': [],
            'tools': [],
            'platforms': [],
            'frontend': [],
            'backend': [],
            'build_tools': [],
            'version_control': [],
            'deployment': []
        }
        
        # Detect languages based on file extensions
        tech_stack['languages'] = self._detect_languages(project_path)
        
        # Detect frameworks and libraries
        tech_stack['frameworks'] = self._detect_frameworks(project_path)
        
        # Detect frontend technologies
        tech_stack['frontend'] = self._detect_frontend_tech(project_path)
        
        # Detect backend technologies
        tech_stack['backend'] = self._detect_backend_tech(project_path)
        
        # Detect databases
        tech_stack['databases'] = self._detect_databases(project_path)
        
        # Detect build tools
        tech_stack['build_tools'] = self._detect_build_tools(project_path)
        
        # Detect deployment platforms
        tech_stack['deployment'] = self._detect_deployment_platforms(project_path)
        
        # Detect version control
        tech_stack['version_control'] = self._detect_version_control(project_path)
        
        # Detect development tools
        tech_stack['tools'] = self._detect_development_tools(project_path)
        
        return tech_stack
    
    def _detect_languages(self, project_path: str) -> List[str]:
        """Detect programming languages based on file extensions"""
        languages = set()
        
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                ext = os.path.splitext(file)[1].lower()
                
                # Language detection by file extension
                if ext in ['.html', '.htm']:
                    languages.add('HTML')
                elif ext in ['.css', '.scss', '.sass', '.less']:
                    languages.add('CSS')
                elif ext in ['.js', '.jsx']:
                    languages.add('JavaScript')
                elif ext in ['.ts', '.tsx']:
                    languages.add('TypeScript')
                elif ext == '.py':
                    languages.add('Python')
                elif ext in ['.java', '.class']:
                    languages.add('Java')
                elif ext in ['.php']:
                    languages.add('PHP')
                elif ext in ['.rb']:
                    languages.add('Ruby')
                elif ext in ['.go']:
                    languages.add('Go')
                elif ext in ['.rs']:
                    languages.add('Rust')
                elif ext in ['.cs']:
                    languages.add('C#')
                elif ext in ['.cpp', '.cc', '.cxx']:
                    languages.add('C++')
                elif ext in ['.c']:
                    languages.add('C')
                elif ext in ['.swift']:
                    languages.add('Swift')
                elif ext in ['.kt']:
                    languages.add('Kotlin')
                elif ext in ['.scala']:
                    languages.add('Scala')
        
        return list(languages)
    
    def _detect_frameworks(self, project_path: str) -> List[str]:
        """Detect frameworks and libraries based on package files and imports"""
        frameworks = set()
        
        # Check package.json for Node.js frameworks
        package_json_path = os.path.join(project_path, 'package.json')
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                dependencies = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                # Frontend frameworks
                if 'react' in dependencies:
                    frameworks.add('React')
                if 'vue' in dependencies:
                    frameworks.add('Vue.js')
                if '@angular/core' in dependencies:
                    frameworks.add('Angular')
                if 'next' in dependencies:
                    frameworks.add('Next.js')
                if 'nuxt' in dependencies:
                    frameworks.add('Nuxt.js')
                if 'gatsby' in dependencies:
                    frameworks.add('Gatsby')
                
                # Backend frameworks
                if 'express' in dependencies:
                    frameworks.add('Express.js')
                if 'koa' in dependencies:
                    frameworks.add('Koa')
                if 'fastify' in dependencies:
                    frameworks.add('Fastify')
                if 'nest' in dependencies:
                    frameworks.add('NestJS')
                
                # UI libraries
                if 'bootstrap' in dependencies:
                    frameworks.add('Bootstrap')
                if 'tailwindcss' in dependencies:
                    frameworks.add('Tailwind CSS')
                if 'material-ui' in dependencies or '@mui/material' in dependencies:
                    frameworks.add('Material-UI')
                if 'antd' in dependencies:
                    frameworks.add('Ant Design')
                if 'chakra-ui' in dependencies:
                    frameworks.add('Chakra UI')
                
                # State management
                if 'redux' in dependencies:
                    frameworks.add('Redux')
                if 'mobx' in dependencies:
                    frameworks.add('MobX')
                if 'zustand' in dependencies:
                    frameworks.add('Zustand')
                
            except:
                pass
        
        # Check requirements.txt for Python frameworks
        requirements_path = os.path.join(project_path, 'requirements.txt')
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, 'r') as f:
                    requirements = f.read().lower()
                
                if 'django' in requirements:
                    frameworks.add('Django')
                if 'flask' in requirements:
                    frameworks.add('Flask')
                if 'fastapi' in requirements:
                    frameworks.add('FastAPI')
                if 'tornado' in requirements:
                    frameworks.add('Tornado')
                if 'pyramid' in requirements:
                    frameworks.add('Pyramid')
                
            except:
                pass
        
        # Check for other framework indicators
        if self._has_file_pattern(project_path, 'angular.json'):
            frameworks.add('Angular')
        if self._has_file_pattern(project_path, 'vue.config.js'):
            frameworks.add('Vue.js')
        if self._has_file_pattern(project_path, 'next.config.js'):
            frameworks.add('Next.js')
        if self._has_file_pattern(project_path, 'nuxt.config.js'):
            frameworks.add('Nuxt.js')
        if self._has_file_pattern(project_path, 'manage.py'):
            frameworks.add('Django')
        if self._has_file_pattern(project_path, 'app.py') and self._search_in_file(project_path, 'Flask'):
            frameworks.add('Flask')
        
        return list(frameworks)
    
    def _detect_frontend_tech(self, project_path: str) -> List[str]:
        """Detect frontend technologies"""
        frontend_tech = set()
        
        # Check for CSS frameworks
        if self._search_in_file(project_path, 'bootstrap'):
            frontend_tech.add('Bootstrap')
        if self._search_in_file(project_path, 'tailwind'):
            frontend_tech.add('Tailwind CSS')
        if self._search_in_file(project_path, 'material-ui') or self._search_in_file(project_path, '@mui'):
            frontend_tech.add('Material-UI')
        
        # Check for JavaScript libraries
        if self._search_in_file(project_path, 'jquery'):
            frontend_tech.add('jQuery')
        if self._search_in_file(project_path, 'lodash'):
            frontend_tech.add('Lodash')
        if self._search_in_file(project_path, 'moment'):
            frontend_tech.add('Moment.js')
        
        # Check for build tools
        if self._has_file_pattern(project_path, 'webpack.config.js'):
            frontend_tech.add('Webpack')
        if self._has_file_pattern(project_path, 'vite.config.js'):
            frontend_tech.add('Vite')
        if self._has_file_pattern(project_path, 'rollup.config.js'):
            frontend_tech.add('Rollup')
        
        return list(frontend_tech)
    
    def _detect_backend_tech(self, project_path: str) -> List[str]:
        """Detect backend technologies"""
        backend_tech = set()
        
        # Check for server technologies
        if self._has_file_pattern(project_path, 'package.json') and self._search_in_file(project_path, 'express'):
            backend_tech.add('Express.js')
        if self._has_file_pattern(project_path, 'requirements.txt') and self._search_in_file(project_path, 'flask'):
            backend_tech.add('Flask')
        if self._has_file_pattern(project_path, 'requirements.txt') and self._search_in_file(project_path, 'django'):
            backend_tech.add('Django')
        
        # Check for API frameworks
        if self._search_in_file(project_path, 'fastapi'):
            backend_tech.add('FastAPI')
        if self._search_in_file(project_path, 'graphql'):
            backend_tech.add('GraphQL')
        
        return list(backend_tech)
    
    def _detect_databases(self, project_path: str) -> List[str]:
        """Detect database technologies"""
        databases = set()
        
        # Check package.json for database drivers
        package_json_path = os.path.join(project_path, 'package.json')
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                
                dependencies = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                
                if 'mongoose' in dependencies or 'mongodb' in dependencies:
                    databases.add('MongoDB')
                if 'mysql' in dependencies or 'mysql2' in dependencies:
                    databases.add('MySQL')
                if 'pg' in dependencies or 'postgres' in dependencies:
                    databases.add('PostgreSQL')
                if 'sqlite3' in dependencies:
                    databases.add('SQLite')
                if 'redis' in dependencies:
                    databases.add('Redis')
                
            except:
                pass
        
        # Check requirements.txt for Python database drivers
        requirements_path = os.path.join(project_path, 'requirements.txt')
        if os.path.exists(requirements_path):
            try:
                with open(requirements_path, 'r') as f:
                    requirements = f.read().lower()
                
                if 'psycopg2' in requirements or 'postgresql' in requirements:
                    databases.add('PostgreSQL')
                if 'mysql-connector' in requirements or 'pymysql' in requirements:
                    databases.add('MySQL')
                if 'sqlite' in requirements:
                    databases.add('SQLite')
                if 'redis' in requirements:
                    databases.add('Redis')
                if 'elasticsearch' in requirements:
                    databases.add('Elasticsearch')
                
            except:
                pass
        
        return list(databases)
    
    def _detect_build_tools(self, project_path: str) -> List[str]:
        """Detect build tools and task runners"""
        build_tools = set()
        
        # Check for build tool configuration files
        if self._has_file_pattern(project_path, 'webpack.config.js'):
            build_tools.add('Webpack')
        if self._has_file_pattern(project_path, 'vite.config.js'):
            build_tools.add('Vite')
        if self._has_file_pattern(project_path, 'rollup.config.js'):
            build_tools.add('Rollup')
        if self._has_file_pattern(project_path, 'gulpfile.js'):
            build_tools.add('Gulp')
        if self._has_file_pattern(project_path, 'gruntfile.js'):
            build_tools.add('Grunt')
        if self._has_file_pattern(project_path, 'package.json') and self._search_in_file(project_path, '"scripts"'):
            build_tools.add('npm scripts')
        
        return list(build_tools)
    
    def _detect_deployment_platforms(self, project_path: str) -> List[str]:
        """Detect deployment platforms"""
        platforms = set()
        
        # Check for deployment configuration files
        if self._has_file_pattern(project_path, 'dockerfile'):
            platforms.add('Docker')
        if self._has_file_pattern(project_path, 'docker-compose.yml'):
            platforms.add('Docker Compose')
        if self._has_file_pattern(project_path, '.github/workflows'):
            platforms.add('GitHub Actions')
        if self._has_file_pattern(project_path, '.gitlab-ci.yml'):
            platforms.add('GitLab CI')
        if self._has_file_pattern(project_path, 'vercel.json'):
            platforms.add('Vercel')
        if self._has_file_pattern(project_path, 'netlify.toml'):
            platforms.add('Netlify')
        if self._has_file_pattern(project_path, 'heroku'):
            platforms.add('Heroku')
        
        return list(platforms)
    
    def _detect_version_control(self, project_path: str) -> List[str]:
        """Detect version control systems"""
        vcs = set()
        
        if os.path.exists(os.path.join(project_path, '.git')):
            vcs.add('Git')
        if os.path.exists(os.path.join(project_path, '.svn')):
            vcs.add('SVN')
        if os.path.exists(os.path.join(project_path, '.hg')):
            vcs.add('Mercurial')
        
        return list(vcs)
    
    def _detect_development_tools(self, project_path: str) -> List[str]:
        """Detect development tools and utilities"""
        tools = set()
        
        # Check for testing frameworks
        if self._has_file_pattern(project_path, 'jest.config.js') or self._search_in_file(project_path, 'jest'):
            tools.add('Jest')
        if self._has_file_pattern(project_path, 'cypress'):
            tools.add('Cypress')
        if self._search_in_file(project_path, 'pytest'):
            tools.add('pytest')
        if self._search_in_file(project_path, 'unittest'):
            tools.add('unittest')
        
        # Check for linting tools
        if self._has_file_pattern(project_path, '.eslintrc'):
            tools.add('ESLint')
        if self._has_file_pattern(project_path, '.prettierrc'):
            tools.add('Prettier')
        if self._has_file_pattern(project_path, 'flake8') or self._has_file_pattern(project_path, 'pylint'):
            tools.add('Python Linters')
        
        # Check for type checking
        if self._has_file_pattern(project_path, 'tsconfig.json'):
            tools.add('TypeScript')
        if self._search_in_file(project_path, 'mypy'):
            tools.add('MyPy')
        
        return list(tools)
    
    def _has_file_pattern(self, project_path: str, pattern: str) -> bool:
        """Check if a file matching the pattern exists"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if pattern.lower() in file.lower():
                    return True
        return False
    
    def _search_in_file(self, project_path: str, pattern: str) -> bool:
        """Search for a pattern in file contents"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.json', '.md', '.txt', '.html', '.css')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read().lower()
                            if pattern.lower() in content:
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
    
    def _identify_missing_features(self, project_path: str) -> List[Dict[str, Any]]:
        """Identify missing features that could enhance the project"""
        missing_features = []
        project_type = self._determine_project_type(project_path)
        
        if project_type == "static_website" or project_type == "html_template":
            # Check for common missing features in static websites
            if not self._has_responsive_design(project_path):
                missing_features.append({
                    'name': 'responsive_design',
                    'priority': 'high',
                    'description': 'Add mobile-responsive design with CSS media queries',
                    'implementation': 'Add CSS media queries and flexible layouts'
                })
            
            if not self._has_contact_forms(project_path):
                missing_features.append({
                    'name': 'contact_forms',
                    'priority': 'medium',
                    'description': 'Add contact forms for user interaction',
                    'implementation': 'Create HTML forms with form validation'
                })
            
            if not self._has_seo_optimization(project_path):
                missing_features.append({
                    'name': 'seo_optimization',
                    'priority': 'medium',
                    'description': 'Add SEO meta tags and optimization',
                    'implementation': 'Add meta tags, structured data, and sitemap'
                })
        
        elif project_type == "nodejs_application":
            # Check for common missing features in Node.js apps
            if not self._has_testing_framework(project_path):
                missing_features.append({
                    'name': 'testing_framework',
                    'priority': 'high',
                    'description': 'Add testing framework for code quality',
                    'implementation': 'Install Jest or Mocha with test files'
                })
            
            if not self._has_error_handling(project_path):
                missing_features.append({
                    'name': 'error_handling',
                    'priority': 'high',
                    'description': 'Add comprehensive error handling',
                    'implementation': 'Implement try-catch blocks and error middleware'
                })
        
        elif project_type == "python_application":
            # Check for common missing features in Python apps
            if not self._has_virtual_environment(project_path):
                missing_features.append({
                    'name': 'virtual_environment',
                    'priority': 'high',
                    'description': 'Add virtual environment configuration',
                    'implementation': 'Create requirements.txt and venv setup'
                })
            
            if not self._has_logging(project_path):
                missing_features.append({
                    'name': 'logging',
                    'priority': 'medium',
                    'description': 'Add proper logging system',
                    'implementation': 'Configure Python logging module'
                })
        
        return missing_features
    
    def _has_responsive_design(self, project_path: str) -> bool:
        """Check if the project has responsive design"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith('.css'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if '@media' in content or 'viewport' in content:
                                return True
                    except:
                        continue
        return False
    
    def _has_interactive_elements(self, project_path: str) -> bool:
        """Check if the project has interactive JavaScript elements"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith('.js'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if 'addEventListener' in content or 'onclick' in content or 'jquery' in content.lower():
                                return True
                    except:
                        continue
        return False
    
    def _has_contact_forms(self, project_path: str) -> bool:
        """Check if the project has contact forms"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if '<form' in content and ('contact' in content.lower() or 'email' in content.lower()):
                                return True
                    except:
                        continue
        return False
    
    def _has_image_galleries(self, project_path: str) -> bool:
        """Check if the project has image galleries"""
        image_count = 0
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    image_count += 1
                    if image_count > 5:  # If there are many images, likely a gallery
                        return True
        return False
    
    def _has_seo_optimization(self, project_path: str) -> bool:
        """Check if the project has SEO optimization"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith('.html'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if 'meta name="description"' in content or 'meta name="keywords"' in content:
                                return True
                    except:
                        continue
        return False
    
    def _has_testing_framework(self, project_path: str) -> bool:
        """Check if the project has a testing framework"""
        package_json_path = os.path.join(project_path, 'package.json')
        if os.path.exists(package_json_path):
            try:
                with open(package_json_path, 'r') as f:
                    package_data = json.load(f)
                dependencies = {**package_data.get('dependencies', {}), **package_data.get('devDependencies', {})}
                return any(dep in dependencies for dep in ['jest', 'mocha', 'chai', 'cypress'])
            except:
                pass
        return False
    
    def _has_error_handling(self, project_path: str) -> bool:
        """Check if the project has error handling"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.js', '.ts')):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if 'try' in content and 'catch' in content:
                                return True
                    except:
                        continue
        return False
    
    def _has_virtual_environment(self, project_path: str) -> bool:
        """Check if the project has virtual environment setup"""
        return os.path.exists(os.path.join(project_path, 'requirements.txt'))
    
    def _has_logging(self, project_path: str) -> bool:
        """Check if the project has logging configuration"""
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith('.py'):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            if 'import logging' in content or 'logging.' in content:
                                return True
                    except:
                        continue
        return False
    
    def _has_config_files(self, project_path: str) -> bool:
        """Check if the project has configuration files"""
        config_files = ['config.json', 'config.js', 'config.py', '.env', 'settings.py']
        for file in config_files:
            if os.path.exists(os.path.join(project_path, file)):
                return True
        return False
    
    def _has_documentation(self, project_path: str) -> bool:
        """Check if the project has documentation"""
        doc_files = ['README.md', 'README.txt', 'docs/', 'documentation/']
        for file in doc_files:
            if os.path.exists(os.path.join(project_path, file)):
                return True
        return False
    
    def _find_css_files(self, project_path: str) -> List[str]:
        """Find CSS files in the project"""
        css_files = []
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith('.css'):
                    css_files.append(os.path.relpath(os.path.join(root, file), project_path))
        return css_files
    
    def _find_js_files(self, project_path: str) -> List[str]:
        """Find JavaScript files in the project"""
        js_files = []
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.js', '.jsx', '.ts', '.tsx')):
                    js_files.append(os.path.relpath(os.path.join(root, file), project_path))
        return js_files
    
    def _find_html_files(self, project_path: str) -> List[str]:
        """Find HTML files in the project"""
        html_files = []
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith('.html'):
                    html_files.append(os.path.relpath(os.path.join(root, file), project_path))
        return html_files
    
    def _find_image_files(self, project_path: str) -> List[str]:
        """Find image files in the project"""
        image_files = []
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                    image_files.append(os.path.relpath(os.path.join(root, file), project_path))
        return image_files
    
    def _find_config_files(self, project_path: str) -> List[str]:
        """Find configuration files in the project"""
        config_files = []
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file in ['config.json', 'config.js', 'config.py', '.env', 'settings.py']:
                    config_files.append(os.path.relpath(os.path.join(root, file), project_path))
        return config_files
    
    def _find_documentation_files(self, project_path: str) -> List[str]:
        """Find documentation files in the project"""
        doc_files = []
        for root, dirs, files in os.walk(project_path):
            dirs[:] = [d for d in dirs if not d.startswith('.') and d not in ['node_modules', '__pycache__', '.git']]
            
            for file in files:
                if file.endswith(('.md', '.txt')) and 'readme' in file.lower():
                    doc_files.append(os.path.relpath(os.path.join(root, file), project_path))
        return doc_files
