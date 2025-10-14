"""
KeyHound Enhanced - Distributed Pool Coordinator
Manages the distributed community pool with secure key delivery and reward distribution.
"""

import os
import sys
import time
import json
import hashlib
import threading
import requests
import cryptography
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime, timedelta
import logging
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

try:
    from core.simple_keyhound import SimpleKeyHound
    from core.bitcoin_cryptography import BitcoinCryptography
    from pool.hardware_scorer import HardwarePerformanceScorer, HardwareScore
    KEYHOUND_AVAILABLE = True
except ImportError:
    KEYHOUND_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@dataclass
class PoolParticipant:
    """Pool participant information."""
    user_id: str
    device_id: str
    device_name: str
    hardware_score: HardwareScore
    joined_at: str
    last_active: str
    total_work_contributed: int
    current_reward_percentage: float
    devices: List[str]  # List of device IDs for this user

@dataclass
class PuzzleWork:
    """Puzzle work assignment."""
    puzzle_id: str
    puzzle_bits: int
    work_range_start: str
    work_range_end: str
    assigned_to: str
    assigned_at: str
    deadline: str
    status: str  # 'assigned', 'in_progress', 'completed', 'expired'

@dataclass
class FoundKey:
    """Found private key with reward information."""
    puzzle_id: str
    private_key: str
    public_key: str
    address: str
    found_by: str
    found_at: str
    reward_amount: float
    reward_distribution: Dict[str, float]

class SecureKeyDelivery:
    """Secure key delivery system - only pool owner receives keys."""
    
    def __init__(self, pool_owner_public_key: str):
        self.pool_owner_public_key = pool_owner_public_key
        self.encryption_key = self._generate_encryption_key()
    
    def _generate_encryption_key(self) -> bytes:
        """Generate encryption key for secure communication."""
        # In production, this would be derived from pool owner's private key
        password = b"keyhound_pool_2024_secure_key"
        salt = b"keyhound_salt_2024"
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
    
    def encrypt_key_for_owner(self, private_key: str, metadata: Dict[str, Any]) -> str:
        """Encrypt found private key for pool owner only."""
        try:
            f = Fernet(self.encryption_key)
            
            # Create payload with key and metadata
            payload = {
                'private_key': private_key,
                'metadata': metadata,
                'timestamp': datetime.now().isoformat(),
                'pool_id': 'keyhound_enhanced_pool'
            }
            
            # Encrypt payload
            encrypted_data = f.encrypt(json.dumps(payload).encode())
            
            # Encode for transmission
            encrypted_key = base64.urlsafe_b64encode(encrypted_data).decode()
            
            logger.info(f"Successfully encrypted key for pool owner")
            return encrypted_key
            
        except Exception as e:
            logger.error(f"Failed to encrypt key: {e}")
            raise
    
    def decrypt_key_for_owner(self, encrypted_key: str) -> Dict[str, Any]:
        """Decrypt key for pool owner."""
        try:
            f = Fernet(self.encryption_key)
            
            # Decode and decrypt
            encrypted_data = base64.urlsafe_b64decode(encrypted_key.encode())
            decrypted_data = f.decrypt(encrypted_data)
            
            # Parse payload
            payload = json.loads(decrypted_data.decode())
            
            logger.info(f"Successfully decrypted key for pool owner")
            return payload
            
        except Exception as e:
            logger.error(f"Failed to decrypt key: {e}")
            raise

