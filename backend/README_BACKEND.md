# FlowForge Backend Server

## Quick Start

### Option 1: Simple Start (Manual)
```bash
cd backend
python app.py
```

### Option 2: Auto-Restart (Recommended)
```bash
cd backend
python run_backend.py
```

### Option 3: Windows Batch File
```bash
cd backend
start_backend.bat
```

## Backend URLs

- **Main Server**: http://localhost:5000
- **Health Check**: http://localhost:5000/api/health
- **Upload Endpoint**: http://localhost:5000/api/upload
- **Graph Generation**: http://localhost:5000/api/generate-graph/{project_id}

## Troubleshooting

### If you get CORS errors:
1. Make sure the backend is running (check http://localhost:5000/api/health)
2. Make sure you're running from the `backend` directory
3. Refresh your browser (Ctrl+Shift+R)

### If the server keeps stopping:
1. Use `python run_backend.py` for auto-restart functionality
2. Check for Python errors in the terminal
3. Make sure all dependencies are installed: `pip install -r requirements.txt`

### If uploads fail:
1. Check that the `uploads`, `extracted`, and `analysis` directories exist
2. Make sure you have write permissions in the backend directory
3. Check the terminal for error messages

## Server Status

The backend should show:
```
* Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: xxx-xxx-xxx
```

If you don't see this, the server is not running properly. 