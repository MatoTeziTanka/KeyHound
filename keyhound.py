#!/usr/bin/env python3
"""
KeyHound - Bitcoin Challenge Solver

A cross-platform Python application designed to help tackle the remaining
1000 Bitcoin puzzle challenges with CPU and optional GPU acceleration.
"""

import hashlib
import time
import argparse
import sys
from typing import Optional, Tuple
import multiprocessing as mp
from tqdm import tqdm
import colorama
from colorama import Fore, Style

# Initialize colorama for cross-platform colored output
colorama.init()


class BitcoinChallengeSolver:
    """Main class for Bitcoin challenge solving operations."""
    
    def __init__(self, use_gpu: bool = False, num_threads: Optional[int] = None):
        """
        Initialize the Bitcoin Challenge Solver.
        
        Args:
            use_gpu: Whether to use GPU acceleration (if available)
            num_threads: Number of CPU threads to use (default: all available)
        """
        self.use_gpu = use_gpu
        self.num_threads = num_threads or mp.cpu_count()
        self.start_time = None
        
        print(f"{Fore.CYAN}KeyHound - Bitcoin Challenge Solver{Style.RESET_ALL}")
        print(f"{Fore.YELLOW}Initializing with {self.num_threads} CPU threads{Style.RESET_ALL}")
        
        if use_gpu:
            print(f"{Fore.GREEN}GPU acceleration enabled{Style.RESET_ALL}")
            # TODO: Add GPU initialization code
        else:
            print(f"{Fore.BLUE}CPU-only mode{Style.RESET_ALL}")
    
    def solve_challenge(self, challenge_range: Tuple[int, int], 
                       target_hash: str = None) -> Optional[str]:
        """
        Solve a Bitcoin challenge within the given range.
        
        Args:
            challenge_range: Tuple of (start, end) range to search
            target_hash: Optional target hash to find
            
        Returns:
            Private key if found, None otherwise
        """
        start, end = challenge_range
        print(f"{Fore.CYAN}Searching range: {start} to {end}{Style.RESET_ALL}")
        
        if target_hash:
            print(f"{Fore.YELLOW}Target hash: {target_hash}{Style.RESET_ALL}")
        
        self.start_time = time.time()
        
        # Create progress bar
        total_keys = end - start
        with tqdm(total=total_keys, desc="Searching", unit="keys") as pbar:
            for private_key in range(start, end):
                # Generate Bitcoin address from private key
                address = self._generate_address(private_key)
                
                # Check if this matches our target (if provided)
                if target_hash and self._check_hash(address, target_hash):
                    elapsed = time.time() - self.start_time
                    print(f"\n{Fore.GREEN}Found match!{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Private Key: {private_key}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Address: {address}{Style.RESET_ALL}")
                    print(f"{Fore.GREEN}Time elapsed: {elapsed:.2f} seconds{Style.RESET_ALL}")
                    return str(private_key)
                
                pbar.update(1)
                
                # Update progress bar with current key
                pbar.set_postfix({
                    'Current': private_key,
                    'Rate': f"{pbar.n / elapsed:.0f}/s" if self.start_time else "0/s"
                })
        
        print(f"\n{Fore.RED}No match found in range {start}-{end}{Style.RESET_ALL}")
        return None
    
    def _generate_address(self, private_key: int) -> str:
        """
        Generate a Bitcoin address from a private key.
        
        Args:
            private_key: The private key as an integer
            
        Returns:
            Bitcoin address string
        """
        # Convert private key to hex
        private_key_hex = hex(private_key)[2:].zfill(64)
        
        # For now, return a simplified hash-based address
        # In a real implementation, this would generate proper Bitcoin addresses
        address_hash = hashlib.sha256(private_key_hex.encode()).hexdigest()
        return f"1{address_hash[:26]}"  # Simplified Bitcoin address format
    
    def _check_hash(self, address: str, target_hash: str) -> bool:
        """
        Check if an address matches the target hash.
        
        Args:
            address: Generated Bitcoin address
            target_hash: Target hash to match
            
        Returns:
            True if match found, False otherwise
        """
        # For demonstration, we'll do a simple hash comparison
        # In a real implementation, this would check against actual Bitcoin puzzle hashes
        return hashlib.sha256(address.encode()).hexdigest() == target_hash
    
    def benchmark(self, test_range: Tuple[int, int]) -> dict:
        """
        Run a benchmark test to measure performance.
        
        Args:
            test_range: Range of keys to test
            
        Returns:
            Dictionary with benchmark results
        """
        print(f"{Fore.CYAN}Running benchmark on range {test_range[0]}-{test_range[1]}...{Style.RESET_ALL}")
        
        start_time = time.time()
        start, end = test_range
        
        for i in range(start, min(start + 1000, end)):  # Test first 1000 keys
            self._generate_address(i)
        
        elapsed = time.time() - start_time
        keys_per_second = 1000 / elapsed
        
        results = {
            'keys_tested': min(1000, end - start),
            'time_elapsed': elapsed,
            'keys_per_second': keys_per_second,
            'estimated_full_range_time': (end - start) / keys_per_second if keys_per_second > 0 else float('inf')
        }
        
        print(f"{Fore.GREEN}Benchmark Results:{Style.RESET_ALL}")
        print(f"  Keys tested: {results['keys_tested']}")
        print(f"  Time elapsed: {results['time_elapsed']:.2f} seconds")
        print(f"  Keys per second: {results['keys_per_second']:.0f}")
        print(f"  Estimated time for full range: {results['estimated_full_range_time']:.2f} seconds")
        
        return results


