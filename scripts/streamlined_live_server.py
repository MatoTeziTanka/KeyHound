#!/usr/bin/env python3
"""
KeyHound Enhanced - Streamlined Live Server
Optimized version focusing on core Bitcoin puzzle solving and cryptography.
Brainwallet functionality phased out due to no high-value targets.
"""

import os
import sys
import time
import threading
from pathlib import Path

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

def start_streamlined_live_server():
    """Start the streamlined KeyHound Enhanced live server."""
    print("=" * 80)
    print("KeyHound Enhanced - Streamlined Live Server")
    print("=" * 80)
    print("Focus: Bitcoin Puzzle Solving & Core Cryptography")
    print("Brainwallet: PHASED OUT (No high-value targets found)")
    print("=" * 80)
    
    try:
        # Test core functionality first
        print("Initializing KeyHound Enhanced...")
        
        from core.simple_keyhound import SimpleKeyHound
        keyhound = SimpleKeyHound(verbose=False)
        
        # Get system info
        system_info = keyhound.get_system_info()
        print(f"System: {system_info.get('platform', 'Unknown')}")
        print(f"CPU Cores: {system_info.get('cpu_count', 'Unknown')}")
        print(f"Memory: {system_info.get('memory_total', 0) / (1024**3):.1f} GB")
        
        print("  [OK] KeyHound Enhanced initialized successfully")
        
        # Create Flask app
        from flask import Flask, jsonify, render_template_string
        
        app = Flask(__name__)
        
        # Main dashboard page
        dashboard_html = '''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>KeyHound Enhanced - Live Dashboard</title>
            <style>
                body {
                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                    background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
                    color: #ffffff;
                    margin: 0;
                    padding: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                }
                .header {
                    text-align: center;
                    margin-bottom: 30px;
                }
                .header h1 {
                    color: #00ff88;
                    font-size: 2.5em;
                    margin: 0;
                    text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
                }
                .stats-grid {
                    display: grid;
                    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                    gap: 20px;
                    margin-bottom: 30px;
                }
                .stat-card {
                    background: rgba(22, 33, 62, 0.8);
                    border: 1px solid #333366;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                }
                .stat-value {
                    font-size: 2em;
                    color: #00ff88;
                    font-weight: bold;
                }
                .stat-label {
                    color: #cccccc;
                    margin-top: 10px;
                }
                .actions {
                    background: rgba(22, 33, 62, 0.8);
                    border: 1px solid #333366;
                    border-radius: 10px;
                    padding: 20px;
                    text-align: center;
                }
                .action-button {
                    background: #00ff88;
                    color: #000000;
                    border: none;
                    padding: 15px 30px;
                    border-radius: 5px;
                    font-size: 1.2em;
                    font-weight: bold;
                    cursor: pointer;
                    margin: 10px;
                    text-decoration: none;
                    display: inline-block;
                }
                .action-button:hover {
                    background: #00cc6a;
                }
                .status {
                    color: #00ff88;
                    font-weight: bold;
                }
                .phased-out {
                    color: #ff6666;
                    font-style: italic;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>KeyHound Enhanced</h1>
                    <h2>Live Bitcoin Cryptography Platform</h2>
                    <p class="phased-out">Brainwallet: PHASED OUT (No high-value targets found)</p>
                </div>
                
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="status">LIVE</div>
                        <div class="stat-label">System Status</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="uptime">0s</div>
                        <div class="stat-label">Uptime</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="keys-generated">0</div>
                        <div class="stat-label">Keys Generated</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="keys-per-sec">0</div>
                        <div class="stat-label">Keys/Second</div>
                    </div>
                </div>
                
                <div class="actions">
                    <h3>Live Actions</h3>
                    <a href="/api/health" class="action-button">Health Check</a>
                    <a href="/api/stats" class="action-button">System Stats</a>
                    <a href="/api/puzzle-solve/40" class="action-button">Solve 40-bit Puzzle</a>
                    <a href="/api/puzzle-solve/50" class="action-button">Solve 50-bit Puzzle</a>
                    <a href="/api/monitor-challenges" class="action-button" style="background: #ff8800;">Monitor Challenges</a>
                    <br>
                    <p class="phased-out">Brainwallet Testing: PHASED OUT</p>
                </div>
            </div>
            
            <script>
                // Auto-refresh stats every 5 seconds
                setInterval(function() {
                    fetch('/api/stats')
                        .then(response => response.json())
                        .then(data => {
                            document.getElementById('keys-generated').textContent = data.performance.keys_generated || 0;
                            document.getElementById('keys-per-sec').textContent = (data.performance.keys_per_second || 0).toFixed(2);
                            document.getElementById('uptime').textContent = (data.performance.uptime || 0).toFixed(1) + 's';
                        })
                        .catch(error => console.error('Error:', error));
                }, 5000);
            </script>
        </body>
        </html>
        '''
        
        @app.route('/')
        def dashboard():
            return render_template_string(dashboard_html)
        
        @app.route('/api/health')
        def health():
            return jsonify({
                'status': 'healthy',
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
                'keyhound': 'running',
                'version': '1.0.0-streamlined',
                'brainwallet': 'phased_out'
            })
        
        @app.route('/api/stats')
        def stats():
            try:
                perf_stats = keyhound.get_performance_stats()
                return jsonify({
                    'system': system_info,
                    'performance': perf_stats,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception as e:
                return jsonify({'error': str(e)})
        
        @app.route('/api/puzzle-solve/<int:bits>')
        def puzzle_solve(bits):
            try:
                if bits > 60:
                    return jsonify({'error': 'Puzzle too large for demo (max 60 bits)'})
                
                print(f"Starting {bits}-bit puzzle solving...")
                result = keyhound.solve_puzzle(bits=bits, max_attempts=1000000, timeout=60)
                
                if result['solved']:
                    return jsonify({
                        'puzzle_solved': True,
                        'bits': bits,
                        'private_key': result['private_key'],
                        'address': result['address'],
                        'attempts': result['attempts'],
                        'time_taken': result['time_taken'],
                        'keys_per_second': result['keys_per_second'],
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
                else:
                    return jsonify({
                        'puzzle_solved': False,
                        'bits': bits,
                        'attempts': result['attempts'],
                        'keys_per_second': result['keys_per_second'],
                        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                    })
            except Exception as e:
                return jsonify({'error': str(e)})
        
        @app.route('/api/monitor-challenges')
        def monitor_challenges():
            try:
                from core.simple_challenge_monitor import SimpleChallengeMonitor
                
                print("Starting Bitcoin challenge address monitoring...")
                monitor = SimpleChallengeMonitor()
                results = monitor.check_solved_addresses()
                
                addresses_with_balance = [r for r in results if r.get('has_balance', False)]
                total_value = sum(r['current_balance_usd'] for r in addresses_with_balance)
                
                return jsonify({
                    'monitor_status': 'completed',
                    'total_addresses_checked': len(results),
                    'addresses_with_balance': len(addresses_with_balance),
                    'total_value_usd': total_value,
                    'addresses_with_balance_details': addresses_with_balance,
                    'notification_systems_tested': len(addresses_with_balance) > 0,
                    'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
                })
            except Exception as e:
                return jsonify({'error': str(e)})
        
        print("\n" + "=" * 80)
        print("STARTING STREAMLINED LIVE SERVER")
        print("=" * 80)
        print("Web Interface: http://localhost:8080")
        print("Health Check: http://localhost:8080/api/health")
        print("System Stats: http://localhost:8080/api/stats")
        print("Puzzle Solving: http://localhost:8080/api/puzzle-solve/40")
        print("\nFocus: Bitcoin Puzzle Solving & Core Cryptography")
        print("Brainwallet: PHASED OUT (No high-value targets)")
        print("\nPress Ctrl+C to stop the server")
        print("=" * 80)
        
        # Start the Flask server
        app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\nStopping KeyHound Enhanced streamlined server...")
        print("Server stopped.")
    except Exception as e:
        print(f"\n[ERROR] Server failed to start: {e}")
        return 1
    
    return 0

if __name__ == '__main__':
    sys.exit(start_streamlined_live_server())
