from flask import Flask
from flask_cors import CORS
import os

# Create upload directories if they don't exist
os.makedirs('uploads', exist_ok=True)
os.makedirs('extracted', exist_ok=True)
os.makedirs('analysis', exist_ok=True)

app = Flask(__name__)

# Configure CORS with more permissive settings
CORS(app, 
     origins=["*"],  # Allow all origins for development
     methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
     allow_headers=["Content-Type", "Authorization", "X-Requested-With"],
     supports_credentials=False)  # Set to False when using wildcard origins

# Import and register blueprints
from routes.upload import upload_bp
from routes.analysis import analysis_bp
from routes.graph import graph_bp

app.register_blueprint(upload_bp, url_prefix='/api')
app.register_blueprint(analysis_bp, url_prefix='/api')
app.register_blueprint(graph_bp, url_prefix='/api')

@app.route('/api/health', methods=['GET'])
def health_check():
    return {'status': 'healthy', 'message': 'FlowForge Backend is running'}

if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0') 