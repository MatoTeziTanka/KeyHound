#!/usr/bin/env python3
"""
KeyHound Enhanced - Focused Brainwallet Scanner
Focuses specifically on the high-value wallet: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2
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

class FocusedBrainwalletScanner:
    """Focused scanner for the specific high-value brainwallet address."""
    
    def __init__(self):
        self.btc_price = self._get_bitcoin_price()
        self.target_address = "1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2"
        self.target_patterns = ["password", "bitcoin", "private"]
        
        print(f"Focused Brainwallet Scanner initialized")
        print(f"Target Address: {self.target_address}")
        print(f"Target Patterns: {', '.join(self.target_patterns)}")
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
    
    def _get_address_transactions(self, address: str) -> List[Dict]:
        """Get recent transaction history for the address."""
        try:
            response = requests.get(f"https://blockstream.info/api/address/{address}/txs", timeout=15)
            if response.status_code == 200:
                return response.json()[:10]  # Last 10 transactions
        except:
            pass
        return []
    
    def _generate_brainwallet_address(self, pattern: str) -> Tuple[str, str]:
        """Generate Bitcoin address from brainwallet pattern."""
        try:
            import hashlib
            
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
    
    def verify_target_wallet(self) -> Dict[str, Any]:
        """Verify and analyze the target high-value wallet."""
        print(f"\nAnalyzing target wallet: {self.target_address}")
        print("=" * 80)
        
        # Check current balance
        print("Checking current balance...")
        balance_satoshi, balance_btc = self._get_address_balance(self.target_address)
        balance_usd = balance_btc * self.btc_price
        
        print(f"Current Balance: {balance_btc:.8f} BTC (${balance_usd:,.2f} USD)")
        
        # Verify patterns generate the correct address
        print(f"\nVerifying brainwallet patterns...")
        pattern_results = []
        
        for pattern in self.target_patterns:
            print(f"Testing pattern: '{pattern}'", end=" ... ")
            
            address, private_key = self._generate_brainwallet_address(pattern)
            
            if address == self.target_address:
                print("✓ MATCHES TARGET ADDRESS")
                pattern_results.append({
                    'pattern': pattern,
                    'address': address,
                    'private_key': private_key,
                    'matches_target': True
                })
            else:
                print(f"✗ Different address: {address}")
                pattern_results.append({
                    'pattern': pattern,
                    'address': address,
                    'private_key': private_key,
                    'matches_target': False
                })
        
        # Get transaction history
        print(f"\nFetching transaction history...")
        transactions = self._get_address_transactions(self.target_address)
        
        # Analyze transaction data
        total_received = 0
        total_sent = 0
        transaction_count = len(transactions)
        
        for tx in transactions:
            # This is a simplified analysis - in reality you'd need to parse inputs/outputs properly
            if 'status' in tx and tx['status'].get('confirmed'):
                # Add logic to calculate received/sent amounts
                pass
        
        result = {
            'target_address': self.target_address,
            'current_balance_satoshi': balance_satoshi,
            'current_balance_btc': balance_btc,
            'current_balance_usd': balance_usd,
            'bitcoin_price_usd': self.btc_price,
            'pattern_verification': pattern_results,
            'transaction_count': transaction_count,
            'recent_transactions': transactions[:5],  # Last 5 transactions
            'scan_timestamp': datetime.now().isoformat()
        }
        
        return result
    
    def monitor_wallet_activity(self, duration_minutes: int = 60) -> Dict[str, Any]:
        """Monitor the wallet for activity changes."""
        print(f"\nMonitoring wallet activity for {duration_minutes} minutes...")
        print("Checking balance every 30 seconds...")
        
        initial_balance_satoshi, initial_balance_btc = self._get_address_balance(self.target_address)
        initial_balance_usd = initial_balance_btc * self.btc_price
        
        print(f"Initial balance: {initial_balance_btc:.8f} BTC (${initial_balance_usd:,.2f} USD)")
        
        monitoring_data = []
        check_interval = 30  # seconds
        total_checks = (duration_minutes * 60) // check_interval
        
        for i in range(total_checks):
            try:
                balance_satoshi, balance_btc = self._get_address_balance(self.target_address)
                balance_usd = balance_btc * self.btc_price
                
                check_data = {
                    'timestamp': datetime.now().isoformat(),
                    'balance_btc': balance_btc,
                    'balance_usd': balance_usd,
                    'balance_change': balance_usd - initial_balance_usd
                }
                
                monitoring_data.append(check_data)
                
                if balance_usd != initial_balance_usd:
                    print(f"⚠️  BALANCE CHANGE DETECTED!")
                    print(f"   New balance: {balance_btc:.8f} BTC (${balance_usd:,.2f} USD)")
                    print(f"   Change: ${balance_usd - initial_balance_usd:,.2f}")
                    break
                else:
                    print(f"[{i+1}/{total_checks}] Balance unchanged: ${balance_usd:,.2f}")
                
                time.sleep(check_interval)
                
            except KeyboardInterrupt:
                print("\nMonitoring stopped by user.")
                break
            except Exception as e:
                print(f"Error during monitoring: {e}")
                time.sleep(check_interval)
        
        return {
            'initial_balance_usd': initial_balance_usd,
            'final_balance_usd': monitoring_data[-1]['balance_usd'] if monitoring_data else initial_balance_usd,
            'total_change_usd': (monitoring_data[-1]['balance_usd'] - initial_balance_usd) if monitoring_data else 0,
            'monitoring_duration_minutes': duration_minutes,
            'checks_performed': len(monitoring_data),
            'monitoring_data': monitoring_data
        }
    
    def save_results(self, verification_result: Dict, monitoring_result: Dict = None, filename: str = None):
        """Save scan results to JSON file."""
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"focused_brainwallet_scan_{timestamp}.json"
        
        data = {
            'scan_summary': {
                'target_address': self.target_address,
                'target_patterns': self.target_patterns,
                'scan_timestamp': datetime.now().isoformat(),
                'bitcoin_price_usd': self.btc_price
            },
            'wallet_verification': verification_result,
            'activity_monitoring': monitoring_result
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        print(f"\nResults saved to: {filename}")
        return filename
    
    def print_summary(self, verification_result: Dict, monitoring_result: Dict = None):
        """Print scan summary."""
        print("\n" + "=" * 100)
        print("FOCUSED BRAINWALLET SCAN SUMMARY")
        print("=" * 100)
        
        print(f"Target Address: {self.target_address}")
        print(f"Current Balance: {verification_result['current_balance_btc']:.8f} BTC (${verification_result['current_balance_usd']:,.2f} USD)")
        print(f"Bitcoin Price: ${self.btc_price:,.2f}")
        
        print(f"\nPattern Verification:")
        for pattern_result in verification_result['pattern_verification']:
            pattern = pattern_result['pattern']
            matches = pattern_result['matches_target']
            status = "✓ MATCHES" if matches else "✗ DIFFERENT"
            print(f"  '{pattern}': {status}")
        
        if verification_result['pattern_verification'][0]['matches_target']:
            print(f"\n🎯 CONFIRMED: The '{verification_result['pattern_verification'][0]['pattern']}' pattern generates the target address!")
            print(f"Private Key: {verification_result['pattern_verification'][0]['private_key']}")
        
        print(f"\nTransaction History: {verification_result['transaction_count']} transactions found")
        
        if monitoring_result:
            print(f"\nActivity Monitoring:")
            print(f"  Monitoring Duration: {monitoring_result['monitoring_duration_minutes']} minutes")
            print(f"  Checks Performed: {monitoring_result['checks_performed']}")
            print(f"  Balance Change: ${monitoring_result['total_change_usd']:,.2f}")
            
            if monitoring_result['total_change_usd'] != 0:
                print(f"  ⚠️  WALLET ACTIVITY DETECTED!")
            else:
                print(f"  ✓ No activity detected during monitoring period")
        
        print("=" * 100)

def main():
    """Main entry point."""
    print("=" * 100)
    print("KeyHound Enhanced - Focused Brainwallet Scanner")
    print("=" * 100)
    print("Focusing on the high-value wallet: 1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2")
    print("Target patterns: password, bitcoin, private")
    print("Use responsibly for legitimate security research only.")
    print("=" * 100)
    
    try:
        # Initialize scanner
        scanner = FocusedBrainwalletScanner()
        
        # Verify target wallet
        verification_result = scanner.verify_target_wallet()
        
        # Ask user if they want to monitor for activity
        print(f"\nWould you like to monitor the wallet for activity changes? (y/n): ", end="")
        monitor_choice = input().lower().strip()
        
        monitoring_result = None
        if monitor_choice in ['y', 'yes']:
            duration = 60  # Default 60 minutes
            print(f"Enter monitoring duration in minutes (default 60): ", end="")
            try:
                duration = int(input().strip())
            except:
                duration = 60
            
            monitoring_result = scanner.monitor_wallet_activity(duration)
        
        # Save results
        filename = scanner.save_results(verification_result, monitoring_result)
        
        # Print summary
        scanner.print_summary(verification_result, monitoring_result)
        
        print(f"\nFocused scan complete! Results saved to: {filename}")
        print("Ready for live KeyHound testing!")
        
        return 0
        
    except KeyboardInterrupt:
        print("\nScan interrupted by user.")
        return 1
    except Exception as e:
        print(f"\nError during scan: {e}")
        return 1

if __name__ == '__main__':
    sys.exit(main())
