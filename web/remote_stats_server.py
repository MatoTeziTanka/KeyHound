"""
KeyHound Enhanced - Remote Statistics Server
A sleek, futuristic real-time statistics dashboard accessible from anywhere in the world.
"""

import asyncio
import json
import time
import os
import sys
import psutil
import platform
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Any, Optional
import logging

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.simple_keyhound import SimpleKeyHound
    from core.bitcoin_cryptography import BitcoinCryptography
    from core.performance_monitoring import PerformanceMonitor
    KEYHOUND_AVAILABLE = True
except ImportError:
    KEYHOUND_AVAILABLE = False

# Web framework imports
try:
    from flask import Flask, render_template, jsonify, request
    from flask_socketio import SocketIO, emit
    import threading
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RemoteStatsServer:
    """
    Remote statistics server for KeyHound Enhanced.
    Provides real-time monitoring dashboard accessible from anywhere.
    """
    
    def __init__(self, host='0.0.0.0', port=8080, update_interval=10):
        self.host = host
        self.port = port
        self.update_interval = update_interval
        self.start_time = time.time()
        self.connected_clients = 0
        self.total_requests = 0
        
        # Initialize KeyHound components if available
        self.keyhound = None
        self.performance_monitor = None
        
        if KEYHOUND_AVAILABLE:
            try:
                self.keyhound = SimpleKeyHound(verbose=False)
                logger.info("KeyHound components initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize KeyHound: {e}")
        
        # Initialize Flask app
        if WEB_AVAILABLE:
            self.app = Flask(__name__, 
                           template_folder='../templates',
                           static_folder='../static')
            self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'keyhound-remote-stats-2024')
            self.socketio = SocketIO(self.app, cors_allowed_origins="*")
            
            # Register routes and socket events
            self._register_routes()
            self._register_socket_events()
        else:
            logger.error("Web dependencies not available. Install Flask and Flask-SocketIO")
            raise ImportError("Web dependencies required for remote stats server")
    
    def _register_routes(self):
        """Register Flask routes."""
        
        @self.app.route('/')
        def dashboard():
            """Main dashboard page."""
            return render_template('remote_stats_dashboard.html')
        
        @self.app.route('/api/stats')
        def api_stats():
            """API endpoint for statistics."""
            self.total_requests += 1
            return jsonify(self.get_current_stats())
        
        @self.app.route('/api/health')
        def api_health():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'uptime': time.time() - self.start_time
            })
    
    def _register_socket_events(self):
        """Register SocketIO events."""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            self.connected_clients += 1
            logger.info(f"Client connected. Total clients: {self.connected_clients}")
            emit('connected', {'message': 'Connected to KeyHound Remote Stats'})
            emit('stats_update', self.get_current_stats())
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            self.connected_clients = max(0, self.connected_clients - 1)
            logger.info(f"Client disconnected. Total clients: {self.connected_clients}")
        
        @self.socketio.on('request_stats')
        def handle_stats_request():
            """Handle stats request from client."""
            emit('stats_update', self.get_current_stats())
    
    def get_current_stats(self) -> Dict[str, Any]:
        """Get current statistics for display."""
        current_time = datetime.now()
        uptime_seconds = time.time() - self.start_time
        
        # System information
        system_info = {
            'platform': platform.platform(),
            'cpu_count': os.cpu_count(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent if os.name != 'nt' else psutil.disk_usage('C:\\').percent
        }
        
        # KeyHound specific stats
        keyhound_stats = {}
        if self.keyhound:
            try:
                perf_stats = self.keyhound.get_performance_stats()
                keyhound_stats = {
                    'keys_generated': self.keyhound.keys_generated,
                    'puzzle_solved': self.keyhound.puzzle_solved,
                    'uptime_seconds': perf_stats['uptime_seconds'],
                    'keys_per_second': perf_stats['overall_rate_keys_per_second'],
                    'status': 'active'
                }
            except Exception as e:
                keyhound_stats = {
                    'status': 'error',
                    'error': str(e)
                }
        else:
            keyhound_stats = {
                'status': 'unavailable',
                'message': 'KeyHound components not available'
            }
        
        # Server stats
        server_stats = {
            'uptime_seconds': uptime_seconds,
            'connected_clients': self.connected_clients,
            'total_requests': self.total_requests,
            'update_interval': self.update_interval,
            'last_update': current_time.isoformat()
        }
        
        return {
            'timestamp': current_time.isoformat(),
            'system': system_info,
            'keyhound': keyhound_stats,
            'server': server_stats,
            'connection_status': 'connected' if self.connected_clients > 0 else 'waiting'
        }
    
    def start_broadcast_loop(self):
        """Start the broadcast loop for real-time updates."""
        def broadcast_loop():
            while True:
                try:
                    if self.connected_clients > 0:
                        stats = self.get_current_stats()
                        self.socketio.emit('stats_update', stats)
                        logger.debug(f"Broadcasted stats to {self.connected_clients} clients")
                    
                    time.sleep(self.update_interval)
                except Exception as e:
                    logger.error(f"Error in broadcast loop: {e}")
                    time.sleep(self.update_interval)
        
        # Start broadcast loop in separate thread
        broadcast_thread = threading.Thread(target=broadcast_loop, daemon=True)
        broadcast_thread.start()
        logger.info(f"Started broadcast loop with {self.update_interval}s interval")
    
    def run(self, debug=False):
        """Run the remote stats server."""
        logger.info(f"Starting KeyHound Remote Stats Server on {self.host}:{self.port}")
        logger.info(f"Update interval: {self.update_interval} seconds")
        
        # Start broadcast loop
        self.start_broadcast_loop()
        
        # Run Flask-SocketIO app
        try:
            self.socketio.run(
                self.app,
                host=self.host,
                port=self.port,
                debug=debug,
                allow_unsafe_werkzeug=True  # For development only
            )
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='KeyHound Remote Statistics Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to (default: 8080)')
    parser.add_argument('--update-interval', type=int, default=10, help='Update interval in seconds (default: 10)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    if not WEB_AVAILABLE:
        print("Error: Web dependencies not available.")
        print("Install with: pip install flask flask-socketio")
        sys.exit(1)
    
    if not KEYHOUND_AVAILABLE:
        print("Warning: KeyHound components not available. Some features will be limited.")
    
    try:
        server = RemoteStatsServer(
            host=args.host,
            port=args.port,
            update_interval=args.update_interval
        )
        server.run(debug=args.debug)
    except Exception as e:
        logger.error(f"Failed to start server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
