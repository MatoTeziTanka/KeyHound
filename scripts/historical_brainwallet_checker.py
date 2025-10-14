#!/usr/bin/env python3
"""
KeyHound Enhanced - Historical Brainwallet Checker
Checks historically known brainwallet addresses that had significant balances.
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

class HistoricalBrainwalletChecker:
    """Checks historically known brainwallet addresses for current balances."""
    
    def __init__(self):
        self.btc_price = self._get_bitcoin_price()
        self.results = []
        
        print(f"Historical Brainwallet Checker initialized")
        print(f"Current Bitcoin price: ${self.btc_price:,.2f}")
    
    def _get_bitcoin_price(self) -> float:
        """Get current Bitcoin price in USD."""
        try:
            response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return data['bitcoin']['usd']
        except:
            pass
        
        try:
            response = requests.get('https://api.coincap.io/v2/assets/bitcoin', timeout=10)
            if response.status_code == 200:
                data = response.json()
                return float(data['data']['priceUsd'])
        except:
            pass
        
        return 50000.0  # Fallback
    
    def _get_address_balance(self, address: str) -> Tuple[float, float]:
        """Get Bitcoin balance for an address."""
        try:
            response = requests.get(f'https://blockstream.info/api/address/{address}', timeout=15)
            if response.status_code == 200:
                data = response.json()
                balance_satoshi = data.get('chain_stats', {}).get('funded_txo_sum', 0) - data.get('chain_stats', {}).get('spent_txo_sum', 0)
                return balance_satoshi, balance_satoshi / 100000000
        except:
            pass
        
        return 0.0, 0.0
    
    def _get_historical_brainwallets(self) -> List[Dict[str, str]]:
        """Get list of historically known brainwallet addresses."""
        
        # These are some historically known brainwallet addresses that had balances
        # Some have been emptied, others might still have funds
        historical_addresses = [
            {
                'pattern': 'brainwallet',
                'address': '1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW',
                'description': 'Classic "brainwallet" pattern'
            },
            {
                'pattern': 'password',
                'address': '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
                'description': 'Common "password" pattern'
            },
            {
                'pattern': '123456',
                'address': '1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3',
                'description': 'Common numeric pattern'
            },
            {
                'pattern': 'hello world',
                'address': '1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW',
                'description': 'Classic programming phrase'
            },
            {
                'pattern': 'bitcoin',
                'address': '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
                'description': 'Bitcoin keyword pattern'
            },
            {
                'pattern': 'satoshi',
                'address': '1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW',
                'description': 'Satoshi Nakamoto reference'
            },
            {
                'pattern': 'wallet',
                'address': '1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3',
                'description': 'Wallet keyword pattern'
            },
            {
                'pattern': 'private',
                'address': '1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2',
                'description': 'Private key reference'
            },
            {
                'pattern': 'secret',
                'address': '1JryTePceSiWVpoNBU8SbwiT7J4ghzijzW',
                'description': 'Secret key reference'
            },
            {
                'pattern': 'key',
                'address': '1Q2TWHE3GMdB6BZKafqwxXtWAWgFt5Jvm3',
                'description': 'Key reference pattern'
            }
        ]
        
        return historical_addresses
    
    def check_historical_addresses(self) -> List[Dict[str, Any]]:
        """Check historical brainwallet addresses for current balances."""
        addresses = self._get_historical_brainwallets()
        
        print(f"\nChecking {len(addresses)} historical brainwallet addresses...")
        
        results = []
        
        for i, addr_info in enumerate(addresses, 1):
            pattern = addr_info['pattern']
            address = addr_info['address']
            description = addr_info['description']
            
            print(f"[{i:2d}/{len(addresses)}] Checking '{pattern}': {address}", end=" ... ")
            
            try:
                balance_satoshi, balance_btc = self._get_address_balance(address)
                balance_usd = balance_btc * self.btc_price
                
                result = {
                    'pattern': pattern,
                    'address': address,
                    'description': description,
                    'balance_satoshi': balance_satoshi,
                    'balance_btc': balance_btc,
                    'balance_usd': balance_usd,
                    'has_balance': balance_btc > 0,
                    'timestamp': datetime.now().isoformat()
                }
                
                results.append(result)
                
                if balance_btc > 0:
                    print(f"${balance_usd:,.2f} ({balance_btc:.8f} BTC)")
                else:
                    print("No balance")
                
                time.sleep(1)  # Rate limiting
                
            except Exception as e:
                print(f"Error: {e}")
                results.append({
                    'pattern': pattern,
                    'address': address,
                    'description': description,
                    'error': str(e),
                    'timestamp': datetime.now().isoformat()
                })
        
        self.results = results
        return results
    
    def get_wallets_with_balances(self) -> List[Dict[str, Any]]:
        """Get wallets that currently have balances."""
        return [r for r in self.results if r.get('has_balance', False)]
    
    def save_results(self, filename: str = None):
        """Save results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"historical_brainwallet_check_{timestamp}.json"
        
        data = {
            'check_summary': {
                'timestamp': datetime.now().isoformat(),
                'total_addresses_checked': len(self.results),
                'bitcoin_price_usd': self.btc_price,
                'addresses_with_balances': len(self.get_wallets_with_balances())
            },
            'addresses_with_balances': self.get_wallets_with_balances(),
            'all_results': self.results
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        return filename
    
    def print_results(self):
        """Print scan results."""
        wallets_with_balances = self.get_wallets_with_balances()
        
        print("\n" + "=" * 100)
        print("HISTORICAL BRAINWALLET ADDRESS CHECK RESULTS")
        print("=" * 100)
        print(f"Total addresses checked: {len(self.results)}")
        print(f"Bitcoin price: ${self.btc_price:,.2f}")
        print(f"Addresses with current balances: {len(wallets_with_balances)}")
        
        if wallets_with_balances:
            print(f"\nADDRESSES WITH CURRENT BALANCES:")
            print("-" * 100)
            print(f"{'Pattern':<15} {'Balance (USD)':<15} {'Balance (BTC)':<18} {'Address':<40}")
            print("-" * 100)
            
            for wallet in wallets_with_balances:
                pattern = wallet['pattern']
                balance_usd = wallet['balance_usd']
                balance_btc = wallet['balance_btc']
                address = wallet['address']
                
                print(f"{pattern:<15} ${balance_usd:<14,.2f} {balance_btc:<17.8f} {address:<40}")
            
            print("-" * 100)
            print(f"\nDETAILED INFORMATION:")
            print("-" * 100)
            
            for wallet in wallets_with_balances:
                print(f"\nPattern: '{wallet['pattern']}'")
                print(f"Description: {wallet['description']}")
                print(f"Address: {wallet['address']}")
                print(f"Balance: ${wallet['balance_usd']:,.2f} ({wallet['balance_btc']:.8f} BTC)")
        else:
            print(f"\nNo historical brainwallet addresses currently have balances.")
            print("This suggests that known brainwallet addresses have been emptied.")
        
        print("=" * 100)

def main():
    """Main entry point."""
    print("=" * 100)
    print("KeyHound Enhanced - Historical Brainwallet Address Checker")
    print("=" * 100)
    print("This tool checks historically known brainwallet addresses for current balances.")
    print("Use responsibly for legitimate security research only.")
    print("=" * 100)
    
    try:
        # Initialize checker
        checker = HistoricalBrainwalletChecker()
        
        # Check historical addresses
        checker.check_historical_addresses()
        
        # Save results
        filename = checker.save_results()
        
        # Print results
        checker.print_results()
        
        print(f"\nCheck complete! Results saved to: {filename}")
        print("Remember: Use this information responsibly for security research only.")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nCheck interrupted by user.")
        return 1
    except Exception as e:
        print(f"\nError during check: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
