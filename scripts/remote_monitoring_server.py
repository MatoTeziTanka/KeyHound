#!/usr/bin/env python3
"""
KeyHound Enhanced - Remote Monitoring Server
Provides remote access to KeyHound monitoring dashboard.
"""

import os
import sys
import time
import json
import threading
from flask import Flask, render_template_string, jsonify, request
from flask_socketio import SocketIO, emit
import requests

# Add KeyHound root to sys.path
sys.path.insert(0, str(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

app = Flask(__name__)
app.config['SECRET_KEY'] = 'keyhound_remote_monitoring_2025'
socketio = SocketIO(app, cors_allowed_origins="*")

# Dashboard HTML template
DASHBOARD_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>KeyHound Enhanced - Remote Monitoring</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/socket.io/4.0.1/socket.io.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; min-height: 100vh;
        }
        .container { max-width: 1200px; margin: 0 auto; padding: 20px; }
        .header { text-align: center; margin-bottom: 30px; }
        .header h1 { font-size: 2.5em; margin-bottom: 10px; }
        .status-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 20px; }
        .status-card { 
            background: rgba(255,255,255,0.1); 
            border-radius: 15px; 
            padding: 25px; 
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.2);
        }
        .status-card h3 { margin-bottom: 15px; color: #ffd700; }
        .metric { display: flex; justify-content: space-between; margin: 10px 0; }
        .metric-value { font-weight: bold; color: #00ff88; }
        .actions { margin-top: 30px; text-align: center; }
        .action-button {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            color: white;
            padding: 12px 25px;
            text-decoration: none;
            border-radius: 25px;
            margin: 5px;
            transition: transform 0.3s;
        }
        .action-button:hover { transform: translateY(-2px); }
        .chart-container { margin-top: 20px; height: 200px; }
        .connection-status { 
            position: fixed; 
            top: 20px; 
            right: 20px; 
            padding: 10px 20px; 
            border-radius: 20px;
            background: rgba(0,255,136,0.2);
            border: 1px solid #00ff88;
        }
        .disconnected { background: rgba(255,0,0,0.2); border-color: #ff0000; }
    </style>
</head>
<body>
    <div class="connection-status" id="connectionStatus">
        Connected
    </div>
    
    <div class="container">
        <div class="header">
            <h1>🚀 KeyHound Enhanced</h1>
            <p>Remote Bitcoin Puzzle Solving & Monitoring Dashboard</p>
            <p><strong>Remote Access Enabled</strong> - Accessible from anywhere!</p>
        </div>
        
        <div class="status-grid">
            <div class="status-card">
                <h3>🎯 Puzzle Solving Status</h3>
                <div class="metric">
                    <span>Current Puzzle:</span>
                    <span class="metric-value" id="currentPuzzle">Not Running</span>
                </div>
                <div class="metric">
                    <span>Keys/Second:</span>
                    <span class="metric-value" id="keysPerSecond">0</span>
                </div>
                <div class="metric">
                    <span>Total Attempts:</span>
                    <span class="metric-value" id="totalAttempts">0</span>
                </div>
                <div class="metric">
                    <span>GPU Acceleration:</span>
                    <span class="metric-value" id="gpuStatus">Unknown</span>
                </div>
            </div>
            
            <div class="status-card">
                <h3>💰 Found Addresses</h3>
                <div class="metric">
                    <span>Addresses Monitored:</span>
                    <span class="metric-value" id="monitoredAddresses">0</span>
                </div>
                <div class="metric">
                    <span>Addresses with Balance:</span>
                    <span class="metric-value" id="addressesWithBalance">0</span>
                </div>
                <div class="metric">
                    <span>Total Value Found:</span>
                    <span class="metric-value" id="totalValue">$0.00</span>
                </div>
                <div class="metric">
                    <span>Last Check:</span>
                    <span class="metric-value" id="lastCheck">Never</span>
                </div>
            </div>
            
            <div class="status-card">
                <h3>📊 System Performance</h3>
                <div class="metric">
                    <span>CPU Usage:</span>
                    <span class="metric-value" id="cpuUsage">0%</span>
                </div>
                <div class="metric">
                    <span>Memory Usage:</span>
                    <span class="metric-value" id="memoryUsage">0%</span>
                </div>
                <div class="metric">
                    <span>Uptime:</span>
                    <span class="metric-value" id="uptime">0s</span>
                </div>
                <div class="metric">
                    <span>Status:</span>
                    <span class="metric-value" id="systemStatus">Online</span>
                </div>
            </div>
            
            <div class="status-card">
                <h3>📈 Performance Chart</h3>
                <div class="chart-container">
                    <canvas id="performanceChart"></canvas>
                </div>
            </div>
        </div>
        
        <div class="actions">
            <h3>Remote Actions</h3>
            <a href="/api/health" class="action-button" target="_blank">Health Check</a>
            <a href="/api/stats" class="action-button" target="_blank">System Stats</a>
            <a href="/api/puzzle-solve/40" class="action-button" target="_blank">Solve 40-bit Puzzle</a>
            <a href="/api/monitor-challenges" class="action-button" target="_blank">Monitor Challenges</a>
            <a href="/api/real-puzzle-monitor" class="action-button" target="_blank">Real Puzzle Monitor</a>
        </div>
    </div>

    <script>
        // WebSocket connection
        const socket = io();
        let performanceChart;
        let chartData = [];
        
        // Connection status
        socket.on('connect', function() {
            document.getElementById('connectionStatus').textContent = 'Connected';
            document.getElementById('connectionStatus').className = 'connection-status';
        });
        
        socket.on('disconnect', function() {
            document.getElementById('connectionStatus').textContent = 'Disconnected';
            document.getElementById('connectionStatus').className = 'connection-status disconnected';
        });
        
        // Real-time updates
        socket.on('status_update', function(data) {
            document.getElementById('currentPuzzle').textContent = data.current_puzzle || 'Not Running';
            document.getElementById('keysPerSecond').textContent = data.keys_per_second || '0';
            document.getElementById('totalAttempts').textContent = data.total_attempts || '0';
            document.getElementById('gpuStatus').textContent = data.gpu_status || 'Unknown';
            document.getElementById('cpuUsage').textContent = data.cpu_usage || '0%';
            document.getElementById('memoryUsage').textContent = data.memory_usage || '0%';
            document.getElementById('uptime').textContent = data.uptime || '0s';
            
            // Update chart
            chartData.push({
                time: new Date().toLocaleTimeString(),
                keysPerSecond: parseInt(data.keys_per_second) || 0
            });
            if (chartData.length > 20) chartData.shift();
            updateChart();
        });
        
        socket.on('monitor_update', function(data) {
            document.getElementById('monitoredAddresses').textContent = data.total_addresses || '0';
            document.getElementById('addressesWithBalance').textContent = data.addresses_with_balance || '0';
            document.getElementById('totalValue').textContent = data.total_value || '$0.00';
            document.getElementById('lastCheck').textContent = data.last_check || 'Never';
        });
        
        // Initialize chart
        function initChart() {
            const ctx = document.getElementById('performanceChart').getContext('2d');
            performanceChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: [],
                    datasets: [{
                        label: 'Keys/Second',
                        data: [],
                        borderColor: '#00ff88',
                        backgroundColor: 'rgba(0,255,136,0.1)',
                        tension: 0.4
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            labels: { color: 'white' }
                        }
                    },
                    scales: {
                        x: { ticks: { color: 'white' } },
                        y: { ticks: { color: 'white' } }
                    }
                }
            });
        }
        
        function updateChart() {
            if (!performanceChart) return;
            performanceChart.data.labels = chartData.map(d => d.time);
            performanceChart.data.datasets[0].data = chartData.map(d => d.keysPerSecond);
            performanceChart.update();
        }
        
        // Initialize
        initChart();
        
        // Request initial data
        fetch('/api/stats')
            .then(response => response.json())
            .then(data => {
                document.getElementById('currentPuzzle').textContent = data.current_puzzle || 'Not Running';
                document.getElementById('keysPerSecond').textContent = data.keys_per_second || '0';
                document.getElementById('gpuStatus').textContent = data.gpu_status || 'Unknown';
            });
    </script>
