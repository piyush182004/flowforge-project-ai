# FlowForge - AI-Powered Project Management

FlowForge is an intelligent project management platform that analyzes your codebase and automatically generates connected, visual workflow graphs to help you understand your project structure and identify missing features.

## 🚀 Features

### AI-Powered Code Analysis
- **Automatic Feature Detection**: Analyzes your codebase to identify existing features like authentication, database integration, APIs, etc.
- **Missing Feature Suggestions**: AI suggests features that would improve your project based on detected patterns
- **Technology Stack Detection**: Automatically identifies frameworks, languages, and tools used in your project
- **Complexity Analysis**: Provides insights into code maintainability and complexity metrics

### Beautiful Workflow Generation
- **Connected Visual Graphs**: Creates beautiful, curvy workflow diagrams with smooth transitions
- **Feature Relationships**: Shows how different features connect and depend on each other
- **Workflow Suggestions**: Generates step-by-step workflows for implementing missing features
- **Interactive Visualization**: Ready-to-use graph data for frontend visualization libraries

### Complete Backend System
- **File Upload & Processing**: Secure ZIP file upload and extraction
- **RESTful API**: Clean API endpoints for frontend integration
- **AI Analysis Engine**: Comprehensive code analysis with pattern recognition
- **Graph Generation**: Advanced workflow graph creation with proper layouts

## 🏗️ Architecture

```
flowforge-project-ai/
├── frontend/                 # React + Vite frontend
│   ├── src/
│   │   ├── pages/           # Application pages
│   │   ├── components/      # UI components
│   │   └── contexts/        # React contexts
│   └── [React app files]
├── backend/                  # Flask backend
│   ├── app.py              # Main Flask application
│   ├── routes/             # API route blueprints
│   │   ├── upload.py       # File upload endpoints
│   │   ├── analysis.py     # AI analysis endpoints
│   │   └── graph.py        # Graph generation endpoints
│   ├── utils/              # Core utilities
│   │   ├── ai_analyzer.py  # AI-powered code analysis
│   │   └── workflow_generator.py # Workflow graph generation
│   ├── uploads/            # Uploaded ZIP files
│   ├── extracted/          # Extracted projects
│   └── analysis/           # Analysis results and graphs
└── README.md
```

## 🛠️ Setup

### Backend Setup

1. **Navigate to backend directory:**
   ```bash
   cd backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv venv
   
   # On Windows:
   venv\Scripts\activate
   
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Flask server:**
   ```bash
   python run.py
   ```

The backend will start on `http://localhost:5000`

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Start the development server:**
   ```bash
   npm run dev
   ```

The frontend will start on `http://localhost:5173`

## 📡 API Endpoints

### File Upload
- `POST /api/upload` - Upload project ZIP file
- `GET /api/projects` - List all uploaded projects

### AI Analysis
- `POST /api/analyze/<project_id>` - Perform AI analysis on project
- `GET /api/features/<project_id>` - Get detected features
- `GET /api/workflow-suggestions/<project_id>` - Get workflow suggestions
- `GET /api/complexity/<project_id>` - Get complexity analysis

### Graph Generation
- `POST /api/generate-graph/<project_id>` - Generate AI-powered workflow graph
- `GET /api/graph/<project_id>` - Get generated workflow graph
- `GET /api/analysis/<project_id>` - Get AI analysis results
- `POST /api/simple-graph/<project_id>` - Generate simple workflow graph

### Health Check
- `GET /api/health` - Server health status

## 🧪 Testing

Run the AI system tests:

```bash
cd backend
python test_system.py
```

This will test:
- AI code analysis
- Feature detection
- Workflow generation
- Graph creation

## 🎯 How It Works

### 1. Upload Your Codebase
Users upload a ZIP file containing their project codebase through the web interface.

### 2. AI Analysis
The system automatically:
- Extracts and analyzes the uploaded code
- Detects existing features (authentication, database, APIs, etc.)
- Identifies the technology stack
- Calculates complexity metrics
- Suggests missing features

### 3. Workflow Generation
Based on the analysis, the system generates:
- **Feature Nodes**: Visual representation of existing and missing features
- **Workflow Steps**: Step-by-step processes for implementing features
- **Connections**: Curvy, animated connections showing relationships between components
- **Layout**: Intelligent positioning of nodes for optimal visualization

### 4. Visual Output
The generated graph data includes:
- **Nodes**: Styled by feature type with icons and colors
- **Edges**: Different line styles for different relationship types
- **Metadata**: Analysis summary and project insights
- **Positioning**: Optimized layout for beautiful visualization

## 🔧 Configuration

### Environment Variables
- `FLASK_ENV`: Set to 'development' or 'production'
- `SECRET_KEY`: Flask secret key for sessions
- `OPENAI_API_KEY`: OpenAI API key for advanced AI features (optional)

### File Size Limits
- **Upload Limit**: 100MB (configurable in `config.py`)
- **Supported Formats**: ZIP files only
- **Analysis Depth**: Configurable file type filtering

## 🎨 Graph Visualization

The system generates graph data compatible with popular visualization libraries:

- **React Flow**: Perfect for React applications
- **Cytoscape.js**: Advanced graph visualization
- **D3.js**: Custom graph implementations
- **Any D3-compatible library**

### Graph Data Structure
```json
{
  "nodes": [
    {
      "id": "feature_0",
      "label": "Authentication",
      "type": "auth",
      "style": {
        "backgroundColor": "#EF4444",
        "color": "white"
      },
      "position": {"x": 400, "y": 300}
    }
  ],
  "edges": [
    {
      "id": "edge_0",
      "source": "feature_0",
      "target": "feature_1",
      "type": "dependency",
      "style": {
        "stroke": "#10B981",
        "strokeWidth": 3
      }
    }
  ],
  "metadata": {
    "project_id": "20241201_abc12345",
    "total_nodes": 10,
    "total_edges": 15
  }
}
```

## 🚀 Next Steps

### Frontend Integration
1. **Install React Flow**: `npm install reactflow`
2. **Create Graph Component**: Use the generated graph data
3. **Add Interactivity**: Node selection, zoom, pan
4. **Styling**: Customize node and edge appearances

### Advanced Features
1. **Real-time Updates**: WebSocket integration for live updates
2. **Collaboration**: Multi-user project analysis
3. **Version Control**: Track changes over time
4. **Export Options**: PNG, SVG, PDF export

### AI Enhancements
1. **OpenAI Integration**: Advanced code analysis with GPT
2. **Custom Models**: Train models on specific codebases
3. **Predictive Analysis**: Suggest future improvements
4. **Security Scanning**: Detect vulnerabilities and security issues

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Check the documentation
- Run the test suite to verify your setup

---

**FlowForge** - Revolutionizing project management with AI-powered insights and beautiful visualizations. 