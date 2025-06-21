from flask import Blueprint, request, jsonify, make_response
import os
import zipfile
import shutil
from werkzeug.utils import secure_filename
from datetime import datetime
import uuid

upload_bp = Blueprint('upload', __name__)

UPLOAD_FOLDER = 'uploads'
EXTRACTED_FOLDER = 'extracted'
ALLOWED_EXTENSIONS = {'zip'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def extract_zip(zip_path, extract_to):
    """Extract zip file to specified directory"""
    try:
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        return True
    except Exception as e:
        print(f"Error extracting zip: {e}")
        return False

@upload_bp.route('/upload', methods=['POST', 'OPTIONS'])
def upload_file():
    """Handle file upload and extraction"""
    # Handle preflight OPTIONS request
    if request.method == 'OPTIONS':
        response = make_response()
        return response
    
    try:
        if 'project' not in request.files:
            return jsonify({'error': 'No file part'}), 400
        
        file = request.files['project']
        if file.filename == '':
            return jsonify({'error': 'No selected file'}), 400
        
        if not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type. Only .zip files are allowed'}), 400
        
        # Generate unique filename
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_id = str(uuid.uuid4())[:8]
        original_filename = secure_filename(file.filename)
        filename = f"{timestamp}_{unique_id}_{original_filename}"
        
        # Save uploaded file
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        
        # Extract the zip file
        project_id = f"{timestamp}_{unique_id}"
        extract_path = os.path.join(EXTRACTED_FOLDER, project_id)
        os.makedirs(extract_path, exist_ok=True)
        
        if not extract_zip(filepath, extract_path):
            return jsonify({'error': 'Failed to extract zip file'}), 500
        
        # Get project structure
        project_structure = get_project_structure(extract_path)
        
        return jsonify({
            'message': 'File uploaded and extracted successfully',
            'project_id': project_id,
            'filename': original_filename,
            'extract_path': extract_path,
            'structure': project_structure
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

def get_project_structure(directory, max_depth=3, current_depth=0):
    """Get the structure of the extracted project"""
    if current_depth >= max_depth:
        return None
    
    structure = {
        'name': os.path.basename(directory),
        'type': 'directory',
        'children': []
    }
    
    try:
        for item in os.listdir(directory):
            item_path = os.path.join(directory, item)
            
            # Skip hidden files and common build directories
            if item.startswith('.') or item in ['node_modules', '__pycache__', '.git', 'build', 'dist']:
                continue
            
            if os.path.isdir(item_path):
                child_structure = get_project_structure(item_path, max_depth, current_depth + 1)
                if child_structure:
                    structure['children'].append(child_structure)
            else:
                # Only include certain file types
                if item.endswith(('.py', '.js', '.ts', '.jsx', '.tsx', '.html', '.css', '.json', '.md', '.txt')):
                    structure['children'].append({
                        'name': item,
                        'type': 'file',
                        'extension': os.path.splitext(item)[1]
                    })
    except Exception as e:
        print(f"Error reading directory {directory}: {e}")
    
    return structure

@upload_bp.route('/projects', methods=['GET'])
def list_projects():
    """List all uploaded projects"""
    try:
        projects = []
        if os.path.exists(EXTRACTED_FOLDER):
            for project_dir in os.listdir(EXTRACTED_FOLDER):
                project_path = os.path.join(EXTRACTED_FOLDER, project_dir)
                if os.path.isdir(project_path):
                    projects.append({
                        'id': project_dir,
                        'name': project_dir,
                        'created_at': datetime.fromtimestamp(os.path.getctime(project_path)).isoformat()
                    })
        
        return jsonify({'projects': projects}), 200
    except Exception as e:
        return jsonify({'error': f'Failed to list projects: {str(e)}'}), 500 