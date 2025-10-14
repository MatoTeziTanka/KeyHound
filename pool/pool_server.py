"""
KeyHound Enhanced - Pool Server API
REST API server for the distributed Bitcoin puzzle solving pool.
"""

import os
import sys
import time
import json
import threading
from pathlib import Path
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
import logging

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from flask import Flask, request, jsonify
    from flask_cors import CORS
    WEB_AVAILABLE = True
except ImportError:
    WEB_AVAILABLE = False

try:
    from pool.pool_coordinator import DistributedPoolCoordinator
    from pool.hardware_scorer import HardwarePerformanceScorer
    POOL_AVAILABLE = True
except ImportError:
    POOL_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class PoolServerAPI:
    """REST API server for the distributed pool."""
    
    def __init__(self, pool_owner_id: str, pool_owner_public_key: str, host='0.0.0.0', port=8080):
        self.host = host
        self.port = port
        
        # Initialize pool coordinator
        self.coordinator = DistributedPoolCoordinator(pool_owner_id, pool_owner_public_key)
        
        # Initialize Flask app
        if WEB_AVAILABLE:
            self.app = Flask(__name__)
            CORS(self.app)  # Enable CORS for cross-origin requests
            self.app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'keyhound-pool-2024')
            
            # Register API routes
            self._register_routes()
            
            # Start background tasks
            self._start_background_tasks()
        else:
            raise ImportError("Web dependencies required for pool server")
    
    def _register_routes(self):
        """Register API routes."""
        
        @self.app.route('/api/health', methods=['GET'])
        def health_check():
            """Health check endpoint."""
            return jsonify({
                'status': 'healthy',
                'timestamp': datetime.now().isoformat(),
                'pool_active': True
            })
        
        @self.app.route('/api/register', methods=['POST'])
        def register_participant():
            """Register a new participant."""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': 'No data provided'}), 400
                
                user_id = data.get('user_id')
                device_name = data.get('device_name')
                hardware_specs = data.get('hardware_specs', {})
                performance_tests = data.get('performance_tests', [])
                hardware_score = data.get('hardware_score', {})
                
                if not user_id or not device_name:
                    return jsonify({'success': False, 'error': 'user_id and device_name required'}), 400
                
                # Register participant
                result = self.coordinator.register_participant(user_id, device_name, "dummy_public_key")
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Registration error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/request_work', methods=['POST'])
        def request_work():
            """Request work assignment."""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': 'No data provided'}), 400
                
                user_id = data.get('user_id')
                device_id = data.get('device_id')
                capabilities = data.get('capabilities', {})
                
                if not user_id or not device_id:
                    return jsonify({'success': False, 'error': 'user_id and device_id required'}), 400
                
                # Check if participant exists
                if device_id not in self.coordinator.participants:
                    return jsonify({'success': False, 'error': 'Participant not found'}), 404
                
                # Assign work (simplified - in production, this would be more sophisticated)
                puzzle_bits = capabilities.get('max_puzzle_bits', 40)
                work_result = self.coordinator.assign_work(f"puzzle_{puzzle_bits}", puzzle_bits)
                
                if work_result.get('success'):
                    # Get work assignment for this device
                    participant = self.coordinator.participants[device_id]
                    active_work = self.coordinator.active_work.get(device_id)
                    
                    if active_work:
                        work_assignment = {
                            'puzzle_id': active_work.puzzle_id,
                            'puzzle_bits': active_work.puzzle_bits,
                            'work_range_start': active_work.work_range_start,
                            'work_range_end': active_work.work_range_end,
                            'deadline': active_work.deadline
                        }
                        
                        return jsonify({
                            'success': True,
                            'work_assignment': work_assignment,
                            'reward_percentage': participant.current_reward_percentage
                        })
                    else:
                        return jsonify({'success': False, 'message': 'No work assignment available'})
                else:
                    return jsonify(work_result)
                
            except Exception as e:
                logger.error(f"Work request error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/submit_key', methods=['POST'])
        def submit_key():
            """Submit a found private key."""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': 'No data provided'}), 400
                
                user_id = data.get('user_id')
                device_id = data.get('device_id')
                puzzle_id = data.get('puzzle_id')
                private_key = data.get('private_key')
                public_key = data.get('public_key')
                address = data.get('address')
                
                if not all([user_id, device_id, puzzle_id, private_key, public_key, address]):
                    return jsonify({'success': False, 'error': 'Missing required fields'}), 400
                
                # Submit found key
                result = self.coordinator.submit_found_key(
                    device_id, puzzle_id, private_key, public_key, address)
                
                return jsonify(result)
                
            except Exception as e:
                logger.error(f"Key submission error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/heartbeat', methods=['POST'])
        def heartbeat():
            """Receive heartbeat from participant."""
            try:
                data = request.get_json()
                if not data:
                    return jsonify({'success': False, 'error': 'No data provided'}), 400
                
                user_id = data.get('user_id')
                device_id = data.get('device_id')
                puzzle_id = data.get('puzzle_id')
                keys_checked = data.get('keys_checked', 0)
                
                if not user_id or not device_id:
                    return jsonify({'success': False, 'error': 'user_id and device_id required'}), 400
                
                # Update participant activity
                if device_id in self.coordinator.participants:
                    participant = self.coordinator.participants[device_id]
                    participant.last_active = datetime.now().isoformat()
                
                return jsonify({'success': True, 'timestamp': datetime.now().isoformat()})
                
            except Exception as e:
                logger.error(f"Heartbeat error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/stats', methods=['GET'])
        def get_stats():
            """Get pool statistics."""
            try:
                # Get general pool stats
                pool_stats = self.coordinator.get_pool_statistics()
                
                # Get user-specific stats if user_id provided
                user_id = request.args.get('user_id')
                user_stats = {}
                
                if user_id:
                    # Find user's devices and calculate stats
                    user_devices = [p for p in self.coordinator.participants.values() if p.user_id == user_id]
                    
                    if user_devices:
                        # Calculate user rank
                        all_participants = sorted(
                            self.coordinator.participants.values(),
                            key=lambda p: p.hardware_score.combined_score,
                            reverse=True
                        )
                        
                        user_rank = 1
                        for i, participant in enumerate(all_participants):
                            if participant.user_id == user_id:
                                user_rank = i + 1
                                break
                        
                        # Calculate combined reward percentage
                        total_reward_percentage = sum(p.current_reward_percentage for p in user_devices)
                        
                        # Calculate total work contributed
                        total_work = sum(p.total_work_contributed for p in user_devices)
                        
                        user_stats = {
                            'rank': user_rank,
                            'reward_percentage': total_reward_percentage,
                            'work_contributed': total_work,
                            'device_count': len(user_devices),
                            'devices': [
                                {
                                    'device_id': p.device_id,
                                    'device_name': p.device_name,
                                    'score': p.hardware_score.combined_score,
                                    'reward_percentage': p.current_reward_percentage
                                }
                                for p in user_devices
                            ]
                        }
                
                return jsonify({
                    **pool_stats,
                    'user_stats': user_stats,
                    'timestamp': datetime.now().isoformat()
                })
                
            except Exception as e:
                logger.error(f"Stats error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/participants', methods=['GET'])
        def get_participants():
            """Get list of participants."""
            try:
                participants = []
                for participant in self.coordinator.participants.values():
                    participants.append({
                        'user_id': participant.user_id,
                        'device_id': participant.device_id,
                        'device_name': participant.device_name,
                        'hardware_score': participant.hardware_score.combined_score,
                        'reward_percentage': participant.current_reward_percentage,
                        'work_contributed': participant.total_work_contributed,
                        'last_active': participant.last_active,
                        'joined_at': participant.joined_at
                    })
                
                # Sort by hardware score
                participants.sort(key=lambda p: p['hardware_score'], reverse=True)
                
                return jsonify({
                    'success': True,
                    'participants': participants,
                    'total': len(participants)
                })
                
            except Exception as e:
                logger.error(f"Participants error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/found_keys', methods=['GET'])
        def get_found_keys():
            """Get list of found keys (metadata only, no private keys)."""
            try:
                keys = []
                for found_key in self.coordinator.found_keys:
                    keys.append({
                        'puzzle_id': found_key.puzzle_id,
                        'address': found_key.address,
                        'found_by': found_key.found_by,
                        'found_at': found_key.found_at,
                        'reward_amount': found_key.reward_amount
                    })
                
                return jsonify({
                    'success': True,
                    'found_keys': keys,
                    'total': len(keys)
                })
                
            except Exception as e:
                logger.error(f"Found keys error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
        
        @self.app.route('/api/pool_dashboard', methods=['GET'])
        def pool_dashboard():
            """Serve the pool dashboard page."""
            try:
                dashboard_html = self._generate_dashboard_html()
                return dashboard_html, 200, {'Content-Type': 'text/html'}
            except Exception as e:
                logger.error(f"Dashboard error: {e}")
                return jsonify({'success': False, 'error': str(e)}), 500
    
    def _generate_dashboard_html(self) -> str:
        """Generate the pool dashboard HTML."""
        stats = self.coordinator.get_pool_statistics()
        
        html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KeyHound Enhanced - Distributed Pool Dashboard</title>
    <style>
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 100%);
            color: #ffffff;
            margin: 0;
            padding: 20px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
        }}
        .header h1 {{
            color: #00ff88;
            font-size: 2.5em;
            margin: 0;
            text-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }}
        .stat-card {{
            background: rgba(22, 33, 62, 0.8);
            border: 1px solid #333366;
            border-radius: 10px;
            padding: 20px;
            text-align: center;
        }}
        .stat-value {{
            font-size: 2em;
            color: #00ff88;
            font-weight: bold;
        }}
        .stat-label {{
            color: #cccccc;
            margin-top: 10px;
        }}
        .participants-section {{
            background: rgba(22, 33, 62, 0.8);
            border: 1px solid #333366;
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 30px;
        }}
        .participant-item {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding: 10px;
            border-bottom: 1px solid #333366;
        }}
        .participant-item:last-child {{
            border-bottom: none;
        }}
        .participant-info {{
            flex: 1;
        }}
        .participant-stats {{
            text-align: right;
        }}
        .join-pool {{
            background: rgba(0, 255, 136, 0.2);
            border: 2px solid #00ff88;
            border-radius: 10px;
            padding: 30px;
            text-align: center;
        }}
        .join-button {{
            background: #00ff88;
            color: #000000;
            border: none;
            padding: 15px 30px;
            border-radius: 5px;
            font-size: 1.2em;
            font-weight: bold;
            cursor: pointer;
            margin: 10px;
        }}
        .join-button:hover {{
            background: #00cc6a;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>KeyHound Enhanced</h1>
            <h2>Distributed Bitcoin Puzzle Solving Pool</h2>
        </div>
        
        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">{stats['total_participants']}</div>
                <div class="stat-label">Total Participants</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['active_participants']}</div>
                <div class="stat-label">Active Participants</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['total_keys_found']}</div>
                <div class="stat-label">Keys Found</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{stats['total_rewards_distributed']:.2f}</div>
                <div class="stat-label">Rewards Distributed (BTC)</div>
            </div>
        </div>
        
        <div class="participants-section">
            <h3>Top Performers</h3>
            {self._generate_participants_html(stats['top_performers'])}
        </div>
        
        <div class="join-pool">
            <h3>Join the Pool!</h3>
            <p>Contribute your computing power to solve Bitcoin puzzles and earn rewards.</p>
            <p>Fair reward distribution based on your hardware performance.</p>
            <button class="join-button" onclick="showJoinInstructions()">How to Join</button>
            <button class="join-button" onclick="downloadClient()">Download Client</button>
        </div>
    </div>
    
    <script>
        function showJoinInstructions() {{
            alert('To join the pool:\\n\\n1. Download the KeyHound Pool Client\\n2. Run: python pool_client.py --user-id YOUR_USER_ID\\n3. Your device will be automatically tested and scored\\n4. Start earning rewards based on your contribution!');
        }}
        
        function downloadClient() {{
            alert('Download the KeyHound Pool Client from:\\n\\nhttps://github.com/sethpizzaboy/KeyHound\\n\\nOr clone the repository and run the pool client.');
        }}
        
        // Auto-refresh stats every 30 seconds
        setInterval(function() {{
            location.reload();
        }}, 30000);
    </script>
</body>
</html>
        """
        
        return html
    
    def _generate_participants_html(self, top_performers: List[Dict]) -> str:
        """Generate HTML for participants list."""
        if not top_performers:
            return "<p>No participants yet. Be the first to join!</p>"
        
        html = ""
        for i, performer in enumerate(top_performers[:10]):  # Top 10
            html += f"""
            <div class="participant-item">
                <div class="participant-info">
                    <strong>#{i+1} {performer['user_id']}</strong><br>
                    <small>{performer['device_name']}</small>
                </div>
                <div class="participant-stats">
                    <div>Score: {performer['score']:.0f}</div>
                    <div>Reward: {performer['reward_percentage']:.3f}%</div>
                    <div>Work: {performer['work_contributed']}</div>
                </div>
            </div>
            """
        
        return html
    
    def _start_background_tasks(self):
        """Start background tasks."""
        # Start performance update thread
        def update_performance():
            while True:
                try:
                    self.coordinator.update_performance_scores()
                    time.sleep(3600)  # Update every hour
                except Exception as e:
                    logger.error(f"Performance update error: {e}")
                    time.sleep(3600)
        
        performance_thread = threading.Thread(target=update_performance, daemon=True)
        performance_thread.start()
        
        logger.info("Background tasks started")
    
    def run(self, debug=False):
        """Run the pool server."""
        logger.info(f"Starting KeyHound Pool Server on {self.host}:{self.port}")
        
        try:
            self.app.run(
                host=self.host,
                port=self.port,
                debug=debug,
                threaded=True
            )
        except KeyboardInterrupt:
            logger.info("Pool server stopped by user")
        except Exception as e:
            logger.error(f"Pool server error: {e}")

def main():
    """Main entry point."""
    import argparse
    
    parser = argparse.ArgumentParser(description='KeyHound Pool Server')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8080, help='Port to bind to')
    parser.add_argument('--pool-owner', default='pool_owner_2024', help='Pool owner ID')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    
    args = parser.parse_args()
    
    if not WEB_AVAILABLE:
        print("Error: Web dependencies not available.")
        print("Install with: pip install flask flask-cors")
        sys.exit(1)
    
    if not POOL_AVAILABLE:
        print("Error: Pool components not available.")
        print("Make sure all pool modules are properly installed.")
        sys.exit(1)
    
    try:
        # Initialize and run pool server
        pool_owner_public_key = "pool_owner_public_key_placeholder"  # In production, use real key
        
        server = PoolServerAPI(
            pool_owner_id=args.pool_owner,
            pool_owner_public_key=pool_owner_public_key,
            host=args.host,
            port=args.port
        )
        
        print("=" * 60)
        print("KeyHound Enhanced - Distributed Pool Server")
        print("=" * 60)
        print(f"Pool Owner: {args.pool_owner}")
        print(f"Server URL: http://{args.host}:{args.port}")
        print(f"Dashboard: http://{args.host}:{args.port}/api/pool_dashboard")
        print(f"API Base: http://{args.host}:{args.port}/api/")
        print("=" * 60)
        
        server.run(debug=args.debug)
        
    except Exception as e:
        logger.error(f"Failed to start pool server: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
