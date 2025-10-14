#!/usr/bin/env python3
"""
Advanced Web Interface for KeyHound Enhanced Remote Monitoring

This module provides a comprehensive web interface for remote monitoring,
control, and management of KeyHound Enhanced operations.

Features:
- Real-time dashboard with live metrics and status
- Remote puzzle solving control and monitoring
- Performance metrics visualization with charts
- Result management and download capabilities
- Configuration management through web interface
- System health monitoring and alerting
- User authentication and session management
- RESTful API for external integrations
- WebSocket support for real-time updates
- Mobile-responsive design

Legendary Code Quality Standards:
- Comprehensive error handling and logging
- Type hints for all functions and methods
- Detailed documentation and examples
- Performance optimization and monitoring
- Security best practices implementation
"""

import os
import json
import time
import threading
from typing import Any, Dict, List, Optional, Union
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
import asyncio
import logging

# Web framework imports
try:
    from flask import Flask, render_template, jsonify, request, session, redirect, url_for, send_file
    from flask_socketio import SocketIO, emit, join_room, leave_room
    from werkzeug.security import generate_password_hash, check_password_hash
    FLASK_AVAILABLE = True
except ImportError:
    FLASK_AVAILABLE = False
    Flask = None
    SocketIO = None

# Import KeyHound modules
from ..core.error_handling import KeyHoundLogger, error_handler, performance_monitor
from keyhound_enhanced import KeyHoundEnhanced
from result_persistence import ResultType, StorageBackend
from performance_monitoring import MetricType, AlertLevel

# Configure logging
logger = KeyHoundLogger("WebInterface")


@dataclass
class WebConfig:
    """Web interface configuration."""
    host: str = "0.0.0.0"
    port: int = 5000
    debug: bool = False
    secret_key: str = "keyhound-secret-key-change-in-production"
    auth_enabled: bool = True
    username: str = "admin"
    password_hash: str = ""
    ssl_enabled: bool = False
    ssl_cert_path: str = ""
    ssl_key_path: str = ""


