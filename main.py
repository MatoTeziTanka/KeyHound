#!/usr/bin/env python3
"""
KeyHound Enhanced - Production Entry Point
Enterprise-grade Bitcoin cryptography and puzzle solving platform
"""

import sys
import os
import argparse
from pathlib import Path

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent / "src"))

def main():
    """Main entry point for KeyHound Enhanced"""
    parser = argparse.ArgumentParser(
        description="KeyHound Enhanced - Bitcoin Cryptography Platform",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py --web                    # Start web interface
  python main.py --puzzle 66             # Solve 66-bit puzzle
  python main.py --brainwallet-test      # Test brainwallet security
  python main.py --gpu --puzzle 40       # GPU-accelerated solving
        """
    )
    
    parser.add_argument('--web', action='store_true',
                       help='Start web interface dashboard')
    parser.add_argument('--puzzle', type=int, metavar='BITS',
                       help='Solve Bitcoin puzzle with specified bit length')
    parser.add_argument('--brainwallet-test', action='store_true',
                       help='Test brainwallet security')
    parser.add_argument('--gpu', action='store_true',
                       help='Enable GPU acceleration')
    parser.add_argument('--distributed', action='store_true',
                       help='Enable distributed computing')
    parser.add_argument('--config', type=str, default='config/default.yaml',
                       help='Configuration file path')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
                       default='INFO', help='Logging level')
    
    args = parser.parse_args()
    
    try:
        if args.web:
            from web.web_interface import start_web_interface
            start_web_interface()
        elif args.puzzle:
            from core.keyhound_enhanced import KeyHoundEnhanced
            keyhound = KeyHoundEnhanced(config_file=args.config)
            if args.gpu:
                keyhound.enable_gpu_acceleration()
            if args.distributed:
                keyhound.enable_distributed_computing()
            keyhound.solve_puzzle(args.puzzle)
        elif args.brainwallet_test:
            from core.keyhound_enhanced import KeyHoundEnhanced
            keyhound = KeyHoundEnhanced(config_file=args.config)
            keyhound.test_brainwallet_security()
        else:
            parser.print_help()
            
    except ImportError as e:
        print(f"Error importing module: {e}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
