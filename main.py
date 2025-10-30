#!/usr/bin/env python3
"""
KeyHound Enhanced - Main Entry Point
Bitcoin cryptography platform for puzzle solving and challenge monitoring.
"""

import sys
import os
import time
from typing import Optional, Dict
import argparse
from pathlib import Path

# Add current directory to Python path for local imports
sys.path.insert(0, str(Path(__file__).parent))

def main():
    """Main entry point for KeyHound Enhanced"""
    parser = argparse.ArgumentParser(
        description="KeyHound Enhanced - Bitcoin Cryptography Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --web                    # Start web interface
  python main.py --puzzle 66             # Solve 66-bit puzzle
  # python main.py --brainwallet-test      # PHASED OUT: No high-value brainwallets found
  python main.py --gpu --puzzle 40       # GPU-accelerated solving
  python main.py --monitor-challenges    # Monitor Bitcoin challenge addresses
        """
    )
    
    parser.add_argument('--web', action='store_true',
                       help='Start web interface dashboard')
    parser.add_argument('--puzzle', type=int, metavar='BITS',
                       help='Solve Bitcoin puzzle with specified bit length (overrides env PUZZLE_BITS)')
    # parser.add_argument('--brainwallet-test', action='store_true',
    #                    help='Test brainwallet security')  # PHASED OUT: No high-value brainwallets found
    parser.add_argument('--gpu', action='store_true',
                       help='Enable GPU acceleration')
    parser.add_argument('--distributed', action='store_true',
                       help='Enable distributed computing')
    parser.add_argument('--monitor-challenges', action='store_true',
                       help='Monitor Bitcoin challenge addresses and test notifications')
    parser.add_argument('--config', type=str, default='../config/default.yaml',
                       help='Configuration file path')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Logging level')
    
    args = parser.parse_args()
    
    def resolve_puzzle_bits(cli_bits: Optional[int]) -> int:
        """Resolve which puzzle bits to target based on CLI, env, and auto-selection.

        Rules:
        - If CLI provides --puzzle, use it.
        - Else if env PUZZLE_BITS provided and not 'auto', use it.
        - Else auto-select the first unsolved from a prioritized list (skips known solved like 66).
        - If live balance check fails, fall back to the first candidate (67).
        """
        if cli_bits is not None:
            return int(cli_bits)

        env_val = os.environ.get('PUZZLE_BITS', '').strip()
        if env_val and env_val.lower() != 'auto':
            try:
                return int(env_val)
            except ValueError:
                pass

        # Prioritized candidates (easiest first). 66 is known solved; start at 67.
        candidates = [67, 68, 69, 70, 71, 72, 73, 74, 75]

        # Optional live check: consider an address has balance => unsolved (targetable)
        addr_by_bits: Dict[int, str] = {
            66: '13zb1hQbWVsc2S7ZTZnP2G4undNNpdh5so',
            67: '1BY8GQbnueYofwSuFAT3USAhGjPrkxDdW9',
            # Add additional known addresses as needed
        }
        try:
            import requests  # lightweight; present in requirements
            for bits in candidates:
                addr = addr_by_bits.get(bits)
                if not addr:
                    # If we do not know the address, assume unsolved and return it
                    return bits
                # Query a public API with tight timeout
                r = requests.get(
                    f'https://api.blockcypher.com/v1/btc/main/addrs/{addr}/balance', timeout=3
                )
                if r.ok:
                    data = r.json()
                    # balance or unconfirmed_balance > 0 implies still unclaimed/funded
                    if (data.get('balance', 0) + data.get('unconfirmed_balance', 0)) > 0:
                        return bits
            # If none marked with balance, default to the first candidate
            return candidates[0]
        except Exception:
            # Network not available or API changed; pick the first candidate
            return candidates[0]

    try:
        if args.web:
            from web.web_interface import start_web_interface
            start_web_interface()
        elif args.puzzle is not None or os.environ.get('PUZZLE_BITS') is not None:
            target_bits = resolve_puzzle_bits(args.puzzle)
            print(f"Selected target puzzle: {target_bits}-bit (source: {'CLI' if args.puzzle is not None else os.environ.get('PUZZLE_BITS','auto')})")
            # Always try GPU-enabled version first (auto-detects and falls back to CPU)
            try:
                from core.gpu_enabled_keyhound import GPUEnabledKeyHound
                print("Attempting to use GPU-enabled KeyHound (auto-detects GPU availability)...")
                keyhound = GPUEnabledKeyHound(use_gpu=args.gpu, gpu_framework="cuda")
                if args.distributed:
                    print("Distributed computing requested but not implemented in GPU version")
                keyhound.solve_puzzle(target_bits)
            except ImportError:
                # Fallback to simple version if GPU version not available
                print("GPU-enabled version not available, using simple version...")
                from core.simple_keyhound import SimpleKeyHound
                keyhound = SimpleKeyHound()
                if args.distributed:
                    print("Distributed computing requested but not implemented in simple version")
                keyhound.solve_puzzle(target_bits)
        # elif args.brainwallet_test:
        #     from core.keyhound_enhanced import KeyHoundEnhanced
        #     keyhound = KeyHoundEnhanced(config_file=args.config)
        #     keyhound.test_brainwallet_security()  # PHASED OUT: No high-value brainwallets found
        elif args.monitor_challenges:
            from core.simple_challenge_monitor import SimpleChallengeMonitor
            monitor = SimpleChallengeMonitor()
            results = monitor.check_solved_addresses()
            monitor.save_results(results)
        else:
            parser.print_help()
            
    except ImportError as e:
        print(f"Error importing module: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()