class KeyHoundWebInterface:
    """
    Advanced web interface for KeyHound Enhanced remote monitoring.
    
    Provides comprehensive web-based monitoring, control, and management
    capabilities for Bitcoin cryptographic operations.
    """
    
    def __init__(self, keyhound: KeyHoundEnhanced, config: WebConfig):
        """
        Initialize web interface.
        
        Args:
            keyhound: KeyHoundEnhanced instance
            config: Web interface configuration
        """
        if not FLASK_AVAILABLE:
            raise ImportError("Flask and Flask-SocketIO are required for web interface")
        
        self.keyhound = keyhound
        self.config = config
        self.logger = logger
        
        # Initialize Flask app
        self.app = Flask(__name__)
        self.app.config['SECRET_KEY'] = config.secret_key
        
        # Initialize SocketIO
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")
        
        # Authentication
        self.users = {}
        if config.auth_enabled:
            self._setup_authentication()
        
        # WebSocket rooms
        self.active_sessions = set()
        
        # Setup routes and handlers
        self._setup_routes()
        self._setup_socketio_handlers()
        
        # Background tasks
        self.background_thread = None
        self.running = False
        
        self.logger.info(f"Web interface initialized: {config.host}:{config.port}")
    
    def _setup_authentication(self):
        """Setup user authentication."""
        if not self.config.password_hash:
            # Generate default password hash
            self.config.password_hash = generate_password_hash("keyhound123")
        
        self.users[self.config.username] = self.config.password_hash
        self.logger.info("Authentication enabled")
    
    def _setup_routes(self):
        """Setup Flask routes."""
        
        @self.app.route('/')
        def index():
            """Main dashboard page."""
            if self.config.auth_enabled and 'username' not in session:
                return redirect(url_for('login'))
            return render_template('dashboard.html')
        
        @self.app.route('/login', methods=['GET', 'POST'])
        def login():
            """Login page."""
            if not self.config.auth_enabled:
                session['username'] = 'anonymous'
                return redirect(url_for('index'))
            
            if request.method == 'POST':
                username = request.form['username']
                password = request.form['password']
                
                if username in self.users and check_password_hash(self.users[username], password):
                    session['username'] = username
                    return redirect(url_for('index'))
                else:
                    return render_template('login.html', error='Invalid credentials')
            
            return render_template('login.html')
        
        @self.app.route('/logout')
        def logout():
            """Logout and clear session."""
            session.pop('username', None)
            return redirect(url_for('login'))
        
        @self.app.route('/api/status')
        def api_status():
            """Get system status."""
            try:
                status = self._get_system_status()
                return jsonify(status)
            except Exception as e:
                self.logger.error(f"Status API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/metrics')
        def api_metrics():
            """Get performance metrics."""
            try:
                metrics = self._get_performance_metrics()
                return jsonify(metrics)
            except Exception as e:
                self.logger.error(f"Metrics API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/results')
        def api_results():
            """Get stored results."""
            try:
                limit = request.args.get('limit', 100, type=int)
                result_type = request.args.get('type')
                
                results = self._get_stored_results(limit, result_type)
                return jsonify(results)
            except Exception as e:
                self.logger.error(f"Results API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/results/<result_id>')
        def api_get_result(result_id):
            """Get specific result."""
            try:
                result = self._get_result_by_id(result_id)
                if result:
                    return jsonify(result)
                else:
                    return jsonify({"error": "Result not found"}), 404
            except Exception as e:
                self.logger.error(f"Get result API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/results/<result_id>/download')
        def api_download_result(result_id):
            """Download result as file."""
            try:
                result = self._get_result_by_id(result_id)
                if result:
                    filename = f"keyhound_result_{result_id}.json"
                    return send_file(
                        json.dumps(result, indent=2),
                        as_attachment=True,
                        download_name=filename,
                        mimetype='application/json'
                    )
                else:
                    return jsonify({"error": "Result not found"}), 404
            except Exception as e:
                self.logger.error(f"Download result API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/puzzle/solve', methods=['POST'])
        def api_solve_puzzle():
            """Start puzzle solving operation."""
            try:
                data = request.get_json()
                puzzle_id = data.get('puzzle_id')
                max_keys = data.get('max_keys', 1000000)
                use_streaming = data.get('use_streaming', True)
                
                if not puzzle_id:
                    return jsonify({"error": "puzzle_id is required"}), 400
                
                # Start puzzle solving in background
                self._start_puzzle_solving(puzzle_id, max_keys, use_streaming)
                
                return jsonify({"message": f"Puzzle solving started for puzzle {puzzle_id}"})
            except Exception as e:
                self.logger.error(f"Solve puzzle API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/brainwallet/test', methods=['POST'])
        def api_brainwallet_test():
            """Start brainwallet security test."""
            try:
                data = request.get_json()
                target_address = data.get('target_address')
                max_patterns = data.get('max_patterns', 10000)
                
                if not target_address:
                    return jsonify({"error": "target_address is required"}), 400
                
                # Start brainwallet test in background
                self._start_brainwallet_test(target_address, max_patterns)
                
                return jsonify({"message": f"Brainwallet test started for {target_address}"})
            except Exception as e:
                self.logger.error(f"Brainwallet test API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/benchmark', methods=['POST'])
        def api_benchmark():
            """Start performance benchmark."""
            try:
                data = request.get_json()
                duration = data.get('duration', 60)
                use_gpu = data.get('use_gpu', False)
                
                # Start benchmark in background
                self._start_benchmark(duration, use_gpu)
                
                return jsonify({"message": f"Benchmark started for {duration} seconds"})
            except Exception as e:
                self.logger.error(f"Benchmark API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/config')
        def api_get_config():
            """Get current configuration."""
            try:
                if not self.keyhound.config_manager:
                    return jsonify({"error": "Configuration manager not available"}), 500
                
                config = self.keyhound.config_manager.get_all()
                return jsonify(config)
            except Exception as e:
                self.logger.error(f"Get config API error: {e}")
                return jsonify({"error": str(e)}), 500
        
        @self.app.route('/api/config', methods=['POST'])
        def api_update_config():
            """Update configuration."""
            try:
                if not self.keyhound.config_manager:
                    return jsonify({"error": "Configuration manager not available"}), 500
                
                data = request.get_json()
                
                for key, value in data.items():
                    self.keyhound.config_manager.set(key, value)
                
                return jsonify({"message": "Configuration updated successfully"})
            except Exception as e:
                self.logger.error(f"Update config API error: {e}")
                return jsonify({"error": str(e)}), 500
    
    def _setup_socketio_handlers(self):
        """Setup SocketIO event handlers."""
        
        @self.socketio.on('connect')
        def handle_connect():
            """Handle client connection."""
            session_id = request.sid
            self.active_sessions.add(session_id)
            
            # Send initial status
            status = self._get_system_status()
            emit('status_update', status)
            
            self.logger.info(f"Client connected: {session_id}")
        
        @self.socketio.on('disconnect')
        def handle_disconnect():
            """Handle client disconnection."""
            session_id = request.sid
            self.active_sessions.discard(session_id)
            
            self.logger.info(f"Client disconnected: {session_id}")
        
        @self.socketio.on('join_room')
        def handle_join_room(data):
            """Handle room joining."""
            room = data.get('room', 'default')
            join_room(room)
            
            self.logger.info(f"Client {request.sid} joined room: {room}")
        
        @self.socketio.on('leave_room')
        def handle_leave_room(data):
            """Handle room leaving."""
            room = data.get('room', 'default')
            leave_room(room)
            
            self.logger.info(f"Client {request.sid} left room: {room}")
    
    def _get_system_status(self) -> Dict[str, Any]:
        """Get comprehensive system status."""
        try:
            status = {
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "keyhound": {
                    "version": "0.7.0",
                    "status": "running",
                    "uptime": time.time() - (self.keyhound.start_time or time.time()),
                    "found_keys": len(self.keyhound.found_keys),
                    "gpu_enabled": self.keyhound.use_gpu,
                    "thread_count": self.keyhound.num_threads
                },
                "systems": {}
            }
            
            # Memory optimizer status
            if self.keyhound.memory_optimizer:
                memory_stats = self.keyhound.memory_optimizer.get_memory_stats()
                status["systems"]["memory_optimizer"] = {
                    "enabled": True,
                    "stats": memory_stats
                }
            else:
                status["systems"]["memory_optimizer"] = {"enabled": False}
            
            # Performance monitor status
            if self.keyhound.performance_monitor:
                perf_stats = self.keyhound.performance_monitor.get_performance_statistics()
                status["systems"]["performance_monitor"] = {
                    "enabled": True,
                    "stats": perf_stats
                }
            else:
                status["systems"]["performance_monitor"] = {"enabled": False}
            
            # Result persistence status
            if self.keyhound.result_persistence:
                storage_stats = self.keyhound.result_persistence.get_storage_statistics()
                status["systems"]["result_persistence"] = {
                    "enabled": True,
                    "stats": storage_stats
                }
            else:
                status["systems"]["result_persistence"] = {"enabled": False}
            
            # Configuration manager status
            if self.keyhound.config_manager:
                config_env = self.keyhound.config_manager.get("keyhound.environment", "unknown")
                status["systems"]["configuration_manager"] = {
                    "enabled": True,
                    "environment": config_env
                }
            else:
                status["systems"]["configuration_manager"] = {"enabled": False}
            
            return status
            
        except Exception as e:
            self.logger.error(f"Error getting system status: {e}")
            return {"error": str(e)}
    
    def _get_performance_metrics(self) -> Dict[str, Any]:
        """Get performance metrics."""
        try:
            if not self.keyhound.performance_monitor:
                return {"error": "Performance monitor not available"}
            
            metrics = self.keyhound.performance_monitor.get_current_metrics()
            system_metrics = self.keyhound.performance_monitor.get_system_metrics_history(limit=10)
            active_alerts = self.keyhound.performance_monitor.get_active_alerts()
            
            return {
                "current_metrics": {name: asdict(metric) for name, metric in metrics.items()},
                "system_metrics": [asdict(metric) for metric in system_metrics],
                "active_alerts": [asdict(alert) for alert in active_alerts],
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error getting performance metrics: {e}")
            return {"error": str(e)}
    
    def _get_stored_results(self, limit: int = 100, result_type: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get stored results."""
        try:
            if not self.keyhound.result_persistence:
                return {"error": "Result persistence not available"}
            
            # Convert result type string to enum if provided
            result_type_enum = None
            if result_type:
                try:
                    result_type_enum = ResultType(result_type)
                except ValueError:
                    return {"error": f"Invalid result type: {result_type}"}
            
            results = self.keyhound.result_persistence.list_results(
                result_type=result_type_enum,
                limit=limit
            )
            
            return [asdict(result) for result in results]
            
        except Exception as e:
            self.logger.error(f"Error getting stored results: {e}")
            return {"error": str(e)}
    
    def _get_result_by_id(self, result_id: str) -> Optional[Dict[str, Any]]:
        """Get specific result by ID."""
        try:
            if not self.keyhound.result_persistence:
                return None
            
            result = self.keyhound.result_persistence.load_result(result_id)
            return result
            
        except Exception as e:
            self.logger.error(f"Error getting result {result_id}: {e}")
            return None
    
    def _start_puzzle_solving(self, puzzle_id: int, max_keys: int, use_streaming: bool):
        """Start puzzle solving in background thread."""
        def solve_puzzle():
            try:
                self.socketio.emit('operation_started', {
                    'operation': 'puzzle_solving',
                    'puzzle_id': puzzle_id,
                    'max_keys': max_keys
                })
                
                if use_streaming:
                    result = self.keyhound.solve_bitcoin_puzzle_streaming(puzzle_id, max_keys)
                else:
                    result = self.keyhound.solve_bitcoin_puzzle(puzzle_id)
                
                self.socketio.emit('operation_completed', {
                    'operation': 'puzzle_solving',
                    'puzzle_id': puzzle_id,
                    'success': result is not None,
                    'result': result
                })
                
            except Exception as e:
                self.logger.error(f"Puzzle solving error: {e}")
                self.socketio.emit('operation_error', {
                    'operation': 'puzzle_solving',
                    'puzzle_id': puzzle_id,
                    'error': str(e)
                })
        
        thread = threading.Thread(target=solve_puzzle, daemon=True)
        thread.start()
    
    def _start_brainwallet_test(self, target_address: str, max_patterns: int):
        """Start brainwallet test in background thread."""
        def test_brainwallet():
            try:
                self.socketio.emit('operation_started', {
                    'operation': 'brainwallet_test',
                    'target_address': target_address,
                    'max_patterns': max_patterns
                })
                
                result = self.keyhound.brainwallet_security_test(
                    target_address,
                    max_patterns=max_patterns
                )
                
                self.socketio.emit('operation_completed', {
                    'operation': 'brainwallet_test',
                    'target_address': target_address,
                    'result': result
                })
                
            except Exception as e:
                self.logger.error(f"Brainwallet test error: {e}")
                self.socketio.emit('operation_error', {
                    'operation': 'brainwallet_test',
                    'target_address': target_address,
                    'error': str(e)
                })
        
        thread = threading.Thread(target=test_brainwallet, daemon=True)
        thread.start()
    
    def _start_benchmark(self, duration: int, use_gpu: bool):
        """Start benchmark in background thread."""
        def run_benchmark():
            try:
                self.socketio.emit('operation_started', {
                    'operation': 'benchmark',
                    'duration': duration,
                    'use_gpu': use_gpu
                })
                
                result = self.keyhound.performance_benchmark(
                    test_duration=duration,
                    use_gpu=use_gpu
                )
                
                self.socketio.emit('operation_completed', {
                    'operation': 'benchmark',
                    'result': result
                })
                
            except Exception as e:
                self.logger.error(f"Benchmark error: {e}")
                self.socketio.emit('operation_error', {
                    'operation': 'benchmark',
                    'error': str(e)
                })
        
        thread = threading.Thread(target=run_benchmark, daemon=True)
        thread.start()
    
    def _start_background_updates(self):
        """Start background updates thread."""
        def update_clients():
            while self.running:
                try:
                    if self.active_sessions:
                        # Send status update
                        status = self._get_system_status()
                        self.socketio.emit('status_update', status)
                        
                        # Send metrics update
                        metrics = self._get_performance_metrics()
                        self.socketio.emit('metrics_update', metrics)
                    
                    time.sleep(5)  # Update every 5 seconds
                    
                except Exception as e:
                    self.logger.error(f"Background update error: {e}")
                    time.sleep(10)
        
        self.background_thread = threading.Thread(target=update_clients, daemon=True)
        self.background_thread.start()
    
    def start(self):
        """Start web interface."""
        try:
            self.running = True
            self._start_background_updates()
            
            # Create templates directory if it doesn't exist
            templates_dir = Path(__file__).parent / "templates"
            templates_dir.mkdir(exist_ok=True)
            
            # Create static directory if it doesn't exist
            static_dir = Path(__file__).parent / "static"
            static_dir.mkdir(exist_ok=True)
            
            self.logger.info(f"Starting web interface on {self.config.host}:{self.config.port}")
            
            if self.config.ssl_enabled:
                self.socketio.run(
                    self.app,
                    host=self.config.host,
                    port=self.config.port,
                    debug=self.config.debug,
                    ssl_context=(self.config.ssl_cert_path, self.config.ssl_key_path)
                )
            else:
                self.socketio.run(
                    self.app,
                    host=self.config.host,
                    port=self.config.port,
                    debug=self.config.debug
                )
                
        except Exception as e:
            self.logger.error(f"Web interface start error: {e}")
            raise
    
    def stop(self):
        """Stop web interface."""
        self.running = False
        self.logger.info("Web interface stopped")


def create_web_interface(keyhound: KeyHoundEnhanced, config: Optional[WebConfig] = None) -> KeyHoundWebInterface:
    """Create web interface instance."""
    if config is None:
        config = WebConfig()
    
    return KeyHoundWebInterface(keyhound, config)


# Example usage and testing
if __name__ == "__main__":
    # Test web interface
    print("Testing KeyHound Web Interface...")
    
    try:
        # Create KeyHound instance
        keyhound = KeyHoundEnhanced(use_gpu=False, verbose=True)
        
        # Create web interface
        web_config = WebConfig(
            host="127.0.0.1",
            port=5000,
            debug=True,
            auth_enabled=False  # Disable auth for testing
        )
        
        web_interface = create_web_interface(keyhound, web_config)
        
        print("Web interface created successfully")
        print(f"Access the interface at: http://{web_config.host}:{web_config.port}")
        print("Press Ctrl+C to stop")
        
        # Start web interface
        web_interface.start()
        
    except Exception as e:
        print(f"Web interface test failed: {e}")

