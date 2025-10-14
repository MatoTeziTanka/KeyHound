#!/usr/bin/env python3
"""
KeyHound Enhanced - Simple Live Test
Simple test to get KeyHound running live.
"""

import os
import sys
import time
import threading
from pathlib import Path

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def test_core_functionality():
    """Test core functionality."""
    print("Testing core functionality...")
    
    try:
        # Test simple keyhound
        from core.simple_keyhound import SimpleKeyHound
        
        print("  [OK] SimpleKeyHound imported successfully")
        
        # Initialize
        keyhound = SimpleKeyHound(verbose=False)
        print("  [OK] SimpleKeyHound initialized")
        
        # Test system info
        system_info = keyhound.get_system_info()
        print(f"  [OK] System info: {system_info['Platform']}, {system_info['CPU Cores']} cores, {system_info['Memory']}")
        
        # Test brainwallet security (quick)
        print("  [INFO] Testing brainwallet security...")
        brainwallet_results = keyhound.test_brainwallet_security(["password", "123456", "test"])
        vulnerable_count = sum(1 for r in brainwallet_results if r.get("vulnerable", False))
        print(f"  [OK] Brainwallet test: {len(brainwallet_results)} patterns tested, {vulnerable_count} vulnerable")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Core functionality test failed: {e}")
        return False

def test_web_dependencies():
    """Test web dependencies."""
    print("Testing web dependencies...")
    
    try:
        import flask
        print(f"  [OK] Flask {flask.__version__}")
        
        try:
            import flask_socketio
            print(f"  [OK] Flask-SocketIO available")
        except ImportError:
            print("  [WARN] Flask-SocketIO not available (install with: pip install flask-socketio)")
        
        return True
        
    except ImportError as e:
        print(f"  [FAIL] Web dependencies missing: {e}")
        print("  Install with: pip install flask flask-socketio")
        return False

def start_simple_web_server():
    """Start a simple web server for testing."""
    print("Starting simple web server...")
    
    try:
        from flask import Flask, jsonify
        
        app = Flask(__name__)
        
        @app.route('/')
        def index():
            return '''
            <html>
            <head><title>KeyHound Enhanced - Live Test</title></head>
            <body>
                <h1>KeyHound Enhanced - Live Test</h1>
                <p>System is running successfully!</p>
                <p><a href="/api/health">Health Check</a></p>
                <p><a href="/api/stats">System Stats</a></p>
            </body>
            </html>
            '''
        
        @app.route('/api/health')
        def health():
            return jsonify({
                'status': 'healthy',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'keyhound': 'running'
            })
        
        @app.route('/api/stats')
        def stats():
            try:
                from core.simple_keyhound import SimpleKeyHound
                keyhound = SimpleKeyHound(verbose=False)
                system_info = keyhound.get_system_info()
                perf_stats = keyhound.get_performance_stats()
                
                return jsonify({
                    'system': system_info,
                    'performance': perf_stats,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception as e:
                return jsonify({'error': str(e)})
        
        print("  [OK] Simple web server created")
        
        # Start server in background thread
        def run_server():
            app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
        
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        
        # Wait for server to start
        time.sleep(3)
        
        print("  [OK] Web server started on http://localhost:8080")
        print("  [INFO] Available endpoints:")
        print("    - http://localhost:8080 (Main page)")
        print("    - http://localhost:8080/api/health (Health check)")
        print("    - http://localhost:8080/api/stats (System stats)")
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Failed to start web server: {e}")
        return False

def test_live_functionality():
    """Test live functionality."""
    print("Testing live functionality...")
    
    try:
        import requests
        
        # Test health endpoint
        response = requests.get('http://localhost:8080/api/health', timeout=5)
        if response.status_code == 200:
            health_data = response.json()
            print(f"  [OK] Health check: {health_data['status']}")
        else:
            print(f"  [FAIL] Health check failed: {response.status_code}")
            return False
        
        # Test stats endpoint
        response = requests.get('http://localhost:8080/api/stats', timeout=5)
        if response.status_code == 200:
            stats_data = response.json()
            print(f"  [OK] Stats endpoint working")
            if 'system' in stats_data:
                print(f"    Platform: {stats_data['system'].get('Platform', 'Unknown')}")
                print(f"    CPU Cores: {stats_data['system'].get('CPU Cores', 'Unknown')}")
                print(f"    Memory: {stats_data['system'].get('Memory', 'Unknown')}")
        else:
            print(f"  [FAIL] Stats endpoint failed: {response.status_code}")
            return False
        
        return True
        
    except Exception as e:
        print(f"  [FAIL] Live functionality test failed: {e}")
        return False

def main():
    """Main entry point."""
    print("=" * 60)
    print("KeyHound Enhanced - Simple Live Test")
    print("=" * 60)
    
    # Test core functionality
    if not test_core_functionality():
        print("\n[FAILED] Core functionality test failed")
        return 1
    
    # Test web dependencies
    if not test_web_dependencies():
        print("\n[FAILED] Web dependencies test failed")
        return 1
    
    # Start web server
    if not start_simple_web_server():
        print("\n[FAILED] Web server startup failed")
        return 1
    
    # Test live functionality
    if not test_live_functionality():
        print("\n[FAILED] Live functionality test failed")
        return 1
    
    print("\n" + "=" * 60)
    print("KEYHOUND ENHANCED IS LIVE AND WORKING!")
    print("=" * 60)
    print("Web Interface: http://localhost:8080")
    print("Health Check: http://localhost:8080/api/health")
    print("System Stats: http://localhost:8080/api/stats")
    print("\nPress Ctrl+C to stop the server")
    
    try:
        # Keep running
        while True:
            time.sleep(60)
            print(f"[{time.strftime('%H:%M:%S')}] KeyHound Enhanced is running...")
    except KeyboardInterrupt:
        print("\nStopping KeyHound Enhanced...")
        print("Server stopped.")
    
    return 0

if __name__ == '__main__':
    sys.exit(main())