</body>
</html>
"""

@app.route('/')
def dashboard():
    """Main dashboard page."""
    return render_template_string(DASHBOARD_TEMPLATE)

@app.route('/api/health')
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        'uptime': time.time() - start_time,
        'remote_access': True
    })

@app.route('/api/stats')
def get_stats():
    """Get system statistics."""
    try:
        # Get system info
        import psutil
        cpu_percent = psutil.cpu_percent()
        memory = psutil.virtual_memory()
        
        return jsonify({
            'current_puzzle': 'Not Running',
            'keys_per_second': 0,
            'total_attempts': 0,
            'gpu_status': 'Unknown',
            'cpu_usage': f'{cpu_percent}%',
            'memory_usage': f'{memory.percent}%',
            'uptime': f'{time.time() - start_time:.0f}s',
            'system_status': 'Online',
            'remote_access': True,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/puzzle-solve/<int:bits>')
def solve_puzzle(bits):
    """Solve a Bitcoin puzzle."""
    try:
        # Import KeyHound
        from core.gpu_enabled_keyhound import GPUEnabledKeyHound
        
        # Initialize with auto-detection
        keyhound = GPUEnabledKeyHound(use_gpu=True, gpu_framework="cuda")
        
        # Solve puzzle
        result = keyhound.solve_puzzle(bits, max_attempts=100000, timeout=60)
        
        return jsonify({
            'puzzle_bits': bits,
            'result': result,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/monitor-challenges')
def monitor_challenges():
    """Monitor Bitcoin challenge addresses."""
    try:
        from core.simple_challenge_monitor import SimpleChallengeMonitor
        
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
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/real-puzzle-monitor')
def real_puzzle_monitor():
    """Monitor real Bitcoin puzzle addresses."""
    try:
        from core.real_bitcoin_puzzle_monitor import RealBitcoinPuzzleMonitor
        
        monitor = RealBitcoinPuzzleMonitor()
        results = monitor.check_solved_addresses()
        
        addresses_with_balance = [r for r in results if r.get('has_balance', False)]
        total_value = sum(r['current_balance_usd'] for r in addresses_with_balance)
        
        return jsonify({
            'monitor_status': 'completed',
            'total_addresses_checked': len(results),
            'addresses_with_balance': len(addresses_with_balance),
            'addresses_with_private_keys': len([r for r in results if r.get('private_key')]),
            'total_value_usd': total_value,
            'addresses_with_balance_details': addresses_with_balance,
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        })
    except Exception as e:
        return jsonify({'error': str(e)})

# WebSocket events
@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    emit('status', {'data': 'Connected to KeyHound Remote Monitoring'})

@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    print('Client disconnected')

def start_monitoring():
    """Start background monitoring."""
    while True:
        try:
            # Get current stats
            stats = get_stats().get_json()
            monitor_data = real_puzzle_monitor().get_json()
            
            # Emit updates
            socketio.emit('status_update', stats)
            socketio.emit('monitor_update', monitor_data)
            
            time.sleep(10)  # Update every 10 seconds
        except Exception as e:
            print(f"Monitoring error: {e}")
            time.sleep(30)

if __name__ == '__main__':
    start_time = time.time()
    
    print("=" * 80)
    print("KeyHound Enhanced - Remote Monitoring Server")
    print("=" * 80)
    print("Starting remote monitoring server...")
    print("Dashboard will be available at:")
    print("  Local: http://localhost:5000")
    print("  Remote: http://YOUR_IP:5000")
    print("=" * 80)
    
    # Start background monitoring
    monitoring_thread = threading.Thread(target=start_monitoring, daemon=True)
    monitoring_thread.start()
    
    # Start Flask-SocketIO server
    socketio.run(app, host='0.0.0.0', port=5000, debug=False)
