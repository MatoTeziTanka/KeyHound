#!/usr/bin/env python3
"""
GSMG.IO 5 BTC Puzzle Solver
============================

Specialized solver for the GSMG.IO Bitcoin puzzle challenge.
Incorporates coordinate data and visual pattern analysis.

Puzzle Details:
- Address: 1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe
- Prize: 1.5 BTC (reduced from 5 BTC)
- Status: UNSOLVED since April 13, 2019
- Coordinates: 1.25358768, 8.75712266, 34

Author: KeyHound Enhanced
Date: 2025-01-14
"""

import hashlib
import secrets
import time
from datetime import datetime
from typing import Dict, Any, List, Optional
import json

class GSMGPuzzleSolver:
    """Specialized solver for GSMG.IO puzzle challenge."""
    
    def __init__(self):
        self.target_address = "1GSMG1JC9wtdSwfwApgj2xcmJPAwx7prBe"
        self.coordinates = {
            'lat': 1.25358768,
            'lon': 8.75712266,
            'alt': 34
        }
        self.start_time = time.time()
        self.keys_checked = 0
        
        # Import KeyHound components
        try:
            from core.simple_keyhound import SimpleKeyHound
            from core.bitcoin_crypto import BitcoinCrypto
            self.keyhound = SimpleKeyHound(verbose=False)
            self.bitcoin_crypto = BitcoinCrypto()
        except ImportError as e:
            print(f"Error importing KeyHound components: {e}")
            raise
    
    def analyze_coordinates(self) -> Dict[str, Any]:
        """Analyze the provided coordinates for cryptographic patterns."""
        print("🔍 Analyzing GSMG.IO puzzle coordinates...")
        
        lat, lon, alt = self.coordinates['lat'], self.coordinates['lon'], self.coordinates['alt']
        
        # Convert to various formats
        coord_analysis = {
            'raw': {'lat': lat, 'lon': lon, 'alt': alt},
            'hex': {
                'lat_hex': hex(int(lat * 100000000))[2:],  # 8 decimal places
                'lon_hex': hex(int(lon * 100000000))[2:],
                'alt_hex': hex(alt)[2:]
            },
            'combined': {
                'concat': f"{int(lat*100000000)}{int(lon*100000000)}{alt}",
                'concat_hex': hex(int(f"{int(lat*100000000)}{int(lon*100000000)}{alt}"))[2:]
            },
            'hashes': {}
        }
        
        # Generate various hash combinations
        coord_string = f"{lat},{lon},{alt}"
        coord_analysis['hashes'] = {
            'sha256': hashlib.sha256(coord_string.encode()).hexdigest(),
            'md5': hashlib.md5(coord_string.encode()).hexdigest(),
            'sha1': hashlib.sha1(coord_string.encode()).hexdigest()
        }
        
        print(f"📍 Coordinate Analysis:")
        print(f"   Raw: {lat}, {lon}, {alt}")
        print(f"   Hex: {coord_analysis['hex']['lat_hex']}, {coord_analysis['hex']['lon_hex']}, {coord_analysis['hex']['alt_hex']}")
        print(f"   Combined: {coord_analysis['combined']['concat']}")
        print(f"   SHA256: {coord_analysis['hashes']['sha256'][:32]}...")
        
        return coord_analysis
    
    def generate_coordinate_based_keys(self, analysis: Dict[str, Any], count: int = 1000) -> List[str]:
        """Generate private keys based on coordinate analysis."""
        print(f"🔑 Generating {count} coordinate-based private keys...")
        
        keys = []
        base_data = analysis['combined']['concat']
        
        for i in range(count):
            # Method 1: Direct coordinate conversion
            coord_key = hex(int(base_data) + i)[2:].zfill(64)
            keys.append(coord_key)
            
            # Method 2: Hash-based generation
            hash_input = f"{base_data}_{i}_{datetime.now().timestamp()}"
            hash_key = hashlib.sha256(hash_input.encode()).hexdigest()
            keys.append(hash_key)
            
            # Method 3: Coordinate multiplication
            mult_key = hex(int(base_data) * (i + 1))[2:].zfill(64)
            keys.append(mult_key)
        
        return keys[:count]
    
    def solve_gsmg_puzzle(self, max_attempts: int = 1000000, timeout: int = 3600) -> Dict[str, Any]:
        """Main puzzle solving function with multiple strategies."""
        print("🎯 Starting GSMG.IO 5 BTC Puzzle Solver...")
        print(f"📍 Target Address: {self.target_address}")
        print(f"💰 Prize: 1.5 BTC")
        print("=" * 60)
        
        # Analyze coordinates first
        coord_analysis = self.analyze_coordinates()
        
        # Strategy 1: Coordinate-based key generation
        print("\n🔍 Strategy 1: Coordinate-based private keys")
        coord_keys = self.generate_coordinate_based_keys(coord_analysis, 10000)
        result = self._test_keys_batch(coord_keys, "coordinate-based")
        if result['solved']:
            return result
        
        # Strategy 2: Sequential range search around coordinate values
        print("\n🔍 Strategy 2: Sequential range search")
        result = self._sequential_range_search(coord_analysis, max_attempts // 4, timeout // 4)
        if result['solved']:
            return result
        
        # Strategy 3: Pattern-based generation (rabbit symbol analysis)
        print("\n🔍 Strategy 3: Pattern-based generation")
        result = self._pattern_based_search(coord_analysis, max_attempts // 4, timeout // 4)
        if result['solved']:
            return result
        
        # Strategy 4: Random brute force with coordinate seed
        print("\n🔍 Strategy 4: Seeded random search")
        result = self._seeded_random_search(coord_analysis, max_attempts // 4, timeout // 4)
        if result['solved']:
            return result
        
        # No solution found
        elapsed = time.time() - self.start_time
        return {
            'solved': False,
            'target_address': self.target_address,
            'attempts': self.keys_checked,
            'time_elapsed': elapsed,
            'keys_per_second': self.keys_checked / elapsed if elapsed > 0 else 0,
            'timestamp': datetime.now().isoformat(),
            'strategies_tested': 4,
            'message': 'GSMG.IO puzzle remains unsolved after comprehensive analysis'
        }
    
    def _test_keys_batch(self, keys: List[str], strategy_name: str) -> Dict[str, Any]:
        """Test a batch of keys for the target address."""
        print(f"   Testing {len(keys)} {strategy_name} keys...")
        
        for i, private_key in enumerate(keys):
            try:
                # Ensure key is 64 hex characters
                if len(private_key) < 64:
                    private_key = private_key.zfill(64)
                elif len(private_key) > 64:
                    private_key = private_key[:64]
                
                # Generate address
                address = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                self.keys_checked += 1
                
                # Check for match
                if address == self.target_address:
                    elapsed = time.time() - self.start_time
                    print(f"🎉 PUZZLE SOLVED! Found GSMG.IO private key!")
                    print(f"🔑 Private Key: {private_key}")
                    print(f"📍 Address: {address}")
                    print(f"⚡ Strategy: {strategy_name}")
                    print(f"⏱️ Time: {elapsed:.2f} seconds")
                    
                    return {
                        'solved': True,
                        'private_key': private_key,
                        'address': address,
                        'strategy': strategy_name,
                        'attempts': self.keys_checked,
                        'time_elapsed': elapsed,
                        'keys_per_second': self.keys_checked / elapsed,
                        'timestamp': datetime.now().isoformat(),
                        'message': 'GSMG.IO 5 BTC puzzle SOLVED!'
                    }
                
                # Progress update
                if i % 1000 == 0 and i > 0:
                    print(f"     Checked {i:,} keys...")
                    
            except Exception as e:
                continue
        
        return {'solved': False}
    
    def _sequential_range_search(self, analysis: Dict[str, Any], max_attempts: int, timeout: int) -> Dict[str, Any]:
        """Sequential search around coordinate-derived values."""
        print(f"   Sequential search: {max_attempts:,} attempts, {timeout}s timeout")
        
        base_value = int(analysis['combined']['concat'])
        start_time = time.time()
        
        for i in range(max_attempts):
            # Try values around the coordinate base
            test_value = base_value + i
            private_key = hex(test_value)[2:].zfill(64)
            
            try:
                address = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                self.keys_checked += 1
                
                if address == self.target_address:
                    elapsed = time.time() - self.start_time
                    return {
                        'solved': True,
                        'private_key': private_key,
                        'address': address,
                        'strategy': 'sequential_range',
                        'attempts': self.keys_checked,
                        'time_elapsed': elapsed,
                        'keys_per_second': self.keys_checked / elapsed,
                        'timestamp': datetime.now().isoformat()
                    }
                
                if time.time() - start_time > timeout:
                    break
                    
            except Exception:
                continue
        
        return {'solved': False}
    
    def _pattern_based_search(self, analysis: Dict[str, Any], max_attempts: int, timeout: int) -> Dict[str, Any]:
        """Pattern-based search incorporating visual elements (rabbit, grid)."""
        print(f"   Pattern search: {max_attempts:,} attempts, {timeout}s timeout")
        
        # Rabbit symbol could represent various cryptographic patterns
        rabbit_patterns = [
            "rabbit", "bunny", "hare", "lapin", "coniglio", "conejo",
            "🐰", "🐇", "rabbit1", "rabbit2", "bunny1", "bunny2"
        ]
        
        base_hash = analysis['hashes']['sha256']
        start_time = time.time()
        
        for i in range(max_attempts):
            for pattern in rabbit_patterns:
                # Combine pattern with coordinates
                test_input = f"{pattern}_{analysis['combined']['concat']}_{i}"
                private_key = hashlib.sha256(test_input.encode()).hexdigest()
                
                try:
                    address = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                    self.keys_checked += 1
                    
                    if address == self.target_address:
                        elapsed = time.time() - self.start_time
                        return {
                            'solved': True,
                            'private_key': private_key,
                            'address': address,
                            'strategy': 'pattern_based',
                            'attempts': self.keys_checked,
                            'time_elapsed': elapsed,
                            'keys_per_second': self.keys_checked / elapsed,
                            'timestamp': datetime.now().isoformat()
                        }
                    
                    if time.time() - start_time > timeout:
                        return {'solved': False}
                        
                except Exception:
                    continue
        
        return {'solved': False}
    
    def _seeded_random_search(self, analysis: Dict[str, Any], max_attempts: int, timeout: int) -> Dict[str, Any]:
        """Random search seeded with coordinate data."""
        print(f"   Seeded random search: {max_attempts:,} attempts, {timeout}s timeout")
        
        # Use coordinates as seed for more deterministic randomness
        seed = int(analysis['combined']['concat']) % (2**32)
        secrets.seed = seed
        
        start_time = time.time()
        
        for i in range(max_attempts):
            # Generate random key with coordinate influence
            random_part = secrets.randbelow(2**256)
            coord_part = int(analysis['combined']['concat'])
            private_key_int = (random_part ^ coord_part) % (2**256)
            private_key = hex(private_key_int)[2:].zfill(64)
            
            try:
                address = self.bitcoin_crypto.generate_bitcoin_address(private_key)
                self.keys_checked += 1
                
                if address == self.target_address:
                    elapsed = time.time() - self.start_time
                    return {
                        'solved': True,
                        'private_key': private_key,
                        'address': address,
                        'strategy': 'seeded_random',
                        'attempts': self.keys_checked,
                        'time_elapsed': elapsed,
                        'keys_per_second': self.keys_checked / elapsed,
                        'timestamp': datetime.now().isoformat()
                    }
                
                if time.time() - start_time > timeout:
                    break
                    
            except Exception:
                continue
        
        return {'solved': False}
    
    def save_results(self, results: Dict[str, Any]) -> str:
        """Save results to file."""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"gsmg_puzzle_attempt_{timestamp}.json"
        
        with open(filename, 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Results saved to: {filename}")
        return filename

def main():
    """Main execution function."""
    print("🔑 GSMG.IO 5 BTC Puzzle Solver")
    print("=" * 50)
    
    try:
        solver = GSMGPuzzleSolver()
        results = solver.solve_gsmg_puzzle(max_attempts=1000000, timeout=3600)
        
        print("\n" + "=" * 60)
        print("📊 FINAL RESULTS")
        print("=" * 60)
        
        if results['solved']:
            print("🎉 SUCCESS! GSMG.IO puzzle SOLVED!")
            print(f"🔑 Private Key: {results['private_key']}")
            print(f"📍 Address: {results['address']}")
            print(f"💰 Prize: 1.5 BTC")
            print(f"⚡ Strategy: {results.get('strategy', 'unknown')}")
            print(f"⏱️ Time: {results['time_elapsed']:.2f} seconds")
            print(f"🔢 Keys checked: {results['attempts']:,}")
            print(f"🚀 Rate: {results['keys_per_second']:.0f} keys/sec")
        else:
            print("⏳ Puzzle remains unsolved")
            print(f"🔢 Total keys checked: {results['attempts']:,}")
            print(f"⏱️ Total time: {results['time_elapsed']:.2f} seconds")
            print(f"🚀 Average rate: {results['keys_per_second']:.0f} keys/sec")
            print(f"📋 Strategies tested: {results.get('strategies_tested', 'unknown')}")
        
        # Save results
        solver.save_results(results)
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
