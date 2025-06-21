#!/usr/bin/env python3
"""
Backend server runner with auto-restart functionality
"""

import subprocess
import sys
import time
import os

def run_backend():
    """Run the backend server with auto-restart"""
    print("🚀 Starting FlowForge Backend Server...")
    print("📍 Backend URL: http://localhost:5000")
    print("🔍 Health Check: http://localhost:5000/api/health")
    print("=" * 50)
    
    while True:
        try:
            print(f"\n⏰ {time.strftime('%H:%M:%S')} - Starting backend server...")
            
            # Run the Flask app
            result = subprocess.run([sys.executable, 'app.py'], 
                                  cwd=os.path.dirname(os.path.abspath(__file__)),
                                  capture_output=False)
            
            if result.returncode != 0:
                print(f"❌ Server crashed with exit code {result.returncode}")
                print("🔄 Restarting in 3 seconds...")
                time.sleep(3)
            else:
                print("✅ Server stopped normally")
                break
                
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user")
            break
        except Exception as e:
            print(f"❌ Error: {e}")
            print("🔄 Restarting in 3 seconds...")
            time.sleep(3)

if __name__ == "__main__":
    run_backend() 