class RewardDistributor:
    """Reward distribution system based on performance and contribution."""
    
    def __init__(self):
        self.distribution_history = []
    
    def calculate_reward_distribution(self, 
                                    total_reward: float,
                                    participants: List[PoolParticipant],
                                    finder: PoolParticipant) -> Dict[str, float]:
        """Calculate fair reward distribution."""
        
        # Pool owner gets 40%
        pool_owner_share = total_reward * 0.40
        
        # Finder gets 20% (bonus for finding the key)
        finder_share = total_reward * 0.20
        
        # Remaining 40% distributed among all participants based on performance
        community_pool = total_reward * 0.40
        
        # Calculate total performance score for all participants
        total_performance = sum(p.hardware_score.combined_score for p in participants)
        
        distribution = {
            'pool_owner': pool_owner_share,
            'finder': finder_share
        }
        
        # Distribute community pool based on performance scores
        for participant in participants:
            if participant.device_id == finder.device_id:
                # Finder gets their performance share plus finder bonus
                performance_share = (participant.hardware_score.combined_score / total_performance) * community_pool
                distribution[participant.user_id] = performance_share + finder_share
            else:
                # Regular participants get their performance share
                performance_share = (participant.hardware_score.combined_score / total_performance) * community_pool
                distribution[participant.user_id] = performance_share
        
        # Normalize to ensure total equals 100%
        total_distributed = sum(distribution.values())
        if total_distributed > 0:
            for user_id in distribution:
                distribution[user_id] = (distribution[user_id] / total_distributed) * total_reward
        
        return distribution
    
    def get_multi_device_bonus(self, user_id: str, participants: List[PoolParticipant]) -> float:
        """Calculate bonus for users with multiple devices."""
        user_devices = [p for p in participants if p.user_id == user_id]
        
        if len(user_devices) <= 1:
            return 1.0
        
        # Bonus increases with more devices, but with diminishing returns
        bonus = 1.0 + (len(user_devices) - 1) * 0.2
        return min(bonus, 2.0)  # Cap at 2x bonus

