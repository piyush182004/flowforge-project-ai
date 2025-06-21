#!/usr/bin/env python3
"""
Test script for the AI analysis and workflow generation system
"""

import os
import sys
import json
from utils.ai_analyzer import AIAnalyzer
from utils.workflow_generator import WorkflowGenerator

def test_ai_analyzer():
    """Test the AI analyzer with a sample project structure"""
    print("🧪 Testing AI Analyzer...")
    
    # Create a sample project structure for testing
    test_project_path = "test_project"
    os.makedirs(test_project_path, exist_ok=True)
    
    # Create sample files
    sample_files = {
        "package.json": '{"name": "test-project", "dependencies": {"react": "^18.0.0"}}',
        "src/App.js": 'import React from "react";\nfunction App() { return <div>Hello World</div>; }',
        "src/components/Login.js": 'import React from "react";\nfunction Login() { return <div>Login Form</div>; }',
        "README.md": "# Test Project\nThis is a test project for AI analysis.",
        "requirements.txt": "flask==2.3.3\nflask-cors==4.0.0"
    }
    
    for file_path, content in sample_files.items():
        full_path = os.path.join(test_project_path, file_path)
        os.makedirs(os.path.dirname(full_path), exist_ok=True)
        with open(full_path, 'w') as f:
            f.write(content)
    
    # Test AI analyzer
    try:
        ai_analyzer = AIAnalyzer()
        analysis_result = ai_analyzer.analyze_codebase(test_project_path)
        
        print("✅ AI Analysis completed successfully!")
        print(f"📊 Found {len(analysis_result['existing_features'])} existing features")
        print(f"🔍 Found {len(analysis_result['missing_features'])} missing features")
        print(f"🔄 Generated {len(analysis_result['workflow_suggestions'])} workflow suggestions")
        
        # Print detected features
        print("\n📋 Detected Features:")
        for feature in analysis_result['existing_features']:
            print(f"  - {feature['name']} (confidence: {feature['confidence']:.2f})")
        
        # Print missing features
        print("\n❌ Missing Features:")
        for feature in analysis_result['missing_features']:
            print(f"  - {feature['name']} (priority: {feature['priority']})")
        
        return analysis_result
        
    except Exception as e:
        print(f"❌ AI Analysis failed: {e}")
        return None

def test_workflow_generator(analysis_result):
    """Test the workflow generator"""
    print("\n🔄 Testing Workflow Generator...")
    
    if not analysis_result:
        print("❌ Skipping workflow generation - no analysis result")
        return None
    
    try:
        workflow_generator = WorkflowGenerator()
        graph_data = workflow_generator.generate_workflow_graph("test_project", analysis_result)
        
        print("✅ Workflow generation completed successfully!")
        print(f"📊 Generated {len(graph_data['nodes'])} nodes")
        print(f"🔗 Generated {len(graph_data['edges'])} edges")
        
        # Print node types
        node_types = set(node['type'] for node in graph_data['nodes'])
        print(f"🎨 Node types: {', '.join(node_types)}")
        
        # Print edge types
        edge_types = set(edge['type'] for edge in graph_data['edges'])
        print(f"🔗 Edge types: {', '.join(edge_types)}")
        
        return graph_data
        
    except Exception as e:
        print(f"❌ Workflow generation failed: {e}")
        return None

def test_simple_workflow():
    """Test simple workflow generation"""
    print("\n🚀 Testing Simple Workflow Generator...")
    
    try:
        workflow_generator = WorkflowGenerator()
        simple_graph = workflow_generator.generate_simple_workflow("simple_test")
        
        print("✅ Simple workflow generation completed successfully!")
        print(f"📊 Generated {len(simple_graph['nodes'])} nodes")
        print(f"🔗 Generated {len(simple_graph['edges'])} edges")
        
        return simple_graph
        
    except Exception as e:
        print(f"❌ Simple workflow generation failed: {e}")
        return None

def cleanup_test_files():
    """Clean up test files"""
    import shutil
    test_project_path = "test_project"
    if os.path.exists(test_project_path):
        shutil.rmtree(test_project_path)
        print("🧹 Cleaned up test files")

def main():
    """Main test function"""
    print("🚀 Starting AI Analysis and Workflow Generation Tests")
    print("=" * 60)
    
    # Test AI analyzer
    analysis_result = test_ai_analyzer()
    
    # Test workflow generator
    graph_data = test_workflow_generator(analysis_result)
    
    # Test simple workflow
    simple_graph = test_simple_workflow()
    
    # Clean up
    cleanup_test_files()
    
    print("\n" + "=" * 60)
    if analysis_result and graph_data and simple_graph:
        print("🎉 All tests passed! The AI system is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the errors above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1) 