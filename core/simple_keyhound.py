#!/usr/bin/env python3
"""
KeyHound Enhanced - Simplified Core Implementation
A working, simplified version of KeyHound Enhanced that focuses on core functionality
"""

import sys
import os
import time
import hashlib
import secrets
from pathlib import Path
from datetime import datetime
import logging

# Add current directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Import core modules
try:
    from .bitcoin_cryptography import BitcoinCryptography
    from .puzzle_data import BITCOIN_PUZZLES, get_brainwallet_patterns
    from .brainwallet_patterns import BrainwalletPatternLibrary
except ImportError:
    # Fallback for direct execution
    from bitcoin_cryptography import BitcoinCryptography
    from puzzle_data import BITCOIN_PUZZLES, get_brainwallet_patterns
    from brainwallet_patterns import BrainwalletPatternLibrary

class SimpleKeyHound:
    """
    Simplified KeyHound Enhanced - Core functionality without complex dependencies
    """
    
    def __init__(self, verbose=True):
        """Initialize SimpleKeyHound with core functionality."""
        self.verbose = verbose
        self.start_time = time.time()
        
        # Set up logging
        logging.basicConfig(
            level=logging.INFO if verbose else logging.WARNING,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('SimpleKeyHound')
        
        # Initialize core components
        self.bitcoin_crypto = BitcoinCryptography()
        self.pattern_library = BrainwalletPatternLibrary()
        
        # Performance tracking
        self.keys_generated = 0
        self.start_time = time.time()
        
        self.logger.info("SimpleKeyHound initialized successfully")
        self.logger.info(f"Bitcoin cryptography module: {'✓' if self.bitcoin_crypto else '✗'}")
        self.logger.info(f"Pattern library: {'✓' if self.pattern_library else '✗'}")
    
    def solve_puzzle(self, bits, target_address=None, max_attempts=None, timeout=3600):
        """
        Solve a Bitcoin puzzle of specified bit length.
        
        Args:
            bits (int): Bit length of the puzzle (40-66 recommended)
            target_address (str, optional): Target Bitcoin address to find
            max_attempts (int, optional): Maximum number of attempts
            timeout (int): Timeout in seconds (default: 3600)
        
        Returns:
            dict: Result containing private_key, address, and metadata
        """
        self.logger.info(f"Starting puzzle solving: {bits}-bit puzzle")
        
        if bits < 40 or bits > 66:
            raise ValueError("Puzzle bits must be between 40 and 66")
        
        # Calculate range
        max_key = 2 ** bits
        start_key = 0
        
        # Set reasonable limits
        if max_attempts is None:
            max_attempts = min(2 ** (bits - 10), 10000000)  # Reasonable limit
        
        # Checkpoint setup
        checkpoint_dir = Path("checkpoints")
        checkpoint_dir.mkdir(exist_ok=True)
        checkpoint_file = checkpoint_dir / f"puzzle_{bits}_checkpoint.json"
        
        # Load checkpoint if exists
        last_key = start_key
        total_attempts_before = 0
        if checkpoint_file.exists():
            try:
                import json
                with open(checkpoint_file, 'r') as f:
                    checkpoint = json.load(f)
                    last_key = checkpoint.get('last_key', start_key)
                    total_attempts_before = checkpoint.get('total_attempts', 0)
                    self.logger.info(f"Resuming from checkpoint: last_key={last_key:,}, total_attempts={total_attempts_before:,}")
            except Exception as e:
                self.logger.warning(f"Failed to load checkpoint: {e}, starting fresh")
                last_key = start_key
        
        self.logger.info(f"Search range: {last_key:,} to {max_key:,}")
        self.logger.info(f"Max attempts: {max_attempts:,}")
        
        # Performance tracking
        start_time = time.time()
        keys_checked = 0
        last_checkpoint_time = start_time
        checkpoint_interval = 60  # Save checkpoint every 60 seconds
        
        # Initialize loop variables
        current_key = last_key
        total_attempts = total_attempts_before
        
        def save_checkpoint(key, attempts):
            """Save checkpoint to file."""
            try:
                import json
                checkpoint_data = {
                    'last_key': key,
                    'total_attempts': attempts,
                    'timestamp': datetime.now().isoformat(),
                    'puzzle_bits': bits,
                    'target_address': target_address
                }
                with open(checkpoint_file, 'w') as f:
                    json.dump(checkpoint_data, f, indent=2)
                self.logger.debug(f"Checkpoint saved: key={key:,}, attempts={attempts:,}")
            except Exception as e:
                self.logger.warning(f"Failed to save checkpoint: {e}")
        
        try:
            # Generate and check keys sequentially starting from last_key
            
            # Generate and check keys
            while current_key < max_key and total_attempts < max_attempts:
                # Generate private key from current integer
                private_key = format(current_key, '064x')
                
                # Generate address
                try:
                    public_key = self.bitcoin_crypto.private_key_to_public_key(private_key)
                    address = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                    keys_checked += 1
                    total_attempts += 1
                    current_key += 1
                    
                    # Check if we found the target
                    if target_address and address == target_address:
                        elapsed = time.time() - start_time
                        self.logger.info(f"PUZZLE SOLVED! Found target address: {address}")
                        
                        # Delete checkpoint on success
                        if checkpoint_file.exists():
                            checkpoint_file.unlink()
                            self.logger.info("Checkpoint deleted after successful solve")
                        
                        return {
                            'private_key': private_key,
                            'public_key': public_key,
                            'address': address,
                            'puzzle_bits': bits,
                            'attempts': total_attempts,
                            'time_elapsed': elapsed,
                            'keys_per_second': keys_checked / elapsed if elapsed > 0 else 0,
                            'timestamp': datetime.now().isoformat(),
                            'solved': True
                        }
                    
                    # Progress reporting and checkpointing
                    if keys_checked % 10000 == 0:
                        elapsed = time.time() - start_time
                        rate = keys_checked / elapsed if elapsed > 0 else 0
                        self.logger.info(f"Progress: {total_attempts:,} attempts ({rate:.0f} keys/sec) - {elapsed:.1f}s")
                    
                    # Periodic checkpoint save
                    current_time = time.time()
                    if current_time - last_checkpoint_time >= checkpoint_interval:
                        save_checkpoint(current_key, total_attempts)
                        last_checkpoint_time = current_time
                    
                    # Timeout check
                    if time.time() - start_time > timeout:
                        self.logger.warning(f"Timeout reached after {timeout} seconds")
                        break
                
                except Exception as e:
                    self.logger.debug(f"Error generating key: {e}")
                    current_key += 1  # Skip invalid key and continue
                    continue
            
            # Save final checkpoint before exit
            save_checkpoint(current_key, total_attempts)
            
            # Puzzle not solved
            elapsed = time.time() - start_time
            self.logger.info(f"Puzzle not solved after {total_attempts:,} attempts (resumed from {total_attempts_before:,})")
            
            return {
                'private_key': None,
                'public_key': None,
                'address': None,
                'puzzle_bits': bits,
                'attempts': total_attempts,
                'time_elapsed': elapsed,
                'keys_per_second': keys_checked / elapsed if elapsed > 0 else 0,
                'timestamp': datetime.now().isoformat(),
                'solved': False,
                'checkpoint_saved': True,
                'last_key': current_key
            }
        
        except KeyboardInterrupt:
            self.logger.info("Puzzle solving interrupted by user")
            elapsed = time.time() - start_time
            
            # Save checkpoint on interrupt
            save_checkpoint(current_key, total_attempts)
            
            return {
                'private_key': None,
                'public_key': None,
                'address': None,
                'puzzle_bits': bits,
                'attempts': total_attempts,
                'time_elapsed': elapsed,
                'keys_per_second': keys_checked / elapsed if elapsed > 0 else 0,
                'timestamp': datetime.now().isoformat(),
                'solved': False,
                'interrupted': True,
                'checkpoint_saved': True,
                'last_key': current_key
            }
    
    def test_brainwallet_security(self, patterns=None, max_attempts=100000):
        """
        Test brainwallet security against common patterns.
        
        Args:
            patterns (list, optional): Custom patterns to test
            max_attempts (int): Maximum attempts per pattern
        
        Returns:
            dict: Security test results
        """
        self.logger.info("Starting brainwallet security test")
        
        if patterns is None:
            # Use default patterns
            patterns = [
                "password",
                "password123",
                "123456",
                "qwerty",
                "bitcoin",
                "wallet",
                "secret",
                "MyPassword123",
                "BitcoinWallet",
                "CryptoKey2024"
            ]
        
        results = {
            'patterns_tested': len(patterns),
            'total_attempts': 0,
            'vulnerable_patterns': [],
            'security_summary': {},
            'timestamp': datetime.now().isoformat()
        }
        
        for pattern in patterns:
            self.logger.info(f"Testing pattern: '{pattern}'")
            
            try:
                # Generate brainwallet private key
                private_key = hashlib.sha256(pattern.encode()).hexdigest()
                
                # Generate address
                public_key = self.bitcoin_crypto.private_key_to_public_key(private_key)
                address = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                
                # Assess security
                security_score = self._assess_pattern_security(pattern)
                
                pattern_result = {
                    'pattern': pattern,
                    'private_key': private_key,
                    'address': address,
                    'security_score': security_score,
                    'is_vulnerable': security_score < 50
                }
                
                results['security_summary'][pattern] = pattern_result
                
                if security_score < 50:
                    results['vulnerable_patterns'].append(pattern_result)
                    self.logger.warning(f"VULNERABLE: '{pattern}' (score: {security_score})")
                else:
                    self.logger.info(f"Secure: '{pattern}' (score: {security_score})")
                
                results['total_attempts'] += 1
                
            except Exception as e:
                self.logger.error(f"Error testing pattern '{pattern}': {e}")
                continue
        
        # Summary
        vulnerable_count = len(results['vulnerable_patterns'])
        self.logger.info(f"Security test complete: {vulnerable_count}/{len(patterns)} patterns vulnerable")
        
        return results
    
    def _assess_pattern_security(self, pattern):
        """
        Assess the security of a brainwallet pattern.
        
        Args:
            pattern (str): The pattern to assess
        
        Returns:
            int: Security score (0-100, higher is better)
        """
        score = 100
        
        # Length penalty
        if len(pattern) < 8:
            score -= 30
        elif len(pattern) < 12:
            score -= 15
        
        # Character variety bonus/penalty
        has_upper = any(c.isupper() for c in pattern)
        has_lower = any(c.islower() for c in pattern)
        has_digit = any(c.isdigit() for c in pattern)
        has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in pattern)
        
        char_types = sum([has_upper, has_lower, has_digit, has_special])
        if char_types < 3:
            score -= 20
        elif char_types == 4:
            score += 10
        
        # Common patterns penalty
        common_patterns = [
            "password", "123456", "qwerty", "abc123", "admin",
            "bitcoin", "wallet", "crypto", "secret", "key"
        ]
        
        pattern_lower = pattern.lower()
        for common in common_patterns:
            if common in pattern_lower:
                score -= 25
                break
        
        # Sequential patterns penalty
        if self._has_sequential_chars(pattern):
            score -= 15
        
        # Dictionary words penalty
        if self._is_dictionary_word(pattern_lower):
            score -= 20
        
        return max(0, min(100, score))
    
    def _has_sequential_chars(self, pattern):
        """Check if pattern has sequential characters."""
        for i in range(len(pattern) - 2):
            if (ord(pattern[i+1]) == ord(pattern[i]) + 1 and 
                ord(pattern[i+2]) == ord(pattern[i]) + 2):
                return True
        return False
    
    def _is_dictionary_word(self, pattern):
        """Check if pattern is a common dictionary word."""
        # Simple dictionary check - in real implementation, use proper dictionary
        dictionary_words = [
            "password", "admin", "user", "login", "secret", "key",
            "bitcoin", "wallet", "crypto", "money", "bank", "account"
        ]
        return pattern in dictionary_words
    
    def get_performance_stats(self):
        """Get current performance statistics."""
        elapsed = time.time() - self.start_time
        
        return {
            'uptime': elapsed,
            'keys_generated': self.keys_generated,
            'keys_per_second': self.keys_generated / elapsed if elapsed > 0 else 0,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_system_info(self):
        """Get system information and capabilities."""
        import platform
        import psutil
        
        return {
            'platform': platform.platform(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'memory_total': psutil.virtual_memory().total,
            'memory_available': psutil.virtual_memory().available,
            'disk_usage': psutil.disk_usage('/').percent,
            'features': {
                'bitcoin_crypto': bool(self.bitcoin_crypto),
                'pattern_library': bool(self.pattern_library),
                'gpu_available': False,  # Simplified version
                'distributed_available': False,  # Simplified version
                'ml_available': False  # Simplified version
            }
        }

def main():
    """Main function for testing SimpleKeyHound."""
    print("KeyHound Enhanced - Simplified Core")
    print("=" * 40)
    
    # Initialize
    keyhound = SimpleKeyHound(verbose=True)
    
    # Show system info
    system_info = keyhound.get_system_info()
    print(f"Platform: {system_info['platform']}")
    print(f"CPU Cores: {system_info['cpu_count']}")
    print(f"Memory: {system_info['memory_total'] / (1024**3):.1f} GB")
    
    # Test brainwallet security - PHASED OUT
    print("\nBrainwallet security testing: PHASED OUT")
    print("Reason: No high-value brainwallet targets found in comprehensive scan")
    print("Focus: KeyHound now optimized for puzzle solving and core Bitcoin cryptography")
    
    # # Test brainwallet security
    # print("\nTesting brainwallet security...")
    # security_results = keyhound.test_brainwallet_security()
    # 
    # print(f"Patterns tested: {security_results['patterns_tested']}")
    # print(f"Vulnerable patterns: {len(security_results['vulnerable_patterns'])}")
    # 
    # # Show vulnerable patterns
    # if security_results['vulnerable_patterns']:
    #     print("\nVulnerable patterns:")
    #     for pattern in security_results['vulnerable_patterns']:
    #         print(f"  - '{pattern['pattern']}' (score: {pattern['security_score']})")
    
    # Test puzzle solving (small puzzle for demo)
    print("\nTesting puzzle solving (40-bit demo)...")
    result = keyhound.solve_puzzle(bits=40, max_attempts=100000, timeout=30)
    
    if result['solved']:
        print(f"PUZZLE SOLVED!")
        print(f"Private Key: {result['private_key']}")
        print(f"Address: {result['address']}")
    else:
        print(f"Puzzle not solved after {result['attempts']:,} attempts")
        print(f"Performance: {result['keys_per_second']:.0f} keys/sec")
    
    # Performance stats
    stats = keyhound.get_performance_stats()
    print(f"\nPerformance Stats:")
    print(f"Uptime: {stats['uptime']:.1f} seconds")
    print(f"Keys generated: {stats['keys_generated']:,}")
    print(f"Overall rate: {stats['keys_per_second']:.0f} keys/sec")

if __name__ == "__main__":
    main()