class DistributedPoolCoordinator:
    """Main coordinator for the distributed Bitcoin puzzle solving pool."""
    
    def __init__(self, pool_owner_id: str, pool_owner_public_key: str):
        self.pool_owner_id = pool_owner_id
        self.pool_owner_public_key = pool_owner_public_key
        
        # Initialize components
        self.hardware_scorer = HardwarePerformanceScorer()
        self.secure_delivery = SecureKeyDelivery(pool_owner_public_key)
        self.reward_distributor = RewardDistributor()
        
        # Pool state
        self.participants: Dict[str, PoolParticipant] = {}
        self.active_work: Dict[str, PuzzleWork] = {}
        self.found_keys: List[FoundKey] = []
        self.performance_history: Dict[str, List[Dict]] = {}
        
        # Performance tracking periods
        self.performance_periods = [
            '1_hour', '6_hour', '12_hour', '18_hour', '24_hour',
            '48_hour', '96_hour', '1_week'
        ]
        self.current_period = 0
        self.period_start_time = datetime.now()
        
        # Statistics
        self.total_keys_found = 0
        self.total_rewards_distributed = 0.0
        
    def register_participant(self, user_id: str, device_name: str, 
                           public_key: str) -> Dict[str, Any]:
        """Register a new participant in the pool."""
        try:
            # Get hardware specifications
            hardware_specs = self.hardware_scorer.get_hardware_specs(user_id, device_name)
            
            # Run quick performance test (1 minute)
            logger.info(f"Running quick performance test for {user_id}...")
            quick_tests = self.hardware_scorer.run_quick_performance_test(60)
            
            # Calculate hardware score
            hardware_score = self.hardware_scorer.calculate_hardware_score(
                hardware_specs, quick_tests)
            hardware_score.user_id = user_id
            
            # Create participant
            participant = PoolParticipant(
                user_id=user_id,
                device_id=hardware_score.device_id,
                device_name=hardware_specs.device_name,
                hardware_score=hardware_score,
                joined_at=datetime.now().isoformat(),
                last_active=datetime.now().isoformat(),
                total_work_contributed=0,
                current_reward_percentage=hardware_score.reward_percentage,
                devices=[hardware_score.device_id]
            )
            
            # Register participant
            self.participants[participant.device_id] = participant
            
            # Initialize performance history
            self.performance_history[participant.device_id] = []
            
            logger.info(f"Registered participant {user_id} with device {device_name}")
            logger.info(f"Hardware score: {hardware_score.combined_score:.2f}")
            logger.info(f"Reward percentage: {hardware_score.reward_percentage:.3f}%")
            
            return {
                'success': True,
                'device_id': participant.device_id,
                'hardware_score': hardware_score.combined_score,
                'reward_percentage': hardware_score.reward_percentage,
                'message': 'Successfully registered in pool'
            }
            
        except Exception as e:
            logger.error(f"Failed to register participant: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Registration failed'
            }
    
    def assign_work(self, puzzle_id: str, puzzle_bits: int) -> Dict[str, Any]:
        """Assign puzzle work to participants."""
        try:
            # Find best available participants
            available_participants = [
                p for p in self.participants.values() 
                if p.device_id not in [w.assigned_to for w in self.active_work.values()]
            ]
            
            if not available_participants:
                return {
                    'success': False,
                    'message': 'No available participants'
                }
            
            # Sort by performance score
            available_participants.sort(
                key=lambda p: p.hardware_score.combined_score, reverse=True)
            
            # Calculate work ranges based on performance
            total_performance = sum(p.hardware_score.combined_score for p in available_participants)
            
            work_assignments = []
            current_range = 0
            
            for participant in available_participants:
                # Calculate work share based on performance
                performance_ratio = participant.hardware_score.combined_score / total_performance
                work_share = int(2**puzzle_bits * performance_ratio)
                
                # Create work assignment
                work = PuzzleWork(
                    puzzle_id=puzzle_id,
                    puzzle_bits=puzzle_bits,
                    work_range_start=hex(current_range),
                    work_range_end=hex(current_range + work_share),
                    assigned_to=participant.device_id,
                    assigned_at=datetime.now().isoformat(),
                    deadline=(datetime.now() + timedelta(hours=24)).isoformat(),
                    status='assigned'
                )
                
                self.active_work[work.assigned_to] = work
                work_assignments.append(work)
                
                current_range += work_share
                
                # Update participant
                participant.last_active = datetime.now().isoformat()
            
            logger.info(f"Assigned {puzzle_id} ({puzzle_bits}-bit) to {len(work_assignments)} participants")
            
            return {
                'success': True,
                'puzzle_id': puzzle_id,
                'assignments': len(work_assignments),
                'message': f'Work assigned to {len(work_assignments)} participants'
            }
            
        except Exception as e:
            logger.error(f"Failed to assign work: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Work assignment failed'
            }
    
    def submit_found_key(self, device_id: str, puzzle_id: str, 
                        private_key: str, public_key: str, address: str) -> Dict[str, Any]:
        """Submit a found private key."""
        try:
            # Verify participant
            if device_id not in self.participants:
                return {
                    'success': False,
                    'message': 'Unknown participant'
                }
            
            participant = self.participants[device_id]
            
            # Encrypt key for pool owner
            metadata = {
                'finder': participant.user_id,
                'device_id': device_id,
                'puzzle_id': puzzle_id,
                'found_at': datetime.now().isoformat()
            }
            
            encrypted_key = self.secure_delivery.encrypt_key_for_owner(
                private_key, metadata)
            
            # Calculate reward distribution
            participants_list = list(self.participants.values())
            reward_distribution = self.reward_distributor.calculate_reward_distribution(
                1.0, participants_list, participant)  # Assume 1 BTC reward for now
            
            # Create found key record
            found_key = FoundKey(
                puzzle_id=puzzle_id,
                private_key=private_key,  # This will be encrypted in production
                public_key=public_key,
                address=address,
                found_by=participant.user_id,
                found_at=datetime.now().isoformat(),
                reward_amount=1.0,
                reward_distribution=reward_distribution
            )
            
            self.found_keys.append(found_key)
            self.total_keys_found += 1
            
            # Update participant stats
            participant.total_work_contributed += 1
            
            logger.info(f"Key found by {participant.user_id} for puzzle {puzzle_id}")
            logger.info(f"Reward distribution: {reward_distribution}")
            
            # TODO: Send encrypted key to pool owner via secure channel
            
            return {
                'success': True,
                'encrypted_key': encrypted_key,
                'reward_distribution': reward_distribution,
                'message': 'Key successfully submitted and encrypted for pool owner'
            }
            
        except Exception as e:
            logger.error(f"Failed to submit found key: {e}")
            return {
                'success': False,
                'error': str(e),
                'message': 'Key submission failed'
            }
    
    def update_performance_scores(self):
        """Update performance scores based on current period."""
        try:
            current_time = datetime.now()
            period_duration = self._get_period_duration()
            
            # Check if period has ended
            if (current_time - self.period_start_time).total_seconds() >= period_duration:
                self._advance_performance_period()
            
            # Run comprehensive tests for active participants
            for participant in self.participants.values():
                if participant.last_active > (current_time - timedelta(hours=1)).isoformat():
                    # Run comprehensive performance test
                    comprehensive_tests = self.hardware_scorer.run_comprehensive_performance_test(3600)
                    
                    # Update hardware score
                    new_score = self.hardware_scorer.calculate_hardware_score(
                        participant.hardware_score, comprehensive_tests)
                    new_score.user_id = participant.user_id
                    
                    # Update participant
                    participant.hardware_score = new_score
                    participant.current_reward_percentage = new_score.reward_percentage
                    
                    # Record in history
                    self.performance_history[participant.device_id].append({
                        'timestamp': current_time.isoformat(),
                        'score': new_score.combined_score,
                        'reward_percentage': new_score.reward_percentage,
                        'period': self.performance_periods[self.current_period]
                    })
            
            logger.info(f"Updated performance scores for {len(self.participants)} participants")
            
        except Exception as e:
            logger.error(f"Failed to update performance scores: {e}")
    
    def _get_period_duration(self) -> int:
        """Get duration of current performance period in seconds."""
        period_durations = {
            '1_hour': 3600,
            '6_hour': 21600,
            '12_hour': 43200,
            '18_hour': 64800,
            '24_hour': 86400,
            '48_hour': 172800,
            '96_hour': 345600,
            '1_week': 604800
        }
        
        current_period = self.performance_periods[self.current_period]
        return period_durations.get(current_period, 3600)
    
    def _advance_performance_period(self):
        """Advance to next performance period."""
        self.current_period = (self.current_period + 1) % len(self.performance_periods)
        self.period_start_time = datetime.now()
        
        logger.info(f"Advanced to performance period: {self.performance_periods[self.current_period]}")
    
    def get_pool_statistics(self) -> Dict[str, Any]:
        """Get comprehensive pool statistics."""
        return {
            'total_participants': len(self.participants),
            'active_participants': len([p for p in self.participants.values() 
                                      if p.last_active > (datetime.now() - timedelta(hours=24)).isoformat()]),
            'total_work_assignments': len(self.active_work),
            'total_keys_found': self.total_keys_found,
            'total_rewards_distributed': self.total_rewards_distributed,
            'current_performance_period': self.performance_periods[self.current_period],
            'period_start_time': self.period_start_time.isoformat(),
            'participants_by_device_type': self._get_participants_by_device_type(),
            'top_performers': self._get_top_performers()
        }
    
    def _get_participants_by_device_type(self) -> Dict[str, int]:
        """Get participant count by device type."""
        device_types = {}
        for participant in self.participants.values():
            device_type = participant.hardware_score.device_type
            device_types[device_type] = device_types.get(device_type, 0) + 1
        return device_types
    
    def _get_top_performers(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get top performing participants."""
        sorted_participants = sorted(
            self.participants.values(),
            key=lambda p: p.hardware_score.combined_score,
            reverse=True
        )
        
        return [
            {
                'user_id': p.user_id,
                'device_name': p.device_name,
                'score': p.hardware_score.combined_score,
                'reward_percentage': p.current_reward_percentage,
                'work_contributed': p.total_work_contributed
            }
            for p in sorted_participants[:limit]
        ]

def main():
    """Main entry point for testing."""
    print("=" * 60)
    print("KeyHound Enhanced - Distributed Pool Coordinator")
    print("=" * 60)
    
    # Initialize pool coordinator
    pool_owner_id = "pool_owner_2024"
    pool_owner_public_key = "pool_owner_public_key_placeholder"
    
    coordinator = DistributedPoolCoordinator(pool_owner_id, pool_owner_public_key)
    
    # Test participant registration
    print("\nTesting participant registration...")
    result = coordinator.register_participant("test_user_1", "gaming_pc", "test_public_key")
    print(f"Registration result: {result}")
    
    # Test work assignment
    print("\nTesting work assignment...")
    work_result = coordinator.assign_work("puzzle_66", 66)
    print(f"Work assignment result: {work_result}")
    
    # Get pool statistics
    print("\nPool statistics:")
    stats = coordinator.get_pool_statistics()
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    print(f"\n[SUCCESS] Distributed pool coordinator test completed!")

if __name__ == '__main__':
    main()
