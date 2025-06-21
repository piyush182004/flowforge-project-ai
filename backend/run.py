#!/usr/bin/env python3
"""
FlowForge Backend Runner
Simple script to start the Flask application
"""

import os
import sys
from app import app
from config import config

def main():
    """Main entry point for the application"""
    # Get configuration from environment
    config_name = os.environ.get('FLASK_ENV', 'development')
    
    # Initialize app with configuration
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    
    # Get port from environment or use default
    port = int(os.environ.get('PORT', 5000))
    
    print(f"Starting FlowForge Backend on port {port}")
    print(f"Environment: {config_name}")
    print(f"Debug mode: {app.config['DEBUG']}")
    
    # Run the application
    app.run(
        host='0.0.0.0',
        port=port,
        debug=app.config['DEBUG']
    )

if __name__ == '__main__':
    main() 