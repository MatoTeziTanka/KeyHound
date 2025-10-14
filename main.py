#!/usr/bin/env python3
"""
KeyHound Enhanced - Main Entry Point
Bitcoin cryptography platform for puzzle solving and challenge monitoring.
"""

import sys
import os
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
                       help='Solve Bitcoin puzzle with specified bit length')
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
    
    try:
        if args.web:
            from web.web_interface import start_web_interface
            start_web_interface()
        elif args.puzzle:
            # Always try GPU-enabled version first (auto-detects and falls back to CPU)
            try:
                from core.gpu_enabled_keyhound import GPUEnabledKeyHound
                print("Attempting to use GPU-enabled KeyHound (auto-detects GPU availability)...")
                keyhound = GPUEnabledKeyHound(use_gpu=args.gpu, gpu_framework="cuda")
                if args.distributed:
                    print("Distributed computing requested but not implemented in GPU version")
                keyhound.solve_puzzle(args.puzzle)
            except ImportError:
                # Fallback to simple version if GPU version not available
                print("GPU-enabled version not available, using simple version...")
                from core.simple_keyhound import SimpleKeyHound
                keyhound = SimpleKeyHound()
                if args.distributed:
                    print("Distributed computing requested but not implemented in simple version")
                keyhound.solve_puzzle(args.puzzle)
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