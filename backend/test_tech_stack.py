#!/usr/bin/env python3
"""
Test script to check technology stack detection with real project data
"""

from utils.ai_analyzer import AIAnalyzer
import json

def test_tech_stack_detection():
    """Test the technology stack detection with real project data"""
    
    # Test with the Villa Agency project
    project_path = 'extracted/20250621_084636_7b729154'
    
    print("🔍 Testing Technology Stack Detection...")
    print(f"📁 Project Path: {project_path}")
    print("-" * 50)
    
    # Initialize analyzer
    analyzer = AIAnalyzer()
    
    # Perform analysis
    result = analyzer.analyze_codebase(project_path)
    
    # Display technology stack results
    tech_stack = result['technology_stack']
    
    print("🏷️  Project Type:", result['project_type'])
    print()
    
    print("🛠️  Technology Stack Analysis:")
    print("=" * 40)
    
    print("📝 Languages:")
    for lang in tech_stack['languages']:
        print(f"   • {lang}")
    if not tech_stack['languages']:
        print("   • No languages detected")
    print()
    
    print("⚙️  Frameworks:")
    for framework in tech_stack['frameworks']:
        print(f"   • {framework}")
    if not tech_stack['frameworks']:
        print("   • No frameworks detected")
    print()
    
    print("🖥️  Frontend Technologies:")
    for tech in tech_stack['frontend']:
        print(f"   • {tech}")
    if not tech_stack['frontend']:
        print("   • No frontend technologies detected")
    print()
    
    print("⚡ Backend Technologies:")
    for tech in tech_stack['backend']:
        print(f"   • {tech}")
    if not tech_stack['backend']:
        print("   • No backend technologies detected")
    print()
    
    print("🗄️  Databases:")
    for db in tech_stack['databases']:
        print(f"   • {db}")
    if not tech_stack['databases']:
        print("   • No databases detected")
    print()
    
    print("🔨 Build Tools:")
    for tool in tech_stack['build_tools']:
        print(f"   • {tool}")
    if not tech_stack['build_tools']:
        print("   • No build tools detected")
    print()
    
    print("🚀 Deployment Platforms:")
    for platform in tech_stack['deployment']:
        print(f"   • {platform}")
    if not tech_stack['deployment']:
        print("   • No deployment platforms detected")
    print()
    
    print("📦 Version Control:")
    for vcs in tech_stack['version_control']:
        print(f"   • {vcs}")
    if not tech_stack['version_control']:
        print("   • No version control detected")
    print()
    
    print("🛠️  Development Tools:")
    for tool in tech_stack['tools']:
        print(f"   • {tool}")
    if not tech_stack['tools']:
        print("   • No development tools detected")
    print()
    
    # Save detailed results
    output_file = 'tech_stack_test_results.json'
    with open(output_file, 'w') as f:
        json.dump(tech_stack, f, indent=2)
    
    print(f"📄 Detailed tech stack saved to: {output_file}")
    print("✅ Technology Stack Detection Complete!")

if __name__ == "__main__":
    test_tech_stack_detection() 