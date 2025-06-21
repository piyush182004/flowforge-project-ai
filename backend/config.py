import os

class Config:
    """Base configuration class"""
    # Flask settings
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    # Upload settings
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB max file size
    UPLOAD_FOLDER = 'uploads'
    EXTRACTED_FOLDER = 'extracted'
    ANALYSIS_FOLDER = 'analysis'
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'zip'}
    
    # File processing settings
    MAX_FILE_SIZE = 50 * 1024 * 1024  # 50MB
    SUPPORTED_LANGUAGES = {
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
    
    # Graph generation settings
    MAX_GRAPH_NODES = 1000
    MAX_GRAPH_EDGES = 5000
    
    # Security settings
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5173', 'http://127.0.0.1:5173']
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration"""
        # Create necessary directories
        for folder in [Config.UPLOAD_FOLDER, Config.EXTRACTED_FOLDER, Config.ANALYSIS_FOLDER]:
            os.makedirs(folder, exist_ok=True)

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # Stricter settings for production
    MAX_CONTENT_LENGTH = 50 * 1024 * 1024  # 50MB max file size
    MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB

class TestingConfig(Config):
    """Testing configuration"""
    TESTING = True
    DEBUG = True

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
} 