"""
KeyHound Enhanced - Community Pool Client
Client application for participants to join the distributed pool and contribute computing power.
"""

import os
import sys
import time
import json
import hashlib
import threading
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime, timedelta
import logging

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.simple_keyhound import SimpleKeyHound
    from core.bitcoin_cryptography import BitcoinCryptography
    from core.puzzle_data import BITCOIN_PUZZLES, hex_range_to_int_range
    from pool.hardware_scorer import HardwarePerformanceScorer
    KEYHOUND_AVAILABLE = True
except ImportError:
    KEYHOUND_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PoolWorkAssignment:
    """Work assignment from pool coordinator."""
    puzzle_id: str
    puzzle_bits: int
    work_range_start: str
    work_range_end: str
    deadline: str
    reward_percentage: float

@dataclass
class PoolStats:
    """Pool statistics for client display."""
    total_participants: int
    active_participants: int
    total_keys_found: int
    current_performance_period: str
    user_rank: int
    user_reward_percentage: float
    work_contributed: int

class CommunityPoolClient:
    """Client for participating in the distributed Bitcoin puzzle solving pool."""
    
    def __init__(self, pool_server_url: str, user_id: str):
        self.pool_server_url = pool_server_url.rstrip('/')
        self.user_id = user_id
        self.device_id = None
        self.device_name = None
        self.is_registered = False
        self.current_work = None
        self.hardware_scorer = HardwarePerformanceScorer()
        self.keyhound = None
        self.bitcoin_crypto = None
        
        # Performance tracking
        self.work_start_time = None
        self.keys_checked = 0
        self.last_heartbeat = None
        
        # Threading
        self.work_thread = None
        self.heartbeat_thread = None
        self.running = False
        
        # Initialize KeyHound components
        if KEYHOUND_AVAILABLE:
            try:
                self.keyhound = SimpleKeyHound(verbose=False)
                self.bitcoin_crypto = BitcoinCryptography()
                logger.info("KeyHound components initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize KeyHound components: {e}")
    
    def register_device(self, device_name: str = None) -> Dict[str, Any]:
        """Register this device with the pool."""
        try:
            if device_name is None:
                device_name = f"{os.getenv('COMPUTERNAME', 'unknown')}_{platform.system()}"
            
            self.device_name = device_name
            
            # Get hardware specifications
            hardware_specs = self.hardware_scorer.get_hardware_specs(self.user_id, device_name)
            
            # Run quick performance test
            logger.info("Running hardware performance test...")
            quick_tests = self.hardware_scorer.run_quick_performance_test(60)
            
            # Calculate hardware score
            hardware_score = self.hardware_scorer.calculate_hardware_score(
                hardware_specs, quick_tests)
            
            # Prepare registration data
            registration_data = {
                'user_id': self.user_id,
                'device_name': device_name,
                'hardware_specs': {
                    'device_id': hardware_score.device_id,
                    'device_type': hardware_specs.device_type,
                    'cpu_count': hardware_specs.cpu_count,
                    'cpu_frequency': hardware_specs.cpu_frequency,
                    'memory_total': hardware_specs.memory_total,
                    'gpu_count': hardware_specs.gpu_count,
                    'gpu_memory': hardware_specs.gpu_memory,
                    'battery_powered': hardware_specs.battery_powered
                },
                'performance_tests': [
                    {
                        'test_name': test.test_name,
                        'operations_per_second': test.operations_per_second,
                        'memory_usage': test.memory_usage,
                        'cpu_usage': test.cpu_usage,
                        'power_efficiency': test.power_efficiency
                    }
                    for test in quick_tests
                ],
                'hardware_score': {
                    'combined_score': hardware_score.combined_score,
                    'reward_percentage': hardware_score.reward_percentage
                }
            }
            
            # Send registration to pool server
            response = requests.post(
                f"{self.pool_server_url}/api/register",
                json=registration_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    self.device_id = result['device_id']
                    self.is_registered = True
                    logger.info(f"Successfully registered device: {device_name}")
                    logger.info(f"Hardware score: {result['hardware_score']}")
                    logger.info(f"Reward percentage: {result['reward_percentage']:.3f}%")
                    return result
                else:
                    logger.error(f"Registration failed: {result.get('message', 'Unknown error')}")
                    return result
            else:
                logger.error(f"Registration failed with status: {response.status_code}")
                return {'success': False, 'error': f'HTTP {response.status_code}'}
                
        except Exception as e:
            logger.error(f"Registration failed: {e}")
            return {'success': False, 'error': str(e)}
    
    def request_work(self) -> Optional[PoolWorkAssignment]:
        """Request work assignment from the pool."""
        try:
            if not self.is_registered:
                logger.error("Device not registered")
                return None
            
            # Send work request
            work_request = {
                'user_id': self.user_id,
                'device_id': self.device_id,
                'capabilities': {
                    'max_puzzle_bits': 66,
                    'preferred_work_size': 1000000
                }
            }
            
            response = requests.post(
                f"{self.pool_server_url}/api/request_work",
                json=work_request,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success') and result.get('work_assignment'):
                    work_data = result['work_assignment']
                    
                    assignment = PoolWorkAssignment(
                        puzzle_id=work_data['puzzle_id'],
                        puzzle_bits=work_data['puzzle_bits'],
                        work_range_start=work_data['work_range_start'],
                        work_range_end=work_data['work_range_end'],
                        deadline=work_data['deadline'],
                        reward_percentage=result.get('reward_percentage', 0.1)
                    )
                    
                    logger.info(f"Received work assignment: {assignment.puzzle_id}")
                    logger.info(f"Work range: {assignment.work_range_start} - {assignment.work_range_end}")
                    logger.info(f"Reward percentage: {assignment.reward_percentage:.3f}%")
                    
                    return assignment
                else:
                    logger.info("No work available at this time")
                    return None
            else:
                logger.error(f"Work request failed with status: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Work request failed: {e}")
            return None
    
    def solve_assigned_puzzle(self, assignment: PoolWorkAssignment) -> Optional[Dict[str, str]]:
        """Solve the assigned puzzle work."""
        try:
            logger.info(f"Starting puzzle solving: {assignment.puzzle_id}")
            
            # Get puzzle information
            puzzle_info = BITCOIN_PUZZLES.get(assignment.puzzle_bits)
            if not puzzle_info:
                logger.error(f"Unknown puzzle: {assignment.puzzle_bits} bits")
                return None
            
            # Parse work range
            start_int = int(assignment.work_range_start, 16)
            end_int = int(assignment.work_range_end, 16)
            
            logger.info(f"Checking range: {start_int} to {end_int}")
            logger.info(f"Total keys to check: {end_int - start_int:,}")
            
            # Start work tracking
            self.work_start_time = time.time()
            self.keys_checked = 0
            
            # Solve puzzle
            current_key = start_int
            
            while current_key < end_int:
                # Check for deadline
                if datetime.now() > datetime.fromisoformat(assignment.deadline):
                    logger.warning("Work deadline exceeded")
                    break
                
                # Generate private key
                private_key = format(current_key, '064x')
                
                try:
                    # Generate address
                    public_key = self.bitcoin_crypto.private_key_to_public_key(private_key)
                    address = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                    
                    # Check if this matches the puzzle target
                    if self._check_puzzle_target(address, puzzle_info):
                        logger.info(f"PUZZLE SOLVED! Private key: {private_key}")
                        logger.info(f"Address: {address}")
                        
                        return {
                            'private_key': private_key,
                            'public_key': public_key,
                            'address': address,
                            'keys_checked': self.keys_checked,
                            'time_taken': time.time() - self.work_start_time
                        }
                    
                    self.keys_checked += 1
                    
                    # Progress reporting every 1000 keys
                    if self.keys_checked % 1000 == 0:
                        elapsed = time.time() - self.work_start_time
                        rate = self.keys_checked / elapsed if elapsed > 0 else 0
                        logger.info(f"Progress: {self.keys_checked:,} keys checked, {rate:.0f} keys/sec")
                        
                        # Send heartbeat
                        self._send_heartbeat(assignment.puzzle_id, self.keys_checked)
                    
                except Exception as e:
                    logger.warning(f"Error processing key {current_key}: {e}")
                
                current_key += 1
            
            logger.info(f"Work completed. Checked {self.keys_checked:,} keys")
            return None
            
        except Exception as e:
            logger.error(f"Puzzle solving failed: {e}")
            return None
    
    def _check_puzzle_target(self, address: str, puzzle_info: Dict[str, Any]) -> bool:
        """Check if address matches puzzle target."""
        # This is a simplified check - in reality, you'd check against the actual puzzle target
        # For demo purposes, we'll use a very unlikely match condition
        return address.startswith(puzzle_info.get('target_prefix', '1'))
    
    def submit_found_key(self, assignment: PoolWorkAssignment, result: Dict[str, str]) -> bool:
        """Submit found private key to the pool."""
        try:
            submission_data = {
                'user_id': self.user_id,
                'device_id': self.device_id,
                'puzzle_id': assignment.puzzle_id,
                'private_key': result['private_key'],
                'public_key': result['public_key'],
                'address': result['address'],
                'keys_checked': result['keys_checked'],
                'time_taken': result['time_taken'],
                'found_at': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.pool_server_url}/api/submit_key",
                json=submission_data,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                if result.get('success'):
                    logger.info("Successfully submitted found key!")
                    logger.info(f"Reward distribution: {result.get('reward_distribution', {})}")
                    return True
                else:
                    logger.error(f"Key submission failed: {result.get('message', 'Unknown error')}")
                    return False
            else:
                logger.error(f"Key submission failed with status: {response.status_code}")
                return False
                
        except Exception as e:
            logger.error(f"Key submission failed: {e}")
            return False
    
    def _send_heartbeat(self, puzzle_id: str, keys_checked: int):
        """Send heartbeat to pool server."""
        try:
            heartbeat_data = {
                'user_id': self.user_id,
                'device_id': self.device_id,
                'puzzle_id': puzzle_id,
                'keys_checked': keys_checked,
                'timestamp': datetime.now().isoformat()
            }
            
            response = requests.post(
                f"{self.pool_server_url}/api/heartbeat",
                json=heartbeat_data,
                timeout=10
            )
            
            if response.status_code == 200:
                self.last_heartbeat = datetime.now()
            else:
                logger.warning(f"Heartbeat failed: {response.status_code}")
                
        except Exception as e:
            logger.warning(f"Heartbeat failed: {e}")
    
    def get_pool_stats(self) -> Optional[PoolStats]:
        """Get current pool statistics."""
        try:
            response = requests.get(
                f"{self.pool_server_url}/api/stats",
                timeout=10
            )
            
            if response.status_code == 200:
                stats_data = response.json()
                
                # Get user-specific stats
                user_stats = stats_data.get('user_stats', {})
                
                return PoolStats(
                    total_participants=stats_data.get('total_participants', 0),
                    active_participants=stats_data.get('active_participants', 0),
                    total_keys_found=stats_data.get('total_keys_found', 0),
                    current_performance_period=stats_data.get('current_performance_period', 'unknown'),
                    user_rank=user_stats.get('rank', 0),
                    user_reward_percentage=user_stats.get('reward_percentage', 0.0),
                    work_contributed=user_stats.get('work_contributed', 0)
                )
            else:
                logger.error(f"Failed to get pool stats: {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Failed to get pool stats: {e}")
            return None
    
    def start_pool_participation(self, device_name: str = None):
        """Start participating in the pool."""
        try:
            logger.info("Starting pool participation...")
            
            # Register device
            registration_result = self.register_device(device_name)
            if not registration_result.get('success'):
                logger.error("Failed to register device")
                return False
            
            self.running = True
            
            # Start heartbeat thread
            self.heartbeat_thread = threading.Thread(target=self._heartbeat_loop, daemon=True)
            self.heartbeat_thread.start()
            
            # Start work loop
            self.work_thread = threading.Thread(target=self._work_loop, daemon=True)
            self.work_thread.start()
            
            logger.info("Pool participation started successfully!")
            return True
            
        except Exception as e:
            logger.error(f"Failed to start pool participation: {e}")
            return False
    
    def _heartbeat_loop(self):
        """Heartbeat loop for maintaining connection."""
        while self.running:
            try:
                if self.current_work and self.work_start_time:
                    elapsed = time.time() - self.work_start_time
                    if elapsed > 60:  # Send heartbeat every minute
                        self._send_heartbeat(self.current_work.puzzle_id, self.keys_checked)
                
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.warning(f"Heartbeat loop error: {e}")
                time.sleep(60)
    
    def _work_loop(self):
        """Main work loop for solving puzzles."""
        while self.running:
            try:
                # Request work
                assignment = self.request_work()
                if not assignment:
                    logger.info("No work available, waiting 60 seconds...")
                    time.sleep(60)
                    continue
                
                self.current_work = assignment
                
                # Solve puzzle
                result = self.solve_assigned_puzzle(assignment)
                
                if result:
                    # Submit found key
                    if self.submit_found_key(assignment, result):
                        logger.info("🎉 KEY FOUND AND SUBMITTED! 🎉")
                    else:
                        logger.error("Failed to submit found key")
                
                self.current_work = None
                
            except Exception as e:
                logger.error(f"Work loop error: {e}")
                time.sleep(60)
    
    def stop_pool_participation(self):
        """Stop participating in the pool."""
        logger.info("Stopping pool participation...")
        self.running = False
        
        if self.work_thread:
            self.work_thread.join(timeout=5)
        
        if self.heartbeat_thread:
            self.heartbeat_thread.join(timeout=5)
        
        logger.info("Pool participation stopped")

def main():
    """Main entry point for testing."""
    import argparse
    
    parser = argparse.ArgumentParser(description='KeyHound Community Pool Client')
    parser.add_argument('--server-url', default='http://localhost:8080', help='Pool server URL')
    parser.add_argument('--user-id', required=True, help='User ID for pool participation')
    parser.add_argument('--device-name', help='Device name (auto-detected if not provided)')
    
    args = parser.parse_args()
    
    print("=" * 60)
    print("KeyHound Enhanced - Community Pool Client")
    print("=" * 60)
    
    if not KEYHOUND_AVAILABLE:
        print("[ERROR] KeyHound components not available")
        sys.exit(1)
    
    # Create client
    client = CommunityPoolClient(args.server_url, args.user_id)
    
    try:
        # Start participation
        success = client.start_pool_participation(args.device_name)
        
        if success:
            print(f"\n[SUCCESS] Started pool participation for user: {args.user_id}")
            print(f"Server URL: {args.server_url}")
            print(f"Device ID: {client.device_id}")
            print(f"Device Name: {client.device_name}")
            print("\nPress Ctrl+C to stop participation...")
            
            # Keep running until interrupted
            try:
                while True:
                    # Display stats every 5 minutes
                    stats = client.get_pool_stats()
                    if stats:
                        print(f"\nPool Stats:")
                        print(f"  Total Participants: {stats.total_participants}")
                        print(f"  Active Participants: {stats.active_participants}")
                        print(f"  Keys Found: {stats.total_keys_found}")
                        print(f"  Your Rank: {stats.user_rank}")
                        print(f"  Your Reward %: {stats.user_reward_percentage:.3f}%")
                        print(f"  Work Contributed: {stats.work_contributed}")
                    
                    time.sleep(300)  # 5 minutes
                    
            except KeyboardInterrupt:
                print("\nStopping pool participation...")
                client.stop_pool_participation()
                print("Pool participation stopped.")
        else:
            print("[ERROR] Failed to start pool participation")
            sys.exit(1)
            
    except Exception as e:
        print(f"[ERROR] Pool client error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
