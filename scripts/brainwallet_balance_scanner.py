#!/usr/bin/env python3
"""
KeyHound Enhanced - Brainwallet Balance Scanner
Scans brainwallet addresses for real Bitcoin balances and filters by value.
"""

import os
import sys
import time
import json
import requests
from pathlib import Path
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime

# Add KeyHound root to sys.path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

class BitcoinBalanceScanner:
    """Scans Bitcoin addresses for real balances using blockchain APIs."""
    
    def __init__(self, min_balance_usd: float = 100.0):
        self.min_balance_usd = min_balance_usd
        self.btc_price = self._get_bitcoin_price()
        self.results = []
        self.scanned_count = 0
        self.found_balances = []
        
        print(f"Bitcoin Balance Scanner initialized")
        print(f"Minimum balance threshold: ${min_balance_usd}")
        print(f"Current Bitcoin price: ${self.btc_price:,.2f}")
    
    def _get_bitcoin_price(self) -> float:
        """Get current Bitcoin price in USD."""
        try:
            # Try CoinGecko API first
            response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['bitcoin']['usd']
        except:
            pass
        
        try:
            # Fallback to CoinCap API
            response = requests.get('https://api.coincap.io/v2/assets/bitcoin', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return float(data['data']['priceUsd'])
        except:
            pass
        
        # Default fallback price
        print("Warning: Could not fetch Bitcoin price, using $50,000 as fallback")
        return 50000.0
    
    def _get_address_balance(self, address: str) -> Tuple[float, float]:
        """
        Get Bitcoin balance for an address.
        Returns (balance_satoshi, balance_btc)
        """
        try:
            # Try multiple APIs for reliability
            apis = [
                f"https://blockstream.info/api/address/{address}",
                f"https://api.blockcypher.com/v1/btc/main/addrs/{address}/balance",
                f"https://blockchain.info/q/addressbalance/{address}"
            ]
            
            for api_url in apis:
                try:
                    response = requests.get(api_url, timeout=10)
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
                
                except Exception as e:
                    continue
            
            return 0.0, 0.0
            
        except Exception as e:
            print(f"Error checking balance for {address}: {e}")
            return 0.0, 0.0
    
    def scan_brainwallet_patterns(self, patterns: List[str]) -> List[Dict[str, Any]]:
        """Scan brainwallet patterns for balances."""
        print(f"\nScanning {len(patterns)} brainwallet patterns...")
        print("This may take a while due to API rate limits...")
        
        results = []
        
        for i, pattern in enumerate(patterns, 1):
            print(f"Scanning {i}/{len(patterns)}: '{pattern}'", end=" ... ")
            
            try:
                # Generate brainwallet address
                from core.simple_keyhound import SimpleKeyHound
                keyhound = SimpleKeyHound(verbose=False)
                
                # Test this pattern
                brainwallet_results = keyhound.test_brainwallet_security([pattern])
                
                if brainwallet_results:
                    result = brainwallet_results[0]
                    address = result.get('address')
                    private_key = result.get('private_key')
                    
                    if address:
                        # Check balance
                        balance_satoshi, balance_btc = self._get_address_balance(address)
                        balance_usd = balance_btc * self.btc_price
                        
                        result_data = {
                            'pattern': pattern,
                            'address': address,
                            'private_key': private_key,
                            'balance_satoshi': balance_satoshi,
                            'balance_btc': balance_btc,
                            'balance_usd': balance_usd,
                            'meets_threshold': balance_usd >= self.min_balance_usd,
                            'timestamp': datetime.now().isoformat()
                        }
                        
                        results.append(result_data)
                        self.scanned_count += 1
                        
                        if balance_usd > 0:
                            print(f"Balance: ${balance_usd:,.2f} ({balance_btc:.8f} BTC)")
                            if balance_usd >= self.min_balance_usd:
                                self.found_balances.append(result_data)
                                print(f"  *** FOUND BALANCE >= ${self.min_balance_usd} ***")
                        else:
                            print("No balance")
                    else:
                        print("Failed to generate address")
                else:
                    print("Failed to test pattern")
                
                # Rate limiting - be respectful to APIs
                time.sleep(1)
                
            except Exception as e:
                print(f"Error: {e}")
                continue
        
        self.results = results
        return results
    
    def get_high_value_wallets(self) -> List[Dict[str, Any]]:
        """Get wallets with balances >= minimum threshold, sorted by balance."""
        high_value = [r for r in self.results if r['meets_threshold']]
        return sorted(high_value, key=lambda x: x['balance_usd'], reverse=True)
    
    def save_results(self, filename: str = None):
        """Save scan results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"brainwallet_scan_results_{timestamp}.json"
        
        data = {
            'scan_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_patterns_scanned': self.scanned_count,
                'min_balance_threshold_usd': self.min_balance_usd,
                'bitcoin_price_usd': self.btc_price,
                'high_value_wallets_found': len(self.found_balances)
            },
            'high_value_wallets': self.get_high_value_wallets(),
            'all_results': self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        return filename
    
    def print_summary(self):
        """Print scan summary."""
        high_value = self.get_high_value_wallets()
        
        print("\n" + "=" * 80)
        print("BRAINWALLET BALANCE SCAN SUMMARY")
        print("=" * 80)
        print(f"Total patterns scanned: {self.scanned_count}")
        print(f"Minimum balance threshold: ${self.min_balance_usd}")
        print(f"Bitcoin price: ${self.btc_price:,.2f}")
        print(f"High-value wallets found: {len(high_value)}")
        
        if high_value:
            print(f"\nHIGH-VALUE WALLETS (${self.min_balance_usd}+):")
            print("-" * 80)
            for i, wallet in enumerate(high_value, 1):
                print(f"{i:2d}. Pattern: '{wallet['pattern']}'")
                print(f"    Address: {wallet['address']}")
                print(f"    Balance: ${wallet['balance_usd']:,.2f} ({wallet['balance_btc']:.8f} BTC)")
                print(f"    Private Key: {wallet['private_key']}")
                print()
        else:
            print(f"\nNo wallets found with balance >= ${self.min_balance_usd}")
        
        print("=" * 80)

def get_comprehensive_brainwallet_patterns() -> List[str]:
    """Get comprehensive list of brainwallet patterns to scan."""
    
    # Common passwords and patterns
    common_passwords = [
        "password", "123456", "qwerty", "abc123", "password123", "admin", "letmein",
        "welcome", "monkey", "1234567890", "password1", "qwerty123", "dragon",
        "master", "hello", "freedom", "whatever", "qazwsx", "trustno1", "654321",
        "jordan23", "harley", "password1", "hunter", "hunter2", "ranger", "jordan",
        "jennifer", "zxcvbn", "asdfgh", "123123", "qwertyuiop", "solo", "princess",
        "daniel", "mustang", "batman", "summer", "iloveyou", "ashley", "fuckyou",
        "000000", "tigger", "sunshine", "charlie", "hockey", "rangers", "jordan23",
        "hannah", "michelle", "andrew", "love", "pepper", "shadow", "jordan",
        "michael", "blazer", "ferrari", "matrix", "guitar", "pussy", "2112",
        "tiffany", "jessica", "daniel", "banana", "chelsea", "biteme", "stella",
        "hokey", "lorena", "bitch", "panties", "soccer", "hockey", "killer",
        "george", "sexy", "andrew", "charlie", "superman", "asshole", "fuckyou",
        "dallas", "jessica", "panties", "pepper", "1234", "12345", "123456",
        "1234567", "12345678", "123456789", "1234567890"
    ]
    
    # Bitcoin-related patterns
    bitcoin_patterns = [
        "bitcoin", "btc", "satoshi", "nakamoto", "blockchain", "crypto", "cryptocurrency",
        "wallet", "private", "key", "secret", "password", "passphrase", "seed",
        "mnemonic", "recovery", "backup", "security", "encryption", "hash",
        "mining", "miner", "pool", "exchange", "trading", "hodl", "hodler",
        "bull", "bear", "market", "price", "value", "coin", "token", "altcoin",
        "ethereum", "eth", "litecoin", "ltc", "dogecoin", "doge", "ripple", "xrp"
    ]
    
    # Common phrases and words
    common_phrases = [
        "hello world", "test", "example", "sample", "demo", "password123",
        "mypassword", "secret123", "private123", "key123", "wallet123",
        "bitcoin123", "crypto123", "money", "cash", "rich", "wealthy",
        "millionaire", "billionaire", "invest", "investment", "profit",
        "earn", "income", "salary", "work", "job", "business", "company"
    ]
    
    # Date patterns
    date_patterns = [
        "2024", "2025", "2023", "2022", "2021", "2020", "2019", "2018",
        "january", "february", "march", "april", "may", "june", "july",
        "august", "september", "october", "november", "december",
        "jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep",
        "oct", "nov", "dec", "monday", "tuesday", "wednesday", "thursday",
        "friday", "saturday", "sunday", "mon", "tue", "wed", "thu", "fri",
        "sat", "sun"
    ]
    
    # Combine all patterns
    all_patterns = list(set(
        common_passwords + 
        bitcoin_patterns + 
        common_phrases + 
        date_patterns
    ))
    
    return all_patterns

def main():
    """Main entry point for brainwallet balance scanning."""
    print("=" * 80)
    print("KeyHound Enhanced - Brainwallet Balance Scanner")
    print("=" * 80)
    print("This tool scans common brainwallet patterns for real Bitcoin balances.")
    print("Use responsibly and only for legitimate security research.")
    print("=" * 80)
    
    try:
        # Get patterns to scan
        print("Loading brainwallet patterns...")
        patterns = get_comprehensive_brainwallet_patterns()
        print(f"Loaded {len(patterns)} patterns to scan")
        
        # Initialize scanner
        min_balance = 100.0  # $100 minimum
        scanner = BitcoinBalanceScanner(min_balance_usd=min_balance)
        
        # Scan patterns
        results = scanner.scan_brainwallet_patterns(patterns)
        
        # Save results
        filename = scanner.save_results()
        
        # Print summary
        scanner.print_summary()
        
        print(f"\nScan complete! Results saved to: {filename}")
        print("Use this information responsibly for security research only.")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        return 1
    except Exception as e:
        print(f"\nError during scan: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
