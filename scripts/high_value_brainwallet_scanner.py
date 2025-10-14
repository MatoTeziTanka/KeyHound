#!/usr/bin/env python3
"""
KeyHound Enhanced - High-Value Brainwallet Scanner
Focused scanner for brainwallet patterns likely to have significant balances.
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime
import hashlib

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class HighValueBrainwalletScanner:
    """Scans high-probability brainwallet patterns for significant balances."""
    
    def __init__(self, min_balance_usd: float = 100.0):
        self.min_balance_usd = min_balance_usd
        self.btc_price = self._get_bitcoin_price()
        self.results = []
        self.high_value_wallets = []
        
        print(f"High-Value Brainwallet Scanner initialized")
        print(f"Minimum balance threshold: ${min_balance_usd}")
        print(f"Current Bitcoin price: ${self.btc_price:,.2f}")
    
    def _get_bitcoin_price(self) -> float:
        """Get current Bitcoin price in USD."""
        apis = [
            ('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', 'coingecko'),
            ('https://api.coincap.io/v2/assets/bitcoin', 'coincap'),
            ('https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT', 'binance')
        ]
        
        for url, source in apis:
            try:
                response = requests.get(url, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    
                    if source == 'coingecko':
                        return data['bitcoin']['usd']
                    elif source == 'coincap':
                        return float(data['data']['priceUsd'])
                    elif source == 'binance':
                        return float(data['price'])
            except:
                continue
        
        print("Warning: Could not fetch Bitcoin price, using $50,000 as fallback")
        return 50000.0
    
    def _generate_brainwallet_address(self, pattern: str) -> Tuple[str, str]:
        """Generate Bitcoin address from brainwallet pattern."""
        try:
            # Generate private key from pattern using SHA256
            private_key_hex = hashlib.sha256(pattern.encode('utf-8')).hexdigest()
            
            # Import Bitcoin cryptography
            from core.bitcoin_cryptography import BitcoinCryptography
            crypto = BitcoinCryptography()
            
            # Generate address
            public_key = crypto.private_key_to_public_key(private_key_hex)
            address = crypto.generate_bitcoin_address(private_key_hex)
            
            return address, private_key_hex
            
        except Exception as e:
            print(f"Error generating address for '{pattern}': {e}")
            return None, None
    
    def _get_address_balance(self, address: str) -> Tuple[float, float]:
        """Get Bitcoin balance for an address using multiple APIs."""
        apis = [
            f"https://blockstream.info/api/address/{address}",
            f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance",
            f"https://blockchain.info/q/addressbalance/{address}"
        ]
        
        for api_url in apis:
            try:
                response = requests.get(api_url, timeout=15)
                if response.status_code == 200:
                    if 'blockstream.info' in api_url:
                        data = response.json()
                        balance_satoshi = data.get('chain_stats', {}).get('funded_txo_sum', 0) - data.get('chain_stats', {}).get('spent_txo_sum', 0)
                        return balance_satoshi, balance_satoshi / 100000000
                    
                    elif 'blockcypher.com' in api_url:
                        data = response.json()
                        balance_satoshi = data.get('balance', 0)
                        return balance_satoshi, balance_satoshi / 100000000
                    
                    elif 'blockchain.info' in api_url:
                        balance_satoshi = int(response.text)
                        return balance_satoshi, balance_satoshi / 100000000
                
            except Exception:
                continue
        
        return 0.0, 0.0
    
    def _get_high_priority_patterns(self) -> List[str]:
        """Get high-priority brainwallet patterns most likely to have significant balances."""
        
        # Most common passwords that people actually use for important things
        common_passwords = [
            "password", "123456", "password123", "admin", "qwerty", "abc123",
            "123456789", "password1", "welcome", "monkey", "dragon", "master",
            "hello", "freedom", "whatever", "qazwsx", "trustno1", "654321",
            "jordan23", "harley", "hunter", "ranger", "jordan", "jennifer",
            "zxcvbn", "asdfgh", "123123", "qwertyuiop", "solo", "princess",
            "daniel", "mustang", "batman", "summer", "iloveyou", "ashley",
            "000000", "tigger", "sunshine", "charlie", "hockey", "rangers",
            "hannah", "michelle", "andrew", "love", "pepper", "shadow",
            "michael", "blazer", "ferrari", "matrix", "guitar", "tiffany",
            "jessica", "daniel", "banana", "chelsea", "stella", "hokey",
            "lorena", "soccer", "killer", "george", "sexy", "andrew",
            "charlie", "superman", "dallas", "panties", "pepper"
        ]
        
        # Bitcoin-specific patterns that people might use
        bitcoin_patterns = [
            "bitcoin", "btc", "satoshi", "nakamoto", "blockchain", "crypto",
            "wallet", "private", "key", "secret", "password", "passphrase",
            "seed", "mnemonic", "recovery", "backup", "security", "encryption",
            "hash", "mining", "miner", "pool", "exchange", "trading", "hodl",
            "bull", "bear", "market", "price", "value", "coin", "token",
            "ethereum", "eth", "litecoin", "ltc", "dogecoin", "doge"
        ]
        
        # Common phrases and combinations
        phrases = [
            "hello world", "test", "example", "sample", "demo", "password123",
            "mypassword", "secret123", "private123", "key123", "wallet123",
            "bitcoin123", "crypto123", "money", "cash", "rich", "wealthy",
            "millionaire", "billionaire", "invest", "investment", "profit",
            "earn", "income", "salary", "work", "job", "business", "company"
        ]
        
        # Date and time patterns
        dates = [
            "2024", "2025", "2023", "2022", "2021", "2020", "2019", "2018",
            "january", "february", "march", "april", "may", "june", "july",
            "august", "september", "october", "november", "december"
        ]
        
        # Combine and deduplicate
        all_patterns = list(set(common_passwords + bitcoin_patterns + phrases + dates))
        
        # Sort by priority (most common first)
        priority_order = ["password", "123456", "bitcoin", "wallet", "private", "key", "secret"]
        priority_patterns = []
        
        for pattern in priority_order:
            if pattern in all_patterns:
                priority_patterns.append(pattern)
                all_patterns.remove(pattern)
        
        # Add remaining patterns
        return priority_patterns + all_patterns
    
    def scan_high_priority_patterns(self) -> List[Dict[str, Any]]:
        """Scan high-priority brainwallet patterns."""
        patterns = self._get_high_priority_patterns()
        
        print(f"\nScanning {len(patterns)} high-priority brainwallet patterns...")
        print("This will check real Bitcoin balances - please be patient...")
        
        results = []
        
        for i, pattern in enumerate(patterns, 1):
            print(f"[{i:3d}/{len(patterns)}] Scanning: '{pattern}'", end=" ... ")
            
            try:
                # Generate address
                address, private_key = self._generate_brainwallet_address(pattern)
                
                if not address:
                    print("Failed to generate address")
                    continue
                
                # Check balance
                balance_satoshi, balance_btc = self._get_address_balance(address)
                balance_usd = balance_btc * self.btc_price
                
                result = {
                    'pattern': pattern,
                    'address': address,
                    'private_key': private_key,
                    'balance_satoshi': balance_satoshi,
                    'balance_btc': balance_btc,
                    'balance_usd': balance_usd,
                    'meets_threshold': balance_usd >= self.min_balance_usd,
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(result)
                
                if balance_usd > 0:
                    print(f"${balance_usd:,.2f} ({balance_btc:.8f} BTC)")
                    if balance_usd >= self.min_balance_usd:
                        self.high_value_wallets.append(result)
                        print(f"    *** HIGH VALUE FOUND! >= ${self.min_balance_usd} ***")
                else:
                    print("No balance")
                
                # Rate limiting - be respectful to APIs
                time.sleep(2)
                
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        self.results = results
        return results
    
    def get_sorted_high_value_wallets(self) -> List[Dict[str, Any]]:
        """Get high-value wallets sorted by balance (highest first)."""
        high_value = [r for r in self.results if r['meets_threshold']]
        return sorted(high_value, key=lambda x: x['balance_usd'], reverse=True)
    
    def save_results(self, filename: str = None):
        """Save scan results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"high_value_brainwallet_scan_{timestamp}.json"
        
        data = {
            'scan_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_patterns_scanned': len(self.results),
                'min_balance_threshold_usd': self.min_balance_usd,
                'bitcoin_price_usd': self.btc_price,
                'high_value_wallets_found': len(self.high_value_wallets)
            },
            'high_value_wallets_sorted': self.get_sorted_high_value_wallets(),
            'all_results': self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        return filename
    
    def print_high_value_results(self):
        """Print high-value wallet results sorted by balance."""
        high_value = self.get_sorted_high_value_wallets()
        
        print("\n" + "=" * 100)
        print("HIGH-VALUE BRAINWALLET SCAN RESULTS")
        print("=" * 100)
        print(f"Total patterns scanned: {len(self.results)}")
        print(f"Minimum balance threshold: ${self.min_balance_usd}")
        print(f"Bitcoin price: ${self.btc_price:,.2f}")
        print(f"High-value wallets found: {len(high_value)}")
        
        if high_value:
            print(f"\nWALLETS WITH BALANCE >= ${self.min_balance_usd} (Sorted by Balance):")
            print("-" * 100)
            print(f"{'#':<3} {'Balance (USD)':<15} {'Balance (BTC)':<18} {'Pattern':<20} {'Address':<40}")
            print("-" * 100)
            
            for i, wallet in enumerate(high_value, 1):
                balance_usd = wallet['balance_usd']
                balance_btc = wallet['balance_btc']
                pattern = wallet['pattern'][:18] + ".." if len(wallet['pattern']) > 20 else wallet['pattern']
                address = wallet['address'][:37] + ".." if len(wallet['address']) > 40 else wallet['address']
                
                print(f"{i:<3} ${balance_usd:<14,.2f} {balance_btc:<17.8f} {pattern:<20} {address:<40}")
            
            print("-" * 100)
            print(f"\nDETAILED INFORMATION FOR HIGH-VALUE WALLETS:")
            print("-" * 100)
            
            for i, wallet in enumerate(high_value, 1):
                print(f"\n{i}. Pattern: '{wallet['pattern']}'")
                print(f"   Address: {wallet['address']}")
                print(f"   Balance: ${wallet['balance_usd']:,.2f} ({wallet['balance_btc']:.8f} BTC)")
                print(f"   Private Key: {wallet['private_key']}")
        else:
            print(f"\nNo wallets found with balance >= ${self.min_balance_usd}")
        
        print("=" * 100)

def main():
    """Main entry point."""
    print("=" * 100)
    print("KeyHound Enhanced - High-Value Brainwallet Scanner")
    print("=" * 100)
    print("This tool scans brainwallet patterns for Bitcoin balances >= $100")
    print("Results are sorted by balance value (highest first)")
    print("Use responsibly for legitimate security research only.")
    print("=" * 100)
    
    try:
        # Initialize scanner
        scanner = HighValueBrainwalletScanner(min_balance_usd=100.0)
        
        # Scan patterns
        scanner.scan_high_priority_patterns()
        
        # Save results
        filename = scanner.save_results()
        
        # Print results
        scanner.print_high_value_results()
        
        print(f"\nScan complete! Results saved to: {filename}")
        print("Remember: Use this information responsibly for security research only.")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        return 1
    except Exception as e:
        print(f"\nError during scan: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