def main():
    """Main entry point for the KeyHound application."""
    parser = argparse.ArgumentParser(
        description="KeyHound - Bitcoin Challenge Solver",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python keyhound.py --range 1 1000000
  python keyhound.py --range 1000000 2000000 --target abc123...
  python keyhound.py --benchmark --range 1 10000
  python keyhound.py --gpu --threads 8
        """
    )
    
    parser.add_argument(
        '--range', 
        nargs=2, 
        type=int, 
        metavar=('START', 'END'),
        help='Range of private keys to search (start end)'
    )
    
    parser.add_argument(
        '--target',
        type=str,
        help='Target hash to find (optional)'
    )
    
    parser.add_argument(
        '--gpu',
        action='store_true',
        help='Enable GPU acceleration (if available)'
    )
    
    parser.add_argument(
        '--threads',
        type=int,
        help='Number of CPU threads to use (default: all available)'
    )
    
    parser.add_argument(
        '--benchmark',
        action='store_true',
        help='Run benchmark test instead of solving'
    )
    
    args = parser.parse_args()
    
    try:
        # Initialize solver
        solver = BitcoinChallengeSolver(
            use_gpu=args.gpu,
            num_threads=args.threads
        )
        
        if args.benchmark:
            if not args.range:
                print(f"{Fore.RED}Error: --benchmark requires --range{Style.RESET_ALL}")
                sys.exit(1)
            
            results = solver.benchmark((args.range[0], args.range[1]))
            
        elif args.range:
            result = solver.solve_challenge(
                (args.range[0], args.range[1]),
                args.target
            )
            
            if result:
                print(f"\n{Fore.GREEN}Solution found: {result}{Style.RESET_ALL}")
            else:
                print(f"\n{Fore.YELLOW}No solution found in the specified range{Style.RESET_ALL}")
        
        else:
            # Interactive mode
            print(f"{Fore.CYAN}Interactive mode - enter ranges to search{Style.RESET_ALL}")
            print("Type 'quit' to exit")
            
            while True:
                try:
                    user_input = input("\nEnter range (start end) or 'quit': ").strip()
                    
                    if user_input.lower() == 'quit':
                        break
                    
                    parts = user_input.split()
                    if len(parts) == 2:
                        start, end = int(parts[0]), int(parts[1])
                        solver.solve_challenge((start, end))
                    else:
                        print(f"{Fore.RED}Invalid input. Please enter two numbers separated by space{Style.RESET_ALL}")
                        
                except KeyboardInterrupt:
                    print(f"\n{Fore.YELLOW}Exiting...{Style.RESET_ALL}")
                    break
                except ValueError:
                    print(f"{Fore.RED}Invalid input. Please enter valid numbers{Style.RESET_ALL}")
    
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}Operation cancelled by user{Style.RESET_ALL}")
        sys.exit(0)
    except Exception as e:
        print(f"{Fore.RED}Error: {e}{Style.RESET_ALL}")
        sys.exit(1)


if __name__ == "__main__":
    main()
